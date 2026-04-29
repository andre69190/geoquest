/* GeoQuest – Service Worker v1.0 */
const CACHE = "geoquest-v1";
const ASSETS = [
  "./GeoQuest.html",
  "./manifest.json",
  "./icon.svg",
  "./cities.json"
];

self.addEventListener("install", e => {
  e.waitUntil(
    caches.open(CACHE).then(cache => {
      // Cache what we can; cities.json may be missing – ignore errors
      return Promise.allSettled(ASSETS.map(url =>
        cache.add(url).catch(() => {})
      ));
    }).then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", e => {
  // Network-first for Supabase API calls
  if (e.request.url.includes("supabase.co")) {
    e.respondWith(
      fetch(e.request).catch(() => new Response("", { status: 503 }))
    );
    return;
  }
  // Cache-first for everything else
  e.respondWith(
    caches.match(e.request).then(cached => {
      if (cached) return cached;
      return fetch(e.request).then(response => {
        if (response.ok) {
          const clone = response.clone();
          caches.open(CACHE).then(cache => cache.put(e.request, clone));
        }
        return response;
      }).catch(() => caches.match("./GeoQuest.html"));
    })
  );
});
