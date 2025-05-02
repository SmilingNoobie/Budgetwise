self.addEventListener("install", e => {
  console.log("Service Worker installed");
  e.waitUntil(self.skipWaiting());
});
self.addEventListener("activate", e => {
  console.log("Service Worker activated");
  e.waitUntil(self.clients.claim());
});
self.addEventListener("fetch", event => {
  event.respondWith(
    fetch(event.request).catch(() => caches.match(event.request))
  );
});
