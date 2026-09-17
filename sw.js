// Service Worker for macWave Mexico - Performance & Caching
// v1.4.0: no cachear HTML (evita footer/login viejos tras hotfix OPS)
const CACHE_NAME = 'macwave-v1.5.1-ops';
const urlsToCache = [
  '/style.css?v=26.5.1',
  '/script.js?v=26.5.1',
  '/images/favicon1.png',
  '/images/dispositivos.jpg',
  'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap'
];

function isDocumentRequest(request) {
  if (request.mode === 'navigate') return true;
  try {
    const url = new URL(request.url);
    if (url.origin !== self.location.origin) return false;
    const path = url.pathname;
    return path.endsWith('.html') || path === '/' || !path.includes('.');
  } catch (_) {
    return false;
  }
}

self.addEventListener('install', (event) => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(urlsToCache))
  );
});

self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) =>
      Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) return caches.delete(cacheName);
        })
      )
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;

  // HTML siempre red primero (login + footer OPS actualizados)
  if (isDocumentRequest(event.request)) {
    event.respondWith(
      fetch(event.request).catch(() => caches.match(event.request))
    );
    return;
  }

  event.respondWith(
    caches.match(event.request).then((cached) => {
      const network = fetch(event.request)
        .then((response) => {
          if (response && response.status === 200 && response.type === 'basic') {
            const clone = response.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
          }
          return response;
        })
        .catch(() => cached);
      return cached || network;
    })
  );
});
