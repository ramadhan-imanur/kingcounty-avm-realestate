/**
 * KingCounty-AVM: Interactive Spatial Map View Component
 * Dynamic Leaflet Map with Pan/Zoom, Geo-filtering, and Comps Synchronization
 */

import { appStore } from '../../core/state.js';
import { DataService } from '../../core/data-service.js';
import { LeafletAdapter } from './leaflet-adapter.js';
import { LayerManager } from './layer-manager.js';
import { findComparableProperties } from './comps-finder.js';
import { renderCompsTable } from '../../components/ui/comps-table.js';
import { renderMarketKpiCards } from '../../components/ui/market-kpi-cards.js';

export function renderMapView() {
  const container = document.createElement('div');
  container.className = 'map-view flex flex-col gap-5';
  let currentTier = 'all', mapAdapter = null;
  const allZipcodes = DataService.getAllZipcodes();

  container.appendChild(renderMarketKpiCards());

  const mainGrid = document.createElement('div');
  mainGrid.className = 'grid grid-cols-1 lg:grid-cols-12 gap-5 items-start';
  mainGrid.innerHTML = `
    <div class="lg:col-span-8 glass-card p-4 flex flex-col gap-3">
      <div class="flex flex-wrap items-center justify-between gap-2">
        <div>
          <h2 class="text-sm font-extrabold text-slate-900 tracking-tight flex items-center gap-1.5">
            <svg class="w-4 h-4 text-emerald-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"></polygon><line x1="8" y1="2" x2="8" y2="18"></line><line x1="16" y1="6" x2="16" y2="22"></line></svg>
            Peta Spasial Pasar Properti King County
          </h2>
          <p class="text-[11px] text-slate-500">Peta kepadatan harga per square feet dan titik klaster transaksi</p>
        </div>
        <div id="coord-badge" class="font-mono text-[10px] text-sky-800 bg-sky-50 px-2.5 py-1 rounded-full border border-sky-200">
          Koordinat: 47.6101° N, 122.2015° W
        </div>
      </div>

      <div class="flex items-center justify-between gap-2 text-xs pt-1 border-t border-slate-100">
        <div class="flex items-center gap-2">
          <span class="text-[11px] font-bold text-slate-600">Filter Strata:</span>
          <div class="inline-flex rounded-lg bg-slate-100 p-0.5" id="map-tier-filters">
            <button data-tier="all" class="px-2 py-0.5 text-[11px] font-bold rounded-md bg-white text-slate-900 shadow-xs cursor-pointer">Semua</button>
            <button data-tier="entry" class="px-2 py-0.5 text-[11px] font-medium rounded-md text-slate-600 hover:text-slate-900 cursor-pointer">Terjangkau</button>
            <button data-tier="mid" class="px-2 py-0.5 text-[11px] font-medium rounded-md text-slate-600 hover:text-slate-900 cursor-pointer">Menengah</button>
            <button data-tier="luxury" class="px-2 py-0.5 text-[11px] font-medium rounded-md text-slate-600 hover:text-slate-900 cursor-pointer">Mewah</button>
          </div>
        </div>
        <span class="font-mono text-[10px] text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">Pan & Zoom Aktif</span>
      </div>

      <div id="leaflet-map-canvas" class="w-full h-[410px] rounded-xl border border-slate-200 shadow-inner z-10"></div>

      <div class="flex items-center justify-between text-[11px] font-mono text-slate-600 pt-2 border-t border-slate-100">
        <div class="flex items-center gap-3">
          <span class="font-bold text-slate-400 text-[10px]">HARGA / SQ.FT:</span>
          <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-teal-600"></span>&lt;$250</span>
          <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-sky-600"></span>$250 &ndash; $450</span>
          <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-purple-600"></span>&gt;$450</span>
        </div>
        <span class="text-[10px] text-slate-400">Klik titik untuk detail submarket</span>
      </div>
    </div>

    <div class="lg:col-span-4 glass-card p-4 flex flex-col gap-3">
      <div class="flex justify-between items-center border-b border-slate-100 pb-2">
        <div>
          <h3 class="font-bold text-xs text-slate-900 uppercase tracking-wider">Perbandingan Submarket</h3>
          <p class="text-[10px] text-slate-400">Pilih baris untuk navigasi peta</p>
        </div>
        <span class="text-[10px] font-mono font-medium text-slate-500 bg-slate-100 px-2 py-0.5 rounded">Benchmark 2024</span>
      </div>
      <div class="overflow-y-auto max-h-[460px] text-xs">
        <table class="w-full text-left font-mono" id="submarket-table">
          <thead><tr class="text-[10px] text-slate-400 uppercase border-b border-slate-200"><th class="py-1">Wilayah</th><th class="py-1 text-right">Median</th><th class="py-1 text-right">/sq.ft</th></tr></thead>
          <tbody class="divide-y divide-slate-100" id="submarket-tbody"></tbody>
        </table>
      </div>
    </div>
  `;
  container.appendChild(mainGrid);

  const compsSection = document.createElement('div');
  compsSection.className = 'glass-card p-4 flex flex-col gap-3';
  compsSection.innerHTML = `
    <div class="flex justify-between items-center border-b border-slate-100 pb-2"><h3 class="font-bold text-sm text-slate-900">Properti Pembanding Terdekat (Comps Radius)</h3><span class="text-xs text-slate-500 font-mono">Radius 2.5 Mil</span></div>
    <div id="comps-table-mount"></div>
  `;
  container.appendChild(compsSection);

  function updateSubmarketTable(filtered) {
    const tbody = container.querySelector('#submarket-tbody');
    if (!tbody) return;
    tbody.innerHTML = filtered.map(z => `
      <tr class="hover:bg-slate-100/70 cursor-pointer transition-colors" data-zip="${z.code}">
        <td class="py-1.5 font-sans font-medium text-slate-800">${z.name.split(' ')[0]} <span class="text-[10px] text-slate-400">(${z.code})</span></td>
        <td class="py-1.5 text-right font-bold ${z.ppsqft > 450 ? 'text-purple-700' : (z.ppsqft >= 250 ? 'text-sky-700' : 'text-teal-700')}">$${Math.round(z.medianPrice / 1000)}k</td>
        <td class="py-1.5 text-right font-mono text-slate-700">$${z.ppsqft}</td>
      </tr>
    `).join('');
    tbody.querySelectorAll('tr').forEach(r => r.addEventListener('click', () => selectLocation(r.dataset.zip)));
  }

  function selectLocation(zipcode) {
    const zData = DataService.getZipcode(zipcode);
    appStore.setState({ property: { ...appStore.getState().property, zipcode, lat: zData.lat, lon: zData.lon } });
    const badge = container.querySelector('#coord-badge');
    if (badge) badge.textContent = `Koordinat: ${zData.lat.toFixed(4)}° N, ${Math.abs(zData.lon).toFixed(4)}° W`;
    if (mapAdapter) { mapAdapter.flyTo(zData.lat, zData.lon, 12); refreshLayers(); }
  }

  function refreshLayers() {
    const currentProp = appStore.getState().property;
    const filtered = currentTier === 'all' ? allZipcodes : allZipcodes.filter(z => z.tier === currentTier);
    if (mapAdapter) {
      LayerManager.renderSubmarkets(mapAdapter, filtered, currentProp.zipcode, selectLocation);
      const comps = findComparableProperties(currentProp);
      LayerManager.renderComps(mapAdapter, currentProp.lat, currentProp.lon, comps, 2.5);
    }
    const comps = findComparableProperties(currentProp);
    container.querySelector('#comps-table-mount').innerHTML = renderCompsTable(comps);
    updateSubmarketTable(filtered);
  }

  function initMap() {
    const canvas = container.querySelector('#leaflet-map-canvas');
    if (!canvas || !document.body.contains(canvas)) return;
    if (!mapAdapter && typeof L !== 'undefined') {
      const prop = appStore.getState().property;
      mapAdapter = new LeafletAdapter(canvas, [prop.lat, prop.lon], 10);
      refreshLayers();
    }
    if (mapAdapter) mapAdapter.invalidateSize();
  }

  container.onMount = initMap;
  container.querySelectorAll('#map-tier-filters button').forEach(btn => {
    btn.addEventListener('click', () => {
      container.querySelectorAll('#map-tier-filters button').forEach(b => b.className = 'px-2 py-0.5 text-[11px] font-medium rounded-md text-slate-600 hover:text-slate-900 cursor-pointer');
      btn.className = 'px-2 py-0.5 text-[11px] font-bold rounded-md bg-white text-slate-900 shadow-xs cursor-pointer';
      currentTier = btn.dataset.tier;
      refreshLayers();
    });
  });

  refreshLayers();
  setTimeout(initMap, 150);
  return container;
}
