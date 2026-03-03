import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from molmass import Formula

st.set_page_config(page_title="ChemLab Calculator V1.1", layout="wide")

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

st.title("🧪 Chemist Calculator V1.1")
st.write("Aplikasi Kalkulator Kimia Interaktif (Update :v)")

menu = st.sidebar.selectbox(
    "Pilih Fitur",
    [
        "Pengenceran (M1V1 = M2V2)",
        "Stoikiometri",
        "Massa Molekul Otomatis",
        "Mol & Molaritas Visual",
        "Kalkulator Normalitas",
        "Persen Konsentrasi",
        "Rumus Kimia Penting",
        "Kalkulator pH",
        "Larutan Buffer",
        "Kurva Kalibrasi Spektrofotometri"
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
# ====================================================
# NORMALITAS
# ====================================================

elif menu == "Kalkulator Normalitas":

    st.header("Kalkulator Normalitas (N)")

    massa = st.number_input("Massa zat (gram)", min_value=0.0)
    BE = st.number_input("Berat Ekuivalen", min_value=0.0)
    volume = st.number_input("Volume larutan (Liter)", min_value=0.0)

    if st.button("Hitung Normalitas"):

        if BE != 0 and volume != 0:

            N = massa / (BE * volume)

            st.success(f"Normalitas = {N:.4f} N")

        else:
            st.error("Berat ekuivalen dan volume tidak boleh 0!")
            st.plotly_chart(fig, use_container_width=True)

# ====================================================
# PERSEN KONSENTRASI
# ====================================================

elif menu == "Persen Konsentrasi":

    st.header("Perhitungan Persen Konsentrasi")

    jenis = st.radio(
        "Pilih jenis konsentrasi",
        ["Persen b/b", "Persen b/v"]
    )

    massa_zat = st.number_input("Massa zat terlarut (gram)", min_value=0.0)

    if jenis == "Persen b/b":

        massa_larutan = st.number_input("Massa larutan (gram)", min_value=0.0)

        if st.button("Hitung % b/b"):

            if massa_larutan != 0:

                persen = (massa_zat / massa_larutan) * 100

                st.success(f"Persen b/b = {persen:.2f}%")

    else:

        volume_larutan = st.number_input("Volume larutan (mL)", min_value=0.0)

        if st.button("Hitung % b/v"):

            if volume_larutan != 0:

                persen = (massa_zat / volume_larutan) * 100

                st.success(f"Persen b/v = {persen:.2f}%")
# ====================================================
# RUMUS KIMIA PENTING
# ====================================================

elif menu == "Rumus Kimia Penting":

    st.header("📚 Kumpulan Rumus Kimia Dasar")

    st.subheader("1️⃣ Mol")

    st.latex(r"n = \frac{m}{Mr}")

    st.write("""
    n = mol  
    m = massa (gram)  
    Mr = massa molekul relatif
    """)

    st.subheader("2️⃣ Molaritas")

    st.latex(r"M = \frac{n}{V}")

    st.write("""
    M = molaritas (mol/L)  
    n = mol  
    V = volume larutan (L)
    """)

    st.subheader("3️⃣ Normalitas")

    st.latex(r"N = \frac{massa}{BE \times V}")

    st.write("""
    BE = berat ekuivalen  
    V = volume larutan (L)
    """)

    st.subheader("4️⃣ Persen Konsentrasi")

    st.latex(r"\% b/b = \frac{massa zat}{massa larutan} \times 100")

    st.latex(r"\% b/v = \frac{massa zat}{volume larutan} \times 100")

    st.subheader("5️⃣ Pengenceran")

    st.latex(r"M_1 V_1 = M_2 V_2")

    st.subheader("6️⃣ Berat Ekuivalen")

    st.latex(r"BE = \frac{Mr}{n}")
# ====================================================
# KALKULATOR pH
# ====================================================

elif menu == "Kalkulator pH":

    st.header("Kalkulator pH Larutan")

    jenis = st.radio(
        "Pilih jenis larutan",
        ["Asam kuat", "Basa kuat"]
    )

    konsentrasi = st.number_input("Masukkan konsentrasi (M)", min_value=0.0)

    if st.button("Hitung pH"):

        if jenis == "Asam kuat":

            pH = -np.log10(konsentrasi)
            st.success(f"pH = {pH:.2f}")

        else:

            pOH = -np.log10(konsentrasi)
            pH = 14 - pOH

            st.success(f"pH = {pH:.2f}")
# ====================================================
# BUFFER
# ====================================================

elif menu == "Larutan Buffer":

    st.header("Kalkulator Larutan Buffer")

    Ka = st.number_input("Nilai Ka", min_value=0.0, format="%.6f")

    asam = st.number_input("Konsentrasi Asam (M)", min_value=0.0)

    basa = st.number_input("Konsentrasi Basa Konjugasi (M)", min_value=0.0)

    if st.button("Hitung pH Buffer"):

        if Ka != 0 and asam != 0:

            pKa = -np.log10(Ka)

            pH = pKa + np.log10(basa/asam)

            st.success(f"pH Buffer = {pH:.2f}")
# ====================================================
# KURVA KALIBRASI
# ====================================================

elif menu == "Kurva Kalibrasi Spektrofotometri":

    st.header("Kurva Kalibrasi Spektrofotometri")

    st.write("Masukkan data konsentrasi standar dan absorbansi.")

    konsentrasi = st.text_input(
        "Konsentrasi standar (pisahkan dengan koma)",
        "1,2,3,4,5"
    )

    absorbansi = st.text_input(
        "Absorbansi (pisahkan dengan koma)",
        "0.12,0.25,0.37,0.50,0.61"
    )

    if st.button("Buat Kurva Kalibrasi"):

        x = np.array([float(i) for i in konsentrasi.split(",")])
        y = np.array([float(i) for i in absorbansi.split(",")])

        slope, intercept = np.polyfit(x, y, 1)

        y_pred = slope * x + intercept

        r2 = 1 - (np.sum((y-y_pred)**2) / np.sum((y-np.mean(y))**2))

        st.success(f"Persamaan regresi: y = {slope:.4f}x + {intercept:.4f}")
        st.success(f"R² = {r2:.4f}")

        fig = px.scatter(x=x, y=y, title="Kurva Kalibrasi")

        fig.add_scatter(x=x, y=y_pred, mode='lines')

        st.plotly_chart(fig)
# ====================================================
# UPLOAD DATA EXCEL
# ====================================================

st.subheader("Upload Data Excel")

file = st.file_uploader("Upload file Excel", type=["xlsx"])

if file is not None:

    data = pd.read_excel(file)

    st.write("Data yang diupload:")

    st.dataframe(data)

    if "Konsentrasi" in data.columns and "Absorbansi" in data.columns:

        x = data["Konsentrasi"]
        y = data["Absorbansi"]

        slope, intercept = np.polyfit(x, y, 1)

        y_pred = slope * x + intercept

        fig = px.scatter(x=x, y=y, title="Kurva Kalibrasi dari Excel")

        fig.add_scatter(x=x, y=y_pred, mode='lines')

        st.plotly_chart(fig)
