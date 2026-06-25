// Service Worker for "The Calm Before" / Sam's MCAT page.
// Network-first for documents (fresh content when online, cached when offline);
// stale-while-revalidate for assets + Google Fonts so the page works fully offline.
const CACHE = 'calm-before-v1';
const CORE = ['.', './sam.html', './index.html', './favicon.svg'];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE).then((c) => c.addAll(CORE)).catch(() => {})
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  const cacheable = url.origin === self.location.origin ||
    url.hostname.includes('gstatic.com') || url.hostname.includes('googleapis.com');

  // Documents: network-first.
  if (req.mode === 'navigate' || (req.headers.get('accept') || '').includes('text/html')) {
    e.respondWith(
      fetch(req).then((r) => {
        const cp = r.clone();
        caches.open(CACHE).then((c) => c.put(req, cp));
        return r;
      }).catch(() => caches.match(req).then((m) => m || caches.match('./sam.html')))
    );
    return;
  }

  // Assets & fonts: stale-while-revalidate.
  if (cacheable) {
    e.respondWith(
      caches.match(req).then((cached) => {
        const network = fetch(req).then((r) => {
          if (r && r.status === 200) {
            const cp = r.clone();
            caches.open(CACHE).then((c) => c.put(req, cp));
          }
          return r;
        }).catch(() => cached);
        return cached || network;
      })
    );
  }
});
