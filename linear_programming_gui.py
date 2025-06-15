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
    "input_parameters_header": {
        "id": "Parameter Input",
        "en": "Input Parameters"
    },
    "solve_optimization_header": {
        "id": "⚙️ Selesaikan Optimisasi",
        "en": "⚙️ Solve Optimization"
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
    "p1_guide_header": {
        "id": "📖 Panduan Penggunaan - Perencanaan Produksi",
        "en": "📖 User Guide - Production Planning"
    },
    "p1_solve_button": {
        "id": "🚀 Selesaikan Masalah Produksi",
        "en": "🚀 Solve Production Problem"
    },
    "p1_obj_func_header": {
        "id": "Fungsi Tujuan (Maksimalkan Profit)",
        "en": "Objective Function (Maximize Profit)"
    },
    "p1_constraints_header": {
        "id": "Batasan (Constraints)",
        "en": "Constraints"
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
        "id": "Batasan Variabel (Bounds)",
        "en": "Variable Bounds"
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
        "id": "🎯 **Profit Maksimum**",
        "en": "🎯 **Maximum Profit**"
    },
    "p1_metric_production": {
        "id": "📈 **Total Produksi**",
        "en": "📈 **Total Production**"
    },
    "p1_metric_c1": {
        "id": "⚡ **Penggunaan Batasan 1**",
        "en": "⚡ **Constraint 1 Usage**"
    },
    "p1_metric_c2": {
        "id": "🔧 **Penggunaan Batasan 2**",
        "en": "🔧 **Constraint 2 Usage**"
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
    "p2_guide_header": {
        "id": "📖 Panduan Penggunaan - Alokasi Sumber Daya",
        "en": "📖 User Guide - Resource Allocation"
    },
    "p2_solve_button": {
        "id": "🚀 Selesaikan Masalah Alokasi",
        "en": "🚀 Solve Allocation Problem"
    },
    "p2_obj_func_header": {
        "id": "Fungsi Tujuan (Maksimalkan Output)",
        "en": "Objective Function (Maximize Output)"
    },
    "p2_budget_header": {
        "id": "Batasan Anggaran (Budget Constraint)",
        "en": "Budget Constraint"
    },
    "p2_capacity_header": {
        "id": "Batasan Kapasitas",
        "en": "Capacity Bounds"
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
        "id": "🎯 **Output Maksimum**",
        "en": "🎯 **Maximum Output**"
    },
    "p2_metric_cost": {
        "id": "💰 **Total Biaya**",
        "en": "💰 **Total Cost**"
    },
    "p2_metric_budget_usage": {
        "id": "📊 **Penggunaan Anggaran**",
        "en": "📊 **Budget Usage**"
    },
    "p2_metric_rem_budget": {
        "id": "💵 **Sisa Anggaran**",
        "en": "💵 **Remaining Budget**"
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
        "id": "✅ **Optimisasi Berhasil!** Solusi optimal telah ditemukan.",
        "en": "✅ **Optimization Successful!** An optimal solution has been found."
    },
    "error_message": {
        "id": "❌ **Optimisasi Gagal:**",
        "en": "❌ **Optimization Failed:**"
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
        "id": "Variabel",
        "en": "Variables"
    },
    "summary_constraints": {
        "id": "Batasan",
        "en": "Constraints"
    },
    "summary_bounds": {
        "id": "Batas",
        "en": "Bounds"
    },
    "summary_objective": {
        "id": "Tujuan",
        "en": "Objective"
    },
}

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
    .main-header { background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 10px; color: white; text-align: center; margin-bottom: 2rem; }
    .problem-card { background: #FFFFFF; padding: 1.5rem; border-radius: 10px; border-left: 5px solid #667eea; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin: 1rem 0; color: #333; }
    .problem-card h2, .problem-card p { color: #333; }
    .info-box { background: #f0f2f6; padding: 1rem; border-radius: 8px; border: 1px solid #dcdcdc; margin: 1rem 0; }
    .metric-card { background: white; padding: 1rem; border-radius: 8px; border-left: 4px solid #667eea; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin: 0.5rem 0; }
    .success-alert { background-color: #d4edda; border: 1px solid #c3e6cb; color: #155724; padding: 1rem; border-radius: 8px; margin: 1rem 0; }
    .error-alert { background-color: #f8d7da; border: 1px solid #f5c6cb; color: #721c24; padding: 1rem; border-radius: 8px; margin: 1rem 0; }
    .stButton > button { background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 8px; padding: 0.5rem 2rem; font-weight: bold; transition: all 0.3s ease; width: 100%; font-family: 'Inter', sans-serif; }
    .stButton > button:hover { transform: translateY(-2px); box-shadow: 0 4px 8px rgba(0,0,0,0.2); }
    .separator { border-top: 3px solid #667eea; margin: 2rem 0; border-radius: 2px; }
</style>
""", unsafe_allow_html=True)

def get_text(key):
    """Helper function to get text based on the current language in session state."""
    lang = st.session_state.get('lang', 'id')
    return TEXTS[key][lang]

def main():
    if 'lang' not in st.session_state:
        st.session_state.lang = 'id'

    with st.sidebar:
        lang_map = {"Bahasa Indonesia": "id", "English": "en"}
        lang_choice = st.radio(
            TEXTS["lang_select_label"],
            lang_map.keys(),
            index=list(lang_map.values()).index(st.session_state.lang)
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
            help=get_text("sidebar_problem_select_help")
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
    
    st.markdown(f"## {get_text('input_parameters_header')}")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"### {get_text('p1_obj_func_header')}")
        variables = ['x₁₁ (Gergaji Reg)', 'x₁₂ (Gergaji OT)', 'x₂₁ (Bor Reg)', 'x₂₂ (Bor OT)']
        obj_defaults = [150, 50, 100, 75]
        
        c_cols = st.columns(4)
        obj_coeffs = []
        for i, (var, default) in enumerate(zip(variables, obj_defaults)):
            with c_cols[i]:
                obj_coeffs.append(st.number_input(f"**{var}**", value=default, key=f"obj_13_8_5_{i}"))
        
        st.markdown(f"### {get_text('p1_constraints_header')}")
        
        st.markdown(f"{get_text('p1_constraint1_label')}")
        a1_defaults = [1, 1, 1, 1]
        constraint1_coeffs = []
        a1_cols = st.columns(5)
        for i, default in enumerate(a1_defaults):
            with a1_cols[i]:
                constraint1_coeffs.append(st.number_input(f"a₁{i+1}", value=default, key=f"c1_13_8_5_{i}"))
        with a1_cols[4]:
            b1 = st.number_input("**≤ RHS₁**", value=10000, key="b1_13_8_5")
        
        st.markdown(f"{get_text('p1_constraint2_label')}")
        a2_defaults = [2, 2, 1, 1]
        constraint2_coeffs = []
        a2_cols = st.columns(5)
        for i, default in enumerate(a2_defaults):
            with a2_cols[i]:
                constraint2_coeffs.append(st.number_input(f"a₂{i+1}", value=default, key=f"c2_13_8_5_{i}"))
        with a2_cols[4]:
            b2 = st.number_input("**≤ RHS₂**", value=15000, key="b2_13_8_5")
    
    with col2:
        st.markdown(f"### {get_text('p1_bounds_header')}")
        bounds_defaults = [3000, 2000, 5000, 3000]
        bounds = []
        for i, (var, default) in enumerate(zip(variables, bounds_defaults)):
            bounds.append((0, st.number_input(f"**Max {var.split(' ')[0]}**", value=default, key=f"bound_13_8_5_{i}")))
        
        st.markdown(f"""
        <div class="info-box">
            <h4>📋 {get_text('problem_summary')}</h4>
            <p><strong>{get_text('summary_vars')}:</strong> 4</p>
            <p><strong>{get_text('summary_constraints')}:</strong> 2</p>
            <p><strong>{get_text('summary_bounds')}:</strong> {get_text('summary_bounds')}</p>
            <p><strong>{get_text('summary_objective')}:</strong> Maximize Profit</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    st.markdown(f"## {get_text('solve_optimization_header')}")
    
    solve_col, _, _ = st.columns([1, 1, 1])
    with solve_col:
        if st.button(get_text('p1_solve_button'), key="solve_13_8_5", use_container_width=True):
            result = linprog(-np.array(obj_coeffs), A_ub=[constraint1_coeffs, constraint2_coeffs], b_ub=[b1, b2], bounds=bounds, method='highs')
            display_results_13_8_5(result, variables, obj_coeffs, [constraint1_coeffs, constraint2_coeffs], [b1, b2], bounds)

def problem_13_8_9():
    st.markdown(f"""
    <div class="problem-card">
        <h2>{get_text('p2_title')}</h2>
        <p><strong>{get_text('p2_desc')}</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"## {get_text('input_parameters_header')}")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"### {get_text('p2_obj_func_header')}")
        variables = ['x₁ᴿ (Reguler P1)', 'x₁ᴼ (Lembur P1)', 'x₂ᴿ (Reguler P2)', 'x₂ᴼ (Lembur P2)']
        obj_defaults = [1, 1, 1, 1]
        c_cols = st.columns(4)
        obj_coeffs = []
        for i, (var, default) in enumerate(zip(variables, obj_defaults)):
            with c_cols[i]:
                obj_coeffs.append(st.number_input(f"**{var}**", value=default, key=f"obj_13_8_9_{i}"))
        
        st.markdown(f"### {get_text('p2_budget_header')}")
        cost_defaults = [15, 25, 16, 24]
        cost_coeffs = []
        cost_cols = st.columns(5)
        for i, default in enumerate(cost_defaults):
            with cost_cols[i]:
                cost_coeffs.append(st.number_input(f"**Cost {i+1}**", value=default, key=f"cost_13_8_9_{i}"))
        with cost_cols[4]:
            cost_limit = st.number_input("**≤ Budget**", value=60000, key="cost_limit_13_8_9")
    
    with col2:
        st.markdown(f"### {get_text('p2_capacity_header')}")
        bounds_defaults = [2000, 1000, 1000, 500]
        bounds = []
        for i, (var, default) in enumerate(zip(variables, bounds_defaults)):
            bounds.append((0, st.number_input(f"**Max {var.split(' ')[0]}**", value=default, key=f"bound_13_8_9_{i}")))
        
        st.markdown(f"""
        <div class="info-box">
            <h4>📋 {get_text('problem_summary')}</h4>
            <p><strong>{get_text('summary_vars')}:</strong> 4</p>
            <p><strong>{get_text('summary_constraints')}:</strong> 1</p>
            <p><strong>{get_text('summary_bounds')}:</strong> {get_text('summary_bounds')}</p>
            <p><strong>{get_text('summary_objective')}:</strong> Maximize Output</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    st.markdown(f"## {get_text('solve_optimization_header')}")
    
    solve_col, _, _ = st.columns([1, 1, 1])
    with solve_col:
        if st.button(get_text('p2_solve_button'), key="solve_13_8_9", use_container_width=True):
            result = linprog(-np.array(obj_coeffs), A_ub=[cost_coeffs], b_ub=[cost_limit], bounds=bounds, method='highs')
            display_results_13_8_9(result, variables, obj_coeffs, cost_coeffs, cost_limit, bounds)

def display_results_13_8_5(result, variables, obj_coeffs, A_ub, b_ub, bounds):
    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    st.markdown(f"## {get_text('results_header')}")
    
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
        res_col1, res_col2 = st.columns(2)
        with res_col1:
            st.markdown(f"### {get_text('optimal_vars_header')}")
            results_df = pd.DataFrame({
                get_text('df_variable_col'): variables,
                get_text('df_optimal_val_col'): [f"{x:.2f}" for x in result.x],
                get_text('p1_df_profit_col'): obj_coeffs,
                get_text('p1_df_totalprofit_col'): [f"{x * c:.2f}" for x, c in zip(result.x, obj_coeffs)]
            })
            st.dataframe(results_df, use_container_width=True, hide_index=True)
            
            st.markdown(f"### {get_text('constraint_analysis_header')}")
            constraint_df = pd.DataFrame({
                get_text('p1_df_constraint_col'): get_text('p1_df_constraints'),
                get_text('df_usage_col'): [f"{u:.2f}" for u in constraint_usage],
                get_text('df_limit_col'): b_ub,
                get_text('df_slack_col'): [f"{b - u:.2f}" for b, u in zip(b_ub, constraint_usage)],
                get_text('df_utilization_col'): [f"{(u/b)*100:.1f}%" for u, b in zip(constraint_usage, b_ub)]
            })
            st.dataframe(constraint_df, use_container_width=True, hide_index=True)
        
        with res_col2:
            fig1 = px.bar(x=[var.split(' ')[0] for var in variables], y=result.x, title=get_text('p1_chart1_title'), labels={'x': get_text('chart_vars_label'), 'y': get_text('chart_units_label')}, color=result.x, color_continuous_scale="viridis")
            st.plotly_chart(fig1, use_container_width=True)
            
            profit_contrib = result.x * np.array(obj_coeffs)
            fig2 = px.pie(values=profit_contrib, names=[var.split(' ')[0] for var in variables], title=get_text('p1_chart2_title'))
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown(f"### {get_text('p1_interpretation_title')}")
        interpretation = get_text('p1_interpretation_text').format(profit=-result.fun, val1=result.x[0], val3=result.x[2])
        st.markdown(f"<div class='success-alert' style='background-color: #e6ffed; border-left: 5px solid #28a745;'>{interpretation}</div>", unsafe_allow_html=True)
        
    else:
        st.markdown(f"<div class='error-alert'>{get_text('error_message')} {result.message}</div>", unsafe_allow_html=True)

def display_results_13_8_9(result, variables, obj_coeffs, cost_coeffs, cost_limit, bounds):
    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    st.markdown(f"## {get_text('results_header')}")
    
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
        res_col1, res_col2 = st.columns(2)
        with res_col1:
            st.markdown(f"### {get_text('optimal_vars_header')}")
            results_df = pd.DataFrame({
                get_text('df_variable_col'): variables,
                get_text('df_optimal_val_col'): [f"{x:.2f}" for x in result.x],
                get_text('p2_df_unitcost_col'): cost_coeffs,
                get_text('p2_df_totalcost_col'): [f"{x * c:.2f}" for x, c in zip(result.x, cost_coeffs)],
                get_text('p2_df_cap_usage_col'): [f"{(x/bound[1])*100:.1f}%" if bound[1] > 0 else "0.0%" for x, bound in zip(result.x, bounds)]
            })
            st.dataframe(results_df, use_container_width=True, hide_index=True)
            
            st.markdown(f"### {get_text('budget_analysis_header')}")
            budget_df = pd.DataFrame({
                get_text('p2_df_budget_item_col'): get_text('p2_df_budget_items'),
                get_text('df_value_col'): [f"${cost_limit:,.2f}", f"${total_cost:,.2f}", f"${remaining_budget:,.2f}", f"{budget_utilization:.1f}%"]
            })
            st.dataframe(budget_df, use_container_width=True, hide_index=True)

        with res_col2:
            fig1 = px.bar(x=[var.split(' ')[0] for var in variables], y=result.x, title=get_text('p2_chart1_title'), labels={'x': get_text('chart_vars_label'), 'y': get_text('chart_resources_label')}, color=result.x, color_continuous_scale="plasma")
            st.plotly_chart(fig1, use_container_width=True)
            
            cost_values = [x * c for x, c in zip(result.x, cost_coeffs)]
            fig2 = px.pie(values=cost_values, names=[var.split(' ')[0] for var in variables], title=get_text('p2_chart2_title'))
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown(f"### {get_text('p2_interpretation_title')}")
        interpretation = get_text('p2_interpretation_text').format(val4=result.x[3], usage=budget_utilization)
        st.markdown(f"<div class='success-alert' style='background-color: #e6ffed; border-left: 5px solid #28a745;'>{interpretation}</div>", unsafe_allow_html=True)
        
    else:
        st.markdown(f"<div class='error-alert'>{get_text('error_message')} {result.message}</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
