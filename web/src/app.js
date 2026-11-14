/**
 * KingCounty-AVM Application Bootstrap Entry Point
 * Aeris Spatial Valuation - Google Stitch Design Implementation
 * Project ID: 612066658549398949
 */

import { initNavigation, initSidebarToggle } from './features/navigation/nav-controller.js';
import { initValuator } from './features/estimator/valuator-controller.js';
import { initRenovationSimulator } from './features/simulator/renovation-controller.js';
import { initSpatialMapInteractions } from './features/map/spatial-controller.js';
import { initMarketAnalytics } from './features/analytics/market-controller.js';

let isBootstrapped = false;

export function bootstrap() {
  if (isBootstrapped) return;
  isBootstrapped = true;

  initSidebarToggle();
  initNavigation();
  initValuator();
  initRenovationSimulator();
  initSpatialMapInteractions();
  initMarketAnalytics();
}

if (typeof window !== 'undefined' && typeof document !== 'undefined') {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', bootstrap);
  } else {
    bootstrap();
  }
}
