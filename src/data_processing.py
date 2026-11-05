"""
Modul Pipeline Pembersihan & Rekayasa Fitur: KingCounty-AVM
Mengolah data mentah cleansales.tab menjadi king_county_clean.csv.
"""

import os
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from .utils import wa_north_to_latlon

def clean_and_process_data(raw_path, output_path=None):
    """
    Menjalankan alur pembersihan dan transformasi data King County Real Estate.
    """
    print(f"Memuat data mentah dari: {raw_path}...")
    df = pd.read_csv(raw_path, sep='\t', low_memory=False)
    initial_rows = len(df)
    print(f"Data awal dimuat: {initial_rows:,} baris, {df.shape[1]} kolom.")

    # 1. Filter Transaksi Non-Pasar / Nilai Ekstrem Rendah
    df = df[df['SalePrice'] >= 50000].copy()
    print(f"Menyaring transaksi non-pasar (SalePrice >= $50,000): {len(df):,} baris tersisa.")

    # 2. Pembersihan Trailing Whitespaces pada Kolom Teks
    text_cols = df.select_dtypes(include=['object']).columns
    for col in text_cols:
        df[col] = df[col].astype(str).str.strip()

    # 3. Imputasi Spasial untuk Missing ZipCode menggunakan KNN
    missing_zip_mask = df['ZipCode'].isnull() | (df['ZipCode'] == 'nan') | (df['ZipCode'] == '')
    known_zip = df[~missing_zip_mask].copy()
    known_zip['ZipClean'] = known_zip['ZipCode'].str[:5]
    
    if missing_zip_mask.sum() > 0:
        print(f"Melakukan imputasi spasial KNN untuk {missing_zip_mask.sum():,} baris ZipCode kosong...")
        knn = KNeighborsClassifier(n_neighbors=3, weights='distance')
        knn.fit(known_zip[['X', 'Y']], known_zip['ZipClean'])
        imputed_zips = knn.predict(df.loc[missing_zip_mask, ['X', 'Y']])
        df.loc[missing_zip_mask, 'ZipCode'] = imputed_zips
    
    df['ZipCode'] = df['ZipCode'].astype(str).str[:5]

    # 4. Konversi Koordinat Spasial ke Latitude & Longitude WGS84
    print("Mengonversi koordinat spasial WA North ke Latitude dan Longitude WGS84...")
    lats, lons = [], []
    for x_val, y_val in zip(df['X'], df['Y']):
        lat, lon = wa_north_to_latlon(x_val, y_val)
        lats.append(round(lat, 5))
        lons.append(round(lon, 5))
    df['Latitude'] = lats
    df['Longitude'] = lons

    # 5. Rekayasa Fitur Domain (Feature Engineering)
    print("Menghitung fitur turunan ekonometrika real estat...")
    # Usia properti saat terjual
    df['PropertyAge'] = np.maximum(0, df['salesYear'] - df['YrBuilt'])
    
    # Status renovasi
    df['IsRenovated'] = (df['YrRenovated'] > 0).astype(int)
    df['YearsSinceRenovation'] = np.where(
        df['YrRenovated'] > 0, 
        np.maximum(0, df['salesYear'] - df['YrRenovated']), 
        df['PropertyAge']
    )

    # Total kamar mandi tertimbang
    df['TotalBaths'] = (
        df['BathFullCount'] + 
        0.75 * df['Bath3qtrCount'] + 
        0.5 * df['BathHalfCount']
    )

    # Indikator pemandangan (Panorama Views)
    df['HasView'] = (
        (df['SeattleSkyline'] > 0) | 
        (df['LakeWashington'] > 0) | 
        (df['LakeSammamish'] > 0) | 
        (df['PugetSound'] > 0) | 
        (df['MtRainier'] > 0)
    ).astype(int)

    # Indikator Waterfront
    df['IsWaterfront'] = (df['WfntLocation'] > 0).astype(int)

    # Harga per satuan luas
    df['PricePerSqFt'] = df['SalePrice'] / np.maximum(1, df['SqFtTotLiving'])

    # Segmentasi Tier Pasar (Target Klasifikasi)
    df['PropertyTier'] = pd.cut(
        df['SalePrice'],
        bins=[-np.inf, 350000, 700000, np.inf],
        labels=['Entry-Level', 'Mid-Market', 'Luxury']
    )

    # 6. Seleksi Kolom Terpilih (Menyusutkan 147 kolom menjadi fitur esensial)
    selected_columns = [
        # Target
        'SalePrice', 'PropertyTier',
        # Dimensi Fisik
        'SqFtTotLiving', 'SqFtLot', 'Bedrooms', 'TotalBaths',
        'BathFullCount', 'BathHalfCount', 'Bath3qtrCount',
        'Stories', 'SqFtTotBasement', 'SqFtFinBasement', 'SqFtGarageAttached',
        # Kualitas & Usia
        'BldgGrade', 'Condition', 'YrBuilt', 'YrRenovated',
        'PropertyAge', 'IsRenovated', 'YearsSinceRenovation',
        # Lokasi & Spasial
        'ZipCode', 'X', 'Y', 'Latitude', 'Longitude', 'DistrictName',
        # Pemandangan & Lingkungan
        'IsWaterfront', 'HasView', 'SeattleSkyline', 'LakeWashington',
        'LakeSammamish', 'PugetSound', 'MtRainier',
        'TrafficNoise', 'AirportNoise',
        # Transaksi & Taksiran Pajak
        'LandVal', 'ImpsVal', 'PricePerSqFt', 'DocumentDate', 'salesYear'
    ]
    
    clean_df = df[selected_columns].copy()
    
    # Drop duplicates if any
    clean_df = clean_df.drop_duplicates().reset_index(drop=True)
    
    print(f"Pembersihan selesai: {len(clean_df):,} baris x {clean_df.shape[1]} kolom.")

    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        clean_df.to_csv(output_path, index=False)
        print(f"Data bersih berhasil disimpan ke: {output_path}")

    return clean_df

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(__file__))
    raw_file = os.path.join(base_dir, "data", "raw", "02_king_county_real_estate", "cleansales.tab")
    out_file = os.path.join(base_dir, "data", "processed", "king_county_clean.csv")
    clean_and_process_data(raw_file, out_file)

