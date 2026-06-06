-- Fix login + RLS: administrador principal reconocido por JWT Auth
-- Ejecutar si el login sigue bloqueado o el dashboard no carga ODS.

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
    set role = 'admin', active = true;

  select * into v_row from public.ops_technicians
  where lower(email) = 'joel.duran.mendoza@me.com';

  return jsonb_build_object('ok', true, 'role', coalesce(v_row.role, 'admin'));
end;
$$;

grant execute on function public.ensure_primary_admin_access() to authenticated;

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
      select 1 from public.ops_technicians t
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
  select
    lower(trim(coalesce(auth.jwt() ->> 'email', ''))) = 'joel.duran.mendoza@me.com'
    or exists (
      select 1 from public.ops_technicians t
      where lower(t.email) = lower(coalesce(auth.jwt() ->> 'email', ''))
        and t.active = true and t.role = 'admin'
    );
$$;
