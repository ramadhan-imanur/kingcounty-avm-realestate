/**
 * Renovation ROI Simulator Controller
 * Value-add simulations, cost-benefit modeling, and projected appreciation
 */

import { formatCurrency, animateValue, debounce } from '../../core/config.js';
import { store } from '../../core/state.js';

const RENOVATION_UPGRADES = Object.freeze([
  { id: 'renov-bath', cost: 24000, valueGain: 38500 },
  { id: 'renov-kitchen', cost: 48000, valueGain: 72000 },
  { id: 'renov-basement', cost: 36000, valueGain: 52000 },
  { id: 'renov-deck', cost: 16000, valueGain: 22500 },
  { id: 'renov-grade', cost: 65000, valueGain: 125000 },
  { id: 'renov-energy', cost: 15000, valueGain: 19500 }
]);

export function initRenovationSimulator() {
  const baseValueInput = document.getElementById('renov-base-value');
  const checkboxes = document.querySelectorAll('.renov-toggle');

  if (!checkboxes.length) return;

  const debouncedCalc = debounce(calculateRenovationROI, 40);

  checkboxes.forEach(cb => {
    cb.addEventListener('change', debouncedCalc);
  });

  if (baseValueInput) {
    baseValueInput.addEventListener('input', debouncedCalc);
  }

  calculateRenovationROI();
}

export function calculateRenovationROI() {
  const baseVal = parseFloat(document.getElementById('renov-base-value')?.value || 650000);
  let totalCost = 0;
  let totalAppreciation = 0;

  RENOVATION_UPGRADES.forEach(u => {
    const el = document.getElementById(u.id);
    if (el && el.checked) {
      totalCost += u.cost;
      totalAppreciation += u.valueGain;
    }
  });

  const netProfit = totalAppreciation - totalCost;
  const roiPct = totalCost > 0 ? Math.round((totalAppreciation / totalCost) * 100) : 0;
  const projectedVal = baseVal + totalAppreciation;

  store.set('renovation', { baseValue: baseVal, totalCost, totalAppreciation, netProfit, roiPct, projectedVal });

  requestAnimationFrame(() => {
    const totalCostEl = document.getElementById('renov-total-cost');
    const appreciationEl = document.getElementById('renov-total-appreciation');
    const netProfitEl = document.getElementById('renov-net-profit');
    const roiBadgeEl = document.getElementById('renov-roi-badge');
    const projectedValEl = document.getElementById('renov-projected-val');

    if (totalCostEl) totalCostEl.textContent = formatCurrency(totalCost);
    if (appreciationEl) appreciationEl.textContent = formatCurrency(totalAppreciation);

    if (netProfitEl) {
      netProfitEl.textContent = (netProfit >= 0 ? '+' : '') + formatCurrency(netProfit);
      netProfitEl.className = netProfit >= 0
        ? 'text-2xl font-bold font-mono text-shap-positive'
        : 'text-2xl font-bold font-mono text-shap-negative';
    }

    if (roiBadgeEl) {
      roiBadgeEl.textContent = `${roiPct}% ROI Gross`;
      roiBadgeEl.className = roiPct >= 120
        ? 'px-3 py-1 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800 border border-emerald-300'
        : 'px-3 py-1 rounded-full text-xs font-bold bg-sky-100 text-sky-800 border border-sky-300';
    }

    if (projectedValEl) animateValue(projectedValEl, projectedVal);
  });
}
