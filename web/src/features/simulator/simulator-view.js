/**
 * KingCounty-AVM: Investment Feasibility Simulator View
 */

import { appStore } from '../../core/state.js';
import { formatUSD } from '../../core/config.js';
import {
  calculateMonthlyMortgage,
  calculateCapRate,
  calculatePriceToRentRatio,
  RENOVATION_PACKAGES
} from './mortgage-math.js';
import { renderRenovationChecklist } from './renovation-panel.js';

export function renderSimulatorView() {
  const container = document.createElement('div');
  container.className = 'simulator-view flex flex-col gap-6';

  let basePrice = appStore.getState().valuation.estimatedPrice || 650000;
  let downPaymentPct = 20, interestRate = 6.5, loanTerm = 30;
  let monthlyRent = Math.round(basePrice * 0.0055);
  const selectedRenovations = new Set(['kitchen']);

  function render() {
    const loanAmount = basePrice * (1 - downPaymentPct / 100);
    const monthlyMortgage = calculateMonthlyMortgage(loanAmount, interestRate, loanTerm);
    const prr = calculatePriceToRentRatio(basePrice, monthlyRent);
    const capRate = calculateCapRate(basePrice, monthlyRent);

    let renoCost = 0, renoAppr = 0;
    RENOVATION_PACKAGES.forEach(pkg => {
      if (selectedRenovations.has(pkg.id)) {
        renoCost += pkg.cost;
        renoAppr += pkg.appreciation;
      }
    });
    const renoProfit = renoAppr - renoCost;
    const renoRoi = renoCost > 0 ? Math.round((renoAppr / renoCost) * 100) : 0;

    container.innerHTML = `
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        <div class="lg:col-span-6 glass-card flex flex-col gap-4">
          <div class="border-b border-slate-100 pb-2">
            <h3 class="font-bold text-base text-slate-900">Parameter Pembiayaan & Investasi</h3>
            <p class="text-xs text-slate-500">Simulasi cicilan KPR / hipotek dan rasio kelayakan sewa.</p>
          </div>
          <div class="grid grid-cols-2 gap-3 text-xs">
            <div class="flex flex-col gap-1">
              <label class="font-semibold text-slate-700">Harga Properti ($)</label>
              <input type="number" id="sim-price" value="${basePrice}" step="25000" class="glass-input font-mono font-bold">
            </div>
            <div class="flex flex-col gap-1">
              <label class="font-semibold text-slate-700">Uang Muka (%)</label>
              <input type="number" id="sim-dp" value="${downPaymentPct}" min="5" max="50" step="5" class="glass-input font-mono">
            </div>
            <div class="flex flex-col gap-1">
              <label class="font-semibold text-slate-700">Bunga KPR (% p.a)</label>
              <input type="number" id="sim-rate" value="${interestRate}" min="3" max="12" step="0.25" class="glass-input font-mono">
            </div>
            <div class="flex flex-col gap-1">
              <label class="font-semibold text-slate-700">Tenor Pinjaman</label>
              <select id="sim-term" class="glass-input font-mono">
                <option value="15" ${loanTerm === 15 ? 'selected' : ''}>15 Tahun</option>
                <option value="30" ${loanTerm === 30 ? 'selected' : ''}>30 Tahun</option>
              </select>
            </div>
          </div>
          <div class="grid grid-cols-2 gap-3 pt-2 border-t border-slate-100">
            <div class="p-3 bg-slate-50 rounded-xl flex flex-col">
              <span class="text-[10px] uppercase font-bold text-slate-400">Cicilan Bulanan</span>
              <span class="text-lg font-bold font-mono text-slate-900">${formatUSD(monthlyMortgage)}</span>
              <span class="text-[10px] text-slate-500">Pinjaman: ${formatUSD(loanAmount)}</span>
            </div>
            <div class="p-3 bg-slate-50 rounded-xl flex flex-col">
              <span class="text-[10px] uppercase font-bold text-slate-400">Cap Rate & PRR</span>
              <span class="text-lg font-bold font-mono text-emerald-700">${capRate.toFixed(2)}%</span>
              <span class="text-[10px] text-slate-500">Price-to-Rent: ${prr.toFixed(1)}x</span>
            </div>
          </div>
        </div>

        <div class="lg:col-span-6 glass-card flex flex-col gap-4">
          <div class="border-b border-slate-100 pb-2 flex justify-between items-center">
            <div>
              <h3 class="font-bold text-base text-slate-900">Simulasi Paket Renovasi</h3>
              <p class="text-xs text-slate-500">Kenaikan ekuitas vs biaya modal aktual King County.</p>
            </div>
            <span class="font-mono text-xs font-bold px-2 py-0.5 rounded bg-emerald-100 text-emerald-800">ROI ${renoRoi}%</span>
          </div>
          <div id="reno-list-container"></div>
          <div class="p-3 rounded-xl bg-gradient-to-r from-emerald-900 to-teal-800 text-white flex justify-between items-center text-xs font-mono">
            <div>
              <div class="text-[10px] text-emerald-200">Estimasi Nilai Baru</div>
              <div class="text-xl font-bold">${formatUSD(basePrice + renoAppr)}</div>
            </div>
            <div class="text-right">
              <div class="text-[10px] text-emerald-200">Laba Bersih</div>
              <div class="text-lg font-bold text-emerald-300">+${formatUSD(renoProfit)}</div>
            </div>
          </div>
        </div>
      </div>
    `;

    const renoMount = container.querySelector('#reno-list-container');
    renoMount.appendChild(renderRenovationChecklist(selectedRenovations, (id, checked) => {
      if (checked) selectedRenovations.add(id);
      else selectedRenovations.delete(id);
      render();
    }));

    container.querySelector('#sim-price').addEventListener('input', e => { basePrice = Number(e.target.value) || 0; render(); });
    container.querySelector('#sim-dp').addEventListener('input', e => { downPaymentPct = Number(e.target.value) || 0; render(); });
    container.querySelector('#sim-rate').addEventListener('input', e => { interestRate = Number(e.target.value) || 0; render(); });
    container.querySelector('#sim-term').addEventListener('change', e => { loanTerm = Number(e.target.value) || 30; render(); });
  }

  render();
  return container;
}
