"""
Modul Tampilan: Model Health & Methodology (Modul 5)
Dokumentasi teknis arsitektur model, tabel scorecard algoritma (Regresi, Klasifikasi, dan K-Means Clustering), dan landasan data.
"""

import streamlit as st
import pandas as pd

def render_methodology(metadata=None):
    """Merender halaman dokumentasi metodologi ekonometrika dan scorecard performa."""
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
                Empirical evaluation benchmarks across 7 comparative regression models, multi-class classification, and unsupervised micro-market spatial clustering.
            </p>
        </div>
        """, unsafe_allow_html=True
    )

    st.markdown('<div class="aeris-card">', unsafe_allow_html=True)
    st.markdown(
        """
        <div style="display:flex; align-items:center; gap:8px; margin-bottom:12px;">
            <span class="material-symbols-outlined" style="color:#006948; font-size:22px;">assessment</span>
            <h3 style="margin:0; font-size:1.15rem; font-weight:700; color:#0b1c30;">Regression Algorithm Performance Scorecard (7 Models)</h3>
        </div>
        """, unsafe_allow_html=True
    )
    scorecard = [
        {"Model Algorithm": "OLS Linear Regression", "R² (Log)": "0.7460", "RMSE (Log)": "0.2860", "MAPE": "22.04%", "MAE": "$124,551", "Paradigma": "Classical Econometrics"},
        {"Model Algorithm": "Ridge Regression (L2)", "R² (Log)": "0.7460", "RMSE (Log)": "0.2859", "MAPE": "22.01%", "MAE": "$124,387", "Paradigma": "Regularized L2 (Shrinkage)"},
        {"Model Algorithm": "Lasso Regression (L1)", "R² (Log)": "0.7458", "RMSE (Log)": "0.2861", "MAPE": "22.05%", "MAE": "$124,637", "Paradigma": "Regularized L1 (Sparsity)"},
        {"Model Algorithm": "Elastic Net Regression", "R² (Log)": "0.7460", "RMSE (Log)": "0.2860", "MAPE": "22.03%", "MAE": "$124,510", "Paradigma": "Hybrid L1 + L2 Regularization"},
        {"Model Algorithm": "Decision Tree Regressor", "R² (Log)": "0.8168", "RMSE (Log)": "0.2429", "MAPE": "17.60%", "MAE": "$98,721", "Paradigma": "Non-Linear Decision Tree"},
        {"Model Algorithm": "Random Forest Regressor", "R² (Log)": "0.8659", "RMSE (Log)": "0.2078", "MAPE": "14.34%", "MAE": "$79,588", "Paradigma": "Tree Ensemble (Bagging)"},
        {"Model Algorithm": "HistGradientBoosting Regressor", "R² (Log)": "0.8836 (Production)", "RMSE (Log)": "0.1936", "MAPE": "13.55%", "MAE": "$73,452", "Paradigma": "Tree Ensemble (Boosting)"}
    ]
    st.table(pd.DataFrame(scorecard))

    st.markdown(
        """
        <div style="display:flex; align-items:center; gap:8px; margin-bottom:12px; margin-top:24px;">
            <span class="material-symbols-outlined" style="color:#006948; font-size:22px;">category</span>
            <h3 style="margin:0; font-size:1.15rem; font-weight:700; color:#0b1c30;">Market Tier Classifier Performance Scorecard</h3>
        </div>
        """, unsafe_allow_html=True
    )
    clf_scorecard = [
        {"Classifier Algorithm": "Decision Tree Classifier", "Accuracy": "83.52%", "Macro F1-Score": "0.8350", "Status": "Baseline Tree"},
        {"Classifier Algorithm": "Random Forest Classifier", "Accuracy": "85.96%", "Macro F1-Score": "0.8568", "Status": "Ensemble Bagging"},
        {"Classifier Algorithm": "HistGradientBoosting Classifier", "Accuracy": "87.78%", "Macro F1-Score": "0.8774", "Status": "Production Classifier"}
    ]
    st.table(pd.DataFrame(clf_scorecard))

    st.markdown(
        """
        <div style="display:flex; align-items:center; gap:8px; margin-bottom:12px; margin-top:24px;">
            <span class="material-symbols-outlined" style="color:#006948; font-size:22px;">hub</span>
            <h3 style="margin:0; font-size:1.15rem; font-weight:700; color:#0b1c30;">Unsupervised Learning: K-Means Micro-Market Clustering (k=6)</h3>
        </div>
        <p style="font-size:0.88rem; color:#475569; margin-top:-6px; margin-bottom:12px;">
            Spatial-economic segmentation partitioning King County into 6 micro-markets based on Latitude, Longitude, and ln(SalePrice).
        </p>
        """, unsafe_allow_html=True
    )
    cluster_scorecard = [
        {"Metrik Evaluasi": "Inertia (Within-Cluster Sum of Squares)", "Skor Nilai": "19,691.06", "Keterangan": "Konvergensi kompak WCSS"},
        {"Metrik Evaluasi": "Silhouette Score (5,000 Sample)", "Skor Nilai": "0.3120", "Keterangan": "Pemisahan batas klaster spasial-ekonomi solid"},
        {"Metrik Evaluasi": "Calinski-Harabasz Score", "Skor Nilai": "11,215.17", "Keterangan": "Rasio dispersi antar-klaster sangat tinggi"},
        {"Metrik Evaluasi": "Davies-Bouldin Index", "Skor Nilai": "1.0748", "Keterangan": "Indeks kedekatan mendekati 1.0 (klaster terpisah baik)"}
    ]
    st.table(pd.DataFrame(cluster_scorecard))

    st.markdown(
        """
        <div style="display:flex; align-items:center; gap:8px; margin-bottom:12px; margin-top:24px;">
            <span class="material-symbols-outlined" style="color:#006398; font-size:22px;">source</span>
            <h3 style="margin:0; font-size:1.15rem; font-weight:700; color:#0b1c30;">Data Provenance & Citation</h3>
        </div>
        """, unsafe_allow_html=True
    )
    st.markdown("""
    - **Primary Dataset:** King County Department of Assessments & University of Washington (*Harvard Dataverse*).
    - **Methodology:** CRISP-DM (*Cross-Industry Standard Process for Data Mining*) & Hedonic Pricing Econometrics.
    - **Machine Learning Scope:** Supervised Hedonic Regression (7 models), Tier Classification (3 models), & Unsupervised Spatial K-Means Clustering ($k=6$).
    - **Core Stack:** Python 3.12, Scikit-Learn 1.4+, Streamlit, Plotly, Joblib, Pandas, NumPy.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
