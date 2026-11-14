/**
 * KingCounty-AVM: Renovation Packages Panel Component
 */

import { formatUSD } from '../../core/config.js';
import { RENOVATION_PACKAGES } from './mortgage-math.js';

export function renderRenovationChecklist(selectedIds, onToggle) {
  const container = document.createElement('div');
  container.className = 'flex flex-col gap-2 text-xs';

  container.innerHTML = RENOVATION_PACKAGES.map(pkg => `
    <label class="p-2.5 rounded-lg border border-slate-200/80 hover:bg-slate-50 flex items-center justify-between cursor-pointer transition-colors">
      <div class="flex items-center gap-2.5">
        <input type="checkbox" data-reno-id="${pkg.id}" ${selectedIds.has(pkg.id) ? 'checked' : ''} class="rounded text-emerald-600">
        <span class="font-semibold text-slate-800">${pkg.name}</span>
      </div>
      <div class="text-right font-mono text-[11px]">
        <span class="text-slate-500">${formatUSD(pkg.cost)}</span>
        <span class="text-emerald-700 font-bold ml-1.5">+${formatUSD(pkg.appreciation)}</span>
      </div>
    </label>
  `).join('');

  container.querySelectorAll('input[data-reno-id]').forEach(cb => {
    cb.addEventListener('change', e => {
      onToggle(e.target.dataset.renoId, e.target.checked);
    });
  });

  return container;
}
