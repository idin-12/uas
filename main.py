import streamlit as st
from scipy.optimize import linprog
import numpy as np
import matplotlib.pyplot as plt

# ===============================
# Konfigurasi halaman
st.set_page_config(page_title="Optimasi Produksi", page_icon="📈", layout="centered")

# ===============================
# Sidebar untuk inputan
st.sidebar.title("🔧 Input Parameter")
num_products = st.sidebar.number_input("Jumlah Produk", min_value=2, value=2)

st.sidebar.markdown("### 💰 Keuntungan per Unit Produk")
profit = []
for i in range(num_products):
    p = st.sidebar.number_input(f"Produk {i+1}", value=10)
    profit.append(p)

num_constraints = st.sidebar.number_input("Jumlah Kendala (misal bahan baku, waktu, tenaga kerja)", min_value=1, value=2)

st.sidebar.markdown("### ⚙️ Koefisien Kendala dan Batasannya")
A = []
b = []
for j in range(num_constraints):
    st.sidebar.markdown(f"**Kendala {j+1}**")
    row = []
    for i in range(num_products):
        a = st.sidebar.number_input(f"Koefisien Produk {i+1} (Kendala {j+1})", value=1)
        row.append(a)
    A.append(row)
    b_value = st.sidebar.number_input(f"Batas Kendala {j+1}", value=100)
    b.append(b_value)

# ===============================
# Header aplikasi
st.title("📈 Aplikasi Optimasi Produksi")
st.write("Maksimalkan keuntungan produksi dengan kendala waktu, bahan baku, dan tenaga kerja menggunakan Linear Programming (Simplex Method).")

# ===============================
# Convert input ke numpy array
A = np.array(A)
b = np.array(b)
c = -np.array(profit)  # dikali -1 karena linprog meminimasi

# ===============================
# Solve linear programming ketika tombol ditekan
if st.button("🚀 Hitung Solusi Optimal"):
    res = linprog(c, A_ub=A, b_ub=b, method='highs')

    if res.success:
        st.success("✅ Solusi Optimal Ditemukan!")
        col1, col2 = st.columns(2)
        with col1:
            for i, x in enumerate(res.x):
                st.write(f"**Produksi Produk {i+1}** = {x:.2f} unit")
        with col2:
            st.metric(label="💲 **Keuntungan Maksimum**", value=f"{(-res.fun):.2f}")
    else:
        st.error("❌ Tidak ada solusi feasible. Periksa kembali input kendala dan keuntungan.")

    # ===============================
    # Visualisasi area feasible (hanya untuk 2 produk)
    if num_products == 2:
        x = np.linspace(0, max(b)*1.2, 400)
        plt.figure(figsize=(8,6))

        for i in range(num_constraints):
            if A[i,1] != 0:
                y = (b[i] - A[i,0]*x) / A[i,1]
                y = np.maximum(0, y)
                plt.plot(x, y, label=f'Kendala {i+1}')
                plt.fill_between(x, 0, y, alpha=0.1)
            else:
                # Jika koefisien produk 2 = 0 (horizontal line)
                x_line = b[i]/A[i,0]
                plt.axvline(x=x_line, label=f'Kendala {i+1}', alpha=0.5)

        plt.xlabel('Produk 1')
        plt.ylabel('Produk 2')
        plt.title('📊 Area Feasible dan Solusi Optimal')
        plt.legend()
        plt.xlim(0, max(b)*1.2)
        plt.ylim(0, max(b)*1.2)
        plt.grid(True)

        if res.success:
            plt.scatter(res.x[0], res.x[1], color='red', label='Solusi Optimal')
            plt.legend()

        st.pyplot(plt)

# ===============================
# Footer
st.markdown("---")
st.caption("Dibuat dengan ❤️ menggunakan Streamlit dan SciPy oleh Muhyiddin As Syarif.")
