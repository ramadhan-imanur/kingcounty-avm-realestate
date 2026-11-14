/**
 * Statistical & Valuation Diagnostic Engine
 * Pure mathematical routines for intervals, quantiles, and depreciation
 */

/**
 * Calculates 95% Confidence Bounds (P10 and P90) based on validated test MAPE
 * @param {number} medianValuation Inferred point estimate
 * @param {number} mape Model Mean Absolute Percentage Error (default 0.114 = 11.4%)
 * @param {number} roundStep Rounding boundary (default $500)
 */
export function calculateConfidenceBounds(medianValuation, mape = 0.114, roundStep = 500) {
  const p10Raw = medianValuation * (1 - (mape * 0.789)); // ~0.91 factor
  const p90Raw = medianValuation * (1 + (mape * 0.789)); // ~1.09 factor

  const p10 = Math.round(p10Raw / roundStep) * roundStep;
  const p90 = Math.round(p90Raw / roundStep) * roundStep;

  return { p10, p90 };
}

/**
 * Computes non-linear age depreciation with renovation recovery
 * @param {number} yrBuilt Construction year
 * @param {number} yrRenovated Renovation year (0 if never renovated)
 * @param {number} currentYear Reference evaluation year
 */
export function calculateAgeDepreciation(yrBuilt, yrRenovated = 0, currentYear = 2026) {
  const effectiveYear = yrRenovated > yrBuilt ? yrRenovated : yrBuilt;
  const effectiveAge = Math.max(0, currentYear - effectiveYear);

  // Concave depreciation curve: 0.5% - 0.8% annually up to 40% maximum floor
  const depreciationFactor = Math.max(0.60, 1 - (effectiveAge * 0.0075));
  return depreciationFactor;
}

/**
 * Quantile calculation from array of numeric observations
 */
export function calculateQuantiles(data, quantiles = [0.1, 0.25, 0.5, 0.75, 0.9]) {
  if (!data || data.length === 0) return {};
  const sorted = [...data].sort((a, b) => a - b);
  const n = sorted.length;
  const results = {};

  quantiles.forEach(q => {
    const pos = (n - 1) * q;
    const base = Math.floor(pos);
    const rest = pos - base;
    if (sorted[base + 1] !== undefined) {
      results[q] = sorted[base] + rest * (sorted[base + 1] - sorted[base]);
    } else {
      results[q] = sorted[base];
    }
  });

  return results;
}
