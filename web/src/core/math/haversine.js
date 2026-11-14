/**
 * Pure Mathematical Engine: Haversine Distance Calculator
 * Computes great-circle distance between two latitude/longitude points
 */

const EARTH_RADIUS_MILES = 3958.8;
const EARTH_RADIUS_KM = 6371.0;

function toRadians(degrees) {
  return (degrees * Math.PI) / 180;
}

/**
 * Calculates distance between two geospatial coordinates
 * @param {number} lat1
 * @param {number} lon1
 * @param {number} lat2
 * @param {number} lon2
 * @param {'miles'|'km'} unit
 * @returns {number} Distance in requested unit
 */
export function haversineDistance(lat1, lon1, lat2, lon2, unit = 'miles') {
  if (lat1 === lat2 && lon1 === lon2) return 0;

  const dLat = toRadians(lat2 - lat1);
  const dLon = toRadians(lon2 - lon1);

  const radLat1 = toRadians(lat1);
  const radLat2 = toRadians(lat2);

  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.sin(dLon / 2) * Math.sin(dLon / 2) * Math.cos(radLat1) * Math.cos(radLat2);

  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  const radius = unit === 'km' ? EARTH_RADIUS_KM : EARTH_RADIUS_MILES;

  return radius * c;
}
