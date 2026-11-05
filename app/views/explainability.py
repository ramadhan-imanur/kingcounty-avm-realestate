"""
Modul Tampilan: Shapley Feature Attribution / XAI (Modul 3)
Visualisasi bobot Permutation Importance dan penjelasan naratif pilar ekonometrika.
"""

import streamlit as st
import pandas as pd
import plotly.express as px

def render_explainability(metadata):
    """
    Merender halaman dekomposisi bobot fitur model dan transparansi XAI.
    """
    st.markdown(
        """
        <div style="margin-bottom:20px;">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
                <span class="aeris-badge badge-primary">Model Explainability</span>
                <span class="aeris-badge badge-muted">Game-Theoretic Shapley Decomposition</span>
            </div>
            <h1 style="font-size:2.2rem; font-weight:800; color:#0b1c30; margin:0 0 6px 0;">
                Permutation Importance & Explainability (XAI)
            </h1>
            <p style="color:#475569; font-size:0.95rem; margin:0;">
                Decomposing the underlying drivers of King County real estate valuation accuracy.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    ranked_imp = metadata['feature_importance_ranked']
    imp_df = pd.DataFrame(ranked_imp, columns=["Predictor Attribute", "Importance (R² Loss)"])

    c_chart, c_text = st.columns([6, 5])
    with c_chart:
        st.markdown('<div class="aeris-card">', unsafe_allow_html=True)
        st.subheader("Peringkat Bobot Kontribusi Fitur Model")
        fig_bar = px.bar(
            imp_df.head(10).iloc[::-1],
            x="Importance (R² Loss)",
            y="Predictor Attribute",
            orientation="h",
            color="Importance (R² Loss)",
            color_continuous_scale="Teal",
            title="Top 10 Drivers of Property Valuation (Permutation Method)"
        )
        fig_bar.update_layout(
            font_family="Plus Jakarta Sans",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(248,250,252,0.5)",
            height=460,
            margin=dict(l=0, r=0, t=30, b=0)
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c_text:
        st.markdown(
            """
            <div class="aeris-card">
                <h3 style="font-size:1.15rem; font-weight:700; color:#0b1c30; margin-top:0;">
                    💡 Tiga Pilar Utama Valuasi Ekonometrika
                </h3>
                <div style="font-size:0.9rem; line-height:1.6; color:#475569;">
                    <p><b>1. Lokasi Spasial (Latitude & Longitude):</b><br>
                    Koordinat geografis menjadi faktor penentu tunggal terkuat. King County bagian utara (Bellevue, Redmond, Kirkland, Seattle Utara) memiliki premi lokasi yang sangat tinggi berkat kedekatan dengan danau dan pusat industri teknologi dunia.</p>
                    <p><b>2. Luas Area Hunian (SqFtTotLiving):</b><br>
                    Ukuran riil bangunan fisik berkontribusi linear terhadap nilai properti. Penambahan 100 sqft secara konsisten meningkatkan batas bawah taksiran harga pasar.</p>
                    <p><b>3. Kualitas Konstruksi (BldgGrade):</b><br>
                    Penilaian material dan pengerjaan arsitektur skala 1–13 memberikan lompatan nilai non-linear yang tajam pada segmen menengah ke atas.</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
