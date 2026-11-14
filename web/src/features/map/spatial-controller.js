/**
 * Geospatial Map Interaction Controller
 * Throttled submarket exploration, SVG points, and dynamic card updates
 */

import { formatCurrency, throttle } from '../../core/config.js';
import { store } from '../../core/state.js';
import { KING_COUNTY_DATA, getZipcode } from '../../services/data-service.js';

export function initSpatialMapInteractions() {
  const mapPoints = document.querySelectorAll('[data-submarket]');
  const infoCard = document.getElementById('map-floating-card');
  const cardTitle = document.getElementById('map-card-title');
  const cardPrice = document.getElementById('map-card-price');
  const cardPpsqft = document.getElementById('map-card-ppsqft');
  const cardZip = document.getElementById('map-card-zip');

  if (!mapPoints.length) return;

  const updateSubmarketDisplay = (zip) => {
    const data = getZipcode(zip);
    if (!data) return;

    requestAnimationFrame(() => {
      if (cardTitle) cardTitle.textContent = data.name;
      if (cardPrice) cardPrice.textContent = formatCurrency(data.medianPrice);
      if (cardPpsqft) cardPpsqft.textContent = `$${data.ppsqft} / sq.ft`;
      if (cardZip) cardZip.textContent = `Area ${zip}`;
      if (infoCard) {
        infoCard.classList.remove('opacity-0');
        infoCard.classList.add('opacity-100');
      }
    });

    store.set('selectedSubmarket', zip);
  };

  const throttledUpdate = throttle(updateSubmarketDisplay, 60);

  mapPoints.forEach(point => {
    point.addEventListener('mouseenter', () => {
      const zip = point.getAttribute('data-submarket');
      if (zip) throttledUpdate(zip);
    });

    point.addEventListener('click', () => {
      const zip = point.getAttribute('data-submarket');
      if (zip) {
        updateSubmarketDisplay(zip);
        const zipSelect = document.getElementById('input-zip');
        if (zipSelect && zipSelect.querySelector(`option[value="${zip}"]`)) {
          zipSelect.value = zip;
          zipSelect.dispatchEvent(new Event('change'));
        }
      }
    });
  });
}
