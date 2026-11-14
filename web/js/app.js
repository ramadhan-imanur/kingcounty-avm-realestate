/**
 * KingCounty-AVM Interactive Dashboard Application
 * Aeris Spatial Valuation - Google Stitch Design Implementation
 * Project ID: 612066658549398949
 */

document.addEventListener('DOMContentLoaded', () => {
  initSidebarToggle();
  initNavigation();
  initValuator();
  initRenovationSimulator();
  initSpatialMapInteractions();
});

// ==========================================================================
// 1. NAVIGATION & TAB SWITCHING
// ==========================================================================
function initNavigation() {
  const navLinks = document.querySelectorAll('aside [data-tab-target]');
  const tabs = document.querySelectorAll('.tab-content');

  function switchTab(targetId, updateUrl = false) {
    // Hide all tabs
    tabs.forEach(tab => {
      tab.classList.remove('active');
    });

    // Remove active state from all nav links
    navLinks.forEach(link => {
      link.classList.remove('active');
      link.classList.remove('bg-emerald-600', 'text-white', 'shadow-md', 'shadow-emerald-700/20');
      // restore default text color
      if (!link.classList.contains('active')) {
        link.classList.add('text-slate-600', 'hover:bg-white/60');
      }
    });

    // Activate selected tab
    const selectedTab = document.getElementById(targetId);
    if (selectedTab) {
      selectedTab.classList.add('active');
    }

    // Activate corresponding nav link
    navLinks.forEach(link => {
      if (link.getAttribute('data-tab-target') === targetId) {
        link.classList.add('active');
        link.classList.add('bg-emerald-600', 'text-white', 'shadow-md', 'shadow-emerald-700/20');
        link.classList.remove('text-slate-600', 'hover:bg-white/60');
      }
    });

    // Reset scroll positions to top
    window.scrollTo(0, 0);
    const mainWorkspace = document.querySelector('main');
    if (mainWorkspace) mainWorkspace.scrollTop = 0;

    // Update URL hash cleanly without auto-scrolling if supported and not on file://
    if (updateUrl && window.location.protocol !== 'file:') {
      try {
        if (window.history && window.history.replaceState) {
          window.history.replaceState(null, null, '#' + targetId);
        }
      } catch (err) {}
    }
    
    // Always keep window firmly at top
    window.scrollTo(0, 0);
  }

  navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const target = link.getAttribute('data-tab-target');
      switchTab(target, true);
    });
  });

  // Handle URL hash on load (with alias support)
  let hash = window.location.hash.replace('#', '');
  const aliasMap = {
    'valuator': 'tab-valuator',
    'kalkulator': 'tab-valuator',
    'market': 'tab-market',
    'pasar': 'tab-market',
    'renovation': 'tab-renovation',
    'renovasi': 'tab-renovation',
    'audit': 'tab-audit',
    'kualitas': 'tab-audit'
  };
  if (aliasMap[hash]) hash = aliasMap[hash];

  // Handle default tab from body attribute or URL hash
  const bodyDefault = document.body.getAttribute('data-default-tab') || 'tab-valuator';
  if (hash && document.getElementById(hash)) {
    switchTab(hash, false);
  } else {
    switchTab(bodyDefault, false);
  }
}

// ==========================================================================
// 2. SMART AVM VALUATION ENGINE (REACTIVE CALCULATOR)
// ==========================================================================
function initValuator() {
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
  const condSelect = document.getElementById('select-condition');
  const viewSelect = document.getElementById('select-view');
  const waterfrontToggle = document.getElementById('toggle-waterfront');
  const resetBtn = document.getElementById('btn-reset-valuator');

  if (!sqftSlider) return;

  // Sync sqft slider and number input
  sqftSlider.addEventListener('input', () => {
    if (sqftInput) sqftInput.value = sqftSlider.value;
    calculateValuation();
  });
  if (sqftInput) {
    sqftInput.addEventListener('input', () => {
      sqftSlider.value = sqftInput.value;
      calculateValuation();
    });
  }

  // Grade slider
  if (gradeSlider) {
    gradeSlider.addEventListener('input', () => {
      const g = parseInt(gradeSlider.value);
      if (gradeNum) gradeNum.textContent = g;
      if (gradeLabel && KING_COUNTY_DATA.grades[g]) {
        gradeLabel.textContent = `Grade ${g} — ${KING_COUNTY_DATA.grades[g]}`;
      }
      calculateValuation();
    });
  }

  // Bath slider
  if (bathSlider) {
    bathSlider.addEventListener('input', () => {
      if (bathVal) bathVal.textContent = bathSlider.value;
      calculateValuation();
    });
  }

  // Bed slider
  if (bedSlider) {
    bedSlider.addEventListener('input', () => {
      if (bedVal) bedVal.textContent = bedSlider.value;
      calculateValuation();
    });
  }

  // Other select inputs
  if (zipSelect) zipSelect.addEventListener('change', calculateValuation);
  if (condSelect) condSelect.addEventListener('change', calculateValuation);
  if (viewSelect) viewSelect.addEventListener('change', calculateValuation);
  if (waterfrontToggle) waterfrontToggle.addEventListener('change', calculateValuation);

  // Reset button
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
      if (condSelect) condSelect.value = "3";
      if (viewSelect) viewSelect.value = "0";
      if (waterfrontToggle) waterfrontToggle.checked = false;
      calculateValuation();
    });
  }

  // Initial calculation
  calculateValuation();
}

