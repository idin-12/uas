import streamlit as st
from scipy.optimize import linprog
import numpy as np
import matplotlib.pyplot as plt

# Judul aplikasi
st.title("Aplikasi Optimasi Produksi (Linear Programming)")
st.write("Maksimalkan keuntungan produksi dengan kendala waktu, bahan baku, dan tenaga kerja.")

# Input jumlah produk
num_products = st.number_input("Jumlah Produk", min_value=2, value=2)

# Input keuntungan per unit
profit = []
st.write("### Input Keuntungan per Unit Produk")
for i in range(num_products):
    p = st.number_input(f"Keuntungan Produk {i+1}", value=10)
    profit.append(p)

# Input jumlah kendala (sumber daya)
num_constraints = st.number_input("Jumlah Kendala (misal bahan baku, waktu, tenaga kerja)", min_value=1, value=2)

# Input batasan kendala dan koefisiennya
A = []
b = []
st.write("### Input Koefisien Kendala dan Batasannya")
for j in range(num_constraints):
    st.write(f"Kendala {j+1}")
    row = []
    for i in range(num_products):
        a = st.number_input(f"Koefisien Produk {i+1} pada Kendala {j+1}", value=1)
        row.append(a)
    A.append(row)
    b_value = st.number_input(f"Batas Kendala {j+1}", value=100)
    b.append(b_value)

# Convert ke array numpy
A = np.array(A)
b = np.array(b)
c = -np.array(profit)  # dikali -1 karena linprog meminimasi

# Solve linear programming
if st.button("Hitung Solusi Optimal"):
    res = linprog(c, A_ub=A, b_ub=b, method='highs')

    if res.success:
        st.success("Solusi Optimal Ditemukan!")
        for i, x in enumerate(res.x):
            st.write(f"Produksi Produk {i+1} = {x:.2f} unit")
        st.write(f"Total Keuntungan Maksimum = {(-res.fun):.2f}")
    else:
        st.error("Tidak ada solusi feasible.")

    # Visualisasi area feasible (hanya untuk dua variabel)
    if num_products == 2:
        x = np.linspace(0, max(b)*1.2, 400)
        plt.figure(figsize=(8,6))

        for i in range(num_constraints):
            y = (b[i] - A[i,0]*x) / A[i,1]
            plt.plot(x, y, label=f'Kendala {i+1}')
            plt.fill_between(x, 0, y, alpha=0.1)

        plt.xlabel('Produk 1')
        plt.ylabel('Produk 2')
        plt.title('Area Feasible dan Solusi Optimal')
        plt.legend()
        plt.xlim(0, max(b)*1.2)
        plt.ylim(0, max(b)*1.2)

        # Plot titik optimal jika ada
        if res.success:
            plt.scatter(res.x[0], res.x[1], color='red', label='Solusi Optimal')
            plt.legend()

        st.pyplot(plt)
