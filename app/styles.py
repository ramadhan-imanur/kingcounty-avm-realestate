"""
Styling Ringan & Non-Intrusif: KingCounty-AVM
Menjaga tampilan tetap sederhana, bersih, dan menggunakan tema default Streamlit agar tetap ringan.
"""

AERIS_CSS = """
<style>
/* Pengaturan container utama agar nyaman di layar lebar */
.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 2.5rem !important;
    max-width: 1400px !important;
}

/* Badge status yang elegan dan adaptif */
.badge-pill {
    display: inline-block;
    padding: 0.25rem 0.65rem;
    font-size: 0.75rem;
    font-weight: 600;
    border-radius: 9999px;
    margin-right: 0.5rem;
}
.badge-emerald {
    background-color: rgba(5, 150, 105, 0.12);
    color: #059669;
    border: 1px solid rgba(5, 150, 105, 0.3);
}
.badge-sky {
    background-color: rgba(2, 132, 199, 0.12);
    color: #0284c7;
    border: 1px solid rgba(2, 132, 199, 0.3);
}
.badge-purple {
    background-color: rgba(124, 58, 237, 0.12);
    color: #7c3aed;
    border: 1px solid rgba(124, 58, 237, 0.3);
}

/* Sedikit padding pada kartu container */
[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 12px;
}
</style>
"""
