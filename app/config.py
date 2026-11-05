"""
Modul Konfigurasi & Pemuatan Model Ter-Cache: KingCounty-AVM
Menangani pemuatan artefak serialisasi, dataset analitik, dan koordinat spasial.
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
    Memiliki mekanisme self-healing jika unpickle lintas versi scikit-learn gagal.
    """
    reg_path = os.path.join(MODELS_DIR, "best_valuation_model.joblib")
    clf_path = os.path.join(MODELS_DIR, "market_tier_classifier.joblib")
    meta_path = os.path.join(MODELS_DIR, "model_metadata.json")
    
    with open(meta_path, "r") as f:
        metadata = json.load(f)
        
    reg_model = None
    clf_model = None
    
    # 1. Coba muat model serialisasi biner
    try:
        reg_model = joblib.load(reg_path)
        clf_model = joblib.load(clf_path)
        dummy_sample = pd.DataFrame([metadata['feature_defaults']])[metadata['features']]
        reg_model.predict(dummy_sample)
        clf_model.predict(dummy_sample)
    except Exception:
        # Fallback otomatis on-the-fly jika ada perbedaan versi scikit-learn di Cloud
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

