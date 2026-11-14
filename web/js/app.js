/**
 * KingCounty-AVM Application Bridge
 * Seamless backward compatibility for classic script loaders
 */

(function() {
  import('../src/app.js')
    .then(module => {
      if (typeof module.bootstrap === 'function') {
        module.bootstrap();
      }
    })
    .catch(err => {
      console.warn('[KingCounty-AVM] ES Module bootstrap info:', err);
    });
})();
