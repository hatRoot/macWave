-- Backfill opcional: copiar eventos visibles desde notas JSON a client_timeline
-- Ejecutar UNA vez después de FASE 2A si hay ODS legacy sin client_timeline poblado.
-- Nota: el filtrado fino [INTERNO] se aplica en app; aquí solo copia el array parseable.

update public.ordenes_servicio o
set client_timeline = coalesce(
  (
    select jsonb_agg(elem)
    from jsonb_array_elements(
      case
        when o.notas ~ '^\s*\[' then o.notas::jsonb
        else '[]'::jsonb
      end
    ) elem
    where coalesce((elem->>'internal')::boolean, false) = false
      and coalesce((elem->>'clientVisible')::boolean, true) = true
  ),
  '[]'::jsonb
)
where (client_timeline is null or client_timeline = '[]'::jsonb)
  and o.notas is not null
  and o.notas ~ '^\s*\[';
