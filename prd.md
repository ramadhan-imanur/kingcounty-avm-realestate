# 📄 PRODUCT REQUIREMENT DOCUMENT (PRD)
## KingCounty-AVM: Sistem Cerdas Valuasi Properti & Ekonometrika Spasial Real Estat Berbasis Machine Learning

---

### 📌 Ringkasan Status Dokumen
| Atribut | Keterangan Standar Perusahaan |
| :--- | :--- |
| **Nama Produk / Proyek** | **KingCounty-AVM: Automated Valuation Model & Spatial Real Estate Intelligence Engine** |
| **Dataset Acuan** | `data/raw/02_king_county_real_estate/cleansales.tab` (Harvard Dataverse) |
| **Tim Pengembang** | **Tim 6 Sains Data FMIPA UNS** (6 Anggota) |
| **Daftar Anggota Tim** | 1. **Ramadhan Imanur Rochim**<br>2. **Thalita Anindya Ramadani**<br>3. **Amdadur Rohman**<br>4. **Hanifah Qurratul 'Aini**<br>5. **Dyandra Rizky Aulia**<br>6. **Alysia Putri Pradita** |
| **Stakeholder / Klien** | Dosen Pengampu Sains Data FMIPA UNS, Calon Pembeli/Penjual Properti, Agen Real Estat, Investor Properti |
| **Status Dokumen** | `APPROVED / READY FOR IMPLEMENTATION` |
| **Target Peluncuran (Target Launch)** | Akhir Siklus Semester Genap 2026 |
| **Versi Dokumen** | `v2.0.0` (Transisi Penuh ke Dataset 02_king_county_real_estate) |

---

### 👥 Distribusi Peran & Tanggung Jawab Tim (Team RACI Matrix)

| No | Nama Anggota | Peran Utama Proyek | Fokus Tanggung Jawab Fungsional |
| :-: | :--- | :--- | :--- |
| 1 | **Ramadhan Imanur Rochim** | *Project Lead & Full-Stack Data Scientist* | Koordinasi arsitektur sistem, orkestrasi PRD, integrasi model inferensi ke aplikasi web Streamlit, dan penjaminan mutu end-to-end. |
| 2 | **Thalita Anindya Ramadani** | *Data Profiling & Spatial EDA Specialist* | Eksplorasi statistik korpus 22.847 transaksi x 147 kolom (`01_eda.ipynb`), analisis distribusi *heavy-tailed* harga jual, dan pemetaan korelasi spasial koordinat (`X`, `Y`). |
| 3 | **Amdadur Rohman** | *Data Cleaning & Feature Engineering Engineer* | Pembersihan *trailing whitespaces*, reduksi dimensi dari 147 kolom menjadi fitur prediktor esensial, parsing tanggal transaksi (`DocumentDate`), dan rekayasa fitur usia bangunan serta rasio luas. |
| 4 | **Hanifah Qurratul 'Aini** | *Machine Learning Engineer (Hedonic Regression)* | Pengembangan model regresi harga properti (`SalePrice` / $\log(\text{SalePrice})$): Linear, Ridge, Random Forest, XGBoost/LightGBM, dan optimasi $R^2$ / RMSE. |
| 5 | **Dyandra Rizky Aulia** | *Machine Learning Engineer (Classification & Valuation)* | Pengembangan model klasifikasi tier pasar properti (*Entry-level*, *Mid-tier*, *Luxury*) serta deteksi properti *under-assessed / undervalued* berbasis rasio pajak (`ImpsVal + LandVal`). |
| 6 | **Alysia Putri Pradita** | *UI/UX & Web Application Specialist* | Desain tata letak antarmuka Streamlit (`app/app.py`), pembangunan form kalkulator valuasi properti, peta interaktif sebaran harga, dan visualisasi *Explainable AI* (SHAP). |

---

## 1. Ringkasan Eksekutif & Latar Belakang (Executive Summary & Context)

> **Standar Industri:** Bagian ini memberikan gambaran ringkas (*elevator pitch*) kepada eksekutif dan pemangku kepentingan mengenai masalah nyata yang dihadapi dan solusi berbasis data yang akan dikembangkan.

### ❓ Pertanyaan Panduan & Konteks:
1. **Nama & Identitas Proyek:** Apa nama ringkas dan deskriptif untuk solusi/produk data sains yang ingin dibangun?
2. **Konteks & Masalah Nyata:** Masalah nyata apa di dunia nyata/bisnis yang memicu lahirnya proyek ini? Mengapa masalah ini mendesak untuk diselesaikan sekarang?
3. **Solusi yang Diajukan:** Secara garis besar, bagaimana pendekatan machine learning dan aplikasi web (Streamlit) memecahkan masalah tersebut secara efektif?

