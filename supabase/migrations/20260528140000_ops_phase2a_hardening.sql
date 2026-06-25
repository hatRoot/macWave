-- macWave OPS — FASE 2A: Hardening, RLS, tracking token, audit log
-- Ejecutar en Supabase SQL Editor (staging → producción).

-- ---------------------------------------------------------------------------
-- 1. Columnas de separación cliente / interno
-- ---------------------------------------------------------------------------
alter table public.ordenes_servicio
  add column if not exists client_timeline jsonb not null default '[]'::jsonb;

alter table public.ordenes_servicio
  add column if not exists internal_notes text;

alter table public.ordenes_servicio
  add column if not exists tracking_token text unique;

alter table public.ordenes_servicio
  add column if not exists garantia_hasta date;

create index if not exists idx_ordenes_servicio_folio on public.ordenes_servicio (folio);
create index if not exists idx_ordenes_servicio_serie on public.ordenes_servicio (serie);
create index if not exists idx_ordenes_servicio_tracking_token on public.ordenes_servicio (tracking_token);

-- Tokens para ODS existentes (QR legacy con folio siguen funcionando vía RPC acotado)
update public.ordenes_servicio
set tracking_token = encode(gen_random_bytes(24), 'hex')
where tracking_token is null;

-- ---------------------------------------------------------------------------
-- 2. Técnicos autorizados (reemplaza whitelist en frontend)
-- ---------------------------------------------------------------------------
create table if not exists public.ops_technicians (
  email text primary key,
  role text not null default 'tecnico' check (role in ('tecnico', 'admin')),
  active boolean not null default true,
  created_at timestamptz not null default now()
);

insert into public.ops_technicians (email, role) values
  ('joel.duran.mendoza@me.com', 'admin'),
  ('joel@macwave.com.mx', 'admin'),
  ('contabilidad@macwave.com.mx', 'tecnico'),
  ('contacto@macwave.com.mx', 'tecnico'),
  ('procell.bip@gmail.com', 'tecnico')
on conflict (email) do update set active = true;

-- ---------------------------------------------------------------------------
-- 3. Audit log operativo
-- ---------------------------------------------------------------------------
create table if not exists public.ops_audit_log (
  id uuid primary key default gen_random_uuid(),
  ods_id uuid references public.ordenes_servicio(id) on delete set null,
  folio text,
  action text not null,
  details jsonb not null default '{}'::jsonb,
  actor_email text,
  created_at timestamptz not null default now()
);

create index if not exists idx_ops_audit_log_folio on public.ops_audit_log (folio);
create index if not exists idx_ops_audit_log_ods_id on public.ops_audit_log (ods_id);
create index if not exists idx_ops_audit_log_created_at on public.ops_audit_log (created_at desc);

-- ---------------------------------------------------------------------------
-- 4. Rate limiting (anti-scraping tracking)
-- ---------------------------------------------------------------------------
create table if not exists public.ops_rate_limit (
  id bigserial primary key,
  rate_key text not null,
  action text not null,
  attempted_at timestamptz not null default now()
);

create index if not exists idx_ops_rate_limit_key_action_time
  on public.ops_rate_limit (rate_key, action, attempted_at desc);

-- ---------------------------------------------------------------------------
-- 5. Helpers
-- ---------------------------------------------------------------------------
create or replace function public.ops_is_technician()
returns boolean
language sql
stable
security definer
set search_path = public
as $$
  select exists (
    select 1
    from public.ops_technicians t
    where lower(t.email) = lower(coalesce(auth.jwt() ->> 'email', ''))
      and t.active = true
  );
$$;

create or replace function public.ops_is_admin()
returns boolean
language sql
stable
security definer
set search_path = public
as $$
  select exists (
    select 1
    from public.ops_technicians t
    where lower(t.email) = lower(coalesce(auth.jwt() ->> 'email', ''))
      and t.active = true
      and t.role = 'admin'
  );
