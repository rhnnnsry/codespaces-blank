import streamlit as st
import numpy as np
import pandas as pd
from molmass import Formula

st.set_page_config(page_title="Web Kalkulator Kimia Lengkap", layout="wide")

st.title("🧪 Web Kalkulator Kimia Lengkap")
st.write("Aplikasi berbasis Python untuk membantu perhitungan kimia laboratorium.")

menu = st.sidebar.selectbox(
    "Pilih Fitur",
    [
        "Pengenceran (M1V1 = M2V2)",
        "Konversi ppm ↔ mg/L",
        "Kalkulator Stoikiometri",
        "Kalkulator Massa Molekul",
        "Perhitungan Mol & Molaritas"
    ]
)

# ==========================================
# 1. PENGENCERAN
# ==========================================
if menu == "Pengenceran (M1V1 = M2V2)":
    st.header("Kalkulator Pengenceran")
    
    M1 = st.number_input("M1 (Molaritas awal)", min_value=0.0)
    V1 = st.number_input("V1 (Volume awal dalam mL)", min_value=0.0)
    M2 = st.number_input("M2 (Molaritas akhir)", min_value=0.0)

    if st.button("Hitung V2"):
        if M2 != 0:
            V2 = (M1 * V1) / M2
            st.success(f"Volume akhir (V2) = {V2:.2f} mL")
        else:
            st.error("M2 tidak boleh 0!")

# ==========================================
# 2. KONVERSI ppm
# ==========================================
elif menu == "Konversi ppm ↔ mg/L":
    st.header("Konversi ppm dan mg/L")

    pilihan = st.radio("Pilih Konversi", ["ppm ke mg/L", "mg/L ke ppm"])

    nilai = st.number_input("Masukkan nilai", min_value=0.0)

    if st.button("Konversi"):
        if pilihan == "ppm ke mg/L":
            st.success(f"{nilai} ppm = {nilai} mg/L (untuk air)")
        else:
            st.success(f"{nilai} mg/L = {nilai} ppm (untuk air)")

# ==========================================
# 3. STOIKIOMETRI
# ==========================================
elif menu == "Kalkulator Stoikiometri":
    st.header("Kalkulator Stoikiometri Sederhana")

    massa = st.number_input("Masukkan massa zat (gram)", min_value=0.0)
    mr = st.number_input("Masukkan Massa Molekul Relatif (Mr)", min_value=0.0)

    if st.button("Hitung Mol"):
        if mr != 0:
            mol = massa / mr
            st.success(f"Jumlah mol = {mol:.4f} mol")
        else:
            st.error("Mr tidak boleh 0!")

# ==========================================
# 4. MASSA MOLEKUL OTOMATIS
# ==========================================
elif menu == "Kalkulator Massa Molekul":
    st.header("Kalkulator Massa Molekul Otomatis")

    rumus = st.text_input("Masukkan rumus kimia (contoh: H2SO4)")

    if st.button("Hitung Massa Molekul"):
        try:
            f = Formula(rumus)
            st.success(f"Massa Molekul {rumus} = {f.mass:.2f} g/mol")
        except:
            st.error("Rumus kimia tidak valid!")

# ==========================================
# 5. MOL & MOLARITAS
# ==========================================
elif menu == "Perhitungan Mol & Molaritas":
    st.header("Perhitungan Mol dan Molaritas")

    massa = st.number_input("Massa zat (gram)", min_value=0.0)
    mr = st.number_input("Mr", min_value=0.0)
    volume = st.number_input("Volume larutan (Liter)", min_value=0.0)

    if st.button("Hitung"):
        if mr != 0 and volume != 0:
            mol = massa / mr
            M = mol / volume
            st.success(f"Jumlah mol = {mol:.4f} mol")
            st.success(f"Molaritas = {M:.4f} M")
        else:
            st.error("Mr dan Volume tidak boleh 0!")
