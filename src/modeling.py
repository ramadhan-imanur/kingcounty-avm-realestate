"""
Modul Pelatihan, Evaluasi, dan Serialisasi Model: KingCounty-AVM
Melatih model Hedonic Regression, Market Tier Classifier, dan Unsupervised K-Means Micro-Market Clustering serta mengekspor artefak.
"""

import os
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
from .utils import save_fig

def assign_cluster_archetype(row):
    """
    Menetapkan label deskriptif mikro-pasar berdasarkan karakteristik harga median dan letak geografis.
    """
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

def train_kmeans_clustering(df, n_clusters=6, random_state=42, models_dir=None, figures_dir=None):
    """
    Melatih algoritma K-Means Clustering berbasis koordinat geospasial (Latitude, Longitude)
    dan nilai logaritmik harga ln(SalePrice) untuk membagi King County ke dalam 6 mikro-pasar.
    """
    print("\n--- 3. Pelatihan Model Unsupervised Learning: K-Means Micro-Market Clustering ---")
    base_dir = os.path.dirname(os.path.dirname(__file__))
    if models_dir is None:
        models_dir = os.path.join(base_dir, "models")
    if figures_dir is None:
        figures_dir = os.path.join(base_dir, "reports", "figures")
        
    os.makedirs(models_dir, exist_ok=True)
    os.makedirs(figures_dir, exist_ok=True)

    # 1. Ekstraksi Fitur Spasial dan Harga Logaritmik
    cluster_features = ['Latitude', 'Longitude']
    X_cluster = df[cluster_features].copy()
    X_cluster['LogPrice'] = np.log(df['SalePrice'])

    # 2. Standarisasi Fitur Menggunakan StandardScaler
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_cluster)

    # 3. Fitting Model K-Means (k=6)
    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)
    cluster_labels = kmeans.fit_predict(X_scaled)
    df_clustered = df.copy()
    df_clustered['Cluster'] = cluster_labels

    # 4. Perhitungan Metrik Evaluasi Unsupervised Learning
    inertia_val = float(kmeans.inertia_)
    sample_size = min(5000, len(df))
    sample_idx = np.random.RandomState(random_state).choice(len(df), size=sample_size, replace=False)
    sil_val = float(silhouette_score(X_scaled[sample_idx], cluster_labels[sample_idx]))
    ch_val = float(calinski_harabasz_score(X_scaled, cluster_labels))
    db_val = float(davies_bouldin_score(X_scaled, cluster_labels))

    print(f"Hasil Evaluasi Klastering (k={n_clusters}):")
    print(f"  -> Inertia (WCSS)        : {inertia_val:,.2f}")
    print(f"  -> Silhouette Score (5k) : {sil_val:.4f}")
    print(f"  -> Calinski-Harabasz     : {ch_val:,.2f}")
    print(f"  -> Davies-Bouldin Index  : {db_val:.4f}")

    # 5. Profiling 6 Mikro-Pasar Properti
    summary = df_clustered.groupby('Cluster').agg(
        Jumlah_Properti=('SalePrice', 'count'),
        Persentase_Pasar=('SalePrice', lambda x: len(x) / len(df) * 100),
        Median_Harga=('SalePrice', 'median'),
        Mean_Harga=('SalePrice', 'mean'),
        Median_SqFtLiving=('SqFtTotLiving', 'median'),
        Median_BldgGrade=('BldgGrade', 'median'),
        Rata_Latitude=('Latitude', 'mean'),
        Rata_Longitude=('Longitude', 'mean')
    ).reset_index()

    summary['Profil_Mikro_Pasar'] = summary.apply(assign_cluster_archetype, axis=1)
    summary = summary.sort_values(by='Median_Harga').reset_index(drop=True)

    cluster_profiles = []
    for _, row in summary.iterrows():
        cluster_profiles.append({
            'cluster_id': int(row['Cluster']),
            'archetype': str(row['Profil_Mikro_Pasar']),
            'property_count': int(row['Jumlah_Properti']),
            'market_share_pct': round(float(row['Persentase_Pasar']), 2),
            'median_price': float(row['Median_Harga']),
            'mean_price': float(row['Mean_Harga']),
            'median_sqft_living': float(row['Median_SqFtLiving']),
            'median_grade': float(row['Median_BldgGrade']),
            'centroid_lat': round(float(row['Rata_Latitude']), 5),
            'centroid_lon': round(float(row['Rata_Longitude']), 5)
        })

    # 6. Visualisasi Evaluasi Spasial & Distribusi Harga Klaster
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    palette = sns.color_palette("tab10", n_colors=n_clusters)

    # Plot 1: Sebaran Spasial dan Centroid
    sns.scatterplot(
        data=df_clustered,
        x='Longitude',
        y='Latitude',
        hue='Cluster',
        palette=palette,
        alpha=0.35,
        s=15,
        ax=axes[0],
        legend='full'
    )
    centers_orig = scaler.inverse_transform(kmeans.cluster_centers_)
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
    axes[0].set_title("Peta Sebaran 6 Klaster Mikro-Pasar Properti King County", fontsize=12, fontweight='bold')
    axes[0].set_xlabel("Longitude (WGS84)", fontsize=11)
    axes[0].set_ylabel("Latitude (WGS84)", fontsize=11)
    axes[0].legend(title="Cluster ID", loc="lower left", fontsize=9)

    # Plot 2: Boxplot Distribusi Harga per Klaster
    sns.boxplot(
        data=df_clustered,
        x='Cluster',
        y=df_clustered['SalePrice'] / 1000,
        palette=palette,
        ax=axes[1],
        showfliers=False
    )
    axes[1].set_title("Distribusi Harga Properti per Klaster Mikro-Pasar ($1,000 USD)", fontsize=12, fontweight='bold')
    axes[1].set_xlabel("Cluster ID", fontsize=11)
    axes[1].set_ylabel("Harga Jual ($1,000)", fontsize=11)

    plt.tight_layout()
    save_fig("micro_market_clusters")
    plt.close()

    # 7. Serialisasi Model Klastering
    kmeans_bundle = {
        'model': kmeans,
        'scaler': scaler,
        'features': ['Latitude', 'Longitude', 'LogPrice'],
        'n_clusters': n_clusters,
        'cluster_profiles': cluster_profiles,
        'metrics': {
            'inertia': inertia_val,
            'silhouette': sil_val,
            'calinski_harabasz': ch_val,
            'davies_bouldin': db_val
        }
    }
    kmeans_path = os.path.join(models_dir, "kmeans_cluster_model.joblib")
    joblib.dump(kmeans_bundle, kmeans_path)
    print(f"Model K-Means Clustering tersimpan ke: {kmeans_path}")

    return kmeans_bundle, df_clustered