### ✍️ Jawaban & Spesifikasi Dokumen:
- **Nama Resmi Proyek:**  
  `KingCounty-AVM: Automated Valuation Model & Spatial Real Estate Intelligence Engine`
- **Latar Belakang Masalah:**  
  Pasar properti di kawasan metropolitan King County, Washington (mencakup Seattle, Bellevue, Redmond, dan sekitarnya) merupakan salah satu pasar real estat paling dinamis dan bernilai tinggi di Amerika Serikat. Namun, penentuan harga wajar properti (*fair market valuation*) secara konvensional memiliki kelemahan mendasar:
  1. *Biaya Appraisal Mahal:* Menggunakan jasa penilai independen (*professional property appraiser*) memakan biaya \$400–\$800 per transaksi dan membutuhkan waktu beberapa hari hingga minggu.
  2. *Asimetri Informasi & Subjektivitas:* Pembeli pertama (*first-time homebuyers*) dan penjual sering kali kesulitan menentukan apakah harga yang ditawarkan terlalu mahal (*overpriced*) atau murah (*underpriced*).
  3. *Kompleksitas Multi-Faktor Spasial:* Harga properti tidak hanya ditentukan oleh luas bangunan dan jumlah kamar, melainkan interaksi kompleks antara faktor ekonometrika spasial: kedekatan dengan tepi air (*waterfront*), panorama (Seattle Skyline, Mt. Rainier, Lake Washington), polusi suara (bandara/jalan raya), usia bangunan, hingga kualitas konstruksi (*building grade*).
- **Ringkasan Solusi (Executive Summary):**  
  Membangun aplikasi web cerdas berbasis **Streamlit** yang mengintegrasikan model pembelajaran mesin (*Automated Valuation Model / AVM*) terlatih pada dataset resmi transaksi properti King County (22.847 baris transaksi dengan 147 atribut). Sistem ini mampu:
  1. Melakukan valuasi harga jual wajar properti secara instan ($< 1$ detik) berdasarkan spesifikasi fisik dan koordinat spasial.
  2. Mengklasifikasikan kelas properti ke dalam tier segmen pasar (*Entry-level*, *Mid-market*, *Luxury*).
  3. Memberikan dekomposisi transparan mengenai faktor apa saja yang mendongkrak atau menurunkan nilai rumah menggunakan teknik *Explainable AI* (XAI/SHAP).
  4. Menampilkan peta interaktif sebaran harga dan perbandingan pasar komparatif (*Comparative Market Analysis* / CMA).

---

## 2. Definisi Masalah & Target Pengguna (Problem Statement & User Personas)

> **Standar Industri:** Mengidentifikasi secara presisi siapa yang mengalami masalah, seberapa besar rasa sakit (*pain point*) mereka, serta bagaimana produk ini akan mengubah alur kerja mereka.

### ❓ Pertanyaan Panduan & Konteks:
1. **Siapa Target Pengguna Utama (Primary Persona)?**
2. **Apa Rasa Sakit (*Pain Points*) Mereka Saat Ini?**
3. **Apa Nilai Tambah (*Value Proposition*) Utama yang Dirasakan Pengguna?**

### ✍️ Jawaban & Spesifikasi Dokumen:
| Elemen Persona | Deskripsi Rinci Spesifikasi Proyek |
| :--- | :--- |
| **Profil Pengguna (User Persona)** | **1. Calon Pembeli & Penjual Rumah (*Homebuyers & Sellers*):** Individu yang ingin membeli atau menjual rumah di King County dan membutuhkan estimasi harga independen.<br>**2. Agen Properti & Broker Real Estat:** Profesional yang membutuhkan alat estimasi cepat untuk menyusun *Comparative Market Analysis* (CMA) bagi klien.<br>**3. Investor Real Estat & Flippers:** Investor yang mencari rumah dengan potensi *undervalued* (harga pasar di bawah estimasi wajar mesin AVM) untuk direnovasi dan dijual kembali. |
| **Tugas Utama Sehari-hari (Jobs to be Done)** | Menghitung perkiraan harga jual properti, menganalisis faktor kenaikan nilai rumah jika direnovasi, membandingkan harga properti di suatu kode pos (*zip code*), dan menyusun anggaran penawaran (*bidding price*). |
| **Kendala Utama (Pain Points)** | - Mengandalkan intuisi atau perbandingan manual yang rawan bias.<br>- Menunggu laporan penilai (*appraisal report*) terlalu lama saat persaingan transaksi berlangsung cepat.<br>- Ketidakmampuan memperhitungkan premi pemandangan (*view amenity premium*) seperti Lake Washington atau Seattle Skyline secara kuantitatif. |
| **Ekspektasi Hasil (Desired Outcome)** | Pengguna cukup memasukkan karakteristik rumah (luas bangunan, kamar tidur, kamar mandi, grade, tahun bangun, lokasi/zip code), lalu dalam hitungan detik menerima estimasi harga wajar lengkap dengan rentang batas keyakinan (*confidence interval*), kelas segmen pasar, dan simulasi penambahan nilai jika direnovasi. |

