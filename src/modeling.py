"""
Modul Pelatihan, Evaluasi, dan Serialisasi Model: KingCounty-AVM
Melatih model Hedonic Regression dan Market Tier Classifier serta mengekspor artefak.
"""

import os
import json
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import HistGradientBoostingRegressor, HistGradientBoostingClassifier, RandomForestRegressor
from sklearn.metrics import (
    r2_score, mean_squared_error, mean_absolute_error, 
    mean_absolute_percentage_error, accuracy_score, f1_score, confusion_matrix
)
from sklearn.inspection import permutation_importance
from .utils import save_fig

def run_modeling_pipeline(clean_data_path, models_dir=None, figures_dir=None):
    """
    Menjalankan pelatihan model regresi dan klasifikasi secara menyeluruh.
    """
    base_dir = os.path.dirname(os.path.dirname(__file__))
    if models_dir is None:
        models_dir = os.path.join(base_dir, "models")
    if figures_dir is None:
        figures_dir = os.path.join(base_dir, "reports", "figures")
        
    os.makedirs(models_dir, exist_ok=True)
    os.makedirs(figures_dir, exist_ok=True)

    print(f"Memuat data bersih dari: {clean_data_path}...")
    df = pd.read_csv(clean_data_path, low_memory=False)

    feature_cols = [
        'SqFtTotLiving', 'SqFtLot', 'Bedrooms', 'TotalBaths', 'Stories',
        'SqFtTotBasement', 'SqFtGarageAttached', 'BldgGrade', 'Condition',
        'PropertyAge', 'IsRenovated', 'Latitude', 'Longitude',
        'IsWaterfront', 'HasView', 'TrafficNoise', 'AirportNoise', 'salesYear'
    ]

    X = df[feature_cols].copy()
    y_price = df['SalePrice']
    y_log = np.log(y_price)
    y_tier = df['PropertyTier']

    # 1. Train-Test Split (80/20)
    X_train, X_test, y_train, y_test, ylog_train, ylog_test, ytier_train, ytier_test = train_test_split(
        X, y_price, y_log, y_tier, test_size=0.20, random_state=42, stratify=y_tier
    )
    print(f"Dataset dibagi: Train={len(X_train):,} baris, Test={len(X_test):,} baris.")

    # 2. Benchmarking Model Regresi
    print("\n--- 1. Pelatihan Model Regresi Hedonik (AVM) ---")
    reg_models = {
        'OLS Linear Regression': LinearRegression(),
        'Ridge Regression (L2)': Ridge(alpha=10.0),
        'Random Forest Regressor': RandomForestRegressor(n_estimators=100, max_depth=14, n_jobs=-1, random_state=42),
        'HistGradientBoosting Regressor': HistGradientBoostingRegressor(max_iter=250, learning_rate=0.08, random_state=42)
    }

    reg_results = {}
    best_r2 = -1
    best_reg_model = None
    best_reg_name = ""

    for name, model in reg_models.items():
        print(f"Melatih {name}...")
        model.fit(X_train, ylog_train)
        pred_log = model.predict(X_test)
        pred_dollars = np.exp(pred_log)

        r2 = float(r2_score(ylog_test, pred_log))
        rmse_log = float(np.sqrt(mean_squared_error(ylog_test, pred_log)))
        mape = float(mean_absolute_percentage_error(y_test, pred_dollars))
        mae = float(mean_absolute_error(y_test, pred_dollars))

        reg_results[name] = {
            'R2_log': round(r2, 4),
            'RMSE_log': round(rmse_log, 4),
            'MAPE': round(mape * 100, 2),
            'MAE_dollars': round(mae, 0)
        }
        print(f"  -> R2(log): {r2:.4f} | RMSE(log): {rmse_log:.4f} | MAPE: {mape*100:.2f}% | MAE: ${mae:,.0f}")

        if r2 > best_r2:
            best_r2 = r2
            best_reg_model = model
            best_reg_name = name

    print(f"\nModel Regresi Terbaik: {best_reg_name} dengan R2 = {best_r2:.4f}")

    # 3. Pelatihan Model Klasifikasi Tier Properti
    print("\n--- 2. Pelatihan Model Klasifikasi Tier Properti ---")
    clf = HistGradientBoostingClassifier(max_iter=150, learning_rate=0.08, random_state=42)
    clf.fit(X_train, ytier_train)
    tier_preds = clf.predict(X_test)

    clf_acc = float(accuracy_score(ytier_test, tier_preds))
    clf_f1 = float(f1_score(ytier_test, tier_preds, average='macro'))
    print(f"Akurasi Klasifikasi: {clf_acc*100:.2f}% | Macro F1-Score: {clf_f1:.4f}")

    # 4. Feature Importance (Permutation Importance)
    print("\nMenghitung bobot fitur (Feature Importance) menggunakan Permutation Importance...")
    perm_importance = permutation_importance(
        best_reg_model, X_test, ylog_test, n_repeats=5, random_state=42, n_jobs=-1
    )
    feature_importance_dict = dict(zip(feature_cols, [round(float(v), 5) for v in perm_importance.importances_mean]))
    sorted_features = sorted(feature_importance_dict.items(), key=lambda x: x[1], reverse=True)

    # 5. Visualisasi Hasil Evaluasi ke reports/figures/
    print("\nMenghasilkan grafik visualisasi evaluasi...")
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')

    # Plot 1: Actual vs Predicted
    pred_best_dollars = np.exp(best_reg_model.predict(X_test))
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(y_test / 1000, pred_best_dollars / 1000, alpha=0.25, color="#1f77b4", s=20)
    max_val = max(y_test.max(), pred_best_dollars.max()) / 1000
    ax.plot([0, max_val], [0, max_val], 'r--', lw=2, label="Garis Ideal (y = x)")
    ax.set_title("Evaluasi Nilai Aktual vs Prediksi Model AVM (dalam Ribuan USD)", fontsize=13, fontweight='bold')
    ax.set_xlabel("Harga Aktual Transaksi ($1,000)", fontsize=11)
    ax.set_ylabel("Harga Prediksi Model ($1,000)", fontsize=11)
    ax.legend()
    save_fig("actual_vs_predicted")
    plt.close()

    # Plot 2: Residual Distribution
    residuals = ylog_test - best_reg_model.predict(X_test)
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(residuals, kde=True, color="#2ca02c", ax=ax, bins=50)
    ax.set_title(f"Distribusi Residual Logaritma ({best_reg_name})", fontsize=13, fontweight='bold')
    ax.set_xlabel("Residual (Log Actual - Log Pred)", fontsize=11)
    ax.set_ylabel("Frekuensi", fontsize=11)
    save_fig("residuals_distribution")
    plt.close()

    # Plot 3: Feature Importance Bar Plot
    top_10 = sorted_features[:10]
    top_names = [x[0] for x in top_10]
    top_scores = [x[1] for x in top_10]
    fig, ax = plt.subplots(figsize=(9, 6))
    bars = ax.barh(top_names[::-1], top_scores[::-1], color="#3366cc")
    ax.set_title("10 Fitur Paling Berpengaruh terhadap Nilai Properti (Permutation Importance)", fontsize=13, fontweight='bold')
    ax.set_xlabel("Penurunan R2 saat Fitur Diacak", fontsize=11)
    save_fig("feature_importance")
    plt.close()

    # Plot 4: Confusion Matrix Tiering
    cm = confusion_matrix(ytier_test, tier_preds, labels=['Entry-Level', 'Mid-Market', 'Luxury'])
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=['Entry', 'Mid', 'Luxury'], 
                yticklabels=['Entry', 'Mid', 'Luxury'], ax=ax)
    ax.set_title("Confusion Matrix Klasifikasi Tier Properti", fontsize=13, fontweight='bold')
    ax.set_xlabel("Prediksi Model", fontsize=11)
    ax.set_ylabel("Kelas Aktual", fontsize=11)
    save_fig("confusion_matrix_tiers")
    plt.close()

    # 6. Serialisasi Model & Metadata
    reg_path = os.path.join(models_dir, "best_valuation_model.joblib")
    clf_path = os.path.join(models_dir, "market_tier_classifier.joblib")
    meta_path = os.path.join(models_dir, "model_metadata.json")

    print(f"\nMenyimpan model ke {models_dir}...")
    joblib.dump(best_reg_model, reg_path)
    joblib.dump(clf, clf_path)

    # Hitung nilai median per fitur dan per ZipCode untuk nilai default form
    feature_defaults = {}
    for col in feature_cols:
        feature_defaults[col] = float(df[col].median())

    zip_price_medians = df.groupby('ZipCode')['SalePrice'].median().to_dict()
    zip_price_medians = {str(k): float(v) for k, v in zip_price_medians.items()}

    metadata = {
        'model_name': best_reg_name,
        'features': feature_cols,
        'target': 'SalePrice',
        'target_transform': 'log',
        'metrics_regression': reg_results,
        'metrics_classification': {
            'accuracy': round(clf_acc * 100, 2),
            'macro_f1': round(clf_f1, 4)
        },
        'feature_importance_ranked': sorted_features,
        'feature_defaults': feature_defaults,
        'zip_price_medians': zip_price_medians,
        'tiers': ['Entry-Level', 'Mid-Market', 'Luxury'],
        'train_samples': len(X_train),
        'test_samples': len(X_test)
    }

    with open(meta_path, 'w') as f:
        json.dump(metadata, f, indent=2)

    print("Pipeline pemodelan berhasil dijalankan 100%!")
    return metadata

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(__file__))
    clean_csv = os.path.join(base_dir, "data", "processed", "king_county_clean.csv")
    run_modeling_pipeline(clean_csv)

