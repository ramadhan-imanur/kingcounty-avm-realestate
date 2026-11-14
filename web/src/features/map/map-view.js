/**
 * KingCounty-AVM: Spatial Map View Component
 * Interactive cartographic canvas & submarket comparison benchmarks
 */

import { appStore } from '../../core/state.js';
import { formatUSD } from '../../core/config.js';
import { DataService } from '../../core/data-service.js';
import { LayerManager } from './layer-manager.js';
import { findComparableProperties } from './comps-finder.js';
import { renderCompsTable } from '../../components/ui/comps-table.js';

export function renderMapView() {
  const container = document.createElement('div');
  container.className = 'map-view flex flex-col gap-6';

  const zipcodes = DataService.getAllZipcodes();
  const currentProp = appStore.getState().property;
  const comps = findComparableProperties(currentProp);

  // Generate SVG points for zipcodes
  const pointsSVG = zipcodes.map(z => {
    const pt = LayerManager.project(z.lat, z.lon);
    const isCurrent = z.code === currentProp.zipcode;
    const color = z.tier === 'luxury' ? '#7C3AED' : (z.tier === 'mid' ? '#0284C7' : '#0D9488');
    const radius = isCurrent ? 9 : 6;

    return `
      <g class="map-node cursor-pointer" data-zip="${z.code}" data-name="${z.name}" data-price="${z.medianPrice}" data-ppsqft="${z.ppsqft}">
        <circle cx="${pt.x}" cy="${pt.y}" r="${radius}" fill="${color}" stroke="#ffffff" stroke-width="2" class="transition-all hover:scale-150" />
        ${isCurrent ? `<circle cx="${pt.x}" cy="${pt.y}" r="15" fill="none" stroke="${color}" stroke-width="1.5" class="animate-ping opacity-60" />` : ''}
      </g>
    `;
  }).join('');

  container.innerHTML = `
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
      <!-- Interactive SVG Map Canvas (Cols 1-8) -->
      <div class="lg:col-span-8 glass-card p-4 flex flex-col gap-3 relative overflow-hidden">
        <div class="flex justify-between items-center border-b border-slate-100 pb-2">
          <div>
            <h3 class="font-bold text-sm text-slate-900">Peta Spasial Klaster Properti King County</h3>
            <p class="text-xs text-slate-500">Kepadatan harga per sq.ft & koordinat centroid submarket.</p>
          </div>
          <span class="font-mono text-xs text-emerald-800 bg-emerald-50 px-2.5 py-1 rounded-full border border-emerald-200">
            EPSG:4326 Proyeksi
          </span>
        </div>

        <div class="relative w-full h-[420px] bg-slate-900/5 rounded-xl border border-slate-200/80 overflow-hidden">
          <svg viewBox="0 0 800 500" class="w-full h-full select-none">
            ${LayerManager.renderWaterBodiesSVG()}
            ${pointsSVG}
          </svg>

          <!-- Floating Info Overlay Card -->
          <div id="map-hover-card" class="absolute top-3 right-3 glass-card p-3 shadow-lg flex flex-col gap-1 text-xs pointer-events-none min-w-[200px]">
            <span class="font-mono font-bold text-slate-500 uppercase text-[10px]" id="map-card-zip">Area 98004</span>
            <div class="font-bold text-slate-900 text-sm" id="map-card-name">Bellevue Downtown</div>
            <div class="flex justify-between pt-1 border-t border-slate-100 font-mono">
              <span class="text-slate-500">Median:</span>
              <span class="font-bold text-slate-900" id="map-card-price">$1,420,000</span>
            </div>
            <div class="flex justify-between font-mono">
              <span class="text-slate-500">$/sq.ft:</span>
              <span class="font-bold text-emerald-700" id="map-card-ppsqft">$542</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Submarket Benchmark Table (Cols 9-12) -->
      <div class="lg:col-span-4 glass-card p-4 flex flex-col gap-3">
        <div class="border-b border-slate-100 pb-2">
          <h3 class="font-bold text-sm text-slate-900">Perbandingan Submarket</h3>
          <p class="text-[11px] text-slate-500">Standar benchmark King County 2026.</p>
        </div>
        <div class="overflow-y-auto max-h-[360px] text-xs">
          <table class="w-full text-left font-mono">
            <thead>
              <tr class="text-[10px] text-slate-400 uppercase border-b border-slate-200">
                <th class="py-1">Wilayah</th>
                <th class="py-1 text-right">Median</th>
                <th class="py-1 text-right">/sq.ft</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100">
              ${zipcodes.slice(0, 7).map(z => `
                <tr>
                  <td class="py-1.5 font-sans font-medium text-slate-800">${z.code}</td>
                  <td class="py-1.5 text-right font-bold text-slate-900">${formatUSD(z.medianPrice)}</td>
                  <td class="py-1.5 text-right text-emerald-700">$${z.ppsqft}</td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Comps Section -->
    <div class="glass-card p-4 flex flex-col gap-3">
      <h3 class="font-bold text-sm text-slate-900">Properti Pembanding Terdekat (Radius 5 Mil)</h3>
      ${renderCompsTable(comps)}
    </div>
  `;

  // Attach hover events to nodes
  const cardZip = container.querySelector('#map-card-zip');
  const cardName = container.querySelector('#map-card-name');
  const cardPrice = container.querySelector('#map-card-price');
  const cardPpsqft = container.querySelector('#map-card-ppsqft');

  container.querySelectorAll('.map-node').forEach(node => {
    node.addEventListener('mouseenter', () => {
      cardZip.textContent = `Area ${node.dataset.zip}`;
      cardName.textContent = node.dataset.name;
      cardPrice.textContent = formatUSD(Number(node.dataset.price));
      cardPpsqft.textContent = `$${node.dataset.ppsqft}`;
    });
  });

  return container;
}