---

## 3. Visi Produk, Batasan & Ruang Lingkup (Vision, Goals & Non-Goals)

> **Standar Industri:** Menetapkan batasan yang tegas sangat penting untuk mencegah *scope creep* (pelebaran lingkup proyek tanpa kendali). *Non-Goals* sama pentingnya dengan *Goals*.

### ❓ Pertanyaan Panduan & Konteks:
1. **Product Goals (Target In-Scope):** Apa saja capaian utama yang wajib terwujud dalam rilis versi v1?
2. **Product Non-Goals (Batasan Out-of-Scope):** Hal-hal apa saja yang secara sadar tidak dikerjakan agar pengembangan tetap fokus dan selesai tepat waktu?

### ✍️ Jawaban & Spesifikasi Dokumen:
- **Goals (Tujuan Utama yang Dicakup):**
  1. Melakukan pembersihan data (*data cleaning*) pada korpus 22.847 data transaksi King County: mengatasi spasi berlebih (*trailing whitespace*), parsing tanggal dokumen transaksi, pembuangan transaksi anomali non-pasar, dan transformasi logaritmik harga.
  2. Melakukan reduksi dimensi (*feature selection*) terstruktur dari 147 kolom menjadi 20–30 fitur kunci prediktif berbasis domain ekonometrika properti.
  3. Membangun dan memvalidasi model Machine Learning:
     - **Regresi Hedonik (AVM):** Memprediksi harga jual kontinu (`SalePrice`) menggunakan algoritma regresi linear terregularisasi dan ensemble (*Random Forest / LightGBM / XGBoost*).
     - **Klasifikasi Segmen Pasar:** Memprediksi tier properti (*Entry*, *Mid*, *Luxury*) atau mendeteksi properti berstatus *bargain/undervalued*.
  4. Mengembangkan aplikasi web interaktif berbasis **Streamlit** (`app/app.py`) dengan simulator kalkulasi harga interaktif, kalkulator dampak renovasi (*renovation ROI simulator*), visualisasi fitur penting (*XAI SHAP values*), dan dashboard filter geografis.
  5. Menghasilkan modul kode bersih di `src/` dan model serialisasi `.joblib` di `models/`.
- **Non-Goals (Batasan yang Dikecualikan):**
  1. *Tidak melayani transaksi di luar wilayah yurisdiksi King County, Washington* (model dispesifikasikan khusus untuk karakteristik ekonometrika King County).
  2. *Tidak mengintegrasikan feed langsung MLS (Multiple Listing Service) real-time via koneksi streaming API berbayar* (menggunakan korpus resmi Harvard Dataverse).
  3. *Tidak menggantikan fungsi legal sertifikat appraisal resmi perbankan untuk pencairan hipotek/KPR* (aplikasi ditujukan sebagai alat estimasi analitik keputusan bisnis).

---

## 4. Matriks Keberhasilan (Success Metrics & KPIs)

> **Standar Industri:** Setiap proyek teknologi yang matang harus memiliki metrik kuantitatif yang jelas untuk memvalidasi apakah produk berhasil atau gagal.

### ❓ Pertanyaan Panduan & Konteks:
1. **Business / User KPIs:** Indikator dampak apa yang ingin diukur bagi pengguna aplikasi?
2. **Machine Learning Performance Metrics:** Berapa target ambang batas metrik evaluasi model?
3. **Engineering / Operational KPIs:** Berapa batas toleransi waktu inferensi aplikasi?

