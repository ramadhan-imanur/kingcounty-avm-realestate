/**
 * KingCounty-AVM: Sidebar Navigation Component
 * Independent fixed navigation with institutional audit badge
 */

import { iconHome, iconMap, iconAnalytics, iconSimulator } from './icons.js';
import { appStore } from '../../core/state.js';

export function renderSidebar() {
  const aside = document.createElement('aside');
  aside.id = 'main-sidebar';
  aside.className = 'app-sidebar p-4 flex flex-col justify-between';

  const navItems = [
    { id: 'estimator', label: 'Kalkulator Nilai', icon: iconHome },
    { id: 'map', label: 'Jelajah Pasar', icon: iconMap },
    { id: 'simulator', label: 'Simulasi Renovasi', icon: iconSimulator },
    { id: 'analytics', label: 'Kualitas & Audit', icon: iconAnalytics }
  ];

  aside.innerHTML = `
    <div class="flex flex-col gap-2">
      <div class="flex items-center justify-between px-3 mb-1">
        <span class="font-mono text-[11px] font-bold uppercase tracking-wider text-slate-400">Menu Utama</span>
        <button id="sidebar-close-btn" type="button" title="Tutup Menu Utama (Desktop)" class="hidden md:flex items-center justify-center w-6 h-6 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-200/60 transition-colors cursor-pointer">
          <svg class="w-3.5 h-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="15 18 9 12 15 6"></polyline></svg>
        </button>
      </div>

      <nav class="flex md:flex-col gap-1.5 overflow-x-auto md:overflow-visible">
        ${navItems.map(item => `
          <button data-tab="${item.id}" class="nav-item nav-btn w-full flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-xs font-semibold text-slate-600 hover:bg-white/60 transition-all text-left cursor-pointer">
            ${item.icon('w-4 h-4')}
            <span>${item.label}</span>
          </button>
        `).join('')}
      </nav>
    </div>

    <!-- Institutional Governance Card (Stitch High-Fidelity) -->
    <div class="rounded-2xl bg-[#064e3b] text-white p-3.5 mt-4 flex flex-col gap-2 shadow-lg shadow-emerald-950/20 border border-emerald-500/20">
      <div class="flex items-center gap-1.5 text-xs font-bold text-emerald-300">
        <svg class="w-4 h-4 text-emerald-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
        <span>IAAO AUDIT PASS</span>
      </div>
      <p class="text-[11px] text-emerald-100/80 leading-relaxed font-sans">
        Model dievaluasi berkala menggunakan validasi silang bertingkat (Stratified 5-Fold) & standar penilaian AVM internasional.
      </p>
      <div class="pt-2 border-t border-emerald-700/50 flex flex-col gap-1 font-mono text-[10px]">
        <div class="flex justify-between">
          <span class="text-emerald-300/80">Test MAPE:</span>
          <span class="font-bold text-white">11.4% (R² 0.89)</span>
        </div>
        <div class="flex justify-between">
          <span class="text-emerald-300/80">Klaster Geo:</span>
          <span class="font-bold text-white">k = 6 Mikromarket</span>
        </div>
        <div class="flex justify-between">
          <span class="text-emerald-300/80">Coverage:</span>
          <span class="font-bold text-white">King County, WA</span>
        </div>
      </div>
    </div>
  `;

  function updateActive(activeTab) {
    aside.querySelectorAll('.nav-btn').forEach(btn => {
      const isTarget = btn.dataset.tab === activeTab;
      if (isTarget) {
        btn.className = 'nav-item nav-btn active w-full flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-xs font-bold bg-[#006948] text-white shadow-md shadow-emerald-950/25 text-left transition-all';
      } else {
        btn.className = 'nav-item nav-btn w-full flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-xs font-semibold text-slate-600 hover:bg-white/60 text-left transition-all';
      }
    });
  }

  aside.querySelectorAll('.nav-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      appStore.setState({ activeTab: btn.dataset.tab });
    });
  });

  const closeBtn = aside.querySelector('#sidebar-close-btn');
  if (closeBtn) {
    closeBtn.addEventListener('click', () => {
      document.body.classList.add('sidebar-collapsed');
      const toggleText = document.querySelector('#sidebar-toggle-text');
      if (toggleText) toggleText.textContent = 'Buka Menu';
      appStore.setState({ sidebarCollapsed: true });
    });
  }

  appStore.subscribe('activeTab', (newTab) => {
    updateActive(newTab);
  });

  updateActive(appStore.getState().activeTab);
  return aside;
}
