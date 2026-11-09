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
:root {
    --primary: #006948;
    --primary-container: #00855d;
    --secondary: #006398;
    --surface: #f8f9ff;
    --surface-card: #ffffff;
    --border-subtle: rgba(226, 232, 240, 0.9);
    --on-surface: #0b1c30;
    --text-secondary: #475569;
    --text-muted: #94A3B8;
    --tier-luxury: #7C3AED;
    --shap-pos: #059669;
    --shap-neg: #E11D48;
    --font-sans: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    --font-mono: 'JetBrains Mono', monospace;
}

.stApp { background-color: var(--surface) !important; font-family: var(--font-sans) !important; color: var(--on-surface) !important; }
.block-container { padding-top: 1.5rem !important; padding-bottom: 2.5rem !important; max-width: 1380px !important; }

/* Material Symbols Ligature */
.material-symbols-outlined {
    font-family: 'Material Symbols Outlined' !important; font-weight: normal; font-style: normal;
    font-size: 20px; line-height: 1; display: inline-block; vertical-align: middle; -webkit-font-smoothing: antialiased;
}

/* Fix Labels and Typography Contrast */
label, label p, [data-testid="stWidgetLabel"] p, [data-testid="stWidgetLabel"] span {
    color: #0b1c30 !important; font-weight: 600 !important; font-size: 0.85rem !important; font-family: var(--font-sans) !important;
}
[data-testid="stMarkdownContainer"] p, [data-testid="stMarkdownContainer"] span { color: #0b1c30; }

/* Light Inputs & Selectboxes */
div[data-baseweb="input"], div[data-baseweb="base-input"], div[data-baseweb="select"] > div {
    background-color: #ffffff !important; border: 1px solid #dce9ff !important; border-radius: 10px !important; color: #0b1c30 !important;
}
div[data-baseweb="input"] input, div[data-baseweb="base-input"] input {
    color: #0b1c30 !important; background-color: #ffffff !important; font-family: var(--font-mono) !important; font-weight: 600 !important;
}
button[data-testid="stNumberInputStepDown"], button[data-testid="stNumberInputStepUp"] {
    background-color: #eff4ff !important; color: #006948 !important; border: 1px solid #dce9ff !important; border-radius: 6px !important;
}

/* Native Streamlit Form styled as Aeris Card */
[data-testid="stForm"] {
    background: #ffffff !important; border: 1px solid var(--border-subtle) !important; border-radius: 16px !important;
    padding: 24px !important; box-shadow: 0 4px 20px -2px rgba(11, 28, 48, 0.04) !important;
}

/* Glassmorphism Cards */
.aeris-card {
    background: #ffffff; border: 1px solid var(--border-subtle); border-radius: 16px;
    padding: 22px; margin-bottom: 18px; box-shadow: 0 4px 20px -2px rgba(11, 28, 48, 0.04);
}
.aeris-card-hero {
    background: linear-gradient(135deg, #ffffff 0%, #f0f7f4 100%);
    border: 1px solid rgba(0, 105, 72, 0.18); border-radius: 18px;
    padding: 24px; margin-bottom: 18px; box-shadow: 0 8px 24px -4px rgba(0, 105, 72, 0.08);
}

/* Badges & Metrics */
.aeris-badge {
    display: inline-flex; align-items: center; gap: 6px; padding: 4px 12px;
    border-radius: 9999px; font-size: 0.75rem; font-family: var(--font-mono); font-weight: 600;
}
.badge-primary { background: #85f8c4; color: #002114; }
.badge-muted { background: #eff4ff; color: #475569; }
.badge-entry { background: #ccfbf1; color: #0f766e; }
.badge-mid { background: #e0f2fe; color: #0369a1; }
.badge-luxury { background: #f3e8ff; color: #6b21a8; }

.aeris-val-hero {
    font-family: var(--font-mono); font-size: 2.6rem; font-weight: 800;
    color: #0b1c30; letter-spacing: -0.03em; line-height: 1.1; margin: 6px 0;
}
.aeris-val-idr { font-family: var(--font-sans); font-size: 1.05rem; font-weight: 600; color: var(--primary); }

/* SHAP Breakdown Items */
.shap-item {
    display: flex; justify-content: space-between; align-items: center; padding: 8px 12px;
    border-radius: 8px; background: #f8faff; border: 1px solid #e2e8f0; margin-bottom: 6px; font-size: 0.85rem;
}
.shap-val-pos { font-family: var(--font-mono); font-weight: 700; color: var(--shap-pos); }
.shap-val-neg { font-family: var(--font-mono); font-weight: 700; color: var(--shap-neg); }

/* Buttons */
div.stButton > button:first-child {
    background-color: var(--primary) !important; color: #ffffff !important;
    font-family: var(--font-sans) !important; font-weight: 700 !important; border-radius: 12px !important;
    border: none !important; padding: 12px 24px !important; box-shadow: 0 4px 14px rgba(0, 105, 72, 0.25) !important;
    transition: all 0.2s ease !important;
}
div.stButton > button:first-child:hover {
    background-color: var(--primary-container) !important; transform: translateY(-1px) !important;
}

/* Custom Sidebar Navigation (Stitch Pills) */
section[data-testid="stSidebar"] {
    background: #ffffff !important; border-right: 1px solid #e2e8f0 !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] {
    display: flex; flex-direction: column; gap: 4px;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label {
    background: #f8faff !important; border: 1px solid #eef2f6 !important;
    padding: 8px 12px !important; border-radius: 10px !important;
    cursor: pointer !important; display: flex !important; align-items: center !important; margin: 0 !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: #eff4ff !important; border-color: #00855d !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label p {
    color: #0b1c30 !important; font-size: 0.825rem !important; font-weight: 600 !important; margin: 0 !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label > div:first-child { display: none !important; }
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
    background: #006948 !important; border-color: #006948 !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) p {
    color: #ffffff !important;
}

header[data-testid="stHeader"] { background: transparent !important; }
#MainMenu, footer { visibility: hidden; }
</style>
"""