### ✍️ Jawaban & Spesifikasi Dokumen:
| Kategori Metrik | Nama Metrik | Target Kuantitatif | Alasan Pemilihan Metrik |
| :--- | :--- | :--- | :--- |
| **Model Regresi (Akurasi)** | Koefisien Determinasi ($R^2$) | $R^2 \ge 0.85$ pada *test set* | Menjamin model mampu menjelaskan minimal 85% variansi harga properti dari fitur fisik dan spasial. |
| **Model Regresi (Deviasi)** | Mean Absolute Percentage Error (MAPE) | $\text{MAPE} \le 12\%$ | Standar industri AVM properti (Zillow/Redfin) menetapkan error median berkisar antara 10%–15%. |
| **Model Regresi (Root Error)** | Root Mean Squared Error (RMSE) | $\text{RMSE}_{\log} \le 0.18$ | Mengukur kestabilan estimasi pada skala logaritmik harga untuk meminimalkan penalti deviasi ekstrem. |
| **Model Klasifikasi** | Macro F1-Score | $\text{F1-Score} \ge 0.85$ | Memastikan akurasi tinggi dan seimbang pada seluruh kelas segmentasi pasar (*Entry, Mid, Luxury*). |
| **Latensi Inferensi Web** | Prediction Response Time | $\le 0.8$ detik per evaluasi | Memberikan hasil estimasi harga instan saat pengguna mengubah slider atau mengisi form di Streamlit. |
| **Efisiensi Seleksi Fitur** | Reduksi Dimensi Fitur | Dari 147 kolom menjadi $\le 30$ fitur | Meminimalkan beban komputasi dan menyederhanakan formulir input pengguna tanpa mengorbankan akurasi. |

---

## 5. Fondasi Data & Kebutuhan Pra-Pemrosesan (Data Foundation & Cleaning)

> **Standar Industri:** Model AI berkualitas tinggi bermula dari data yang bersih dan representatif (*Garbage In, Garbage Out*).

### ❓ Pertanyaan Panduan & Konteks:
1. **Dataset Pilihan:** Dataset apa yang digunakan, format, dan jumlah observasinya?
2. **Target Variabel ($Y$):** Apa target prediksi untuk tugas regresi dan klasifikasi?
3. **Fitur Kunci Prediktor ($X$):** Fitur apa saja yang diseleksi dari 147 kolom yang tersedia?
4. **Tantangan Pembersihan Data (Data Wrangling):** Masalah kotor apa yang ada dan bagaimana penanganannya?

### ✍️ Jawaban & Spesifikasi Dokumen:
- **Dataset Terpilih:**  
  `data/raw/02_king_county_real_estate/cleansales.tab` (22.847 baris transaksi x 147 kolom, format TSV) dan kamus data `dataDictionary.tab`.
- **Target Variabel ($Y$):**
  - **Tugas Regresi Utama:** `SalePrice` (nilai kontinu harga jual transaksi properti, rentang \$5.000 hingga \$9.400.000, median \$450.000). Target dimodelkan menggunakan transformasi logaritmik $\ln(\text{SalePrice})$ guna mengatasi kemencengan (*skewness*).
  - **Tugas Klasifikasi:** `PropertyTier` (kategori 3-kelas):
    - *Entry-Level:* $\text{SalePrice} < \$350.000$
    - *Mid-Market:* $\$350.000 \le \text{SalePrice} \le \$700.000$
    - *Luxury / High-End:* $\text{SalePrice} > \$700.000$
- **Seleksi Fitur Kunci ($X$) dari 147 Kolom:**
  Dari 147 kolom yang sangat lebar, dilakukan seleksi berbasis domain menjadi 5 kelompok fitur esensial:
  1. *Struktur Fisik & Dimensi:*
     - `SqFtTotLiving` (Luas total area hunian)
     - `SqFtLot` (Luas tanah pekarangan)
     - `Bedrooms` (Jumlah kamar tidur)
     - `BathFullCount`, `BathHalfCount`, `Bath3qtrCount` (Jumlah kamar mandi terpisah)
     - `Stories` (Jumlah lantai bangunan)
     - `SqFtTotBasement`, `SqFtFinBasement` (Luas ruang bawah tanah)
     - `SqFtGarageAttached` (Luas garasi mobil)
     - `SqFtOpenPorch`, `SqFtDeck` (Luas teras & dek terbuka)
  2. *Kualitas & Usia Properti:*
     - `BldgGrade` (Nilai mutu konstruksi bangunan skala 1–13 dari King County Assessor)
     - `Condition` (Kondisi pemeliharaan bangunan skala 1–5)
     - `YrBuilt` (Tahun pembangunan awal)
     - `YrRenovated` (Tahun renovasi terakhir, jika pernah direnovasi)
  3. *Lokasi & Koordinat Spasial:*
     - `ZipCode` (Kode pos area)
     - `DistrictName`, `Area`, `SubArea` (Distrik yurisdiksi properti)
     - `X`, `Y` (Koordinat spasial proyeksi wilayah)
  4. *Pemandangan & Lingkungan (Amenity Views):*
     - `WfntLocation` & `WfntFootage` (Keberadaan & panjang garis tepi air/waterfront)
     - `SeattleSkyline`, `PugetSound`, `LakeWashington`, `LakeSammamish`, `MtRainier`, `Olympics`, `Cascades` (Indikator pemandangan lanskap)
     - `TrafficNoise`, `AirportNoise`, `PowerLines` (Faktor gangguan lingkungan)
  5. *Nilai Taksiran Pajak (Tax Assessments):*
     - `LandVal` (Taksiran nilai tanah oleh penilai pajak)
     - `ImpsVal` (Taksiran nilai bangunan fisik)
