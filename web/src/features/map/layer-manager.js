/**
 * KingCounty-AVM: Cartographic Layer Manager & Coordinate Projection
 * Projects WGS84 geographic coordinates (EPSG:4326) into SVG cartographic canvas
 */

import { APP_CONFIG } from '../../core/config.js';

export class LayerManager {
  static project(lat, lon, width = 800, height = 500) {
    const { minLat, maxLat, minLon, maxLon } = APP_CONFIG.spatial.bounds;

    const x = ((lon - minLon) / (maxLon - minLon)) * width;
    const y = ((maxLat - lat) / (maxLat - minLat)) * height;

    return {
      x: Math.round(Math.max(20, Math.min(width - 20, x))),
      y: Math.round(Math.max(20, Math.min(height - 20, y)))
    };
  }

  static renderWaterBodiesSVG() {
    return `
      <!-- Puget Sound (Western Coast) -->
      <path d="M 0 0 L 140 0 C 130 90 90 140 110 240 C 125 310 90 400 80 500 L 0 500 Z" 
            fill="#dbeafe" opacity="0.65" />
      <text x="35" y="280" font-family="'JetBrains Mono'" font-size="11" fill="#0369a1" font-weight="700" letter-spacing="2">PUGET SOUND</text>

      <!-- Lake Washington -->
      <path d="M 230 70 C 220 130 240 180 230 260 C 225 300 245 350 240 400 C 235 370 215 310 220 260 C 215 190 205 130 215 70 Z" 
            fill="#bae6fd" stroke="#0284c7" stroke-width="1.5" opacity="0.85" />
      <text x="210" y="270" font-family="'JetBrains Mono'" font-size="9" fill="#0284c7" font-weight="600" transform="rotate(-90 210,270)">LAKE WASHINGTON</text>

      <!-- Lake Sammamish -->
      <path d="M 330 180 C 335 220 330 260 335 300 C 325 280 320 230 325 180 Z" 
            fill="#bae6fd" stroke="#0284c7" stroke-width="1.2" opacity="0.75" />
      <text x="345" y="250" font-family="'JetBrains Mono'" font-size="8" fill="#0284c7">L. SAMMAMISH</text>
    `;
  }
}
