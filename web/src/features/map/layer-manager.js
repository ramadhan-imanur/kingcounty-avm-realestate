/**
 * KingCounty-AVM: Leaflet Layer Manager & GeoJSON Markers
 * Binds submarket centroids, interactive popups, and radius rings
 */

import { formatUSD } from '../../core/config.js';

export class LayerManager {
  static getTierColor(ppsqft) {
    if (ppsqft > 450) return '#7C3AED'; // Purple
    if (ppsqft >= 250) return '#0284C7'; // Blue
    return '#0D9488'; // Teal
  }

  static renderSubmarkets(adapter, zipcodes, activeZip, onSelect) {
    if (!adapter || !adapter.submarketLayer) return;
    adapter.clearSubmarkets();

    zipcodes.forEach(z => {
      const isSelected = z.code === activeZip;
      const color = this.getTierColor(z.ppsqft);

      const marker = L.circleMarker([z.lat, z.lon], {
        radius: isSelected ? 10 : 7,
        fillColor: color,
        color: '#ffffff',
        weight: isSelected ? 3 : 2,
        opacity: 1,
        fillOpacity: 0.9
      });

      const popupHtml = `
        <div class="p-2.5 flex flex-col gap-1.5 min-w-[190px] font-sans">
          <div class="flex justify-between items-center text-[10px] font-mono">
            <span class="px-2 py-0.5 rounded font-bold bg-purple-50 text-purple-700 border border-purple-200">
              Area ${z.code}
            </span>
            <span class="flex items-center gap-1 font-bold text-emerald-700">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
              Aktif
            </span>
          </div>
          <div class="font-bold text-slate-900 text-xs mt-0.5">${z.name}</div>
          <div class="flex justify-between text-xs font-mono pt-1.5 border-t border-slate-100">
            <span class="text-slate-500">Harga Median:</span>
            <span class="font-bold text-slate-900">${formatUSD(z.medianPrice)}</span>
          </div>
          <div class="flex justify-between text-xs font-mono">
            <span class="text-slate-500">Rata-rata / sq.ft:</span>
            <span class="font-bold text-emerald-700">$${z.ppsqft} / sq.ft</span>
          </div>
          <button data-select-zip="${z.code}" class="mt-2 w-full py-1.5 px-2 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-[11px] cursor-pointer transition-colors text-center shadow-xs">
            Pilih Submarket Ini
          </button>
        </div>
      `;

      marker.bindPopup(popupHtml, { className: 'custom-leaflet-popup' });
      marker.on('popupopen', () => {
        const btn = document.querySelector(`[data-select-zip="${z.code}"]`);
        if (btn) {
          btn.addEventListener('click', () => {
            if (onSelect) onSelect(z.code);
            marker.closePopup();
          });
        }
      });

      adapter.submarketLayer.addLayer(marker);
    });
  }

  static renderComps(adapter, centerLat, centerLon, comps, radiusMiles = 2.5) {
    if (!adapter || !adapter.compsLayer) return;
    adapter.clearComps();

    const circle = L.circle([centerLat, centerLon], {
      radius: radiusMiles * 1609.34,
      color: '#059669',
      dashArray: '5, 5',
      weight: 1.5,
      fillColor: '#10B981',
      fillOpacity: 0.08
    });
    adapter.radiusLayer.addLayer(circle);

    comps.forEach((comp, idx) => {
      const compMarker = L.circleMarker([comp.lat, comp.lon], {
        radius: 6,
        fillColor: '#D97706',
        color: '#ffffff',
        weight: 2,
        fillOpacity: 0.95
      });

      compMarker.bindPopup(`
        <div class="p-1.5 text-xs font-sans">
          <div class="font-bold text-slate-900">Comp #${idx + 1}: ${comp.address}</div>
          <div class="font-mono font-bold text-slate-800">${formatUSD(comp.price)}</div>
          <div class="text-[10px] text-slate-500">${comp.beds} KT &bull; ${comp.baths} KM &bull; ${comp.sqft} sqft</div>
        </div>
      `, { className: 'custom-leaflet-popup' });

      adapter.compsLayer.addLayer(compMarker);
    });
  }
}