def find_cluster_comparables(df, target_lat, target_lon, target_price, kmeans_bundle=None, n_comps=5):
    """
    Menemukan properti pembanding terbaik (Comps) di dalam klaster mikro-pasar yang sama.
    """
    if kmeans_bundle is None:
        base_dir = os.path.dirname(os.path.dirname(__file__))
        kmeans_bundle = joblib.load(os.path.join(base_dir, "models", "kmeans_cluster_model.joblib"))
        
    scaler = kmeans_bundle['scaler']
    kmeans = kmeans_bundle['model']
    
    target_vec = np.array([[target_lat, target_lon, np.log(target_price)]])
    target_scaled = scaler.transform(target_vec)
    target_cluster = int(kmeans.predict(target_scaled)[0])
    
    # Filter kandidat properti pada klaster yang sama
    if 'Cluster' not in df.columns:
        pool_vecs = df[['Latitude', 'Longitude']].copy()
        pool_vecs['LogPrice'] = np.log(df['SalePrice'])
        df['Cluster'] = kmeans.predict(scaler.transform(pool_vecs))
        
    cluster_pool = df[df['Cluster'] == target_cluster].copy()
    pool_vecs = cluster_pool[['Latitude', 'Longitude']].copy()
    pool_vecs['LogPrice'] = np.log(cluster_pool['SalePrice'])
    pool_scaled = scaler.transform(pool_vecs)
    
    dists = np.linalg.norm(pool_scaled - target_scaled, axis=1)
    cluster_pool['DistanceScore'] = dists
    cluster_pool['MatchScore'] = np.clip(100 * (1 - dists / (dists.max() + 1e-6)), 70, 99.9).round(1)
    
    comps = cluster_pool.sort_values(by='DistanceScore').head(n_comps)
    return target_cluster, comps

