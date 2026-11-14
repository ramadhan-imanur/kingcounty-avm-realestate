"""
Modul Konfigurasi & Pemuatan Model Ter-Cache: KingCounty-AVM
Menangani pemuatan artefak serialisasi, dataset analitik, K-Means clustering, dan koordinat spasial.
"""

import os
import json
import joblib
import pandas as pd
import numpy as np
import streamlit as st

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")
DATA_DIR = os.path.join(BASE_DIR, "data", "processed")

@st.cache_resource
def load_models_and_metadata():
    """
    Memuat model regresi, classifier tier, dan metadata.
    Memiliki mekanisme fallback otomatis jika unpickle lintas versi scikit-learn gagal.
    """
    reg_path = os.path.join(MODELS_DIR, "best_valuation_model.joblib")
    clf_path = os.path.join(MODELS_DIR, "market_tier_classifier.joblib")
    meta_path = os.path.join(MODELS_DIR, "model_metadata.json")
    
    with open(meta_path, "r", encoding="utf-8") as f:
        metadata = json.load(f)
        
    reg_model = None
    clf_model = None
    
    try:
        reg_model = joblib.load(reg_path)
        clf_model = joblib.load(clf_path)
        dummy_sample = pd.DataFrame([metadata['feature_defaults']])[metadata['features']]
        reg_model.predict(dummy_sample)
        clf_model.predict(dummy_sample)
    except Exception:
        from sklearn.ensemble import HistGradientBoostingRegressor, HistGradientBoostingClassifier
        data_clean_path = os.path.join(DATA_DIR, "king_county_clean.csv")
        df_train = pd.read_csv(data_clean_path, low_memory=False)
        
        features = metadata["features"]
        X = df_train[features]
        y_log = np.log(df_train["SalePrice"])
        y_tier = df_train["PropertyTier"]
        
        reg_model = HistGradientBoostingRegressor(max_iter=250, learning_rate=0.08, random_state=42)
        reg_model.fit(X, y_log)
        
        clf_model = HistGradientBoostingClassifier(max_iter=150, learning_rate=0.08, random_state=42)
        clf_model.fit(X, y_tier)
        
        try:
            joblib.dump(reg_model, reg_path)
            joblib.dump(clf_model, clf_path)
        except Exception:
            pass
        
    return reg_model, clf_model, metadata

@st.cache_resource
def load_kmeans_data():
    """
    Memuat artefak K-Means micro-market clustering.
    """
    kmeans_path = os.path.join(MODELS_DIR, "kmeans_cluster_model.joblib")
    if os.path.exists(kmeans_path):
        try:
            return joblib.load(kmeans_path)
        except Exception:
            return None
    return None

def assign_kmeans_cluster(kmeans_data, lat, lon, price):
    """
    Menentukan klaster mikro-pasar spasial berdasarkan Latitude, Longitude, dan LogPrice.
    """
    if not kmeans_data or 'model' not in kmeans_data or 'scaler' not in kmeans_data:
        return 0, "Klaster Geospasial Standar"
    try:
        scaler = kmeans_data['scaler']
        model = kmeans_data['model']
        log_price = float(np.log(max(10000.0, float(price))))
        df_feat = pd.DataFrame([[lat, lon, log_price]], columns=['Latitude', 'Longitude', 'LogPrice'])
        scaled_feat = scaler.transform(df_feat)
        cluster_id = int(model.predict(scaled_feat)[0])
        profiles = kmeans_data.get('cluster_profiles', [])
        profile = next((p for p in profiles if p.get('Cluster') == cluster_id), None)
        archetype = profile.get('Profil_Mikro_Pasar', f'Klaster {cluster_id}') if profile else f'Klaster {cluster_id}'
        return cluster_id, archetype
    except Exception:
        return 0, "Klaster Geospasial Standar"

@st.cache_data
def load_clean_data_sample():
    """
    Memuat dataset analitik bersih King County Real Estate.
    """
    clean_csv_path = os.path.join(DATA_DIR, "king_county_clean.csv")
    df = pd.read_csv(clean_csv_path, low_memory=False)
    return df

def get_zip_coordinates(df):
    """
    Mengekstrak koordinat spasial representatif (median Lat/Lon) per ZipCode.
    """
    coords = df.groupby('ZipCode')[['Latitude', 'Longitude']].median().to_dict(orient='index')
    all_zips = sorted([str(z) for z in coords.keys()])
    return coords, all_zips
