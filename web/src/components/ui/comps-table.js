/**
 * KingCounty-AVM: Comparable Properties Table Component
 */

import { formatUSD, formatNumber } from '../../core/config.js';

export function renderCompsTable(comps, targetCoord = null) {
  if (!comps || comps.length === 0) {
    return `<div class="text-xs text-slate-500 py-3">Tidak ada data pembanding.</div>`;
  }

  const rows = comps.map((comp) => {
    const ppsqft = Math.round(comp.price / comp.sqft);
    const distText = comp.distance != null ? `${comp.distance.toFixed(2)} mi` : '-';

    return `
      <tr class="hover:bg-slate-50/60 transition-colors border-b border-slate-100 text-xs">
        <td class="py-2.5 font-medium text-slate-800">${comp.address}</td>
        <td class="py-2.5 font-mono text-slate-600">${comp.zipcode}</td>
        <td class="py-2.5 font-mono text-slate-600">${distText}</td>
        <td class="py-2.5 font-mono font-bold text-slate-900 text-right">${formatUSD(comp.price)}</td>
        <td class="py-2.5 font-mono text-slate-600 text-right">${formatNumber(comp.sqft)}</td>
        <td class="py-2.5 font-mono text-slate-600 text-right">${formatUSD(ppsqft)}</td>
      </tr>
    `;
  }).join('');

  return `
    <div class="overflow-x-auto">
      <table class="w-full text-left border-collapse">
        <thead>
          <tr class="text-[10px] text-slate-400 uppercase tracking-wider border-b border-slate-200">
            <th class="py-2">Alamat Properti</th>
            <th class="py-2">Kode Pos</th>
            <th class="py-2">Jarak</th>
            <th class="py-2 text-right">Harga Jual</th>
            <th class="py-2 text-right">Luas</th>
            <th class="py-2 text-right">$/sq.ft</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100">
          ${rows}
        </tbody>
      </table>
    </div>
  `;
}