def run_modeling_pipeline(clean_data_path, models_dir=None, figures_dir=None):
    """
    Menjalankan pelatihan model regresi, klasifikasi, dan unsupervised K-Means secara menyeluruh.
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

    # 2. Benchmarking Model Regresi (7 Model Komparatif Sesuai Standar Akademik & Industri)
    print("\n--- 1. Pelatihan & Benchmarking Model Regresi Hedonik (AVM) ---")
    reg_models = {
        'OLS Linear Regression': LinearRegression(),
        'Ridge Regression (L2)': Ridge(alpha=10.0),
        'Lasso Regression (L1)': Lasso(alpha=0.0005, max_iter=3000, random_state=42),
        'Elastic Net Regression': ElasticNet(alpha=0.0005, l1_ratio=0.5, max_iter=3000, random_state=42),
        'Decision Tree Regressor': DecisionTreeRegressor(max_depth=12, min_samples_leaf=10, random_state=42),
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

    # 3. Pelatihan Model Klasifikasi Tier Properti (Multi-Model Benchmarking)
    print("\n--- 2. Pelatihan & Benchmarking Model Klasifikasi Tier Properti ---")
    clf_models = {
        'Decision Tree Classifier': DecisionTreeClassifier(max_depth=10, random_state=42),
        'Random Forest Classifier': RandomForestClassifier(n_estimators=100, max_depth=12, n_jobs=-1, random_state=42),
        'HistGradientBoosting Classifier': HistGradientBoostingClassifier(max_iter=150, learning_rate=0.08, random_state=42)
    }

    clf_results = {}
    best_f1 = -1
    best_clf_model = None
    best_clf_name = ""

    for name, clf_cand in clf_models.items():
        print(f"Melatih {name}...")
        clf_cand.fit(X_train, ytier_train)
        preds = clf_cand.predict(X_test)
        acc = float(accuracy_score(ytier_test, preds))
        f1 = float(f1_score(ytier_test, preds, average='macro'))
        clf_results[name] = {
            'accuracy': round(acc * 100, 2),
            'macro_f1': round(f1, 4)
        }
        print(f"  -> Akurasi: {acc*100:.2f}% | Macro F1-Score: {f1:.4f}")
        if f1 > best_f1:
            best_f1 = f1
            best_clf_model = clf_cand
            best_clf_name = name

    clf = best_clf_model
    tier_preds = clf.predict(X_test)
    clf_acc = float(accuracy_score(ytier_test, tier_preds))
    clf_f1 = float(f1_score(ytier_test, tier_preds, average='macro'))
    print(f"\nModel Klasifikasi Terbaik: {best_clf_name} (Akurasi: {clf_acc*100:.2f}%, Macro F1: {clf_f1:.4f})")

    # 4. Pelatihan Unsupervised Learning (K-Means 6 Klaster Mikro Pasar)
    kmeans_bundle, df_clustered = train_kmeans_clustering(
        df=df,
        n_clusters=6,
        random_state=42,
        models_dir=models_dir,
        figures_dir=figures_dir
    )

    # 5. Feature Importance (Permutation Importance)
    print("\nMenghitung bobot fitur (Feature Importance) menggunakan Permutation Importance...")
    perm_importance = permutation_importance(
        best_reg_model, X_test, ylog_test, n_repeats=5, random_state=42, n_jobs=-1
    )
    feature_importance_dict = dict(zip(feature_cols, [round(float(v), 5) for v in perm_importance.importances_mean]))
    sorted_features = sorted(feature_importance_dict.items(), key=lambda x: x[1], reverse=True)

    # 6. Visualisasi Hasil Evaluasi ke reports/figures/
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
    ax.barh(top_names[::-1], top_scores[::-1], color="#3366cc")
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

    # 7. Serialisasi Model & Metadata
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
            'best_model': best_clf_name,
            'accuracy': round(clf_acc * 100, 2),
            'macro_f1': round(clf_f1, 4),
            'models_comparison': clf_results
        },
        'unsupervised_learning': {
            'algorithm': 'K-Means Clustering',
            'n_clusters': 6,
            'features': ['Latitude', 'Longitude', 'LogPrice'],
            'metrics': kmeans_bundle['metrics'],
            'cluster_profiles': kmeans_bundle['cluster_profiles']
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

    print("Pipeline pemodelan (Supervised & Unsupervised) berhasil dijalankan 100%!")
    return metadata

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(__file__))
    clean_csv = os.path.join(base_dir, "data", "processed", "king_county_clean.csv")
    run_modeling_pipeline(clean_csv)
