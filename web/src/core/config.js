/**
 * KingCounty-AVM: Global Application Configuration
 * Spatial Bounds, Formats, and Model Governance Standards
 */

export const APP_CONFIG = {
  appName: 'KingCounty-AVM',
  tagline: 'Valuasi Cerdas Properti & Riset Spasial',
  datasetSize: 22847,
  version: 'Dual-Pipeline v4.2',
  
  // Geospatial boundaries for King County, WA (EPSG:4326)
  spatial: {
    center: { lat: 47.5480, lon: -122.0326 },
    bounds: {
      minLat: 47.1550,
      maxLat: 47.7780,
      minLon: -122.5190,
      maxLon: -121.6850
    },
    defaultRadiusMiles: 1.5,
    maxComps: 3
  },

  // Econometric and Valuation benchmarks
  benchmarks: {
    medianPrice: 450000,
    avgPricePerSqFt: 284,
    rSquared: 0.8836,
    testMape: 11.4,
    cod: 7.14,
    prd: 1.008,
    prb: -0.012,
    idrExchangeRate: 16250
  },

  // Market tier categorization
  tiers: {
    entry: { id: 'entry', label: 'Terjangkau (<$350k)', threshold: 350000, color: '#0D9488' },
    mid: { id: 'mid', label: 'Menengah ($350k-$750k)', threshold: 750000, color: '#0284C7' },
    luxury: { id: 'luxury', label: 'Mewah (>$750k)', threshold: Infinity, color: '#7C3AED' }
  }
};

/**
 * Format currency to USD display ($450,000)
 */
export function formatUSD(val, maxDecimals = 0) {
  if (val == null || isNaN(val)) return '$0';
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    maximumFractionDigits: maxDecimals
  }).format(val);
}

/**
 * Format currency to IDR Billion display (Rp 7,31 Miliar)
 */
export function formatIDRBillions(valUSD) {
  if (!valUSD || isNaN(valUSD)) return 'Rp 0 M';
  const totalIDR = valUSD * APP_CONFIG.benchmarks.idrExchangeRate;
  const billions = totalIDR / 1_000_000_000;
  return `Rp ${billions.toFixed(2)} Miliar`;
}

/**
 * Format integer numbers with locale separators
 */
export function formatNumber(val) {
  if (val == null || isNaN(val)) return '0';
  return Number(val).toLocaleString('id-ID');
}
