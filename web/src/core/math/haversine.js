/**
 * Haversine Great-Circle Distance Engine
 * Pure mathematical functions with memoization for spatial comps
 */

const distanceCache = new Map();
const MAX_CACHE_SIZE = 1000;

function toRad(degrees) {
  return (degrees * Math.PI) / 180;
}

/**
 * Calculates great-circle distance between two coordinate pairs
 * @param {number} lat1 Latitude point 1
 * @param {number} lon1 Longitude point 1
 * @param {number} lat2 Latitude point 2
 * @param {number} lon2 Longitude point 2
 * @param {'miles'|'km'} unit Output distance unit
 * @returns {number} Distance in chosen unit
 */
export function haversineDistance(lat1, lon1, lat2, lon2, unit = 'miles') {
  const cacheKey = `${lat1.toFixed(4)},${lon1.toFixed(4)}_${lat2.toFixed(4)},${lon2.toFixed(4)}_${unit}`;
  if (distanceCache.has(cacheKey)) {
    return distanceCache.get(cacheKey);
  }

  const R = unit === 'miles' ? 3958.8 : 6371.0; // Earth radius
  const dLat = toRad(lat2 - lat1);
  const dLon = toRad(lon2 - lon1);
  const rLat1 = toRad(lat1);
  const rLat2 = toRad(lat2);

  const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
            Math.cos(rLat1) * Math.cos(rLat2) *
            Math.sin(dLon / 2) * Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  const distance = R * c;

  if (distanceCache.size >= MAX_CACHE_SIZE) {
    const firstKey = distanceCache.keys().next().value;
    distanceCache.delete(firstKey);
  }
  distanceCache.set(cacheKey, distance);

  return distance;
}
