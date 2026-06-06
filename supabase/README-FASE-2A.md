# macWave OPS — FASE 2A (despliegue Supabase)

## Orden de ejecución

1. Abrir **Supabase → SQL Editor**
2. Ejecutar en orden:
   - `migrations/20260528120000_ops_phase2_client_visibility.sql` (si no se aplicó)
   - `migrations/20260528140000_ops_phase2a_hardening.sql`
3. Verificar en **Authentication** que cada técnico tenga usuario activo
4. Verificar tabla `ops_technicians` (emails autorizados)

## Validación rápida

```sql
-- Debe devolver 1 fila (con token de prueba)
select * from get_public_ods_tracking(p_token := (select tracking_token from ordenes_servicio limit 1));

-- Anon NO debe leer tabla base
-- (probar desde cliente con rol anon en SQL o desde status-ods)
```

## QR legacy

- URLs con `?folio=` siguen funcionando (rate limit más estricto)
- URLs nuevas con `?token=` son el estándar desde generador ODS

## Bootstrap administrador principal

Si el login falla con “no tiene acceso al panel técnico”, ejecutar:

`migrations/20260528160000_ensure_primary_admin_bootstrap.sql`

Luego `joel.duran.mendoza@me.com` se auto-registra en `ops_technicians` al iniciar sesión (RPC + fallback RLS).

## FASE 2B — Activity UI

- Panel **Activity** en `dashboard-ods.html` (sidebar)
- Lee `ops_audit_log` con paginación (40 por página)
- Archivos: `js/dashboard/audit-log.js`, `css/ops-audit.css`

## Rollback

Si el panel deja de cargar ODS: revisar que el usuario autenticado exista en `ops_technicians` con `active = true`.
