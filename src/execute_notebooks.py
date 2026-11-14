"""
Skrip Eksekutor Headless Tiga Notebook: KingCounty-AVM
Menjalankan 01_eda.ipynb, 02_cleaning_preprocessing.ipynb, dan 03_modeling_evaluation.ipynb
secara berurutan menggunakan nbclient, merekam seluruh execution count, tabel HTML, dan gambar PNG permanen.
"""

import os
import sys
import time
import nbformat
from nbclient import NotebookClient

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NB_DIR = os.path.join(BASE_DIR, "notebooks")

NOTEBOOKS = [
    "01_eda.ipynb",
    "02_cleaning_preprocessing.ipynb",
    "03_modeling_evaluation.ipynb"
]

def execute_notebook(nb_filename):
    nb_path = os.path.join(NB_DIR, nb_filename)
    print(f"\n{'='*70}")
    print(f"🚀 Memulai Eksekusi Penuh Headless: {nb_filename}")
    print(f"{'='*70}")
    start_time = time.time()

    with open(nb_path, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    client = NotebookClient(
        nb,
        timeout=1200,
        kernel_name="kingcounty-venv",
        resources={"metadata": {"path": NB_DIR}}
    )

    try:
        client.execute()
    except Exception as e:
        print(f"❌ Error saat mengeksekusi {nb_filename}: {e}")
        raise e

    # Simpan kembali notebook dengan seluruh output permanen
    with open(nb_path, "w", encoding="utf-8") as f:
        nbformat.write(nb, f)

    elapsed = time.time() - start_time
    print(f"✅ Selesai mengeksekusi {nb_filename} dalam {elapsed:.2f} detik.")

    # Verifikasi Integritas Sel Kode & Output
    total_cells = len(nb.cells)
    code_cells = [c for c in nb.cells if c.cell_type == "code"]
    executed_cells = [c for c in code_cells if c.get("execution_count") is not None]
    cells_with_output = [c for c in code_cells if len(c.get("outputs", [])) > 0]

    print(f"   -> Total Sel           : {total_cells}")
    print(f"   -> Sel Kode            : {len(code_cells)}")
    print(f"   -> Sel Tereksekusi     : {len(executed_cells)} / {len(code_cells)}")
    print(f"   -> Sel Memiliki Output : {len(cells_with_output)} / {len(code_cells)}")

    for idx, c in enumerate(code_cells):
        ec = c.get("execution_count")
        out_types = [o.output_type for o in c.get("outputs", [])]
        has_png = any("image/png" in o.get("data", {}) for o in c.get("outputs", []) if o.output_type == "display_data")
        has_table = any("text/html" in o.get("data", {}) for o in c.get("outputs", []) if o.output_type in ["display_data", "execute_result"])
        
        info = []
        if has_png:
            info.append("📊 Grafik PNG")
        if has_table:
            info.append("📋 Tabel HTML/DataFrame")
        if any(o.output_type == "stream" for o in c.get("outputs", [])):
            info.append("📝 Output Teks/Stream")

        summary_str = ", ".join(info) if info else "Output terrekam"
        print(f"      Sel #{idx+1} [In {ec}]: {summary_str} ({len(c.get('outputs', []))} elemen output)")

    return nb

def main():
    print(f"Menjalankan otomatisasi eksekusi 3 Jupyter Notebook di direktori: {NB_DIR}")
    for nb_name in NOTEBOOKS:
        execute_notebook(nb_name)
    print(f"\n{'='*70}")
    print("🎉 SELURUH NOTEBOOK BERHASIL DIEKSEKUSI SECARA PENUH!")
    print(f"{'='*70}")

if __name__ == "__main__":
    main()
