var staticCacheName ='django-pwa-v9'+ new Date().getTime();
var filesToCache = [
    '/',
    '/registro/',
    '/productos/',
    '/login/',
    '/static/img/icons/icon-72x72.png',
    '/static/img/icons/icon-96x96.png',
    '/static/img/icons/icon-128x128.png',
    '/static/img/icons/icon-144x144.png',
    '/static/img/icons/icon-152x152.png',
    '/static/img/icons/icon-192x192.png',
    '/static/img/icons/icon-384x384.png',
    '/static/img/icons/icon-512x512.png',
    '/static/img/default-product.jpg',
    '/static/img/img-about.jpg',
    '/static/img/icon-menu.png',
    '/static/js/bootstrap.min.js',
    '/static/js/bs-custom-file-input.min.js',
    '/static/js/javamenu.js',
    '/static/js/jquery-3.3.1.slim.min.js',
    '/static/js/popper.min.js',
    '/static/js/wow.js',
    '/static/css/about.css',
    '/static/css/animate.css',
    '/static/css/bootstrap.min.css',
    '/static/css/crear_producto.css',
    '/static/css/detalle_producto.css',
    '/static/css/first-register.css',
    '/static/css/icons.css',
    '/static/css/login.css',
    '/static/css/main.css',
    '/static/css/menu.css',
    '/static/css/productos.css',
    '/static/css/solicitar_mantencion.css',
    '/static/css/solicitudes.css',
    '/manifest.json'

];

// Cache on install
self.addEventListener("install", event => {
    this.skipWaiting();
    event.waitUntil(
        caches.open(staticCacheName)
            .then(cache => {
                return cache.addAll(filesToCache);
            })
    )
});

// Clear cache on activate
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames
                    .filter(cacheName => (cacheName.startsWith("django-pwa-")))
                    .filter(cacheName => (cacheName !== staticCacheName))
                    .map(cacheName => caches.delete(cacheName))
            );
        })
    );
});

// Serve from Cache
self.addEventListener("fetch", event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                return response || fetch(event.request);
            })
            .catch(() => {
                return caches.match('/');
            })
    )
});