- **Rencana & Strategi Pembersihan Data Kotor:**
  - *Pembersihan Teks (*Trailing Whitespaces*):* Menghapus spasi berlebih pada nama pihak (`SellerName`, `BuyerName`), alamat, dan kode teks menggunakan `.str.strip()`.
  - *Filtering Transaksi Non-Pasar / Outlier Ekstrem:* Menyaring transaksi yang bukan harga pasar wajar (misal transaksi hibah keluarga dengan harga $<\$10.000$ atau properti cacat).
  - *Parsing Tanggal & Rekayasa Fitur Waktu:* Mengonversi `DocumentDate` ke tipe data `datetime` untuk mengekstraksi bulan penjualan (`SaleMonth`), kuartal (`SaleQuarter`), dan tren musiman properti (*seasonality*).
  - *Rekayasa Fitur Domain (*Feature Engineering*):*
    - $\text{PropertyAge} = \text{salesYear} - \text{YrBuilt}$ (Usia bangunan saat terjual).
    - $\text{IsRenovated} = 1 \text{ jika } \text{YrRenovated} > 0 \text{ else } 0$ (Status renovasi).
    - $\text{TotalBaths} = \text{BathFullCount} + 0.75 \times \text{Bath3qtrCount} + 0.5 \times \text{BathHalfCount}$.
    - $\text{PricePerSqFt} = \text{SalePrice} / \text{SqFtTotLiving}$ (Metrik harga per luas lantai).
    - $\text{AssessmentRatio} = \text{SalePrice} / (\text{LandVal} + \text{ImpsVal})$ (Rasio harga pasar terhadap taksiran pajak).

---

## 6. Formulasi Machine Learning & Arsitektur Model (ML Formulation)

> **Standar Industri:** Mendefinisikan pendekatan matematis dan algoritma komputasi yang selaras dengan tujuan produk.

### ❓ Pertanyaan Panduan & Konteks:
1. **Paradigma Machine Learning yang Diterapkan?**
2. **Model Baseline vs Algoritma Kandidat Utama?**
3. **Kebutuhan Interpretasi & Explainable AI (XAI)?**

### ✍️ Jawaban & Spesifikasi Dokumen:
- **Paradigma ML:**  
  Supervised Learning dengan arsitektur pipa ganda (*Dual Machine Learning Pipeline*):
  1. *Model Regresi Hedonik (AVM Engine):* Memprediksi harga kontinu $\log(\text{SalePrice})$ yang kemudian ditransformasikan kembali via eksponensial $\exp(\hat{y})$.
  2. *Model Klasifikasi Segmentasi Pasar:* Mengklasifikasikan properti ke dalam kelas tier (*Entry / Mid / Luxury*).
- **Strategi Model Baseline:**
  - Regresi Baseline: *Ordinary Least Squares (OLS) Multiple Linear Regression* sebagai tolok ukur ekonometrika klasik.
  - Klasifikasi Baseline: *Logistic Regression* multinomial dengan standardisasi fitur.
- **Kandidat Algoritma Utama (Benchmarking 7 Model):**
  - **OLS Linear Regression:** Model dasar ekonometrika klasik kuadrat terkecil.
  - **Ridge, Lasso & Elastic Net Regression:** Analisis komparatif penalti norma $L_2$ (Ridge shrinkage), norma $L_1$ (Lasso sparsity), dan hibrida Elastic Net ($L_1 + L_2$) untuk menangani multikolinearitas antar fitur fisik dan koordinat sesuai rujukan akademis (Zou & Hastie, 2005; Saputro, 2025).
  - **Decision Tree & Random Forest Regressor:** Model non-linear pohon tunggal dan ensemble bagging untuk menangkap interaksi batas wilayah non-linear tanpa asumsi linearitas.
  - **HistGradientBoosting Regressor (LightGBM-style):** Algoritma *gradient boosted decision trees* berbasis histogram yang menjadi standar industri teratas dalam pemodelan tabel real estat berskala besar ($R^2 = 0.8848$).
