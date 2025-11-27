import streamlit as st
import pandas as pd

# -----------------------------
# Load Google Sheets REAL-TIME
# -----------------------------
@st.cache_data(ttl=15)  # cache 15 detik → data diperbarui tiap 15 detik
def load_data():
    sheet_id = "1lt1ksGwUK-pEUl-30Rsp4znMd5sq5nsX7BEMnWW2cEA"  # ganti jika perlu
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()  # bersihkan spasi header
    return df

df = load_data()

# -----------------------------
# UI Streamlit
# -----------------------------
st.set_page_config(page_title="Cek Pengisian Kuesioner Notaris", layout="wide")
st.title("🔍 Cek Pengisian Kuesioner PMPJ Notaris 2025")

st.write("Silakan masukkan 'Nama Notaris' atau 'NIK KTP' untuk memeriksa status pengisian kuesioner.")

search_type = st.radio("Cari berdasarkan:", ["Nama Notaris", "NIK KTP"])

if search_type == "Nama Notaris":
    keyword = st.text_input("Masukkan Nama Notaris ...")
else:
    keyword = st.text_input("Masukkan NIK KTP ...")

if st.button("Cek Status"):
    if not keyword.strip():
        st.warning("🚨 Mohon masukkan kata pencarian terlebih dahulu.")
    else:
        # 🔎 Filter sesuai pilihan pencarian
        if search_type == "Nama Notaris":
            hasil = df[df["Nama Notaris"].str.contains(keyword, case=False, na=False)]
        else:
            hasil = df[df["NIK KTP"].astype(str).str.contains(keyword, na=False)]

        if hasil.empty:
            st.error("❌ Tidak ditemukan: kemungkinan belum mengisi atau data belum ada di sheet.")
        else:
            st.success("✔ Data ditemukan — peserta sudah mengisi kuesioner.")

            # 🔒 Tampilkan hanya kolom yang diizinkan
            allowed_columns = ["Nama Notaris", "NIK KTP", "Kedudukan Kota/Kabupaten"]

            # jika kolom tidak lengkap, Streamlit tidak error
            existing_columns = [c for c in allowed_columns if c in hasil.columns]

            st.dataframe(hasil[existing_columns])
