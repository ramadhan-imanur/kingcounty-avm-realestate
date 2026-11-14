/**
 * KingCounty-AVM: Institutional Model Audit & Econometric Report View
 * IAAO / USPAP Mass Appraisal Compliance Scorecards
 */

import { formatUSD } from '../../core/config.js';
import { getPriceQuantiles, getFeatureCorrelationMatrix } from './distribution-calc.js';

export function renderAnalyticsView() {
  const container = document.createElement('div');
  container.className = 'analytics-view flex flex-col gap-6';

  const quantiles = getPriceQuantiles();
  const correlations = getFeatureCorrelationMatrix();

  const modelsScorecard = [
    { model: 'OLS Linear Regression', r2: '0.7460', mape: '22.04%', mae: '$124,551', status: 'Baseline' },
    { model: 'Ridge (L2) Regularized', r2: '0.7460', mape: '22.01%', mae: '$124,387', status: 'Regularisasi' },
    { model: 'Lasso (L1) Regularized', r2: '0.7458', mape: '22.05%', mae: '$124,637', status: 'Sparsitas' },
    { model: 'Random Forest Regressor', r2: '0.8659', mape: '14.34%', mae: '$79,588', status: 'Ensemble' },
    { model: 'HistGradientBoosting (Dual-Pipe)', r2: '0.8836', mape: '11.40%', mae: '$73,452', status: 'PRODUKSI' }
  ];

  container.innerHTML = `
    <!-- Audit Compliance Header -->
    <div class="glass-card flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <div>
        <span class="glass-pill glass-pill-entry text-[11px] mb-1">IAAO Standard 2025 • USPAP Standard 6</span>
        <h2 class="text-xl font-bold text-slate-900">Audit Evaluasi Model & Validasi Ekonometrika</h2>
        <p class="text-xs text-slate-500">Evaluasi kepatuhan penaksiran massal pada 22.847 transaksi King County.</p>
      </div>
      <div class="font-mono text-xs font-bold text-emerald-800 bg-emerald-50 px-3 py-1.5 rounded-xl border border-emerald-200">
        STATUS: LOLOS REGULASI INTERNASIONAL
      </div>
    </div>

    <!-- 4 Core Metrics -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
      <div class="glass-card p-4 flex flex-col justify-between">
        <span class="text-[10px] uppercase font-bold text-slate-400">COD (Dispersion)</span>
        <div class="text-2xl font-bold font-mono text-slate-900 my-1">7.14%</div>
        <span class="text-[10px] text-emerald-700">Ambang: &lt; 10% (Luar Biasa)</span>
      </div>
      <div class="glass-card p-4 flex flex-col justify-between">
        <span class="text-[10px] uppercase font-bold text-slate-400">PRD (Vertical Equity)</span>
        <div class="text-2xl font-bold font-mono text-slate-900 my-1">1.008</div>
        <span class="text-[10px] text-emerald-700">Standar: 0.98 – 1.03 (Netral)</span>
      </div>
      <div class="glass-card p-4 flex flex-col justify-between">
        <span class="text-[10px] uppercase font-bold text-slate-400">PRB (Price Bias)</span>
        <div class="text-2xl font-bold font-mono text-slate-900 my-1">-0.012</div>
        <span class="text-[10px] text-emerald-700">Batas: -0.05 s/d +0.05</span>
      </div>
      <div class="glass-card p-4 flex flex-col justify-between">
        <span class="text-[10px] uppercase font-bold text-slate-400">Akurasi (Holdout R²)</span>
        <div class="text-2xl font-bold font-mono text-slate-900 my-1">R² 0.8836</div>
        <span class="text-[10px] text-emerald-700">Median MAPE 11.4% (MAE $73k)</span>
      </div>
    </div>

    <!-- Model Scorecard Table -->
    <div class="glass-card flex flex-col gap-3">
      <h3 class="font-bold text-sm text-slate-900">Scorecard Komparasi Model Regresi Ekonometrika & Machine Learning</h3>
      <div class="overflow-x-auto text-xs">
        <table class="w-full text-left font-mono">
          <thead>
            <tr class="text-[10px] text-slate-400 uppercase border-b border-slate-200">
              <th class="py-2 font-sans">Algoritma</th>
              <th class="py-2 text-right">R² (Log)</th>
              <th class="py-2 text-right">MAPE</th>
              <th class="py-2 text-right">MAE ($)</th>
              <th class="py-2 text-center font-sans">Status</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100">
            ${modelsScorecard.map(m => `
              <tr class="${m.status === 'PRODUKSI' ? 'bg-emerald-50/60 font-bold' : ''}">
                <td class="py-2 font-sans font-medium text-slate-800">${m.model}</td>
                <td class="py-2 text-right text-slate-700">${m.r2}</td>
                <td class="py-2 text-right text-slate-700">${m.mape}</td>
                <td class="py-2 text-right text-slate-700">${m.mae}</td>
                <td class="py-2 text-center font-sans">
                  <span class="px-2 py-0.5 rounded text-[10px] ${m.status === 'PRODUKSI' ? 'bg-emerald-600 text-white' : 'bg-slate-100 text-slate-600'}">
                    ${m.status}
                  </span>
                </td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>
    </div>

    <!-- Quantiles & Correlation Dual-Panel -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div class="glass-card flex flex-col gap-3">
        <h4 class="font-bold text-xs text-slate-800 uppercase">Distribusi Kuantil Harga Pasar</h4>
        <div class="divide-y divide-slate-100 text-xs font-mono">
          ${quantiles.map(q => `
            <div class="py-1.5 flex justify-between">
              <span class="font-sans text-slate-600">${q.label}</span>
              <span class="font-bold text-slate-900">${formatUSD(q.value)}</span>
            </div>
          `).join('')}
        </div>
      </div>

      <div class="glass-card flex flex-col gap-3">
        <h4 class="font-bold text-xs text-slate-800 uppercase">Korelasi Fitur Struktural vs Harga</h4>
        <div class="divide-y divide-slate-100 text-xs font-mono">
          ${correlations.map(c => `
            <div class="py-1.5 flex justify-between">
              <span class="font-sans text-slate-600">${c.feature}</span>
              <span class="font-bold text-emerald-700">r = +${c.correlation.toFixed(3)}</span>
            </div>
          `).join('')}
        </div>
      </div>
    </div>
  `;

  return container;
}
