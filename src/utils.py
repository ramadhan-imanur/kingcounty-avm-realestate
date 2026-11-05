"""
Modul Utilitas Pendukung Proyek Data Sains 2026: KingCounty-AVM
Fungsi-fungsi reusable untuk penyimpanan visualisasi, konversi koordinat spasial, dan pemformatan.
"""

import os
import math
import matplotlib.pyplot as plt

def save_fig(fig_id, tight_layout=True, fig_extension="png", resolution=300):
    """
    Menyimpan objek figure matplotlib ke folder reports/figures/.
    """
    figures_dir = os.path.join(os.path.dirname(__file__), "..", "reports", "figures")
    os.makedirs(figures_dir, exist_ok=True)
    path = os.path.join(figures_dir, f"{fig_id}.{fig_extension}")
    if tight_layout:
        plt.tight_layout()
    plt.savefig(path, format=fig_extension, dpi=resolution)
    print(f"Grafik berhasil disimpan ke: {path}")

def wa_north_to_latlon(x_ft, y_ft):
    """
    Mengonversi koordinat Washington State Plane North (EPSG:2926 / NAD83 ftUS)
    ke Latitude dan Longitude WGS84 (derajat desimal).
    Formula Lambert Conformal Conic 2-Paralel Standar.
    """
    to_meters = 1200.0 / 3937.0
    x_m = x_ft * to_meters
    y_m = y_ft * to_meters
    
    a = 6378137.0  # WGS84 semi-major axis (meter)
    f = 1.0 / 298.257222101
    e = math.sqrt(2 * f - f * f)
    
    phi1 = math.radians(47.5)
    phi2 = math.radians(48.733333333333333)
    phi0 = math.radians(47.0)
    lam0 = math.radians(-120.833333333333333)
    x0 = 500000.0  # False Easting (meter)
    y0 = 0.0       # False Northing (meter)
    
    def m_func(phi):
        return math.cos(phi) / math.sqrt(1 - e**2 * math.sin(phi)**2)
    def t_func(phi):
        return math.tan(math.pi / 4 - phi / 2) / ((1 - e * math.sin(phi)) / (1 + e * math.sin(phi)))**(e / 2)
        
    m1 = m_func(phi1)
    m2 = m_func(phi2)
    t1 = t_func(phi1)
    t2 = t_func(phi2)
    t0 = t_func(phi0)
    
    n = (math.log(m1) - math.log(m2)) / (math.log(t1) - math.log(t2))
    F = m1 / (n * t1**n)
    rho0 = a * F * t0**n
    
    x_rel = x_m - x0
    y_rel = y_m - y0
    
    rho = math.hypot(x_rel, rho0 - y_rel)
    theta = math.atan2(x_rel, rho0 - y_rel)
    
    t = (rho / (a * F))**(1 / n)
    
    phi = math.pi / 2 - 2 * math.atan(t)
    for _ in range(5):
        con = e * math.sin(phi)
        phi = math.pi / 2 - 2 * math.atan(t * ((1 - con) / (1 + con))**(e / 2))
        
    lam = lam0 + theta / n
    return math.degrees(phi), math.degrees(lam)

def format_currency(val):
    """
    Format angka numerik ke format dolar ($).
    """
    return f"${val:,.0f}"