- **Prosedur Validasi & Pencegahan Leakage:**
  - Pembagian data: 80% *Train Set*, 20% *Test Set* secara acak terkontrol (`random_state=42`).
  - 5-Fold Cross-Validation pada set pelatihan.
  - Seluruh *scaling*, *encoding*, dan imputasi dibungkus dalam `scikit-learn Pipeline` agar tidak terjadi kebocoran data (*data leakage*) ke test set.
- **Kebutuhan Explainability (XAI):**  
  Implementasi **SHAP (SHapley Additive exPlanations)** untuk memberikan transparansi valuasi (*Decomposed Property Valuation*):
  - Berapa dolar nilai tambah dari pemandangan Seattle Skyline atau Lake Washington?
  - Berapa dolar depresiasi harga akibat usia bangunan tua yang belum direnovasi?
  - Fitur apa yang paling dominan mengatrol harga rumah spesifik yang dimasukkan pengguna?

---

## 7. Kebutuhan Fungsional & Antarmuka Pengguna (User Stories & UI/UX)

> **Standar Industri:** Menggambarkan pengalaman pengguna langkah demi langkah dari membuka aplikasi web Streamlit hingga mendapatkan hasil keputusan bisnis.

### ❓ Pertanyaan Panduan & Konteks:
1. **Bagaimana Alur Pengguna (User Journey)?**
2. **Bagaimana Rancangan Struktur Antarmuka Aplikasi Streamlit (`app/app.py`)?**
3. **Apa Prioritas Fitur dengan Pendekatan MoSCoW?**

### ✍️ Jawaban & Spesifikasi Dokumen:
- **Daftar User Stories Utama:**
  - *Sebagai Calon Pembeli Rumah*, saya ingin memasukkan spesifikasi rumah impian saya (kamar tidur, kamar mandi, luas tanah, kode pos, dan pemandangan), sehingga saya mendapatkan estimasi harga pasar wajar sebelum mengajukan penawaran.
  - *Sebagai Penjual Rumah*, saya ingin mensimulasikan dampak renovasi (misal menaikkan *BldgGrade* dari 7 ke 9 atau memperbarui *YrRenovated*), sehingga saya mengetahui estimasi potensi kenaikan harga jual (*Renovation ROI*).
  - *Sebagai Agen Properti*, saya ingin melihat perbandingan harga rumah di peta sebaran interaktif King County, sehingga saya dapat menunjukkan tren harga komparatif (*CMA*) kepada klien.
- **Rancangan Struktur Menu Antarmuka Web Streamlit (`app/app.py`):**
  1. **Menu 1: Market Overview & Spatial Explorer:**  
     Menampilkan ringkasan metrik 22.847 transaksi King County, histogram distribusi harga rumah, dan peta sebaran transaksi interaktif berdasarkan koordinat (`X`, `Y`) dan filter kode pos (`ZipCode`).
  2. **Menu 2: AVM Smart Property Valuator (Kalkulator Valuasi):**  
     Formulir input di sidebar: luas area hunian (`SqFtTotLiving`), luas pekarangan (`SqFtLot`), jumlah kamar tidur/mandi, grade bangunan (1–13), tahun bangun, kode pos, dan checkbox pemandangan (*Lake Washington*, *Waterfront*, *Seattle Skyline*).
  3. **Menu 3: Hasil Valuasi & Dekomposisi SHAP (Valuation Breakdown):**  
     Menampilkan kartu metrik harga estimasi ($\$X$), rentang deviasi wajar ($\pm 10\%$), badge kelas segmen (*Entry/Mid/Luxury*), serta grafik *SHAP Waterfall Plot* yang merinci kontribusi rupiah setiap fitur terhadap harga akhir.
  4. **Menu 4: Simulator ROI Renovasi (Renovation Value-Add):**  
     Fitur simulasi: membandingkan harga rumah saat ini vs harga setelah direnovasi (peningkatan grade dan kondisi) untuk melihat estimasi kenaikan ekuitas properti.
