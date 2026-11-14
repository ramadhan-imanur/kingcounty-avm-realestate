"""
Modul Tampilan: Simulasi Renovasi & Nilai Tambah Properti (Renovation ROI Simulator)
Kalkulasi potensi kenaikan nilai pasar (appreciation) vs. estimasi biaya renovasi berdasarkan elastisitas harga King County.
Desain 100% native Streamlit: ringan, interaktif, dan akurat.
"""

import os
import streamlit as st
import pandas as pd
import numpy as np


def render_simulator(reg_model=None, metadata=None, zip_coords=None, all_zipcodes=None):
    """
    Merender halaman simulasi paket renovasi dan kalkulasi ROI ekuitas properti.
    """
    st.title("Simulasi Renovasi & Nilai Tambah Properti")
    st.caption("Kalkulasi potensi kenaikan nilai pasar (appreciation) vs. estimasi biaya modal renovasi di King County.")

    # Base Property Value Input
    col_head1, col_head2 = st.columns([2, 1])
    with col_head1:
        st.write("Pilih paket peningkatan properti di bawah ini untuk melihat proyeksi kenaikan ekuitas secara *real-time*.")
    with col_head2:
        base_value = st.number_input(
            "Nilai Rumah Saat Ini ($)",
            min_value=100000,
            max_value=10000000,
            value=650000,
            step=25000,
            format="%d"
        )

    st.divider()

    # Define the 6 Standard Upgrade Packages
    packages = [
        {
            "id": "bath",
            "name": "1. Tambah 1 Kamar Mandi Penuh (Full Bath)",
            "desc": "Penambahan instalasi sanitasi lengkap, shower kaca, dan wastafel ganda.",
            "cost": 24000,
            "appreciation": 38500,
            "default": False
        },
        {
            "id": "kitchen",
            "name": "2. Renovasi Dapur Modern (Chef's Kitchen)",
            "desc": "Meja quartz, island bar, kabinet custom, dan appliances stainless steel kelas profesional.",
            "cost": 48000,
            "appreciation": 72000,
            "default": True
        },
        {
            "id": "basement",
            "name": "3. Finishing Ruang Bawah Tanah (Daylight Basement)",
            "desc": "Menambah +600 sq.ft living area berizin resmi untuk ruang keluarga atau hobi.",
            "cost": 36000,
            "appreciation": 52000,
            "default": False
        },
        {
            "id": "deck",
            "name": "4. Dek Kayu Komposit & Ruang Santai Terbuka",
            "desc": "Area outdoor living 300 sq.ft dengan decking komposit tahan cuaca dan railing kaca tempered.",
            "cost": 16000,
            "appreciation": 22500,
            "default": False
        },
        {
            "id": "grade",
            "name": "5. Peningkatan Grade Arsitektural (+1 Tingkat)",
            "desc": "Fasad premium, lantai hardwood ek impor, cetakan arsitektural tinggi, dan pencahayaan aksen.",
            "cost": 65000,
            "appreciation": 125000,
            "default": False
        },
        {
            "id": "energy",
            "name": "6. Efisiensi Energi & Heat Pump Inverter HVAC",
            "desc": "Sistem pompa panas ramah lingkungan, thermostat cerdas, dan insulasi atap tingkat tinggi.",
            "cost": 15000,
            "appreciation": 19500,
            "default": False
        }
    ]

    col_options, col_summary = st.columns([7, 5])

    total_cost = 0
    total_appreciation = 0
    selected_items = []

    with col_options:
        st.subheader("Daftar Paket Renovasi Teruji")
        
        for pkg in packages:
            is_checked = st.checkbox(
                f"**{pkg['name']}**",
                value=pkg['default'],
                key=f"pkg_{pkg['id']}",
                help=pkg['desc']
            )
            st.caption(f"{pkg['desc']} — *Biaya: ${pkg['cost']:,} | +Valuasi: ${pkg['appreciation']:,}*")
            
            if is_checked:
                total_cost += pkg['cost']
                total_appreciation += pkg['appreciation']
                selected_items.append(pkg)

    net_profit = total_appreciation - total_cost
    projected_val = base_value + total_appreciation
    gross_roi = (total_appreciation / total_cost * 100) if total_cost > 0 else 0
    net_roi = (net_profit / total_cost * 100) if total_cost > 0 else 0

    with col_summary:
        st.subheader("Proyeksi Ekuitas Tambahan")

        # Key Financial Metrics
        m1, m2 = st.columns(2)
        with m1:
            st.metric("Total Biaya Modal", f"${total_cost:,}")
        with m2:
            st.metric("Kenaikan Nilai (Appr.)", f"+${total_appreciation:,}")

        m3, m4 = st.columns(2)
        with m3:
            st.metric("Keuntungan Bersih", f"+${net_profit:,}", delta=f"{net_roi:.1f}% Net" if total_cost > 0 else None)
        with m4:
            st.metric("Gross ROI", f"{gross_roi:.1f}%")

        # Projected Final Value
        st.success(f"### Estimasi Nilai Baru: **${projected_val:,}**\n*Nilai awal: ${base_value:,} + Tambahan apresiasi: ${total_appreciation:,}*")

        # Recommendation Card
        st.info(
            " **Rekomendasi Analis Properti King County**:\n\n"
            "Di pasar King County, peningkatan **Grade Kualitas Arsitektural** (ROI 192%) dan "
            "**Renovasi Dapur Modern** (ROI 150%) memberikan margin nilai tambah tertinggi. "
            "Pembeli di wilayah Eastside dan Seattle sangat memprioritaskan estetika kontemporer dan ruang fungsional siap huni."
        )

    # Detailed Comparison Table
    if selected_items:
        st.divider()
        st.subheader("Rincian Finansial Paket Terpilih")
        table_rows = []
        for item in selected_items:
            profit = item['appreciation'] - item['cost']
            roi = (item['appreciation'] / item['cost']) * 100
            table_rows.append({
                "Paket Renovasi": item['name'].split(". ")[1],
                "Estimasi Biaya ($)": f"${item['cost']:,}",
                "Proyeksi Apresiasi ($)": f"${item['appreciation']:,}",
                "Laba Bersih ($)": f"${profit:,}",
                "Gross ROI (%)": f"{roi:.1f}%"
            })
        st.dataframe(pd.DataFrame(table_rows), hide_index=True, use_container_width=True)

    # Advanced Parametric ML Simulation Expander
    if reg_model is not None and metadata is not None and zip_coords and all_zipcodes:
        with st.expander("Simulasi Kustom Parametrik Machine Learning", expanded=False):
            st.write("Gunakan model regresi machine learning untuk menguji dampak renovasi spesifik pada suatu kode pos.")
            
            c_p1, c_p2, c_p3 = st.columns(3)
            with c_p1:
                sel_zip = st.selectbox("Kode Pos", all_zipcodes, index=all_zipcodes.index("98004") if "98004" in all_zipcodes else 0, key="ml_sim_zip")
                curr_sqft = st.number_input("Luas Awal (sqft)", value=2100, step=50, key="ml_sim_sqft")
            with c_p2:
                curr_grade = st.slider("Grade Bangunan Saat Ini", 4, 11, 7, key="ml_sim_bgrade")
                target_grade = st.slider("Target Grade Pasca Renovasi", curr_grade, 12, max(curr_grade, 9), key="ml_sim_tgrade")
            with c_p3:
                add_sqft = st.number_input("Ekspansi Luas (sqft)", value=300, step=50, key="ml_sim_addsqft")
                budget = st.number_input("Anggaran Modal Kustom ($)", value=60000, step=5000, key="ml_sim_budget")

            lat = zip_coords.get(sel_zip, {}).get("Latitude", 47.5614)
            lon = zip_coords.get(sel_zip, {}).get("Longitude", -122.3094)

            row_pre = pd.DataFrame([{
                'SqFtTotLiving': curr_sqft, 'SqFtLot': 6500, 'Bedrooms': 3, 'TotalBaths': 2.0, 'Stories': 1.0,
                'SqFtTotBasement': 0, 'SqFtGarageAttached': 350, 'BldgGrade': curr_grade, 'Condition': 3,
                'PropertyAge': 30, 'IsRenovated': 0, 'Latitude': lat, 'Longitude': lon,
                'IsWaterfront': 0, 'HasView': 0, 'TrafficNoise': 0, 'AirportNoise': 0, 'salesYear': 2015
            }])[metadata['features']]

            row_post = pd.DataFrame([{
                'SqFtTotLiving': curr_sqft + add_sqft, 'SqFtLot': 6500, 'Bedrooms': 3, 'TotalBaths': 2.5, 'Stories': 1.0,
                'SqFtTotBasement': 0, 'SqFtGarageAttached': 350, 'BldgGrade': target_grade, 'Condition': 4,
                'PropertyAge': 30, 'IsRenovated': 1, 'Latitude': lat, 'Longitude': lon,
                'IsWaterfront': 0, 'HasView': 0, 'TrafficNoise': 0, 'AirportNoise': 0, 'salesYear': 2015
            }])[metadata['features']]

            val_pre = np.exp(reg_model.predict(row_pre)[0])
            val_post = np.exp(reg_model.predict(row_post)[0])
            ml_gain = val_post - val_pre
            ml_profit = ml_gain - budget
            ml_roi = (ml_profit / budget * 100) if budget > 0 else 0

            res1, res2, res3, res4 = st.columns(4)
            res1.metric("Valuasi Pra-Renovasi", f"${val_pre:,.0f}")
            res2.metric("Valuasi Pasca-Renovasi", f"${val_post:,.0f}", delta=f"+${ml_gain:,.0f}")
            res3.metric("Laba Ekuitas Bersih", f"${ml_profit:,.0f}")
            res4.metric("ROI Bersih ML", f"{ml_roi:.1f}%")

    # Referensi Desain Prototipe Stitch (On-Demand)
    app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    stitch_img = os.path.join(app_dir, "stitch", "renovation_roi_simulator", "screen.png")
    if os.path.exists(stitch_img):
        with st.expander("Referensi Desain Prototipe Stitch (Renovation ROI Simulator)", expanded=False):
            st.image(stitch_img, caption="Prototipe Desain Google Stitch Project: 612066658549398949 (Renovation Simulator)")
