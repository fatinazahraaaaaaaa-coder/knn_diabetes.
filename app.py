from pathlib import Path
import pandas as pd
import streamlit as st
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from collections import Counter

st.set_page_config(page_title="SPK KNN - Data Mining KKN", page_icon="📊", layout="wide")
st.title("📊 Sistem Pendukung Keputusan — Metode K-Nearest Neighbors (KNN)")
st.caption("Aplikasi pembelajaran untuk klasifikasi berdasarkan dataset Excel. Bukan alat diagnosis medis.")

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "Data_Mining_KKN.xlsx"
FEATURES = ["Usia", "BMI", "Glukosa", "Tekanan Darah", "Riwayat Keluarga"]
TARGET = "Kelas"

@st.cache_data
def load_dataset(uploaded_file=None):
    # Excel tugas memiliki judul di beberapa baris pertama; cari baris header berdasarkan kolom Pasien.
    source = uploaded_file if uploaded_file is not None else DATA_FILE
    raw = pd.read_excel(source, header=None)
    header_idx = None
    for i in range(min(len(raw), 15)):
        vals = [str(v).strip().lower() for v in raw.iloc[i].tolist()]
        if "pasien" in vals and "usia" in vals and "kelas" in vals:
            header_idx = i
            break
    if header_idx is None:
        # fallback untuk Excel yang sudah berbentuk tabel biasa
        df = pd.read_excel(source)
    else:
        df = pd.read_excel(source, header=header_idx)
    df.columns = [str(c).strip() for c in df.columns]
    # Hilangkan kolom kosong/Unnamed
    df = df.loc[:, [not c.lower().startswith("unnamed") and c.lower() != "nan" for c in df.columns]]
    required = ["Pasien"] + FEATURES + [TARGET]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError("Kolom tidak ditemukan: " + ", ".join(missing))
    df = df[required].copy()
    # Hanya baris data pasien seperti P01, P02, dst. Abaikan tabel perhitungan dan catatan di bawahnya.
    df["Pasien"] = df["Pasien"].astype(str).str.strip()
    df = df[df["Pasien"].str.match(r"^P\d+$", na=False)]
    for col in FEATURES:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df[TARGET] = df[TARGET].astype(str).str.strip()
    df = df.dropna(subset=FEATURES + [TARGET])
    df = df[df[TARGET].str.lower().isin(["tinggi", "rendah", "sedang"])]
    if len(df) < 1:
        raise ValueError("Tidak ada baris pasien yang valid pada dataset.")
    return df.reset_index(drop=True)

with st.sidebar:
    st.header("📁 Dataset")
    st.write("Aplikasi otomatis membaca Excel dari folder `data`.")
    uploaded = st.file_uploader("Atau unggah file Excel", type=["xlsx", "xls"])

try:
    data = load_dataset(uploaded)
except Exception as e:
    st.error(f"Gagal membaca dataset: {e}")
    st.info("Pastikan file ada di folder data dengan nama Data_Mining_KKN.xlsx. Struktur ZIP sudah menyertakan file ini.")
    st.stop()

st.success(f"Dataset berhasil dibaca: {len(data)} data pasien.")
left, right = st.columns([1.2, 1])
with left:
    st.subheader("📋 Dataset Pasien")
    st.dataframe(data, use_container_width=True, hide_index=True)
with right:
    st.subheader("📈 Ringkasan Kelas")
    st.bar_chart(data[TARGET].value_counts())
    st.write("Jumlah data per kelas:")
    st.dataframe(data[TARGET].value_counts().rename_axis("Kelas").reset_index(name="Jumlah"), use_container_width=True, hide_index=True)

st.divider()
st.subheader("🧮 Prediksi Data Baru")
st.write("Masukkan nilai untuk pasien/data baru, lalu tentukan jumlah tetangga terdekat (K).")
with st.form("prediction_form"):
    c1, c2, c3 = st.columns(3)
    with c1:
        usia = st.number_input("Usia", min_value=1, max_value=120, value=42, step=1)
        bmi = st.number_input("BMI", min_value=10.0, max_value=80.0, value=28.5, step=0.1)
    with c2:
        glukosa = st.number_input("Glukosa", min_value=20, max_value=600, value=130, step=1)
        tekanan = st.number_input("Tekanan Darah", min_value=40, max_value=300, value=128, step=1)
    with c3:
        riwayat = st.selectbox("Riwayat Keluarga", options=[0, 1], format_func=lambda x: "Tidak (0)" if x == 0 else "Ya (1)")
        max_k = max(1, len(data))
        k = st.number_input("Nilai K", min_value=1, max_value=max_k, value=min(3, max_k), step=1)
    submitted = st.form_submit_button("🔍 Hitung Prediksi", type="primary", use_container_width=True)

if submitted:
    X = data[FEATURES].astype(float)
    y = data[TARGET].astype(str)
    k_use = min(int(k), len(data))
    model = Pipeline([("scaler", StandardScaler()), ("knn", KNeighborsClassifier(n_neighbors=k_use))])
    model.fit(X, y)
    new_x = pd.DataFrame([[usia, bmi, glukosa, tekanan, riwayat]], columns=FEATURES)
    prediction = model.predict(new_x)[0]
    distances, indices = model.named_steps["knn"].kneighbors(model.named_steps["scaler"].transform(new_x), n_neighbors=k_use)
    neighbors = data.iloc[indices[0]][["Pasien"] + FEATURES + [TARGET]].copy()
    neighbors.insert(1, "Jarak (fitur distandardisasi)", distances[0])
    st.subheader("✅ Hasil Prediksi")
    st.metric("Kelas prediksi", str(prediction))
    st.write(f"Model menggunakan K = {k_use} dan {len(data)} data latih.")
    st.subheader("Tetangga Terdekat")
    st.dataframe(neighbors, use_container_width=True, hide_index=True)
    st.subheader("Data yang Diuji")
    st.dataframe(new_x, use_container_width=True, hide_index=True)
    st.caption("Catatan: hasil hanya untuk demonstrasi metode KNN pada tugas data mining, bukan diagnosis medis.")

st.divider()
st.subheader("ℹ️ Cara Kerja KNN")
st.markdown("""
1. Program membaca data pasien dari Excel.
2. Fitur numerik distandardisasi agar skala angka berbeda tidak mendominasi perhitungan.
3. KNN mencari K data dengan jarak paling dekat.
4. Kelas yang paling banyak muncul di tetangga digunakan sebagai hasil prediksi.
""")
