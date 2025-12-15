import streamlit as st
import pandas as pd

# -----------------------------
# Load Google Sheets REAL-TIME
# -----------------------------
@st.cache_data(ttl=15)  # cache 15 detik → data diperbarui tiap 15 detik
def load_data():
    sheet_id = "172mEV_i2Yr6l4udGjxDK03MtMFo2bvjfPdSUyD1-c9g"  # sheet id benar
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# -----------------------------
# UI Streamlit
# -----------------------------
st.set_page_config(page_title="Cek Pendataan Buka Blokir Akun AHU", layout="wide")
st.title("🔍 Cek Pendataan Buka Blokir Akun AHU")

st.write("Silakan masukkan 'Nama Notaris' atau 'Kedudukan' untuk memeriksa status pengisian kuesioner.")

search_type = st.radio("Cari berdasarkan:", ["Nama Notaris", "Kedudukan"])

if search_type == "Nama Notaris":
    keyword = st.text_input("Masukkan Nama Notaris ...")
else:
    keyword = st.text_input("Masukkan Kedudukan ...")

if st.button("Cek Status"):
    if not keyword.strip():
        st.warning("🚨 Mohon masukkan kata pencarian terlebih dahulu.")
    else:
        # 🔎 Filter sesuai pilihan pencarian
        if search_type == "Nama Notaris":
            hasil = df[df["Nama Notaris"].str.contains(keyword, case=False, na=False)]
        else:
            hasil = df[df["Kedudukan"].astype(str).str.contains(keyword, na=False)]

        if hasil.empty:
            st.error("❌ Tidak ditemukan: belum mengisi formulir pendataan buka blokir atau data belum diajukan ke pusat.")
        else:
            st.success("✔ Data ditemukan — peserta sudah mengisi formulir pendataan buka blokir akun AHU dan sudah diajukan ke pusat")

            # 🔒 Tampilkan hanya kolom yang diizinkan
            allowed_columns = ["Timestamp", "Nama Notaris", "Kedudukan", "Batch"]

            # jika kolom tidak lengkap, Streamlit tidak error
            existing_columns = [c for c in allowed_columns if c in hasil.columns]

            st.dataframe(hasil[existing_columns])