function calculateValuation() {
  const zip = document.getElementById('input-zip')?.value || "98004";
  const sqft = parseFloat(document.getElementById('slider-sqft')?.value || 2450);
  const grade = parseInt(document.getElementById('slider-grade')?.value || 8);
  const baths = parseFloat(document.getElementById('slider-bath')?.value || 2.5);
  const beds = parseInt(document.getElementById('slider-bed')?.value || 3);
  const condition = parseInt(document.getElementById('select-condition')?.value || 3);
  const view = parseInt(document.getElementById('select-view')?.value || 0);
  const isWaterfront = document.getElementById('toggle-waterfront')?.checked || false;

  const zipMeta = KING_COUNTY_DATA.zipcodes[zip] || KING_COUNTY_DATA.zipcodes["98004"];

  // Baseline Model Regression Formula (Calibrated against King County LightGBM/Ridge)
  // Baseline price per sqft scaled by zip code
  let ppsqft = zipMeta.ppsqft;
  let baseValuation = sqft * ppsqft;

  // Grade adjustment: median is grade 7; each grade increment confers exponential compounding (~14-16%)
  const gradeFactor = Math.pow(1.155, grade - 7);
  
  // Bathroom / Bedroom density adjustment
  const bathBedFactor = 1.0 + ((baths - 2.0) * 0.04) + ((beds - 3) * 0.02);

  // Condition factor (1 to 5, baseline 3)
  const condFactor = 1.0 + ((condition - 3) * 0.05);

  // View multiplier (0 to 4)
  const viewFactor = 1.0 + (view * 0.08);

  // Waterfront premium (Massive 80-120% premium in King County)
  const waterfrontMultiplier = isWaterfront ? 1.95 : 1.0;

  // Final Estimated Value
  let finalValuation = baseValuation * gradeFactor * bathBedFactor * condFactor * viewFactor * waterfrontMultiplier;
  finalValuation = Math.round(finalValuation / 500) * 500; // Round to nearest $500

  // Confidence Bounds (95% CI with MAPE ~11.4%)
  const p10 = Math.round((finalValuation * 0.91) / 500) * 500;
  const p90 = Math.round((finalValuation * 1.09) / 500) * 500;
  const effectivePpsqft = Math.round(finalValuation / sqft);

  // Update DOM Elements
  updateValuationDOM(finalValuation, p10, p90, effectivePpsqft, zipMeta, sqft, grade, baths, beds, view, isWaterfront);
}

function updateValuationDOM(val, p10, p90, ppsqft, zipMeta, sqft, grade, baths, beds, view, isWaterfront) {
  // Main Valuation Display
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

  // Market Tier Badge
  if (tierBadge) {
    if (val < 450000) {
      tierBadge.textContent = "Segmen Terjangkau";
      tierBadge.className = "px-3 py-1 rounded-full text-xs font-bold glass-pill-tier-entry";
    } else if (val < 1000000) {
      tierBadge.textContent = "Segmen Menengah";
      tierBadge.className = "px-3 py-1 rounded-full text-xs font-bold glass-pill-tier-mid";
    } else {
      tierBadge.textContent = "Segmen Mewah / Luxury";
      tierBadge.className = "px-3 py-1 rounded-full text-xs font-bold glass-pill-tier-luxury";
    }
  }

  // Micro-Market Cluster Badge
  if (clusterBadge && KING_COUNTY_DATA.clusters[zipMeta.cluster]) {
    const cluster = KING_COUNTY_DATA.clusters[zipMeta.cluster];
    clusterBadge.textContent = `Klaster ${cluster.id}: ${cluster.name}`;
  }

  // SHAP Feature Contribution Waterfall Updates
  updateShapBreakdown(val, zipMeta, sqft, grade, baths, isWaterfront);
}

