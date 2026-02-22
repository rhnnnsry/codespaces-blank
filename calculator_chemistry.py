import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from molmass import Formula

st.set_page_config(page_title="ChemLab Calculator Pro", layout="wide")

# =========================
# CUSTOM CSS (MODERN UI)
# =========================
st.markdown("""
<style>
.main {
    background-color: #0e1117;
    color: white;
}
h1, h2, h3 {
    color: #4CAF50;
}
.stButton>button {
    background-color: #4CAF50;
    color: white;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("🧪 ChemLab Calculator Pro")
st.write("Aplikasi Kalkulator Kimia Interaktif Berbasis Python & Streamlit")

menu = st.sidebar.selectbox(
    "Pilih Fitur",
    [
        "Pengenceran (M1V1 = M2V2)",
        "Stoikiometri",
        "Massa Molekul Otomatis",
        "Mol & Molaritas Visual"
    ]
)

# ====================================================
# 1️⃣ PENGENCERAN + GRAFIK
# ====================================================
if menu == "Pengenceran (M1V1 = M2V2)":

    st.header("Kalkulator Pengenceran")

    col1, col2 = st.columns(2)

    with col1:
        M1 = st.number_input("M1 (M)", min_value=0.0)
        V1 = st.number_input("V1 (mL)", min_value=0.0)
        M2 = st.number_input("M2 (M)", min_value=0.0)

    if st.button("Hitung Volume Akhir"):

        if M2 != 0:
            V2 = (M1 * V1) / M2
            st.success(f"Volume akhir (V2) = {V2:.2f} mL")

            # Grafik Visualisasi
            volume_range = np.linspace(V1, V2, 50)
            concentration = (M1 * V1) / volume_range

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=volume_range,
                y=concentration,
                mode='lines',
                name='Kurva Pengenceran'
            ))

            fig.update_layout(
                title="Grafik Perubahan Konsentrasi terhadap Volume",
                xaxis_title="Volume (mL)",
                yaxis_title="Konsentrasi (M)",
                template="plotly_dark"
            )

            st.plotly_chart(fig, use_container_width=True)

        else:
            st.error("M2 tidak boleh 0!")

# ====================================================
# 2️⃣ STOIKIOMETRI + VISUAL BAR
# ====================================================
elif menu == "Stoikiometri":

    st.header("Kalkulator Stoikiometri")

    massa = st.number_input("Massa (gram)", min_value=0.0)
    mr = st.number_input("Mr", min_value=0.0)

    if st.button("Hitung Mol"):

        if mr != 0:
            mol = massa / mr
            st.success(f"Jumlah mol = {mol:.4f} mol")

            fig = px.bar(
                x=["Massa (g)", "Mol"],
                y=[massa, mol],
                title="Perbandingan Massa dan Mol",
                template="plotly_dark"
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Mr tidak boleh 0!")

# ====================================================
# 3️⃣ MASSA MOLEKUL OTOMATIS
# ====================================================
elif menu == "Massa Molekul Otomatis":

    st.header("Kalkulator Massa Molekul")

    rumus = st.text_input("Masukkan rumus kimia (contoh: NaCl, H2SO4)")

    if st.button("Hitung Massa Molekul"):

        try:
            f = Formula(rumus)
            st.success(f"Massa Molekul {rumus} = {f.mass:.2f} g/mol")

            elements = f.composition().dataframe()
            elements.reset_index(inplace=True)

            fig = px.pie(
                elements,
                names="Element",
                values="Fraction",
                title="Komposisi Unsur (%)",
                template="plotly_dark"
            )

            st.plotly_chart(fig, use_container_width=True)

        except:
            st.error("Rumus kimia tidak valid!")

# ====================================================
# 4️⃣ MOL & MOLARITAS + VISUALISASI
# ====================================================
elif menu == "Mol & Molaritas Visual":

    st.header("Perhitungan Mol & Molaritas")

    massa = st.number_input("Massa zat (g)", min_value=0.0)
    mr = st.number_input("Mr", min_value=0.0)
    volume = st.number_input("Volume (L)", min_value=0.0)

    if st.button("Hitung"):

        if mr != 0 and volume != 0:
            mol = massa / mr
            M = mol / volume

            st.success(f"Mol = {mol:.4f}")
            st.success(f"Molaritas = {M:.4f} M")

            fig = go.Figure(data=[
                go.Bar(name='Mol', x=['Nilai'], y=[mol]),
                go.Bar(name='Molaritas', x=['Nilai'], y=[M])
            ])

            fig.update_layout(
                title="Visualisasi Mol dan Molaritas",
                template="plotly_dark"
            )

            st.plotly_chart(fig, use_container_width=True)

        else:
            st.error("Mr dan Volume tidak boleh 0!")