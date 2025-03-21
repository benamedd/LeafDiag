// Nom du cache
const CACHE_NAME = 'leaf-disease-analyzer-v1';

// Liste des fichiers � mettre en cache
const urlsToCache = [
  '/',
  '/static/icons/icon-192x192.png',
  '/static/icons/icon-512x512.png',
  // Ajoute ici d'autres fichiers statiques si n�cessaire
];

// Installation du service worker
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Cache ouvert');
        return cache.addAll(urlsToCache);
      })
  );
});

// Activation du service worker
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            console.log('Suppression de l�ancien cache :', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// Interception des requ�tes r�seau
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Si la ressource est dans le cache, on la renvoie
        if (response) {
          return response;
        }
        // Sinon, on fait une requ�te r�seau
        return fetch(event.request)
          .then(response => {
            // On met en cache la r�ponse pour les futures requ�tes
            if (!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }
            const responseToCache = response.clone();
            caches.open(CACHE_NAME)
              .then(cache => {
                cache.put(event.request, responseToCache);
              });
            return response;
          });
      })
  );
});