- **Spesifikasi Prioritas Fitur (Metode MoSCoW):**
  - **Must-Have (Wajib Ada):**
    - Pemuatan model regresi terlatih dari direktori `models/`.
    - Form input parameter fisik dan geografis properti.
    - Komputasi prediksi harga seketika ($< 1$ detik).
    - Kartu ringkasan harga dan rentang batas keyakinan (*confidence interval*).
  - **Should-Have (Sangat Dianjurkan):**
    - Visualisasi SHAP value (faktor pendorong & penahan harga).
    - Simulator nilai tambah renovasi (*Renovation ROI*).
    - Peta sebaran spasial transaksi komparatif di kode pos terkait.
  - **Could-Have (Fitur Tambahan Opsional):**
    - Tombol unduh laporan taksiran properti format PDF/Markdown.
  - **Won't-Have (Fase Mendatang):**
    - Sambungan API langsung ke portal Zillow/Redfin atau pengajuan hipotek KPR bank otomatis.

---

## 8. Kebutuhan Non-Fungsional (Non-Functional Requirements - NFR)

> **Standar Industri:** Kriteria kualitas teknis yang memastikan aplikasi dapat diandalkan, cepat, aman, dan mudah diakses.

### ❓ Pertanyaan Panduan & Konteks:
1. **Performa & Kecepatan:** Seberapa responsif aplikasi saat digunakan?
2. **Keterbacaan & Aksesibilitas:** Bagaimana standar tampilan bagi pembaca layar dan kemudahan navigasi?
3. **Portabilitas & Reproducibility:** Bagaimana memastikan kode dapat direplikasi dengan mudah?

### ✍️ Jawaban & Spesifikasi Dokumen:
- **Standar Performa & Kecepatan:**
  - *Startup Time:* Pemuatan awal aplikasi Streamlit dan model LightGBM/Random Forest $< 3$ detik.
  - *Inferensi Cepat:* Waktu prediksi harga properti $< 0.5$ detik setelah tombol "Hitung Valuasi" ditekan.
  - *Optimasi Memori:* Menggunakan caching `@st.cache_resource` untuk model dan `@st.cache_data` untuk data sampel peta agar hemat memori RAM.
- **Aksesibilitas & Keterbacaan (Screen-Reader Friendly):**
  - Mengikuti hierarki Markdown semantik murni (`#`, `##`, `###`).
  - Form input memiliki label teks yang jelas tanpa singkatan asing yang membingungkan.
  - Visualisasi grafik dilengkapi tabel ringkasan data tekstual alternatif agar pengguna dengan pembaca layar (*screen reader*) dapat memahami hasil analitik secara utuh.
  - Kontras visual yang tajam dan nyaman dibaca.
- **Portabilitas & Reproducibility:**
  - Pustaka terdaftar lengkap di `requirements.txt` (`pandas`, `numpy`, `scipy`, `scikit-learn`, `xgboost`, `lightgbm`, `streamlit`, `plotly`, `shap`, `joblib`).
  - Nilai pengacakan terkunci konsisten (`random_state=42`) di seluruh script pemodelan.

---

## 9. Rencana Kerja & Tahapan Rilis (Milestones & Timeline)

> **Standar Industri:** Alur pengerjaan terstruktur bertahap dari repositori mentah hingga produk akhir siap didemonstrasikan.

### ✍️ Jadwal Eksekusi 6 Tahap Proyek:
| Fase Proyek | Artefak & Berkas yang Dihasilkan | Fokus Pekerjaan Utama | Status |
| :--- | :--- | :--- | :---: |
| **Fase 1: PRD & Ruang Lingkup** | Berkas `prd.md` terintegrasi | Mengunci spesifikasi sistem KingCounty-AVM, arsitektur data, dan KPI | `DONE` |
| **Fase 2: Data Profiling & Spasial EDA** | Notebook `notebooks/01_eda.ipynb` | Analisis statistik 22.847 data, matriks korelasi 147 kolom, distribusi harga logaritmik | `DONE` |
| **Fase 3: Data Cleaning & Feature Eng** | Notebook `notebooks/02_cleaning_preprocessing.ipynb` & `data/processed/` | Reduksi 147 kolom $\to 40$ fitur, imputasi KNN spasial, parsing tanggal & usia bangunan | `DONE` |
| **Fase 4: Model Training & Evaluation** | Notebook `notebooks/03_modeling_evaluation.ipynb` & model di `models/` | Pelatihan & evaluasi 7 Model Regresi (OLS, Ridge, Lasso, Elastic Net, Decision Tree, RF, HistGradientBoosting $R^2 = 0.8848$) & 3 Classifier (Akurasi Tier = $87.78\%$), ekspor `.joblib` | `DONE` |
| **Fase 5: Web App Development** | Aplikasi aktif di `app/app.py` | Antarmuka Streamlit (Kalkulator AVM, Peta Spasial, Visualisasi XAI, Simulator ROI) | `DONE` |
| **Fase 6: Pengujian & Laporan Akhir** | Laporan akhir di `reports/` & gambar di `reports/figures/` | Validasi akurasi menyeluruh, evaluasi residual, penyusunan dokumentasi ilmiah | `IN PROGRESS` |

