/**
 * Inverse Distance Weighting (IDW) Spatial Interpolator
 * Pure geospatial math for localized price smoothing
 */

import { haversineDistance } from './haversine.js';

/**
 * Computes IDW estimate at target coordinate from array of spatial points
 * @param {number} targetLat Target latitude
 * @param {number} targetLon Target longitude
 * @param {Array<{lat: number, lon: number, value: number}>} points Sample observations
 * @param {number} power Distance decay exponent (typically 2.0)
 * @returns {number} Distance-weighted value estimate
 */
export function calculateIDW(targetLat, targetLon, points, power = 2) {
  if (!points || points.length === 0) return 0;

  let weightedSum = 0;
  let weightSum = 0;

  for (let i = 0; i < points.length; i++) {
    const pt = points[i];
    const dist = haversineDistance(targetLat, targetLon, pt.lat, pt.lon, 'miles');

    // If point coincides with target location, return exact value
    if (dist < 0.0001) {
      return pt.value;
    }

    const weight = 1 / Math.pow(dist, power);
    weightedSum += pt.value * weight;
    weightSum += weight;
  }

  if (weightSum === 0) return points[0].value;
  return weightedSum / weightSum;
}

/**
 * Filter and sort neighboring properties within max radius
 */
export function findNearestNeighbors(targetLat, targetLon, points, maxRadiusMiles = 5, limit = 5) {
  return points
    .map(pt => ({
      ...pt,
      distance: haversineDistance(targetLat, targetLon, pt.lat, pt.lon, 'miles')
    }))
    .filter(pt => pt.distance <= maxRadiusMiles)
    .sort((a, b) => a.distance - b.distance)
    .slice(0, limit);
}