$$;

create or replace function public.ops_check_rate_limit(
  p_key text,
  p_action text,
  p_max_attempts int,
  p_window_seconds int
)
returns boolean
language plpgsql
security definer
set search_path = public
as $$
declare
  v_count int;
begin
  delete from public.ops_rate_limit
  where attempted_at < now() - make_interval(secs => p_window_seconds);

  select count(*)::int into v_count
  from public.ops_rate_limit
  where rate_key = p_key
    and action = p_action
    and attempted_at >= now() - make_interval(secs => p_window_seconds);

  if v_count >= p_max_attempts then
    return false;
  end if;

  insert into public.ops_rate_limit (rate_key, action) values (p_key, p_action);
  return true;
end;
$$;

create or replace function public.ops_compute_progress(p_status text)
returns int
language plpgsql
immutable
as $$
begin
  return case coalesce(p_status, 'Recibido')
    when 'Recibido' then 10
    when 'Diagnóstico' then 25
    when 'Espera de aprobación y pago' then 35
    when 'Espera de piezas' then 45
    when 'Reparación' then 65
    when 'Equipo reparado' then 90
    when 'Equipo entregado' then 100
    when 'Equipo sin reparar' then 100
    else 15
  end;
end;
$$;

-- ---------------------------------------------------------------------------
-- 6. RPC tracking público (única puerta para anon)
-- ---------------------------------------------------------------------------
create or replace function public.get_public_ods_tracking(
  p_token text default null,
  p_folio text default null
)
returns setof jsonb
language plpgsql
security definer
set search_path = public
as $$
declare
  v_key text;
  v_max int;
  v_window int;
begin
  v_key := coalesce(nullif(trim(p_token), ''), nullif(trim(p_folio), ''), 'empty');

  if p_token is not null and length(trim(p_token)) > 0 then
    v_max := 60;
    v_window := 3600;
  else
    v_max := 15;
    v_window := 3600;
  end if;

  if not public.ops_check_rate_limit(v_key, 'tracking_lookup', v_max, v_window) then
    raise exception 'Demasiados intentos. Intenta más tarde.'
      using errcode = 'P0001';
  end if;

  return query
  select jsonb_build_object(
    'folio', o.folio,
    'cliente', case
      when o.cliente is null or o.cliente = '' then ''
      else split_part(o.cliente, ' ', 1) || ' ***'
    end,
    'modelo', coalesce(o.proyecto, ''),
    'status', coalesce(o.status, 'Recibido'),
    'progress', public.ops_compute_progress(o.status),
    'fecha', o.fecha,
    'garantia_hasta', o.garantia_hasta,
    'timeline', coalesce(o.client_timeline, '[]'::jsonb),
    'serie_masked', case
      when o.serie is not null and length(o.serie) > 4 then '***' || right(o.serie, 4)
      else null
    end,
    'tracking_token', o.tracking_token
  )
  from public.ordenes_servicio o
  where (
    (p_token is not null and trim(p_token) <> '' and o.tracking_token = trim(p_token))
    or (
      p_folio is not null and trim(p_folio) <> ''
      and o.folio ilike '%' || trim(p_folio) || '%'
    )
  )
  order by o.created_at desc
  limit case when p_token is not null and trim(p_token) <> '' then 1 else 3 end;
end;
$$;

-- Registrar auditoría desde panel técnico
create or replace function public.log_ops_audit(
  p_ods_id uuid,
  p_folio text,
  p_action text,
  p_details jsonb default '{}'::jsonb
)
returns uuid
language plpgsql
security definer
set search_path = public
as $$
declare
  v_id uuid;
  v_email text := coalesce(auth.jwt() ->> 'email', 'sistema');
begin
  if not public.ops_is_technician() then
    raise exception 'No autorizado' using errcode = '42501';
  end if;

  insert into public.ops_audit_log (ods_id, folio, action, details, actor_email)
  values (p_ods_id, p_folio, p_action, coalesce(p_details, '{}'::jsonb), v_email)
  returning id into v_id;

  return v_id;
