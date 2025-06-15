import streamlit as st
import numpy as np
import pandas as pd
from scipy.optimize import linprog
import plotly.graph_objects as go
import plotly.express as px

# Konfigurasi halaman
st.set_page_config(
    page_title="OR Case Study Solver",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# KAMUS TEKS UNTUK MULTI-BAHASA (INDONESIA & INGGRIS)
# ==============================================================================
TEXTS = {
    # Teks Umum & Sidebar
    "lang_select_label": "Pilih Bahasa / Select Language",
    "main_header_title": {
        "id": "📊 Pemecah Studi Kasus Riset Operasi",
        "en": "📊 Operations Research Case Study Solver"
    },
    "main_header_subtitle": {
        "id": "Solusi Optimal untuk Perencanaan Produksi & Alokasi Sumber Daya",
        "en": "Optimal Solutions for Production Planning & Resource Allocation"
    },
    "sidebar_problem_select_header": {
        "id": "🎯 Pilih Masalah",
        "en": "🎯 Select Problem"
    },
    "sidebar_problem_select_help": {
        "id": "Pilih masalah yang ingin diselesaikan",
        "en": "Choose the problem you want to solve"
    },
    "sidebar_info_header": {
        "id": "ℹ️ Informasi",
        "en": "ℹ️ Information"
    },
    "sidebar_method_header": {
        "id": "📚 Metode",
        "en": "📚 Methods"
    },
    "p1_guide_header": {
        "id": "📖 Panduan Penggunaan - Perencanaan Produksi",
        "en": "📖 User Guide - Production Planning"
    },
    "p2_guide_header": {
        "id": "📖 Panduan Penggunaan - Alokasi Sumber Daya",
        "en": "📖 User Guide - Resource Allocation"
    },

    "p1_guide_content": {
        "id": """
    Panduan ini membantu Anda memahami cara menggunakan solver untuk masalah perencanaan produksi.

    #### **1. Pahami Tujuan & Variabel**
    - **Tujuan**: Memaksimalkan total profit dari semua unit yang diproduksi.
    - **Variabel Keputusan**:
        - `x₁₁ (Gergaji Reg)`: Jumlah unit yang diproduksi mesin gergaji pada waktu reguler.
        - `x₁₂ (Gergaji OT)`: Jumlah unit yang diproduksi mesin gergaji pada waktu lembur.
        - `x₂₁ (Bor Reg)`: Jumlah unit yang diproduksi mesin bor pada waktu reguler.
        - `x₂₂ (Bor OT)`: Jumlah unit yang diproduksi mesin bor pada waktu lembur.

    #### **2. Atur Parameter Input**
    - **Fungsi Tujuan**: Masukkan nilai profit yang didapat dari setiap unit produk.
    - **Batasan**: Definisikan batasan sumber daya yang tersedia.
    - **Batasan Variabel**: Masukkan kapasitas produksi maksimal untuk setiap jenis proses.

    #### **3. Selesaikan dan Analisis**
    1. Setelah semua parameter sesuai, klik tombol **Selesaikan Masalah Produksi**.
    2. Hasilnya akan muncul di bawah, menunjukkan alokasi produksi optimal untuk profit maksimal.
    """,
        "en": """
    This guide helps you understand how to use the solver for the production planning problem.

    #### **1. Understand the Goal & Variables**
    - **Goal**: To maximize the total profit from all units produced.
    - **Decision Variables**:
        - `x₁₁ (Gergaji Reg)`: Number of units produced by the saw during regular time.
        - `x₁₂ (Gergaji OT)`: Number of units produced by the saw during overtime.
        - `x₂₁ (Bor Reg)`: Number of units produced by the drill during regular time.
        - `x₂₂ (Bor OT)`: Number of units produced by the drill during overtime.

    #### **2. Set the Input Parameters**
    - **Objective Function**: Enter the profit value gained from each product unit.
    - **Constraints**: Define the resource limitations.
    - **Variable Bounds**: Input the maximum capacity for each specific production type.

    #### **3. Solve and Analyze**
    1. After all parameters are set, click the **Solve Production Problem** button.
    2. The results will appear below, showing the optimal production plan for maximum profit.
    """
    },
    "p2_guide_content": {
        "id": """
    Panduan ini membantu Anda menggunakan solver untuk masalah alokasi sumber daya.

    #### **1. Pahami Tujuan & Variabel**
    - **Tujuan**: Memaksimalkan total output (jumlah total unit) dari kedua produk.
    - **Variabel Keputusan**:
        - `x₁ᴿ (Reguler P1)`: Unit Produk 1 (Waktu Reguler).
        - `x₁ᴼ (Lembur P1)`: Unit Produk 1 (Lembur).
        - `x₂ᴿ (Reguler P2)`: Unit Produk 2 (Waktu Reguler).
        - `x₂ᴼ (Lembur P2)`: Unit Produk 2 (Lembur).

    #### **2. Atur Parameter Input**
    - **Fungsi Tujuan**: Koefisien `1` berarti setiap unit dihitung sama dalam total output.
    - **Batasan Anggaran**: Definisikan biaya per unit dan total anggaran yang tersedia.
    - **Batasan Kapasitas**: Masukkan batas produksi maksimal untuk setiap jenis produk.

    #### **3. Selesaikan dan Analisis**
    1. Pastikan semua nilai biaya, anggaran, dan kapasitas sudah benar.
    2. Klik tombol **Selesaikan Masalah Alokasi**.
    3. Hasilnya akan menunjukkan jumlah unit optimal untuk diproduksi agar total output maksimal sesuai anggaran.
    """,
        "en": """
    This guide helps you use the solver for the resource allocation problem.

    #### **1. Understand the Goal & Variables**
    - **Goal**: To maximize the total output (total number of units) from both products.
    - **Decision Variables**:
        - `x₁ᴿ (Reguler P1)`: Units of Product 1 (Regular time).
        - `x₁ᴼ (Lembur P1)`: Units of Product 1 (Overtime).
        - `x₂ᴿ (Reguler P2)`: Units of Product 2 (Regular time).
        - `x₂ᴼ (Lembur P2)`: Units of Product 2 (Overtime).

    #### **2. Set the Input Parameters**
    - **Objective Function**: The default coefficient of `1` means every unit contributes equally to the total output.
    - **Budget Constraint**: Define the cost per unit and the total available budget.
    - **Capacity Bounds**: Input the maximum production limit for each individual product type.

    #### **3. Solve and Analyze**
    1. Ensure all cost, budget, and capacity values are correct.
    2. Click the **Solve Allocation Problem** button.
    3. The results will show the optimal number of units to produce for maximum output within the budget.
    """
    },
    "input_parameters_header": {
        "id": "⚙️ Parameter Input",
        "en": "⚙️ Input Parameters"
    },
    "solve_optimization_header": {
        "id": "🚀 Selesaikan Optimisasi",
        "en": "🚀 Solve Optimization"
    },

    # Teks untuk Masalah 1: Perencanaan Produksi
    "p1_title": {
        "id": "🏭 Masalah 1: Perencanaan Produksi",
        "en": "🏭 Problem 1: Production Planning"
    },
    "p1_desc": {
        "id": "Perusahaan memproduksi produk menggunakan mesin gergaji dan bor. Setiap mesin memiliki waktu operasi reguler dan lembur dengan profit yang berbeda.",
        "en": "A company manufactures products using a saw and a drill. Each machine has regular and overtime operational hours with different profit margins."
    },
    "p1_info": {
        "id": "**Perencanaan Produksi**: Optimalisasi produksi dengan mesin gergaji dan bor, mempertimbangkan waktu reguler dan lembur.",
        "en": "**Production Planning**: Optimizing production with a saw and a drill, considering regular and overtime hours."
    },
    "p1_solve_button": {
        "id": "Selesaikan Masalah Produksi",
        "en": "Solve Production Problem"
    },
    "p1_obj_func_header": {
        "id": "💰 Fungsi Tujuan (Maksimalkan Profit)",
        "en": "💰 Objective Function (Maximize Profit)"
    },
    "p1_constraints_header": {
        "id": "⚖️ Batasan (Constraints)",
        "en": "⚖️ Constraints"
    },
    "p1_constraint1_label": {
        "id": "**Batasan 1:** Total Kapasitas Mesin",
        "en": "**Constraint 1:** Total Machine Capacity"
    },
    "p1_constraint2_label": {
        "id": "**Batasan 2:** Kapasitas Produksi",
        "en": "**Constraint 2:** Production Capacity"
    },
    "p1_bounds_header": {
        "id": "🔢 Batasan Variabel (Bounds)",
        "en": "🔢 Variable Bounds"
    },
    "p1_df_profit_col": {
        "id": "Profit Unit ($)",
        "en": "Unit Profit ($)"
    },
    "p1_df_totalprofit_col": {
        "id": "Total Profit ($)",
        "en": "Total Profit ($)"
    },
    "p1_df_constraint_col": {
        "id": "Batasan",
        "en": "Constraint"
    },
    "p1_df_constraints": {
        "id": ['Total Kapasitas Mesin', 'Kapasitas Produksi'],
        "en": ['Total Machine Capacity', 'Production Capacity']
    },
    "p1_metric_profit": {
        "id": "Profit Maksimum",
        "en": "Maximum Profit"
    },
    "p1_metric_production": {
        "id": "Total Produksi",
        "en": "Total Production"
    },
    "p1_metric_c1": {
        "id": "Penggunaan Batasan 1",
        "en": "Constraint 1 Usage"
    },
    "p1_metric_c2": {
        "id": "Penggunaan Batasan 2",
        "en": "Constraint 2 Usage"
    },
    "p1_chart1_title": {
        "id": "Nilai Produksi Optimal",
        "en": "Optimal Production Values"
    },
    "p1_chart2_title": {
        "id": "Kontribusi Profit per Variabel",
        "en": "Profit Contribution by Variable"
    },
    "p1_interpretation_title": {
        "id": "💡 Interpretasi Hasil",
        "en": "💡 Result Interpretation"
    },
    "p1_interpretation_text": {
        "id": "Untuk mencapai **profit maksimum sebesar ${profit:,.2f}**, rencana produksi yang optimal adalah dengan **fokus memproduksi {val1:.0f} unit menggunakan Gergaji Reguler dan {val3:.0f} unit menggunakan Bor Reguler** hingga kapasitas maksimalnya. Produksi lembur (`Gergaji OT` dan `Bor OT`) tidak digunakan sama sekali, menandakan bahwa opsi ini tidak efisien secara biaya dibandingkan produksi reguler. Rencana ini sepenuhnya memanfaatkan kapasitas produksi yang ada (`Batasan 2` terpakai 100%), menunjukkan alokasi sumber daya yang sangat efisien.",
        "en": "To achieve the **maximum profit of ${profit:,.2f}**, the optimal production plan is to **focus on producing {val1:.0f} units using the Regular Saw and {val3:.0f} units using the Regular Drill** to their maximum capacities. Overtime production (`Gergaji OT` and `Bor OT`) is not utilized at all, indicating it is not cost-effective compared to regular production. This plan fully utilizes the available production capacity (`Constraint 2` is at 100% usage), demonstrating a highly efficient allocation of resources."
    },

    # Teks untuk Masalah 2: Alokasi Sumber Daya
    "p2_title": {
        "id": "💰 Masalah 2: Alokasi Sumber Daya",
        "en": "💰 Problem 2: Resource Allocation"
    },
    "p2_desc": {
        "id": "Optimalisasi alokasi sumber daya untuk dua produk dengan waktu reguler dan lembur, dengan batasan anggaran dan kapasitas produksi.",
        "en": "Optimizing resource allocation for two products with regular and overtime hours, subject to a budget and production capacity constraints."
    },
    "p2_info": {
        "id": "**Alokasi Sumber Daya**: Optimalisasi alokasi sumber daya dengan batasan anggaran dan kapasitas produksi.",
        "en": "**Resource Allocation**: Optimizing resource allocation with a budget constraint and production capacities."
    },
    "p2_solve_button": {
        "id": "Selesaikan Masalah Alokasi",
        "en": "Solve Allocation Problem"
    },
    "p2_obj_func_header": {
        "id": "📊 Fungsi Tujuan (Maksimalkan Output)",
        "en": "📊 Objective Function (Maximize Output)"
    },
    "p2_budget_header": {
        "id": "💸 Batasan Anggaran (Budget Constraint)",
        "en": "💸 Budget Constraint"
    },
    "p2_capacity_header": {
        "id": "🔢 Batasan Kapasitas",
        "en": "🔢 Capacity Bounds"
    },
    "p2_df_unitcost_col": {
        "id": "Biaya Unit ($)",
        "en": "Unit Cost ($)"
    },
    "p2_df_totalcost_col": {
        "id": "Total Biaya ($)",
        "en": "Total Cost ($)"
    },
    "p2_df_cap_usage_col": {
        "id": "Penggunaan Kapasitas (%)",
        "en": "Capacity Usage (%)"
    },
    "p2_df_budget_item_col": {
        "id": "Item",
        "en": "Item"
    },
    "p2_df_budget_items": {
        "id": ['Anggaran Dialokasikan', 'Anggaran Terpakai', 'Sisa Anggaran', 'Utilisasi Anggaran'],
        "en": ['Budget Allocated', 'Budget Used', 'Budget Remaining', 'Budget Utilization']
    },
    "p2_metric_output": {
        "id": "Output Maksimum",
        "en": "Maximum Output"
    },
    "p2_metric_cost": {
        "id": "Total Biaya",
        "en": "Total Cost"
    },
    "p2_metric_budget_usage": {
        "id": "Penggunaan Anggaran",
        "en": "Budget Usage"
    },
    "p2_metric_rem_budget": {
        "id": "Sisa Anggaran",
        "en": "Remaining Budget"
    },
    "p2_chart1_title": {
        "id": "Alokasi Sumber Daya Optimal",
        "en": "Optimal Resource Allocation"
    },
    "p2_chart2_title": {
        "id": "Distribusi Biaya per Variabel",
        "en": "Cost Distribution by Variable"
    },
    "p2_interpretation_title": {
        "id": "💡 Interpretasi Hasil",
        "en": "💡 Result Interpretation"
    },
    "p2_interpretation_text": {
        "id": "Untuk memaksimalkan total output, strategi terbaik adalah **memanfaatkan penuh opsi produksi termurah terlebih dahulu**. Dalam kasus ini, produksi `Reguler P1` (biaya $15) dan `Reguler P2` (biaya $16) digunakan hingga kapasitas maksimalnya. Sisa anggaran kemudian dialokasikan untuk memproduksi {val4:.0f} unit `Lembur P2` (biaya $24), karena ini adalah opsi termurah berikutnya yang tersedia. Produksi `Lembur P1` (biaya $25) tidak digunakan sama sekali. Strategi ini berhasil **menghabiskan seluruh anggaran** ({usage:.1f}%) untuk mendapatkan output setinggi mungkin.",
        "en": "To maximize total output, the best strategy is to **fully utilize the cheapest production options first**. In this case, `Regular P1` (cost $15) and `Regular P2` (cost $16) are used to their maximum capacity. The remaining budget is then allocated to produce {val4:.0f} units of `Overtime P2` (cost $24), as it's the next cheapest available option. `Overtime P1` (cost $25) is not used at all. This strategy successfully **exhausts the entire budget** ({usage:.1f}%) to achieve the highest possible output."
    },

    # Teks Umum Hasil
    "results_header": {
        "id": "📊 Hasil & Analisis",
        "en": "📊 Results & Analysis"
    },
    "success_message": {
        "id": "✅ Optimisasi Berhasil! Solusi optimal telah ditemukan.",
        "en": "✅ Optimization Successful! An optimal solution has been found."
    },
    "error_message": {
        "id": "❌ Optimisasi Gagal:",
        "en": "❌ Optimization Failed:"
    },
    "optimal_vars_header": {
        "id": "📋 Nilai Variabel Optimal",
        "en": "📋 Optimal Variable Values"
    },
    "constraint_analysis_header": {
        "id": "🔍 Analisis Batasan",
        "en": "🔍 Constraint Analysis"
    },
    "budget_analysis_header": {
        "id": "💰 Analisis Anggaran",
        "en": "💰 Budget Analysis"
    },
    "df_variable_col": {
        "id": "Variabel",
        "en": "Variable"
    },
    "df_optimal_val_col": {
        "id": "Nilai Optimal",
        "en": "Optimal Value"
    },
    "df_usage_col": {
        "id": "Penggunaan",
        "en": "Usage"
    },
    "df_limit_col": {
        "id": "Batas",
        "en": "Limit"
    },
    "df_slack_col": {
        "id": "Sisa (Slack)",
        "en": "Slack"
    },
    "df_utilization_col": {
        "id": "Utilisasi (%)",
        "en": "Utilization (%)"
    },
    "df_value_col": {
        "id": "Nilai",
        "en": "Value"
    },
     "chart_vars_label": {
        "id": "Variabel",
        "en": "Variables"
    },
    "chart_units_label": {
        "id": "Unit Produksi",
        "en": "Production Units"
    },
    "chart_resources_label": {
        "id": "Sumber Daya Dialokasikan",
        "en": "Allocated Resources"
    },
    "problem_summary": {
        "id": "Ringkasan Masalah",
        "en": "Problem Summary"
    },
    "summary_vars": {
        "id": "Variabel Keputusan",
        "en": "Decision Variables"
    },
    "summary_constraints": {
        "id": "Batasan Pertidaksamaan",
        "en": "Inequality Constraints"
    },
    "summary_bounds": {
        "id": "Batasan Kapasitas",
        "en": "Capacity Limitations"
    },
    "summary_objective": {
        "id": "Tujuan",
        "en": "Objective"
    },
}

# Enhanced Custom CSS with better typography and layout
st.markdown("""
<style>
    /* Import fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* Root variables for consistent theming */
    :root {
        --primary-color: #667eea;
        --secondary-color: #764ba2;
        --accent-color: #f093fb;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --error-color: #ef4444;
        --text-primary: #1f2937;
        --text-secondary: #6b7280;
        --bg-primary: #ffffff;
        --bg-secondary: #f8fafc;
        --border-color: #e5e7eb;
        --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
        --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
        --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
        --border-radius: 12px;
        --border-radius-sm: 8px;
        --spacing-xs: 0.25rem;
        --spacing-sm: 0.5rem;
        --spacing-md: 1rem;
        --spacing-lg: 1.5rem;
        --spacing-xl: 2rem;
        --spacing-2xl: 3rem;
    }
    
    /* Global typography improvements */
    html, body, [class*="st-"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        font-size: 16px;
        line-height: 1.6;
        color: var(--text-primary);
    }
    
    /* Headers with better hierarchy */
    h1, h2, h3, h4, h5, h6 {
        font-weight: 600;
        line-height: 1.3;
        margin-bottom: var(--spacing-md);
        color: var(--text-primary);
    }
    
    h1 { font-size: 2.5rem; font-weight: 700; }
    h2 { font-size: 2rem; font-weight: 600; }
    h3 { font-size: 1.75rem; font-weight: 600; }
    h4 { font-size: 1.5rem; font-weight: 600; }
    h5 { font-size: 1.25rem; font-weight: 500; }
    h6 { font-size: 1.125rem; font-weight: 500; }
    
    /* Enhanced main header */
    .main-header {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 50%, var(--accent-color) 100%);
        padding: var(--spacing-2xl);
        border-radius: var(--border-radius);
        color: white;
        text-align: center;
        margin-bottom: var(--spacing-2xl);
        box-shadow: var(--shadow-lg);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, transparent 100%);
        pointer-events: none;
    }
    
    .main-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: var(--spacing-sm);
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
        color: white;
    }
    
    .main-header p {
        font-size: 1.2rem;
        font-weight: 400;
        opacity: 0.95;
        margin: 0;
        color: white;
    }
    
    /* Enhanced problem cards */
    .problem-card {
        background: var(--bg-primary);
        padding: var(--spacing-xl);
        border-radius: var(--border-radius);
        border-left: 6px solid var(--primary-color);
        box-shadow: var(--shadow-md);
        margin: var(--spacing-xl) 0;
        transition: all 0.3s ease;
        position: relative;
    }
    
    .problem-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }
    
    .problem-card h2 {
        color: var(--text-primary);
        font-size: 1.75rem;
        font-weight: 600;
        margin-bottom: var(--spacing-md);
    }
    
    .problem-card p {
        color: var(--text-secondary);
        font-size: 1.1rem;
        line-height: 1.7;
        margin: 0;
    }
    
    /* Enhanced info boxes */
    .info-box {
        background: linear-gradient(135deg, var(--bg-secondary) 0%, rgba(102, 126, 234, 0.05) 100%);
        padding: var(--spacing-lg);
        border-radius: var(--border-radius);
        border: 2px solid rgba(102, 126, 234, 0.1);
        margin: var(--spacing-lg) 0;
        box-shadow: var(--shadow-sm);
    }
    
    .info-box h4 {
        color: var(--text-primary);
        font-size: 1.25rem;
        font-weight: 600;
        margin-bottom: var(--spacing-md);
    }
    
    .info-box p {
        color: var(--text-secondary);
        font-size: 1rem;
        margin-bottom: var(--spacing-sm);
        font-weight: 500;
    }
    
    .info-box p:last-child {
        margin-bottom: 0;
    }
    
    /* Enhanced alerts */
    .success-alert {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(16, 185, 129, 0.05) 100%);
        border: 2px solid rgba(16, 185, 129, 0.2);
        color: #065f46;
        padding: var(--spacing-lg);
        border-radius: var(--border-radius);
        margin: var(--spacing-lg) 0;
        font-size: 1.1rem;
        font-weight: 500;
        box-shadow: var(--shadow-sm);
    }
    
    .error-alert {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(239, 68, 68, 0.05) 100%);
        border: 2px solid rgba(239, 68, 68, 0.2);
        color: #7f1d1d;
        padding: var(--spacing-lg);
        border-radius: var(--border-radius);
        margin: var(--spacing-lg) 0;
        font-size: 1.1rem;
        font-weight: 500;
        box-shadow: var(--shadow-sm);
    }
    
    /* Enhanced buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        color: white;
        border: none;
        border-radius: var(--border-radius);
        padding: var(--spacing-lg) var(--spacing-2xl);
        font-size: 1.2rem;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: var(--shadow-md);
        text-transform: none;
        letter-spacing: 0.025em;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: var(--shadow-lg);
        background: linear-gradient(135deg, #5a6fd8 0%, #6b4190 100%);
    }
    
    .stButton > button:active {
        transform: translateY(-1px);
    }
    
    /* Enhanced separators */
    .separator {
        border: none;
        height: 3px;
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        margin: var(--spacing-2xl) 0;
        border-radius: 2px;
        box-shadow: var(--shadow-sm);
    }
    
    /* Enhanced sidebar */
    .css-1d391kg {
        background-color: var(--bg-secondary);
        border-right: 2px solid var(--border-color);
    }
    
    /* Enhanced input fields */
    .stNumberInput > div > div > input {
        border-radius: var(--border-radius-sm);
        border: 2px solid var(--border-color);
        padding: var(--spacing-sm) var(--spacing-md);
        font-size: 1rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Enhanced dataframes */
    .stDataFrame {
        border-radius: var(--border-radius);
        overflow: hidden;
        box-shadow: var(--shadow-md);
        border: none;
    }
    
    .stDataFrame thead th {
        background-color: var(--primary-color);
        color: white;
        font-weight: 600;
        font-size: 1rem;
        padding: var(--spacing-md);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .stDataFrame tbody tr:nth-child(even) {
        background-color: var(--bg-secondary);
    }

    .stDataFrame tbody tr:hover {
        background-color: rgba(102, 126, 234, 0.1);
    }
    
    .stDataFrame td {
        font-size: 0.95rem;
        font-weight: 500;
        padding: var(--spacing-sm) var(--spacing-md);
        border-bottom: 1px solid var(--border-color);
    }

    /* Enhanced metrics */
    [data-testid="stMetric"] {
        background: var(--bg-primary);
        border: 2px solid var(--border-color);
        padding: var(--spacing-lg);
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-sm);
        transition: all 0.2s ease;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
        border-color: var(--primary-color);
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        color: var(--text-secondary) !important;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 2.25rem !important;
        font-weight: 700 !important;
        color: var(--primary-color) !important;
    }
    
    /* Enhanced section headers */
    .section-header {
        font-size: 1.75rem;
        font-weight: 600;
        color: var(--text-primary);
        margin: var(--spacing-xl) 0 var(--spacing-lg) 0;
        padding-bottom: var(--spacing-sm);
        border-bottom: 3px solid var(--primary-color);
        display: inline-block;
    }
    
    /* Responsive improvements */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        
        .main-header p {
            font-size: 1rem;
        }
        
        .main-header {
            padding: var(--spacing-lg);
        }
        
        .problem-card {
            padding: var(--spacing-lg);
        }
    }
    
    /* Enhanced plotly charts */
    .js-plotly-plot {
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-sm);
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# Helper functions
def get_text(key):
    lang = st.session_state.get('lang', 'id')
    return TEXTS[key][lang]

def format_interpretation(text):
    """Replaces markdown bold with HTML strong tags for safe rendering."""
    return text.replace('**', '<strong>').replace('**', '</strong>')

# Main application logic
def main():
    if 'lang' not in st.session_state:
        st.session_state.lang = 'id'

    with st.sidebar:
        lang_map = {"Bahasa Indonesia": "id", "English": "en"}
        lang_choice = st.radio(
            TEXTS["lang_select_label"],
            lang_map.keys(),
            index=list(lang_map.values()).index(st.session_state.lang),
            key="lang_radio"
        )
        st.session_state.lang = lang_map[lang_choice]

        st.markdown(f"### {get_text('sidebar_problem_select_header')}")
        problem_options = {
            "p1": get_text("p1_title"),
            "p2": get_text("p2_title")
        }
        problem_key = st.selectbox(
            "Problem:",
            options=problem_options.keys(),
            format_func=lambda key: problem_options[key],
            label_visibility="collapsed",
            help=get_text("sidebar_problem_select_help"),
            key="problem_selectbox"
        )
        
        st.markdown("---")
        st.markdown(f"### {get_text('sidebar_info_header')}")
        st.info(get_text(f"{problem_key}_info"))
        
        st.markdown(f"### {get_text('sidebar_method_header')}")
        st.markdown("- **Algorithm**: Simplex\n- **Solver**: SciPy HiGHS\n- **Type**: Linear Programming")
    
    st.markdown(f"""
    <div class="main-header">
        <h1>{get_text('main_header_title')}</h1>
        <p>{get_text('main_header_subtitle')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if problem_key == "p1":
        problem_13_8_5()
    else:
        problem_13_8_9()

def problem_13_8_5():
    st.markdown(f"""
    <div class="problem-card">
        <h2>{get_text('p1_title')}</h2>
        <p><strong>{get_text('p1_desc')}</strong></p>
    </div>
    """, unsafe_allow_html=True)
    with st.expander(get_text('p1_guide_header')):
        st.markdown(get_text('p1_guide_content'))    
    st.markdown(f'<h2 class="section-header">{get_text("input_parameters_header")}</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"<h5>{get_text('p1_obj_func_header')}</h5>", unsafe_allow_html=True)
        variables = ['x₁₁ (Gergaji Reg)', 'x₁₂ (Gergaji OT)', 'x₂₁ (Bor Reg)', 'x₂₂ (Bor OT)']
        obj_defaults = [150, 50, 100, 75]
        
        c_cols = st.columns(4)
        obj_coeffs = []
        for i, (var, default) in enumerate(zip(variables, obj_defaults)):
            with c_cols[i]:
                obj_coeffs.append(st.number_input(f"**{var}**", value=default, key=f"obj_13_8_5_{i}"))
        
        st.markdown(f"<h5>{get_text('p1_constraints_header')}</h5>", unsafe_allow_html=True)
        
        st.write(f"**{get_text('p1_constraint1_label')}**")
        a1_defaults = [1, 1, 1, 1]
        constraint1_coeffs = []
        a1_cols = st.columns(5)
        for i, default in enumerate(a1_defaults):
            with a1_cols[i]:
                constraint1_coeffs.append(st.number_input(f"a₁{i+1}", value=default, key=f"c1_13_8_5_{i}", label_visibility="collapsed"))
        with a1_cols[4]:
            b1 = st.number_input("**≤ RHS₁**", value=10000, key="b1_13_8_5", label_visibility="collapsed")
        
        st.write(f"**{get_text('p1_constraint2_label')}**")
        a2_defaults = [2, 2, 1, 1]
        constraint2_coeffs = []
        a2_cols = st.columns(5)
        for i, default in enumerate(a2_defaults):
            with a2_cols[i]:
                constraint2_coeffs.append(st.number_input(f"a₂{i+1}", value=default, key=f"c2_13_8_5_{i}", label_visibility="collapsed"))
        with a2_cols[4]:
            b2 = st.number_input("**≤ RHS₂**", value=15000, key="b2_13_8_5", label_visibility="collapsed")
    
    with col2:
        st.markdown(f"<h5>{get_text('p1_bounds_header')}</h5>", unsafe_allow_html=True)
        bounds_defaults = [3000, 2000, 5000, 3000]
        bounds = []
        for i, (var, default) in enumerate(zip(variables, bounds_defaults)):
            bounds.append((0, st.number_input(f"**Max {var.split(' ')[0]}**", value=default, key=f"bound_13_8_5_{i}")))
        
        st.markdown(f"""
        <div class="info-box">
            <h4>{get_text('problem_summary')}</h4>
            <p><strong>{get_text('summary_vars')}:</strong> 4</p>
            <p><strong>{get_text('summary_constraints')}:</strong> 2</p>
            <p><strong>{get_text('summary_bounds')}:</strong> {get_text('summary_bounds')}</p>
            <p><strong>{get_text('summary_objective')}:</strong> Maximize Profit</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    st.markdown(f'<h2 class="section-header">{get_text("solve_optimization_header")}</h2>', unsafe_allow_html=True)
    
    _, solve_col, _ = st.columns([1, 2, 1])
    with solve_col:
        if st.button(get_text('p1_solve_button'), key="solve_13_8_5"):
            result = linprog(-np.array(obj_coeffs), A_ub=[constraint1_coeffs, constraint2_coeffs], b_ub=[b1, b2], bounds=bounds, method='highs')
            display_results_13_8_5(result, variables, obj_coeffs, [constraint1_coeffs, constraint2_coeffs], [b1, b2], bounds)

def problem_13_8_9():
    st.markdown(f"""
    <div class="problem-card">
        <h2>{get_text('p2_title')}</h2>
        <p><strong>{get_text('p2_desc')}</strong></p>
    </div>
    """, unsafe_allow_html=True)
    with st.expander(get_text('p2_guide_header')):
        st.markdown(get_text('p2_guide_content'))    
    st.markdown(f'<h2 class="section-header">{get_text("input_parameters_header")}</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"<h5>{get_text('p2_obj_func_header')}</h5>", unsafe_allow_html=True)
        variables = ['x₁ᴿ (Reguler P1)', 'x₁ᴼ (Lembur P1)', 'x₂ᴿ (Reguler P2)', 'x₂ᴼ (Lembur P2)']
        obj_defaults = [1, 1, 1, 1]
        c_cols = st.columns(4)
        obj_coeffs = []
        for i, (var, default) in enumerate(zip(variables, obj_defaults)):
            with c_cols[i]:
                obj_coeffs.append(st.number_input(f"**{var}**", value=default, key=f"obj_13_8_9_{i}"))
        
        st.markdown(f"<h5>{get_text('p2_budget_header')}</h5>", unsafe_allow_html=True)
        cost_defaults = [15, 25, 16, 24]
        cost_coeffs = []
        cost_cols = st.columns(5)
        for i, default in enumerate(cost_defaults):
            with cost_cols[i]:
                cost_coeffs.append(st.number_input(f"**Cost {i+1}**", value=default, key=f"cost_13_8_9_{i}", label_visibility="collapsed"))
        with cost_cols[4]:
            cost_limit = st.number_input("**≤ Budget**", value=60000, key="cost_limit_13_8_9", label_visibility="collapsed")
    
    with col2:
        st.markdown(f"<h5>{get_text('p2_capacity_header')}</h5>", unsafe_allow_html=True)
        bounds_defaults = [2000, 1000, 1000, 500]
        bounds = []
        for i, (var, default) in enumerate(zip(variables, bounds_defaults)):
            bounds.append((0, st.number_input(f"**Max {var.split(' ')[0]}**", value=default, key=f"bound_13_8_9_{i}")))
        
        st.markdown(f"""
        <div class="info-box">
            <h4>{get_text('problem_summary')}</h4>
            <p><strong>{get_text('summary_vars')}:</strong> 4</p>
            <p><strong>{get_text('summary_constraints')}:</strong> 1</p>
            <p><strong>{get_text('summary_bounds')}:</strong> {get_text('summary_bounds')}</p>
            <p><strong>{get_text('summary_objective')}:</strong> Maximize Output</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    st.markdown(f'<h2 class="section-header">{get_text("solve_optimization_header")}</h2>', unsafe_allow_html=True)
    
    _, solve_col, _ = st.columns([1, 2, 1])
    with solve_col:
        if st.button(get_text('p2_solve_button'), key="solve_13_8_9"):
            result = linprog(-np.array(obj_coeffs), A_ub=[cost_coeffs], b_ub=[cost_limit], bounds=bounds, method='highs')
            display_results_13_8_9(result, variables, obj_coeffs, cost_coeffs, cost_limit, bounds)

def display_results_13_8_5(result, variables, obj_coeffs, A_ub, b_ub, bounds):
    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    st.markdown(f'<h2 class="section-header">{get_text("results_header")}</h2>', unsafe_allow_html=True)
    
    if result.success:
        st.markdown(f"<div class='success-alert'>{get_text('success_message')}</div>", unsafe_allow_html=True)
        
        row1_col1, row1_col2 = st.columns(2)
        row2_col1, row2_col2 = st.columns(2)
        with row1_col1:
            st.metric(get_text('p1_metric_profit'), f"${-result.fun:,.2f}")
        with row1_col2:
            st.metric(get_text('p1_metric_production'), f"{sum(result.x):,.0f} units")
        constraint_usage = np.dot(A_ub, result.x)
        with row2_col1:
            st.metric(get_text('p1_metric_c1'), f"{(constraint_usage[0] / b_ub[0]) * 100:.1f}%")
        with row2_col2:
            st.metric(get_text('p1_metric_c2'), f"{(constraint_usage[1] / b_ub[1]) * 100:.1f}%")
        
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"<h5>{get_text('optimal_vars_header')}</h5>", unsafe_allow_html=True)
            results_df = pd.DataFrame({
                get_text('df_variable_col'): variables,
                get_text('df_optimal_val_col'): [f"{x:.2f}" for x in result.x],
                get_text('p1_df_profit_col'): obj_coeffs,
                get_text('p1_df_totalprofit_col'): [f"{x * c:.2f}" for x, c in zip(result.x, obj_coeffs)]
            })
            st.dataframe(results_df, use_container_width=True, hide_index=True)
            
            st.markdown(f"<h5>{get_text('constraint_analysis_header')}</h5>", unsafe_allow_html=True)
            constraint_df = pd.DataFrame({
                get_text('p1_df_constraint_col'): get_text('p1_df_constraints'),
                get_text('df_usage_col'): [f"{u:.2f}" for u in constraint_usage],
                get_text('df_limit_col'): b_ub,
                get_text('df_slack_col'): [f"{b - u:.2f}" for b, u in zip(b_ub, constraint_usage)],
                get_text('df_utilization_col'): [f"{(u/b)*100:.1f}%" for u, b in zip(constraint_usage, b_ub)]
            })
            st.dataframe(constraint_df, use_container_width=True, hide_index=True)
        
        with col2:
            fig1 = px.bar(x=[var.split(' ')[0] for var in variables], y=result.x, title=get_text('p1_chart1_title'), labels={'x': get_text('chart_vars_label'), 'y': get_text('chart_units_label')}, color=result.x, color_continuous_scale="viridis")
            st.plotly_chart(fig1, use_container_width=True)
            
            profit_contrib = result.x * np.array(obj_coeffs)
            fig2 = px.pie(values=profit_contrib, names=[var.split(' ')[0] for var in variables], title=get_text('p1_chart2_title'))
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown(f'<h3 class="section-header" style="border-bottom: none; margin-bottom: 0;">{get_text("p1_interpretation_title")}</h3>', unsafe_allow_html=True)
        raw_text = get_text('p1_interpretation_text').format(profit=-result.fun, val1=result.x[0], val3=result.x[2])
        formatted_text = format_interpretation(raw_text)
        st.markdown(f"<div class='success-alert'>{formatted_text}</div>", unsafe_allow_html=True)
        
    else:
        st.markdown(f"<div class='error-alert'>{get_text('error_message')} {result.message}</div>", unsafe_allow_html=True)

def display_results_13_8_9(result, variables, obj_coeffs, cost_coeffs, cost_limit, bounds):
    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    st.markdown(f'<h2 class="section-header">{get_text("results_header")}</h2>', unsafe_allow_html=True)
    
    if result.success:
        st.markdown(f"<div class='success-alert'>{get_text('success_message')}</div>", unsafe_allow_html=True)
        
        total_cost = np.dot(result.x, cost_coeffs)
        budget_utilization = (total_cost / cost_limit) * 100 if cost_limit > 0 else 0
        remaining_budget = cost_limit - total_cost

        row1_col1, row1_col2 = st.columns(2)
        row2_col1, row2_col2 = st.columns(2)
        with row1_col1:
            st.metric(get_text('p2_metric_output'), f"{-result.fun:,.2f}")
        with row1_col2:
            st.metric(get_text('p2_metric_cost'), f"${total_cost:,.2f}")
        with row2_col1:
            st.metric(get_text('p2_metric_budget_usage'), f"{budget_utilization:.1f}%")
        with row2_col2:
            st.metric(get_text('p2_metric_rem_budget'), f"${remaining_budget:,.2f}")
        
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"<h5>{get_text('optimal_vars_header')}</h5>", unsafe_allow_html=True)
            results_df = pd.DataFrame({
                get_text('df_variable_col'): variables,
                get_text('df_optimal_val_col'): [f"{x:.2f}" for x in result.x],
                get_text('p2_df_unitcost_col'): cost_coeffs,
                get_text('p2_df_totalcost_col'): [f"{x * c:.2f}" for x, c in zip(result.x, cost_coeffs)],
                get_text('p2_df_cap_usage_col'): [f"{(x/bound[1])*100:.1f}%" if bound[1] > 0 else "0.0%" for x, bound in zip(result.x, bounds)]
            })
            st.dataframe(results_df, use_container_width=True, hide_index=True)
            
            st.markdown(f"<h5>{get_text('budget_analysis_header')}</h5>", unsafe_allow_html=True)
            budget_df = pd.DataFrame({
                get_text('p2_df_budget_item_col'): get_text('p2_df_budget_items'),
                get_text('df_value_col'): [f"${cost_limit:,.2f}", f"${total_cost:,.2f}", f"${remaining_budget:,.2f}", f"{budget_utilization:.1f}%"]
            })
            st.dataframe(budget_df, use_container_width=True, hide_index=True)

        with col2:
            fig1 = px.bar(x=[var.split(' ')[0] for var in variables], y=result.x, title=get_text('p2_chart1_title'), labels={'x': get_text('chart_vars_label'), 'y': get_text('chart_resources_label')}, color=result.x, color_continuous_scale="plasma")
            st.plotly_chart(fig1, use_container_width=True)
            
            cost_values = [x * c for x, c in zip(result.x, cost_coeffs)]
            fig2 = px.pie(values=cost_values, names=[var.split(' ')[0] for var in variables], title=get_text('p2_chart2_title'))
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown(f'<h3 class="section-header" style="border-bottom: none; margin-bottom: 0;">{get_text("p2_interpretation_title")}</h3>', unsafe_allow_html=True)
        raw_text = get_text('p2_interpretation_text').format(val4=result.x[3], usage=budget_utilization)
        formatted_text = format_interpretation(raw_text)
        st.markdown(f"<div class='success-alert'>{formatted_text}</div>", unsafe_allow_html=True)
        
    else:
        st.markdown(f"<div class='error-alert'>{get_text('error_message')} {result.message}</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
