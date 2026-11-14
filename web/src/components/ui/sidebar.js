/**
 * KingCounty-AVM: Sidebar Navigation Component
 * Independent fixed navigation with institutional audit badge
 */

import { iconHome, iconMap, iconAnalytics, iconSimulator } from './icons.js';
import { appStore } from '../../core/state.js';

export function renderSidebar() {
  const aside = document.createElement('aside');
  aside.className = 'app-sidebar p-4 flex flex-col justify-between';

  const navItems = [
    { id: 'estimator', label: 'Kalkulator Nilai', icon: iconHome },
    { id: 'map', label: 'Jelajah Spasial', icon: iconMap },
    { id: 'analytics', label: 'Analisis Pasar & Audit', icon: iconAnalytics },
    { id: 'simulator', label: 'Simulasi Investasi', icon: iconSimulator }
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
          <button data-tab="${item.id}" class="nav-btn w-full flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-xs font-semibold text-slate-600 hover:bg-white/60 transition-all text-left cursor-pointer">
            ${item.icon('w-4 h-4')}
            <span>${item.label}</span>
          </button>
        `).join('')}
      </nav>
    </div>

    <!-- Governance Status Box -->
    <div class="glass-card border border-emerald-600/20 p-3 mt-4 text-xs font-mono flex flex-col gap-1">
      <div class="text-[10px] font-bold text-emerald-800 uppercase flex items-center gap-1.5">
        <span class="w-1.5 h-1.5 rounded-full bg-emerald-600"></span>
        <span>IAAO Audit Pass</span>
      </div>
      <div class="text-slate-600 text-[11px]">COD: <b>7.14%</b> • R²: <b>0.8836</b></div>
      <div class="text-[10px] text-slate-400 mt-1">King County Dual-Pipe v4.2</div>
    </div>
  `;

  // Function to highlight active tab
  function updateActive(activeTab) {
    aside.querySelectorAll('.nav-btn').forEach(btn => {
      const isTarget = btn.dataset.tab === activeTab;
      if (isTarget) {
        btn.className = 'nav-btn w-full flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-xs font-bold bg-emerald-600 text-white shadow-md shadow-emerald-700/20 text-left transition-all';
      } else {
        btn.className = 'nav-btn w-full flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-xs font-semibold text-slate-600 hover:bg-white/60 text-left transition-all';
      }
    });
  }

  // Click handlers
  aside.querySelectorAll('.nav-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      appStore.setState({ activeTab: btn.dataset.tab });
    });
  });

  // Close button handler
  const closeBtn = aside.querySelector('#sidebar-close-btn');
  if (closeBtn) {
    closeBtn.addEventListener('click', () => {
      document.body.classList.add('sidebar-collapsed');
      const toggleText = document.querySelector('#sidebar-toggle-text');
      if (toggleText) toggleText.textContent = 'Buka Menu';
      appStore.setState({ sidebarCollapsed: true });
    });
  }

  // Subscribe to state changes
  appStore.subscribe('activeTab', (newTab) => {
    updateActive(newTab);
  });

  updateActive(appStore.getState().activeTab);
  return aside;
}
