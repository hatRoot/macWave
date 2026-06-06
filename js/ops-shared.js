/**
 * macWave OPS — utilidades compartidas (seguridad, timeline, tracking).
 */
(function (global) {
  const cfg = global.MacWaveSupabaseConfig || {};
  const SUPABASE_URL = cfg.url || 'https://lifxtyhvgnxjjqgbzare.supabase.co';
  const SUPABASE_ANON_KEY = cfg.anonKey || '';

  const STATUS_CONFIG = {
    Recibido: { color: '#FFD60A', clientLabel: 'Recibido' },
    Diagnóstico: { color: '#FFD60A', clientLabel: 'Diagnóstico' },
    'Espera de aprobación y pago': { color: '#FF9F0A', clientLabel: 'Esperando tu aprobación' },
    'Espera de piezas': { color: '#FF9F0A', clientLabel: 'Esperando piezas' },
    Reparación: { color: '#FFD60A', clientLabel: 'Reparación en proceso' },
    'Equipo reparado': { color: '#30D158', clientLabel: 'Listo para entrega' },
    'Equipo entregado': { color: '#30D158', clientLabel: 'Entregado' },
    'Equipo sin reparar': { color: '#FF453A', clientLabel: 'Sin reparación' },
    'Nota General': { color: '#8E8E93', clientLabel: 'Actualización' },
  };

  const CLIENT_TRACKING_STEPS = [
    { key: 'Recibido', label: 'Recibido', icon: '📩' },
    { key: 'Diagnóstico', label: 'Diagnóstico', icon: '🔍' },
    { key: 'Espera de aprobación y pago', label: 'Aprobación', icon: '✋' },
    { key: 'Espera de piezas', label: 'Piezas', icon: '📦' },
    { key: 'Reparación', label: 'Reparación', icon: '🔧' },
    { key: 'Equipo reparado', label: 'Listo', icon: '✅' },
    { key: 'Equipo entregado', label: 'Entregado', icon: '📦' },
  ];

  function createSupabaseClient() {
    if (!global.supabase || !SUPABASE_ANON_KEY) {
      throw new Error('Supabase no disponible');
    }
    return global.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
  }

  function generateTrackingToken() {
    if (global.crypto && crypto.randomUUID) {
      return crypto.randomUUID().replace(/-/g, '');
    }
    const arr = new Uint8Array(24);
    crypto.getRandomValues(arr);
    return Array.from(arr, (b) => b.toString(16).padStart(2, '0')).join('');
  }

  function escapeHtml(value) {
    if (value == null) return '';
    return String(value)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function sanitizeSearchInput(raw) {
    return String(raw || '')
      .trim()
      .slice(0, 80)
      .replace(/[<>'"\\;]/g, '');
  }

  function parseHistorial(notas, fechaFallback) {
    try {
      const parsed = JSON.parse(notas || '[]');
      if (Array.isArray(parsed)) return parsed;
    } catch (_) {
      /* legacy */
    }
    if (notas) {
      return [{ date: fechaFallback || '', status: 'Nota General', text: notas, img: null }];
    }
    return [
      {
        date: fechaFallback || '',
        status: 'Recibido',
        text: 'Equipo recibido e ingresado al sistema.',
        img: null,
        clientVisible: true,
      },
    ];
  }

  function filterClientTimeline(historial) {
    return historial.filter((ev) => {
      if (ev.internal === true || ev.clientVisible === false) return false;
      if (ev.text && /^\[INTERNO\]/i.test(String(ev.text).trim())) return false;
      if (ev.type && ev.internal === true) return false;
      return true;
    });
  }

  function toClientEvent(ev) {
    const photos = [];
    if (ev.img) photos.push(ev.img);
    if (Array.isArray(ev.photos)) photos.push(...ev.photos.filter(Boolean));
    return {
      type: ev.type || ev.status || 'update',
      message: ev.message || ev.text || '',
      timestamp: ev.timestamp || ev.date || '',
      clientVisible: true,
      status: ev.status || ev.type || 'update',
      photos,
    };
  }

  function buildClientTimeline(historial) {
    return filterClientTimeline(historial).map(toClientEvent);
  }

  function timelineFromClientColumn(clientTimeline, fechaFallback) {
    if (!Array.isArray(clientTimeline) || !clientTimeline.length) return [];
    return clientTimeline.map((ev) => ({
      date: ev.timestamp || fechaFallback || '',
      status: ev.status || ev.type || 'Actualización',
      text: ev.message || '',
      img: Array.isArray(ev.photos) && ev.photos.length ? ev.photos[0] : null,
      photos: ev.photos || [],
      clientVisible: true,
    }));
  }

  function createTimelineEvent({ date, status, text, img, photos, internal, type }) {
    const event = {
      date,
      status: status || 'Nota General',
      type: type || status || 'update',
      text: text || '',
      message: text || '',
      timestamp: date,
      img: img || null,
    };
    if (photos && photos.length) event.photos = photos;
    if (internal) {
      event.internal = true;
      event.clientVisible = false;
    } else {
      event.clientVisible = true;
    }
    return event;
  }

  function enrichOrdenPatch(patch, fechaFallback) {
    if (patch.notas == null) return patch;
    const hist = parseHistorial(patch.notas, fechaFallback);
    patch.client_timeline = buildClientTimeline(hist);
    return patch;
  }

  function trackingUrl(folio, token) {
    const base = typeof location !== 'undefined' ? location.origin : 'https://macwave.com.mx';
    if (token) {
      return `${base}/status-ods.html?token=${encodeURIComponent(token)}`;
    }
    return `${base}/status-ods.html?folio=${encodeURIComponent(folio || '')}`;
  }

  /** Rate limit local (capa extra antes del RPC). */
  function checkLocalRateLimit(action, maxAttempts, windowMs) {
    const key = `mw_rate_${action}`;
    const now = Date.now();
    let bucket = [];
    try {
      bucket = JSON.parse(localStorage.getItem(key) || '[]');
    } catch (_) {
      bucket = [];
    }
    bucket = bucket.filter((t) => now - t < windowMs);
    if (bucket.length >= maxAttempts) return false;
    bucket.push(now);
    localStorage.setItem(key, JSON.stringify(bucket));
    return true;
  }

  async function fetchPublicTracking(client, { token, folio }) {
    if (!checkLocalRateLimit('tracking', 20, 60000)) {
      return { error: { message: 'Demasiados intentos. Espera un momento.' }, data: null };
    }
    const { data, error } = await client.rpc('get_public_ods_tracking', {
      p_token: token || null,
      p_folio: folio || null,
    });
    return { data, error };
  }

  async function logAudit(client, { ods_id, folio, action, details }) {
    try {
      await client.rpc('log_ops_audit', {
        p_ods_id: ods_id || null,
        p_folio: folio || null,
        p_action: action,
        p_details: details || {},
      });
    } catch (e) {
      console.warn('[AUDIT]', e.message);
    }
  }

  const PRIMARY_ADMIN_EMAIL = 'joel.duran.mendoza@me.com';

  function normalizeEmail(email) {
    return String(email || '').trim().toLowerCase();
  }

  function isPrimaryAdminEmail(email) {
    return normalizeEmail(email) === normalizeEmail(PRIMARY_ADMIN_EMAIL);
  }

  /**
   * Tras login Auth: garantiza fila admin en ops_technicians solo para el administrador principal.
   * No abre acceso a otros emails.
   */
  async function ensurePrimaryAdminAccess(client, email) {
    if (!isPrimaryAdminEmail(email)) {
      return { ok: false, skipped: true };
    }

    const { data: rpcData, error: rpcError } = await client.rpc('ensure_primary_admin_access');
    if (!rpcError && rpcData && rpcData.ok === true) {
      return { ok: true, role: rpcData.role || 'admin', via: 'rpc' };
    }

    const { data: upsertData, error: upsertError } = await client
      .from('ops_technicians')
      .upsert(
        { email: PRIMARY_ADMIN_EMAIL, role: 'admin', active: true },
        { onConflict: 'email' }
      )
      .select('role, active')
      .maybeSingle();

    if (!upsertError && upsertData && upsertData.active) {
      return { ok: true, role: upsertData.role, via: 'upsert' };
    }

    const { data: existing, error: readError } = await client
      .from('ops_technicians')
      .select('role, active')
      .ilike('email', PRIMARY_ADMIN_EMAIL)
      .maybeSingle();

    if (!readError && existing && existing.active) {
      return { ok: true, role: existing.role, via: 'read' };
    }

    console.warn('[OPS] ensurePrimaryAdminAccess:', rpcError?.message || upsertError?.message || readError?.message);
    return { ok: false, rpcError, upsertError, readError };
  }

  /** Alias solicitado en spec OPS (mismo comportamiento que ensurePrimaryAdminAccess). */
  async function ensureTechnicianAccess(client, email) {
    return ensurePrimaryAdminAccess(client, email);
  }

  async function verifyTechnicianAccessFromDb(client, email) {
    const normalized = normalizeEmail(email);
    const { data, error } = await client
      .from('ops_technicians')
      .select('role, active')
      .ilike('email', normalized)
      .maybeSingle();
    if (error || !data || !data.active) return null;
    return data.role;
  }

  /**
   * Resuelve rol OPS tras Supabase Auth.
   * Admin principal: acceso inmediato (email verificado por Auth); bootstrap en segundo plano.
   */
  async function verifyTechnicianAccess(client, email) {
    const normalized = normalizeEmail(email);
    if (!normalized) return null;

    if (isPrimaryAdminEmail(normalized)) {
      ensurePrimaryAdminAccess(client, PRIMARY_ADMIN_EMAIL).catch((err) => {
        console.warn('[OPS] bootstrap admin (background):', err?.message || err);
      });
      return 'admin';
    }

    return verifyTechnicianAccessFromDb(client, normalized);
  }

  async function resolveOpsAccess(client, email) {
    return verifyTechnicianAccess(client, email);
  }

  global.MacWaveOps = {
    SUPABASE_URL,
    SUPABASE_ANON_KEY,
    STATUS_CONFIG,
    CLIENT_TRACKING_STEPS,
    createSupabaseClient,
    generateTrackingToken,
    escapeHtml,
    sanitizeSearchInput,
    parseHistorial,
    filterClientTimeline,
    buildClientTimeline,
    timelineFromClientColumn,
    createTimelineEvent,
    enrichOrdenPatch,
    trackingUrl,
    checkLocalRateLimit,
    fetchPublicTracking,
    logAudit,
    PRIMARY_ADMIN_EMAIL,
    isPrimaryAdminEmail,
    ensurePrimaryAdminAccess,
    ensureTechnicianAccess,
    verifyTechnicianAccessFromDb,
    verifyTechnicianAccess,
    resolveOpsAccess,
  };
})(typeof window !== 'undefined' ? window : globalThis);
