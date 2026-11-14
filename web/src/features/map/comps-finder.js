/**
 * KingCounty-AVM: Geospatial Comps Search Engine
 * Discovers nearest comparable deeds using Haversine distance & similarity weighting
 */

import { haversineDistance } from '../../core/math/haversine.js';
import { DataService } from '../../core/data-service.js';

export function findComparableProperties(targetProp, maxRadiusMiles = 5.0, limit = 3) {
  const parcels = DataService.getParcels();
  const candidates = [];

  for (let i = 0; i < parcels.length; i++) {
    const comp = parcels[i];
    const dist = haversineDistance(targetProp.lat, targetProp.lon, comp.lat, comp.lon);

    if (dist <= maxRadiusMiles) {
      // Calculate structural similarity (0 to 1)
      const sqftDiff = Math.abs(comp.sqft - targetProp.sqft_living) / targetProp.sqft_living;
      const gradeDiff = Math.abs(comp.grade - targetProp.grade) / 10;
      const similarityScore = Math.max(0.7, 1 - (sqftDiff * 0.4 + gradeDiff * 0.3 + (dist / maxRadiusMiles) * 0.3));

      candidates.push({
        ...comp,
        distance: dist,
        similarityScore: Math.round(similarityScore * 100)
      });
    }
  }

  // Sort by lowest distance first, then highest similarity
  candidates.sort((a, b) => a.distance - b.distance);
  return candidates.slice(0, limit);
}