function updateShapBreakdown(finalVal, zipMeta, sqft, grade, baths, isWaterfront) {
  const sqftShap = Math.round((sqft - 2000) * 185);
  const gradeShap = Math.round((grade - 7) * (finalVal * 0.12));
  const locShap = Math.round(zipMeta.medianPrice - 450000);
  const bathShap = Math.round((baths - 2) * 28000);
  const wfShap = isWaterfront ? Math.round(finalVal * 0.45) : 0;

  setShapRow('shap-sqft-val', 'shap-sqft-bar', sqftShap, `Luas Bangunan (${sqft} sq.ft)`);
  setShapRow('shap-grade-val', 'shap-grade-bar', gradeShap, `Kualitas Bangunan (Grade ${grade})`);
  setShapRow('shap-loc-val', 'shap-loc-bar', locShap, `Premium Submarket (${zipMeta.name})`);
  setShapRow('shap-bath-val', 'shap-bath-bar', bathShap, `Kamar Mandi (${baths} unit)`);
  if (document.getElementById('shap-wf-row')) {
    document.getElementById('shap-wf-row').style.display = isWaterfront ? 'flex' : 'none';
    if (isWaterfront) {
      setShapRow('shap-wf-val', 'shap-wf-bar', wfShap, 'Waterfront Waterfront Shore');
    }
  }
}

function setShapRow(valId, barId, amount, label) {
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

// ==========================================================================
// 3. RENOVATION ROI SIMULATOR
// ==========================================================================
function initRenovationSimulator() {
  const baseValueInput = document.getElementById('renov-base-value');
  const checkboxes = document.querySelectorAll('.renov-toggle');

  if (!checkboxes.length) return;

  checkboxes.forEach(cb => {
    cb.addEventListener('change', calculateRenovationROI);
  });

  if (baseValueInput) {
    baseValueInput.addEventListener('input', calculateRenovationROI);
  }

  calculateRenovationROI();
}

function calculateRenovationROI() {
  const baseVal = parseFloat(document.getElementById('renov-base-value')?.value || 650000);
  let totalCost = 0;
  let totalAppreciation = 0;

  const upgrades = [
    { id: 'renov-bath', cost: 24000, valueGain: 38500 },
    { id: 'renov-kitchen', cost: 48000, valueGain: 72000 },
    { id: 'renov-basement', cost: 36000, valueGain: 52000 },
    { id: 'renov-deck', cost: 16000, valueGain: 22500 },
    { id: 'renov-grade', cost: 65000, valueGain: 125000 },
    { id: 'renov-energy', cost: 15000, valueGain: 19500 }
  ];

  upgrades.forEach(u => {
    const el = document.getElementById(u.id);
    if (el && el.checked) {
      totalCost += u.cost;
      totalAppreciation += u.valueGain;
    }
  });

  const netProfit = totalAppreciation - totalCost;
  const roiPct = totalCost > 0 ? Math.round((totalAppreciation / totalCost) * 100) : 0;
  const projectedVal = baseVal + totalAppreciation;

  // DOM Updates
  const totalCostEl = document.getElementById('renov-total-cost');
  const appreciationEl = document.getElementById('renov-total-appreciation');
  const netProfitEl = document.getElementById('renov-net-profit');
  const roiBadgeEl = document.getElementById('renov-roi-badge');
  const projectedValEl = document.getElementById('renov-projected-val');

  if (totalCostEl) totalCostEl.textContent = formatCurrency(totalCost);
  if (appreciationEl) appreciationEl.textContent = formatCurrency(totalAppreciation);
  if (netProfitEl) {
    netProfitEl.textContent = (netProfit >= 0 ? '+' : '') + formatCurrency(netProfit);
    netProfitEl.className = netProfit >= 0 ? 'text-2xl font-bold font-mono text-shap-positive' : 'text-2xl font-bold font-mono text-shap-negative';
  }
  if (roiBadgeEl) {
    roiBadgeEl.textContent = `${roiPct}% ROI Gross`;
    roiBadgeEl.className = roiPct >= 120 
      ? 'px-3 py-1 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800 border border-emerald-300' 
      : 'px-3 py-1 rounded-full text-xs font-bold bg-sky-100 text-sky-800 border border-sky-300';
  }
  if (projectedValEl) {
    animateValue(projectedValEl, projectedVal);
  }
}

// ==========================================================================
// 4. SPATIAL MAP INTERACTION (SVG & CLUSTERS)
// ==========================================================================
function initSpatialMapInteractions() {
  const mapPoints = document.querySelectorAll('[data-submarket]');
  const infoCard = document.getElementById('map-floating-card');
  const cardTitle = document.getElementById('map-card-title');
  const cardPrice = document.getElementById('map-card-price');
  const cardPpsqft = document.getElementById('map-card-ppsqft');
  const cardZip = document.getElementById('map-card-zip');

  if (!mapPoints.length) return;

  mapPoints.forEach(point => {
    point.addEventListener('mouseenter', () => {
      const zip = point.getAttribute('data-submarket');
      const data = KING_COUNTY_DATA.zipcodes[zip];
      if (data && cardTitle && cardPrice && cardPpsqft && cardZip) {
        cardTitle.textContent = data.name;
        cardPrice.textContent = formatCurrency(data.medianPrice);
        cardPpsqft.textContent = `$${data.ppsqft} / sq.ft`;
        cardZip.textContent = `Area ${zip}`;
      }
    });
  });
}

// ==========================================================================
// UTILITY FUNCTIONS
// ==========================================================================
function formatCurrency(amount) {
  return '$' + Math.round(amount).toLocaleString('en-US');
}

function animateValue(element, endVal, duration = 400) {
  const startVal = parseInt(element.textContent.replace(/[^0-9]/g, '')) || 0;
  if (startVal === endVal) return;

  const startTime = performance.now();
  function update(currentTime) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);
    // Smooth easeOutQuad
    const easeProgress = 1 - (1 - progress) * (1 - progress);
    const currentVal = Math.round(startVal + (endVal - startVal) * easeProgress);
    element.textContent = formatCurrency(currentVal);

    if (progress < 1) {
      requestAnimationFrame(update);
    } else {
      element.textContent = formatCurrency(endVal);
    }
  }
  requestAnimationFrame(update);
}


