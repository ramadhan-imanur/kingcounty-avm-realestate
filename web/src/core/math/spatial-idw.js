/**
 * Pure Mathematical Engine: Spatial Inverse Distance Weighting (IDW)
 * Interpolates property valuation from empirical comparable parcels
 */

import { haversineDistance } from './haversine.js';

/**
 * Calculates IDW price benchmark from a set of comparable properties
 * @param {{lat: number, lon: number}} target
 * @param {Array<{lat: number, lon: number, price: number}>} comps
 * @param {number} power Distance exponent (default 2)
 * @returns {{ estimatedPrice: number, totalWeight: number, compsCount: number }}
 */
export function calculateIDW(target, comps, power = 2) {
  if (!comps || comps.length === 0) {
    return { estimatedPrice: 0, totalWeight: 0, compsCount: 0 };
  }

  let weightedSum = 0;
  let totalWeight = 0;

  for (let i = 0; i < comps.length; i++) {
    const comp = comps[i];
    const dist = haversineDistance(target.lat, target.lon, comp.lat, comp.lon);

    // Exact location match gives 100% weight to that comp
    if (dist < 0.001) {
      return {
        estimatedPrice: comp.price,
        totalWeight: 1,
        compsCount: 1
      };
    }

    const weight = 1 / Math.pow(dist, power);
    weightedSum += comp.price * weight;
    totalWeight += weight;
  }

  const estimatedPrice = totalWeight > 0 ? Math.round(weightedSum / totalWeight) : 0;

  return {
    estimatedPrice,
    totalWeight,
    compsCount: comps.length
  };
}
