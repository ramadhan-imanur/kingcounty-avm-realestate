/**
 * KingCounty-AVM: Top Navigation Bar Component
 * Brand, Status Badges, and Desktop Collapsible Sidebar Button
 */

import { iconSidebarToggle, iconHome } from './icons.js';
import { appStore } from '../../core/state.js';

export function renderNavbar() {
  const header = document.createElement('header');
  header.className = 'app-header flex items-center justify-between px-5 py-3.5 border-b border-slate-200/80 bg-white/80 backdrop-blur-md sticky top-0 z-30';

  header.innerHTML = `
    <!-- Brand & Breadcrumb -->
    <div class="flex items-center gap-3 select-none">
      <div class="w-9 h-9 rounded-xl bg-gradient-to-tr from-emerald-700 to-teal-500 flex items-center justify-center text-white shadow-md shadow-emerald-700/25 border border-emerald-400/40">
        ${iconHome('w-5 h-5')}
      </div>
      <div class="flex flex-col">
        <div class="flex items-center gap-1.5">
          <span class="text-base font-extrabold tracking-tight text-slate-900 leading-none">KingCounty</span>
          <span class="text-base font-extrabold tracking-tight text-emerald-600 leading-none">AVM</span>
          <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
        </div>
        <span class="text-[10px] font-medium text-slate-500 tracking-wide mt-0.5">Valuasi Cerdas Properti & Riset Spasial</span>
      </div>

      <div class="hidden xl:flex items-center gap-1.5 ml-4 font-mono text-[11px] text-slate-400">
        <span>King County MLS</span>
        <span>&gt;</span>
        <span class="px-2 py-0.5 rounded-md bg-slate-100 text-slate-600 font-semibold border border-slate-200">Dataset 22.847 Unit</span>
      </div>

      <button id="sidebar-toggle-btn" type="button" aria-label="Toggle Sidebar" title="Tutup / Buka Menu Utama" class="ml-2 px-2.5 py-1.5 rounded-xl bg-white/80 hover:bg-white text-slate-700 hover:text-emerald-700 border border-slate-200 shadow-xs transition-all flex items-center gap-1.5 cursor-pointer text-xs font-bold select-none">
        ${iconSidebarToggle('w-3.5 h-3.5')}
        <span id="sidebar-toggle-text" class="hidden sm:inline text-[11px]">Tutup Menu</span>
      </button>
    </div>

    <!-- Quick Status Badges (Stitch Fidelity) -->
    <div class="flex items-center gap-2 text-xs font-mono">
      <span class="hidden md:inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-slate-50 text-slate-700 border border-slate-200 text-[11px]">
        <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
        Status: <b class="font-sans font-bold">Terverifikasi</b> (22.847)
      </span>
      <span class="hidden lg:inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-slate-50 text-slate-700 border border-slate-200 text-[11px]">
        <svg class="w-3 h-3 text-slate-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
        Inference: <b class="font-sans font-bold">34ms</b>
      </span>
      <span class="hidden sm:inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-emerald-50 text-emerald-800 border border-emerald-200 font-bold text-[11px]">
        <svg class="w-3 h-3 text-emerald-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
        IAAO: COD 7.14% (Pass)
      </span>
      <div class="w-8 h-8 rounded-full bg-gradient-to-tr from-emerald-800 to-teal-600 text-white flex items-center justify-center font-bold text-xs select-none shadow-xs">
        KC
      </div>
    </div>
  `;

  const toggleBtn = header.querySelector('#sidebar-toggle-btn');
  const toggleText = header.querySelector('#sidebar-toggle-text');

  toggleBtn.addEventListener('click', () => {
    const isCollapsed = document.body.classList.contains('sidebar-collapsed');
    if (isCollapsed) {
      document.body.classList.remove('sidebar-collapsed');
      toggleText.textContent = 'Tutup Menu';
      appStore.setState({ sidebarCollapsed: false });
    } else {
      document.body.classList.add('sidebar-collapsed');
      toggleText.textContent = 'Buka Menu';
      appStore.setState({ sidebarCollapsed: true });
    }
  });

  return header;
}
