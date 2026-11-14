/**
 * Smart AVM Valuation Engine Controller
 * Debounced input handlers, regression math, and batched DOM rendering
 */

import { formatCurrency, animateValue, debounce } from '../../core/config.js';
import { store } from '../../core/state.js';
import { KING_COUNTY_DATA, getZipcode } from '../../services/data-service.js';
import { calculateConfidenceBounds } from '../../core/math/stats.js';

export function initValuator() {
  const zipSelect = document.getElementById('input-zip');
  const sqftSlider = document.getElementById('slider-sqft');
  const sqftInput = document.getElementById('input-sqft');
  const gradeSlider = document.getElementById('slider-grade');
  const gradeLabel = document.getElementById('label-grade-desc');
  const gradeNum = document.getElementById('val-grade');
  const bathSlider = document.getElementById('slider-bath');
  const bathVal = document.getElementById('val-bath');
  const bedSlider = document.getElementById('slider-bed');
  const bedVal = document.getElementById('val-bed');
  const resetBtn = document.getElementById('btn-reset-valuator');

  if (!sqftSlider) return;
  const debouncedCalc = debounce(calculateValuation, 40);

  sqftSlider.addEventListener('input', () => {
    if (sqftInput) sqftInput.value = sqftSlider.value;
    debouncedCalc();
  });
  if (sqftInput) {
    sqftInput.addEventListener('input', () => {
      sqftSlider.value = sqftInput.value;
      debouncedCalc();
    });
  }

  if (gradeSlider) {
    gradeSlider.addEventListener('input', () => {
      const g = parseInt(gradeSlider.value, 10);
      if (gradeNum) gradeNum.textContent = g;
      if (gradeLabel && KING_COUNTY_DATA.grades[g]) {
        gradeLabel.textContent = `Grade ${g} — ${KING_COUNTY_DATA.grades[g]}`;
      }
      debouncedCalc();
    });
  }

  if (bathSlider) bathSlider.addEventListener('input', () => {
    if (bathVal) bathVal.textContent = bathSlider.value;
    debouncedCalc();
  });

  if (bedSlider) bedSlider.addEventListener('input', () => {
    if (bedVal) bedVal.textContent = bedSlider.value;
    debouncedCalc();
  });

  ['input-zip', 'select-condition', 'select-view', 'toggle-waterfront'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.addEventListener('change', debouncedCalc);
  });

  if (resetBtn) {
    resetBtn.addEventListener('click', () => {
      if (zipSelect) zipSelect.value = "98004";
      if (sqftSlider) sqftSlider.value = 2450;
      if (sqftInput) sqftInput.value = 2450;
      if (gradeSlider) gradeSlider.value = 8;
      if (gradeNum) gradeNum.textContent = "8";
      if (gradeLabel) gradeLabel.textContent = "Grade 8 — Sedikit Di Atas Rata-rata (Finishing Baik)";
      if (bathSlider) bathSlider.value = 2.5;
      if (bathVal) bathVal.textContent = "2.5";
      if (bedSlider) bedSlider.value = 3;
      if (bedVal) bedVal.textContent = "3";
      document.getElementById('select-condition').value = "3";
      document.getElementById('select-view').value = "0";
      document.getElementById('toggle-waterfront').checked = false;
      calculateValuation();
    });
  }

  calculateValuation();
}

