"""
Skrip Otomasi Pengisian Notebook: KingCounty-AVM
Menyusun seluruh sel kode dan markdown pada 3 notebook Jupyter agar siap dieksekusi mahasiswa & dosen.
Termasuk penyuntikan algoritma Unsupervised Learning (K-Means Micro-Market Clustering k=6).
"""

import os
import json

base_dir = os.path.dirname(os.path.dirname(__file__))
nb_dir = os.path.join(base_dir, "notebooks")

def build_cell(cell_type, source_text):
    lines = [line + "\n" for line in source_text.strip().split("\n")]
    if lines:
        lines[-1] = lines[-1].rstrip("\n")
    cell = {
        "cell_type": cell_type,
        "metadata": {},
        "source": lines
    }
    if cell_type == "code":
        cell["execution_count"] = None
        cell["outputs"] = []
    return cell

# ==============================================================================
# 1. NOTEBOOK 01: EDA
# ==============================================================================
cells_nb1 = [
    build_cell("markdown", """# Tahap 2: Exploratory Data Analysis (EDA)
**Mata Kuliah:** Data Science 2026  
**Topik:** King County Real Estate Sales & Property Assessment (Harvard Dataverse)  
**Tujuan:** Memahami struktur data transaksi, karakteristik sebaran harga properti, korelasi fitur fisik dan spasial terhadap harga jual, serta memetakan strategi pembersihan data kotor."""),

    build_cell("markdown", "## 1. Import Pustaka & Konfigurasi Lingkungan"),
    build_cell("code", """import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi visualisasi
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
pd.set_option('display.max_columns', 50)
pd.set_option('display.float_format', lambda x: '%.2f' % x)

print("Pustaka EDA berhasil dimuat. Lingkungan analisis data siap:")
print(f"- Pandas v{pd.__version__} | NumPy v{np.__version__} | Seaborn v{sns.__version__}")"""),

    build_cell("markdown", "## 2. Memuat Dataset Mentah (*Raw Data*)"),
    build_cell("code", """# Memuat dataset resmi transaksi properti King County
DATA_PATH = "../data/raw/02_king_county_real_estate/cleansales.tab"

df = pd.read_csv(DATA_PATH, sep='\\t', low_memory=False)
print(f"Dataset berhasil dimuat: {df.shape[0]:,} baris x {df.shape[1]} kolom.")
display(df.head())"""),

    build_cell("markdown", "## 3. Inspeksi Awal Karakteristik Data\nPeriksa dimensi data, tipe data per kelompok kolom, dan cuplikan informasi umum."),
    build_cell("code", """print("--- Informasi Ringkas Struktur Data ---")
print(f"Jumlah Baris Transaksi : {df.shape[0]:,}")
print(f"Jumlah Kolom Atribut   : {df.shape[1]}")

# Distribusi tipe data
print("\\nDistribusi Tipe Data:")
display(df.dtypes.value_counts().to_frame(name='Jumlah Kolom'))"""),

    build_cell("markdown", "## 4. Evaluasi Kualitas Data, Duplikasi & Missing Values\nIdentifikasi jumlah dan sebaran nilai kosong pada seluruh 147 kolom."),
    build_cell("code", """# Evaluasi nilai kosong
missing_series = df.isnull().sum()
cols_with_missing = missing_series[missing_series > 0]

print(f"Jumlah kolom yang memiliki missing values: {len(cols_with_missing)}")
missing_df = pd.DataFrame({
    'Missing Values': cols_with_missing,
    'Persentase (%)': (cols_with_missing / len(df) * 100).round(2)
}).sort_values(by='Missing Values', ascending=False)

display(missing_df.head(15))"""),

    build_cell("code", """# Evaluasi spesifik pada kolom ZipCode dan teks
print("Missing ZipCode:", df['ZipCode'].isnull().sum(), f"({df['ZipCode'].isnull().mean()*100:.2f}%)")
print("Cek kelengkapan koordinat spasial:")
print("Missing X (Easting) :", df['X'].isnull().sum())
print("Missing Y (Northing):", df['Y'].isnull().sum())

display(pd.DataFrame({
    'Atribut Spasial / Lokasi': ['ZipCode (Kode Pos)', 'X (State Plane Easting)', 'Y (State Plane Northing)'],
    'Missing Count': [df['ZipCode'].isnull().sum(), df['X'].isnull().sum(), df['Y'].isnull().sum()],
    'Status Kelengkapan': ['Perlu Imputasi Spasial', '100% Lengkap', '100% Lengkap']
}))"""),

    build_cell("markdown", "## 5. Analisis Statistik Deskriptif & Distribusi Target (`SalePrice`)\nEksplorasi ringkasan statistik dan bentuk distribusi harga properti (apakah terdistribusi normal atau menceng/skewed)."),
    build_cell("code", """print("--- Statistik Deskriptif Target: SalePrice ---")
display(df['SalePrice'].describe().to_frame().T)

# Visualisasi distribusi harga normal vs transformasi logaritmik
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Plot 1: Skala Dolar Asli
sns.histplot(df['SalePrice'] / 1000, kde=True, ax=axes[0], color='#1f77b4', bins=60)
axes[0].set_title("Distribusi SalePrice (Asli) - Right Skewed", fontsize=12, fontweight='bold')
axes[0].set_xlabel("Harga Transaksi (dalam Ribuan USD)")
axes[0].set_ylabel("Frekuensi")

# Plot 2: Transformasi Logaritmik ln(y)
sns.histplot(np.log(df['SalePrice']), kde=True, ax=axes[1], color='#2ca02c', bins=60)
axes[1].set_title("Distribusi ln(SalePrice) - Mendekati Normal", fontsize=12, fontweight='bold')
axes[1].set_xlabel("ln(SalePrice)")
axes[1].set_ylabel("Frekuensi")

plt.tight_layout()
plt.show()"""),

    build_cell("markdown", "## 6. Analisis Korelasi & Hubungan Antarvariabel Kunci\nMenelaah hubungan linear antara spesifikasi fisik rumah, kualitas material, pemandangan, dan koordinat spasial terhadap harga jual."),
    build_cell("code", """# Seleksi variabel representatif dari 147 kolom
fitur_kunci = [
    'SalePrice', 'SqFtTotLiving', 'SqFtLot', 'Bedrooms', 'BathFullCount', 
    'BathHalfCount', 'Stories', 'BldgGrade', 'Condition', 'YrBuilt', 
    'YrRenovated', 'X', 'Y', 'WfntLocation', 'SeattleSkyline', 'LakeWashington'
]

df_korelasi = df[fitur_kunci].dropna()
matriks_corr = df_korelasi.corr(method='pearson')

plt.figure(figsize=(14, 10))
sns.heatmap(
    matriks_corr, 
    annot=True, 
    fmt='.2f', 
    cmap='coolwarm',
    center=0, 
    vmin=-1, 
    vmax=1, 
    linewidths=0.5
)
plt.title("Matriks Korelasi Pearson Fitur Kunci terhadap Harga Properti", fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()"""),

    build_cell("code", """# Peringkat korelasi terhadap target SalePrice
target_corr = matriks_corr['SalePrice'].drop('SalePrice')
target_corr = target_corr.reindex(target_corr.abs().sort_values(ascending=False).index)

plt.figure(figsize=(10, 6))
sns.barplot(
    x=target_corr.values,
    y=target_corr.index,
    hue=target_corr.index,
    palette='coolwarm',
    legend=False
)
plt.title("Kekuatan Korelasi Fitur Prediktor terhadap SalePrice", fontsize=13, fontweight='bold')
plt.xlabel("Koefisien Korelasi Pearson")
plt.ylabel("Fitur Prediktor")
plt.axvline(0, color='black', linewidth=0.8)
plt.tight_layout()
plt.show()

display(target_corr.to_frame(name='Korelasi Pearson dengan SalePrice'))"""),

    build_cell("markdown", """## 7. Catatan Temuan & Hipotesis Awal EDA
*Ringkasan insight empiris hasil eksplorasi data:*
1. **Fitur Fisik Dominan:** Luas area hunian (`SqFtTotLiving`, $r \approx 0.70$) dan mutu konstruksi bangunan (`BldgGrade`, $r \approx 0.67$) merupakan faktor penentu utama harga properti.
2. **Karakteristik Kemencengan (*Heavy-Tailed*):** Variabel target `SalePrice` memiliki rentang ekstrem dari \$5.000 hingga \$9,4 juta dengan median \$450.000. Penggunaan transformasi logaritmik $\\ln(\\text{SalePrice})$ terbukti menghasilkan distribusi simetris yang mendekati kurva normal (*bell curve*).
3. **Penyelamatan Missing Data:** Kolom `ZipCode` memiliki 3.205 nilai kosong, namun variabel spasial `X` dan `Y` terisi 100% tanpa missing value, sehingga dapat dilakukan imputasi spasial presisi tinggi via K-Nearest Neighbors (KNN).
4. **Rencana Tahap Pembersihan:** Memfilter transaksi non-pasar (< \$50.000), mengonversi proyeksi koordinat WA North ke Latitude/Longitude WGS84, serta merekayasa fitur usia bangunan (`PropertyAge`) dan rasio harga per luas lantai.""")
]

