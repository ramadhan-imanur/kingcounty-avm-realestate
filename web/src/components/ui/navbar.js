/**
 * KingCounty-AVM: Top Navigation Bar Component
 * Includes Brand, Status Badges, and Desktop Collapsible Sidebar Button
 */

import { iconSidebarToggle, iconHome } from './icons.js';
import { appStore } from '../../core/state.js';

export function renderNavbar() {
  const header = document.createElement('header');
  header.className = 'app-header';

  header.innerHTML = `
    <!-- Brand & Toggle -->
    <div class="flex items-center gap-4">
      <div class="flex items-center gap-3 select-none">
        <div class="w-9 h-9 rounded-xl bg-gradient-to-tr from-emerald-700 to-teal-500 flex items-center justify-center text-white shadow-md shadow-emerald-700/25 border border-emerald-400/40">
          ${iconHome('w-5 h-5')}
        </div>
        <div class="flex flex-col">
          <div class="flex items-center gap-1">
            <span class="text-base font-extrabold tracking-tight text-slate-900 leading-none">KingCounty</span>
            <span class="text-base font-extrabold tracking-tight text-emerald-600 leading-none">AVM</span>
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 ml-0.5"></span>
          </div>
          <span class="text-[10px] font-medium text-slate-500 tracking-wide mt-0.5">Valuasi Cerdas & Riset Spasial</span>
        </div>
      </div>

      <!-- Desktop Sidebar Toggle Button -->
      <button id="sidebar-toggle-btn" type="button" aria-label="Toggle Sidebar" title="Tutup / Buka Menu Utama" class="px-2.5 py-1.5 rounded-xl bg-white/70 hover:bg-white text-slate-700 hover:text-emerald-700 border border-slate-200/80 shadow-xs transition-all flex items-center gap-1.5 cursor-pointer text-xs font-bold select-none">
        ${iconSidebarToggle('w-4 h-4')}
        <span id="sidebar-toggle-text" class="hidden sm:inline">Tutup Menu</span>
      </button>
    </div>

    <!-- Quick Status Badges -->
    <div class="flex items-center gap-2.5 text-xs font-mono">
      <span class="hidden md:inline-flex px-2.5 py-1 rounded-full bg-slate-100 text-slate-600 border border-slate-200">
        Dataset: 22.847 Unit
      </span>
      <span class="hidden lg:inline-flex px-2.5 py-1 rounded-full bg-emerald-50 text-emerald-800 border border-emerald-200 font-bold">
        IAAO: COD 7.14% (Pass)
      </span>
      <div class="w-8 h-8 rounded-full bg-gradient-to-tr from-emerald-700 to-teal-600 text-white flex items-center justify-center font-bold text-xs select-none">
        KC
      </div>
    </div>
  `;

  // Toggle button listener
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
