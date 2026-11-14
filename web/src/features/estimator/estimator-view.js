/**
 * KingCounty-AVM: Valuation Estimator View Component
 * Handles property parameter input controls and real-time inference rendering
 */

import { appStore } from '../../core/state.js';
import { formatUSD, formatIDRBillions, formatNumber } from '../../core/config.js';
import { DataService } from '../../core/data-service.js';
import { runAVMInference } from './avm-inference.js';
import { renderHorizontalBarChart } from '../../components/charts/simple-chart.js';

export function renderEstimatorView() {
  const container = document.createElement('div');
  container.className = 'estimator-view flex flex-col gap-6';

  const prop = appStore.getState().property;
  const zipcodes = DataService.getAllZipcodes();

  container.innerHTML = `
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
      <!-- Input Controls (Cols 1-6) -->
      <div class="lg:col-span-6 glass-card flex flex-col gap-4">
        <div class="border-b border-slate-100 pb-3">
          <h3 class="font-bold text-base text-slate-900">Parameter Fisik & Lokasi Properti</h3>
          <p class="text-xs text-slate-500">Sesuaikan atribut hunian untuk kalkulasi nilai pasar wajar seketika.</p>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3.5 text-xs">
          <div class="flex flex-col gap-1">
            <label class="font-semibold text-slate-700">Kode Pos Wilayah</label>
            <select id="est-zip" class="p-2 rounded-lg border border-slate-300 font-mono text-xs">
              ${zipcodes.map(z => `<option value="${z.code}" ${z.code === prop.zipcode ? 'selected' : ''}>${z.code} - ${z.name}</option>`).join('')}
            </select>
          </div>
          <div class="flex flex-col gap-1">
            <label class="font-semibold text-slate-700">Luas Bangunan (sqft)</label>
            <input type="number" id="est-sqft" value="${prop.sqft_living}" step="50" class="p-2 rounded-lg border border-slate-300 font-mono font-bold">
          </div>
        </div>

        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
          <div class="flex flex-col gap-1">
            <label class="font-semibold text-slate-700">Kamar Tidur</label>
            <select id="est-beds" class="p-2 rounded-lg border border-slate-300 font-mono">
              ${[1, 2, 3, 4, 5, 6].map(n => `<option value="${n}" ${n === prop.bedrooms ? 'selected' : ''}>${n} KT</option>`).join('')}
            </select>
          </div>
          <div class="flex flex-col gap-1">
            <label class="font-semibold text-slate-700">Kamar Mandi</label>
            <select id="est-baths" class="p-2 rounded-lg border border-slate-300 font-mono">
              ${[1, 1.5, 2, 2.5, 3, 3.5, 4].map(n => `<option value="${n}" ${n === prop.bathrooms ? 'selected' : ''}>${n} KM</option>`).join('')}
            </select>
          </div>
          <div class="flex flex-col gap-1">
            <label class="font-semibold text-slate-700">Grade (1-13)</label>
            <input type="number" id="est-grade" min="4" max="13" value="${prop.grade}" class="p-2 rounded-lg border border-slate-300 font-mono">
          </div>
          <div class="flex flex-col gap-1">
            <label class="font-semibold text-slate-700">Kondisi (1-5)</label>
            <input type="number" id="est-cond" min="1" max="5" value="${prop.condition}" class="p-2 rounded-lg border border-slate-300 font-mono">
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

      <!-- Valuation Output (Cols 7-12) -->
      <div id="est-output-panel" class="lg:col-span-6 flex flex-col gap-4">
        <!-- Rendered dynamically -->
      </div>
    </div>
  `;

  function update() {
    const updatedProp = {
      ...appStore.getState().property,
      zipcode: container.querySelector('#est-zip').value,
      sqft_living: Number(container.querySelector('#est-sqft').value) || 2000,
      bedrooms: Number(container.querySelector('#est-beds').value),
      bathrooms: Number(container.querySelector('#est-baths').value),
      grade: Number(container.querySelector('#est-grade').value),
      condition: Number(container.querySelector('#est-cond').value),
      waterfront: container.querySelector('#est-water').checked ? 1 : 0,
      has_view: container.querySelector('#est-view').checked ? 1 : 0
    };

    const result = runAVMInference(updatedProp);
    appStore.setState({ property: updatedProp, valuation: result });

    const outPanel = container.querySelector('#est-output-panel');
    outPanel.innerHTML = `
      <div class="glass-card border-2 border-emerald-600/20 flex flex-col gap-3">
        <div class="flex justify-between items-center text-xs text-slate-500 border-b border-slate-100 pb-2">
          <span class="font-semibold uppercase tracking-wider">Estimasi Nilai Pasar Wajar</span>
          <span class="glass-pill glass-pill-${result.tier}">Strata ${result.tier.toUpperCase()}</span>
        </div>
        <div class="text-3xl font-extrabold font-mono text-slate-900 tracking-tight">
          ${formatUSD(result.estimatedPrice)}
        </div>
        <div class="text-xs font-semibold text-emerald-700 font-mono">
          ≈ ${formatIDRBillions(result.estimatedPrice)} • ${formatUSD(result.pricePerSqFt)} / sq.ft
        </div>
        <div class="pt-2 border-t border-slate-100 text-xs text-slate-500 flex justify-between font-mono">
          <span>Selang Keyakinan 90%:</span>
          <span class="font-bold text-slate-800">${formatUSD(result.p10)} – ${formatUSD(result.p90)}</span>
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
