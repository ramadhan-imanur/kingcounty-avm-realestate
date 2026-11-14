/**
 * KingCounty-AVM: Leaflet Map Core Adapter
 * Initializes smooth vector tiles and handles viewport projection
 */

export class LeafletAdapter {
  constructor(target, center = [47.5480, -122.18], zoom = 10) {
    if (typeof L === 'undefined') {
      console.warn('Leaflet is not loaded on window.');
      return;
    }

    const el = typeof target === 'string' ? document.getElementById(target) : target;
    if (!el) {
      console.warn('LeafletAdapter: target element not found in DOM.');
      return;
    }

    this.map = L.map(el, {
      center,
      zoom,
      minZoom: 9,
      maxZoom: 17,
      zoomControl: true,
      scrollWheelZoom: true
    });

    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
      attribution: '&copy; OpenStreetMap &copy; CARTO',
      subdomains: 'abcd',
      maxZoom: 19
    }).addTo(this.map);

    this.submarketLayer = L.layerGroup().addTo(this.map);
    this.compsLayer = L.layerGroup().addTo(this.map);
    this.radiusLayer = L.layerGroup().addTo(this.map);
  }

  invalidateSize() {
    if (this.map) {
      setTimeout(() => this.map.invalidateSize(), 80);
    }
  }

  flyTo(lat, lon, zoom = 12) {
    if (this.map) {
      this.map.flyTo([lat, lon], zoom, { duration: 1.2 });
    }
  }

  clearSubmarkets() {
    if (this.submarketLayer) this.submarketLayer.clearLayers();
  }

  clearComps() {
    if (this.compsLayer) this.compsLayer.clearLayers();
    if (this.radiusLayer) this.radiusLayer.clearLayers();
  }
}
