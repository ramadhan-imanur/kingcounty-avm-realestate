/**
 * KingCounty-AVM: Valuation Estimator View Component
 * Handles property parameter input controls and real-time inference rendering
 */

import { appStore } from '../../core/state.js';
import { formatUSD, formatIDRBillions } from '../../core/config.js';
import { DataService } from '../../core/data-service.js';
import { runAVMInference } from './avm-inference.js';
import { renderHorizontalBarChart } from '../../components/charts/simple-chart.js';

export function renderEstimatorView() {
  const container = document.createElement('div');
  container.className = 'estimator-view flex flex-col gap-5';

  const prop = appStore.getState().property;
  const zipcodes = DataService.getAllZipcodes();

  container.innerHTML = `
    <!-- Hero Banner with Photographic Background -->
    <div class="min-h-[135px] rounded-3xl p-5 flex flex-col justify-between relative overflow-hidden shadow-md border border-white/60">
      <div class="absolute inset-0 z-0 overflow-hidden">
        <img src="https://images.unsplash.com/photo-1580587771525-78b9dba3b914?auto=format&fit=crop&w=1600&q=80" alt="King County Real Estate" class="w-full h-full object-cover object-center absolute inset-0">
        <div class="absolute inset-0 bg-gradient-to-r from-slate-950/85 via-slate-900/65 to-emerald-950/45"></div>
      </div>
      <div class="relative z-10 flex items-center justify-between gap-2">
        <span class="px-2.5 py-0.5 rounded-full bg-white/20 backdrop-blur-md text-white border border-white/30 text-[11px] font-mono font-bold flex items-center gap-1.5">
          <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          Dual-Pipeline v4.2 &bull; Geospatial LightGBM + K-Means
        </span>
        <span class="hidden sm:inline-flex px-2.5 py-0.5 rounded-xl bg-white/20 backdrop-blur-md border border-white/30 text-white font-mono text-[11px]">22.847 Unit</span>
      </div>
      <div class="relative z-10 mt-1.5">
        <h1 class="text-xl sm:text-2xl font-extrabold text-white tracking-tight">Kalkulator Nilai Properti Cerdas</h1>
        <p class="text-xs text-slate-200 mt-0.5 max-w-xl">Perkiraan nilai pasar wajar hunian King County berbasis ML dengan interpretasi SHAP.</p>
      </div>
    </div>

    <!-- 2-Column Grid: Form Controls & Output -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-5 items-start">
      <div class="lg:col-span-6 glass-card flex flex-col gap-4">
        <div class="border-b border-slate-100 pb-2">
          <h3 class="font-bold text-sm text-slate-900">Parameter Fisik & Lokasi Properti</h3>
          <p class="text-[11px] text-slate-500">Sesuaikan atribut hunian untuk kalkulasi nilai pasar wajar seketika.</p>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
          <div class="flex flex-col gap-1">
            <label class="font-semibold text-slate-700">Kode Pos Wilayah</label>
            <select id="est-zip" class="glass-input w-full font-mono text-xs">
              ${zipcodes.map(z => `<option value="${z.code}" ${z.code === prop.zipcode ? 'selected' : ''}>${z.code} - ${z.name.split(' ')[0]}</option>`).join('')}
            </select>
          </div>
          <div class="flex flex-col gap-1">
            <label class="font-semibold text-slate-700">Luas Bangunan (sqft)</label>
            <input type="number" id="est-sqft" value="${prop.sqft_living}" step="50" class="glass-input font-mono font-bold">
          </div>
        </div>

        <div class="grid grid-cols-2 sm:grid-cols-4 gap-2.5 text-xs">
          <div class="flex flex-col gap-1">
            <label class="font-semibold text-slate-700">Kamar Tidur</label>
            <select id="est-beds" class="glass-input font-mono">
              ${[1, 2, 3, 4, 5, 6].map(n => `<option value="${n}" ${n === prop.bedrooms ? 'selected' : ''}>${n} KT</option>`).join('')}
            </select>
          </div>
          <div class="flex flex-col gap-1">
            <label class="font-semibold text-slate-700">Kamar Mandi</label>
            <select id="est-baths" class="glass-input font-mono">
              ${[1, 1.5, 2, 2.5, 3, 3.5, 4].map(n => `<option value="${n}" ${n === prop.bathrooms ? 'selected' : ''}>${n} KM</option>`).join('')}
            </select>
          </div>
          <div class="flex flex-col gap-1">
            <label class="font-semibold text-slate-700">Grade (1-13)</label>
            <input type="number" id="est-grade" min="4" max="13" value="${prop.grade}" class="glass-input font-mono">
          </div>
          <div class="flex flex-col gap-1">
            <label class="font-semibold text-slate-700">Kondisi (1-5)</label>
            <input type="number" id="est-cond" min="1" max="5" value="${prop.condition}" class="glass-input font-mono">
          </div>
        </div>

        <div class="flex items-center gap-6 pt-2 border-t border-slate-100 text-xs">
          <label class="flex items-center gap-2 cursor-pointer">
            <input type="checkbox" id="est-water" ${prop.waterfront ? 'checked' : ''} class="rounded text-emerald-600">
            <span class="font-medium text-slate-700">Tepi Air (Waterfront)</span>
          </label>
          <label class="flex items-center gap-2 cursor-pointer">
            <input type="checkbox" id="est-view" ${prop.has_view ? 'checked' : ''} class="rounded text-emerald-600">
            <span class="font-medium text-slate-700">Pemandangan (View)</span>
          </label>
        </div>
      </div>

      <div id="est-output-panel" class="lg:col-span-6 flex flex-col gap-4"></div>
    </div>
  `;

  function update() {
    const q = sel => container.querySelector(sel);
    const updatedProp = {
      ...appStore.getState().property,
      zipcode: q('#est-zip').value,
      sqft_living: Number(q('#est-sqft').value) || 2000,
      bedrooms: Number(q('#est-beds').value),
      bathrooms: Number(q('#est-baths').value),
      grade: Number(q('#est-grade').value),
      condition: Number(q('#est-cond').value),
      waterfront: q('#est-water').checked ? 1 : 0,
      has_view: q('#est-view').checked ? 1 : 0
    };

    const result = runAVMInference(updatedProp);
    appStore.setState({ property: updatedProp, valuation: result });

    container.querySelector('#est-output-panel').innerHTML = `
      <div class="glass-card border-2 border-emerald-600/20 flex flex-col gap-3">
        <div class="flex justify-between items-center text-xs text-slate-500 border-b border-slate-100 pb-2">
          <span class="font-semibold uppercase tracking-wider">Estimasi Nilai Pasar Wajar</span>
          <span class="glass-pill glass-pill-tier-${result.tier}">Strata ${result.tier.toUpperCase()}</span>
        </div>
        <div class="text-3xl font-extrabold font-mono text-slate-900 tracking-tight">${formatUSD(result.estimatedPrice)}</div>
        <div class="text-xs font-semibold text-emerald-700 font-mono">&asymp; ${formatIDRBillions(result.estimatedPrice)} &bull; ${formatUSD(result.pricePerSqFt)} / sq.ft</div>
        <div class="pt-2 border-t border-slate-100 text-xs text-slate-500 flex justify-between font-mono">
          <span>Selang Keyakinan 90%:</span>
          <span class="font-bold text-slate-800">${formatUSD(result.p10)} &ndash; ${formatUSD(result.p90)}</span>
        </div>
      </div>

      <div class="glass-card flex flex-col gap-3">
        <h4 class="font-bold text-xs text-slate-800 uppercase tracking-wider">Atribusi Fitur Marjinal (SHAP)</h4>
        ${renderHorizontalBarChart(result.shap.map(s => ({
          label: s.feature,
          value: s.value,
          displayValue: (s.dollar >= 0 ? '+' : '') + formatUSD(s.dollar)
        })))}
      </div>
    `;
  }

  container.querySelectorAll('input, select').forEach(el => {
    el.addEventListener('change', update);
    el.addEventListener('input', update);
  });

  update();
  return container;
}