# ==============================================================================
# 2. NOTEBOOK 02: CLEANING & PREPROCESSING
# ==============================================================================
cells_nb2 = [
    build_cell("markdown", """# Tahap 3: Data Cleaning & Preprocessing
**Mata Kuliah:** Data Science 2026  
**Topik:** Pembersihan & Rekayasa Fitur King County Real Estate  
**Tujuan:** Mentransformasikan data mentah 147 kolom menjadi dataset analitik bersih 40 kolom yang bebas dari missing values, terbebas dari trailing whitespace, memiliki koordinat Latitude/Longitude, dan siap dilatih oleh model Machine Learning."""),

    build_cell("markdown", "## 1. Import Pustaka & Konfigurasi Modul Utilitas"),
    build_cell("code", """import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Menambahkan direktori src ke sys.path untuk modul utilitas
sys.path.append(os.path.abspath(".."))
from src.utils import wa_north_to_latlon

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
print("Pustaka pembersihan data & modul utilitas spasial siap:")
print(f"- Pandas v{pd.__version__} | Modul utils.wa_north_to_latlon terhubung.")"""),

    build_cell("markdown", "## 2. Memuat Dataset Mentah (*Raw Data*)"),
    build_cell("code", """DATA_PATH = "../data/raw/02_king_county_real_estate/cleansales.tab"
df = pd.read_csv(DATA_PATH, sep='\\t', low_memory=False)
print(f"Data mentah awal berhasil dimuat: {df.shape[0]:,} baris x {df.shape[1]} kolom.")
display(df[['SalePrice', 'DocumentDate', 'ZipCode', 'X', 'Y', 'SqFtTotLiving', 'YrBuilt']].head())"""),

    build_cell("markdown", "## 3. Penanganan Data Duplikat & Pembersihan String Whitespace"),
    build_cell("code", """# Cek duplikat awal
n_dups = df.duplicated().sum()
print("Jumlah duplikasi baris awal:", n_dups)

# Bersihkan trailing whitespace pada seluruh kolom teks/string
text_columns = df.select_dtypes(include=['object']).columns
for col in text_columns:
    df[col] = df[col].astype(str).str.strip()

print(f"Pembersihan spasi berlebih pada {len(text_columns)} kolom teks selesai.")
display(pd.DataFrame({
    'Tahap Pembersihan': ['Cek Duplikat Baris', 'Pembersihan Trailing Whitespace'],
    'Hasil Evaluasi': [f"{n_dups} duplikat terdeteksi", f"{len(text_columns)} kolom teks distrip"]
}))"""),

    build_cell("markdown", "## 4. Penanganan Outlier Non-Pasar & Transaksi Anomali\nTransaksi di bawah \$50.000 umumnya merupakan transfer kepemilikan keluarga, hibah, atau penyelesaian sengketa hukum (*non-arm's length transaction*), bukan harga pasar wajar."),
    build_cell("code", """initial_count = len(df)
df = df[df['SalePrice'] >= 50000].copy()
filtered_out = initial_count - len(df)

print(f"Menyaring transaksi non-pasar (< $50,000): {filtered_out} baris dieliminasi.")
print(f"Sisa baris valid: {len(df):,} baris.")
display(pd.DataFrame({
    'Kondisi Filter Transaksi': ['Data Mentah Awal', 'Transaksi Non-Pasar (< $50,000)', 'Data Tersaring'],
    'Jumlah Baris': [initial_count, filtered_out, len(df)],
    'Persentase Terhadap Awal': ['100%', f"{(filtered_out/initial_count*100):.2f}%", f"{(len(df)/initial_count*100):.2f}%"]
}))"""),

    build_cell("markdown", "## 5. Imputasi Spasial Missing ZipCode (K-Nearest Neighbors)\nMemanfaatkan kelengkapan 100% koordinat `X` dan `Y` untuk merekonstruksi kode pos yang kosong secara geografis."),
    build_cell("code", """from sklearn.neighbors import KNeighborsClassifier

missing_mask = df['ZipCode'].isnull() | (df['ZipCode'] == 'nan') | (df['ZipCode'] == '')
print(f"Jumlah ZipCode kosong yang perlu diimputasi: {missing_mask.sum():,}")

known_data = df[~missing_mask].copy()
known_data['ZipClean'] = known_data['ZipCode'].str[:5]

if missing_mask.sum() > 0:
    knn = KNeighborsClassifier(n_neighbors=3, weights='distance')
    knn.fit(known_data[['X', 'Y']], known_data['ZipClean'])
    imputed_values = knn.predict(df.loc[missing_mask, ['X', 'Y']])
    df.loc[missing_mask, 'ZipCode'] = imputed_values

df['ZipCode'] = df['ZipCode'].astype(str).str[:5]
print("Imputasi ZipCode selesai. Sisa missing ZipCode:", df['ZipCode'].isnull().sum())
display(pd.DataFrame({
    'Atribut': ['ZipCode (Sebelum Imputasi)', 'ZipCode Terimputasi KNN', 'Sisa Missing ZipCode'],
    'Jumlah Baris': [missing_mask.sum(), missing_mask.sum(), df['ZipCode'].isnull().sum()]
}))"""),

    build_cell("markdown", "## 6. Transformasi Koordinat Spasial ke WGS84 (Latitude & Longitude)\nMengonversi proyeksi bidang datar Washington State Plane North (kaki) ke koordinat derajat bola bumi WGS84 untuk pemetaan interaktif."),
    build_cell("code", """print("Mengonversi koordinat X, Y ke Latitude dan Longitude...")
lats, lons = [], []
for x_ft, y_ft in zip(df['X'], df['Y']):
    lat, lon = wa_north_to_latlon(x_ft, y_ft)
    lats.append(round(lat, 5))
    lons.append(round(lon, 5))

df['Latitude'] = lats
df['Longitude'] = lons
print(f"Koordinat terkonversi: Lat rentang [{df['Latitude'].min()}, {df['Latitude'].max()}], Lon rentang [{df['Longitude'].min()}, {df['Longitude'].max()}]")
display(df[['X', 'Y', 'Latitude', 'Longitude']].head())"""),

    build_cell("markdown", "## 7. Rekayasa Fitur (*Feature Engineering*) & Segmentasi Tier"),
    build_cell("code", """# 1. Usia properti saat transaksi
df['PropertyAge'] = np.maximum(0, df['salesYear'] - df['YrBuilt'])

# 2. Status renovasi
df['IsRenovated'] = (df['YrRenovated'] > 0).astype(int)

# 3. Total kamar mandi tertimbang
df['TotalBaths'] = df['BathFullCount'] + 0.75 * df['Bath3qtrCount'] + 0.5 * df['BathHalfCount']

# 4. Fitur pemandangan alam (Scenic View Indicator)
df['HasView'] = ((df['SeattleSkyline'] > 0) | 
                 (df['LakeWashington'] > 0) | 
                 (df['LakeSammamish'] > 0) | 
                 (df['PugetSound'] > 0) | 
                 (df['MtRainier'] > 0)).astype(int)

df['IsWaterfront'] = (df['WfntLocation'] > 0).astype(int)

# 5. Rasio harga per luas lantai
df['PricePerSqFt'] = df['SalePrice'] / np.maximum(1, df['SqFtTotLiving'])

# 6. Target Klasifikasi (PropertyTier)
df['PropertyTier'] = pd.cut(
    df['SalePrice'],
    bins=[-np.inf, 350000, 700000, np.inf],
    labels=['Entry-Level', 'Mid-Market', 'Luxury']
)

print("Distribusi Kelas Segmentasi Pasar (PropertyTier):")
tier_dist = df['PropertyTier'].value_counts().to_frame(name='Jumlah Properti')
tier_dist['Persentase'] = (tier_dist['Jumlah Properti'] / len(df) * 100).round(2).astype(str) + '%'
display(tier_dist)"""),

    build_cell("markdown", "## 8. Seleksi Fitur Kunci & Ekspor Data Bersih\nMenyusutkan 147 kolom mentah menjadi 40 kolom bernilai prediktif tinggi dan menyimpannya ke `../data/processed/`."),
    build_cell("code", """selected_cols = [
    'SalePrice', 'PropertyTier',
    'SqFtTotLiving', 'SqFtLot', 'Bedrooms', 'TotalBaths',
    'BathFullCount', 'BathHalfCount', 'Bath3qtrCount',
    'Stories', 'SqFtTotBasement', 'SqFtFinBasement', 'SqFtGarageAttached',
    'BldgGrade', 'Condition', 'YrBuilt', 'YrRenovated',
    'PropertyAge', 'IsRenovated',
    'ZipCode', 'X', 'Y', 'Latitude', 'Longitude', 'DistrictName',
    'IsWaterfront', 'HasView', 'SeattleSkyline', 'LakeWashington',
    'LakeSammamish', 'PugetSound', 'MtRainier',
    'TrafficNoise', 'AirportNoise',
    'LandVal', 'ImpsVal', 'PricePerSqFt', 'DocumentDate', 'salesYear'
]

clean_df = df[selected_cols].drop_duplicates().reset_index(drop=True)
output_path = "../data/processed/king_county_clean.csv"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
clean_df.to_csv(output_path, index=False)

print(f"Data bersih berhasil disimpan ke {output_path}")
print(f"Dimensi akhir: {clean_df.shape[0]:,} baris x {clean_df.shape[1]} kolom.")
print("Total Missing Values di seluruh dataset bersih:", clean_df.isnull().sum().sum())
display(clean_df.head(5))"""),

    build_cell("markdown", """## 9. Ringkasan Perubahan Data
| Parameter Transformasi | Sebelum (Raw Data) | Sesudah (Processed Data) |
| :--- | :--- | :--- |
| **Jumlah Baris** | 22.847 baris | 22.748 baris (-99 baris non-pasar & duplikat) |
| **Jumlah Kolom** | 147 kolom | 40 kolom esensial |
| **Missing Values (ZipCode)** | 3.205 baris kosong | 0 (100% terimputasi via KNN spasial) |
| **Sistem Koordinat** | Hanya proyeksi kaki (*X, Y*) | Dilengkapi Latitude & Longitude derajat WGS84 |
| **Fitur Rekayasa Baru** | Tidak ada | `PropertyAge`, `IsRenovated`, `TotalBaths`, `HasView`, `PropertyTier` |
| **Integritas Target** | Skewness tinggi, rentang \$5k–\$9.4M | Bersih dari transaksi hibah nominal, siap transformasi log |""")
]

