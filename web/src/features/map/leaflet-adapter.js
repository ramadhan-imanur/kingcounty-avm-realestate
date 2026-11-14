/**
 * KingCounty-AVM: Leaflet Map Core Adapter
 * Initializes smooth vector tiles and handles viewport projection
 */

export class LeafletAdapter {
  constructor(elementId, center = [47.5480, -122.18], zoom = 10) {
    if (typeof L === 'undefined') {
      console.warn('Leaflet is not loaded on window.');
      return;
    }

    this.map = L.map(elementId, {
      center,
      zoom,
      minZoom: 9,
      maxZoom: 17,
      zoomControl: true,
      scrollWheelZoom: true
    });

    // Sleek CartoDB Positron Cartography
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
      setTimeout(() => this.map.invalidateSize(), 50);
    }
  }

  flyTo(lat, lon, zoom = 12) {
    if (this.map) {
      this.map.flyTo([lat, lon], zoom, { duration: 1.2 });
    }
  }

  clearSubmarkets() {
    this.submarketLayer.clearLayers();
  }

  clearComps() {
    this.compsLayer.clearLayers();
    this.radiusLayer.clearLayers();
  }
}
