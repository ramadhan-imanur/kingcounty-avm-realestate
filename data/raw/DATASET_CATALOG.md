# 📚 Katalog Dataset Terbuka Kredibel (Harvard Dataverse)

Dokumen ini memuat deskripsi lengkap 5 pilihan dataset yang telah diunduh dari repositori ilmiah resmi [Harvard Dataverse](https://dataverse.harvard.edu/). Kelima dataset ini berasal dari domain **Bisnis, Manajemen, Keuangan, dan Sains Matematika Terapan** serta sengaja memuat kondisi riil (*kotor/tidak bersih*) untuk latihan data wrangling, cleaning, dan preprocessing sebelum pemodelan Machine Learning.

---

## 1. World Management Survey (WMS) - Manufacturing
- **Institusi/Penyusun:** Harvard Business School, Stanford University, & London School of Economics (Bloom, Sadun, Van Reenen)
- **Persistent DOI:** [https://doi.org/10.7910/DVN/OY6CBK](https://doi.org/10.7910/DVN/OY6CBK)
- **Lokasi Folder:** `data/raw/01_world_management_survey/`
- **Berkas yang Tersedia:**
  - `wmsdata_2004_2015.tab` (Data utama: 11.702 baris x 27 kolom)
  - `wms_manufacturing_survey_instrument.pdf` (Instrumen survei & definisi skala penilaian 1–5)
  - `readme.txt` (Dokumentasi teknis variabel)
- **Bidang:** *Business Management, Operational Efficiency, Quantitative Economics*
- **Tantangan Data Cleaning (Kotor):**
  - Mengandung *missing values* (NA) yang tersebar pada beberapa dimensi evaluasi operasional dan data karakteristik perusahaan.
  - Nilai desimal dan diskrit campuran pada skor evaluasi manajerial (*lean manufacturing*, pemantauan kinerja, target, manajemen SDM).
  - Variabel kategorik tingkat kepemilikan dan ukuran perusahaan dalam bentuk *binned ranges* (misal `"A) 50 to 100"`, `"E) 1000+"`) yang memerlukan parsing teks dan encoding.
  - Outlier pada metrik numerik operasional.
- **Potensi Proyek ML:**
  - **Regresi:** Memprediksi skor efisiensi manajemen (`management`) berdasarkan dimensi target, lean, dan karakteristik perusahaan.
  - **Klasifikasi:** Mengklasifikasikan perusahaan kategori performa unggul (*High-tier*) vs standar (*Low-tier*).
  - **Clustering:** Segmentasi gaya manajemen manufaktur global.

---

## 2. King County Real Estate Sales & Property Assessment
- **Institusi/Penyusun:** King County Department of Assessments & University of Washington
- **Persistent DOI:** [https://doi.org/10.7910/DVN/VUAIMQ](https://doi.org/10.7910/DVN/VUAIMQ) & [https://doi.org/10.7910/DVN/GPRRND](https://doi.org/10.7910/DVN/GPRRND)
- **Lokasi Folder:** `data/raw/02_king_county_real_estate/`
- **Berkas yang Tersedia:**
  - `cleansales.tab` (Data transaksi: 22.847 baris x 147 kolom)
  - `dataDictionary.tab` (Kamus data definisi kode atribut properti dan perpajakan)
- **Bidang:** *Mathematical Econometrics, Spatial Statistics, Real Estate Finance & Valuation*
- **Tantangan Data Cleaning (Kotor):**
  - Data teks memiliki spasi berlebih (*trailing whitespaces*) yang masif pada nama pihak penjual/pembeli.
  - Dimensi data sangat lebar (147 kolom) sehingga memerlukan seleksi fitur (*feature selection*) dan pemahaman domain.
  - Nilai transaksi non-pasar (penjualan $0 atau transfer keluarga) dan outlier harga rumah mewah (*heavy-tailed price distribution*).
  - Format tanggal penjualan (*DocumentDate*) dalam bentuk string yang memerlukan parsing tanggal untuk ekstraksi fitur musiman/tren waktu.
- **Potensi Proyek ML:**
  - **Regresi:** Memprediksi harga jual properti (`SalePrice`) menggunakan pemodelan ekonometrika hedonik.
  - **Feature Engineering:** Rasio harga per luas area, kalkulasi usia bangunan saat terjual, indikator renovasi.
  - **Klasifikasi:** Prediksi tier kelas properti (*Entry-level, Middle, Luxury*).

---

## 3. Texas Liability Insurance Closed Claims Data
- **Institusi/Penyusun:** Texas Department of Insurance (TDI)
- **Persistent DOI:** [https://doi.org/10.7910/DVN/HJIJLX](https://doi.org/10.7910/DVN/HJIJLX)
- **Lokasi Folder:** `data/raw/03_texas_liability_insurance/`
- **Berkas yang Tersedia:**
  - `CLOSED2000.csv` (Data klaim: 9.092 baris x 220 kolom)
  - `taccar2000_codebook.pdf` (Codebook panduan resmi klasifikasi klaim dan kode hukum)
- **Bidang:** *Actuarial Science, Financial Risk Management, Quantitative Loss Modeling*
- **Tantangan Data Cleaning (Kotor):**
  - Tingkat *missing values* sangat tinggi (38,86% atau 777.381 sel kosong), terjadi karena alur klaim bersyarat (*conditional reporting*—klaim yang selesai damai tidak mengisi instrumen litigasi pengadilan).
  - Variabel tanggal jamak (tanggal insiden, pelaporan, gugatan, disposisi) dalam string yang perlu dikonversi menjadi durasi waktu (*claim lag* & *settlement duration*).
  - Skewness ekstrem dan outlier nilai klaim ganti rugi (*indemnity payments*) serta biaya penasehat hukum (*defense attorney fees*).
  - Kode instrumen hukum dan klasifikasi cedera dalam kode numerik/kategorik diskrit yang memerlukan pemetaan codebook.
- **Potensi Proyek ML:**
  - **Regresi:** Estimasi total kerugian klaim asuransi (*Total Loss/Indemnity Prediction*).
  - **Klasifikasi:** Memprediksi risiko klaim berujung ke pengadilan (*Litigation vs Settlement*) atau deteksi klaim keparahan tinggi (*Catastrophic Loss*).

---

## 4. Classic Car Auction Sales & Pricing (France 2025)
- **Institusi/Penyusun:** Independent Academic Market Research
- **Persistent DOI:** [https://doi.org/10.7910/DVN/J4MYQJ](https://doi.org/10.7910/DVN/J4MYQJ)
- **Lokasi Folder:** `data/raw/04_classic_car_auction_2025/`
- **Berkas yang Tersedia:**
  - `classic_cars_sales_france_2025.tab` (Data lelang: 584 baris x 44 kolom)
- **Bidang:** *Market Analytics, Auction Theory, Luxury Asset Pricing & E-commerce*
- **Tantangan Data Cleaning (Kotor):**
  - Teks deskriptif asli berbahasa Prancis bercampur dengan atribut numerik.
  - Kolom estimasi harga berupa rentang string (*e.g., "15 000 - 20 000 €"*) yang memerlukan *regex parsing* untuk memisahkan batas bawah dan batas atas serta pembersihan simbol mata uang.
  - Terdapat lot lelang yang tidak terjual (*unsold lots/no bid*).
  - Missing values pada kolom odometer, spesifikasi mesin, dan tahun pembuatan yang tercampur dalam judul lot lelang.
- **Potensi Proyek ML:**
  - **Regresi:** Memprediksi harga ketok palu lelang (*Hammer Price / Adjudication*).
  - **Klasifikasi:** Memprediksi apakah kendaraan laku di atas batas estimasi kurator (*Sold Above High Estimate*).
  - **Text Feature Extraction:** Ekstraksi merk, model, dan kondisi dari deskripsi lelang.

---

## 5. South Korean Customer Satisfaction & Vehicle Reliability Survey (2024)
- **Institusi/Penyusun:** Consumer Insight Korea Automotive Research
- **Persistent DOI:** [https://doi.org/10.7910/DVN/OH8PKW](https://doi.org/10.7910/DVN/OH8PKW)
- **Lokasi Folder:** `data/raw/05_customer_satisfaction_korea_2024/`
- **Berkas yang Tersedia:**
  - `customer_satisfaction_raw_data.tab` (Data mentah: 21.626 baris x 21 kolom)
  - `codebook.xlsx` (Buku kode lengkap variabel survei dan arti nilai numerik)
  - `introduction.pdf` (Dokumen latar belakang metodologi survei nasional)
- **Bidang:** *Marketing Science, Customer Relationship Management (CRM), Behavioral Statistics*
- **Tantangan Data Cleaning (Kotor):**
  - Data mentah survei (*raw responses*) dengan persentase missing 17,86% akibat *skip patterns* (pertanyaan yang dilewati responden jika tidak relevan).
  - Nama variabel masih berupa kode kuesioner (`SQ03`, `Q010101`, dll.) yang perlu di-mapping menjadi nama variabel informatif berdasarkan `codebook.xlsx`.
  - Skala Likert bertingkat yang memerlukan standardisasi dan pengecekan inkonsistensi jawaban responden (*straight-lining*).
- **Potensi Proyek ML:**
  - **Klasifikasi:** Memprediksi loyalitas pelanggan / risiko berpindah merek (*Churn vs Retention*).
  - **Clustering:** Segmentasi profil kepuasan konsumen otomotif (*Customer Persona Profiling*).
  - **Regresi:** Memprediksi indeks kepuasan menyeluruh berdasarkan evaluasi produk dan layanan.