end;
$$;

-- ---------------------------------------------------------------------------
-- 7. Vista pública (solo lectura vía PostgREST si se necesita; preferir RPC)
-- ---------------------------------------------------------------------------
drop view if exists public.ordenes_servicio_public;
create or replace view public.ordenes_servicio_public as
select
  o.id,
  o.folio,
  split_part(o.cliente, ' ', 1) || ' ***' as cliente,
  coalesce(o.proyecto, '') as modelo,
  coalesce(o.status, 'Recibido') as status,
  public.ops_compute_progress(o.status) as progress,
  o.fecha,
  o.garantia_hasta,
  coalesce(o.client_timeline, '[]'::jsonb) as timeline,
  case
    when o.serie is not null and length(o.serie) > 4 then '***' || right(o.serie, 4)
    else null
  end as serie_masked,
  o.tracking_token,
  o.created_at
from public.ordenes_servicio o;

-- ---------------------------------------------------------------------------
-- 8. RLS — ordenes_servicio
-- ---------------------------------------------------------------------------
alter table public.ordenes_servicio enable row level security;

drop policy if exists "ops_tech_all_ordenes" on public.ordenes_servicio;
create policy "ops_tech_all_ordenes"
  on public.ordenes_servicio
  for all
  to authenticated
  using (public.ops_is_technician())
  with check (public.ops_is_technician());

-- Sin políticas para anon → denegado en tabla base

-- ---------------------------------------------------------------------------
-- 9. RLS — tickets_taller
-- ---------------------------------------------------------------------------
alter table public.tickets_taller enable row level security;

drop policy if exists "ops_tech_all_tickets" on public.tickets_taller;
create policy "ops_tech_all_tickets"
  on public.tickets_taller
  for all
  to authenticated
  using (public.ops_is_technician())
  with check (public.ops_is_technician());

-- ---------------------------------------------------------------------------
-- 10. RLS — ops_technicians, audit, rate_limit
-- ---------------------------------------------------------------------------
alter table public.ops_technicians enable row level security;

drop policy if exists "ops_tech_read_self" on public.ops_technicians;
create policy "ops_tech_read_self"
  on public.ops_technicians
  for select
  to authenticated
  using (lower(email) = lower(auth.jwt() ->> 'email'));

drop policy if exists "ops_admin_manage_tech" on public.ops_technicians;
create policy "ops_admin_manage_tech"
  on public.ops_technicians
  for all
  to authenticated
  using (public.ops_is_admin())
  with check (public.ops_is_admin());

alter table public.ops_audit_log enable row level security;

drop policy if exists "ops_tech_read_audit" on public.ops_audit_log;
create policy "ops_tech_read_audit"
  on public.ops_audit_log
  for select
  to authenticated
  using (public.ops_is_technician());

drop policy if exists "ops_tech_insert_audit" on public.ops_audit_log;
create policy "ops_tech_insert_audit"
  on public.ops_audit_log
  for insert
  to authenticated
  with check (public.ops_is_technician());

-- rate_limit: solo service role / security definer (sin grant anon)

revoke all on public.ops_rate_limit from anon, authenticated;

-- ---------------------------------------------------------------------------
-- 11. Permisos RPC
-- ---------------------------------------------------------------------------
grant execute on function public.get_public_ods_tracking(text, text) to anon, authenticated;
grant execute on function public.log_ops_audit(uuid, text, text, jsonb) to authenticated;
grant execute on function public.ops_is_technician() to authenticated;
grant execute on function public.ops_is_admin() to authenticated;

revoke select on public.ordenes_servicio from anon;
grant select on public.ordenes_servicio_public to anon;

comment on function public.get_public_ods_tracking is
  'Tracking cliente: usar p_token (preferido) o p_folio (legacy, rate limited)';
