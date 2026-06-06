/**
 * macWave OPS — Audit Log UI (FASE 2B)
 * Conecta ops_audit_log al dashboard sin duplicar backend.
 */
(function (global) {
  const PAGE_SIZE = 40;
  const GROUP_WINDOW_MS = 2 * 60 * 1000;

  const ACTION_META = {
    ods_created: { icon: '📋', tag: 'ODS', color: 'rgba(48, 209, 88, 0.2)' },
    status_change: { icon: '↔️', tag: 'Estatus', color: 'rgba(255, 214, 10, 0.15)' },
    meta_update: { icon: '✏️', tag: 'Datos', color: 'rgba(100, 210, 255, 0.12)' },
    photos_uploaded: { icon: '📷', tag: 'Fotos', color: 'rgba(175, 82, 222, 0.15)' },
    photo_deleted: { icon: '🗑️', tag: 'Fotos', color: 'rgba(255, 159, 10, 0.12)' },
    gallery_photos_added: { icon: '🖼️', tag: 'Galería', color: 'rgba(175, 82, 222, 0.15)' },
    payment_update: { icon: '💳', tag: 'Pago', color: 'rgba(48, 209, 88, 0.15)' },
    warranty_update: { icon: '🛡️', tag: 'Garantía', color: 'rgba(100, 210, 255, 0.12)' },
    ticket_created: { icon: '🎟️', tag: 'Visita', color: 'rgba(0, 113, 227, 0.18)' },
    ticket_updated: { icon: '🎟️', tag: 'Visita', color: 'rgba(0, 113, 227, 0.18)' },
  };

  const PHOTO_ACTIONS = new Set(['photos_uploaded', 'gallery_photos_added', 'photo_deleted']);

  let client = null;
  let onOpenOds = null;
  let state = {
    offset: 0,
    total: 0,
    loading: false,
    hasMore: true,
    rows: [],
    filters: {
      q: '',
      action: '',
      actor: '',
      status: '',
      dateFrom: '',
      dateTo: '',
    },
  };

  let debounceTimer = null;

  function escapeHtml(value) {
    if (global.MacWaveOps && global.MacWaveOps.escapeHtml) {
      return global.MacWaveOps.escapeHtml(value);
    }
    if (value == null) return '';
    return String(value)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function formatActor(email) {
    if (!email) return 'Sistema';
    const local = String(email).split('@')[0];
    return local
      .split(/[._-]/)
      .filter(Boolean)
      .map((p) => p.charAt(0).toUpperCase() + p.slice(1).toLowerCase())
      .join(' ');
  }

  function formatRelativeTime(iso) {
    const then = new Date(iso).getTime();
    const now = Date.now();
    const diff = Math.max(0, now - then);
    const sec = Math.floor(diff / 1000);
    if (sec < 60) return 'hace un momento';
    const min = Math.floor(sec / 60);
    if (min < 60) return `hace ${min} min`;
    const hr = Math.floor(min / 60);
    if (hr < 24) return `hace ${hr} h`;
    const day = Math.floor(hr / 24);
    if (day < 7) return `hace ${day} d`;
    return new Date(iso).toLocaleDateString('es-MX', {
      day: '2-digit',
      month: 'short',
      year: 'numeric',
    });
  }

  function formatExactTime(iso) {
    return new Date(iso).toLocaleString('es-MX', {
      day: '2-digit',
      month: 'short',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  }

  function humanizeEvent(row) {
    const actor = formatActor(row.actor_email);
    const d = row.details || {};

    if (row._grouped && row._groupCount > 1) {
      const n = row._groupCount;
      if (row.action === 'photo_deleted') {
        return `${actor} eliminó ${n} fotos`;
      }
      return `${actor} subió ${n} fotos`;
    }

    switch (row.action) {
      case 'ods_created':
        return `${actor} creó la ODS${d.source ? ` (${d.source})` : ''}`;
      case 'status_change': {
        const from = d.from || d.old_status || '—';
        const to = d.to || d.new_status || '—';
        const via = d.via === 'kanban' ? ' desde tablero' : '';
        return `${actor} movió el equipo: ${from} → ${to}${via}`;
      }
      case 'meta_update':
        return `${actor} actualizó datos del cliente/equipo`;
      case 'photos_uploaded': {
        const c = d.count || 1;
        return c > 1 ? `${actor} subió ${c} fotos` : `${actor} subió una foto`;
      }
      case 'gallery_photos_added': {
        const c = d.count || 1;
        return c > 1 ? `${actor} agregó ${c} fotos a galería` : `${actor} agregó una foto a galería`;
      }
      case 'photo_deleted':
        return `${actor} eliminó una foto de evidencia`;
      case 'payment_update':
        return `${actor} actualizó información de pago`;
      case 'warranty_update':
        return `${actor} actualizó la garantía`;
      case 'ticket_created':
        return `${actor} generó ticket de visita${d.cliente ? ` para ${d.cliente}` : ''}`;
      case 'ticket_updated':
        return `${actor} actualizó ticket de visita`;
      default:
        return `${actor} registró actividad: ${row.action.replace(/_/g, ' ')}`;
    }
  }

  function canGroupPhotos(a, b) {
    if (!PHOTO_ACTIONS.has(a.action) || a.action !== b.action) return false;
    if ((a.actor_email || '') !== (b.actor_email || '')) return false;
    if ((a.folio || '') !== (b.folio || '')) return false;
    const t1 = new Date(a.created_at).getTime();
    const t2 = new Date(b.created_at).getTime();
    return Math.abs(t1 - t2) <= GROUP_WINDOW_MS;
  }

  function groupEvents(rows) {
    const out = [];
    let i = 0;
    while (i < rows.length) {
      const row = rows[i];
      if (PHOTO_ACTIONS.has(row.action)) {
        let total = row.details?.count || 1;
        let j = i + 1;
        while (j < rows.length && canGroupPhotos(rows[i], rows[j])) {
          total += rows[j].details?.count || 1;
          j++;
        }
        if (j > i + 1) {
          out.push({
            ...row,
            _grouped: true,
            _groupCount: total,
          });
          i = j;
          continue;
        }
      }
      out.push(row);
      i++;
    }
    return out;
  }

  function matchesClientFilters(row) {
    const { q, status } = state.filters;
    if (status) {
      const d = row.details || {};
      const st = d.to || d.status || '';
      if (!String(st).toLowerCase().includes(status.toLowerCase())) return false;
    }
    if (!q) return true;
    const hay = [
      row.folio,
      row.actor_email,
      row.action,
      humanizeEvent(row),
      JSON.stringify(row.details || {}),
    ]
      .join(' ')
      .toLowerCase();
    return hay.includes(q.toLowerCase());
  }

  async function fetchPage(reset) {
    if (!client || state.loading) return;
    if (reset) {
      state.offset = 0;
      state.rows = [];
      state.hasMore = true;
    }
    if (!state.hasMore && !reset) return;

    state.loading = true;
    renderLoading(reset);

    let query = client
      .from('ops_audit_log')
      .select('id, ods_id, folio, action, details, actor_email, created_at', { count: 'exact' })
      .order('created_at', { ascending: false });

    const { action, actor, dateFrom, dateTo } = state.filters;
    if (action) query = query.eq('action', action);
    if (actor) query = query.ilike('actor_email', `%${actor}%`);
    if (dateFrom) query = query.gte('created_at', `${dateFrom}T00:00:00`);
    if (dateTo) query = query.lte('created_at', `${dateTo}T23:59:59`);

    const q = state.filters.q.trim();
    if (q && q.length >= 3 && !action) {
      query = query.or(`folio.ilike.%${q}%,actor_email.ilike.%${q}%`);
    } else if (q && q.length >= 3 && action) {
      query = query.ilike('folio', `%${q}%`);
    }

    const from = state.offset;
    const to = state.offset + PAGE_SIZE - 1;
    query = query.range(from, to);

    const { data, error, count } = await query;

    state.loading = false;

    if (error) {
      renderError(error.message);
      return;
    }

    const batch = data || [];
    state.total = count ?? state.total;
    state.rows = reset ? batch : state.rows.concat(batch);
    state.offset = state.rows.length;
    state.hasMore = batch.length === PAGE_SIZE;

    renderFeed();
    updateStats();
    updateLoadMore();
  }

  function renderLoading(reset) {
    const feed = document.getElementById('audit-feed');
    if (!feed || !reset) return;
    feed.innerHTML = `
      <div class="audit-skeleton"></div>
      <div class="audit-skeleton"></div>
      <div class="audit-skeleton"></div>
    `;
  }

  function renderError(message) {
    const feed = document.getElementById('audit-feed');
    if (!feed) return;
    feed.innerHTML = `<div class="audit-error">${escapeHtml(message)}</div>`;
  }

  function renderFeed() {
    const feed = document.getElementById('audit-feed');
    if (!feed) return;

    const grouped = groupEvents(state.rows).filter(matchesClientFilters);

    if (!grouped.length) {
      feed.innerHTML = `
        <div class="audit-empty">
          No hay actividad con estos filtros.<br>
          <span style="font-size:12px;opacity:0.8">Los eventos nuevos aparecerán aquí automáticamente.</span>
        </div>`;
      return;
    }

    feed.innerHTML = grouped
      .map((row) => {
        const meta = ACTION_META[row.action] || { icon: '•', tag: 'Evento', color: 'rgba(255,255,255,0.06)' };
        const message = humanizeEvent(row);
        const folio = row.folio || '—';
        const hasOds = !!(row.ods_id || row.folio);
        const clickable = hasOds ? ' clickable' : '';

        return `
          <article class="audit-card${clickable}" data-ods-id="${escapeHtml(row.ods_id || '')}" data-folio="${escapeHtml(folio)}">
            <div class="audit-icon" style="background:${meta.color}">${meta.icon}</div>
            <div class="audit-body">
              <p class="audit-message">${escapeHtml(message)}</p>
              <div class="audit-meta">
                <span class="audit-tag">${escapeHtml(meta.tag)}</span>
                ${
                  folio !== '—'
                    ? `<button type="button" class="audit-folio-link" data-open-folio="${escapeHtml(folio)}">${escapeHtml(folio)}</button>`
                    : ''
                }
                <span class="audit-time-relative">${escapeHtml(formatRelativeTime(row.created_at))}</span>
                <span class="audit-time-exact">${escapeHtml(formatExactTime(row.created_at))}</span>
              </div>
            </div>
          </article>`;
      })
      .join('');

    feed.querySelectorAll('.audit-card.clickable').forEach((card) => {
      card.addEventListener('click', (e) => {
        if (e.target.closest('.audit-folio-link')) return;
        openOds(card.dataset.odsId, card.dataset.folio);
      });
    });

    feed.querySelectorAll('[data-open-folio]').forEach((btn) => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        openOds(btn.closest('.audit-card')?.dataset.odsId, btn.dataset.openFolio);
      });
    });
  }

  function openOds(odsId, folio) {
    if (typeof onOpenOds === 'function') {
      onOpenOds(odsId || null, folio || null);
    }
  }

  function updateStats() {
    const el = document.getElementById('audit-stats');
    if (!el) return;
    el.innerHTML = `
      <span class="audit-stat-pill">${state.rows.length} cargados</span>
      ${state.total ? `<span class="audit-stat-pill">${state.total} total</span>` : ''}
    `;
  }

  function updateLoadMore() {
    const btn = document.getElementById('audit-load-more');
    if (!btn) return;
    btn.style.display = state.hasMore ? 'inline-block' : 'none';
    btn.disabled = state.loading;
    btn.textContent = state.loading ? 'Cargando…' : 'Cargar más actividad';
  }

  function readFiltersFromUi() {
    state.filters.q = document.getElementById('audit-search')?.value?.trim() || '';
    state.filters.action = document.getElementById('audit-action-filter')?.value || '';
    state.filters.actor = document.getElementById('audit-actor-filter')?.value?.trim() || '';
    state.filters.status = document.getElementById('audit-status-filter')?.value?.trim() || '';
    state.filters.dateFrom = document.getElementById('audit-date-from')?.value || '';
    state.filters.dateTo = document.getElementById('audit-date-to')?.value || '';
  }

  function bindUi() {
    const search = document.getElementById('audit-search');
    const refresh = document.getElementById('audit-refresh');
    const loadMore = document.getElementById('audit-load-more');
    const filters = ['audit-action-filter', 'audit-actor-filter', 'audit-status-filter', 'audit-date-from', 'audit-date-to'];

    const scheduleReload = () => {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => {
        readFiltersFromUi();
        fetchPage(true);
      }, 320);
    };

    if (search) {
      search.addEventListener('input', scheduleReload);
      search.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
          readFiltersFromUi();
          fetchPage(true);
        }
      });
    }

    filters.forEach((id) => {
      const el = document.getElementById(id);
      if (el) el.addEventListener('change', () => {
        readFiltersFromUi();
        fetchPage(true);
      });
    });

    if (refresh) {
      refresh.addEventListener('click', () => {
        readFiltersFromUi();
        fetchPage(true);
      });
    }

    if (loadMore) {
      loadMore.addEventListener('click', () => fetchPage(false));
    }
  }

  function init(options) {
    client = options.supabaseClient;
    onOpenOds = options.onOpenOds || null;
    bindUi();
  }

  function onViewActive() {
    readFiltersFromUi();
    if (!state.rows.length) fetchPage(true);
  }

  function refresh() {
    readFiltersFromUi();
    fetchPage(true);
  }

  global.MacWaveAuditLog = {
    init,
    onViewActive,
    refresh,
    PAGE_SIZE,
  };
})(typeof window !== 'undefined' ? window : globalThis);
