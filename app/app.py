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
st.set_page_config(
    page_title="KingCounty-AVM | Smart Valuator",
    page_icon="🏠",
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
    <div style="display:flex; align-items:center; gap:12px; margin-bottom:16px;">
        <div style="background:#006948; color:white; border-radius:12px; width:44px; height:44px; display:flex; align-items:center; justify-content:center; font-weight:800; font-size:1.3rem;">
            KC
        </div>
        <div>
            <div style="font-weight:700; font-size:1.1rem; color:#0b1c30; line-height:1.2;">KingCounty-AVM</div>
            <div style="font-size:0.75rem; color:#64748B; font-family:'JetBrains Mono';">Aeris Spatial Valuation</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

app_mode = st.sidebar.radio(
    "Modul Navigasi:",
    [
        "🏠 Smart AVM Valuator",
        "📊 Market Overview & Spatial Explorer",
        "🔍 Shapley Feature Attribution (XAI)",
        "🔨 Renovation ROI Simulator",
        "ℹ️ Model Health & Methodology"
    ]
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
            Trained on <b>22,847 King County parcels</b> with validated geospatial metrics.
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
if app_mode == "🏠 Smart AVM Valuator":
    render_valuator(reg_model, clf_model, metadata, zip_coords, all_zipcodes)
elif app_mode == "📊 Market Overview & Spatial Explorer":
    render_explorer(clean_df)
elif app_mode == "🔍 Shapley Feature Attribution (XAI)":
    render_explainability(metadata)
elif app_mode == "🔨 Renovation ROI Simulator":
    render_simulator(reg_model, metadata, zip_coords, all_zipcodes)
elif app_mode == "ℹ️ Model Health & Methodology":
    render_methodology()
