/**
 * Pure Mathematical Engine: Statistical Aggregations & Quantiles
 */

export function mean(arr) {
  if (!arr || arr.length === 0) return 0;
  return arr.reduce((acc, v) => acc + v, 0) / arr.length;
}

export function median(arr) {
  if (!arr || arr.length === 0) return 0;
  const sorted = [...arr].sort((a, b) => a - b);
  const mid = Math.floor(sorted.length / 2);
  return sorted.length % 2 !== 0 ? sorted[mid] : (sorted[mid - 1] + sorted[mid]) / 2;
}

export function quantile(arr, q) {
  if (!arr || arr.length === 0) return 0;
  const sorted = [...arr].sort((a, b) => a - b);
  const pos = (sorted.length - 1) * q;
  const base = Math.floor(pos);
  const rest = pos - base;
  if (sorted[base + 1] !== undefined) {
    return sorted[base] + rest * (sorted[base + 1] - sorted[base]);
  }
  return sorted[base];
}

export function standardDeviation(arr) {
  if (!arr || arr.length < 2) return 0;
  const m = mean(arr);
  const variance = arr.reduce((acc, v) => acc + Math.pow(v - m, 2), 0) / (arr.length - 1);
  return Math.sqrt(variance);
}

/**
 * Calculates 90% log-normal confidence bounds (P10 - P90)
 * @param {number} pointEstimate
 * @param {number} mapePercent
 */
export function calculateConfidenceInterval(pointEstimate, mapePercent = 11.4) {
  const sigma = (mapePercent / 100) * 1.25;
  const z90 = 1.645;
  const p10 = Math.round(pointEstimate * Math.exp(-z90 * sigma * 0.6));
  const p90 = Math.round(pointEstimate * Math.exp(z90 * sigma * 0.6));
  return { p10, p90, spread: p90 - p10 };
}
