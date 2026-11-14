/**
 * KingCounty-AVM: Application Bootstrapper & View Router
 * Modular Feature-Sliced Orchestration (Zero Monolith, Strict LOC Bound)
 */

import { appStore } from './core/state.js';
import { renderNavbar } from './components/ui/navbar.js';
import { renderSidebar } from './components/ui/sidebar.js';
import { renderEstimatorView } from './features/estimator/estimator-view.js';
import { renderMapView } from './features/map/map-view.js';
import { renderAnalyticsView } from './features/analytics/analytics-view.js';
import { renderSimulatorView } from './features/simulator/simulator-view.js';

document.addEventListener('DOMContentLoaded', () => {
  const chassis = document.querySelector('.glass-chassis');
  if (!chassis) return;

  // 1. Mount Top Navbar
  const navbar = renderNavbar();
  chassis.appendChild(navbar);

  // 2. Mount Workspace Flex Container
  const workspace = document.createElement('div');
  workspace.className = 'main-workspace-container';
  chassis.appendChild(workspace);

  // 3. Mount Left Sidebar
  const sidebar = renderSidebar();
  workspace.appendChild(sidebar);

  // 4. Mount Floating Reopen Button (Desktop)
  const reopenBtn = document.createElement('button');
  reopenBtn.id = 'sidebar-reopen-float-btn';
  reopenBtn.type = 'button';
  reopenBtn.title = 'Buka Menu Utama';
  reopenBtn.className = 'hidden fixed left-6 top-24 z-40 px-3 py-2 rounded-xl bg-emerald-700 hover:bg-emerald-800 text-white shadow-lg text-xs font-bold items-center gap-2 cursor-pointer select-none';
  reopenBtn.innerHTML = `
    <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
      <line x1="9" y1="3" x2="9" y2="21"></line>
    </svg>
    <span>Buka Menu</span>
  `;
  reopenBtn.addEventListener('click', () => {
    document.body.classList.remove('sidebar-collapsed');
    const toggleText = document.querySelector('#sidebar-toggle-text');
    if (toggleText) toggleText.textContent = 'Tutup Menu';
    appStore.setState({ sidebarCollapsed: false });
  });
  workspace.appendChild(reopenBtn);

  // 5. Mount Main Viewport (<main>)
  const mainViewport = document.createElement('main');
  mainViewport.className = 'app-main';
  workspace.appendChild(mainViewport);

  // 6. View Cache
  const views = {
    estimator: renderEstimatorView(),
    map: renderMapView(),
    analytics: renderAnalyticsView(),
    simulator: renderSimulatorView()
  };

  function switchTab(tabId) {
    mainViewport.innerHTML = '';
    const view = views[tabId] || views.estimator;
    mainViewport.appendChild(view);
    mainViewport.scrollTop = 0;
  }

  // Subscribe to navigation events
  appStore.subscribe('activeTab', (newTab) => {
    switchTab(newTab);
  });

  // Handle URL hash on load
  const hash = window.location.hash.replace('#', '');
  const aliasMap = {
    valuator: 'estimator',
    kalkulator: 'estimator',
    map: 'map',
    pasar: 'map',
    analytics: 'analytics',
    audit: 'analytics',
    simulator: 'simulator',
    renovasi: 'simulator'
  };
  const initialTab = aliasMap[hash] || 'estimator';

  appStore.setState({ activeTab: initialTab });
  switchTab(initialTab);
});