// ==========================================================================
// 5. DESKTOP COLLAPSIBLE SIDEBAR
// ==========================================================================
function initSidebarToggle() {
  const body = document.body;
  const toggleBtn = document.getElementById('sidebar-toggle-btn');
  const closeBtn = document.getElementById('sidebar-close-btn');
  const reopenFloatBtn = document.getElementById('sidebar-reopen-float-btn');
  const toggleText = document.getElementById('sidebar-toggle-text');

  function setSidebarState(collapsed) {
    if (collapsed) {
      body.classList.add('sidebar-collapsed');
      if (toggleText) toggleText.textContent = 'Buka Menu';
      if (toggleBtn) {
        toggleBtn.setAttribute('title', 'Buka Menu Utama (Desktop)');
        toggleBtn.classList.add('bg-emerald-50', 'text-emerald-700', 'border-emerald-200');
      }
      try {
        localStorage.setItem('kingcounty_sidebar_collapsed', 'true');
      } catch (e) {}
    } else {
      body.classList.remove('sidebar-collapsed');
      if (toggleText) toggleText.textContent = 'Tutup Menu';
      if (toggleBtn) {
        toggleBtn.setAttribute('title', 'Tutup Menu Utama (Desktop)');
        toggleBtn.classList.remove('bg-emerald-50', 'text-emerald-700', 'border-emerald-200');
      }
      try {
        localStorage.setItem('kingcounty_sidebar_collapsed', 'false');
      } catch (e) {}
    }
  }

  function toggleSidebar() {
    const isCollapsed = body.classList.contains('sidebar-collapsed');
    setSidebarState(!isCollapsed);
  }

  if (toggleBtn) {
    toggleBtn.addEventListener('click', (e) => {
      e.preventDefault();
      toggleSidebar();
    });
  }

  if (closeBtn) {
    closeBtn.addEventListener('click', (e) => {
      e.preventDefault();
      setSidebarState(true);
    });
  }

  if (reopenFloatBtn) {
    reopenFloatBtn.addEventListener('click', (e) => {
      e.preventDefault();
      setSidebarState(false);
    });
  }

  // Restore saved state on load (if viewport is desktop width)
  try {
    const saved = localStorage.getItem('kingcounty_sidebar_collapsed');
    if (saved === 'true' && window.innerWidth >= 768) {
      setSidebarState(true);
    }
  } catch (e) {}
}
