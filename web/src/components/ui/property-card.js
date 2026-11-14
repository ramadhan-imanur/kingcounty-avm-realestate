/**
 * KingCounty-AVM: Property Metric Card Component
 */

import { formatUSD, formatNumber } from '../../core/config.js';

export function renderMetricCard(title, value, subtitle, delta = null, deltaPositive = true) {
  const deltaHtml = delta ? `
    <span class="text-xs font-semibold ${deltaPositive ? 'text-emerald-700' : 'text-rose-700'}">
      ${delta}
    </span>
  ` : '';

  return `
    <div class="glass-card flex flex-col justify-between hover:translate-y-[-2px] transition-transform">
      <div class="flex items-center justify-between text-xs text-slate-500 font-semibold uppercase tracking-wider mb-2">
        <span>${title}</span>
        ${deltaHtml}
      </div>
      <div class="text-2xl font-bold font-mono text-slate-900 tracking-tight">
        ${value}
      </div>
      <div class="text-xs text-slate-500 mt-1 font-sans">
        ${subtitle}
      </div>
    </div>
  `;
}

export function renderCompCard(comp, targetPrice) {
  const matchPct = Math.max(90, Math.min(99, Math.round(100 - Math.abs(comp.price - targetPrice) / targetPrice * 100)));

  return `
    <div class="glass-card border border-slate-200/80 p-3.5 flex flex-col gap-1.5">
      <div class="flex items-center justify-between text-xs">
        <span class="font-bold text-slate-800 truncate">${comp.address}</span>
        <span class="px-2 py-0.5 rounded font-mono font-bold text-[10px] bg-emerald-100 text-emerald-800">
          Match ${matchPct}%
        </span>
      </div>
      <div class="text-lg font-bold font-mono text-slate-900">
        ${formatUSD(comp.price)}
      </div>
      <div class="text-xs text-slate-500 flex items-center gap-2">
        <span>${comp.beds} KT</span>
        <span>•</span>
        <span>${comp.baths} KM</span>
        <span>•</span>
        <span>${formatNumber(comp.sqft)} sqft</span>
      </div>
    </div>
  `;
}
