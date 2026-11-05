"""
KingCounty-AVM: Automated Real Estate Valuation & Spatial Intelligence Engine
Design System: Aeris Spatial Valuation (Google Stitch)
Main Application Entrypoint & Router
"""

import os
import sys
import streamlit as st

# Pastikan direktori app dan root proyek berada dalam sys.path
APP_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(APP_DIR)
for p in [APP_DIR, PROJECT_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)

from styles import AERIS_CSS
from config import load_models_and_metadata, load_clean_data_sample, get_zip_coordinates
from views import (
    render_valuator,
    render_explorer,
    render_explainability,
    render_simulator,
    render_methodology
)

# 1. Konfigurasi Halaman & Injeksi Stylesheet Aeris Spatial Valuation
icon_path = os.path.join(APP_DIR, "assets", "icon.png")
st.set_page_config(
    page_title="KingCounty-AVM | Enterprise Real Estate Valuation",
    page_icon=icon_path if os.path.exists(icon_path) else "A",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown(AERIS_CSS, unsafe_allow_html=True)

# 2. Pemuatan Data & Model Ter-Cache
reg_model, clf_model, metadata = load_models_and_metadata()
clean_df = load_clean_data_sample()
zip_coords, all_zipcodes = get_zip_coordinates(clean_df)

# 3. Sidebar Navigasi (Stitch Aeris Branding)
st.sidebar.markdown(
    """
    <div style="display:flex; align-items:center; gap:12px; margin-bottom:20px; padding:4px 0;">
        <div style="background:#006948; color:white; border-radius:12px; width:44px; height:44px; display:flex; align-items:center; justify-content:center; box-shadow:0 4px 12px rgba(0,105,72,0.25);">
            <span class="material-symbols-outlined" style="font-size:26px; color:#ffffff;">apartment</span>
        </div>
        <div>
            <div style="font-weight:800; font-size:1.15rem; color:#0b1c30; letter-spacing:-0.02em; line-height:1.2;">KingCounty-AVM</div>
            <div style="font-size:0.75rem; color:#006948; font-family:'JetBrains Mono'; font-weight:600;">Aeris Spatial Engine</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

NAV_VALUATOR = "Smart AVM Valuator"
NAV_EXPLORER = "Market Overview & Spatial Explorer"
NAV_XAI = "SHAP XAI Decomposition"
NAV_SIMULATOR = "Renovation ROI Simulator"
NAV_METHODOLOGY = "Model Health & Methodology"

app_mode = st.sidebar.radio(
    "Navigation Modules:",
    [NAV_VALUATOR, NAV_EXPLORER, NAV_XAI, NAV_SIMULATOR, NAV_METHODOLOGY],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    f"""
    <div style="background:#eff4ff; border:1px solid #dce9ff; border-radius:14px; padding:14px; font-size:0.8rem;">
        <div style="font-weight:700; color:#006398; margin-bottom:4px; display:flex; align-items:center; gap:6px;">
            <span class="material-symbols-outlined" style="font-size:16px;">verified</span>
            v2.4 Production Engine
        </div>
        <div style="color:#475569; margin-bottom:8px;">
            Trained on <b>22,847 King County parcels</b> with validated spatial metrics.
        </div>
        <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
            <span>Core Regressor:</span>
            <span style="font-family:'JetBrains Mono'; font-weight:700; color:#006948;">LightGBM / HGB</span>
        </div>
        <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
            <span>Test R² Score:</span>
            <span style="font-family:'JetBrains Mono'; font-weight:700; color:#006948;">0.8848</span>
        </div>
        <div style="display:flex; justify-content:space-between;">
            <span>Test MAPE:</span>
            <span style="font-family:'JetBrains Mono'; font-weight:700; color:#006948;">13.39%</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# 4. Router Modul Halaman
if app_mode == NAV_VALUATOR:
    render_valuator(reg_model, clf_model, metadata, zip_coords, all_zipcodes)
elif app_mode == NAV_EXPLORER:
    render_explorer(clean_df)
elif app_mode == NAV_XAI:
    render_explainability(metadata)
elif app_mode == NAV_SIMULATOR:
    render_simulator(reg_model, metadata, zip_coords, all_zipcodes)
elif app_mode == NAV_METHODOLOGY:
    render_methodology()
