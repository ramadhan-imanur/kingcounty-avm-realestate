"""
Desain Sistem & Injeksi Token Visual: Aeris Spatial Valuation (Google Stitch)
Berisi styling CSS kustom untuk tipografi, efek kaca, dan kartu metrik analitik.
"""

AERIS_CSS = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet" />

<style>
/* CSS Variables dari Aeris Spatial Valuation DESIGN.md */
:root {
    --primary: #006948;
    --primary-container: #00855d;
    --secondary: #006398;
    --surface: #f8f9ff;
    --surface-card: rgba(255, 255, 255, 0.88);
    --surface-card-elevated: rgba(255, 255, 255, 0.95);
    --border-subtle: rgba(226, 232, 240, 0.85);
    --on-surface: #0b1c30;
    --text-secondary: #475569;
    --text-muted: #94A3B8;
    --tier-entry: #0D9488;
    --tier-mid: #0284C7;
    --tier-luxury: #7C3AED;
    --shap-pos: #059669;
    --shap-neg: #E11D48;
    --font-sans: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    --font-mono: 'JetBrains Mono', monospace;
}

/* Base Body Styling */
.stApp {
    background-color: var(--surface);
    font-family: var(--font-sans);
    color: var(--on-surface);
}

/* Glassmorphism Cards */
.aeris-card {
    background: var(--surface-card);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--border-subtle);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 20px;
    box-shadow: 0 4px 20px -2px rgba(11, 28, 48, 0.04);
}

.aeris-card-hero {
    background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(240,246,255,0.92) 100%);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(0, 105, 72, 0.15);
    border-radius: 20px;
    padding: 28px;
    margin-bottom: 24px;
    box-shadow: 0 10px 30px -5px rgba(0, 105, 72, 0.08);
}

/* Header & Badges */
.aeris-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 12px;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-family: var(--font-mono);
    font-weight: 600;
}
.badge-primary { background: #85f8c4; color: #002114; }
.badge-muted { background: #eff4ff; color: #475569; }
.badge-entry { background: #ccfbf1; color: #0f766e; }
.badge-mid { background: #e0f2fe; color: #0369a1; }
.badge-luxury { background: #f3e8ff; color: #6b21a8; }

/* Large Metric Numbers */
.aeris-val-hero {
    font-family: var(--font-mono);
    font-size: 2.8rem;
    font-weight: 700;
    color: var(--on-surface);
    letter-spacing: -0.03em;
    line-height: 1.1;
    margin: 8px 0;
}

.aeris-val-idr {
    font-family: var(--font-sans);
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--primary);
}

/* SHAP Breakdown Items */
.shap-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 14px;
    border-radius: 10px;
    background: rgba(248, 250, 252, 0.8);
    border: 1px solid rgba(226, 232, 240, 0.6);
    margin-bottom: 8px;
    font-size: 0.875rem;
}
.shap-val-pos {
    font-family: var(--font-mono);
    font-weight: 700;
    color: var(--shap-pos);
}
.shap-val-neg {
    font-family: var(--font-mono);
    font-weight: 700;
    color: var(--shap-neg);
}

/* Button & Form Inputs */
div.stButton > button:first-child {
    background-color: var(--primary) !important;
    color: #ffffff !important;
    font-family: var(--font-sans) !important;
    font-weight: 600 !important;
    border-radius: 12px !important;
    border: none !important;
    padding: 12px 24px !important;
    box-shadow: 0 4px 14px rgba(0, 105, 72, 0.25) !important;
    transition: all 0.2s ease !important;
}
div.stButton > button:first-child:hover {
    background-color: var(--primary-container) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(0, 105, 72, 0.35) !important;
}

/* Custom Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0.82) !important;
    backdrop-filter: blur(20px) !important;
    border-right: 1px solid var(--border-subtle) !important;
}
</style>
"""
