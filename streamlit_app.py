import streamlit as st
import matplotlib.pyplot as plt
from math import factorial
from datetime import datetime
import io

from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle, Image, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT


# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="EngsetPro Professional",
    page_icon="📡",
    layout="wide"
)


# =========================
# UNPIX MOBILE-RESPONSIVE UI STYLE
# =========================
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Poppins:wght@400;500;600;700&display=swap');

/* ── Global Reset ── */
* { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #EEF4FF;
    font-family: 'Nunito', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background: linear-gradient(160deg, #dbeafe 0%, #EEF4FF 40%, #f0f9ff 100%);
    min-height: 100vh;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1d4ed8 0%, #1e40af 60%, #1e3a8a 100%) !important;
    border-right: none !important;
    box-shadow: 4px 0 24px rgba(29,78,216,0.18);
}

[data-testid="stSidebar"] > div {
    padding-top: 1.5rem !important;
}

[data-testid="stSidebar"] * {
    color: #e0eaff !important;
    font-family: 'Nunito', sans-serif !important;
}

/* ── Sidebar navigation label header ── */
[data-testid="stSidebar"] .stRadio > label {
    color: #93c5fd !important;
    font-size: 12px !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    padding-bottom: 8px !important;
    display: block;
    margin-bottom: 4px;
}

/* ── Sidebar radio items ── */
[data-testid="stSidebar"] .stRadio [data-testid="stWidgetLabel"] {
    color: #93c5fd !important;
    font-size: 12px !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 8px;
}

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
    display: flex;
    flex-direction: column;
    gap: 6px;
}

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
    background: rgba(255,255,255,0.08) !important;
    border-radius: 14px !important;
    padding: 12px 16px !important;
    margin: 0 !important;
    transition: background 0.2s;
    font-weight: 700 !important;
    font-size: 14px !important;
    display: flex !important;
    align-items: center !important;
    width: 100% !important;
    cursor: pointer;
    border: 1.5px solid transparent;
}

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
    background: rgba(255,255,255,0.16) !important;
    border-color: rgba(255,255,255,0.15) !important;
}

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label[data-checked="true"],
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] [aria-checked="true"] ~ label {
    background: rgba(255,255,255,0.22) !important;
    border-color: rgba(255,255,255,0.3) !important;
}

/* Radio dot color */
[data-testid="stSidebar"] .stRadio [data-testid="stMarkdownContainer"] p {
    color: #93c5fd !important;
    font-size: 12px;
    line-height: 1.5;
}

[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.15) !important;
    margin: 16px 0 !important;
}

/* Sidebar info box */
[data-testid="stSidebar"] [data-testid="stAlert"] {
    background: rgba(255,255,255,0.10) !important;
    border: 1px solid rgba(255,255,255,0.18) !important;
    border-radius: 14px !important;
    color: #bfdbfe !important;
}

[data-testid="stSidebar"] [data-testid="stAlert"] * {
    color: #bfdbfe !important;
    font-size: 13px !important;
}

/* ── Header Banner ── */
.unpix-header {
    background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 50%, #3b82f6 100%);
    border-radius: 24px;
    padding: 28px 32px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 12px;
    box-shadow: 0 8px 32px rgba(29,78,216,0.28);
    position: relative;
    overflow: hidden;
}

.unpix-header::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 180px; height: 180px;
    background: rgba(255,255,255,0.07);
    border-radius: 50%;
    pointer-events: none;
}

.unpix-header::after {
    content: '';
    position: absolute;
    bottom: -60px; right: 60px;
    width: 240px; height: 240px;
    background: rgba(255,255,255,0.05);
    border-radius: 50%;
    pointer-events: none;
}

.header-app-name {
    font-family: 'Poppins', sans-serif;
    font-size: 12px;
    font-weight: 600;
    color: #93c5fd;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 4px;
}

.header-title {
    font-family: 'Poppins', sans-serif;
    font-size: 28px;
    font-weight: 800;
    color: #ffffff;
    line-height: 1.1;
    margin: 0;
}

.header-subtitle {
    font-size: 13px;
    color: #bfdbfe;
    margin-top: 6px;
    font-weight: 500;
}

.header-badge {
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 50px;
    padding: 8px 20px;
    color: white;
    font-size: 13px;
    font-weight: 700;
    backdrop-filter: blur(8px);
    white-space: nowrap;
}

/* ── Section Title ── */
.section-title {
    font-family: 'Poppins', sans-serif;
    font-size: 16px;
    font-weight: 700;
    color: #1e40af;
    margin: 20px 0 12px 0;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ── Card ── */
.unpix-card {
    background: #ffffff;
    border-radius: 20px;
    padding: 24px;
    border: 1px solid rgba(219,234,254,0.8);
    box-shadow: 0 4px 20px rgba(29,78,216,0.07);
    margin-bottom: 16px;
}

/* ── Metric Cards — responsive grid ── */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin: 16px 0;
}

@media (max-width: 900px) {
    .metric-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 480px) {
    .metric-grid {
        grid-template-columns: 1fr 1fr;
        gap: 8px;
    }
    .header-title { font-size: 20px; }
    .unpix-header { padding: 20px 18px; }
}

.metric-card {
    background: white;
    border-radius: 18px;
    padding: 18px 12px;
    border: 1.5px solid #dbeafe;
    box-shadow: 0 4px 16px rgba(29,78,216,0.07);
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s, box-shadow 0.2s;
}

.metric-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(29,78,216,0.13);
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    background: linear-gradient(90deg, #1d4ed8, #3b82f6);
    border-radius: 18px 18px 0 0;
}

