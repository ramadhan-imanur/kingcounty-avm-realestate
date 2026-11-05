"""
Aplikasi Web Streamlit - Proyek Sains Data 2026
KingCounty-AVM: Automated Valuation Model & Spatial Real Estate Intelligence Engine
Tim 6 Sains Data FMIPA UNS
"""

import os
import json
import joblib
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# 1. Konfigurasi Halaman Web
st.set_page_config(
    page_title="KingCounty-AVM | Smart Real Estate Valuation",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Pemuatan Model & Data Ter-Cache (dengan Self-Healing Cloud Fallback)
@st.cache_resource
def load_models_and_metadata():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    models_dir = os.path.join(base_dir, "models")
    
    reg_path = os.path.join(models_dir, "best_valuation_model.joblib")
    clf_path = os.path.join(models_dir, "market_tier_classifier.joblib")
    meta_path = os.path.join(models_dir, "model_metadata.json")
    
    with open(meta_path, "r") as f:
        metadata = json.load(f)
        
    reg_model = None
    clf_model = None
    
    # 1. Coba muat model serialisasi
    try:
        reg_model = joblib.load(reg_path)
        clf_model = joblib.load(clf_path)
        # Verifikasi kompatibilitas inferensi scikit-learn
        dummy_sample = pd.DataFrame([metadata['feature_defaults']])[metadata['features']]
        reg_model.predict(dummy_sample)
        clf_model.predict(dummy_sample)
    except Exception as err:
        # Fallback otomatis jika terjadi ketidakcocokan versi Python / Scikit-Learn / Pickle di Cloud
        from sklearn.ensemble import HistGradientBoostingRegressor, HistGradientBoostingClassifier
        
        data_path = os.path.join(base_dir, "data", "processed", "king_county_clean.csv")
        df_train = pd.read_csv(data_path, low_memory=False)
        
        features = metadata["features"]
        X = df_train[features]
        y_log = np.log(df_train["SalePrice"])
        y_tier = df_train["PropertyTier"]
        
        reg_model = HistGradientBoostingRegressor(max_iter=250, learning_rate=0.08, random_state=42)
        reg_model.fit(X, y_log)
        
        clf_model = HistGradientBoostingClassifier(max_iter=150, learning_rate=0.08, random_state=42)
        clf_model.fit(X, y_tier)
        
        # Simpan kembali jika memiliki izin tulis
        try:
            joblib.dump(reg_model, reg_path)
            joblib.dump(clf_model, clf_path)
        except Exception:
            pass
        
    return reg_model, clf_model, metadata

@st.cache_data
def load_clean_data_sample():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_path = os.path.join(base_dir, "data", "processed", "king_county_clean.csv")
    df = pd.read_csv(data_path, low_memory=False)
    return df

reg_model, clf_model, metadata = load_models_and_metadata()
clean_df = load_clean_data_sample()

# Koordinat representatif per ZipCode untuk pemetaan instan
zip_coords = clean_df.groupby('ZipCode')[['Latitude', 'Longitude']].median().to_dict(orient='index')
all_zipcodes = sorted([str(z) for z in zip_coords.keys()])

# 3. Sidebar Navigasi & Identitas Proyek
st.sidebar.image("https://img.icons8.com/clouds/200/real-estate.png", width=110)
st.sidebar.title("KingCounty-AVM")
st.sidebar.caption("Automated Property Valuation Engine | Tim 6 FMIPA UNS")
st.sidebar.markdown("---")

app_mode = st.sidebar.radio(
    "Navigasi Modul Sistem:",
    [
        "🏠 Kalkulator Valuasi AVM",
        "📊 Eksplorasi Pasar & Peta Spasial",
        "🔍 Analisis Bobot Fitur (XAI)",
        "🔨 Simulator ROI Renovasi",
        "ℹ️ Metodologi & Evaluasi Model"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info(
    "💡 **Sains Data FMIPA UNS 2026**\n"
    "Dataset: *Harvard Dataverse (King County)*\n"
    f"Model Terbaik: **{metadata['model_name']}**\n"
    f"Akurasi Regresi ($R^2$): **{metadata['metrics_regression']['HistGradientBoosting Regressor']['R2_log']:.4f}**\n"
    f"Akurasi Klasifikasi: **{metadata['metrics_classification']['accuracy']}%**"
)

# ==============================================================================
# MODUL 1: KALKULATOR VALUASI AVM
# ==============================================================================
if app_mode == "🏠 Kalkulator Valuasi AVM":
    st.title("🏠 Automated Valuation Model (AVM) Properti")
    st.markdown(
        "Masukkan spesifikasi fisik, kualitas konstruksi, dan lokasi properti di King County, Washington "
        "untuk memperoleh estimasi harga pasar wajar (*Fair Market Value*) secara instan berbasis Machine Learning."
    )
    st.markdown("---")

    with st.form("valuation_input_form"):
        st.subheader("1. Karakteristik Fisik & Dimensi Bangunan")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            sqft_living = st.number_input(
                "Luas Hunian (SqFt Living)", 
                min_value=300, max_value=15000, value=2050, step=50,
                help="Total luas lantai hunian dalam satuan square feet (1 sqft ≈ 0.093 m²)."
            )
            sqft_lot = st.number_input(
                "Luas Tanah (SqFt Lot)", 
                min_value=500, max_value=500000, value=7500, step=250,
                help="Total luas pekarangan properti."
            )
        with c2:
            bedrooms = st.slider("Jumlah Kamar Tidur", min_value=1, max_value=10, value=3)
            stories = st.selectbox("Jumlah Lantai", options=[1.0, 1.5, 2.0, 2.5, 3.0], index=2)
        with c3:
            bath_full = st.number_input("Kamar Mandi Lengkap (Full Bath)", min_value=1, max_value=8, value=2)
            bath_half = st.number_input("Kamar Mandi Setengah (Half Bath)", min_value=0, max_value=4, value=1)
        with c4:
            sqft_basement = st.number_input("Luas Basement (SqFt)", min_value=0, max_value=5000, value=0, step=100)
            sqft_garage = st.number_input("Luas Garasi Mobil (SqFt)", min_value=0, max_value=2000, value=400, step=50)

        st.subheader("2. Kualitas Konstruksi, Kondisi & Usia")
        q1, q2, q3, q4 = st.columns(4)
        with q1:
            bldg_grade = st.select_slider(
                "Grade Kualitas Bangunan (King County Assessor)",
                options=list(range(4, 14)),
                value=8,
                help="7: Average, 8: Good, 9: Better, 10: Very Good, 11: Luxury/Custom, 12-13: Mansion."
            )
        with q2:
            condition = st.select_slider(
                "Kondisi Pemeliharaan Bangunan",
                options=[1, 2, 3, 4, 5],
                value=4,
                help="1: Buruk/Rusak, 3: Rata-rata Standar, 4: Terawat Baik, 5: Istimewa/Sempurna."
            )
        with q3:
            yr_built = st.number_input("Tahun Pembangunan Awal", min_value=1900, max_value=2025, value=1985)
        with q4:
            is_renovated_opt = st.selectbox("Pernah Direnovasi?", options=["Tidak", "Ya"])
            if is_renovated_opt == "Ya":
                yr_renovated = st.number_input("Tahun Renovasi Terakhir", min_value=1950, max_value=2025, value=2010)
            else:
                yr_renovated = 0

        st.subheader("3. Lokasi Geografis, Pemandangan & Lingkungan")
        l1, l2, l3 = st.columns([1.5, 1.5, 1])
        with l1:
            selected_zip = st.selectbox(
                "Pilih Kode Pos (ZipCode King County)",
                options=all_zipcodes,
                index=all_zipcodes.index("98108") if "98108" in all_zipcodes else 0,
                help="Kode pos secara otomatis menentukan estimasi titik koordinat spasial."
            )
            # Default lat/lon dari ZipCode terpilih
            default_lat = zip_coords.get(selected_zip, {}).get("Latitude", 47.5614)
            default_lon = zip_coords.get(selected_zip, {}).get("Longitude", -122.3094)
            
            coord_exp = st.expander("Sesuaikan Titik Koordinat Spasial Presisi (Opsional)")
            with coord_exp:
                custom_lat = st.number_input("Latitude", value=float(default_lat), format="%.5f")
                custom_lon = st.number_input("Longitude", value=float(default_lon), format="%.5f")

        with l2:
            st.markdown("**Faktor Panorama & Pemandangan:**")
            view_skyline = st.checkbox("Pemandangan Seattle Skyline", value=False)
            view_lake_wa = st.checkbox("Pemandangan Danau Washington", value=False)
            view_lake_sam = st.checkbox("Pemandangan Danau Sammamish", value=False)
            view_sound = st.checkbox("Pemandangan Puget Sound / Laut", value=False)
            view_mountain = st.checkbox("Pemandangan Gunung Rainier / Cascades", value=False)

        with l3:
            st.markdown("**Faktor Lingkungan Sekitar:**")
            is_waterfront = st.checkbox("Lokasi Tepi Air (Waterfront)", value=False)
            traffic_noise = st.checkbox("Terpapar Kebisingan Jalan Raya Utama", value=False)
            airport_noise = st.checkbox("Terpapar Kebisingan Lintasan Bandara", value=False)

        btn_submit = st.form_submit_button("🚀 Hitung Estimasi Valuasi Wajar Properti", use_container_width=True)

    if btn_submit:
        # Kalkulasi Fitur Turunan
        sales_year = 2015
        property_age = max(0, sales_year - yr_built)
        is_renovated_flag = 1 if yr_renovated > 0 else 0
        total_baths = bath_full + 0.5 * bath_half
        has_view = 1 if (view_skyline or view_lake_wa or view_lake_sam or view_sound or view_mountain) else 0

        # Susun DataFrame Input sesuai urutan fitur model
        input_data = pd.DataFrame([{
            'SqFtTotLiving': sqft_living,
            'SqFtLot': sqft_lot,
            'Bedrooms': bedrooms,
            'TotalBaths': total_baths,
            'Stories': stories,
            'SqFtTotBasement': sqft_basement,
            'SqFtGarageAttached': sqft_garage,
            'BldgGrade': bldg_grade,
            'Condition': condition,
            'PropertyAge': property_age,
            'IsRenovated': is_renovated_flag,
            'Latitude': custom_lat,
            'Longitude': custom_lon,
            'IsWaterfront': 1 if is_waterfront else 0,
            'HasView': has_view,
            'TrafficNoise': 1 if traffic_noise else 0,
            'AirportNoise': 1 if airport_noise else 0,
            'salesYear': sales_year
        }])[metadata['features']]

        # Inferensi Model
        pred_log = reg_model.predict(input_data)[0]
        estimated_price = np.exp(pred_log)
        predicted_tier = clf_model.predict(input_data)[0]

        # Rentang Wajar (Confidence Interval 90% berbasis MAPE 13.4%)
        lower_bound = estimated_price * 0.866
        upper_bound = estimated_price * 1.134
        
        # Kurs Indikatif IDR (1 USD = Rp 16.000)
        kurs_usd_idr = 16000
        estimated_idr = estimated_price * kurs_usd_idr

        st.success("✅ Valuasi Berhasil Dihitung!")
        
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric(
                label="💰 Estimasi Nilai Wajar (USD)", 
                value=f"${estimated_price:,.0f}"
            )
        with m2:
            st.metric(
                label="🇮🇩 Estimasi Ekuivalen (Rupiah)", 
                value=f"Rp {estimated_idr/1e9:,.2f} Miliar"
            )
        with m3:
            st.metric(
                label="🏷️ Segmen Kelas Pasar", 
                value=predicted_tier
            )
        with m4:
            st.metric(
                label="📏 Harga per SqFt", 
                value=f"${estimated_price/sqft_living:,.0f} / sqft"
            )

        st.info(
            f"📊 **Rentang Valuasi Wajar Pasar (±13.4% Interval Toleransi):** "
            f"**${lower_bound:,.0f}** s.d. **${upper_bound:,.0f}**\n\n"
            f"📍 *Kode Pos {selected_zip}:* Median harga historis di wilayah ini adalah "
            f"**${metadata['zip_price_medians'].get(selected_zip, 450000):,.0f}**."
        )

# ==============================================================================
# MODUL 2: EKSPLORASI PASAR & PETA SPASIAL
# ==============================================================================
elif app_mode == "📊 Eksplorasi Pasar & Peta Spasial":
    st.title("📊 Eksplorasi Pasar & Distribusi Spasial Real Estat")
    st.markdown("Analisis interaktif terhadap korpus **22.748 transaksi properti** resmi di King County, Washington.")
    st.markdown("---")

    # Ringkasan KPI Pasar
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Properti Teranalisis", f"{len(clean_df):,} unit")
    k2.metric("Median Harga Transaksi", f"${clean_df['SalePrice'].median():,.0f}")
    k3.metric("Rata-rata Harga / SqFt", f"${clean_df['PricePerSqFt'].median():,.0f} / sqft")
    k4.metric("Median Luas Hunian", f"{clean_df['SqFtTotLiving'].median():,.0f} sqft")

    st.markdown("---")
    
    # Filter Interaktif
    f1, f2, f3 = st.columns(3)
    with f1:
        tier_filter = st.multiselect(
            "Filter Segmen Pasar:", 
            options=['Entry-Level', 'Mid-Market', 'Luxury'],
            default=['Entry-Level', 'Mid-Market', 'Luxury']
        )
    with f2:
        price_range = st.slider(
            "Rentang Harga Jual ($):",
            min_value=50000, max_value=3000000,
            value=(100000, 1500000), step=50000
        )
    with f3:
        waterfront_only = st.checkbox("Hanya Tampilkan Properti Tepi Air (Waterfront)", value=False)

    filtered_df = clean_df[
        (clean_df['PropertyTier'].isin(tier_filter)) &
        (clean_df['SalePrice'] >= price_range[0]) &
        (clean_df['SalePrice'] <= price_range[1])
    ]
    if waterfront_only:
        filtered_df = filtered_df[filtered_df['IsWaterfront'] == 1]

    st.markdown(f"*Menampilkan {len(filtered_df):,} properti yang sesuai filter.*")

    # Visualisasi Peta Spasial
    st.subheader("🗺️ Peta Sebaran Spasial Properti King County (Latitude vs Longitude)")
    sample_map = filtered_df.sample(min(3000, len(filtered_df)), random_state=42)
    
    fig_map = px.scatter(
        sample_map,
        x="Longitude",
        y="Latitude",
        color="SalePrice",
        size="SqFtTotLiving",
        hover_data=["ZipCode", "BldgGrade", "Bedrooms", "TotalBaths"],
        color_continuous_scale="Viridis",
        title="Distribusi Spasial Titik Lokasi Properti & Gradasi Harga (Sample 3,000 Transaksi)"
    )
    fig_map.update_layout(height=550)
    st.plotly_chart(fig_map, use_container_width=True)

    # Distribusi Harga
    st.subheader("📈 Distribusi Harga Properti Berdasarkan Segmen Pasar")
    fig_box = px.box(
        filtered_df,
        x="PropertyTier",
        y="SalePrice",
        color="PropertyTier",
        title="Sebaran Harga Transaksi per Tier Segmen Properti",
        points=False
    )
    st.plotly_chart(fig_box, use_container_width=True)

# ==============================================================================
# MODUL 3: ANALISIS BOBOT FITUR (XAI)
# ==============================================================================
elif app_mode == "🔍 Analisis Bobot Fitur (XAI)":
    st.title("🔍 Transparansi Model: Analisis Bobot Fitur (*Explainable AI*)")
    st.markdown(
        "Pendekatan *Explainable AI* (XAI) menggunakan **Permutation Feature Importance** untuk mengukur "
        "seberapa besar setiap atribut memengaruhi akurasi estimasi harga model Machine Learning."
    )
    st.markdown("---")

    ranked = metadata['feature_importance_ranked']
    imp_df = pd.DataFrame(ranked, columns=["Fitur Prediktor", "Importance Score (R2 Drop)"])

    c1, c2 = st.columns([1.5, 1])
    with c1:
        st.subheader("Peringkat Kepentingan Fitur Penentu Harga")
        fig_imp = px.bar(
            imp_df.head(10).iloc[::-1],
            x="Importance Score (R2 Drop)",
            y="Fitur Prediktor",
            orientation="h",
            color="Importance Score (R2 Drop)",
            color_continuous_scale="Teal",
            title="10 Fitur Paling Berpengaruh dalam Model AVM"
        )
        fig_imp.update_layout(height=450)
        st.plotly_chart(fig_imp, use_container_width=True)

    with c2:
        st.subheader("💡 Tiga Pilar Penentu Valuasi Real Estat")
        st.markdown("""
        1. **Faktor Spasial (*Latitude & Longitude*):**  
           Menempati bobot kepentingan tertinggi. Properti di sebelah utara (dekat danau, pusat teknologi Bellevue/Redmond, dan Seattle Utara) menikmati premi lokasi yang sangat masif dibandingkan wilayah pinggiran selatan.
        2. **Dimensi Hunian (*SqFtTotLiving*):**  
           Luas bangunan riil merupakan determinan fisik nomor satu. Setiap penambahan 100 sqft luas hunian secara stabil mendongkrak valuasi properti.
        3. **Mutu Pengerjaan (*BldgGrade*):**  
           Material konstruksi, arsitektur, dan *finishing* (skala 1–13 dari penilai pajak) memberikan lonjakan nilai non-linear yang tajam pada segmen menengah ke atas.
        """)

# ==============================================================================
# MODUL 4: SIMULATOR ROI RENOVASI
# ==============================================================================
elif app_mode == "🔨 Simulator ROI Renovasi":
    st.title("🔨 Simulator Nilai Tambah & ROI Renovasi Properti")
    st.markdown(
        "Bagi pemilik rumah atau investor (*flippers*), simulator ini memproyeksikan potensi kenaikan harga jual "
        "jika properti ditingkatkan kualitas bangunannya (*BldgGrade*) dan kondisinya (*Condition*)."
    )
    st.markdown("---")

    col_base, col_reno = st.columns(2)
    with col_base:
        st.subheader("Status Rumah Saat Ini (Sebelum Renovasi)")
        b_grade = st.slider("Grade Saat Ini", 4, 11, 7, key="b_grade")
        b_cond = st.slider("Kondisi Saat Ini", 1, 5, 3, key="b_cond")
        b_sqft = st.number_input("Luas Hunian (SqFt)", value=1800, step=100, key="b_sqft")
        b_zip = st.selectbox("Wilayah Kode Pos", all_zipcodes, index=all_zipcodes.index("98108") if "98108" in all_zipcodes else 0, key="b_zip")
        b_cost = st.number_input("Estimasi Biaya Anggaran Renovasi ($)", value=45000, step=5000, key="b_cost")

    with col_reno:
        st.subheader("Target Peningkatan Setelah Renovasi")
        t_grade = st.slider("Target Grade Baru", 4, 12, max(b_grade, 8), key="t_grade")
        t_cond = st.slider("Target Kondisi Baru", 1, 5, 5, key="t_cond")
        t_add_sqft = st.number_input("Tambahan Luas Bangunan (SqFt)", value=0, step=50, key="t_add_sqft")

    btn_sim = st.button("Hitung Proyeksi Keuntungan Renovasi", use_container_width=True)

    if btn_sim:
        lat = zip_coords.get(b_zip, {}).get("Latitude", 47.5614)
        lon = zip_coords.get(b_zip, {}).get("Longitude", -122.3094)
        
        # Kondisi Sebelum
        row_before = pd.DataFrame([{
            'SqFtTotLiving': b_sqft, 'SqFtLot': 6000, 'Bedrooms': 3, 'TotalBaths': 2.0, 'Stories': 1.0,
            'SqFtTotBasement': 0, 'SqFtGarageAttached': 300, 'BldgGrade': b_grade, 'Condition': b_cond,
            'PropertyAge': 35, 'IsRenovated': 0, 'Latitude': lat, 'Longitude': lon,
            'IsWaterfront': 0, 'HasView': 0, 'TrafficNoise': 0, 'AirportNoise': 0, 'salesYear': 2015
        }])[metadata['features']]

        # Kondisi Sesudah
        row_after = pd.DataFrame([{
            'SqFtTotLiving': b_sqft + t_add_sqft, 'SqFtLot': 6000, 'Bedrooms': 3, 'TotalBaths': 2.5, 'Stories': 1.0,
            'SqFtTotBasement': 0, 'SqFtGarageAttached': 300, 'BldgGrade': t_grade, 'Condition': t_cond,
            'PropertyAge': 35, 'IsRenovated': 1, 'Latitude': lat, 'Longitude': lon,
            'IsWaterfront': 0, 'HasView': 0, 'TrafficNoise': 0, 'AirportNoise': 0, 'salesYear': 2015
        }])[metadata['features']]

        price_before = np.exp(reg_model.predict(row_before)[0])
        price_after = np.exp(reg_model.predict(row_after)[0])
        gain = price_after - price_before
        net_profit = gain - b_cost
        roi = (net_profit / b_cost) * 100 if b_cost > 0 else 0

        st.markdown("---")
        res1, res2, res3, res4 = st.columns(4)
        res1.metric("Harga Sebelum Renovasi", f"${price_before:,.0f}")
        res2.metric("Harga Setelah Renovasi", f"${price_after:,.0f}", delta=f"+${gain:,.0f}")
        res3.metric("Laba Bersih (*Net Profit*)", f"${net_profit:,.0f}", delta=f"${net_profit:,.0f}")
        res4.metric("Proyeksi ROI", f"{roi:.1f}%")

        if net_profit > 0:
            st.success(f"🎉 **Rencana Renovasi Layak Eksekusi!** Estimasi penambahan ekuitas properti sebesar **${gain:,.0f}**, menghasilkan keuntungan bersih **${net_profit:,.0f}** di atas anggaran renovasi.")
        else:
            st.warning("⚠️ Biaya renovasi lebih tinggi daripada estimasi kenaikan nilai pasar properti. Disarankan mengoptimalkan efisiensi anggaran.")

# ==============================================================================
# MODUL 5: METODOLOGI & EVALUASI MODEL
# ==============================================================================
elif app_mode == "ℹ️ Metodologi & Evaluasi Model":
    st.title("ℹ️ Metodologi Sains Data & Evaluasi Model")
    st.markdown("Dokumentasi teknis arsitektur machine learning, evaluasi benchmark performa, dan landasan data.")
    st.markdown("---")

    st.subheader("📊 Tabel Perbandingan Kinerja Algoritma (Scorecard)")
    scorecard = [
        {"Algoritma": "OLS Linear Regression", "R2 (Log)": 0.7460, "RMSE (Log)": 0.2860, "MAPE": "22.04%", "MAE": "$124,551"},
        {"Algoritma": "Ridge Regression (L2)", "R2 (Log)": 0.7460, "RMSE (Log)": 0.2859, "MAPE": "22.01%", "MAE": "$124,387"},
        {"Algoritma": "Random Forest Regressor", "R2 (Log)": 0.8659, "RMSE (Log)": 0.2078, "MAPE": "14.33%", "MAE": "$79,623"},
        {"Algoritma": "HistGradientBoosting Regressor", "R2 (Log)": "0.8848 (Terbaik)", "RMSE (Log)": 0.1926, "MAPE": "13.39%", "MAE": "$72,329"}
    ]
    st.table(pd.DataFrame(scorecard))

    st.subheader("📚 Pustaka Acuan & Sumber Data")
    st.markdown("""
    - **Dataset Primer:** King County Department of Assessments & University of Washington (*Harvard Dataverse*).
    - **Metodologi:** CRISP-DM (*Cross-Industry Standard Process for Data Mining*) & Hedonic Pricing Econometrics.
    - **Teknologi:** Python 3.12, Scikit-Learn 1.4, Streamlit, Plotly, Joblib, Pandas, NumPy.
    """)