export function calculateValuation() {
  const zip = document.getElementById('input-zip')?.value || "98004";
  const sqft = parseFloat(document.getElementById('slider-sqft')?.value || 2450);
  const grade = parseInt(document.getElementById('slider-grade')?.value || 8, 10);
  const baths = parseFloat(document.getElementById('slider-bath')?.value || 2.5);
  const beds = parseInt(document.getElementById('slider-bed')?.value || 3, 10);
  const condition = parseInt(document.getElementById('select-condition')?.value || 3, 10);
  const view = parseInt(document.getElementById('select-view')?.value || 0, 10);
  const isWaterfront = document.getElementById('toggle-waterfront')?.checked || false;

  const zipMeta = getZipcode(zip);
  const baseValuation = sqft * zipMeta.ppsqft;
  const gradeFactor = Math.pow(1.155, grade - 7);
  const bathBedFactor = 1.0 + ((baths - 2.0) * 0.04) + ((beds - 3) * 0.02);
  const condFactor = 1.0 + ((condition - 3) * 0.05);
  const viewFactor = 1.0 + (view * 0.08);
  const waterfrontMultiplier = isWaterfront ? 1.95 : 1.0;

  const rawVal = baseValuation * gradeFactor * bathBedFactor * condFactor * viewFactor * waterfrontMultiplier;
  const finalVal = Math.round(rawVal / 500) * 500;
  const { p10, p90 } = calculateConfidenceBounds(finalVal, 0.114);
  const effectivePpsqft = Math.round(finalVal / sqft);

  store.set('valuation', { zip, sqft, grade, baths, beds, condition, view, isWaterfront, estimatedPrice: finalVal, p10, p90, effectivePpsqft });
  updateValuationDOM(finalVal, p10, p90, effectivePpsqft, zipMeta, sqft, grade, baths, isWaterfront);
}

function updateValuationDOM(val, p10, p90, ppsqft, zipMeta, sqft, grade, baths, isWaterfront) {
  requestAnimationFrame(() => {
    const valEl = document.getElementById('display-valuation');
    const p10El = document.getElementById('display-p10');
    const p90El = document.getElementById('display-p90');
    const ppsqftEl = document.getElementById('display-ppsqft');
    const tierBadge = document.getElementById('display-tier-badge');
    const clusterBadge = document.getElementById('display-cluster-badge');

    if (valEl) animateValue(valEl, val);
    if (p10El) p10El.textContent = formatCurrency(p10);
    if (p90El) p90El.textContent = formatCurrency(p90);
    if (ppsqftEl) ppsqftEl.textContent = `$${ppsqft.toLocaleString()} / sq.ft`;

    if (tierBadge) {
      const isEntry = val < 450000;
      const isMid = val >= 450000 && val < 1000000;
      tierBadge.textContent = isEntry ? "Segmen Terjangkau" : (isMid ? "Segmen Menengah" : "Segmen Mewah / Luxury");
      tierBadge.className = `px-3 py-1 rounded-full text-xs font-bold ${isEntry ? 'glass-pill-tier-entry' : (isMid ? 'glass-pill-tier-mid' : 'glass-pill-tier-luxury')}`;
    }

    if (clusterBadge && KING_COUNTY_DATA.clusters[zipMeta.cluster]) {
      const cluster = KING_COUNTY_DATA.clusters[zipMeta.cluster];
      clusterBadge.textContent = `Klaster ${cluster.id}: ${cluster.name}`;
    }

    setShapRow('shap-sqft-val', 'shap-sqft-bar', Math.round((sqft - 2000) * 185));
    setShapRow('shap-grade-val', 'shap-grade-bar', Math.round((grade - 7) * (val * 0.12)));
    setShapRow('shap-loc-val', 'shap-loc-bar', Math.round(zipMeta.medianPrice - 450000));
    setShapRow('shap-bath-val', 'shap-bath-bar', Math.round((baths - 2) * 28000));

    const wfRow = document.getElementById('shap-wf-row');
    if (wfRow) {
      wfRow.style.display = isWaterfront ? 'flex' : 'none';
      if (isWaterfront) setShapRow('shap-wf-val', 'shap-wf-bar', Math.round(val * 0.45));
    }
  });
}

function setShapRow(valId, barId, amount) {
  const valEl = document.getElementById(valId);
  const barEl = document.getElementById(barId);
  if (!valEl || !barEl) return;
  const isPos = amount >= 0;
  valEl.textContent = (isPos ? '+' : '') + formatCurrency(amount);
  valEl.className = isPos ? 'font-mono text-xs font-bold text-shap-positive' : 'font-mono text-xs font-bold text-shap-negative';
  const pct = Math.min(Math.max(Math.abs(amount) / 250000 * 100, 10), 100);
  barEl.style.width = `${pct}%`;
  barEl.className = `shap-bar ${isPos ? 'shap-bar-positive' : 'shap-bar-negative'}`;
}
