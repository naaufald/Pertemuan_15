import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Judul aplikasi
st.title("Aplikasi Pencatatan Pemasukan dan Pengeluaran")

# Sidebar untuk mencatat pemasukan atau pengeluaran
st.sidebar.header("Catat Pemasukan atau Pengeluaran")
tanggal = st.sidebar.date_input("Tanggal")
jenis = st.sidebar.text_input('Jenis Pemasukan atau Pengeluaran')
kategori = st.sidebar.selectbox("Kategori", ["Pemasukan", "Pengeluaran"])
jumlah = st.sidebar.number_input("Jumlah (kelipatan 10.000)", min_value=0, step=10000)

if st.sidebar.button("Simpan"):
    # Validasi untuk memastikan jumlah adalah kelipatan 10.000
    if jumlah % 10000 != 0:
        st.error("Jumlah harus merupakan kelipatan 10.000.")
    else:
        # Menyimpan data ke DataFrame
        new_entry = pd.DataFrame({
            'Jenis': [jenis],
            'Tanggal': [tanggal],
            'Kategori': [kategori],
            'Jumlah': [jumlah]
        })
        if 'data' not in st.session_state:
            st.session_state.data = pd.DataFrame(columns=['Tanggal', 'Jenis', 'Kategori', 'Jumlah'])
        st.session_state.data = pd.concat([st.session_state.data, new_entry], ignore_index=True)
        st.success("Data berhasil disimpan! Congrats! You Did It!")

# Container untuk menampilkan data yang telah dicatat
with st.container():
    st.subheader("Data Pemasukan dan Pengeluaran")
    if 'data' in st.session_state and not st.session_state.data.empty:
        st.write(st.session_state.data)
    else:
        st.write("Belum ada data yang dicatat.")

# Visualisasi dan perhitungan sisa
if 'data' in st.session_state and not st.session_state.data.empty:
    st.subheader("Data yang masuk :")
     
    # Menghitung total pemasukan dan pengeluaran
    total_pemasukan = st.session_state.data[st.session_state.data['Kategori'] == 'Pemasukan']['Jumlah'].sum()
    total_pengeluaran = st.session_state.data[st.session_state.data['Kategori'] == 'Pengeluaran']['Jumlah'].sum()
    
    # Menghitung sisa
    sisa = total_pemasukan - total_pengeluaran
    
    # Menampilkan total dan sisa
    st.write(f"Total Pemasukan: {total_pemasukan}")
    st.write(f"Total Pengeluaran: {total_pengeluaran}")
    st.write(f"Sisa Pemasukan: {sisa}")

    # Membuat grafik pie
    summary = st.session_state.data.groupby('Kategori')['Jumlah'].sum()
    
    fig, ax = plt.subplots()
    ax.pie(summary, labels=summary.index, autopct='%1.1f%%', startangle=90, colors=['green', 'red'])
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title('Distribusi Pemasukan dan Pengeluaran')
    
    # Menampilkan grafik
    st.pyplot(fig)