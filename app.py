import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
import random

# Konfigurasi halaman
st.set_page_config(page_title="Survei Makanan Favorit Mahasiswa Makassar", layout="wide")

# --- List Data Umum ---
universitas_list = [
    "UNHAS", "UNM", "UP", "UIN Alauddin", 
    "STIMIK Dipanegara", "Universitas Bosowa", "Universitas Muslim Indonesia"
]
fakultas_list = [
    "Fakultas Teknik", "Fakultas Kedokteran", "Fakultas Ekonomi", 
    "Fakultas Hukum", "Fakultas Sastra", "Fakultas Ilmu Sosial", "Fakultas Pertanian"
]
makanan_list = ["Ayam Geprek"] * 40 + ["Mie Goreng", "Nasi Kuning", "Bakso", "Soto", "Coto Makassar", "Pallubasa", "Pizza", "Burger"]
gender_list = ["Pria", "Wanita"]
alasan_list = [
    "Enak dan pedas", "Murah dan mengenyangkan", "Rasa khas daerah", 
    "Banyak topping", "Cepat disajikan", "Favorit sejak kecil", 
    "Bikin nagih", "Cocok di lidah"
]

# --- Sidebar Navigasi ---
with st.sidebar:
    st.title("🍜 Navigasi")
    menu = st.radio("Pilih Halaman", ["Beranda", "Formulir", "Data Survei", "Grafik", "Peta Lokasi"])

# --- Halaman Beranda ---
if menu == "Beranda":
    st.title("🎓 Survei Makanan Favorit Mahasiswa Makassar")
    st.markdown("""
    Aplikasi ini bertujuan mengumpulkan dan menampilkan data makanan favorit mahasiswa dari berbagai universitas di Makassar.

    **Tujuan:**
    - Mengetahui tren makanan favorit
    - Menggali alasan mahasiswa menyukai makanan tertentu
    - Menampilkan persebaran universitas di Makassar secara geografis

    Silakan navigasi ke tab **Formulir** untuk mengisi survei atau lihat data dan grafik hasil survei di tab lainnya.
    """)

# --- Halaman Formulir ---
elif menu == "Formulir":
    st.title("📝 Formulir Survei")
    with st.form("form_survei"):
        nama = st.text_input("Nama Lengkap")
        jenis_kelamin = st.radio("Jenis Kelamin", gender_list)
        umur = st.number_input("Umur", min_value=17, max_value=30)
        semester = st.selectbox("Semester", list(range(1, 15)))
        universitas = st.selectbox("Universitas", universitas_list + ["Lainnya"])
        fakultas = st.text_input("Fakultas")
        makanan = st.text_input("Makanan Favorit")
        alasan = st.text_area("Mengapa menyukai makanan tersebut?")
        gambar = st.file_uploader("Upload Gambar Makanan Favorit", type=["jpg", "jpeg", "png"])
        submit = st.form_submit_button("Kirim")

    if submit:
        if nama and makanan and alasan:
            data_baru = pd.DataFrame({
                "Nama": [nama],
                "Jenis Kelamin": [jenis_kelamin],
                "Umur": [umur],
                "Semester": [semester],
                "Universitas": [universitas],
                "Fakultas": [fakultas],
                "Makanan Favorit": [makanan],
                "Alasan": [alasan]
            })
            data_baru.to_csv("data_survei.csv", mode='a', header=not os.path.exists("data_survei.csv"), index=False)
            st.success(f"Terima kasih {nama}, data kamu berhasil dikirim!")
            if gambar:
                st.image(gambar, caption="Gambar Makanan Favorit", use_column_width=True)
        else:
            st.warning("Mohon lengkapi semua kolom penting sebelum mengirim.")

# --- Halaman Data Survei ---
elif menu == "Data Survei":
    st.title("📊 Data Survei")

    st.subheader("📁 Upload File CSV Data Survei")
    file = st.file_uploader("Unggah file CSV", type="csv")
    if file:
        df_upload = pd.read_csv(file)
        st.dataframe(df_upload)

    if os.path.exists("data_survei.csv"):
        st.subheader("📂 Data Survei Tersimpan")
        df_local = pd.read_csv("data_survei.csv")
        st.dataframe(df_local)

    st.subheader("🔗 Data Survei dari API (Simulasi)")
    data_api = [{
        "Nama": f"Mahasiswa {i+1}",
        "Jenis Kelamin": random.choice(gender_list),
        "Umur": random.randint(17, 27),
        "Semester": random.randint(1, 14),
        "Universitas": random.choice(universitas_list),
        "Fakultas": random.choice(fakultas_list),
        "Makanan Favorit": random.choice(makanan_list),
        "Alasan": random.choice(alasan_list)
    } for i in range(100)]
    df_api = pd.DataFrame(data_api)
    st.dataframe(df_api)