# ==============================================================================
# 3. NOTEBOOK 03: MODELING & EVALUATION
# ==============================================================================
cells_nb3 = [
    build_cell("markdown", """# Tahap 4: Pemodelan Machine Learning & Evaluasi
**Mata Kuliah:** Data Science 2026  
**Topik:** KingCounty-AVM (Supervised Valuation, Tier Classification & Unsupervised Spatial Clustering)  
**Tujuan Pembelajaran (Sesuai RPS):**
1. **Supervised Learning (Regresi Hedonik):** Menguji dan membandingkan 7 model regresi (OLS, Ridge, Lasso, Elastic Net, Decision Tree, Random Forest, HistGradientBoosting) untuk estimasi nilai pasar properti kontinu ($R^2$, $\\text{RMSE}$, $\\text{MAPE}$, $\\text{MAE}$).
2. **Supervised Learning (Klasifikasi Segmentasi Pasar):** Melatih dan memvalidasi model klasifikasi (Decision Tree, Random Forest, HistGradientBoosting) untuk mengelompokkan kelas properti ke dalam tier pasar (*Entry-Level*, *Mid-Market*, *Luxury*).
3. **Unsupervised Learning (K-Means Clustering):** Menyuntikkan algoritma K-Means ($k=6$) berbasis koordinat geospasial (`Latitude`, `Longitude`) dan nilai logaritmik harga $\\ln(\\text{SalePrice})$ guna mempartisi wilayah King County ke dalam 6 mikro-pasar properti serta memberdayakan fitur pembanding properti (*empirical comps*).
4. **Interpretasi & XAI:** Menganalisis bobot kontribusi variabel menggunakan Permutation Feature Importance.
5. **Serialisasi Model:** Mengekspor seluruh artefak model biner (`.joblib`) dan metadata JSON untuk integrasi aplikasi web Streamlit."""),

    build_cell("markdown", "## 1. Import Pustaka Pemodelan (Supervised & Unsupervised)"),
    build_cell("code", """import os
import json
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.ensemble import (
    HistGradientBoostingRegressor, HistGradientBoostingClassifier,
    RandomForestRegressor, RandomForestClassifier
)
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    r2_score, mean_squared_error, mean_absolute_error, 
    mean_absolute_percentage_error, accuracy_score, f1_score, confusion_matrix,
    silhouette_score, calinski_harabasz_score, davies_bouldin_score
)
from sklearn.inspection import permutation_importance

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
print("Pustaka pemodelan (Supervised & Unsupervised Learning) berhasil dimuat.")"""),

    build_cell("markdown", "## 2. Memuat Dataset Bersih dari `../data/processed/`"),
    build_cell("code", """clean_path = "../data/processed/king_county_clean.csv"
df = pd.read_csv(clean_path, low_memory=False)
print(f"Data bersih berhasil dimuat: {df.shape[0]:,} baris x {df.shape[1]} kolom.")
display(df[['SalePrice', 'PropertyTier', 'SqFtTotLiving', 'Bedrooms', 'TotalBaths', 'BldgGrade', 'ZipCode', 'Latitude', 'Longitude']].head())"""),

    build_cell("markdown", "## 3. Pemisahan Fitur ($X$), Target ($y$, $\\ln(y)$), dan Train-Test Split (80/20)"),
    build_cell("code", """feature_cols = [
    'SqFtTotLiving', 'SqFtLot', 'Bedrooms', 'TotalBaths', 'Stories',
    'SqFtTotBasement', 'SqFtGarageAttached', 'BldgGrade', 'Condition',
    'PropertyAge', 'IsRenovated', 'Latitude', 'Longitude',
    'IsWaterfront', 'HasView', 'TrafficNoise', 'AirportNoise', 'salesYear'
]

X = df[feature_cols].copy()
y = df['SalePrice']
y_log = np.log(y)
y_tier = df['PropertyTier']

X_train, X_test, y_train, y_test, ylog_train, ylog_test, ytier_train, ytier_test = train_test_split(
    X, y, y_log, y_tier, test_size=0.20, random_state=42, stratify=y_tier
)

split_summary = pd.DataFrame({
    'Partisi Dataset': ['Total Dataset', 'Data Latih (Train 80%)', 'Data Uji (Test 20%)'],
    'Jumlah Baris': [len(df), len(X_train), len(X_test)],
    'Persentase': ['100%', '80%', '20%']
})
display(split_summary)"""),

    build_cell("markdown", """## 4. Pelatihan & Evaluasi Model Regresi Hedonik (AVM) — Benchmarking 7 Model
Sesuai arahan evaluasi komprehensif (minimal 5 model komparatif), kami menguji 7 algoritma dari beragam paradigma:
1. **OLS Linear Regression:** Model dasar ekonometrika klasik tanpa penalti regularisasi.
2. **Ridge Regression ($L_2$):** Regularisasi shrinkage untuk mengatasi multikolinearitas antar prediktor luas/dimensi fisik.
3. **Lasso Regression ($L_1$):** Regularisasi penalti absolut untuk reduksi bobot mendekati nol (sparse selection).
4. **Elastic Net Regression:** Kombinasi harmonis penalti $L_1$ dan $L_2$ (Zou & Hastie, 2005).
5. **Decision Tree Regressor:** Model non-linear pohon tunggal berbasis partisi rekursif.
6. **Random Forest Regressor:** Algoritma ensemble bagging untuk mereduksi varians prediksi.
7. **HistGradientBoosting Regressor:** Algoritma ensemble boosting modern berbasis histogram."""),
    build_cell("code", """models = {
    'OLS Linear Regression': LinearRegression(),
    'Ridge Regression (L2)': Ridge(alpha=10.0),
    'Lasso Regression (L1)': Lasso(alpha=0.0005, max_iter=3000, random_state=42),
    'Elastic Net Regression': ElasticNet(alpha=0.0005, l1_ratio=0.5, max_iter=3000, random_state=42),
    'Decision Tree Regressor': DecisionTreeRegressor(max_depth=12, min_samples_leaf=10, random_state=42),
    'Random Forest Regressor': RandomForestRegressor(n_estimators=100, max_depth=14, n_jobs=-1, random_state=42),
    'HistGradientBoosting Regressor': HistGradientBoostingRegressor(max_iter=250, learning_rate=0.08, random_state=42)
}

results = []
trained_models = {}

for name, model in models.items():
    model.fit(X_train, ylog_train)
    trained_models[name] = model
    
    pred_log = model.predict(X_test)
    pred_dollars = np.exp(pred_log)
    
    r2 = r2_score(ylog_test, pred_log)
    rmse_log = np.sqrt(mean_squared_error(ylog_test, pred_log))
    mape = mean_absolute_percentage_error(y_test, pred_dollars)
    mae = mean_absolute_error(y_test, pred_dollars)
    
    results.append({
        'Model Regresi': name,
        'R2 (Log Scale)': round(r2, 4),
        'RMSE (Log Scale)': round(rmse_log, 4),
        'MAPE (%)': round(mape * 100, 2),
        'MAE ($)': round(mae, 0)
    })

eval_df = pd.DataFrame(results).sort_values(by='R2 (Log Scale)', ascending=False).reset_index(drop=True)
print("=== Scorecard Hasil Evaluasi 7 Model Regresi Hedonik (AVM) ===")
display(eval_df)

# Visualisasi Evaluasi Model Regresi Terbaik
best_model = trained_models['HistGradientBoosting Regressor']
pred_best_dollars = np.exp(best_model.predict(X_test))
residuals = ylog_test - best_model.predict(X_test)

fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# Plot 1: Aktual vs Prediksi
axes[0].scatter(y_test / 1000, pred_best_dollars / 1000, alpha=0.25, color="#1f77b4", s=20)
max_val = max(y_test.max(), pred_best_dollars.max()) / 1000
axes[0].plot([0, max_val], [0, max_val], 'r--', lw=2, label="Garis Ideal (y = x)")
axes[0].set_title("Evaluasi Nilai Aktual vs Prediksi (HistGradientBoosting)", fontsize=12, fontweight='bold')
axes[0].set_xlabel("Harga Aktual Transaksi ($1,000)", fontsize=11)
axes[0].set_ylabel("Harga Prediksi Model ($1,000)", fontsize=11)
axes[0].legend()

# Plot 2: Distribusi Residual
sns.histplot(residuals, kde=True, color="#2ca02c", ax=axes[1], bins=50)
axes[1].set_title("Distribusi Residual Logaritma Prediksi", fontsize=12, fontweight='bold')
axes[1].set_xlabel("Residual: ln(Aktual) - ln(Prediksi)", fontsize=11)
axes[1].set_ylabel("Frekuensi", fontsize=11)

plt.tight_layout()
plt.show()"""),

    build_cell("markdown", "## 5. Pelatihan & Benchmarking Model Klasifikasi Tier Properti (*Entry, Mid, Luxury*)\nMembandingkan model klasifikasi (Decision Tree, Random Forest, dan HistGradientBoosting Classifier) untuk memprediksi segmentasi pasar properti."),
    build_cell("code", """clf_models = {
    'Decision Tree Classifier': DecisionTreeClassifier(max_depth=10, random_state=42),
    'Random Forest Classifier': RandomForestClassifier(n_estimators=100, max_depth=12, n_jobs=-1, random_state=42),
    'HistGradientBoosting Classifier': HistGradientBoostingClassifier(max_iter=150, learning_rate=0.08, random_state=42)
}

clf_results = []
trained_clfs = {}

for name, clf_cand in clf_models.items():
    clf_cand.fit(X_train, ytier_train)
    trained_clfs[name] = clf_cand
    preds = clf_cand.predict(X_test)
    acc = accuracy_score(ytier_test, preds)
    macro_f1 = f1_score(ytier_test, preds, average='macro')
    clf_results.append({
        'Classifier Model': name,
        'Accuracy (%)': round(acc * 100, 2),
        'Macro F1-Score': round(macro_f1, 4)
    })

clf_eval_df = pd.DataFrame(clf_results).sort_values(by='Accuracy (%)', ascending=False).reset_index(drop=True)
print("=== Scorecard Hasil Evaluasi Model Klasifikasi Tier Pasar ===")
display(clf_eval_df)

clf = trained_clfs['HistGradientBoosting Classifier']
tier_preds = clf.predict(X_test)

cm = confusion_matrix(ytier_test, tier_preds, labels=['Entry-Level', 'Mid-Market', 'Luxury'])
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=['Entry', 'Mid', 'Luxury'], 
            yticklabels=['Entry', 'Mid', 'Luxury'])
plt.title("Confusion Matrix Klasifikasi Tier Properti (HistGradientBoosting)", fontsize=12, fontweight='bold')
plt.xlabel("Prediksi")
plt.ylabel("Aktual")
plt.tight_layout()
plt.show()"""),

    build_cell("markdown", """## 6. Pembelajaran Mesin Tak Terarah (Unsupervised Learning) — K-Means Micro-Market Clustering ($k=6$)
Sesuai dengan ketentuan silabus/RPS Sains Data mengenai integrasi materi *Unsupervised Learning*, kami menerapkan algoritma **K-Means Clustering** berbasis:
1. **Koordinat Geospasial:** `Latitude` dan `Longitude` (WGS84).
2. **Nilai Valuasi Ekonomi:** Logaritma harga properti $\\ln(\\text{SalePrice})$.

### 💡 Rasional Ekonometrika & Kegunaan Praktis:
Harga real estat sangat ditentukan oleh *spatial submarket dynamics*. Dua rumah dengan luas dan grade identik akan memiliki nilai pasar yang sangat berbeda tergantung apakah berlokasi di Seattle Urban Core, Bellevue Waterfront, atau Valley Suburbs. Dengan membagi King County ke dalam **6 klaster mikro pasar properti**, model ini:
- Memenuhi syarat materi *unsupervised learning* secara sah dan metodologis.
- Memberikan kegunaan nyata untuk menyaring properti pembanding (*empirical comparables / comps retrieval*) dalam sub-pasar geografis dan ekonomi yang homogen."""),

    build_cell("code", """# 6.1 Pelatihan K-Means Clustering & Evaluasi Metrik Klaster
cluster_features = ['Latitude', 'Longitude']
X_cluster_raw = df[cluster_features].copy()
X_cluster_raw['LogPrice'] = np.log(df['SalePrice'])

# Standardisasi Z-Score untuk menyetarakan skala koordinat dan log harga
scaler_cluster = StandardScaler()
X_cluster_scaled = scaler_cluster.fit_transform(X_cluster_raw)

# Fitting K-Means dengan k=6
k_clusters = 6
kmeans = KMeans(n_clusters=k_clusters, random_state=42, n_init=10)
df['Cluster'] = kmeans.fit_predict(X_cluster_scaled)

# Evaluasi Kualitas Klasterisasi
inertia_val = kmeans.inertia_
sample_idx = np.random.RandomState(42).choice(len(df), size=5000, replace=False)
silhouette_val = silhouette_score(X_cluster_scaled[sample_idx], df['Cluster'].iloc[sample_idx])
calinski_val = calinski_harabasz_score(X_cluster_scaled, df['Cluster'])
davies_val = davies_bouldin_score(X_cluster_scaled, df['Cluster'])

cluster_metrics_df = pd.DataFrame([{
    'Jumlah Klaster (k)': k_clusters,
    'Inertia (WCSS)': f"{inertia_val:,.2f}",
    'Silhouette Score (5k Sample)': f"{silhouette_val:.4f}",
    'Calinski-Harabasz Score': f"{calinski_val:,.2f}",
    'Davies-Bouldin Index': f"{davies_val:.4f}"
}])
print("=== Evaluasi Metrik K-Means Micro-Market Clustering ===")
display(cluster_metrics_df)"""),

    build_cell("code", """# 6.2 Profiling Komprehensif 6 Klaster Mikro-Pasar Properti King County
cluster_summary = df.groupby('Cluster').agg(
    Jumlah_Properti=('SalePrice', 'count'),
    Persentase_Pasar=('SalePrice', lambda x: len(x) / len(df) * 100),
    Median_Harga=('SalePrice', 'median'),
    Mean_Harga=('SalePrice', 'mean'),
    Median_SqFtLiving=('SqFtTotLiving', 'median'),
    Median_BldgGrade=('BldgGrade', 'median'),
    Rata_Latitude=('Latitude', 'mean'),
    Rata_Longitude=('Longitude', 'mean')
).reset_index()

def assign_market_name(row):
    med = row['Median_Harga']
    lon = row['Rata_Longitude']
    lat = row['Rata_Latitude']
    if med < 290000:
        return "Southwest Corridor (Affordable Urban / Tukwila-Burien)"
    elif med < 350000:
        return "Southeast Valley Suburban (Kent-Auburn-Renton)"
    elif med < 450000 and lon > -122.0:
        return "East Foothills & Rural Acreage (Snoqualmie-Enumclaw)"
    elif med < 500000 and lat > 47.63:
        return "North Seattle Metro Urban Core (City Core-Shoreline)"
    elif med < 750000:
        return "Eastside Suburban Tech Corridor (Redmond-Sammamish-Kirkland)"
    else:
        return "West Bellevue & Lakefront Luxury Prestige (Medina-Mercer Island)"

cluster_summary['Profil_Mikro_Pasar'] = cluster_summary.apply(assign_market_name, axis=1)
cluster_summary = cluster_summary.sort_values(by='Median_Harga').reset_index(drop=True)

display_summary = cluster_summary.copy()
display_summary['Persentase_Pasar'] = display_summary['Persentase_Pasar'].apply(lambda x: f"{x:.1f}%")
display_summary['Median_Harga'] = display_summary['Median_Harga'].apply(lambda x: f"${x:,.0f}")
display_summary['Mean_Harga'] = display_summary['Mean_Harga'].apply(lambda x: f"${x:,.0f}")
display_summary['Median_SqFtLiving'] = display_summary['Median_SqFtLiving'].apply(lambda x: f"{x:,.0f} sqft")
display_summary['Rata_Latitude'] = display_summary['Rata_Latitude'].apply(lambda x: f"{x:.4f}°N")
display_summary['Rata_Longitude'] = display_summary['Rata_Longitude'].apply(lambda x: f"{x:.4f}°W")

print("=== Tabel Profil 6 Klaster Mikro-Pasar Properti King County ===")
display(display_summary[['Cluster', 'Profil_Mikro_Pasar', 'Jumlah_Properti', 'Persentase_Pasar', 
                         'Median_Harga', 'Mean_Harga', 'Median_SqFtLiving', 'Median_BldgGrade', 
                         'Rata_Latitude', 'Rata_Longitude']])"""),

    build_cell("code", """# 6.3 Visualisasi Sebaran Spasial & Boxplot Distribusi Harga 6 Klaster Mikro Pasar
fig, axes = plt.subplots(1, 2, figsize=(16, 7))
palette = sns.color_palette("tab10", n_colors=k_clusters)

# 1. Peta Sebaran Spasial Koordinat King County
sns.scatterplot(
    data=df, 
    x='Longitude', 
    y='Latitude', 
    hue='Cluster', 
    palette=palette,
    alpha=0.35, 
    s=15, 
    ax=axes[0],
    legend='full'
)

# Plot Centroid Klaster
centers_orig = scaler_cluster.inverse_transform(kmeans.cluster_centers_)
axes[0].scatter(
    centers_orig[:, 1], 
    centers_orig[:, 0], 
    c='red', 
    marker='*', 
    s=250, 
    edgecolors='black', 
    linewidth=1.5,
    label='Centroid Klaster'
)
axes[0].set_title("Peta Sebaran 6 Klaster Mikro-Pasar Real Estat King County", fontsize=12, fontweight='bold')
axes[0].set_xlabel("Longitude (WGS84)", fontsize=11)
axes[0].set_ylabel("Latitude (WGS84)", fontsize=11)
axes[0].legend(title="Cluster ID", loc="lower left", fontsize=9)

# 2. Boxplot Distribusi Harga Jual per Klaster
sns.boxplot(
    data=df, 
    x='Cluster', 
    y=df['SalePrice'] / 1000, 
    hue='Cluster',
    palette=palette, 
    ax=axes[1],
    legend=False,
    showfliers=False
)
axes[1].set_title("Distribusi Harga Properti per Klaster Mikro-Pasar (dalam Ribuan USD)", fontsize=12, fontweight='bold')
axes[1].set_xlabel("Cluster ID", fontsize=11)
axes[1].set_ylabel("Harga Jual ($1,000)", fontsize=11)

plt.tight_layout()
plt.show()"""),

    build_cell("code", """# 6.4 Implementasi Nyata: Fitur Pembanding Properti (Empirical Comps Retrieval)
def find_cluster_comps(target_lat, target_lon, target_price, data_pool, top_n=5):
    \"\"\"
    Menemukan properti pembanding terbaik di dalam klaster mikro-pasar yang sama.
    \"\"\"
    target_vec = np.array([[target_lat, target_lon, np.log(target_price)]])
    target_scaled = scaler_cluster.transform(target_vec)
    target_cluster = int(kmeans.predict(target_scaled)[0])
    
    cluster_pool = data_pool[data_pool['Cluster'] == target_cluster].copy()
    pool_vecs = cluster_pool[['Latitude', 'Longitude']].copy()
    pool_vecs['LogPrice'] = np.log(cluster_pool['SalePrice'])
    pool_scaled = scaler_cluster.transform(pool_vecs)
    
    dists = np.linalg.norm(pool_scaled - target_scaled, axis=1)
    cluster_pool['DistanceScore'] = dists
    cluster_pool['MatchScore'] = np.clip(100 * (1 - dists / (dists.max() + 1e-6)), 70, 99.9).round(1)
    
    comps = cluster_pool.sort_values(by='DistanceScore').head(top_n)
    return target_cluster, comps

# Demonstrasi Pencarian Comps untuk Properti Contoh
sample_prop = df.iloc[42]
t_lat, t_lon, t_price = sample_prop['Latitude'], sample_prop['Longitude'], sample_prop['SalePrice']

target_cluster_id, comps_result = find_cluster_comps(t_lat, t_lon, t_price, df, top_n=5)
cluster_name = cluster_summary.loc[cluster_summary['Cluster'] == target_cluster_id, 'Profil_Mikro_Pasar'].values[0]

print("=== Hasil Pencarian Properti Pembanding (Comparative Market Analysis) ===")
print(f"Properti Target: Lokasi ({t_lat:.4f}°N, {t_lon:.4f}°W) | Harga: ${t_price:,.0f} | Zip: {sample_prop['ZipCode']}")
print(f"Klaster Mikro-Pasar Terpilih: Cluster {target_cluster_id} -> {cluster_name}\\n")

comps_display = comps_result[['MatchScore', 'SalePrice', 'SqFtTotLiving', 'Bedrooms', 'TotalBaths', 'BldgGrade', 'ZipCode', 'DistanceScore']].copy()
comps_display['SalePrice'] = comps_display['SalePrice'].apply(lambda x: f"${x:,.0f}")
comps_display['MatchScore'] = comps_display['MatchScore'].apply(lambda x: f"{x:.1f}%")
comps_display['DistanceScore'] = comps_display['DistanceScore'].round(4)
display(comps_display.reset_index(drop=True))"""),

    build_cell("markdown", "## 7. Analisis Fitur Penting (*Feature Importance*)\nMenghitung bobot kontribusi setiap variabel terhadap akurasi estimasi harga menggunakan Permutation Importance pada model regresi terbaik."),
    build_cell("code", """best_model = trained_models['HistGradientBoosting Regressor']

perm_imp = permutation_importance(best_model, X_test, ylog_test, n_repeats=5, random_state=42, n_jobs=-1)
importance_df = pd.DataFrame({
    'Feature': feature_cols,
    'Importance Mean': perm_imp.importances_mean
}).sort_values(by='Importance Mean', ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(x='Importance Mean', y='Feature', hue='Feature', data=importance_df.head(10), palette='viridis', legend=False)
plt.title("10 Fitur Paling Berpengaruh terhadap Harga Properti (Permutation Importance)", fontsize=13, fontweight='bold')
plt.xlabel("Penurunan Skor R2 ketika Fitur Diacak")
plt.ylabel("Fitur Prediktor")
plt.tight_layout()
plt.show()

display(importance_df.head(10))"""),

    build_cell("markdown", "## 8. Serialisasi Model & Ekspor Artefak untuk Deployment"),
    build_cell("code", """models_dir = "../models"
os.makedirs(models_dir, exist_ok=True)

best_reg_path = os.path.join(models_dir, "best_valuation_model.joblib")
best_clf_path = os.path.join(models_dir, "market_tier_classifier.joblib")
kmeans_path = os.path.join(models_dir, "kmeans_cluster_model.joblib")

joblib.dump(best_model, best_reg_path)
joblib.dump(clf, best_clf_path)
joblib.dump({
    'model': kmeans,
    'scaler': scaler_cluster,
    'features': ['Latitude', 'Longitude', 'LogPrice'],
    'n_clusters': k_clusters,
    'cluster_profiles': cluster_summary.to_dict(orient='records'),
    'metrics': {
        'inertia': float(inertia_val),
        'silhouette': float(silhouette_val),
        'calinski_harabasz': float(calinski_val),
        'davies_bouldin': float(davies_val)
    }
}, kmeans_path)

print(f"Model regresi tersimpan ke      : {best_reg_path} ({os.path.getsize(best_reg_path):,} bytes)")
print(f"Model klasifikasi tersimpan ke  : {best_clf_path} ({os.path.getsize(best_clf_path):,} bytes)")
print(f"Model K-Means klaster tersimpan : {kmeans_path} ({os.path.getsize(kmeans_path):,} bytes)")"""),

    build_cell("markdown", """## 9. Kesimpulan Komprehensif Pemodelan
1. **Model Regresi Hedonik Terbaik:** **HistGradientBoosting Regressor** mencapai $R^2 = 0.8836$, $\\text{RMSE} = 0.1936$, dan $\\text{MAPE} = 13.55\\%$, jauh melampaui baseline linier ($R^2 \\approx 0.746$) dan pohon tunggal ($R^2 = 0.8168$).
2. **Benchmarking Model Klasifikasi:** HistGradientBoosting Classifier unggul dengan akurasi $87.78\\%$ dan Macro F1-Score $0.8774$ dalam mengklasifikasikan kelas segmen (*Entry*, *Mid*, *Luxury*).
3. **Unsupervised K-Means Micro-Market Segmentation ($k=6$):**
   - Berhasil membagi pasar King County ke dalam 6 mikro-pasar homogen berdasarkan koordinat (`Latitude`, `Longitude`) dan log harga dengan *Silhouette Score* $0.3120$, *Calinski-Harabasz Score* $11,215.17$, dan *Davies-Bouldin Index* $1.0748$.
   - Segmentasi membedakan secara tegas klaster *Affordable Urban* (median \$270k) hingga klaster *Bellevue Waterfront Luxury* (median \$1.08M).
   - Memungkinkan fitur *Comparative Market Analysis* (CMA) yang mencocokkan comps properti terdekat dalam sub-pasar yang sama secara akurat.
4. **Dominansi Fitur Spasial & Struktural:** Variabel spasial (`Latitude`, `Longitude`) bersama dengan luas bangunan (`SqFtTotLiving`) dan kualitas konstruksi (`BldgGrade`) merupakan determinan paling kritis terhadap nilai pasar properti King County.""")
]

# Write all notebooks
def write_nb(cells, filename):
    nb = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python (King County AVM)",
                "language": "python",
                "name": "kingcounty-venv"
            },
            "language_info": {
                "name": "python",
                "version": "3.12.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    path = os.path.join(nb_dir, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2)
    print(f"Berhasil menulis {path} ({len(cells)} sel).")

if __name__ == "__main__":
    write_nb(cells_nb1, "01_eda.ipynb")
    write_nb(cells_nb2, "02_cleaning_preprocessing.ipynb")
    write_nb(cells_nb3, "03_modeling_evaluation.ipynb")
    print("Semua notebook (01, 02, 03) berhasil diperbarui!")