---

## 10. Manajemen Risiko, Asumsi & Mitigasi (Risks & Mitigations)

> **Standar Industri:** Mengidentifikasi potensi kegagalan teknis maupun domain sebelum implementasi dimulai.

### ✍️ Matriks Mitigasi Risiko:
| Potensi Risiko | Tingkat Dampak | Rencana Pencegahan & Mitigasi Konkret |
| :--- | :---: | :--- |
| **Kemencengan Ekstrem (*Heavy-Tailed*) Distribusi Harga** | Tinggi | Menerapkan transformasi logaritmik natural $\log(\text{SalePrice})$ pada tahap pelatihan dan mengubah kembali ke skala mata uang asli menggunakan eksponensial $\exp(\hat{y})$. |
| **Kutukan Dimensi (*Curse of Dimensionality*) dari 147 Kolom** | Tinggi | Melakukan seleksi fitur berbasis domain (*domain knowledge*), mengeliminasi kolom administratif/duplikat (ID, nomor plat, nama agen), dan memilih 20–30 prediktor paling signifikan. |
| **Multikolinearitas Kuat antar Fitur Luas Bangunan** | Sedang | Luas lantai 1, lantai 2, dan total luas hunian saling berkolerasi; gunakan `SqFtTotLiving` sebagai fitur primer dan terapkan algoritma pohon (*LightGBM/Random Forest*) yang kebal multikolinearitas. |
| **Outlier Rumah Mewah / Transaksi Non-Pasar** | Sedang | Menyaring transaksi di bawah \$50.000 (transfer keluarga/non-arm's length) dan menerapkan metode *robust scaling* pada data latih. |
| **Input Nilai Fisik Properti yang Tidak Realistis di Web** | Rendah | Mengunci batas minimum dan maksimum slider input di Streamlit sesuai rentang realistis data historis (misal: kamar tidur 1–10, luas 300–10.000 sqft). |

---

## 11. Pertanyaan Terbuka & Keputusan yang Tertunda (Open Questions)

> **Standar Industri:** Tempat mencatat hal-hal yang masih perlu didiskusikan dengan dosen/klien sebelum mengunci arsitektur final.

### ✍️ Catatan Keputusan:
- [x] **Pilihan Dataset Final:** Disepakati seluruh anggota Tim 6 menggunakan `02_king_county_real_estate` (22.847 baris transaksi x 147 kolom).
- [ ] **Penyajian Peta Spasial di Streamlit:** Apakah visualisasi peta properti cukup menggunakan *scatter map* teragregasi per kode pos (*ZipCode*), atau menggunakan peta interaktif titik koordinat (`X`, `Y`) dengan pustaka Folium/Plotly? *(Rekomendasi: Gabungan Plotly mapbox untuk kecepatan respons).*
- [ ] **Target Evaluasi Tambahan:** Apakah dosen pengampu mewajibkan perbandingan formal antara taksiran penilai pajak pemerintah (`LandVal + ImpsVal`) dengan prediksi model Machine Learning? *(Rekomendasi: Tambahkan metrik selisih akurasi model ML vs Tax Assessor).*

---

## 12. Lembar Persetujuan (Stakeholder Sign-Off)

| Peran Tim / Pemangku Kepentingan | Nama Penanggung Jawab | Status Verifikasi | Tanggal |
| :--- | :--- | :---: | :---: |
| **Project Lead & Full-Stack Data Scientist** | **Ramadhan Imanur Rochim** | `[X] Disetujui` | 2026-11-05 |
| **Data Profiling & Spatial EDA Specialist** | **Thalita Anindya Ramadani** | `[X] Disetujui` | 2026-11-05 |
| **Data Cleaning & Feature Engineering Engineer** | **Amdadur Rohman** | `[X] Disetujui` | 2026-11-05 |
| **ML Engineer (Hedonic Regression)** | **Hanifah Qurratul 'Aini** | `[X] Disetujui` | 2026-11-05 |
| **ML Engineer (Classification & Valuation)** | **Dyandra Rizky Aulia** | `[X] Disetujui` | 2026-11-05 |
| **UI/UX & Web Application Specialist** | **Alysia Putri Pradita** | `[X] Disetujui` | 2026-11-05 |
| **Reviewer Akademik / Dosen Pengampu** | Dosen Pengampu Sains Data FMIPA UNS | `[ ] Menunggu Review` | 2026-11-05 |