# --- Halaman Grafik ---
elif menu == "Grafik":
    st.title("📈 Visualisasi Data Survei Mahasiswa")

    df = pd.DataFrame([{
        "Nama": f"Mahasiswa {i+1}",
        "Jenis Kelamin": random.choice(gender_list),
        "Umur": random.randint(17, 27),
        "Semester": random.randint(1, 14),
        "Universitas": random.choice(universitas_list),
        "Fakultas": random.choice(fakultas_list),
        "Makanan Favorit": random.choice(makanan_list),
        "Alasan": random.choice(alasan_list)
    } for i in range(100)])

    st.subheader("📈 Line Chart: Jumlah Mahasiswa per Semester")
    semester_counts = df['Semester'].value_counts().sort_index().reset_index()
    semester_counts.columns = ['Semester', 'Jumlah']
    st.plotly_chart(px.line(semester_counts, x='Semester', y='Jumlah', markers=True), use_container_width=True)

    st.subheader("📊 Bar Chart: Makanan Favorit")
    fav_counts = df['Makanan Favorit'].value_counts().reset_index()
    fav_counts.columns = ['Makanan', 'Jumlah']
    st.plotly_chart(px.bar(fav_counts, x='Makanan', y='Jumlah'), use_container_width=True)

    st.subheader("🥧 Pie Chart: Jenis Kelamin")
    st.plotly_chart(px.pie(df, names='Jenis Kelamin'), use_container_width=True)

    st.subheader("📊 Histogram: Distribusi Umur")
    st.plotly_chart(px.histogram(df, x='Umur', nbins=10), use_container_width=True)

    st.subheader("📦 Box Plot: Umur per Jenis Kelamin")
    st.plotly_chart(px.box(df, x='Jenis Kelamin', y='Umur'), use_container_width=True)

    st.subheader("🔘 Scatter Plot: Umur vs Semester")
    st.plotly_chart(px.scatter(df, x='Umur', y='Semester', color='Jenis Kelamin'), use_container_width=True)

    st.subheader("🔥 Heatmap: Korelasi Numerik")
    st.plotly_chart(px.imshow(df[['Umur', 'Semester']].corr(), text_auto=True), use_container_width=True)

    st.subheader("🎻 Violin Plot: Umur per Makanan Favorit")
    st.plotly_chart(px.violin(df, y='Umur', x='Makanan Favorit', box=True, points="all"), use_container_width=True)

    st.subheader("📉 Area Chart: Mahasiswa per Universitas")
    uni_counts = df['Universitas'].value_counts().reset_index()
    uni_counts.columns = ['Universitas', 'Jumlah']
    st.plotly_chart(px.area(uni_counts, x='Universitas', y='Jumlah'), use_container_width=True)

    st.subheader("🫧 Bubble Chart: Umur vs Semester")
    bubble_df = df.groupby(['Umur', 'Semester']).size().reset_index(name='Jumlah')
    st.plotly_chart(px.scatter(bubble_df, x='Umur', y='Semester', size='Jumlah', color='Jumlah'), use_container_width=True)

    st.subheader("📊 Stacked Bar Chart: Gender per Universitas")
    stacked_df = df.groupby(['Universitas', 'Jenis Kelamin']).size().reset_index(name='Jumlah')
    st.plotly_chart(px.bar(stacked_df, x='Universitas', y='Jumlah', color='Jenis Kelamin', barmode='stack'), use_container_width=True)

# --- Halaman Peta Lokasi ---
elif menu == "Peta Lokasi":
    st.title("🗺️ Peta Universitas di Makassar")
    data_map = pd.DataFrame({
        'Nama Universitas': [
            'Universitas Hasanuddin', 'Universitas Negeri Makassar',
            'Universitas Muslim Indonesia', 'Universitas Islam Negeri Alauddin',
            'Universitas Bosowa'
        ],
        'lat': [-5.138430, -5.135088, -5.147484, -5.199537, -5.146805],
        'lon': [119.487548, 119.418350, 119.435829, 119.385712, 119.441547]
    })
    st.map(data_map)
