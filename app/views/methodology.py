"""
Modul Tampilan: Model Health & Methodology (Modul 5)
Dokumentasi teknis arsitektur model, tabel scorecard algoritma, dan landasan data.
"""

import streamlit as st
import pandas as pd

def render_methodology():
    """
    Merender halaman dokumentasi metodologi ekonometrika dan scorecard performa.
    """
    st.markdown(
        """
        <div style="margin-bottom:20px;">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
                <span class="aeris-badge badge-primary">Model Governance</span>
                <span class="aeris-badge badge-muted">Audit Verification</span>
            </div>
            <h1 style="font-size:2.2rem; font-weight:800; color:#0b1c30; margin:0 0 6px 0;">
                Model Health & Technical Architecture
            </h1>
            <p style="color:#475569; font-size:0.95rem; margin:0;">
                Empirical evaluation benchmarks and econometric foundations.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="aeris-card">', unsafe_allow_html=True)
    st.subheader("📊 Regression Algorithm Performance Scorecard")
    scorecard = [
        {"Model Algorithm": "OLS Linear Regression", "R² (Log)": 0.7460, "RMSE (Log)": 0.2860, "MAPE": "22.04%", "MAE": "$124,551"},
        {"Model Algorithm": "Ridge Regression (L2)", "R² (Log)": 0.7460, "RMSE (Log)": 0.2859, "MAPE": "22.01%", "MAE": "$124,387"},
        {"Model Algorithm": "Random Forest Regressor", "R² (Log)": 0.8659, "RMSE (Log)": 0.2078, "MAPE": "14.33%", "MAE": "$79,623"},
        {"Model Algorithm": "HistGradientBoosting Regressor", "R² (Log)": "0.8848 (Production)", "RMSE (Log)": 0.1926, "MAPE": "13.39%", "MAE": "$72,329"}
    ]
    st.table(pd.DataFrame(scorecard))

    st.subheader("📚 Data Provenance & Citation")
    st.markdown("""
    - **Primary Dataset:** King County Department of Assessments & University of Washington (*Harvard Dataverse*).
    - **Methodology:** CRISP-DM (*Cross-Industry Standard Process for Data Mining*) & Hedonic Pricing Econometrics.
    - **Core Stack:** Python 3.12, Scikit-Learn 1.4, Streamlit, Plotly, Joblib, Pandas, NumPy.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