.metric-icon {
    width: 42px; height: 42px;
    border-radius: 14px;
    background: linear-gradient(135deg, #dbeafe, #eff6ff);
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
    margin: 0 auto 10px auto;
}

.metric-value {
    font-family: 'Poppins', sans-serif;
    font-size: 20px;
    font-weight: 800;
    color: #1e40af;
    line-height: 1;
    word-break: break-all;
}

.metric-label {
    font-size: 10px;
    color: #64748b;
    font-weight: 700;
    margin-top: 4px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.metric-card.green::before { background: linear-gradient(90deg, #16a34a, #4ade80); }
.metric-card.green .metric-value { color: #15803d; }
.metric-card.red::before { background: linear-gradient(90deg, #dc2626, #f87171); }
.metric-card.red .metric-value { color: #b91c1c; }
.metric-card.orange::before { background: linear-gradient(90deg, #d97706, #fbbf24); }
.metric-card.orange .metric-value { color: #b45309; }

/* ── Status Badge ── */
.status-optimal {
    display: inline-block;
    background: linear-gradient(135deg, #dcfce7, #bbf7d0);
    color: #15803d;
    border: 1.5px solid #86efac;
    border-radius: 50px;
    padding: 3px 12px;
    font-size: 11px;
    font-weight: 700;
}

.status-congested {
    display: inline-block;
    background: linear-gradient(135deg, #fee2e2, #fecaca);
    color: #b91c1c;
    border: 1.5px solid #fca5a5;
    border-radius: 50px;
    padding: 3px 12px;
    font-size: 11px;
    font-weight: 700;
}

/* ── Input styling ── */
[data-testid="stNumberInput"] input {
    border-radius: 14px !important;
    border: 2px solid #dbeafe !important;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 600 !important;
    color: #1e40af !important;
    background: #f8faff !important;
    padding: 10px 14px !important;
    font-size: 16px !important;
    transition: border-color 0.2s !important;
}

[data-testid="stNumberInput"] input:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.12) !important;
}

[data-testid="stNumberInput"] label {
    font-family: 'Nunito', sans-serif !important;
    font-weight: 700 !important;
    color: #374151 !important;
    font-size: 14px !important;
}

/* ── Button ── */
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 16px !important;
    padding: 14px 36px !important;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    letter-spacing: 0.5px;
    box-shadow: 0 4px 16px rgba(29,78,216,0.30) !important;
    transition: all 0.2s !important;
    width: 100%;
}

[data-testid="stButton"] > button:hover {
    background: linear-gradient(135deg, #1e40af 0%, #1d4ed8 100%) !important;
    box-shadow: 0 8px 24px rgba(29,78,216,0.40) !important;
    transform: translateY(-2px);
}

/* ── Download Button ── */
[data-testid="stDownloadButton"] > button {
    background: linear-gradient(135deg, #0f766e, #0d9488) !important;
    color: white !important;
    border-radius: 16px !important;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 700 !important;
    box-shadow: 0 4px 16px rgba(15,118,110,0.30) !important;
    width: 100%;
}

/* ── Divider ── */
hr {
    border-color: #dbeafe !important;
    margin: 20px 0 !important;
}

/* ── DataFrame ── */
[data-testid="stDataFrame"] {
    border-radius: 16px !important;
    overflow: hidden;
    border: 1.5px solid #dbeafe !important;
}

/* ── Alert / Info ── */
[data-testid="stAlert"] {
    border-radius: 16px !important;
    border: none !important;
    font-family: 'Nunito', sans-serif !important;
}

/* ── Plot ── */
[data-testid="stImage"] {
    border-radius: 16px;
}

/* ── Input card ── */
.input-card {
    background: white;
    border-radius: 20px;
    padding: 20px 24px 24px;
    border: 1.5px solid #dbeafe;
    box-shadow: 0 4px 20px rgba(29,78,216,0.06);
    margin-bottom: 20px;
}

.input-label {
    font-family: 'Poppins', sans-serif;
    font-size: 13px;
    font-weight: 700;
    color: #1d4ed8;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ── Page Headings ── */
h2, h3 {
    font-family: 'Poppins', sans-serif !important;
    color: #1e40af !important;
    font-weight: 700 !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #eff6ff; }
::-webkit-scrollbar-thumb { background: #93c5fd; border-radius: 10px; }

/* ── Column gap fix for mobile ── */
[data-testid="stHorizontalBlock"] {
    gap: 12px !important;
}

</style>
""", unsafe_allow_html=True)


# =========================
# ENGSET MODEL
# =========================
def nCr(n, r):
    if r > n:
        return 0
    return factorial(n) // (factorial(r) * factorial(n - r))


def engset_pb(S, N, M):
    num = nCr(S - 1, N) * (M ** N)
    den = sum(nCr(S - 1, k) * (M ** k) for k in range(N + 1))
    return num / den if den != 0 else 0


def iterate(S, N, rho):
    M = rho
    tol = 0.0001
    data = []

    i = 1
    while True:
        Pb = engset_pb(S, N, M)
        M_new = rho * (1 - Pb)
        diff = abs(M_new - M)

        data.append([i, round(M, 16), round(Pb, 16), round(diff, 16)])

        if diff < tol:
            break

        M = M_new
        i += 1

    return M_new, Pb, data, i


# =========================
# SESSION STATE
# =========================
if "history" not in st.session_state:
    st.session_state.history = []


# =========================
# HEADER — UNPIX style
# =========================
st.markdown("""
<div class="unpix-header">
    <div class="header-left">
        <div class="header-app-name">📡 EngsetPro</div>
        <div class="header-title">Engset Simulator</div>
        <div class="header-subtitle">Professional Blocking Probability Analysis System</div>
    </div>
    <div class="header-badge">✦ Pro Edition</div>
</div>
""", unsafe_allow_html=True)


# =========================
# SIDEBAR NAV
# =========================
with st.sidebar:
    st.markdown(
        '<div style="font-family:Poppins,sans-serif;font-size:11px;font-weight:700;'
        'color:#93c5fd;text-transform:uppercase;letter-spacing:2px;'
        'margin-bottom:10px;padding:0 4px;">Navigation</div>',
        unsafe_allow_html=True
    )
    page = st.radio(
        "",
        ["🏠 Dashboard", "📊 Analysis", "📁 History"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.info("Engineering Simulation Tool")


# =========================
# DASHBOARD
# =========================
if page == "🏠 Dashboard":

    st.markdown('<div class="input-card"><div class="input-label">📥 Input Parameters</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1], gap="medium")

    with col1:
        S = st.number_input("Number of Sources (S)", min_value=1, value=10)

    with col2:
        N = st.number_input("Number of Channels (N)", min_value=1, value=3)

    with col3:
        rho = st.number_input("Traffic per Source (ρ)", min_value=0.0, value=0.5, step=0.01, format="%.2f")

    st.markdown('</div>', unsafe_allow_html=True)

    btn_col, _ = st.columns([1, 2])
    with btn_col:
        run = st.button("🚀 RUN ANALYSIS")

    if run:
        if N >= S:
            st.error("⚠️ Channel (N) must be smaller than Source (S). Please adjust your values.")
        else:
            M, Pb, iter_data, iters = iterate(S, N, rho)
            status = "OPTIMAL" if Pb < 0.2 else "CONGESTED"

            st.session_state.result = {
                "S": S, "N": N, "rho": rho,
                "M": M, "Pb": Pb, "status": status,
                "iter": iters, "iter_data": iter_data,
                "time": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            }
            st.session_state.history.append(st.session_state.result)

    # RESULT DASHBOARD
    if "result" in st.session_state:
        r = st.session_state.result
        status_class = "status-optimal" if r['status'] == "OPTIMAL" else "status-congested"

        st.markdown('<div class="section-title">📊 Results Overview</div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="metric-grid">
            <div class="metric-card {'green' if r['status'] == 'OPTIMAL' else 'red'}">
                <div class="metric-icon">🔒</div>
                <div class="metric-value">{r['Pb']:.6f}</div>
                <div class="metric-label">Blocking Prob.</div>
            </div>
            <div class="metric-card">
                <div class="metric-icon">📶</div>
                <div class="metric-value">{r['M']:.6f}</div>
                <div class="metric-label">Traffic Idle (M)</div>
            </div>
            <div class="metric-card orange">
                <div class="metric-icon">🔄</div>
                <div class="metric-value">{r['iter']}</div>
                <div class="metric-label">Iterations</div>
            </div>
            <div class="metric-card {'green' if r['status'] == 'OPTIMAL' else 'red'}">
                <div class="metric-icon">{'✅' if r['status'] == 'OPTIMAL' else '⚠️'}</div>
                <div class="metric-value"><span class="{status_class}">{r['status']}</span></div>
                <div class="metric-label">System Status</div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# =========================
# ANALYSIS PAGE
# =========================
elif page == "📊 Analysis":

    st.markdown('<div class="section-title">📊 System Analysis</div>', unsafe_allow_html=True)

    if "result" not in st.session_state:
        st.warning("⚠️ No simulation data. Please run an analysis on the Dashboard first.")
    else:
        r = st.session_state.result

        st.markdown('<div class="section-title">🔁 Convergence Iteration Table</div>', unsafe_allow_html=True)

        import pandas as pd
        df = pd.DataFrame(r["iter_data"], columns=["Iter", "M", "Pb", "Diff"])
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.markdown('<div class="section-title">📈 Blocking Probability Graph</div>', unsafe_allow_html=True)

        S = r["S"]
        rho = r["rho"]

        x = list(range(1, S))
        y = [engset_pb(S, n, rho) for n in x]

        fig, ax = plt.subplots(figsize=(10, 4))
        fig.patch.set_facecolor('#f8faff')
        ax.set_facecolor('#f8faff')

        ax.fill_between(x, y, alpha=0.15, color="#1d4ed8")
        ax.plot(x, y, linewidth=2.5, color="#1d4ed8", marker='o',
                markersize=5, markerfacecolor='white', markeredgewidth=2)
        ax.axhline(0.2, linestyle="--", color="#ef4444", linewidth=1.5, label="Threshold (0.2)")

        ax.set_xlabel("Number of Channels", fontsize=12, color="#374151", fontweight='bold')
        ax.set_ylabel("Blocking Probability", fontsize=12, color="#374151", fontweight='bold')
        ax.grid(True, color='#dbeafe', linewidth=1)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#dbeafe')
        ax.spines['bottom'].set_color('#dbeafe')
        ax.tick_params(colors='#64748b')
        ax.legend(fontsize=11)

        st.pyplot(fig)


# =========================
# HISTORY PAGE
# =========================
elif page == "📁 History":

    st.markdown('<div class="section-title">📁 Simulation History</div>', unsafe_allow_html=True)

    if st.session_state.history:
        import pandas as pd

        rows = []
        for i, r in enumerate(st.session_state.history, 1):
            rows.append({
                "#": i,
                "Time": r["time"],
                "S": r["S"],
                "N": r["N"],
                "ρ": r["rho"],
                "M": round(r["M"], 6),
                "Pb": round(r["Pb"], 6),
                "Iter": r["iter"],
                "Status": r["status"]
            })

        df_hist = pd.DataFrame(rows)
        st.dataframe(df_hist, use_container_width=True, hide_index=True)

    else:
        st.info("📭 No history yet. Run a simulation on the Dashboard first.")

    st.markdown("---")

    # =========================
    # PROFESSIONAL PDF EXPORT
    # =========================
    def export_pdf(data, fig):
        buffer = io.BytesIO()

        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            leftMargin=2*cm,
            rightMargin=2*cm,
            topMargin=2.5*cm,
            bottomMargin=2.5*cm,
        )

        styles = getSampleStyleSheet()

        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontName='Helvetica-Bold',
            fontSize=20,
            spaceAfter=6,
            textColor=colors.HexColor("#1d4ed8"),
            alignment=TA_CENTER,
        )

        subtitle_style = ParagraphStyle(
            'Subtitle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=11,
            spaceAfter=20,
            textColor=colors.HexColor("#64748b"),
            alignment=TA_CENTER,
        )

        heading2_style = ParagraphStyle(
            'CustomH2',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=13,
            spaceBefore=16,
            spaceAfter=8,
            textColor=colors.HexColor("#1e40af"),
        )

        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            leading=18,
            textColor=colors.HexColor("#374151"),
        )

        label_style = ParagraphStyle(
            'LabelStyle',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=10,
            leading=18,
            textColor=colors.HexColor("#1e40af"),
        )

        elements = []

        # ── Title block ──
        elements.append(Paragraph("ENGSETPRO SIMULATION REPORT", title_style))
        elements.append(Paragraph("Professional Engset Blocking Probability Analysis", subtitle_style))
        elements.append(HRFlowable(width="100%", thickness=1.5,
                                   color=colors.HexColor("#1d4ed8"), spaceAfter=12))

        # ── 1. System Parameters ──
        elements.append(Paragraph("1. System Parameters", heading2_style))

        param_data = [
            ["Parameter", "Value"],
            ["Sources (S)", str(data['S'])],
            ["Channels (N)", str(data['N'])],
            ["Traffic per Source (ρ)", str(data['rho'])],
            ["Idle Traffic (M)", f"{data['M']:.6f}"],
            ["Blocking Probability (Pb)", f"{data['Pb']:.6f}"],
            ["System Status", data['status']],
            ["Iterations", str(data['iter'])],
            ["Timestamp", data['time']],
        ]

        param_table = Table(param_data, colWidths=[7*cm, 9*cm])
        param_table.setStyle(TableStyle([
            # Header row
            ("BACKGROUND",   (0, 0), (-1, 0), colors.HexColor("#1d4ed8")),
            ("TEXTCOLOR",    (0, 0), (-1, 0), colors.white),
            ("FONTNAME",     (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE",     (0, 0), (-1, 0), 10),
            ("ALIGN",        (0, 0), (-1, 0), "CENTER"),
            # Data rows
            ("FONTNAME",     (0, 1), (0, -1), "Helvetica-Bold"),
            ("FONTNAME",     (1, 1), (1, -1), "Helvetica"),
            ("FONTSIZE",     (0, 1), (-1, -1), 10),
            ("TEXTCOLOR",    (0, 1), (0, -1), colors.HexColor("#1e40af")),
            ("TEXTCOLOR",    (1, 1), (1, -1), colors.HexColor("#374151")),
            # Zebra rows
            ("ROWBACKGROUNDS", (0, 1), (-1, -1),
             [colors.HexColor("#f8faff"), colors.white]),
            # Grid
            ("GRID",         (0, 0), (-1, -1), 0.5, colors.HexColor("#dbeafe")),
            ("LINEBELOW",    (0, 0), (-1, 0), 1.5, colors.HexColor("#1d4ed8")),
            # Padding
            ("TOPPADDING",   (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING",(0, 0), (-1, -1), 7),
            ("LEFTPADDING",  (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
            # Status color
            ("TEXTCOLOR",    (1, 6), (1, 6),
             colors.HexColor("#15803d") if data['status'] == "OPTIMAL"
             else colors.HexColor("#b91c1c")),
            ("FONTNAME",     (1, 6), (1, 6), "Helvetica-Bold"),
        ]))

        elements.append(param_table)
        elements.append(Spacer(1, 16))

        # ── 2. Iteration Convergence ──
        elements.append(Paragraph("2. Iteration Convergence", heading2_style))

        col_widths = [2*cm, 5*cm, 5*cm, 4*cm]
        iter_header = [["Iter", "M", "Pb", "Diff"]]
        iter_rows = [[str(row[0]),
                      f"{row[1]:.10f}",
                      f"{row[2]:.10f}",
                      f"{row[3]:.2e}"] for row in data["iter_data"]]
        table_data = iter_header + iter_rows

        iter_table = Table(table_data, colWidths=col_widths, repeatRows=1)
        iter_table.setStyle(TableStyle([
            # Header
            ("BACKGROUND",   (0, 0), (-1, 0), colors.HexColor("#1d4ed8")),
            ("TEXTCOLOR",    (0, 0), (-1, 0), colors.white),
            ("FONTNAME",     (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE",     (0, 0), (-1, 0), 9),
            ("ALIGN",        (0, 0), (-1, 0), "CENTER"),
            # Data
            ("FONTNAME",     (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE",     (0, 1), (-1, -1), 8),
            ("ALIGN",        (0, 1), (-1, -1), "CENTER"),
            ("ROWBACKGROUNDS",(0, 1), (-1, -1),
             [colors.HexColor("#f8faff"), colors.white]),
            ("GRID",         (0, 0), (-1, -1), 0.4, colors.HexColor("#dbeafe")),
            ("LINEBELOW",    (0, 0), (-1, 0), 1.5, colors.HexColor("#1d4ed8")),
            ("TOPPADDING",   (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING",(0, 0), (-1, -1), 5),
            ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
        ]))

        elements.append(iter_table)
        elements.append(Spacer(1, 16))

        # ── 3. Blocking Probability Graph ──
        elements.append(Paragraph("3. Blocking Probability Graph", heading2_style))

        img_buf = io.BytesIO()
        fig.savefig(img_buf, format="png", dpi=180, bbox_inches='tight',
                    facecolor='#f8faff')
        img_buf.seek(0)

        chart_img = Image(img_buf, width=16*cm, height=8*cm)
        elements.append(chart_img)
        elements.append(Spacer(1, 16))

        # ── 4. Conclusion ──
        elements.append(HRFlowable(width="100%", thickness=1,
                                   color=colors.HexColor("#dbeafe"), spaceAfter=8))
        elements.append(Paragraph("4. Conclusion", heading2_style))

        color_word = "#15803d" if data['status'] == "OPTIMAL" else "#b91c1c"
        conclusion = (
            f'Based on the Engset iterative model with <b>S={data["S"]}</b> sources, '
            f'<b>N={data["N"]}</b> channels, and traffic intensity <b>ρ={data["rho"]}</b>, '
            f'the system converged in <b>{data["iter"]} iterations</b>. '
            f'The calculated blocking probability is <b>{data["Pb"]:.6f}</b> '
            f'with idle traffic <b>M={data["M"]:.6f}</b>. '
            f'The system is classified as '
            f'<font color="{color_word}"><b>{data["status"]}</b></font>.'
        )
        elements.append(Paragraph(conclusion, body_style))

        # Footer spacer
        elements.append(Spacer(1, 20))
        elements.append(HRFlowable(width="100%", thickness=0.5,
                                   color=colors.HexColor("#dbeafe"), spaceAfter=4))

        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=8,
            textColor=colors.HexColor("#94a3b8"),
            alignment=TA_CENTER,
        )
        elements.append(Paragraph(
            f"Generated by EngsetPro Professional · {data['time']}",
            footer_style
        ))

        doc.build(elements)
        buffer.seek(0)
        return buffer

    # Export button
    if st.button("📥 EXPORT PROFESSIONAL REPORT"):
        if st.session_state.history:
            last = st.session_state.history[-1]
            S = last["S"]
            rho = last["rho"]

            x = list(range(1, S))
            y = [engset_pb(S, n, rho) for n in x]

            fig, ax = plt.subplots(figsize=(10, 4))
            fig.patch.set_facecolor('#f8faff')
            ax.set_facecolor('#f8faff')
            ax.fill_between(x, y, alpha=0.15, color="#1d4ed8")
            ax.plot(x, y, linewidth=2.5, color="#1d4ed8", marker='o',
                    markersize=5, markerfacecolor='white', markeredgewidth=2)
            ax.axhline(0.2, linestyle="--", color="#ef4444",
                       linewidth=1.5, label="Threshold (0.2)")
            ax.set_xlabel("Number of Channels", fontsize=11,
                          color="#374151", fontweight='bold')
            ax.set_ylabel("Blocking Probability", fontsize=11,
                          color="#374151", fontweight='bold')
            ax.grid(True, color='#dbeafe', linewidth=1)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('#dbeafe')
            ax.spines['bottom'].set_color('#dbeafe')
            ax.tick_params(colors='#64748b')
            ax.legend(fontsize=10)

            pdf = export_pdf(last, fig)

            st.download_button(
                "⬇️ Download Professional PDF",
                data=pdf,
                file_name="EngsetPro_Professional_Report.pdf",
                mime="application/pdf"
            )
        else:
            st.error("⚠️ No data to export. Run a simulation first.")


# =====================================================
# PDF EXPORT
# =====================================================

def export_pdf(data, fig):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
        rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    elements = []
    elements.append(Paragraph('LAPORAN SIMULASI ENGSET', styles['Title']))
    elements.append(Spacer(1, 12))
    info = (
        '<b>Jumlah Sumber (S):</b> ' + str(data['S']) + '<br/>'
        '<b>Jumlah Kanal (N):</b> ' + str(data['N']) + '<br/>'
        '<b>Traffic Offered (A):</b> ' + str(data['A']) + '<br/>'
        '<b>Probabilitas Blocking (P):</b> ' + '{:.6f}'.format(data['Pb']) + '<br/>'
        '<b>Status:</b> ' + data['status'] + '<br/>'
        '<b>Waktu:</b> ' + data['time'] + '<br/>'
    )
    elements.append(Paragraph(info, styles['BodyText']))
    elements.append(Spacer(1, 15))
    tabel = [['Jumlah Kanal (N)', 'Probabilitas Blocking (P)']]
    for row in data['tabel_data']:
        tabel.append(row)
    t = Table(tabel)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.blue),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('ALIGN', (0,0), (-1,-1), 'CENTER')
    ]))
    elements.append(t)
    elements.append(Spacer(1, 20))
    img_buf = io.BytesIO()
    fig.savefig(img_buf, format='png')
    img_buf.seek(0)
    elements.append(Image(img_buf, width=15*cm, height=7*cm))
    doc.build(elements)
    buffer.seek(0)
    return buffer


# =====================================================
# SESSION STATE
# =====================================================

if 'history' not in st.session_state:
    st.session_state.history = []

# =====================================================
# HEADER
# =====================================================

header_html = "<div class='unpix-header'>\n    <div class='header-title'>\U0001f310 Kalkulator Engset</div>\n    <div class='header-subtitle'>Sistem Analisis Probabilitas Blocking Telekomunikasi</div>\n</div>"
st.markdown(header_html, unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:
    st.title('\U0001f4c2 Navigasi')
    page = st.radio('Pilih Menu', ['\U0001f3e0 Dashboard', '\U0001f4ca Analisis', '\U0001f4c1 Riwayat'])

# =====================================================
# DASHBOARD
# =====================================================

if page == '\U0001f3e0 Dashboard':

    st.markdown('<div class="section-title">\U0001f4e5 Input Parameter Sistem</div>', unsafe_allow_html=True)
    st.markdown('<div class="input-card">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        S = st.number_input('Jumlah Sumber (S)', min_value=2, value=10)
    with col2:
        N = st.number_input('Jumlah Kanal (N)', min_value=1, value=3)
    with col3:
        A = st.number_input('Traffic Offered (A)',
            min_value=0.01, max_value=float(S - 1),
            value=min(5.0, float(S - 1)), step=0.01,
            help='Nilai A harus lebih kecil dari S')
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button('\U0001f680 Jalankan Analisis'):
        if N >= S:
            st.error('\u274c Jumlah kanal (N) harus lebih kecil dari jumlah sumber (S).')
        elif A >= S:
            st.error('\u274c Traffic offered (A) harus lebih kecil dari jumlah sumber (S).')
        else:
            Pb = engset_pb(S, N, A)
            status = 'OPTIMAL' if Pb < 0.2 else 'PADAT'
            tabel_data = []
            for n_val in range(1, S):
                tabel_data.append([n_val, round(engset_pb(S, n_val, A), 6)])
            result = {
                'S': S, 'N': N, 'A': A, 'Pb': Pb,
                'status': status, 'tabel_data': tabel_data,
                'time': datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            }
            st.session_state.result = result
            st.session_state.history.append(result)

    if 'result' in st.session_state:
        r = st.session_state.result
        st.markdown('<div class="section-title">\U0001f4ca Hasil Simulasi</div>', unsafe_allow_html=True)
        pb_str = '{:.6f}'.format(r['Pb'])
        a_str  = str(r['A'])
        n_str  = str(r['N'])
        st_str = r['status']
        st.markdown(
            '<div class="metric-grid">'
            '<div class="metric-card"><div class="metric-value">' + pb_str + '</div>'
            '<div class="metric-label">Probabilitas Blocking (P)</div></div>'
            '<div class="metric-card"><div class="metric-value">' + a_str + '</div>'
            '<div class="metric-label">Traffic Offered (A)</div></div>'
            '<div class="metric-card"><div class="metric-value">' + n_str + '</div>'
            '<div class="metric-label">Jumlah Kanal (N)</div></div>'
            '<div class="metric-card"><div class="metric-value">' + st_str + '</div>'
            '<div class="metric-label">Status Sistem</div></div>'
            '</div>',
            unsafe_allow_html=True
        )

# =====================================================
# ANALISIS
# =====================================================

elif page == '\U0001f4ca Analisis':

    if 'result' not in st.session_state:
        st.warning('\u26a0\ufe0f Jalankan simulasi terlebih dahulu di menu Dashboard.')
    else:
        r = st.session_state.result
        st.markdown('<div class="section-title">\U0001f501 Tabel Probabilitas Blocking per Jumlah Kanal</div>', unsafe_allow_html=True)
        df = pd.DataFrame(r['tabel_data'], columns=['Jumlah Kanal (N)', 'Probabilitas Blocking (P)'])
        st.dataframe(df, use_container_width=True)
        st.markdown('<div class="section-title">\U0001f4c8 Grafik Probabilitas Blocking</div>', unsafe_allow_html=True)
        x = [row[0] for row in r['tabel_data']]
        y = [row[1] for row in r['tabel_data']]
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(x, y, marker='o', linewidth=2, label='Probabilitas Blocking (P)')
        ax.axhline(0.2, linestyle='--', color='red', label='Batas Threshold (P = 0.2)')
        ax.axvline(r['N'], linestyle=':', color='green', label='N terpilih = ' + str(r['N']))
        ax.set_xlabel('Jumlah Kanal (N)')
        ax.set_ylabel('Probabilitas Blocking (P)')
        ax.set_title('Grafik Probabilitas Blocking Engset')
        ax.grid(True)
        ax.legend()
        st.pyplot(fig)

# =====================================================
# RIWAYAT
# =====================================================

elif page == '\U0001f4c1 Riwayat':

    if st.session_state.history:
        rows = []
        for i, r in enumerate(st.session_state.history, 1):
            rows.append({
                'No': i, 'Waktu': r['time'],
                'S': r['S'], 'N': r['N'], 'A': r['A'],
                'P (Blocking)': round(r['Pb'], 6),
                'Status': r['status']
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True)
    else:
        st.info('\u2139\ufe0f Belum ada riwayat simulasi.')

# =====================================================
# EXPORT PDF
# =====================================================

if 'result' in st.session_state:
    st.markdown('---')
    st.markdown('<div class="section-title">\U0001f4e5 Export PDF</div>', unsafe_allow_html=True)
    latest = st.session_state.result
    x = [row[0] for row in latest['tabel_data']]
    y = [row[1] for row in latest['tabel_data']]
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(x, y, marker='o', linewidth=2)
    ax.axhline(0.2, linestyle='--', color='red', label='Threshold P = 0.2')
    ax.set_xlabel('Jumlah Kanal (N)')
    ax.set_ylabel('Probabilitas Blocking (P)')
    ax.set_title('Grafik Probabilitas Blocking Engset')
    ax.grid(True)
    ax.legend()
    pdf = export_pdf(latest, fig)
    st.download_button(
        label='\u2b07\ufe0f Download Laporan PDF',
        data=pdf,
        file_name='Laporan_Engset.pdf',
        mime='application/pdf'
        )    background: white; padding: 20px; border-radius: 20px;
    margin-bottom: 20px; box-shadow: 0px 4px 20px rgba(0,0,0,0.1);
}
</style>
''', unsafe_allow_html=True)

# =====================================================
# FUNGSI ENGSET
# Rumus dosen:
#   P = [C(S-1,N) * (A/(S-A))^N]
#      / [SUM i=0..N  C(S-1,i) * (A/(S-A))^i]
# S = Jumlah sumber, N = Jumlah kanal, A = Traffic offered
# =====================================================

def nCr(n, r):
    if r > n or r < 0:
        return 0
    return factorial(n) // (factorial(r) * factorial(n - r))


def engset_pb(S, N, A):
    ratio = A / (S - A)
    numerator = nCr(S - 1, N) * (ratio ** N)
    denominator = sum(nCr(S - 1, i) * (ratio ** i) for i in range(N + 1))
    return numerator / denominator


# =====================================================
# PDF EXPORT
# =====================================================

def export_pdf(data, fig):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
        rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    elements = []
    elements.append(Paragraph('LAPORAN SIMULASI ENGSET', styles['Title']))
    elements.append(Spacer(1, 12))
    info = (
        '<b>Jumlah Sumber (S):</b> ' + str(data['S']) + '<br/>'
        '<b>Jumlah Kanal (N):</b> ' + str(data['N']) + '<br/>'
        '<b>Traffic Offered (A):</b> ' + str(data['A']) + '<br/>'
        '<b>Probabilitas Blocking (P):</b> ' + '{:.6f}'.format(data['Pb']) + '<br/>'
        '<b>Status:</b> ' + data['status'] + '<br/>'
        '<b>Waktu:</b> ' + data['time'] + '<br/>'
    )
    elements.append(Paragraph(info, styles['BodyText']))
    elements.append(Spacer(1, 15))
    tabel = [['Jumlah Kanal (N)', 'Probabilitas Blocking (P)']]
    for row in data['tabel_data']:
        tabel.append(row)
    t = Table(tabel)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.blue),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('ALIGN', (0,0), (-1,-1), 'CENTER')
    ]))
    elements.append(t)
    elements.append(Spacer(1, 20))
    img_buf = io.BytesIO()
    fig.savefig(img_buf, format='png')
    img_buf.seek(0)
    elements.append(Image(img_buf, width=15*cm, height=7*cm))
    doc.build(elements)
    buffer.seek(0)
    return buffer


# =====================================================
# SESSION STATE
# =====================================================

if 'history' not in st.session_state:
    st.session_state.history = []

# =====================================================
# HEADER
# =====================================================

st.markdown('''
<div class='unpix-header'>
    <div class='header-title'>\U0001f310 Kalkulator Engset</div>
    <div class='header-subtitle'>Sistem Analisis Probabilitas Blocking Telekomunikasi</div>
</div>
''', unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:
    st.title('\U0001f4c2 Navigasi')
    page = st.radio('Pilih Menu', ['\U0001f3e0 Dashboard', '\U0001f4ca Analisis', '\U0001f4c1 Riwayat'])

# =====================================================
# DASHBOARD
# =====================================================

if page == '\U0001f3e0 Dashboard':

    st.markdown('<div class="section-title">\U0001f4e5 Input Parameter Sistem</div>', unsafe_allow_html=True)
    st.markdown('<div class="input-card">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        S = st.number_input('Jumlah Sumber (S)', min_value=2, value=10)
    with col2:
        N = st.number_input('Jumlah Kanal (N)', min_value=1, value=3)
    with col3:
        A = st.number_input('Traffic Offered (A)',
            min_value=0.01, max_value=float(S - 1),
            value=min(5.0, float(S - 1)), step=0.01,
            help='Nilai A harus lebih kecil dari S')

    st.markdown('</div>', unsafe_allow_html=True)

    if st.button('\U0001f680 Jalankan Analisis'):
        if N >= S:
            st.error('\u274c Jumlah kanal (N) harus lebih kecil dari jumlah sumber (S).')
        elif A >= S:
            st.error('\u274c Traffic offered (A) harus lebih kecil dari jumlah sumber (S).')
        else:
            Pb = engset_pb(S, N, A)
            status = 'OPTIMAL' if Pb < 0.2 else 'PADAT'
            tabel_data = []
            for n_val in range(1, S):
                tabel_data.append([n_val, round(engset_pb(S, n_val, A), 6)])
            result = {
                'S': S, 'N': N, 'A': A, 'Pb': Pb,
                'status': status, 'tabel_data': tabel_data,
                'time': datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            }
            st.session_state.result = result
            st.session_state.history.append(result)

    if 'result' in st.session_state:
        r = st.session_state.result
        st.markdown('<div class="section-title">\U0001f4ca Hasil Simulasi</div>', unsafe_allow_html=True)
        pb_str = '{:.6f}'.format(r['Pb'])
        a_str  = str(r['A'])
        n_str  = str(r['N'])
        st_str = r['status']
        st.markdown(
            '<div class="metric-grid">'
            '<div class="metric-card"><div class="metric-value">' + pb_str + '</div>'
            '<div class="metric-label">Probabilitas Blocking (P)</div></div>'
            '<div class="metric-card"><div class="metric-value">' + a_str + '</div>'
            '<div class="metric-label">Traffic Offered (A)</div></div>'
            '<div class="metric-card"><div class="metric-value">' + n_str + '</div>'
            '<div class="metric-label">Jumlah Kanal (N)</div></div>'
            '<div class="metric-card"><div class="metric-value">' + st_str + '</div>'
            '<div class="metric-label">Status Sistem</div></div>'
            '</div>',
            unsafe_allow_html=True
        )

# =====================================================
# ANALISIS
# =====================================================

elif page == '\U0001f4ca Analisis':

    if 'result' not in st.session_state:
        st.warning('\u26a0\ufe0f Jalankan simulasi terlebih dahulu di menu Dashboard.')
    else:
        r = st.session_state.result

        st.markdown('<div class="section-title">\U0001f501 Tabel Probabilitas Blocking per Jumlah Kanal</div>', unsafe_allow_html=True)
        df = pd.DataFrame(r['tabel_data'], columns=['Jumlah Kanal (N)', 'Probabilitas Blocking (P)'])
        st.dataframe(df, use_container_width=True)

        st.markdown('<div class="section-title">\U0001f4c8 Grafik Probabilitas Blocking</div>', unsafe_allow_html=True)
        x = [row[0] for row in r['tabel_data']]
        y = [row[1] for row in r['tabel_data']]
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(x, y, marker='o', linewidth=2, label='Probabilitas Blocking (P)')
        ax.axhline(0.2, linestyle='--', color='red', label='Batas Threshold (P = 0.2)')
        ax.axvline(r['N'], linestyle=':', color='green', label='N terpilih = ' + str(r['N']))
        ax.set_xlabel('Jumlah Kanal (N)')
        ax.set_ylabel('Probabilitas Blocking (P)')
        ax.set_title('Grafik Probabilitas Blocking Engset')
        ax.grid(True)
        ax.legend()
        st.pyplot(fig)

# =====================================================
# RIWAYAT
# =====================================================

elif page == '\U0001f4c1 Riwayat':

    if st.session_state.history:
        rows = []
        for i, r in enumerate(st.session_state.history, 1):
            rows.append({
                'No': i, 'Waktu': r['time'],
                'S': r['S'], 'N': r['N'], 'A': r['A'],
                'P (Blocking)': round(r['Pb'], 6),
                'Status': r['status']
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True)
    else:
        st.info('\u2139\ufe0f Belum ada riwayat simulasi.')

# =====================================================
# EXPORT PDF
# =====================================================

if 'result' in st.session_state:
    st.markdown('---')
    st.markdown('<div class="section-title">\U0001f4e5 Export PDF</div>', unsafe_allow_html=True)
    latest = st.session_state.result
    x = [row[0] for row in latest['tabel_data']]
    y = [row[1] for row in latest['tabel_data']]
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(x, y, marker='o', linewidth=2)
    ax.axhline(0.2, linestyle='--', color='red', label='Threshold P = 0.2')
    ax.set_xlabel('Jumlah Kanal (N)')
    ax.set_ylabel('Probabilitas Blocking (P)')
    ax.set_title('Grafik Probabilitas Blocking Engset')
    ax.grid(True)
    ax.legend()
    pdf = export_pdf(latest, fig)
    st.download_button(
        label='\u2b07\ufe0f Download Laporan PDF',
        data=pdf,
        file_name='Laporan_Engset.pdf',
        mime='application/pdf'
    )<style>
.main { background-color: #f1f5f9; }
.unpix-header {
    background: linear-gradient(135deg, #2563eb, #06b6d4);
    padding: 30px;
    border-radius: 25px;
    margin-bottom: 25px;
    box-shadow: 0px 6px 25px rgba(0,0,0,0.2);
}
.header-title { font-size: 38px; font-weight: bold; color: white; }
.header-subtitle { font-size: 15px; color: #e0f2fe; margin-top: 8px; }
.section-title {
    font-size: 28px;
    font-weight: bold;
    color: #2563eb;
    margin-top: 20px;
    margin-bottom: 15px;
}
.metric-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
}
.metric-card {
    background: white;
    padding: 20px;
    border-radius: 20px;
    text-align: center;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.1);
}
.metric-value { font-size: 28px; font-weight: bold; color: #2563eb; }
.metric-label { font-size: 15px; color: #334155; margin-top: 10px; }
.input-card {
    background: white;
    padding: 20px;
    border-radius: 20px;
    margin-bottom: 20px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.1);
}
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)

# =====================================================
# FUNGSI ENGSET (Sesuai Rumus Dosen)
#
# Rumus:
#   P = [ C(S-1, N) * (A/(S-A))^N ]
#       / [ sum_{i=0}^{N} C(S-1, i) * (A/(S-A))^i ]
#
# Keterangan:
#   P = Probabilitas blocking
#   S = Jumlah sumber / pengguna
#   N = Jumlah server / kanal
#   A = Traffic offered to group
# =====================================================

def nCr(n, r):
    if r > n or r < 0:
        return 0
    return factorial(n) // (factorial(r) * factorial(n - r))


def engset_pb(S, N, A):
    ratio = A / (S - A)
    numerator = nCr(S - 1, N) * (ratio ** N)
    denominator = sum(nCr(S - 1, i) * (ratio ** i) for i in range(N + 1))
    return numerator / denominator


# =====================================================
# PDF EXPORT
# =====================================================

def export_pdf(data, fig):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        rightMargin=2*cm, leftMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm
    )
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("LAPORAN SIMULASI ENGSET", styles["Title"]))
    elements.append(Spacer(1, 12))

    info = (
        "<b>Jumlah Sumber (S):</b> " + str(data["S"]) + "<br/>"
        "<b>Jumlah Kanal (N):</b> " + str(data["N"]) + "<br/>"
        "<b>Traffic Offered (A):</b> " + str(data["A"]) + "<br/>"
        "<b>Probabilitas Blocking (P):</b> " + "{:.6f}".format(data["Pb"]) + "<br/>"
        "<b>Status:</b> " + data["status"] + "<br/>"
        "<b>Waktu:</b> " + data["time"] + "<br/>"
    )
    elements.append(Paragraph(info, styles["BodyText"]))
    elements.append(Spacer(1, 15))

    table_data = [["Jumlah Kanal (N)", "Probabilitas Blocking (P)"]]
    for row in data["tabel_data"]:
        table_data.append(row)

    table = Table(table_data)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.blue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("ALIGN", (0, 0), (-1, -1), "CENTER")
    ]))
    elements.append(table)
    elements.append(Spacer(1, 20))

    img_buffer = io.BytesIO()
    fig.savefig(img_buffer, format="png")
    img_buffer.seek(0)
    elements.append(Image(img_buffer, width=15*cm, height=7*cm))

    doc.build(elements)
    buffer.seek(0)
    return buffer


# =====================================================
# SESSION STATE
# =====================================================

if "history" not in st.session_state:
    st.session_state.history = []

# =====================================================
# HEADER
# =====================================================

HEADER_HTML = """
<div class="unpix-header">
    <div class="header-title">\U0001f310 Kalkulator Engset</div>
    <div class="header-subtitle">Sistem Analisis Probabilitas Blocking Telekomunikasi</div>
</div>
"""
st.markdown(HEADER_HTML, unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:
    st.title("\U0001f4c2 Navigasi")
    page = st.radio(
        "Pilih Menu",
        [
            "\U0001f3e0 Dashboard",
            "\U0001f4ca Analisis",
            "\U0001f4c1 Riwayat"
        ]
    )

# =====================================================
# DASHBOARD
# =====================================================

if page == "\U0001f3e0 Dashboard":

    st.markdown(
        '<div class="section-title">\U0001f4e5 Input Parameter Sistem</div>',
        unsafe_allow_html=True
    )
    st.markdown('<div class="input-card">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        S = st.number_input("Jumlah Sumber (S)", min_value=2, value=10)
    with col2:
        N = st.number_input("Jumlah Kanal (N)", min_value=1, value=3)
    with col3:
        A = st.number_input(
            "Traffic Offered (A)",
            min_value=0.01,
            max_value=float(S - 1),
            value=min(5.0, float(S - 1)),
            step=0.01,
            help="Traffic offered to group. Nilai A harus lebih kecil dari S."
        )

    st.markdown("</div>", unsafe_allow_html=True)

    run = st.button("\U0001f680 Jalankan Analisis")

    if run:
        if N >= S:
            st.error("\u274c Jumlah kanal (N) harus lebih kecil dari jumlah sumber (S).")
        elif A >= S:
            st.error("\u274c Traffic offered (A) harus lebih kecil dari jumlah sumber (S).")
        else:
            Pb = engset_pb(S, N, A)
            status = "OPTIMAL" if Pb < 0.2 else "PADAT"

            tabel_data = []
            for n_val in range(1, S):
                pb_val = engset_pb(S, n_val, A)
                tabel_data.append([n_val, round(pb_val, 6)])

            result = {
                "S": S, "N": N, "A": A, "Pb": Pb,
                "status": status,
                "tabel_data": tabel_data,
                "time": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            }
            st.session_state.result = result
            st.session_state.history.append(result)

    if "result" in st.session_state:
        r = st.session_state.result

        st.markdown(
            '<div class="section-title">\U0001f4ca Hasil Simulasi</div>',
            unsafe_allow_html=True
        )

        pb_str = "{:.6f}".format(r["Pb"])
        a_str  = str(r["A"])
        n_str  = str(r["N"])
        st_str = r["status"]

        html_metrics = (
            '<div class="metric-grid">'
              '<div class="metric-card">'
                '<div class="metric-value">' + pb_str + '</div>'
                '<div class="metric-label">Probabilitas Blocking (P)</div>'
              '</div>'
              '<div class="metric-card">'
                '<div class="metric-value">' + a_str + '</div>'
                '<div class="metric-label">Traffic Offered (A)</div>'
              '</div>'
              '<div class="metric-card">'
                '<div class="metric-value">' + n_str + '</div>'
                '<div class="metric-label">Jumlah Kanal (N)</div>'
              '</div>'
              '<div class="metric-card">'
                '<div class="metric-value">' + st_str + '</div>'
                '<div class="metric-label">Status Sistem</div>'
              '</div>'
            '</div>'
        )
        st.markdown(html_metrics, unsafe_allow_html=True)

# =====================================================
# ANALISIS
# =====================================================

elif page == "\U0001f4ca Analisis":

    if "result" not in st.session_state:
        st.warning("\u26a0\ufe0f Jalankan simulasi terlebih dahulu di menu Dashboard.")
    else:
        r = st.session_state.result

        st.markdown(
            '<div class="section-title">\U0001f501 Tabel Probabilitas Blocking per Jumlah Kanal</div>',
            unsafe_allow_html=True
        )

        df = pd.DataFrame(
            r["tabel_data"],
            columns=["Jumlah Kanal (N)", "Probabilitas Blocking (P)"]
        )
        st.dataframe(df, use_container_width=True)

        st.markdown(
            '<div class="section-title">\U0001f4c8 Grafik Probabilitas Blocking</div>',
            unsafe_allow_html=True
        )

        x = [row[0] for row in r["tabel_data"]]
        y = [row[1] for row in r["tabel_data"]]

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(x, y, marker="o", linewidth=2, label="Probabilitas Blocking (P)")
        ax.axhline(0.2, linestyle="--", color="red", label="Batas Threshold (P = 0.2)")
        ax.axvline(r["N"], linestyle=":", color="green", label="N terpilih = " + str(r["N"]))
        ax.set_xlabel("Jumlah Kanal (N)")
        ax.set_ylabel("Probabilitas Blocking (P)")
        ax.set_title("Grafik Probabilitas Blocking Engset")
        ax.grid(True)
        ax.legend()
        st.pyplot(fig)

# =====================================================
# RIWAYAT
# =====================================================

elif page == "\U0001f4c1 Riwayat":

    if st.session_state.history:
        rows = []
        for i, r in enumerate(st.session_state.history, 1):
            rows.append({
                "No": i,
                "Waktu": r["time"],
                "S": r["S"],
                "N": r["N"],
                "A": r["A"],
                "P (Blocking)": round(r["Pb"], 6),
                "Status": r["status"]
            })
        df_history = pd.DataFrame(rows)
        st.dataframe(df_history, use_container_width=True)
    else:
        st.info("\u2139\ufe0f Belum ada riwayat simulasi.")

# =====================================================
# EXPORT PDF
# =====================================================

if "result" in st.session_state:

    st.markdown("---")
    st.markdown(
        '<div class="section-title">\U0001f4e5 Export PDF</div>',
        unsafe_allow_html=True
    )

    latest = st.session_state.result
    x = [row[0] for row in latest["tabel_data"]]
    y = [row[1] for row in latest["tabel_data"]]

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(x, y, marker="o", linewidth=2)
    ax.axhline(0.2, linestyle="--", color="red", label="Threshold P = 0.2")
    ax.set_xlabel("Jumlah Kanal (N)")
    ax.set_ylabel("Probabilitas Blocking (P)")
    ax.set_title("Grafik Probabilitas Blocking Engset")
    ax.grid(True)
    ax.legend()

    pdf = export_pdf(latest, fig)

    st.download_button(
        label="\u2b07\ufe0f Download Laporan PDF",
        data=pdf,
        file_name="Laporan_Engset.pdf",
        mime="application/pdf"
                )}
.header-title { font-size: 38px; font-weight: bold; color: white; }
.header-subtitle { font-size: 15px; color: #e0f2fe; margin-top: 8px; }
.section-title { font-size: 28px; font-weight: bold; color: #2563eb; margin-top: 20px; margin-bottom: 15px; }
.metric-grid { display: grid; grid-template-columns: repeat(2,1fr); gap: 20px; }
.metric-card { background: white; padding: 20px; border-radius: 20px; text-align: center; box-shadow: 0px 4px 20px rgba(0,0,0,0.1); }
.metric-value { font-size: 28px; font-weight: bold; color: #2563eb; }
.metric-label { font-size: 15px; color: #334155; margin-top: 10px; }
.input-card { background: white; padding: 20px; border-radius: 20px; margin-bottom: 20px; box-shadow: 0px 4px 20px rgba(0,0,0,0.1); }
</style>
""", unsafe_allow_html=True)

# =====================================================
# FUNGSI ENGSET (Sesuai Rumus Dosen)
#
# Rumus:
#   P = [ C(S-1, N) * (A/(S-A))^N ]
#       / [ sum_{i=0}^{N} C(S-1, i) * (A/(S-A))^i ]
#
# Keterangan:
#   P = Probabilitas blocking
#   S = Jumlah sumber / pengguna
#   N = Jumlah server / kanal
#   A = Traffic offered to group
# =====================================================

def nCr(n, r):
    if r > n or r < 0:
        return 0
    return factorial(n) // (factorial(r) * factorial(n - r))


def engset_pb(S, N, A):
    ratio = A / (S - A)
    numerator = nCr(S - 1, N) * (ratio ** N)
    denominator = sum(nCr(S - 1, i) * (ratio ** i) for i in range(N + 1))
    return numerator / denominator


# PDF EXPORT
def export_pdf(data, fig):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
        rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    elements = []
    elements.append(Paragraph("LAPORAN SIMULASI ENGSET", styles["Title"]))
    elements.append(Spacer(1, 12))
    info = (
        "<b>Jumlah Sumber (S):</b> " + str(data["S"]) + "<br/>"
        "<b>Jumlah Kanal (N):</b> " + str(data["N"]) + "<br/>"
        "<b>Traffic Offered (A):</b> " + str(data["A"]) + "<br/>"
        "<b>Probabilitas Blocking (P):</b> " + "{:.6f}".format(data["Pb"]) + "<br/>"
        "<b>Status:</b> " + data["status"] + "<br/>"
        "<b>Waktu:</b> " + data["time"] + "<br/>"
    )
    elements.append(Paragraph(info, styles["BodyText"]))
    elements.append(Spacer(1, 15))
    table_data = [["Jumlah Kanal (N)", "Probabilitas Blocking (P)"]]
    for row in data["tabel_data"]:
        table_data.append(row)
    table = Table(table_data)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.blue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("ALIGN", (0, 0), (-1, -1), "CENTER")
    ]))
    elements.append(table)
    elements.append(Spacer(1, 20))
    img_buffer = io.BytesIO()
    fig.savefig(img_buffer, format="png")
    img_buffer.seek(0)
    elements.append(Image(img_buffer, width=15*cm, height=7*cm))
    doc.build(elements)
    buffer.seek(0)
    return buffer


# SESSION STATE
if "history" not in st.session_state:
    st.session_state.history = []

# HEADER
st.markdown("""
<div class=\"unpix-header\">
    <div class=\"header-title\">\U0001f310 Kalkulator Engset</div>
    <div class=\"header-subtitle\">Sistem Analisis Probabilitas Blocking Telekomunikasi</div>
</div>
""", unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.title("\U0001f4c2 Navigasi")
    page = st.radio(
        "Pilih Menu",
        [
            "\U0001f3e0 Dashboard",
            "\U0001f4ca Analisis",
            "\U0001f4c1 Riwayat"
        ]
    )

# =====================================================
# DASHBOARD
# =====================================================

if page == "\U0001f3e0 Dashboard":
    st.markdown('<div class="section-title">\U0001f4e5 Input Parameter Sistem</div>', unsafe_allow_html=True)
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        S = st.number_input("Jumlah Sumber (S)", min_value=2, value=10)
    with col2:
        N = st.number_input("Jumlah Kanal (N)", min_value=1, value=3)
    with col3:
        A = st.number_input(
            "Traffic Offered (A)",
            min_value=0.01,
            max_value=float(S - 1),
            value=min(5.0, float(S - 1)),
            step=0.01,
            help="Traffic offered to group. Nilai A harus lebih kecil dari S."
        )
    st.markdown('</div>', unsafe_allow_html=True)
    run = st.button("\U0001f680 Jalankan Analisis")
    if run:
        if N >= S:
            st.error("\u274c Jumlah kanal (N) harus lebih kecil dari jumlah sumber (S).")
        elif A >= S:
            st.error("\u274c Traffic offered (A) harus lebih kecil dari jumlah sumber (S).")
        else:
            Pb = engset_pb(S, N, A)
            status = "OPTIMAL" if Pb < 0.2 else "PADAT"
            tabel_data = []
            for n_val in range(1, S):
                pb_val = engset_pb(S, n_val, A)
                tabel_data.append([n_val, round(pb_val, 6)])
            result = {
                "S": S, "N": N, "A": A, "Pb": Pb,
                "status": status, "tabel_data": tabel_data,
                "time": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            }
            st.session_state.result = result
            st.session_state.history.append(result)
    if "result" in st.session_state:
        r = st.session_state.result
        st.markdown('<div class="section-title">\U0001f4ca Hasil Simulasi</div>', unsafe_allow_html=True)
        pb_str = "{:.6f}".format(r["Pb"])
        a_str = str(r["A"])
        n_str = str(r["N"])
        status_str = r["status"]
        st.markdown(
            '<div class="metric-grid">'
            '<div class="metric-card"><div class="metric-value">' + pb_str + '</div>'
            '<div class="metric-label">Probabilitas Blocking (P)</div></div>'
            '<div class="metric-card"><div class="metric-value">' + a_str + '</div>'
            '<div class="metric-label">Traffic Offered (A)</div></div>'
            '<div class="metric-card"><div class="metric-value">' + n_str + '</div>'
            '<div class="metric-label">Jumlah Kanal (N)</div></div>'
            '<div class="metric-card"><div class="metric-value">' + status_str + '</div>'
            '<div class="metric-label">Status Sistem</div></div>'
            '</div>',
            unsafe_allow_html=True
        )

# =====================================================
# ANALISIS
# =====================================================

elif page == "\U0001f4ca Analisis":
    if "result" not in st.session_state:
        st.warning("\u26a0\ufe0f Jalankan simulasi terlebih dahulu di menu Dashboard.")
    else:
        r = st.session_state.result
        st.markdown('<div class="section-title">\U0001f501 Tabel Probabilitas Blocking per Jumlah Kanal</div>', unsafe_allow_html=True)
        df = pd.DataFrame(r["tabel_data"], columns=["Jumlah Kanal (N)", "Probabilitas Blocking (P)"])
        st.dataframe(df, use_container_width=True)
        st.markdown('<div class="section-title">\U0001f4c8 Grafik Probabilitas Blocking</div>', unsafe_allow_html=True)
        x = [row[0] for row in r["tabel_data"]]
        y = [row[1] for row in r["tabel_data"]]
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(x, y, marker="o", linewidth=2, label="Probabilitas Blocking (P)")
        ax.axhline(0.2, linestyle="--", color="red", label="Batas Threshold (P = 0.2)")
        ax.axvline(r["N"], linestyle=":", color="green", label="N terpilih = " + str(r["N"]))
        ax.set_xlabel("Jumlah Kanal (N)")
        ax.set_ylabel("Probabilitas Blocking (P)")
        ax.set_title("Grafik Probabilitas Blocking Engset")
        ax.grid(True)
        ax.legend()
        st.pyplot(fig)

# =====================================================
# RIWAYAT
# =====================================================

elif page == "\U0001f4c1 Riwayat":
    if st.session_state.history:
        rows = []
        for i, r in enumerate(st.session_state.history, 1):
            rows.append({
                "No": i, "Waktu": r["time"],
                "S": r["S"], "N": r["N"], "A": r["A"],
                "P (Blocking)": round(r["Pb"], 6),
                "Status": r["status"]
            })
        df_history = pd.DataFrame(rows)
        st.dataframe(df_history, use_container_width=True)
    else:
        st.info("\u2139\ufe0f Belum ada riwayat simulasi.")

# =====================================================
# EXPORT PDF
# =====================================================

if "result" in st.session_state:
    st.markdown("---")
    st.markdown('<div class="section-title">\U0001f4e5 Export PDF</div>', unsafe_allow_html=True)
    latest = st.session_state.result
    x = [row[0] for row in latest["tabel_data"]]
    y = [row[1] for row in latest["tabel_data"]]
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(x, y, marker="o", linewidth=2)
    ax.axhline(0.2, linestyle="--", color="red", label="Threshold P = 0.2")
    ax.set_xlabel("Jumlah Kanal (N)")
    ax.set_ylabel("Probabilitas Blocking (P)")
    ax.set_title("Grafik Probabilitas Blocking Engset")
    ax.grid(True)
    ax.legend()
    pdf = export_pdf(latest, fig)
    st.download_button(
        label="\u2b07\ufe0f Download Laporan PDF",
        data=pdf,
        file_name="Laporan_Engset.pdf",
        mime="application/pdf"
        ).main { background-color: #f1f5f9; }
.unpix-header {
    background: linear-gradient(135deg,#2563eb,#06b6d4);
    padding: 30px;
    border-radius: 25px;
    margin-bottom: 25px;
    box-shadow: 0px 6px 25px rgba(0,0,0,0.2);
}
.header-title { font-size: 38px; font-weight: bold; color: white; }
.header-subtitle { font-size: 15px; color: #e0f2fe; margin-top: 8px; }
.section-title {
    font-size: 28px;
    font-weight: bold;
    color: #2563eb;
    margin-top: 20px;
    margin-bottom: 15px;
}
.metric-grid { display: grid; grid-template-columns: repeat(2,1fr); gap: 20px; }
.metric-card {
    background: white;
    padding: 20px;
    border-radius: 20px;
    text-align: center;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.1);
}
.metric-value { font-size: 28px; font-weight: bold; color: #2563eb; }
.metric-label { font-size: 15px; color: #334155; margin-top: 10px; }
.input-card {
    background: white;
    padding: 20px;
    border-radius: 20px;
    margin-bottom: 20px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# FUNGSI ENGSET (Sesuai Rumus Dosen)
#
# Rumus:
#   P = [ C(S-1, N) * (A/(S-A))^N ]
#       / [ sum_{i=0}^{N} C(S-1, i) * (A/(S-A))^i ]
#
# Keterangan:
#   P = Probabilitas blocking
#   S = Jumlah sumber / pengguna
#   N = Jumlah server / kanal
#   A = Traffic offered to group
# =====================================================

def nCr(n, r):
    if r > n or r < 0:
        return 0
    return factorial(n) // (factorial(r) * factorial(n - r))


def engset_pb(S, N, A):
    ratio = A / (S - A)
    numerator = nCr(S - 1, N) * (ratio ** N)
    denominator = sum(nCr(S - 1, i) * (ratio ** i) for i in range(N + 1))
    return numerator / denominator


# =====================================================
# PDF EXPORT
# =====================================================

def export_pdf(data, fig):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("LAPORAN SIMULASI ENGSET", styles['Title']))
    elements.append(Spacer(1, 12))

    info = (
        "<b>Jumlah Sumber (S):</b> " + str(data['S']) + "<br/>"
        "<b>Jumlah Kanal (N):</b> " + str(data['N']) + "<br/>"
        "<b>Traffic Offered (A):</b> " + str(data['A']) + "<br/>"
        "<b>Probabilitas Blocking (P):</b> " + "{:.6f}".format(data['Pb']) + "<br/>"
        "<b>Status:</b> " + data['status'] + "<br/>"
        "<b>Waktu:</b> " + data['time'] + "<br/>"
    )
    elements.append(Paragraph(info, styles['BodyText']))
    elements.append(Spacer(1, 15))

    table_data = [["Jumlah Kanal (N)", "Probabilitas Blocking (P)"]]
    for row in data["tabel_data"]:
        table_data.append(row)

    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.blue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER')
    ]))
    elements.append(table)
    elements.append(Spacer(1, 20))

    img_buffer = io.BytesIO()
    fig.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    elements.append(Image(img_buffer, width=15*cm, height=7*cm))

    doc.build(elements)
    buffer.seek(0)
    return buffer


# =====================================================
# SESSION STATE
# =====================================================

if "history" not in st.session_state:
    st.session_state.history = []

# =====================================================
# HEADER
# =====================================================

st.markdown("""
<div class="unpix-header">
    <div class="header-title">🌐 Kalkulator Engset</div>
    <div class="header-subtitle">Sistem Analisis Probabilitas Blocking Telekomunikasi</div>
</div>
""", unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:
    st.title("📂 Navigasi")
    page = st.radio(
        "Pilih Menu",
        ["🏠 Dashboard", "📊 Analisis", "📁 Riwayat"]
    )

# =====================================================
# DASHBOARD
# =====================================================

if page == "🏠 Dashboard":

    st.markdown('<div class="section-title">📥 Input Parameter Sistem</div>', unsafe_allow_html=True)
    st.markdown('<div class="input-card">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        S = st.number_input("Jumlah Sumber (S)", min_value=2, value=10)

    with col2:
        N = st.number_input("Jumlah Kanal (N)", min_value=1, value=3)

    with col3:
        A = st.number_input(
            "Traffic Offered (A)",
            min_value=0.01,
            max_value=float(S - 1),
            value=min(5.0, float(S - 1)),
            step=0.01,
            help="Traffic offered to group. Nilai A harus lebih kecil dari S."
        )

    st.markdown("</div>", unsafe_allow_html=True)

    run = st.button("🚀 Jalankan Analisis")

    if run:
        if N >= S:
            st.error("Jumlah kanal (N) harus lebih kecil dari jumlah sumber (S).")
        elif A >= S:
            st.error("Traffic offered (A) harus lebih kecil dari jumlah sumber (S).")
        else:
            Pb = engset_pb(S, N, A)
            status = "OPTIMAL" if Pb < 0.2 else "PADAT"

            tabel_data = []
            for n_val in range(1, S):
                pb_val = engset_pb(S, n_val, A)
                tabel_data.append([n_val, round(pb_val, 6)])

            result = {
                "S": S,
                "N": N,
                "A": A,
                "Pb": Pb,
                "status": status,
                "tabel_data": tabel_data,
                "time": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            }

            st.session_state.result = result
            st.session_state.history.append(result)

    if "result" in st.session_state:
        r = st.session_state.result

        st.markdown('<div class="section-title">📊 Hasil Simulasi</div>', unsafe_allow_html=True)

        pb_str = "{:.6f}".format(r['Pb'])
        a_str = str(r['A'])
        n_str = str(r['N'])
        status_str = r['status']

        st.markdown(
            '<div class="metric-grid">'
            '<div class="metric-card">'
            '<div class="metric-value">' + pb_str + '</div>'
            '<div class="metric-label">Probabilitas Blocking (P)</div>'
            '</div>'
            '<div class="metric-card">'
            '<div class="metric-value">' + a_str + '</div>'
            '<div class="metric-label">Traffic Offered (A)</div>'
            '</div>'
            '<div class="metric-card">'
            '<div class="metric-value">' + n_str + '</div>'
            '<div class="metric-label">Jumlah Kanal (N)</div>'
            '</div>'
            '<div class="metric-card">'
            '<div class="metric-value">' + status_str + '</div>'
            '<div class="metric-label">Status Sistem</div>'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )

# =====================================================
# ANALISIS
# =====================================================

elif page == "📊 Analisis":

    if "result" not in st.session_state:
        st.warning("Jalankan simulasi terlebih dahulu di menu Dashboard.")
    else:
        r = st.session_state.result

        st.markdown('<div class="section-title">🔁 Tabel Probabilitas Blocking per Jumlah Kanal</div>', unsafe_allow_html=True)

        df = pd.DataFrame(
            r["tabel_data"],
            columns=["Jumlah Kanal (N)", "Probabilitas Blocking (P)"]
        )
        st.dataframe(df, use_container_width=True)

        st.markdown('<div class="section-title">📈 Grafik Probabilitas Blocking</div>', unsafe_allow_html=True)

        x = [row[0] for row in r["tabel_data"]]
        y = [row[1] for row in r["tabel_data"]]

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(x, y, marker='o', linewidth=2, label='Probabilitas Blocking (P)')
        ax.axhline(0.2, linestyle='--', color='red', label='Batas Threshold (P = 0.2)')
        ax.axvline(r["N"], linestyle=':', color='green', label='N terpilih = ' + str(r["N"]))
        ax.set_xlabel("Jumlah Kanal (N)")
        ax.set_ylabel("Probabilitas Blocking (P)")
        ax.set_title("Grafik Probabilitas Blocking Engset")
        ax.grid(True)
        ax.legend()
        st.pyplot(fig)

# =====================================================
# RIWAYAT
# =====================================================

elif page == "📁 Riwayat":

    if st.session_state.history:
        rows = []
        for i, r in enumerate(st.session_state.history, 1):
            rows.append({
                "No": i,
                "Waktu": r["time"],
                "S": r["S"],
                "N": r["N"],
                "A": r["A"],
                "P (Blocking)": round(r["Pb"], 6),
                "Status": r["status"]
            })
        df_history = pd.DataFrame(rows)
        st.dataframe(df_history, use_container_width=True)
    else:
        st.info("Belum ada riwayat simulasi.")

# =====================================================
# EXPORT PDF
# =====================================================

if "result" in st.session_state:

    st.markdown("---")
    st.markdown('<div class="section-title">📥 Export PDF</div>', unsafe_allow_html=True)

    latest = st.session_state.result

    x = [row[0] for row in latest["tabel_data"]]
    y = [row[1] for row in latest["tabel_data"]]

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(x, y, marker='o', linewidth=2)
    ax.axhline(0.2, linestyle='--', color='red', label='Threshold P = 0.2')
    ax.set_xlabel("Jumlah Kanal (N)")
    ax.set_ylabel("Probabilitas Blocking (P)")
    ax.set_title("Grafik Probabilitas Blocking Engset")
    ax.grid(True)
    ax.legend()

    pdf = export_pdf(latest, fig)

    st.download_button(
        label="Download Laporan PDF",
        data=pdf,
        file_name="Laporan_Engset.pdf",
        mime="application/pdf"
            )st.markdown("""
<style>

.main {
    background-color: #f1f5f9;
}

.unpix-header {
    background: linear-gradient(135deg,#2563eb,#06b6d4);
    padding: 30px;
    border-radius: 25px;
    margin-bottom: 25px;
    box-shadow: 0px 6px 25px rgba(0,0,0,0.2);
}

.header-title {
    font-size: 38px;
    font-weight: bold;
    color: white;
}

.header-subtitle {
    font-size: 15px;
    color: #e0f2fe;
    margin-top: 8px;
}

.section-title {
    font-size: 28px;
    font-weight: bold;
    color: #2563eb;
    margin-top: 20px;
    margin-bottom: 15px;
}

.metric-grid {
    display: grid;
    grid-template-columns: repeat(2,1fr);
    gap: 20px;
}

.metric-card {
    background: white;
    padding: 20px;
    border-radius: 20px;
    text-align: center;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.1);
}

.metric-value {
    font-size: 28px;
    font-weight: bold;
    color: #2563eb;
}

.metric-label {
    font-size: 15px;
    color: #334155;
    margin-top: 10px;
}

.input-card {
    background: white;
    padding: 20px;
    border-radius: 20px;
    margin-bottom: 20px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.1);
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# FUNGSI ENGSET (Sesuai Rumus Dosen)
#
# Rumus:
#   P = [ C(S-1, N) * (A/(S-A))^N ]
#       / [ sum_{i=0}^{N} C(S-1, i) * (A/(S-A))^i ]
#
# Keterangan:
#   P = Probabilitas blocking
#   S = Jumlah sumber / pengguna
#   N = Jumlah server / kanal
#   A = Traffic offered to group
# =====================================================

def nCr(n, r):
    """Menghitung kombinasi C(n, r)"""
    if r > n or r < 0:
        return 0
    return factorial(n) // (
        factorial(r) * factorial(n - r)
    )


def engset_pb(S, N, A):
    """
    Menghitung probabilitas blocking Engset.

    Rumus:
        P = [ C(S-1,N) * (A/(S-A))^N ]
            / [ sum_{i=0}^{N} C(S-1,i) * (A/(S-A))^i ]

    Parameter:
        S : Jumlah sumber / pengguna
        N : Jumlah server / kanal
        A : Traffic offered to group
    """
    ratio = A / (S - A)

    numerator = nCr(S - 1, N) * (ratio ** N)

    denominator = sum(
        nCr(S - 1, i) * (ratio ** i)
        for i in range(N + 1)
    )

    return numerator / denominator


# =====================================================
# PDF EXPORT
# =====================================================

def export_pdf(data, fig):

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    styles = getSampleStyleSheet()

    elements = []

    title = Paragraph(
        "LAPORAN SIMULASI ENGSET",
        styles['Title']
    )

    elements.append(title)

    elements.append(Spacer(1, 12))

    info = f"""
    <b>Jumlah Sumber (S):</b> {data['S']}<br/>
    <b>Jumlah Kanal (N):</b> {data['N']}<br/>
    <b>Traffic Offered (A):</b> {data['A']}<br/>
    <b>Probabilitas Blocking (P):</b> {data['Pb']:.6f}<br/>
    <b>Status:</b> {data['status']}<br/>
    <b>Waktu:</b> {data['time']}<br/>
    """

    elements.append(
        Paragraph(info, styles['BodyText'])
    )

    elements.append(Spacer(1, 15))

    table_data = [
        ["Jumlah Kanal (N)", "Probabilitas Blocking (P)"]
    ]

    for row in data["tabel_data"]:
        table_data.append(row)

    table = Table(table_data)

    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.blue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER')
    ]))

    elements.append(table)

    elements.append(Spacer(1, 20))

    img_buffer = io.BytesIO()

    fig.savefig(img_buffer, format='png')

    img_buffer.seek(0)

    elements.append(
        Image(img_buffer, width=15*cm, height=7*cm)
    )

    doc.build(elements)

    buffer.seek(0)

    return buffer


# =====================================================
# SESSION STATE
# =====================================================

if "history" not in st.session_state:
    st.session_state.history = []


# =====================================================
# HEADER
# =====================================================

st.markdown("""
<div class="unpix-header">
    <div class="header-title">
        🌐 Kalkulator Engset
    </div>

    <div class="header-subtitle">
        Sistem Analisis Probabilitas Blocking Telekomunikasi
    </div>
</div>
""", unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.title("📂 Navigasi")

    page = st.radio(
        "Pilih Menu",
        [
            "🏠 Dashboard",
            "📊 Analisis",
            "📁 Riwayat"
        ]
    )

# =====================================================
# DASHBOARD
# =====================================================

if page == "🏠 Dashboard":

    st.markdown("""
    <div class="section-title">
        📥 Input Parameter Sistem
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="input-card">',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        S = st.number_input(
            "Jumlah Sumber (S)",
            min_value=2,
            value=10
        )

    with col2:

        N = st.number_input(
            "Jumlah Kanal (N)",
            min_value=1,
            value=3
        )

    with col3:

        A = st.number_input(
            "Traffic Offered (A)",
            min_value=0.01,
            max_value=float(S - 1),
            value=min(0.5, float(S - 1)),
            step=0.01,
            help="Traffic offered to group. Nilai harus lebih kecil dari S."
        )

    st.markdown("</div>", unsafe_allow_html=True)

    run = st.button("🚀 Jalankan Analisis")

    if run:

        if N >= S:
            st.error(
                "❌ Jumlah kanal (N) harus lebih kecil dari jumlah sumber (S)."
            )

        elif A >= S:
            st.error(
                "❌ Traffic offered (A) harus lebih kecil dari jumlah sumber (S)."
            )

        else:

            # Hitung langsung dengan rumus Engset dari dosen
            Pb = engset_pb(S, N, A)

            status = (
                "OPTIMAL"
                if Pb < 0.2
                else "PADAT"
            )

            # Tabel Pb untuk berbagai nilai N (untuk grafik & PDF)
            tabel_data = []
            for n_val in range(1, S):
                pb_val = engset_pb(S, n_val, A)
                tabel_data.append([n_val, round(pb_val, 6)])

            result = {
                "S": S,
                "N": N,
                "A": A,
                "Pb": Pb,
                "status": status,
                "tabel_data": tabel_data,
                "time": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            }

            st.session_state.result = result

            st.session_state.history.append(result)

    if "result" in st.session_state:

        r = st.session_state.result

        st.markdown("""
        <div class="section-title">
            📊 Hasil Simulasi
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""

        <div class="metric-grid">

            <div class="metric-card">
                <div class="metric-value">
                    {r['Pb']:.6f}
                </div>

                <div class="metric-label">
                    Probabilitas Blocking (P)
                </div>
            </div>

            <div class="metric-card">
                <div class="metric-value">
                    {r['A']}
                </div>

                <div class="metric-label">
                    Traffic Offered (A)
                </div>
            </div>

            <div class="metric-card">
                <div class="metric-value">
                    {r['N']}
                </div>

                <div class="metric-label">
                    Jumlah Kanal (N)
                </div>
            </div>

            <div class="metric-card">
                <div class="metric-value">
                    {r['status']}
                </div>

                <div class="metric-label">
                    Status Sistem
                </div>
            </div>

        </div>

        """, unsafe_allow_html=True)

# =====================================================
# ANALISIS
# =====================================================

elif page == "📊 Analisis":

    if "result" not in st.session_state:

        st.warning(
            "⚠️ Jalankan simulasi terlebih dahulu di menu Dashboard."
        )

    else:

        r = st.session_state.result

        st.markdown("""
        <div class="section-title">
            🔁 Tabel Probabilitas Blocking per Jumlah Kanal
        </div>
        """, unsafe_allow_html=True)

        df = pd.DataFrame(
            r["tabel_data"],
            columns=[
                "Jumlah Kanal (N)",
                "Probabilitas Blocking (P)"
            ]
        )

        st.dataframe(
            df,
            use_container_width=True
        )

        st.markdown("""
        <div class="section-title">
            📈 Grafik Probabilitas Blocking
        </div>
        """, unsafe_allow_html=True)

        S = r["S"]
        A = r["A"]

        x = [row[0] for row in r["tabel_data"]]
        y = [row[1] for row in r["tabel_data"]]

        fig, ax = plt.subplots(figsize=(10, 4))

        ax.plot(
            x,
            y,
            marker='o',
            linewidth=2,
            label='Probabilitas Blocking (P)'
        )

        ax.axhline(
            0.2,
            linestyle='--',
            color='red',
            label='Batas Threshold (P = 0.2)'
        )

        ax.axvline(
            r["N"],
            linestyle=':',
            color='green',
            label=f'N terpilih = {r["N"]}'
        )

        ax.set_xlabel("Jumlah Kanal (N)")
        ax.set_ylabel("Probabilitas Blocking (P)")
        ax.set_title("Grafik Probabilitas Blocking Engset")
        ax.grid(True)
        ax.legend()

        st.pyplot(fig)

# =====================================================
# RIWAYAT
# =====================================================

elif page == "📁 Riwayat":

    if st.session_state.history:

        rows = []

        for i, r in enumerate(
            st.session_state.history,
            1
        ):

            rows.append({
                "No": i,
                "Waktu": r["time"],
                "S": r["S"],
                "N": r["N"],
                "A": r["A"],
                "P (Blocking)": round(r["Pb"], 6),
                "Status": r["status"]
            })

        df_history = pd.DataFrame(rows)

        st.dataframe(
            df_history,
            use_container_width=True
        )

    else:

        st.info(
            "ℹ️ Belum ada riwayat simulasi."
        )

# =====================================================
# EXPORT PDF
# =====================================================

if "result" in st.session_state:

    st.markdown("---")

    st.markdown("""
    <div class="section-title">
        📥 Export PDF
    </div>
    """, unsafe_allow_html=True)

    latest = st.session_state.result

    x = [row[0] for row in latest["tabel_data"]]
    y = [row[1] for row in latest["tabel_data"]]

    fig, ax = plt.subplots(figsize=(10, 4))

    ax.plot(x, y, marker='o', linewidth=2)
    ax.axhline(0.2, linestyle='--', color='red', label='Threshold P = 0.2')
    ax.set_xlabel("Jumlah Kanal (N)")
    ax.set_ylabel("Probabilitas Blocking (P)")
    ax.set_title("Grafik Probabilitas Blocking Engset")
    ax.grid(True)
    ax.legend()

    pdf = export_pdf(latest, fig)

    st.download_button(
        label="⬇️ Download Laporan PDF",
        data=pdf,
        file_name="Laporan_Engset.pdf",
        mime="application/pdf"
        )lah Kanal")

        ax.set_ylabel(
            "Probabilitas Blocking"
        )

        ax.grid(True)

        ax.legend()

        st.pyplot(fig)

# =====================================================
# RIWAYAT
# =====================================================

elif page == "📁 Riwayat":

    if st.session_state.history:

        rows = []

        for i, r in enumerate(
            st.session_state.history,
            1
        ):

            rows.append({

                "No": i,
                "Waktu": r["time"],
                "S": r["S"],
                "N": r["N"],
                "ρ": r["rho"],
                "Pb": round(r["Pb"], 6),
                "Status": r["status"]

            })

        df_history = pd.DataFrame(rows)

        st.dataframe(
            df_history,
            use_container_width=True
        )

    else:

        st.info(
            "Belum ada riwayat simulasi"
        )

# =====================================================
# EXPORT PDF
# =====================================================

if "result" in st.session_state:

    st.markdown("---")

    st.markdown("""
    <div class="section-title">
        📥 Export PDF
    </div>
    """, unsafe_allow_html=True)

    latest = st.session_state.result

    S = latest["S"]

    rho = latest["rho"]

    x = list(range(1, S))

    y = [
        engset_pb(S, n, rho)
        for n in x
    ]

    fig, ax = plt.subplots(figsize=(10,4))

    ax.plot(
        x,
        y,
        marker='o'
    )

    ax.grid(True)

    pdf = export_pdf(
        latest,
        fig
    )

    st.download_button(

        label="⬇️ Download PDF",

        data=pdf,

        file_name="Laporan_Engset.pdf",

        mime="application/pdf"
    )
.section-title {
    font-size: 28px;
    font-weight: bold;
    color: #2563eb;
    margin-top: 20px;
    margin-bottom: 15px;
}

.metric-grid {
    display: grid;
    grid-template-columns: repeat(2,1fr);
    gap: 20px;
}

.metric-card {
    background: #1e293b;
    padding: 20px;
    border-radius: 20px;
    text-align: center;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.3);
}

.metric-value {
    font-size: 28px;
    font-weight: bold;
    color: #38bdf8;
}

.metric-label {
    font-size: 15px;
    color: white;
    margin-top: 10px;
}

.input-card {
    background: #111827;
    padding: 20px;
    border-radius: 20px;
    margin-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# RUMUS ENGSET
# =====================================================

def nCr(n, r):

    if r > n:
        return 0

    return factorial(n) // (
        factorial(r) * factorial(n - r)
    )


def engset_pb(S, N, M):

    pembilang = (
        nCr(S - 1, N) * (M ** N)
    )

    penyebut = sum(
        nCr(S - 1, k) * (M ** k)
        for k in range(N + 1)
    )

    return pembilang / penyebut


def iterate(S, N, rho):

    M = rho
    toleransi = 0.0001

    data_iterasi = []

    i = 1

    while True:

        Pb = engset_pb(S, N, M)

        M_baru = rho * (1 - Pb)

        selisih = abs(M_baru - M)

        data_iterasi.append([
            i,
            round(M, 6),
            round(Pb, 6),
            round(selisih, 6)
        ])

        if selisih < toleransi:
            break

        M = M_baru
        i += 1

    return M_baru, Pb, data_iterasi, i


# =====================================================
# SESSION STATE
# =====================================================

if "history" not in st.session_state:
    st.session_state.history = []


# =====================================================
# HEADER
# =====================================================

st.markdown("""
<div class="unpix-header">

    <div class="header-title">
        🌐 Kalkulator Engset
    </div>

    <div class="header-subtitle">
        Sistem Analisis Probabilitas Blocking Engset
    </div>

</div>
""", unsafe_allow_html=True)


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.title("📂 Navigasi")

    page = st.radio(
        "Pilih Menu",
        [
            "🏠 Dashboard",
            "📊 Analisis",
            "📁 Riwayat"
        ]
    )

    st.markdown("---")

    st.info(
        "Aplikasi Simulasi Telekomunikasi"
    )


# =====================================================
# DASHBOARD
# =====================================================

if page == "🏠 Dashboard":

    st.markdown("""
    <div class="section-title">
        📥 Input Parameter Sistem
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="input-card">',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        S = st.number_input(
            "Jumlah Sumber (S)",
            min_value=1,
            value=10
        )

    with col2:

        N = st.number_input(
            "Jumlah Kanal (N)",
            min_value=1,
            value=3
        )

    with col3:

        rho = st.number_input(
            "Traffic per Sumber (ρ)",
            min_value=0.0,
            value=0.5,
            step=0.01,
            format="%.2f"
        )

    st.markdown("</div>", unsafe_allow_html=True)

    run = st.button(
        "🚀 Jalankan Analisis"
    )

    if run:

        if N >= S:

            st.error(
                "Jumlah kanal harus lebih kecil dari jumlah sumber"
            )

        else:

            M, Pb, iterasi, jumlah_iterasi = iterate(
                S,
                N,
                rho
            )

            status = (
                "OPTIMAL"
                if Pb < 0.2
                else "PADAT"
            )

            hasil = {
                "S": S,
                "N": N,
                "rho": rho,
                "M": M,
                "Pb": Pb,
                "iterasi": iterasi,
                "jumlah_iterasi": jumlah_iterasi,
                "status": status,
                "waktu": datetime.now().strftime(
                    "%d-%m-%Y %H:%M:%S"
                )
            }

            st.session_state.result = hasil
            st.session_state.history.append(
                hasil
            )

    if "result" in st.session_state:

        r = st.session_state.result

        st.markdown("""
        <div class="section-title">
            📊 Hasil Simulasi
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="metric-grid">

            <div class="metric-card">
                <div class="metric-value">
                    {r['Pb']:.6f}
                </div>

                <div class="metric-label">
                    Probabilitas Blocking
                </div>
            </div>

            <div class="metric-card">
                <div class="metric-value">
                    {r['M']:.6f}
                </div>

                <div class="metric-label">
                    Traffic Idle
                </div>
            </div>

            <div class="metric-card">
                <div class="metric-value">
                    {r['jumlah_iterasi']}
                </div>

                <div class="metric-label">
                    Jumlah Iterasi
                </div>
            </div>

            <div class="metric-card">
                <div class="metric-value">
                    {r['status']}
                </div>

                <div class="metric-label">
                    Status Sistem
                </div>
            </div>

        </div>
        """, unsafe_allow_html=True)


# =====================================================
# ANALISIS
# =====================================================

elif page == "📊 Analisis":

    st.markdown("""
    <div class="section-title">
        📊 Analisis Sistem
    </div>
    """, unsafe_allow_html=True)

    if "result" not in st.session_state:

        st.warning(
            "Jalankan simulasi terlebih dahulu"
        )

    else:

        r = st.session_state.result

        df = pd.DataFrame(
            r["iterasi"],
            columns=[
                "Iterasi",
                "M",
                "Pb",
                "Selisih"
            ]
        )

        st.dataframe(
            df,
            use_container_width=True
        )

        st.markdown("""
        <div class="section-title">
            📈 Grafik Probabilitas Blocking
        </div>
        """, unsafe_allow_html=True)

        S = r["S"]
        rho = r["rho"]

        x = list(range(1, S))

        y = [
            engset_pb(S, n, rho)
            for n in x
        ]

        fig, ax = plt.subplots(
            figsize=(10, 4)
        )

        ax.plot(
            x,
            y,
            linewidth=2.5,
            marker='o'
        )

        ax.axhline(
            0.2,
            linestyle='--',
            label='Batas 0.2'
        )

        ax.set_xlabel(
            "Jumlah Kanal"
        )

        ax.set_ylabel(
            "Probabilitas Blocking"
        )

        ax.grid(True)

        ax.legend()

        st.pyplot(fig)


# =====================================================
# RIWAYAT
# =====================================================

elif page == "📁 Riwayat":

    st.markdown("""
    <div class="section-title">
        📁 Riwayat Simulasi
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.history:

        rows = []

        for i, r in enumerate(
            st.session_state.history,
            1
        ):

            rows.append({
                "No": i,
                "Waktu": r["waktu"],
                "S": r["S"],
                "N": r["N"],
                "ρ": r["rho"],
                "M": round(r["M"], 6),
                "Pb": round(r["Pb"], 6),
                "Status": r["status"]
            })

        df_hist = pd.DataFrame(rows)

        st.dataframe(
            df_hist,
            use_container_width=True
        )

    else:

        st.info(
            "Belum ada riwayat simulasi"
        )


# =====================================================
# EXPORT PDF
# =====================================================

def export_pdf(data, fig):

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4
    )

    styles = getSampleStyleSheet()

    elements = []

    title = Paragraph(
        "Laporan Kalkulator Engset",
        styles['Title']
    )

    elements.append(title)

    elements.append(
        Spacer(1, 12)
    )

    tabel = Table([
        ["Parameter", "Nilai"],
        ["Jumlah Sumber", data["S"]],
        ["Jumlah Kanal", data["N"]],
        ["Traffic", data["rho"]],
        ["Blocking Probability", f"{data['Pb']:.6f}"],
        ["Traffic Idle", f"{data['M']:.6f}"],
        ["Status", data["status"]]
    ])

    tabel.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.blue),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))

    elements.append(tabel)

    img_buffer = io.BytesIO()

    fig.savefig(
        img_buffer,
        format='png'
    )

    img_buffer.seek(0)

    elements.append(
        Spacer(1, 20)
    )

    elements.append(
        Image(
            img_buffer,
            width=400,
            height=200
        )
    )

    doc.build(elements)

    buffer.seek(0)

    return buffer


# =====================================================
# DOWNLOAD PDF
# =====================================================

if "result" in st.session_state:

    st.markdown("---")

    st.markdown("""
    <div class="section-title">
        📥 Download Laporan PDF
    </div>
    """, unsafe_allow_html=True)

    latest = st.session_state.result

    S = latest["S"]
    rho = latest["rho"]

    x = list(range(1, S))

    y = [
        engset_pb(S, n, rho)
        for n in x
    ]

    fig, ax = plt.subplots(
        figsize=(10, 4)
    )

    ax.plot(
        x,
        y,
        linewidth=2.5,
        marker='o'
    )

    ax.grid(True)

    pdf = export_pdf(
        latest,
        fig
    )

    st.download_button(
        label="⬇️ Download PDF",
        data=pdf,
        file_name="Laporan_Engset.pdf",
        mime="application/pdf"
    )
.section-title {
    font-size: 28px;
    font-weight: bold;
    color: #2563eb;
    margin-top: 20px;
    margin-bottom: 15px;
}

.metric-grid {
    display: grid;
    grid-template-columns: repeat(2,1fr);
    gap: 20px;
}

.metric-card {
    background: #1e293b;
    padding: 20px;
    border-radius: 20px;
    text-align: center;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.3);
}

.metric-value {
    font-size: 28px;
    font-weight: bold;
    color: #38bdf8;
}

.metric-label {
    font-size: 15px;
    color: white;
    margin-top: 10px;
}

.input-card {
    background: #111827;
    padding: 20px;
    border-radius: 20px;
    margin-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# RUMUS ENGSET
# =====================================================

def nCr(n, r):

    if r > n:
        return 0

    return factorial(n) // (
        factorial(r) * factorial(n - r)
    )


def engset_pb(S, N, M):

    pembilang = (
        nCr(S - 1, N) * (M ** N)
    )

    penyebut = sum(
        nCr(S - 1, k) * (M ** k)
        for k in range(N + 1)
    )

    return pembilang / penyebut


def iterate(S, N, rho):

    M = rho
    toleransi = 0.0001

    data_iterasi = []

    i = 1

    while True:

        Pb = engset_pb(S, N, M)

        M_baru = rho * (1 - Pb)

        selisih = abs(M_baru - M)

        data_iterasi.append([
            i,
            round(M, 6),
            round(Pb, 6),
            round(selisih, 6)
        ])

        if selisih < toleransi:
            break

        M = M_baru
        i += 1

    return M_baru, Pb, data_iterasi, i


# =====================================================
# SESSION STATE
# =====================================================

if "history" not in st.session_state:
    st.session_state.history = []


# =====================================================
# HEADER
# =====================================================

st.markdown("""
<div class="unpix-header">

    <div class="header-title">
        🌐 Kalkulator Engset
    </div>

    <div class="header-subtitle">
        Sistem Analisis Probabilitas Blocking Engset
    </div>

</div>
""", unsafe_allow_html=True)


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.title("📂 Navigasi")

    page = st.radio(
        "Pilih Menu",
        [
            "🏠 Dashboard",
            "📊 Analisis",
            "📁 Riwayat"
        ]
    )

    st.markdown("---")

    st.info(
        "Aplikasi Simulasi Telekomunikasi"
    )


# =====================================================
# DASHBOARD
# =====================================================

if page == "🏠 Dashboard":

    st.markdown("""
    <div class="section-title">
        📥 Input Parameter Sistem
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="input-card">',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        S = st.number_input(
            "Jumlah Sumber (S)",
            min_value=1,
            value=10
        )

    with col2:

        N = st.number_input(
            "Jumlah Kanal (N)",
            min_value=1,
            value=3
        )

    with col3:

        rho = st.number_input(
            "Traffic per Sumber (ρ)",
            min_value=0.0,
            value=0.5,
            step=0.01,
            format="%.2f"
        )

    st.markdown("</div>", unsafe_allow_html=True)

    run = st.button(
        "🚀 Jalankan Analisis"
    )

    if run:

        if N >= S:

            st.error(
                "Jumlah kanal harus lebih kecil dari jumlah sumber"
            )

        else:

            M, Pb, iterasi, jumlah_iterasi = iterate(
                S,
                N,
                rho
            )

            status = (
                "OPTIMAL"
                if Pb < 0.2
                else "PADAT"
            )

            hasil = {

                "S": S,
                "N": N,
                "rho": rho,
                "M": M,
                "Pb": Pb,
                "iterasi": iterasi,
                "jumlah_iterasi": jumlah_iterasi,
                "status": status,
                "waktu": datetime.now().strftime(
                    "%d-%m-%Y %H:%M:%S"
                )
            }

            st.session_state.result = hasil
            st.session_state.history.append(
                hasil
            )

    if "result" in st.session_state:

        r = st.session_state.result

        st.markdown("""
        <div class="section-title">
            📊 Hasil Simulasi
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="metric-grid">

            <div class="metric-card">
                <div class="metric-value">
                    {r['Pb']:.6f}
                </div>

                <div class="metric-label">
                    Probabilitas Blocking
                </div>
            </div>

            <div class="metric-card">
                <div class="metric-value">
                    {r['M']:.6f}
                </div>

                <div class="metric-label">
                    Traffic Idle
                </div>
            </div>

            <div class="metric-card">
                <div class="metric-value">
                    {r['jumlah_iterasi']}
                </div>

                <div class="metric-label">
                    Jumlah Iterasi
                </div>
            </div>

            <div class="metric-card">
                <div class="metric-value">
                    {r['status']}
                </div>

                <div class="metric-label">
                    Status Sistem
                </div>
            </div>

        </div>
        """, unsafe_allow_html=True)


# =====================================================
# ANALISIS
# =====================================================

elif page == "📊 Analisis":

    st.markdown("""
    <div class="section-title">
        📊 Analisis Sistem
    </div>
    """, unsafe_allow_html=True)

    if "result" not in st.session_state:

        st.warning(
            "Jalankan simulasi terlebih dahulu"
        )

    else:

        r = st.session_state.result

        df = pd.DataFrame(
            r["iterasi"],
            columns=[
                "Iterasi",
                "M",
                "Pb",
                "Selisih"
            ]
        )

        st.dataframe(
            df,
            use_container_width=True
        )

        st.markdown("""
        <div class="section-title">
            📈 Grafik Probabilitas Blocking
        </div>
        """, unsafe_allow_html=True)

        S = r["S"]
        rho = r["rho"]

        x = list(range(1, S))

        y = [
            engset_pb(S, n, rho)
            for n in x
        ]

        fig, ax = plt.subplots(
            figsize=(10, 4)
        )

        ax.plot(
            x,
            y,
            linewidth=2.5,
            marker='o'
        )

        ax.axhline(
            0.2,
            linestyle='--',
            label='Batas 0.2'
        )

        ax.set_xlabel(
            "Jumlah Kanal"
        )

        ax.set_ylabel(
            "Probabilitas Blocking"
        )

        ax.grid(True)

        ax.legend()

        st.pyplot(fig)


# =====================================================
# RIWAYAT
# =====================================================

elif page == "📁 Riwayat":

    st.markdown("""
    <div class="section-title">
        📁 Riwayat Simulasi
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.history:

        rows = []

        for i, r in enumerate(
            st.session_state.history,
            1
        ):

            rows.append({

                "No": i,
                "Waktu": r["waktu"],
                "S": r["S"],
                "N": r["N"],
                "ρ": r["rho"],
                "M": round(r["M"], 6),
                "Pb": round(r["Pb"], 6),
                "Status": r["status"]

            })

        df_hist = pd.DataFrame(rows)

        st.dataframe(
            df_hist,
            use_container_width=True
        )

    else:

        st.info(
            "Belum ada riwayat simulasi"
        )


# =====================================================
# EXPORT PDF
# =====================================================

def export_pdf(data, fig):

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4
    )

    styles = getSampleStyleSheet()

    elements = []

    title = Paragraph(
        "Laporan Kalkulator Engset",
        styles['Title']
    )

    elements.append(title)

    elements.append(
        Spacer(1, 12)
    )

    tabel = Table([

        ["Parameter", "Nilai"],

        ["Jumlah Sumber", data["S"]],
        ["Jumlah Kanal", data["N"]],
        ["Traffic", data["rho"]],
        ["Blocking Probability", f"{data['Pb']:.6f}"],
        ["Traffic Idle", f"{data['M']:.6f}"],
        ["Status", data["status"]]

    ])

    tabel.setStyle(TableStyle([

        ('BACKGROUND', (0,0), (-1,0), colors.blue),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 1, colors.black)

    ]))

    elements.append(tabel)

    img_buffer = io.BytesIO()

    fig.savefig(
        img_buffer,
        format='png'
    )

    img_buffer.seek(0)

    elements.append(
        Spacer(1, 20)
    )

    elements.append(
        Image(
            img_buffer,
            width=400,
            height=200
        )
    )

    doc.build(elements)

    buffer.seek(0)

    return buffer


# =====================================================
# DOWNLOAD PDF
# =====================================================

if "result" in st.session_state:

    st.markdown("---")

    st.markdown("""
    <div class="section-title">
        📥 Download Laporan PDF
    </div>
    """, unsafe_allow_html=True)

    latest = st.session_state.result

    S = latest["S"]
    rho = latest["rho"]

    x = list(range(1, S))

    y = [
        engset_pb(S, n, rho)
        for n in x
    ]

    fig, ax = plt.subplots(
        figsize=(10, 4)
    )

    ax.plot(
        x,
        y,
        linewidth=2.5,
        marker='o'
    )

    ax.grid(True)

    pdf = export_pdf(
        latest,
        fig
    )

    st.download_button(
        label="⬇️ Download PDF",
        data=pdf,
        file_name="Laporan_Engset.pdf",
        mime="application/pdf"
    )    opacity: 0.9;
}

.section-title {
    font-size: 24px;
    font-weight: bold;
    color: #1e3a8a;
    margin-top: 15px;
    margin-bottom: 15px;
}

.metric-grid {
    display: grid;
    grid-template-columns: repeat(4,1fr);
    gap: 15px;
}

.metric-card {
    background: white;
    padding: 20px;
    border-radius: 18px;
    text-align: center;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.metric-value {
    font-size: 28px;
    font-weight: bold;
    color: #2563eb;
}

.metric-label {
    font-size: 14px;
    color: #555;
    margin-top: 8px;
}

.input-card {
    background: white;
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# RUMUS ENGSET
# =====================================================

def nCr(n, r):

    if r > n:
        return 0

    return factorial(n) // (
        factorial(r) * factorial(n - r)
    )


def engset_pb(S, N, M):

    pembilang = nCr(S - 1, N) * (M ** N)

    penyebut = sum(
        nCr(S - 1, k) * (M ** k)
        for k in range(N + 1)
    )

    if penyebut == 0:
        return 0

    return pembilang / penyebut


def iterate(S, N, rho):

    M = rho

    toleransi = 0.0001

    data_iterasi = []

    i = 1

    while True:

        Pb = engset_pb(S, N, M)

        M_baru = rho * (1 - Pb)

        selisih = abs(M_baru - M)

        data_iterasi.append([
            i,
            round(M, 10),
            round(Pb, 10),
            round(selisih, 10)
        ])

        if selisih < toleransi:
            break

        M = M_baru

        i += 1

    return M_baru, Pb, data_iterasi, i


# =====================================================
# SESSION STATE
# =====================================================

if "history" not in st.session_state:
    st.session_state.history = []


# =====================================================
# HEADER
# =====================================================

st.markdown("""
<div class="unpix-header">

<div class="header-title">
🌐 Kalkulator Engset
</div>

<div class="header-subtitle">
Sistem Analisis Probabilitas Blocking Engset
</div>

</div>
""", unsafe_allow_html=True)


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.title("📂 Navigasi")

    page = st.radio(
        "Pilih Menu",
        [
            "🏠 Dashboard",
            "📊 Analisis",
            "📁 Riwayat"
        ]
    )

    st.markdown("---")

    st.info("Aplikasi Simulasi Teknik Telekomunikasi")


# =====================================================
# DASHBOARD
# =====================================================

if page == "🏠 Dashboard":

    st.markdown("""
    <div class="section-title">
    📥 Input Parameter Sistem
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="input-card">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:

        S = st.number_input(
            "Jumlah Sumber (S)",
            min_value=1,
            value=10
        )

    with col2:

        N = st.number_input(
            "Jumlah Kanal (N)",
            min_value=1,
            value=3
        )

    with col3:

        rho = st.number_input(
            "Traffic per Sumber (ρ)",
            min_value=0.0,
            value=0.5,
            step=0.01,
            format="%.2f"
        )

    st.markdown("</div>", unsafe_allow_html=True)

    run = st.button("🚀 Jalankan Analisis")

    if run:

        if N >= S:

            st.error(
                "Jumlah kanal harus lebih kecil dari jumlah sumber."
            )

        else:

            M, Pb, iter_data, iteration = iterate(
                S,
                N,
                rho
            )

            status = (
                "OPTIMAL"
                if Pb < 0.2
                else "PADAT"
            )

            result = {

                "S": S,
                "N": N,
                "rho": rho,
                "M": M,
                "Pb": Pb,
                "iter": iteration,
                "status": status,
                "iter_data": iter_data,
                "time": datetime.now().strftime(
                    "%d-%m-%Y %H:%M:%S"
                )
            }

            st.session_state.result = result

            st.session_state.history.append(result)

    if "result" in st.session_state:

        r = st.session_state.result

        st.markdown("""
        <div class="section-title">
        📊 Hasil Simulasi
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="metric-grid">

            <div class="metric-card">
                <div class="metric-value">
                    {r['Pb']:.6f}
                </div>
                <div class="metric-label">
                    Probabilitas Blocking
                </div>
            </div>

            <div class="metric-card">
                <div class="metric-value">
                    {r['M']:.6f}
                </div>
                <div class="metric-label">
                    Traffic Idle
                </div>
            </div>

            <div class="metric-card">
                <div class="metric-value">
                    {r['iter']}
                </div>
                <div class="metric-label">
                    Jumlah Iterasi
                </div>
            </div>

            <div class="metric-card">
                <div class="metric-value">
                    {r['status']}
                </div>
                <div class="metric-label">
                    Status Sistem
                </div>
            </div>

        </div>
        """, unsafe_allow_html=True)


# =====================================================
# ANALISIS
# =====================================================

elif page == "📊 Analisis":

    st.markdown("""
    <div class="section-title">
    📊 Analisis Sistem
    </div>
    """, unsafe_allow_html=True)

    if "result" not in st.session_state:

        st.warning(
            "Jalankan simulasi terlebih dahulu."
        )

    else:

        r = st.session_state.result

        st.markdown("""
        <div class="section-title">
        🔁 Tabel Iterasi
        </div>
        """, unsafe_allow_html=True)

        df = pd.DataFrame(

            r["iter_data"],

            columns=[
                "Iterasi",
                "M",
                "Pb",
                "Selisih"
            ]
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.markdown("""
        <div class="section-title">
        📈 Grafik Blocking Probability
        </div>
        """, unsafe_allow_html=True)

        S = r["S"]

        rho = r["rho"]

        x = list(range(1, S))

        y = [

            engset_pb(S, n, rho)

            for n in x
        ]

        fig, ax = plt.subplots(figsize=(10, 4))

        ax.plot(
            x,
            y,
            marker='o',
            linewidth=2.5
        )

        ax.axhline(
            0.2,
            linestyle='--',
            label='Threshold 0.2'
        )

        ax.set_xlabel("Jumlah Kanal")

        ax.set_ylabel(
            "Probabilitas Blocking"
        )

        ax.grid(True)

        ax.legend()

        st.pyplot(fig)


# =====================================================
# RIWAYAT
# =====================================================

elif page == "📁 Riwayat":

    st.markdown("""
    <div class="section-title">
    📁 Riwayat Simulasi
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.history:

        rows = []

        for i, r in enumerate(
            st.session_state.history,
            1
        ):

            rows.append({

                "No": i,
                "Waktu": r["time"],
                "S": r["S"],
                "N": r["N"],
                "ρ": r["rho"],
                "M": round(r["M"], 6),
                "Pb": round(r["Pb"], 6),
                "Iterasi": r["iter"],
                "Status": r["status"]

            })

        df_history = pd.DataFrame(rows)

        st.dataframe(
            df_history,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "Belum ada riwayat simulasi."
        )


# =====================================================
# EXPORT PDF
# =====================================================

def export_pdf(data, fig):

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4
    )

    styles = getSampleStyleSheet()

    elements = []

    title = Paragraph(
        "Laporan Simulasi Engset",
        styles['Title']
    )

    elements.append(title)

    elements.append(
        Spacer(1, 12)
    )

    tabel_data = [

        ["Parameter", "Nilai"],

        ["Jumlah Sumber", data["S"]],

        ["Jumlah Kanal", data["N"]],

        ["Traffic per Sumber", data["rho"]],

        ["Blocking Probability", f"{data['Pb']:.6f}"],

        ["Traffic Idle", f"{data['M']:.6f}"],

        ["Jumlah Iterasi", data["iter"]],

        ["Status Sistem", data["status"]]
    ]

    table = Table(tabel_data)

    table.setStyle(TableStyle([

        ('BACKGROUND', (0,0), (-1,0), colors.blue),

        ('TEXTCOLOR', (0,0), (-1,0), colors.white),

        ('GRID', (0,0), (-1,-1), 1, colors.black),

        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold')

    ]))

    elements.append(table)

    elements.append(
        Spacer(1, 20)
    )

    img_buffer = io.BytesIO()

    fig.savefig(img_buffer, format='png')

    img_buffer.seek(0)

    image = Image(
        img_buffer,
        width=400,
        height=200
    )

    elements.append(image)

    doc.build(elements)

    buffer.seek(0)

    return buffer


# =====================================================
# EXPORT SECTION
# =====================================================

if "result" in st.session_state:

    st.markdown("---")

    st.markdown("""
    <div class="section-title">
    📥 Export Laporan PDF
    </div>
    """, unsafe_allow_html=True)

    latest = st.session_state.result

    S = latest["S"]

    rho = latest["rho"]

    x = list(range(1, S))

    y = [

        engset_pb(S, n, rho)

        for n in x
    ]

    fig, ax = plt.subplots(figsize=(10, 4))

    ax.plot(
        x,
        y,
        marker='o',
        linewidth=2.5
    )

    ax.grid(True)

    pdf = export_pdf(
        latest,
        fig
    )

    st.download_button(
        label="⬇️ Download Laporan PDF",
        data=pdf,
        file_name="Laporan_Engset.pdf",
        mime="application/pdf"
    ).header-subtitle {
    font-size: 15px;
    opacity: 0.9;
}

.section-title {
    font-size: 24px;
    font-weight: bold;
    margin-top: 20px;
    margin-bottom: 15px;
    color: #1d4ed8;
}

.metric-grid {
    display: grid;
    grid-template-columns: repeat(4,1fr);
    gap: 15px;
}

.metric-card {
    background: white;
    padding: 20px;
    border-radius: 18px;
    border: 1px solid #dbeafe;
    text-align: center;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
}

.metric-value {
    font-size: 22px;
    font-weight: bold;
    color: #1d4ed8;
}

.metric-label {
    margin-top: 10px;
    color: #64748b;
}

.input-card {
    background: white;
    padding: 20px;
    border-radius: 20px;
    border: 1px solid #dbeafe;
    margin-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# SESSION STATE
# =====================================================
if "history" not in st.session_state:
    st.session_state.history = []


# =====================================================
# RUMUS ENGSET
# =====================================================
def nCr(n, r):

    if r > n:
        return 0

    return factorial(n) // (
        factorial(r) * factorial(n - r)
    )


def engset_pb(S, N, M):

    num = nCr(S - 1, N) * (M ** N)

    den = sum(
        nCr(S - 1, k) * (M ** k)
        for k in range(N + 1)
    )

    if den == 0:
        return 0

    return num / den


def iterate(S, N, rho):

    M = rho

    tol = 0.0001

    data = []

    i = 1

    while True:

        Pb = engset_pb(S, N, M)

        M_new = rho * (1 - Pb)

        diff = abs(M_new - M)

        data.append([
            i,
            round(M, 8),
            round(Pb, 8),
            round(diff, 8)
        ])

        if diff < tol:
            break

        M = M_new

        i += 1

    return M_new, Pb, data, i


# =====================================================
# EXPORT PDF
# =====================================================
def export_pdf(data, fig):

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=2*cm,
        rightMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'title',
        parent=styles['Title'],
        alignment=TA_CENTER,
        textColor=colors.HexColor("#1d4ed8")
    )

    elements = []

    elements.append(
        Paragraph(
            "LAPORAN ENGSETPRO",
            title_style
        )
    )

    elements.append(Spacer(1, 20))

    table_data = [
        ["Parameter", "Nilai"],
        ["Jumlah Sumber (S)", str(data["S"])],
        ["Jumlah Kanal (N)", str(data["N"])],
        ["Traffic per Sumber", str(data["rho"])],
        ["Blocking Probability", f"{data['Pb']:.6f}"],
        ["Traffic Idle", f"{data['M']:.6f}"],
        ["Iterasi", str(data["iter"])],
        ["Status", data["status"]],
    ]

    table = Table(table_data, colWidths=[7*cm, 7*cm])

    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1d4ed8")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 1, colors.black),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("BACKGROUND", (0,1), (-1,-1), colors.whitesmoke),
    ]))

    elements.append(table)

    elements.append(Spacer(1, 20))

    img_buffer = io.BytesIO()

    fig.savefig(img_buffer, format='png')

    img_buffer.seek(0)

    elements.append(
        Image(
            img_buffer,
            width=15*cm,
            height=7*cm
        )
    )

    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(
            f"Laporan dibuat pada {data['time']}",
            styles['Normal']
        )
    )

    doc.build(elements)

    buffer.seek(0)

    return buffer


# =====================================================
# HEADER
# =====================================================
st.markdown("""
<div class="unpix-header">
    <div class="header-title">
        📡 EngsetPro Professional
    </div>

    <div class="header-subtitle">
        Sistem Analisis Probabilitas Blocking Engset
    </div>
</div>
""", unsafe_allow_html=True)


# =====================================================
# SIDEBAR
# =====================================================
with st.sidebar:

    st.title("📂 Navigasi")

    page = st.radio(
        "Pilih Menu",
        [
            "🏠 Dashboard",
            "📊 Analisis",
            "📁 Riwayat"
        ]
    )

    st.markdown("---")

    st.info(
        "Aplikasi simulasi sistem telekomunikasi"
    )


# =====================================================
# DASHBOARD
# =====================================================
if page == "🏠 Dashboard":

    st.markdown("""
    <div class="section-title">
        📥 Input Parameter Sistem
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="input-card">',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        S = st.number_input(
            "Jumlah Sumber (S)",
            min_value=1,
            value=10
        )

    with col2:

        N = st.number_input(
            "Jumlah Kanal (N)",
            min_value=1,
            value=3
        )

    with col3:

        rho = st.number_input(
            "Traffic per Sumber (ρ)",
            min_value=0.0,
            value=0.5,
            step=0.01
        )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    run = st.button(
        "🚀 Jalankan Analisis"
    )

    if run:

        if N >= S:

            st.error(
                "Jumlah kanal harus lebih kecil dari jumlah sumber"
            )

        else:

            M, Pb, iter_data, iteration = iterate(
                S,
                N,
                rho
            )

            status = (
                "OPTIMAL"
                if Pb < 0.2
                else "PADAT"
            )

            result = {
                "S": S,
                "N": N,
                "rho": rho,
                "M": M,
                "Pb": Pb,
                "iter": iteration,
                "status": status,
                "iter_data": iter_data,
                "time": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            }

            st.session_state.result = result

            st.session_state.history.append(
                result
            )

    if "result" in st.session_state:

        r = st.session_state.result

        st.markdown("""
        <div class="section-title">
            📊 Hasil Simulasi
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="metric-grid">

            <div class="metric-card">
                <div class="metric-value">
                    {r['Pb']:.6f}
                </div>

                <div class="metric-label">
                    Blocking Probability
                </div>
            </div>

            <div class="metric-card">
                <div class="metric-value">
                    {r['M']:.6f}
                </div>

                <div class="metric-label">
                    Traffic Idle
                </div>
            </div>

            <div class="metric-card">
                <div class="metric-value">
                    {r['iter']}
                </div>

                <div class="metric-label">
                    Iterasi
                </div>
            </div>

            <div class="metric-card">
                <div class="metric-value">
                    {r['status']}
                </div>

                <div class="metric-label">
                    Status Sistem
                </div>
            </div>

        </div>
        """, unsafe_allow_html=True)


# =====================================================
# ANALISIS
# =====================================================
elif page == "📊 Analisis":

    st.markdown("""
    <div class="section-title">
        📊 Analisis Sistem
    </div>
    """, unsafe_allow_html=True)

    if "result" not in st.session_state:

        st.warning(
            "Jalankan simulasi terlebih dahulu"
        )

    else:

        r = st.session_state.result

        df = pd.DataFrame(
            r["iter_data"],
            columns=[
                "Iterasi",
                "M",
                "Pb",
                "Selisih"
            ]
        )

        st.dataframe(
            df,
            use_container_width=True
        )

        S = r["S"]

        rho = r["rho"]

        x = list(range(1, S))

        y = [
            engset_pb(S, n, rho)
            for n in x
        ]

        fig, ax = plt.subplots(figsize=(10,4))

        ax.plot(
            x,
            y,
            marker='o',
            linewidth=2
        )

        ax.axhline(
            0.2,
            linestyle='--',
            label='Threshold'
        )

        ax.set_xlabel(
            "Jumlah Kanal"
        )

        ax.set_ylabel(
            "Blocking Probability"
        )

        ax.grid(True)

        ax.legend()

        st.pyplot(fig)


# =====================================================
# RIWAYAT
# =====================================================
elif page == "📁 Riwayat":

    st.markdown("""
    <div class="section-title">
        📁 Riwayat Simulasi
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.history:

        rows = []

        for i, r in enumerate(
            st.session_state.history,
            1
        ):

            rows.append({
                "No": i,
                "Waktu": r["time"],
                "S": r["S"],
                "N": r["N"],
                "ρ": r["rho"],
                "Pb": round(r["Pb"], 6),
                "Status": r["status"]
            })

        df_history = pd.DataFrame(rows)

        st.dataframe(
            df_history,
            use_container_width=True
        )

    else:

        st.info(
            "Belum ada riwayat simulasi"
        )


# =====================================================
# EXPORT PDF
# =====================================================
if "result" in st.session_state:

    st.markdown("---")

    latest = st.session_state.result

    S = latest["S"]

    rho = latest["rho"]

    x = list(range(1, S))

    y = [
        engset_pb(S, n, rho)
        for n in x
    ]

    fig, ax = plt.subplots(figsize=(10,4))

    ax.plot(
        x,
        y,
        marker='o'
    )

    ax.grid(True)

    pdf = export_pdf(
        latest,
        fig
    )

    st.download_button(
        label="⬇️ Download PDF",
        data=pdf,
        file_name="Laporan_EngsetPro.pdf",
        mime="application/pdf"
    )# ENGSET FORMULA
# =========================================================

def engset_blocking_probability(S, N, traffic):

    numerator = nCr(S - 1, N) * (traffic ** N)

    denominator = 0

    for k in range(N + 1):

        denominator += (
            nCr(S - 1, k) * (traffic ** k)
        )

    if denominator == 0:
        return 0

    return numerator / denominator

# =========================================================
# APP
# =========================================================

class EngsetPro(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title("EngsetPro Simulator")

        self.geometry("430x780")

        self.resizable(False, False)

        self.configure(fg_color=BG)

        self.history_data = []

        self.last_iteration_data = []

        self.last_result = {}

        # =================================================
        # HEADER
        # =================================================

        self.header = ctk.CTkFrame(
            self,
            height=75,
            fg_color=PRIMARY,
            corner_radius=0
        )

        self.header.pack(fill="x")

        title = ctk.CTkLabel(
            self.header,
            text="ENGSETPRO",
            font=("Arial", 26, "bold"),
            text_color="white"
        )

        title.pack(
            pady=(10, 0)
        )

        sub = ctk.CTkLabel(
            self.header,
            text="Blocking Probability Simulator",
            font=("Arial", 11),
            text_color="white"
        )

        sub.pack()

        # =================================================
        # CONTENT
        # =================================================

        self.content = ctk.CTkFrame(
            self,
            fg_color=BG
        )

        self.content.pack(
            fill="both",
            expand=True
        )

        # =================================================
        # PAGES
        # =================================================

        self.home_page = ctk.CTkScrollableFrame(
            self.content,
            fg_color=BG
        )

        self.analysis_page = ctk.CTkScrollableFrame(
            self.content,
            fg_color=BG
        )

        self.history_page = ctk.CTkScrollableFrame(
            self.content,
            fg_color=BG
        )

        self.create_home_page()
        self.create_analysis_page()
        self.create_history_page()

        self.show_page(self.home_page)

        # =================================================
        # NAVBAR
        # =================================================

        self.navbar = ctk.CTkFrame(
            self,
            height=70,
            fg_color=CARD,
            corner_radius=0
        )

        self.navbar.pack(
            side="bottom",
            fill="x"
        )

        self.create_nav_button(
            "🏠\nHome",
            lambda: self.show_page(self.home_page)
        )

        self.create_nav_button(
            "📈\nAnalisis",
            lambda: self.show_page(self.analysis_page)
        )

        self.create_nav_button(
            "🕘\nRiwayat",
            lambda: self.show_page(self.history_page)
        )

    # =====================================================
    # NAV BUTTON
    # =====================================================

    def create_nav_button(self, text, command):

        btn = ctk.CTkButton(
            self.navbar,
            text=text,
            width=115,
            height=50,
            fg_color="transparent",
            text_color=PRIMARY,
            hover_color="#DBEAFE",
            font=("Arial", 13, "bold"),
            command=command
        )

        btn.pack(
            side="left",
            padx=8,
            pady=10
        )

    # =====================================================
    # SHOW PAGE
    # =====================================================

    def show_page(self, page):

        for widget in self.content.winfo_children():
            widget.pack_forget()

        page.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

    # =====================================================
    # CARD
    # =====================================================

    def create_card(self, parent):

        return ctk.CTkFrame(
            parent,
            fg_color=CARD,
            corner_radius=20
        )

    # =====================================================
    # ENTRY
    # =====================================================

    def create_entry(self, parent, placeholder):

        entry = ctk.CTkEntry(
            parent,
            height=48,
            corner_radius=14,
            placeholder_text=placeholder,
            font=("Arial", 14)
        )

        entry.pack(
            fill="x",
            padx=18,
            pady=8
        )

        return entry

    # =====================================================
    # HOME PAGE
    # =====================================================

    def create_home_page(self):

        # INPUT CARD

        input_card = self.create_card(
            self.home_page
        )

        input_card.pack(
            fill="x",
            pady=8
        )

        title = ctk.CTkLabel(
            input_card,
            text="INPUT PARAMETER",
            font=("Arial", 20, "bold"),
            text_color=TEXT
        )

        title.pack(pady=15)

        self.s_entry = self.create_entry(
            input_card,
            "Jumlah Source (S)"
        )

        self.n_entry = self.create_entry(
            input_card,
            "Jumlah Channel (N)"
        )

        self.rho_entry = self.create_entry(
            input_card,
            "Traffic per Source (ρ)"
        )

        button = ctk.CTkButton(
            input_card,
            text="HITUNG SEKARANG",
            height=50,
            corner_radius=14,
            fg_color=PRIMARY,
            hover_color=PRIMARY_DARK,
            font=("Arial", 15, "bold"),
            command=self.calculate
        )

        button.pack(
            fill="x",
            padx=18,
            pady=18
        )

        # RESULT CARD

        result_card = self.create_card(
            self.home_page
        )

        result_card.pack(
            fill="x",
            pady=8
        )

        title2 = ctk.CTkLabel(
            result_card,
            text="HASIL ANALISIS",
            font=("Arial", 20, "bold"),
            text_color=TEXT
        )

        title2.pack(pady=15)

        self.pb_label = ctk.CTkLabel(
            result_card,
            text="Blocking Probability : -",
            font=("Arial", 17),
            text_color=TEXT
        )

        self.pb_label.pack(pady=8)

        self.m_label = ctk.CTkLabel(
            result_card,
            text="Traffic Idle (M) : -",
            font=("Arial", 16),
            text_color=TEXT
        )

        self.m_label.pack(pady=8)

        self.iter_label = ctk.CTkLabel(
            result_card,
            text="Jumlah Iterasi : -",
            font=("Arial", 16),
            text_color=TEXT
        )

        self.iter_label.pack(pady=8)

        self.status_label = ctk.CTkLabel(
            result_card,
            text="Status : -",
            font=("Arial", 24, "bold"),
            text_color=PRIMARY
        )

        self.status_label.pack(
            pady=(5, 18)
        )

    # =====================================================
    # ANALYSIS PAGE
    # =====================================================

    def create_analysis_page(self):

        self.graph_card = self.create_card(
            self.analysis_page
        )

        self.graph_card.pack(
            fill="both",
            expand=True,
            pady=8
        )

        title = ctk.CTkLabel(
            self.graph_card,
            text="GRAFIK ANALISIS",
            font=("Arial", 20, "bold"),
            text_color=TEXT
        )

        title.pack(pady=15)

        # =================================================
        # ITERATION TITLE
        # =================================================

        iter_title = ctk.CTkLabel(
            self.graph_card,
            text="TABEL ITERASI KONVERGENSI",
            font=("Arial", 18, "bold"),
            text_color=TEXT
        )

        iter_title.pack(pady=(10, 5))

        # =================================================
        # ITERATION TABLE
        # =================================================

        columns = (
            "Iterasi",
            "M",
            "P(b)",
            "Selisih"
        )

        self.iteration_table = ttk.Treeview(
            self.graph_card,
            columns=columns,
            show="headings",
            height=8
        )

        style = ttk.Style()

        style.theme_use("clam")

        style.configure(
            "Treeview",
            rowheight=28,
            font=("Arial", 10)
        )

        style.configure(
            "Treeview.Heading",
            font=("Arial", 10, "bold")
        )

        widths = {
            "Iterasi": 80,
            "M": 110,
            "P(b)": 110,
            "Selisih": 110
        }

        for col in columns:

            self.iteration_table.heading(
                col,
                text=col
            )

            self.iteration_table.column(
                col,
                width=widths[col],
                anchor="center"
            )

        self.iteration_table.pack(
            fill="x",
            padx=10,
            pady=10
        )

    # =====================================================
    # HISTORY PAGE
    # =====================================================

    def create_history_page(self):

        history_card = self.create_card(
            self.history_page
        )

        history_card.pack(
            fill="both",
            expand=True,
            pady=8
        )

        title = ctk.CTkLabel(
            history_card,
            text="RIWAYAT SIMULASI",
            font=("Arial", 20, "bold"),
            text_color=TEXT
        )

        title.pack(pady=15)

        columns = (
            "No",
            "Waktu",
            "S",
            "N",
            "ρ",
            "M",
            "P(b)",
            "Iterasi",
            "Status"
        )

        self.history_table = ttk.Treeview(
            history_card,
            columns=columns,
            show="headings",
            height=12
        )

        widths = {
            "No": 40,
            "Waktu": 120,
            "S": 40,
            "N": 40,
            "ρ": 60,
            "M": 70,
            "P(b)": 80,
            "Iterasi": 70,
            "Status": 90
        }

        for col in columns:

            self.history_table.heading(
                col,
                text=col
            )

            self.history_table.column(
                col,
                width=widths[col],
                anchor="center"
            )

        self.history_table.pack(
            fill="both",
            padx=10,
            pady=10
        )

        # BUTTONS

        frame = ctk.CTkFrame(
            history_card,
            fg_color="transparent"
        )

        frame.pack(
            fill="x",
            padx=15,
            pady=10
        )

        export_btn = ctk.CTkButton(
            frame,
            text="EXPORT PDF",
            height=45,
            fg_color=PRIMARY,
            hover_color=PRIMARY_DARK,
            font=("Arial", 14, "bold"),
            command=self.export_pdf
        )

        export_btn.pack(
            side="left",
            expand=True,
            fill="x",
            padx=5
        )

        clear_btn = ctk.CTkButton(
            frame,
            text="HAPUS",
            height=45,
            fg_color=DANGER,
            hover_color="#B91C1C",
            font=("Arial", 14, "bold"),
            command=self.clear_history
        )

        clear_btn.pack(
            side="left",
            expand=True,
            fill="x",
            padx=5
        )

    # =====================================================
    # CALCULATE
    # =====================================================

    def calculate(self):

        try:

            S = int(self.s_entry.get())
            N = int(self.n_entry.get())
            rho = float(self.rho_entry.get())

            if N >= S:

                messagebox.showerror(
                    "Error",
                    "N harus lebih kecil dari S"
                )

                return

            self.last_iteration_data.clear()

            M = rho

            tolerance = 0.0001

            iteration = 1

            while True:

                Pb = engset_blocking_probability(
                    S,
                    N,
                    M
                )

                M_new = rho * (1 - Pb)

                diff = abs(M_new - M)

                self.last_iteration_data.append(
                    (
                        iteration,
                        round(M, 6),
                        round(Pb, 6),
                        round(diff, 6)
                    )
                )

                if diff < tolerance:
                    break

                M = M_new

                iteration += 1

            final_pb = Pb

            final_m = M_new

            if final_pb < 0.2:

                status = "OPTIMAL"
                color = SUCCESS

            else:

                status = "PADAT"
                color = DANGER

            # RESULT

            self.pb_label.configure(
                text=f"Blocking Probability : {final_pb:.6f}"
            )

            self.m_label.configure(
                text=f"Traffic Idle (M) : {final_m:.6f}"
            )

            self.iter_label.configure(
                text=f"Jumlah Iterasi : {iteration}"
            )

            self.status_label.configure(
                text=f"Status : {status}",
                text_color=color
            )

            # UPDATE ITERATION TABLE

            for item in self.iteration_table.get_children():

                self.iteration_table.delete(item)

            for row in self.last_iteration_data:

                self.iteration_table.insert(
                    "",
                    "end",
                    values=(
                        row[0],
                        row[1],
                        row[2],
                        row[3]
                    )
                )

            # SAVE LAST RESULT

            self.last_result = {
                "S": S,
                "N": N,
                "rho": rho,
                "M": final_m,
                "Pb": final_pb,
                "status": status,
                "iteration": iteration
            }

            # SAVE HISTORY

            waktu = datetime.now().strftime(
                "%d/%m/%Y %H:%M:%S"
            )

            self.history_data.append(
                (
                    waktu,
                    S,
                    N,
                    rho,
                    round(final_m, 6),
                    round(final_pb, 6),
                    iteration,
                    status
                )
            )

            self.update_history()

            self.create_graph(S, rho)

            messagebox.showinfo(
                "Sukses",
                "Perhitungan berhasil!"
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    # =====================================================
    # UPDATE HISTORY
    # =====================================================

    def update_history(self):

        for item in self.history_table.get_children():
            self.history_table.delete(item)

        for index, row in enumerate(
            self.history_data,
            start=1
        ):

            self.history_table.insert(
                "",
                "end",
                values=(
                    index,
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                    row[4],
                    row[5],
                    row[6],
                    row[7]
                )
            )

    # =====================================================
    # CLEAR HISTORY
    # =====================================================

    def clear_history(self):

        self.history_data.clear()

        for item in self.history_table.get_children():
            self.history_table.delete(item)

        messagebox.showinfo(
            "Sukses",
            "Riwayat berhasil dihapus"
        )

    # =====================================================
    # GRAPH
    # =====================================================

    def create_graph(self, S, rho):

        for widget in self.graph_card.winfo_children():

            if isinstance(widget, ctk.CTkLabel):
                continue

            if widget != self.iteration_table:
                widget.destroy()

        x = []
        y = []

        for n in range(1, S):

            pb = engset_blocking_probability(
                S,
                n,
                rho
            )

            x.append(n)
            y.append(pb)

        fig, ax = plt.subplots(
            figsize=(4, 3)
        )

        ax.plot(
            x,
            y,
            marker='o',
            linewidth=3,
            color=PRIMARY
        )

        ax.fill_between(
            x,
            y,
            alpha=0.2,
            color=PRIMARY
        )

        ax.axhline(
            y=0.2,
            linestyle='--',
            color='red'
        )

        ax.set_title(
            "Blocking Probability"
        )

        ax.set_xlabel(
            "Jumlah Channel"
        )

        ax.set_ylabel(
            "P(b)"
        )

        ax.grid(True)

        canvas = FigureCanvasTkAgg(
            fig,
            master=self.graph_card
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10,
            before=self.iteration_table
        )

    # =====================================================
    # EXPORT PDF
    # =====================================================

    def export_pdf(self):

        try:

            filename = (
                f"Engset_Report_"
                f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            )

            doc = SimpleDocTemplate(filename)

            styles = getSampleStyleSheet()

            elements = []

            # TITLE

            title = Paragraph(
                "<b>ENGSETPRO SIMULATOR REPORT</b>",
                styles['Title']
            )

            elements.append(title)

            elements.append(
                Spacer(1, 20)
            )

            # PARAMETER

            if self.last_result:

                parameter_text = f"""
                <b>Tanggal Export:</b>
                {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}<br/><br/>

                <b>Jumlah Source (S):</b> {self.last_result['S']}<br/>
                <b>Jumlah Channel (N):</b> {self.last_result['N']}<br/>
                <b>Traffic per Source (ρ):</b> {self.last_result['rho']}<br/>
                <b>Traffic Idle (M):</b> {self.last_result['M']:.6f}<br/>
                <b>Blocking Probability:</b> {self.last_result['Pb']:.6f}<br/>
                <b>Status:</b> {self.last_result['status']}<br/>
                <b>Jumlah Iterasi:</b> {self.last_result['iteration']}
                """

                param = Paragraph(
                    parameter_text,
                    styles['BodyText']
                )

                elements.append(param)

                elements.append(
                    Spacer(1, 20)
                )

            # HISTORY TABLE

            history_title = Paragraph(
                "<b>TABEL RIWAYAT SIMULASI</b>",
                styles['Heading2']
            )

            elements.append(history_title)

            elements.append(
                Spacer(1, 10)
            )

            history_data = [[
                "No",
                "Waktu",
                "S",
                "N",
                "ρ",
                "M",
                "P(b)",
                "Iterasi",
                "Status"
            ]]

            for index, row in enumerate(
                self.history_data,
                start=1
            ):

                history_data.append([
                    str(index),
                    str(row[0]),
                    str(row[1]),
                    str(row[2]),
                    str(row[3]),
                    str(row[4]),
                    str(row[5]),
                    str(row[6]),
                    str(row[7])
                ])

            history_table = Table(history_data)

            history_table.setStyle(TableStyle([

                ('BACKGROUND',
                 (0, 0),
                 (-1, 0),
                 colors.HexColor(PRIMARY)),

                ('TEXTCOLOR',
                 (0, 0),
                 (-1, 0),
                 colors.white),

                ('GRID',
                 (0, 0),
                 (-1, -1),
                 1,
                 colors.grey),

                ('ALIGN',
                 (0, 0),
                 (-1, -1),
                 'CENTER'),

                ('FONTNAME',
                 (0, 0),
                 (-1, 0),
                 'Helvetica-Bold'),

                ('FONTSIZE',
                 (0, 0),
                 (-1, -1),
                 8)

            ]))

            elements.append(history_table)

            elements.append(
                Spacer(1, 20)
            )

            # ITERATION TABLE

            iteration_title = Paragraph(
                "<b>TABEL ITERASI KONVERGENSI</b>",
                styles['Heading2']
            )

            elements.append(iteration_title)

            elements.append(
                Spacer(1, 10)
            )

            iteration_data = [[
                "Iterasi",
                "M",
                "P(b)",
                "Selisih"
            ]]

            for row in self.last_iteration_data:

                iteration_data.append([
                    str(row[0]),
                    str(row[1]),
                    str(row[2]),
                    str(row[3])
                ])

            iteration_table = Table(iteration_data)

            iteration_table.setStyle(TableStyle([

                ('BACKGROUND',
                 (0, 0),
                 (-1, 0),
                 colors.HexColor(PRIMARY)),

                ('TEXTCOLOR',
                 (0, 0),
                 (-1, 0),
                 colors.white),

                ('GRID',
                 (0, 0),
                 (-1, -1),
                 1,
                 colors.grey),

                ('ALIGN',
                 (0, 0),
                 (-1, -1),
                 'CENTER'),

                ('FONTNAME',
                 (0, 0),
                 (-1, 0),
                 'Helvetica-Bold')

            ]))

            elements.append(iteration_table)

            elements.append(
                Spacer(1, 20)
            )

            conclusion = Paragraph(
                "Kesimpulan: Sistem "
                f"<b>{self.last_result.get('status', '-')}</b> "
                "berdasarkan hasil perhitungan "
                "Blocking Probability menggunakan "
                "model Engset.",
                styles['BodyText']
            )

            elements.append(conclusion)

            doc.build(elements)

            messagebox.showinfo(
                "Sukses",
                f"PDF berhasil disimpan:\n{filename}"
            )

        except Exception as e:

            messagebox.showerror(
                "Error PDF",
                str(e)
            )

# =========================================================
# RUN APP
# =========================================================

if __name__ == "__main__":

    app = EngsetPro()
    app.mainloop()
