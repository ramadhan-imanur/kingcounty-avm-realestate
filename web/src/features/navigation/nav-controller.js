/**
 * Aeris Navigation & Desktop Chassis Controller
 * Tab routing, URL hash synchronization, and responsive drawer state
 */

import { store } from '../../core/state.js';

const TAB_ALIASES = Object.freeze({
  valuator: 'tab-valuator',
  kalkulator: 'tab-valuator',
  market: 'tab-market',
  pasar: 'tab-market',
  renovation: 'tab-renovation',
  renovasi: 'tab-renovation',
  audit: 'tab-audit',
  kualitas: 'tab-audit'
});

export function initNavigation() {
  const navLinks = document.querySelectorAll('aside [data-tab-target]');
  const tabs = document.querySelectorAll('.tab-content');

  function switchTab(targetId, updateUrl = false) {
    tabs.forEach(tab => tab.classList.remove('active'));

    navLinks.forEach(link => {
      link.classList.remove('active', 'bg-emerald-600', 'text-white', 'shadow-md', 'shadow-emerald-700/20');
      if (!link.classList.contains('active')) {
        link.classList.add('text-slate-600', 'hover:bg-white/60');
      }
    });

    const selectedTab = document.getElementById(targetId);
    if (selectedTab) selectedTab.classList.add('active');

    navLinks.forEach(link => {
      if (link.getAttribute('data-tab-target') === targetId) {
        link.classList.add('active', 'bg-emerald-600', 'text-white', 'shadow-md', 'shadow-emerald-700/20');
        link.classList.remove('text-slate-600', 'hover:bg-white/60');
      }
    });

    window.scrollTo(0, 0);
    const mainWorkspace = document.querySelector('main');
    if (mainWorkspace) mainWorkspace.scrollTop = 0;

    if (updateUrl && window.location.protocol !== 'file:') {
      try {
        if (window.history && window.history.replaceState) {
          window.history.replaceState(null, null, '#' + targetId);
        }
      } catch (err) {}
    }

    store.set('activeTab', targetId);
    window.scrollTo(0, 0);
  }

  navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const target = link.getAttribute('data-tab-target');
      switchTab(target, true);
    });
  });

  let hash = window.location.hash.replace('#', '');
  if (TAB_ALIASES[hash]) hash = TAB_ALIASES[hash];

  const bodyDefault = document.body.getAttribute('data-default-tab') || 'tab-valuator';
  if (hash && document.getElementById(hash)) {
    switchTab(hash, false);
  } else {
    switchTab(bodyDefault, false);
  }
}

export function initSidebarToggle() {
  const body = document.body;
  const toggleBtn = document.getElementById('sidebar-toggle-btn');
  const closeBtn = document.getElementById('sidebar-close-btn');
  const reopenFloatBtn = document.getElementById('sidebar-reopen-float-btn');
  const toggleText = document.getElementById('sidebar-toggle-text');

  function setSidebarState(collapsed) {
    if (collapsed) {
      body.classList.add('sidebar-collapsed');
      if (toggleText) toggleText.textContent = 'Buka Menu';
      if (toggleBtn) {
        toggleBtn.setAttribute('title', 'Buka Menu Utama (Desktop)');
        toggleBtn.classList.add('bg-emerald-50', 'text-emerald-700', 'border-emerald-200');
      }
      try { localStorage.setItem('kingcounty_sidebar_collapsed', 'true'); } catch (e) {}
    } else {
      body.classList.remove('sidebar-collapsed');
      if (toggleText) toggleText.textContent = 'Tutup Menu';
      if (toggleBtn) {
        toggleBtn.setAttribute('title', 'Tutup Menu Utama (Desktop)');
        toggleBtn.classList.remove('bg-emerald-50', 'text-emerald-700', 'border-emerald-200');
      }
      try { localStorage.setItem('kingcounty_sidebar_collapsed', 'false'); } catch (e) {}
    }
    store.set('isSidebarCollapsed', collapsed);
  }

  if (toggleBtn) toggleBtn.addEventListener('click', (e) => { e.preventDefault(); setSidebarState(!body.classList.contains('sidebar-collapsed')); });
  if (closeBtn) closeBtn.addEventListener('click', (e) => { e.preventDefault(); setSidebarState(true); });
  if (reopenFloatBtn) reopenFloatBtn.addEventListener('click', (e) => { e.preventDefault(); setSidebarState(false); });

  try {
    const saved = localStorage.getItem('kingcounty_sidebar_collapsed');
    if (saved === 'true' && window.innerWidth >= 768) setSidebarState(true);
  } catch (e) {}
}
