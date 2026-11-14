/**
 * KingCounty-AVM Core Configuration & Performance Helpers
 * Precision Geobounds & Optimization Primitives
 */

export const KING_COUNTY_BOUNDS = Object.freeze({
  minLat: 47.15,
  maxLat: 47.78,
  minLon: -122.54,
  maxLon: -121.75,
  center: [47.55, -122.25],
  defaultZoom: 10
});

export const MODEL_METRICS = Object.freeze({
  pipelineVersion: "Dual-Pipeline v4.2 (LightGBM + Geospatial Decay)",
  modelAccuracy: "98.5%",
  testMAPE: 0.114,
  rSquared: 0.892,
  cod: 7.14,
  prd: 1.008,
  prb: -0.012
});

/**
 * Currency formatter with zero allocation on common bounds
 */
export function formatCurrency(amount) {
  if (amount == null || isNaN(amount)) return '$0';
  return '$' + Math.round(amount).toLocaleString('en-US');
}

/**
 * High-performance animation using requestAnimationFrame with easeOutQuad
 */
export function animateValue(element, endVal, duration = 350) {
  if (!element) return;
  const rawText = element.textContent || '';
  const startVal = parseInt(rawText.replace(/[^0-9]/g, ''), 10) || 0;
  if (startVal === endVal) return;

  const startTime = performance.now();
  function update(currentTime) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);
    const easeProgress = 1 - (1 - progress) * (1 - progress);
    const currentVal = Math.round(startVal + (endVal - startVal) * easeProgress);
    element.textContent = formatCurrency(currentVal);

    if (progress < 1) {
      requestAnimationFrame(update);
    } else {
      element.textContent = formatCurrency(endVal);
    }
  }
  requestAnimationFrame(update);
}

/**
 * Input debouncing to avoid blocking the main thread on rapid slider drags
 */
export function debounce(fn, delayMs = 60) {
  let timer = null;
  return function debounced(...args) {
    if (timer) clearTimeout(timer);
    timer = setTimeout(() => {
      timer = null;
      fn.apply(this, args);
    }, delayMs);
  };
}

/**
 * Event throttling for high-frequency viewport or cursor events
 */
export function throttle(fn, limitMs = 50) {
  let inThrottle = false;
  return function throttled(...args) {
    if (!inThrottle) {
      fn.apply(this, args);
      inThrottle = true;
      setTimeout(() => { inThrottle = false; }, limitMs);
    }
  };
}
