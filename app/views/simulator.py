"""
Modul Tampilan: Renovation ROI Simulator (Modul 4)
Simulasi peningkatan grade, kondisi, dan luas bangunan untuk proyeksi laba renovasi.
"""

import streamlit as st
import pandas as pd
import numpy as np

def render_simulator(reg_model, metadata, zip_coords, all_zipcodes):
    """Merender halaman simulator proyeksi ROI renovasi dan pertambahan ekuitas."""
    st.markdown(
        """
        <div style="margin-bottom:20px;">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
                <span class="aeris-badge badge-primary">Scenario Modeling</span>
                <span class="aeris-badge badge-muted">Value-Add Equity Forecasting</span>
            </div>
            <h1 style="font-size:2.2rem; font-weight:800; color:#0b1c30; margin:0 0 6px 0;">
                Renovation ROI & Equity Simulator
            </h1>
            <p style="color:#475569; font-size:0.95rem; margin:0;">
                Simulating capital allocation scenarios to forecast equity expansion from architectural upgrades.
            </p>
        </div>
        """, unsafe_allow_html=True
    )

    r_col1, r_col2 = st.columns(2)
    with r_col1:
        st.markdown('<div class="aeris-card">', unsafe_allow_html=True)
        st.markdown(
            """
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:12px;">
                <span class="material-symbols-outlined" style="color:#006398;">home</span>
                <h3 style="margin:0; font-size:1.15rem; font-weight:700; color:#0b1c30;">Baseline: Current Status</h3>
            </div>
            """, unsafe_allow_html=True
        )
        b_grade = st.slider("Current Grade", 4, 11, 7, key="sim_b_grade")
        b_cond = st.slider("Current Condition", 1, 5, 3, key="sim_b_cond")
        b_sqft = st.number_input("Current Living SqFt", value=1950, step=50, key="sim_b_sqft")
        b_zip = st.selectbox("Property ZipCode", all_zipcodes, index=all_zipcodes.index("98108") if "98108" in all_zipcodes else 0, key="sim_b_zip")
        b_budget = st.number_input("Renovation Capital Budget ($)", value=55000, step=5000, key="sim_b_budget")
        st.markdown('</div>', unsafe_allow_html=True)

    with r_col2:
        st.markdown('<div class="aeris-card">', unsafe_allow_html=True)
        st.markdown(
            """
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:12px;">
                <span class="material-symbols-outlined" style="color:#006948;">construction</span>
                <h3 style="margin:0; font-size:1.15rem; font-weight:700; color:#0b1c30;">Scenario: Target Renovation</h3>
            </div>
            """, unsafe_allow_html=True
        )
        t_grade = st.slider("Target Building Grade", 4, 12, max(b_grade, 9), key="sim_t_grade")
        t_cond = st.slider("Target Condition", 1, 5, 5, key="sim_t_cond")
        t_add_sqft = st.number_input("Living Area Expansion (SqFt)", value=250, step=50, key="sim_t_add_sqft")
        st.markdown('</div>', unsafe_allow_html=True)

    lat_sim = zip_coords.get(b_zip, {}).get("Latitude", 47.5614)
    lon_sim = zip_coords.get(b_zip, {}).get("Longitude", -122.3094)

    row_before = pd.DataFrame([{
        'SqFtTotLiving': b_sqft, 'SqFtLot': 6500, 'Bedrooms': 3, 'TotalBaths': 2.0, 'Stories': 1.0,
        'SqFtTotBasement': 0, 'SqFtGarageAttached': 350, 'BldgGrade': b_grade, 'Condition': b_cond,
        'PropertyAge': 35, 'IsRenovated': 0, 'Latitude': lat_sim, 'Longitude': lon_sim,
        'IsWaterfront': 0, 'HasView': 0, 'TrafficNoise': 0, 'AirportNoise': 0, 'salesYear': 2015
    }])[metadata['features']]

    row_after = pd.DataFrame([{
        'SqFtTotLiving': b_sqft + t_add_sqft, 'SqFtLot': 6500, 'Bedrooms': 3, 'TotalBaths': 2.5, 'Stories': 1.0,
        'SqFtTotBasement': 0, 'SqFtGarageAttached': 350, 'BldgGrade': t_grade, 'Condition': t_cond,
        'PropertyAge': 35, 'IsRenovated': 1, 'Latitude': lat_sim, 'Longitude': lon_sim,
        'IsWaterfront': 0, 'HasView': 0, 'TrafficNoise': 0, 'AirportNoise': 0, 'salesYear': 2015
    }])[metadata['features']]

    price_before = np.exp(reg_model.predict(row_before)[0])
    price_after = np.exp(reg_model.predict(row_after)[0])
    gain = price_after - price_before
    net_profit = gain - b_budget
    roi = (net_profit / b_budget) * 100 if b_budget > 0 else 0

    st.markdown('<div class="aeris-card-hero">', unsafe_allow_html=True)
    res1, res2, res3, res4 = st.columns(4)
    res1.metric("Pre-Reno Valuation", f"${price_before:,.0f}")
    res2.metric("Post-Reno Valuation", f"${price_after:,.0f}", delta=f"+${gain:,.0f}")
    res3.metric("Net Equity Gain", f"${net_profit:,.0f}", delta=f"${net_profit:,.0f}")
    res4.metric("Projected ROI", f"{roi:.1f}%")

    if net_profit > 0:
        st.markdown(
            f"""
            <div style="background:#ecfdf5; border:1px solid #a7f3d0; border-radius:12px; padding:14px 18px; margin-top:16px; display:flex; align-items:center; gap:12px;">
                <span class="material-symbols-outlined" style="color:#059669; font-size:24px;">task_alt</span>
                <div>
                    <div style="font-weight:700; color:#065f46; font-size:0.95rem;">Rencana Renovasi Layak Eksekusi (High Equity Return)</div>
                    <div style="color:#047857; font-size:0.875rem;">Proyeksi kenaikan nilai properti <b>+${gain:,.0f}</b> menghasilkan laba bersih <b>+${net_profit:,.0f}</b>.</div>
                </div>
            </div>
            """, unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <div style="background:#fffbeb; border:1px solid #fde68a; border-radius:12px; padding:14px 18px; margin-top:16px; display:flex; align-items:center; gap:12px;">
                <span class="material-symbols-outlined" style="color:#d97706; font-size:24px;">warning</span>
                <div>
                    <div style="font-weight:700; color:#92400e; font-size:0.95rem;">Peringatan Efisiensi Anggaran (Marginal Return)</div>
                    <div style="color:#b45309; font-size:0.875rem;">Biaya renovasi melampaui estimasi kenaikan nilai pasar wajar properti. Pertimbangkan efisiensi scope.</div>
                </div>
            </div>
            """, unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)
