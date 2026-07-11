-- macWave OPS — Storage: bucket ods-photos
-- Crea el bucket de fotos de órdenes de servicio y configura las políticas RLS de Storage.
-- Ejecutar en Supabase SQL Editor ANTES de intentar subir fotos desde el dashboard.

-- ---------------------------------------------------------------------------
-- 1. Crear bucket ods-photos (público: las URLs son legibles sin auth para mostrar en cliente)
-- ---------------------------------------------------------------------------
insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values (
  'ods-photos',
  'ods-photos',
  true,
  5242880,  -- 5 MB por archivo
  array['image/jpeg', 'image/png', 'image/webp', 'image/gif']
)
on conflict (id) do update
  set public = true,
      file_size_limit = 5242880,
      allowed_mime_types = array['image/jpeg', 'image/png', 'image/webp', 'image/gif'];

-- ---------------------------------------------------------------------------
-- 2. Política: técnicos autenticados pueden SUBIR (INSERT) fotos
-- ---------------------------------------------------------------------------
drop policy if exists "ops_tech_upload_photos" on storage.objects;
create policy "ops_tech_upload_photos"
  on storage.objects
  for insert
  to authenticated
  with check (
    bucket_id = 'ods-photos'
    and public.ops_is_technician()
  );

-- ---------------------------------------------------------------------------
-- 3. Política: técnicos autenticados pueden ACTUALIZAR fotos
-- ---------------------------------------------------------------------------
drop policy if exists "ops_tech_update_photos" on storage.objects;
create policy "ops_tech_update_photos"
  on storage.objects
  for update
  to authenticated
  using (
    bucket_id = 'ods-photos'
    and public.ops_is_technician()
  );

-- ---------------------------------------------------------------------------
-- 4. Política: técnicos autenticados pueden ELIMINAR fotos
-- ---------------------------------------------------------------------------
drop policy if exists "ops_tech_delete_photos" on storage.objects;
create policy "ops_tech_delete_photos"
  on storage.objects
  for delete
  to authenticated
  using (
    bucket_id = 'ods-photos'
    and public.ops_is_technician()
  );

-- ---------------------------------------------------------------------------
-- 5. Política: LECTURA pública de las fotos (anon + authenticated)
--    Necesario para que el cliente vea las imágenes en status-ods.html
-- ---------------------------------------------------------------------------
drop policy if exists "public_read_ods_photos" on storage.objects;
create policy "public_read_ods_photos"
  on storage.objects
  for select
  to anon, authenticated
  using (bucket_id = 'ods-photos');
