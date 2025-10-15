const CACHE_NAME = "hangarin-cache-v1";
const urlsToCache = [

    "/tasks/", 
  "/static/tasks/css/main.css",
  "/static/tasks/js/main.js",
  "/static/tasks/icons/icon-192x192.png",
  "/static/tasks/icons/icon-512x512.png",
];


self.addEventListener("install", (event) => {
  console.log("Service Worker: Installing...");
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log("Service Worker: Caching files...");
      return cache.addAll(urlsToCache);
    })
  );
  self.skipWaiting();
});


self.addEventListener("activate", (event) => {
  console.log("Service Worker: Activated");
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cache) => {
          if (cache !== CACHE_NAME) {
            console.log("Service Worker: Clearing old cache:", cache);
            return caches.delete(cache);
          }
        })
      );
    })
  );
  self.clients.claim();
});


self.addEventListener("fetch", (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      return (
        response ||
        fetch(event.request)
          .then((res) => {
            const resClone = res.clone();
            caches.open(CACHE_NAME).then((cache) => {
              cache.put(event.request, resClone);
            });
            return res;
          })
          .catch(() => {
            if (event.request.mode === "navigate") {
              return caches.match("/");
            }
          })
      );
    })
  );
});
