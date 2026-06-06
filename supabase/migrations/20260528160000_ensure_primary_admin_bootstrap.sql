-- Bootstrap automático del administrador principal (sin intervención manual)
-- Solo: joel.duran.mendoza@me.com

create or replace function public.ensure_primary_admin_access()
returns jsonb
language plpgsql
security definer
set search_path = public
as $$
declare
  v_jwt_email text := lower(trim(coalesce(auth.jwt() ->> 'email', '')));
  v_row public.ops_technicians%rowtype;
begin
  if v_jwt_email <> 'joel.duran.mendoza@me.com' then
    return jsonb_build_object('ok', false, 'reason', 'not_primary_admin');
  end if;

  insert into public.ops_technicians (email, role, active)
  values ('joel.duran.mendoza@me.com', 'admin', true)
  on conflict (email) do update
    set role = 'admin',
        active = true;

  select * into v_row
  from public.ops_technicians
  where lower(email) = 'joel.duran.mendoza@me.com';

  if not found or v_row.active is not true then
    return jsonb_build_object('ok', false, 'reason', 'bootstrap_failed');
  end if;

  return jsonb_build_object(
    'ok', true,
    'role', v_row.role,
    'email', v_row.email,
    'bootstrapped', true
  );
end;
$$;

grant execute on function public.ensure_primary_admin_access() to authenticated;

-- Fallback si el RPC aún no está desplegado: el admin puede insertar/actualizar solo su fila
drop policy if exists "ops_primary_admin_bootstrap_insert" on public.ops_technicians;
create policy "ops_primary_admin_bootstrap_insert"
  on public.ops_technicians
  for insert
  to authenticated
  with check (
    lower(email) = 'joel.duran.mendoza@me.com'
    and lower(auth.jwt() ->> 'email') = 'joel.duran.mendoza@me.com'
  );

drop policy if exists "ops_primary_admin_bootstrap_update" on public.ops_technicians;
create policy "ops_primary_admin_bootstrap_update"
  on public.ops_technicians
  for update
  to authenticated
  using (
    lower(email) = 'joel.duran.mendoza@me.com'
    and lower(auth.jwt() ->> 'email') = 'joel.duran.mendoza@me.com'
  )
  with check (
    lower(email) = 'joel.duran.mendoza@me.com'
    and active = true
  );

comment on function public.ensure_primary_admin_access is
  'Auto-registra al administrador principal en ops_technicians tras login Auth';

-- Permitir operaciones RLS al admin principal aunque ops_technicians aún no tenga fila
create or replace function public.ops_is_technician()
returns boolean
language sql
stable
security definer
set search_path = public
as $$
  select
    lower(trim(coalesce(auth.jwt() ->> 'email', ''))) = 'joel.duran.mendoza@me.com'
    or exists (
      select 1
      from public.ops_technicians t
      where lower(t.email) = lower(coalesce(auth.jwt() ->> 'email', ''))
        and t.active = true
    );
$$;

create or replace function public.ops_is_admin()
returns boolean
language sql
security definer
set search_path = public
as $$
  select
    lower(trim(coalesce(auth.jwt() ->> 'email', ''))) = 'joel.duran.mendoza@me.com'
    or exists (
      select 1
      from public.ops_technicians t
      where lower(t.email) = lower(coalesce(auth.jwt() ->> 'email', ''))
        and t.active = true
        and t.role = 'admin'
    );
$$;
