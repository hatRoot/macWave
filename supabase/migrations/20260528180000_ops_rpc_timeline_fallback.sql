-- macWave OPS — Fallback para client_timeline en get_public_ods_tracking
-- Si el client_timeline está vacío (en registros anteriores a FASE 2A),
-- el RPC reconstruye el timeline público a partir de notas JSON sobre la marcha.

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
    'timeline', case
      when o.client_timeline is not null and o.client_timeline <> '[]'::jsonb then o.client_timeline
      else coalesce(
        (
          select jsonb_agg(
            jsonb_build_object(
              'type', coalesce(elem->>'type', elem->>'status', 'update'),
              'status', coalesce(elem->>'status', elem->>'type', 'update'),
              'message', coalesce(elem->>'message', elem->>'text', ''),
              'timestamp', coalesce(elem->>'timestamp', elem->>'date', ''),
              'photos', case 
                when elem->'photos' is not null then elem->'photos'
                when elem->'img' is not null and elem->>'img' <> '' then jsonb_build_array(elem->'img')
                else '[]'::jsonb
              end,
              'clientVisible', true
            )
          )
          from jsonb_array_elements(
            case
              when o.notas ~ '^\s*\[' then o.notas::jsonb
              else '[]'::jsonb
            end
          ) elem
          where coalesce((elem->>'internal')::boolean, false) = false
            and coalesce((elem->>'clientVisible')::boolean, true) = true
            and coalesce(elem->>'text', '') not ilike '[INTERNO]%'
        ),
        '[]'::jsonb
      )
    end,
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

grant execute on function public.get_public_ods_tracking(text, text) to anon, authenticated;
