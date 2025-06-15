import streamlit as st
import numpy as np
import pandas as pd
from scipy.optimize import linprog
import plotly.graph_objects as go
import plotly.express as px

# Konfigurasi halaman
st.set_page_config(
    page_title="Simplex Solver - Problem 13.8",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk styling dan font yang lebih baik
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');

    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif; 
    }

    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .problem-card {
        background: purple;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #667eea;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    
    .success-alert {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .error-alert {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .info-box {
        background: purple;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #bbdefb;
        margin: 1rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
        width: 100%;
        font-family: 'Inter', sans-serif; 
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    .separator {
        border-top: 3px solid #667eea;
        margin: 2rem 0;
        border-radius: 2px;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header utama
    st.markdown("""
    <div class="main-header">
        <h1>📊 Linear Programming Solver</h1>
        <p>Solusi Optimal untuk Problem 13.8-5 dan 13.8-9 dengan Metode Simplex</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar untuk pemilihan masalah
    with st.sidebar:
        st.markdown("### 🎯 Pilih Masalah")
        problem_choice = st.selectbox(
            "Problem:",
            ["Problem 13.8-5 (Production Planning)", "Problem 13.8-9 (Resource Allocation)"],
            help="Pilih masalah yang ingin diselesaikan"
        )
        
        st.markdown("---")
        st.markdown("### ℹ️ Informasi")
        if "13.8-5" in problem_choice:
            st.info("**Problem 13.8-5**: Optimalisasi produksi dengan mesin gergaji dan bor, mempertimbangkan waktu reguler dan lembur.")
        else:
            st.info("**Problem 13.8-9**: Optimalisasi alokasi sumber daya dengan batasan anggaran dan kapasitas produksi.")
        
        st.markdown("### 📚 Metode")
        st.markdown("""
        - **Algorithm**: Simplex Method
        - **Solver**: SciPy HiGHS
        - **Type**: Linear Programming
        - **Goal**: Find Optimal Solution
        """)
    
    # Konten berdasarkan pilihan masalah
    if "13.8-5" in problem_choice:
        problem_13_8_5()
    else:
        problem_13_8_9()

def problem_13_8_5():
    st.markdown("""
    <div class="problem-card">
        <h2>🏭 Problem 13.8-5: Production Planning</h2>
        <p><strong>Deskripsi:</strong> Perusahaan memproduksi produk menggunakan mesin gergaji dan bor. 
        Setiap mesin memiliki waktu operasi reguler dan lembur dengan profit yang berbeda per unit waktu.</p>
    </div>
    """, unsafe_allow_html=True)

    # --- TUTORIAL DITAMBAHKAN DI SINI ---
    with st.expander("📖 Panduan Penggunaan - Production Planning"):
        st.markdown("""
        Panduan ini membantu Anda memahami cara menggunakan solver untuk masalah perencanaan produksi.

        #### **1. Pahami Tujuan & Variabel**
        * **Tujuan**: Memaksimalkan total profit dari semua unit yang diproduksi.
        * **Variabel Keputusan**:
            * `x₁₁ (Gergaji Reg)`: Jumlah unit yang diproduksi mesin gergaji pada waktu reguler.
            * `x₁₂ (Gergaji OT)`: Jumlah unit yang diproduksi mesin gergaji pada waktu lembur (Overtime).
            * `x₂₁ (Bor Reg)`: Jumlah unit yang diproduksi mesin bor pada waktu reguler.
            * `x₂₂ (Bor OT)`: Jumlah unit yang diproduksi mesin bor pada waktu lembur (Overtime).

        #### **2. Atur Parameter Input**
        * **Fungsi Tujuan**: Masukkan nilai profit yang didapat dari setiap unit produk. Contoh: profit $150 untuk setiap unit `x₁₁`.
        * **Batasan (Constraints)**: Definisikan batasan sumber daya.
            * `Batasan 1`: Mengatur total kapasitas gabungan semua mesin.
            * `Batasan 2`: Mengatur kapasitas produksi berdasarkan bobot atau waktu yang dibutuhkan oleh setiap jenis produksi.
        * **Batasan Variabel (Bounds)**: Masukkan batas atas (kapasitas maksimal) untuk setiap jenis produksi. Contoh: mesin gergaji hanya bisa beroperasi maksimal 3000 unit pada waktu reguler.

        #### **3. Selesaikan dan Analisis**
        1.  Setelah semua parameter sesuai dengan soal, klik tombol **"🚀 Solve Problem 13.8-5"**.
        2.  Hasilnya akan muncul di bawah, menunjukkan alokasi produksi yang optimal untuk profit maksimal, serta analisis penggunaan sumber daya.
        """)
    
    # Input Section
    st.markdown("## 📝 Input Parameters")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Fungsi Tujuan (Maksimalkan Profit)")
        
        variables = ['x₁₁ (Gergaji Reg)', 'x₁₂ (Gergaji OT)', 'x₂₁ (Bor Reg)', 'x₂₂ (Bor OT)']
        obj_defaults = [150, 50, 100, 75]
        
        obj_coeffs = []
        cols = st.columns(4)
        for i, (var, default) in enumerate(zip(variables, obj_defaults)):
            with cols[i]:
                coeff = st.number_input(f"**{var}**", value=default, key=f"obj_13_8_5_{i}", help=f"Profit per unit untuk {var}")
                obj_coeffs.append(coeff)
        
        st.markdown("### Batasan (Constraints)")
        
        st.markdown("**Batasan 1:** Total Kapasitas Mesin")
        a1_defaults = [1, 1, 1, 1]
        constraint1_coeffs = []
        cols = st.columns(5)
        for i, default in enumerate(a1_defaults):
            with cols[i]:
                coeff = st.number_input(f"a₁{i+1}", value=default, key=f"c1_13_8_5_{i}", help=f"Koefisien constraint 1 untuk variabel {i+1}")
                constraint1_coeffs.append(coeff)
        with cols[4]:
            b1 = st.number_input("**≤ RHS₁**", value=10000, key="b1_13_8_5", help="Batas kanan constraint 1")
        
        st.markdown("**Batasan 2:** Kapasitas Produksi")
        a2_defaults = [2, 2, 1, 1]
        constraint2_coeffs = []
        cols = st.columns(5)
        for i, default in enumerate(a2_defaults):
            with cols[i]:
                coeff = st.number_input(f"a₂{i+1}", value=default, key=f"c2_13_8_5_{i}", help=f"Koefisien constraint 2 untuk variabel {i+1}")
                constraint2_coeffs.append(coeff)
        with cols[4]:
            b2 = st.number_input("**≤ RHS₂**", value=15000, key="b2_13_8_5", help="Batas kanan constraint 2")
    
    with col2:
        st.markdown("### Batasan Variabel (Bounds)")
        bounds_defaults = [3000, 2000, 5000, 3000]
        bounds = []
        for i, (var, default) in enumerate(zip(variables, bounds_defaults)):
            bound = st.number_input(f"**Max {var.split(' ')[0]}**", value=default, key=f"bound_13_8_5_{i}", help=f"Batas atas untuk {var}")
            bounds.append((0, bound))
        
        st.markdown("""
        <div class="info-box">
            <h4>📋 Problem Summary</h4>
            <p><strong>Variables:</strong> 4 decision variables</p>
            <p><strong>Constraints:</strong> 2 inequality constraints</p>
            <p><strong>Bounds:</strong> Non-negativity + upper bounds</p>
            <p><strong>Objective:</strong> Maximize total profit</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Solve Section
    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    st.markdown("## ⚙️ Solve Optimization")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Solve Problem 13.8-5", key="solve_13_8_5"):
            c = -np.array(obj_coeffs)
            A_ub = [constraint1_coeffs, constraint2_coeffs]
            b_ub = [b1, b2]
            
            result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')
            
            display_results_13_8_5(result, variables, obj_coeffs, A_ub, b_ub, bounds)

def problem_13_8_9():
    st.markdown("""
    <div class="problem-card">
        <h2>💰 Problem 13.8-9: Resource Allocation</h2>
        <p><strong>Deskripsi:</strong> Optimalisasi alokasi sumber daya untuk dua produk dengan 
        waktu reguler dan lembur, dengan batasan anggaran dan kapasitas produksi.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # --- TUTORIAL DITAMBAHKAN DI SINI ---
    with st.expander("📖 Panduan Penggunaan - Resource Allocation"):
        st.markdown("""
        Panduan ini membantu Anda memahami cara menggunakan solver untuk masalah alokasi sumber daya.

        #### **1. Pahami Tujuan & Variabel**
        * **Tujuan**: Memaksimalkan total output (jumlah total unit) dari kedua produk.
        * **Variabel Keputusan**:
            * `x₁ᴿ (Reguler P1)`: Jumlah unit Produk 1 yang diproduksi pada waktu reguler.
            * `x₁ᴼ (Lembur P1)`: Jumlah unit Produk 1 yang diproduksi pada waktu lembur.
            * `x₂ᴿ (Reguler P2)`: Jumlah unit Produk 2 yang diproduksi pada waktu reguler.
            * `x₂ᴼ (Lembur P2)`: Jumlah unit Produk 2 yang diproduksi pada waktu lembur.
        
        #### **2. Atur Parameter Input**
        * **Fungsi Tujuan**: Koefisien di sini melambangkan kontribusi setiap unit terhadap total output. Nilai default `1` berarti setiap unit (apapun jenisnya) dihitung sama.
        * **Batasan Anggaran (Budget Constraint)**: Baris ini mendefinisikan batasan biaya.
            * `Cost 1-4`: Masukkan biaya per unit untuk memproduksi setiap jenis produk.
            * `≤ Budget`: Masukkan total anggaran yang tersedia. Total biaya produksi tidak boleh melebihi anggaran ini.
        * **Batasan Kapasitas**: Masukkan batas produksi maksimal untuk setiap jenis produk secara individual (misalnya, kapasitas produksi reguler untuk Produk 1 adalah 2000 unit).

        #### **3. Selesaikan dan Analisis**
        1.  Pastikan semua nilai biaya, anggaran, dan kapasitas sudah benar.
        2.  Klik tombol **"🚀 Solve Problem 13.8-9"**.
        3.  Hasilnya akan muncul di bawah, menunjukkan jumlah unit optimal yang harus diproduksi untuk setiap jenis agar total output maksimal tanpa melebihi anggaran, beserta rincian biayanya.
        """)

    # Input Section
    st.markdown("## 📝 Input Parameters")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Fungsi Tujuan (Maksimalkan Output)")
        
        variables = ['x₁ᴿ (Reguler P1)', 'x₁ᴼ (Lembur P1)', 'x₂ᴿ (Reguler P2)', 'x₂ᴼ (Lembur P2)']
        obj_defaults = [1, 1, 1, 1]
        
        obj_coeffs = []
        cols = st.columns(4)
        for i, (var, default) in enumerate(zip(variables, obj_defaults)):
            with cols[i]:
                coeff = st.number_input(f"**{var}**", value=default, key=f"obj_13_8_9_{i}", help=f"Output coefficient untuk {var}")
                obj_coeffs.append(coeff)
        
        st.markdown("### Batasan Anggaran (Budget Constraint)")
        cost_defaults = [15, 25, 16, 24]
        cost_coeffs = []
        cols = st.columns(5)
        for i, default in enumerate(cost_defaults):
            with cols[i]:
                coeff = st.number_input(f"**Cost {i+1}**", value=default, key=f"cost_13_8_9_{i}", help=f"Biaya per unit untuk variabel {i+1}")
                cost_coeffs.append(coeff)
        with cols[4]:
            cost_limit = st.number_input("**≤ Budget**", value=60000, key="cost_limit_13_8_9", help="Total anggaran yang tersedia")
    
    with col2:
        st.markdown("### Batasan Kapasitas")
        bounds_defaults = [2000, 1000, 1000, 500]
        bounds = []
        for i, (var, default) in enumerate(zip(variables, bounds_defaults)):
            bound = st.number_input(f"**Max {var.split(' ')[0]}**", value=default, key=f"bound_13_8_9_{i}", help=f"Kapasitas maksimum untuk {var}")
            bounds.append((0, bound))
        
        st.markdown("""
        <div class="info-box">
            <h4>📋 Problem Summary</h4>
            <p><strong>Variables:</strong> 4 decision variables</p>
            <p><strong>Constraints:</strong> 1 budget constraint</p>
            <p><strong>Bounds:</strong> Capacity limitations</p>
            <p><strong>Objective:</strong> Maximize total output</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Solve Section
    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    st.markdown("## ⚙️ Solve Optimization")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Solve Problem 13.8-9", key="solve_13_8_9"):
            c = -np.array(obj_coeffs)
            A_ub = [cost_coeffs]
            b_ub = [cost_limit]
            
            result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')
            
            display_results_13_8_9(result, variables, obj_coeffs, cost_coeffs, cost_limit, bounds)

def display_results_13_8_5(result, variables, obj_coeffs, A_ub, b_ub, bounds):
    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    st.markdown("## 📊 Results & Analysis")
    
    if result.success:
        st.markdown("""
        <div class="success-alert">
            ✅ <strong>Optimization Successful!</strong> Solusi optimal telah ditemukan untuk Problem 13.8-5.
        </div>
        """, unsafe_allow_html=True)
        
        row1_col1, row1_col2 = st.columns(2)
        row2_col1, row2_col2 = st.columns(2)

        with row1_col1:
            st.metric("🎯 **Maximum Profit**", f"${-result.fun:,.2f}", help="Nilai maksimum fungsi tujuan")
        
        with row1_col2:
            total_production = sum(result.x)
            st.metric("📈 **Total Production**", f"{total_production:,.0f} units", help="Total unit yang diproduksi")
        
        with row2_col1:
            constraint_usage = np.dot(A_ub, result.x)
            utilization1 = (constraint_usage[0] / b_ub[0]) * 100
            st.metric("⚡ **Constraint 1 Usage**", f"{utilization1:.1f}%", help="Penggunaan batasan 1")
        
        with row2_col2:
            utilization2 = (constraint_usage[1] / b_ub[1]) * 100
            st.metric("🔧 **Constraint 2 Usage**", f"{utilization2:.1f}%", help="Penggunaan batasan 2")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### 📋 Optimal Variable Values")
            results_df = pd.DataFrame({
                'Variable': variables,
                'Optimal Value': [f"{x:.2f}" for x in result.x],
                'Unit Profit ($)': obj_coeffs,
                'Total Profit ($)': [f"{x * c:.2f}" for x, c in zip(result.x, obj_coeffs)]
            })
            st.dataframe(results_df, use_container_width=True, hide_index=True)
            
            st.markdown("### 🔍 Constraint Analysis")
            constraint_usage = np.dot(A_ub, result.x)
            constraint_df = pd.DataFrame({
                'Constraint': ['Total Machine Capacity', 'Production Capacity'],
                'Usage': [f"{u:.2f}" for u in constraint_usage],
                'Limit': b_ub,
                'Slack': [f"{b - u:.2f}" for b, u in zip(b_ub, constraint_usage)],
                'Utilization (%)': [f"{(u/b)*100:.1f}%" for u, b in zip(constraint_usage, b_ub)]
            })
            st.dataframe(constraint_df, use_container_width=True, hide_index=True)
        
        with col2:
            fig1 = px.bar(
                x=[var.split(' ')[0] for var in variables], 
                y=result.x,
                title="Optimal Production Values",
                color=result.x,
                color_continuous_scale="viridis",
                labels={'x': 'Variables', 'y': 'Production Units'}
            )
            fig1.update_layout(showlegend=False, height=300)
            st.plotly_chart(fig1, use_container_width=True)
            
            profit_contrib = result.x * np.array(obj_coeffs)
            fig2 = px.pie(
                values=profit_contrib,
                names=[var.split(' ')[0] for var in variables],
                title="Profit Contribution by Variable"
            )
            fig2.update_layout(height=300)
            st.plotly_chart(fig2, use_container_width=True)
        
    else:
        st.markdown(f"""
        <div class="error-alert">
            ❌ <strong>Optimization Failed:</strong> {result.message}
        </div>
        """, unsafe_allow_html=True)

def display_results_13_8_9(result, variables, obj_coeffs, cost_coeffs, cost_limit, bounds):
    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    st.markdown("## 📊 Results & Analysis")
    
    if result.success:
        st.markdown("""
        <div class="success-alert">
            ✅ <strong>Optimization Successful!</strong> Solusi optimal telah ditemukan untuk Problem 13.8-9.
        </div>
        """, unsafe_allow_html=True)
        
        total_cost = sum(result.x[i] * cost_coeffs[i] for i in range(len(result.x)))
        
        row1_col1, row1_col2 = st.columns(2)
        row2_col1, row2_col2 = st.columns(2)

        with row1_col1:
            st.metric("🎯 **Maximum Output**", f"{-result.fun:,.2f}", help="Nilai maksimum fungsi tujuan")

        with row1_col2:
            st.metric("💰 **Total Cost**", f"${total_cost:,.2f}", help="Total biaya yang digunakan")

        with row2_col1:
            budget_utilization = (total_cost / cost_limit) * 100
            st.metric("📊 **Budget Usage**", f"{budget_utilization:.1f}%", help="Penggunaan anggaran")

        with row2_col2:
            remaining_budget = cost_limit - total_cost
            st.metric("💵 **Remaining Budget**", f"${remaining_budget:,.2f}", help="Sisa anggaran")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### 📋 Optimal Resource Allocation")
            results_df = pd.DataFrame({
                'Variable': variables,
                'Optimal Value': [f"{x:.2f}" for x in result.x],
                'Unit Cost ($)': cost_coeffs,
                'Total Cost ($)': [f"{x * c:.2f}" for x, c in zip(result.x, cost_coeffs)],
                'Capacity Usage (%)': [f"{(x/bound[1])*100:.1f}%" for x, bound in zip(result.x, bounds)]
            })
            st.dataframe(results_df, use_container_width=True, hide_index=True)
            
            st.markdown("### 💰 Budget Analysis")
            budget_df = pd.DataFrame({
                'Item': ['Budget Allocated', 'Budget Used', 'Budget Remaining', 'Budget Utilization'],
                'Value': [f"${cost_limit:,.2f}", f"${total_cost:,.2f}", f"${remaining_budget:,.2f}", f"{budget_utilization:.1f}%"]
            })
            st.dataframe(budget_df, use_container_width=True, hide_index=True)
        
        with col2:
            fig1 = px.bar(
                x=[var.split(' ')[0] for var in variables], 
                y=result.x,
                title="Optimal Resource Allocation",
                color=result.x,
                color_continuous_scale="plasma",
                labels={'x': 'Variables', 'y': 'Allocated Resources'}
            )
            fig1.update_layout(showlegend=False, height=300)
            st.plotly_chart(fig1, use_container_width=True)
            
            cost_values = [result.x[i] * cost_coeffs[i] for i in range(len(result.x))]
            fig2 = px.pie(
                values=cost_values,
                names=[var.split(' ')[0] for var in variables],
                title="Cost Distribution by Variable"
            )
            fig2.update_layout(height=300)
            st.plotly_chart(fig2, use_container_width=True)
        
    else:
        st.markdown(f"""
        <div class="error-alert">
            ❌ <strong>Optimization Failed:</strong> {result.message}
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()