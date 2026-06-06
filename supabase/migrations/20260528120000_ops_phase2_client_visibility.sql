-- macWave OPS FASE 2 — visibilidad cliente vs interno
-- Ejecutar en Supabase SQL Editor cuando se valide en staging.

-- Columna dedicada al timeline público (evita filtrar JSON en cliente)
alter table public.ordenes_servicio
  add column if not exists client_timeline jsonb default '[]'::jsonb;

-- Notas internas separadas del historial compartido legacy (notas)
alter table public.ordenes_servicio
  add column if not exists internal_notes text;

-- URL de tracking estable
alter table public.ordenes_servicio
  add column if not exists tracking_token text unique;

create index if not exists idx_ordenes_servicio_folio on public.ordenes_servicio (folio);
create index if not exists idx_ordenes_servicio_serie on public.ordenes_servicio (serie);
create index if not exists idx_ordenes_servicio_tracking_token on public.ordenes_servicio (tracking_token);

-- Vista segura para lectura pública (RLS debe permitir solo esta vista al rol anon)
create or replace view public.ordenes_servicio_public as
select
  id,
  folio,
  cliente,
  serie,
  status,
  fecha,
  created_at,
  coalesce(client_timeline, '[]'::jsonb) as timeline
from public.ordenes_servicio;

comment on view public.ordenes_servicio_public is 'Solo campos expuestos al tracking /status/[folio]';

-- Ejemplo RLS (ajustar según políticas actuales):
-- revoke select on public.ordenes_servicio from anon;
-- grant select on public.ordenes_servicio_public to anon;
