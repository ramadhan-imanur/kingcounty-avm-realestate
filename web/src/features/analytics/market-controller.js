/**
 * Market Analytics & Distribution Controller
 * Aggregates cluster statistics, comps rankings, and quantile summaries
 */

import { formatCurrency } from '../../core/config.js';
import { KING_COUNTY_DATA } from '../../services/data-service.js';

export function initMarketAnalytics() {
  const container = document.getElementById('tab-market');
  if (!container) return;

  // Hydrate cluster summaries or comparable list if present
  renderClusterHighlights();
}

export function renderClusterHighlights() {
  const clusterGrid = document.getElementById('market-clusters-summary');
  if (!clusterGrid) return;

  const fragment = document.createDocumentFragment();
  KING_COUNTY_DATA.clusters.forEach(cl => {
    const item = document.createElement('div');
    item.className = 'glass-card-subtle p-3 flex justify-between items-center text-xs';
    item.innerHTML = `
      <div>
        <div class="font-bold text-slate-800">Klaster ${cl.id}: ${cl.name}</div>
        <div class="text-slate-500">${cl.units.toLocaleString()} unit terverifikasi</div>
      </div>
      <div class="text-right">
        <div class="font-mono font-bold text-emerald-700">${formatCurrency(cl.medianPrice)}</div>
        <div class="text-[10px] text-slate-400">Median</div>
      </div>
    `;
    fragment.appendChild(item);
  });

  clusterGrid.innerHTML = '';
  clusterGrid.appendChild(fragment);
}
