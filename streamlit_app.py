import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from math import log, exp
from datetime import datetime
import io

try:
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer,
        Table, TableStyle, HRFlowable
    )
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import cm
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    from reportlab.platypus import Image as RLImage
    PDF_OK = True
except ImportError:
    PDF_OK = False

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="EngsetPro",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════════════════════════
# GLOBAL CSS — Gen Z Pro Aesthetic
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;700&display=swap');

html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif !important; }

.stApp {
    background: linear-gradient(135deg, #f0f4ff 0%, #fafbff 50%, #f0f4ff 100%);
    min-height: 100vh;
}

/* Hide deploy button and default footer */
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
header    { visibility: hidden; }
.stDeployButton { display: none !important; }

/* ── Sidebar — Desktop Only ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e1b4b 40%, #1a1060 100%) !important;
    border-right: 1px solid rgba(139,92,246,0.2) !important;
    box-shadow: 4px 0 32px rgba(139,92,246,0.15);
}
[data-testid="stSidebar"] > div:first-child { padding-top: 0 !important; }
[data-testid="stSidebar"] * { color: rgba(255,255,255,0.9) !important; }
[data-testid="stSidebar"] hr {
    border-color: rgba(139,92,246,0.25) !important;
}

/* Sidebar radio buttons */
[data-testid="stSidebar"] .stRadio > div {
    gap: 4px !important;
}
[data-testid="stSidebar"] .stRadio label {
    background: rgba(255,255,255,0.04) !important;
    border-radius: 12px !important;
    padding: 10px 14px !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    border: 1px solid transparent !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    color: rgba(255,255,255,0.75) !important;
    width: 100%;
    margin: 2px 0;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(139,92,246,0.15) !important;
    border-color: rgba(139,92,246,0.3) !important;
    color: #fff !important;
}
[data-testid="stSidebar"] .stRadio [data-baseweb="radio"] > div:first-child {
    display: none !important;
}

/* ── Cards ── */
.card {
    background: rgba(255,255,255,0.85);
    backdrop-filter: blur(12px);
    border-radius: 20px;
    padding: 1.4rem 1.6rem;
    box-shadow: 0 4px 24px rgba(99,102,241,0.08), 0 1px 3px rgba(0,0,0,0.04);
    border: 1px solid rgba(99,102,241,0.08);
    margin-bottom: 1rem;
    transition: box-shadow 0.2s;
}
.card:hover {
    box-shadow: 0 8px 32px rgba(99,102,241,0.13), 0 2px 6px rgba(0,0,0,0.05);
}

/* ── Hero ── */
.hero-card {
    background: linear-gradient(135deg, #6366f1 0%, #4f46e5 40%, #3730a3 100%);
    border-radius: 28px;
    padding: 2.2rem 2rem 1.8rem;
    color: white;
    margin-bottom: 1.2rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 12px 40px rgba(99,102,241,0.4), 0 4px 12px rgba(0,0,0,0.1);
}
.hero-card::before {
    content:""; position:absolute; top:-80px; right:-60px;
    width:280px; height:280px; border-radius:50%;
    background: radial-gradient(circle, rgba(167,139,250,0.25) 0%, transparent 70%);
}
.hero-card::after {
    content:""; position:absolute; bottom:-70px; left:20%;
    width:220px; height:220px; border-radius:50%;
    background: radial-gradient(circle, rgba(99,102,241,0.2) 0%, transparent 70%);
}

/* ── Chip grid ── */
.chip-grid {
    display:grid; grid-template-columns:1fr 1fr 1fr;
    gap:12px; margin-bottom:1.2rem;
}
.chip {
    background: rgba(255,255,255,0.9);
    border-radius:18px; padding:1.1rem 0.8rem;
    text-align:center;
    box-shadow: 0 2px 16px rgba(99,102,241,0.08);
    border: 1px solid rgba(99,102,241,0.08);
    transition: transform 0.2s, box-shadow 0.2s;
}
.chip:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(99,102,241,0.14); }
.chip-icon { font-size:1.4rem; margin-bottom:6px; }
.chip-val  { font-size:1.1rem; font-weight:800; color:#1e1b4b; font-family:'JetBrains Mono',monospace; }
.chip-lbl  { font-size:0.68rem; color:#9ca3af; text-transform:uppercase; letter-spacing:0.08em; margin-top:3px; }

/* ── Plan card ── */
.plan-card {
    background: rgba(255,255,255,0.9);
    border-radius:18px; padding:1rem 1.2rem;
    display:flex; align-items:center; gap:14px; margin-bottom:10px;
    box-shadow: 0 2px 12px rgba(99,102,241,0.06);
    border: 1px solid rgba(99,102,241,0.06);
    transition: all 0.2s;
}
.plan-card:hover {
    box-shadow: 0 6px 20px rgba(99,102,241,0.12);
    transform: translateX(4px);
}
.plan-icon-wrap {
    width:46px; height:46px; border-radius:14px;
    display:flex; align-items:center; justify-content:center;
    font-size:1.3rem; flex-shrink:0;
}
.plan-icon-blue   { background: linear-gradient(135deg,rgba(99,102,241,0.15),rgba(99,102,241,0.08)); }
.plan-icon-green  { background: linear-gradient(135deg,rgba(34,197,94,0.15),rgba(34,197,94,0.08)); }
.plan-icon-amber  { background: linear-gradient(135deg,rgba(245,158,11,0.15),rgba(245,158,11,0.08)); }
.plan-icon-red    { background: linear-gradient(135deg,rgba(239,68,68,0.15),rgba(239,68,68,0.08)); }
.plan-icon-purple { background: linear-gradient(135deg,rgba(168,85,247,0.15),rgba(168,85,247,0.08)); }
.plan-info { flex:1; }
.plan-name { font-size:0.92rem; font-weight:700; color:#1e1b4b; margin:0; }
.plan-desc { font-size:0.78rem; color:#9ca3af; margin:2px 0 0; }
.plan-val  { font-size:1rem; font-weight:800; color:#6366f1; font-family:'JetBrains Mono',monospace; }

/* ── GoS badge ── */
.gos { display:inline-block; padding:4px 14px; border-radius:100px;
       font-size:0.78rem; font-weight:700; letter-spacing:0.04em; }
.gos-great { background: linear-gradient(135deg,#dcfce7,#bbf7d0); color:#166534; }
.gos-good  { background: linear-gradient(135deg,#d1fae5,#a7f3d0); color:#065f46; }
.gos-ok    { background: linear-gradient(135deg,#fef9c3,#fde68a); color:#713f12; }
.gos-bad   { background: linear-gradient(135deg,#fee2e2,#fecaca); color:#7f1d1d; }

/* ── Formula wrap — PERBAIKAN UTAMA ── */
.formula-wrap {
    background: linear-gradient(135deg, #f5f3ff 0%, #ede9fe 100%);
    border: 2px solid rgba(99,102,241,0.2);
    border-radius: 24px;
    padding: 2rem;
    margin-bottom: 1.2rem;
    position: relative;
    overflow: hidden;
}
.formula-wrap::before {
    content:""; position:absolute; top:-40px; right:-40px;
    width:160px; height:160px; border-radius:50%;
    background: radial-gradient(circle, rgba(99,102,241,0.08) 0%, transparent 70%);
}
.formula-tag {
    display:inline-block;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color:#fff;
    font-size:0.7rem; font-weight:800; letter-spacing:0.12em;
    text-transform:uppercase; padding:5px 14px; border-radius:100px; margin-bottom:1.4rem;
    box-shadow: 0 4px 12px rgba(99,102,241,0.3);
}
.formula-body {
    font-family:'JetBrains Mono',monospace; font-size:0.88rem; color:#1e1b4b;
    line-height:2.4;
    background: rgba(255,255,255,0.7);
    border-radius:16px;
    padding:1.2rem 1.6rem;
    border: 1px solid rgba(99,102,241,0.1);
}
.formula-legend {
    display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-top:1.2rem;
}
.fl-item { font-size:0.82rem; color:#4c1d95; display:flex; align-items:baseline; gap:8px; }
.fl-sym  { font-family:'JetBrains Mono',monospace; font-weight:800; color:#6366f1; min-width:18px; }

/* ── Section ── */
.sec-title {
    font-size:1.05rem; font-weight:800; color:#1e1b4b; margin:0 0 0.8rem;
    display: flex; align-items: center; gap: 8px;
}

/* ── Banners ── */
.eng-warn {
    background: linear-gradient(135deg, #fffbeb, #fef3c7);
    border: 1px solid #fcd34d;
    border-radius:14px; padding:0.9rem 1.2rem;
    color:#92400e; font-size:0.87rem; margin-bottom:1rem;
    box-shadow: 0 2px 8px rgba(245,158,11,0.1);
}
.eng-info {
    background: linear-gradient(135deg, #eff6ff, #dbeafe);
    border: 1px solid #93c5fd;
    border-radius:14px; padding:0.9rem 1.2rem;
    color:#1e40af; font-size:0.87rem; margin-bottom:1rem;
}
.eng-ok {
    background: linear-gradient(135deg, #f0fdf4, #dcfce7);
    border: 1px solid #86efac;
    border-radius:14px; padding:0.9rem 1.2rem;
    color:#166534; font-size:0.87rem; margin-bottom:1rem;
    box-shadow: 0 2px 8px rgba(34,197,94,0.1);
}

/* ── Table ── */
.eng-table {
    width:100%; border-collapse:collapse; font-size:0.85rem;
    border-radius:16px; overflow:hidden;
}
.eng-table th {
    background: linear-gradient(135deg, #6366f1, #4f46e5);
    color:#fff; font-size:0.7rem;
    text-transform:uppercase; letter-spacing:0.1em;
    padding:11px 14px; text-align:left; font-weight:700;
}
.eng-table td {
    padding:9px 14px; border-bottom:1px solid rgba(99,102,241,0.06);
    color:#374151; font-family:'JetBrains Mono',monospace; font-size:0.82rem;
}
.eng-table tr:hover td { background:#f5f3ff; }
.eng-table tr.active td { background:#ede9fe; font-weight:700; color:#1e1b4b; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #4f46e5) !important;
    color:#fff !important; border:none !important; border-radius:16px !important;
    padding:0.7rem 1.8rem !important; font-weight:800 !important;
    font-size:0.92rem !important;
    box-shadow: 0 6px 20px rgba(99,102,241,0.35) !important;
    transition: all 0.2s !important;
    letter-spacing: 0.01em !important;
}
.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 10px 28px rgba(99,102,241,0.45) !important;
}
.stButton > button:active { transform: translateY(-1px) !important; }

/* ── Progress ── */
.progress-wrap {
    background:#ede9fe; border-radius:100px; height:10px; margin:8px 0; overflow:hidden;
}
.progress-fill {
    height:100%; border-radius:100px;
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    transition: width 0.6s ease;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(99,102,241,0.07); border-radius:16px;
    padding:5px; gap:4px; border:none;
}
.stTabs [data-baseweb="tab"] {
    border-radius:12px; font-weight:700; font-size:0.88rem;
    color:#6b7280; padding:9px 22px;
    transition: all 0.2s;
}
.stTabs [aria-selected="true"] {
    background: #fff !important; color:#6366f1 !important;
    box-shadow: 0 3px 12px rgba(99,102,241,0.15) !important;
}

/* ── Mobile nav selectbox ── */
@media (max-width: 768px) {
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="stSidebarCollapsedControl"] { display: none !important; }

    div[data-testid="stSelectbox"] {
        display: block !important;
        background: linear-gradient(135deg, #0f172a, #1e1b4b) !important;
        border-radius: 0 0 20px 20px !important;
        padding: 0.6rem 0.9rem 0.8rem !important;
        margin-bottom: 1rem !important;
        box-shadow: 0 6px 24px rgba(99,102,241,0.35) !important;
        position: fixed !important;
        top: 0 !important; left: 0 !important; right: 0 !important;
        z-index: 99999 !important; width: 100% !important;
    }
    div[data-testid="stSelectbox"] label {
        color: rgba(255,255,255,0.7) !important;
        font-size: 0.7rem !important; font-weight: 800 !important;
        text-transform: uppercase !important; letter-spacing: 0.1em !important;
    }
    div[data-testid="stSelectbox"] > div > div {
        background: rgba(255,255,255,0.1) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 14px !important; color: #fff !important;
    }
    div[data-testid="stSelectbox"] > div > div > div {
        color: #fff !important; font-weight: 700 !important; font-size: 1rem !important;
    }
    div[data-testid="stSelectbox"] svg { fill: #fff !important; }

    .main .block-container {
        padding-left: 0.75rem !important; padding-right: 0.75rem !important;
        padding-top: 5.5rem !important; max-width: 100% !important;
    }
}

/* Desktop: sembunyikan selectbox mobile */
@media (min-width: 769px) {
    /* Hanya sembunyikan selectbox pertama (mobile nav) */
    .mobile-nav-selectbox { display: none !important; }
    #mobile-params-label { display: none !important; }

    .main .block-container {
        padding-top: 1.5rem !important;
        max-width: 1200px !important;
    }
}

/* ── Equation SVG container ── */
.eq-container {
    display:flex; justify-content:center; align-items:center;
    padding: 1.8rem 1rem; margin: 0.5rem 0;
    background: rgba(255,255,255,0.8);
    border-radius:20px;
    border: 1px solid rgba(99,102,241,0.1);
}

/* ── Stat highlight box ── */
.stat-highlight {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    border-radius: 20px;
    padding: 1.4rem;
    text-align: center;
    color: white;
    margin-bottom: 1rem;
}
.stat-highlight .stat-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 2.2rem;
    font-weight: 800;
    line-height: 1;
    margin-bottom: 6px;
}
.stat-highlight .stat-label {
    font-size: 0.78rem;
    opacity: 0.75;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-weight: 600;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #f5f3ff; }
::-webkit-scrollbar-thumb { background: #c4b5fd; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #a78bfa; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# MENU OPTIONS
# ═══════════════════════════════════════════════════════════════════════════════
MENU_OPTIONS = [
    "🏠  Dashboard",
    "🧮  Kalkulator Engset",
    "📐  Hitung Traffic A",
    "📊  Analisis Dan Grafik",
    "📄  Export Laporan"
]

# Selectbox mobile — hanya muncul di mobile via CSS
st.markdown('<div class="mobile-nav-selectbox">', unsafe_allow_html=True)
mobile_page = st.selectbox("📋 Menu", MENU_OPTIONS, key="mobile_nav")
st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# CORE ENGSET
# ═══════════════════════════════════════════════════════════════════════════════
def log_factorial(n):
    if n <= 1: return 0.0
    return sum(log(i) for i in range(2, n + 1))

def log_comb(n, k):
    if k < 0 or k > n: return float('-inf')
    return log_factorial(n) - log_factorial(k) - log_factorial(n - k)

def engset(S, N, A):
    if A <= 0 or A >= S or N <= 0 or S <= N:
        return None
    ratio = A / (S - A)
    if ratio <= 0: return None
    log_ratio = log(ratio)
    log_numer = log_comb(S-1, N) + N * log_ratio
    log_terms = [log_comb(S-1, i) + i * log_ratio for i in range(N+1)]
    max_t     = max(log_terms)
    log_denom = max_t + log(sum(exp(t - max_t) for t in log_terms))
    return max(0.0, min(1.0, exp(log_numer - log_denom)))

def gos_label(p):
    if p < 0.001: return "Sangat Baik", "gos-great"
    if p < 0.01:  return "Baik",        "gos-good"
    if p < 0.05:  return "Cukup",       "gos-ok"
    return "Buruk", "gos-bad"

def find_min_N(S, A, target=0.01):
    for n in range(1, S):
        p = engset(S, n, A)
        if p is not None and p <= target:
            return n
    return None


# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR (desktop only)
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="background:linear-gradient(135deg,rgba(139,92,246,0.2),rgba(99,102,241,0.1));
         border-radius:20px; padding:1.4rem 1.2rem 1.2rem; margin-bottom:1.6rem;
         text-align:center; border:1px solid rgba(139,92,246,0.2);">
      <div style="font-size:2.4rem; margin-bottom:6px;">📡</div>
      <div style="font-size:1.4rem;font-weight:900;color:#fff;letter-spacing:-0.02em;">EngsetPro</div>
      <div style="font-size:0.68rem;color:rgba(255,255,255,0.45);letter-spacing:0.14em;
           margin-top:3px;text-transform:uppercase;font-weight:600;">Rekayasa Trafik v2.0</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div style="font-size:0.68rem;font-weight:800;color:rgba(255,255,255,0.35);'
        'letter-spacing:0.14em;text-transform:uppercase;margin-bottom:10px;padding-left:4px;">Navigasi</div>',
        unsafe_allow_html=True
    )

    page = st.radio(
        "nav", MENU_OPTIONS,
        index=MENU_OPTIONS.index(st.session_state.get("mobile_nav", MENU_OPTIONS[0])),
        label_visibility="collapsed"
    )
    if page != st.session_state.get("mobile_nav"):
        st.session_state["mobile_nav"] = page
        st.rerun()

    st.markdown("<hr style='margin: 1.4rem 0; border-color:rgba(139,92,246,0.2);'>", unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background:rgba(255,255,255,0.06);border-radius:16px;padding:1.1rem;
         border:1px solid rgba(139,92,246,0.15);">
      <div style="font-size:0.68rem;color:rgba(255,255,255,0.4);text-transform:uppercase;
           letter-spacing:0.1em;margin-bottom:10px;font-weight:800;">⚡ Parameter Aktif</div>
      <div style="font-size:0.85rem;color:rgba(255,255,255,0.85);line-height:2.2;">
        S = <strong style="color:#a78bfa;">{st.session_state.get('S_calc', 20)}</strong> pengguna<br>
        N = <strong style="color:#a78bfa;">{st.session_state.get('N_calc', 5)}</strong> kanal<br>
        A = <strong style="color:#a78bfa;">{st.session_state.get('A_calc', 7.0):.1f}</strong> Erlang
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-top:auto;padding-top:2rem;text-align:center;
         font-size:0.7rem;color:rgba(255,255,255,0.2);line-height:1.8;">
      EngsetPro v2.0<br>Metode Log-space Arithmetic
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# SESSION STATE defaults
# ═══════════════════════════════════════════════════════════════════════════════
if "S_calc" not in st.session_state:
    st.session_state["S_calc"] = 20
if "N_calc" not in st.session_state:
    st.session_state["N_calc"] = 5
if "A_calc" not in st.session_state:
    st.session_state["A_calc"] = 7.0
if "kalkulasi_done" not in st.session_state:
    st.session_state["kalkulasi_done"] = True

# ═══════════════════════════════════════════════════════════════════════════════
# COMPUTE
# ═══════════════════════════════════════════════════════════════════════════════
S = st.session_state["S_calc"]
N = st.session_state["N_calc"]
A = st.session_state["A_calc"]

valid    = S > N and 0 < A < S
P        = engset(S, N, A) if valid else None
carried  = A * (1 - P) if P is not None else 0.0
lost     = A * P       if P is not None else 0.0
util_pct = (carried / N) * 100 if (P is not None and N > 0) else 0.0
gos_text, gos_cls = gos_label(P) if P is not None else ("—", "gos-ok")
min_n_1   = find_min_N(S, A, 0.01)  if valid else "—"
min_n_001 = find_min_N(S, A, 0.001) if valid else "—"

INDIGO = '#6366f1'
VIOLET = '#8b5cf6'
TEAL   = '#14b8a6'
AMBER  = '#f59e0b'
RED    = '#ef4444'
BG     = '#f8f7ff'


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE HEADER helper
# ═══════════════════════════════════════════════════════════════════════════════
def page_header(tag, title, sub):
    st.markdown(f"""
    <div style="margin-bottom:1.8rem;">
      <div style="font-size:0.7rem;color:#8b5cf6;font-weight:800;text-transform:uppercase;
           letter-spacing:0.14em;margin-bottom:6px;">{tag}</div>
      <h1 style="font-size:2rem;font-weight:900;color:#1e1b4b;margin:0;letter-spacing:-0.02em;">{title}</h1>
      <p style="color:#9ca3af;margin:6px 0 0;font-size:0.92rem;">{sub}</p>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# RUMUS ENGSET SVG — DIPERBAIKI: pakai &#8722; untuk minus, posisi rapi
# ══════════════════════════════════════════════════════════════════════════════
ENGSET_EQUATION_SVG = """
<svg viewBox="0 0 680 240" xmlns="http://www.w3.org/2000/svg"
     style="max-width:640px;width:100%;display:block;margin:0 auto;">
  <defs>
    <style>
      .sym  { font-family:'Georgia','Times New Roman',serif; fill:#1e1b4b; }
      .mono { font-family:'JetBrains Mono','Courier New',monospace; fill:#1e1b4b; }
      .blue { fill:#6366f1; }
      .viol { fill:#8b5cf6; }
      .gray { fill:#6b7280; font-family:'Plus Jakarta Sans',sans-serif; font-size:11px; }
    </style>
  </defs>

  <!-- === P = === -->
  <text x="28" y="115" class="sym" font-size="26" font-style="italic" font-weight="bold">P</text>
  <text x="52" y="115" class="sym" font-size="24">=</text>

  <!-- ============ NUMERATOR ============ -->
  <!-- C superscript (S-1) subscript N -->
  <!-- "S&#8722;1" at top of binomial -->
  <text x="88"  y="68" class="sym" font-size="11" fill="#6366f1">S&#8722;1</text>
  <!-- Big C -->
  <text x="88"  y="84" class="sym blue" font-size="22" font-weight="bold">C</text>
  <!-- "N" subscript -->
  <text x="108" y="92" class="sym" font-size="12">N</text>

  <!-- multiply sign -->
  <text x="128" y="82" class="sym" font-size="18" fill="#9ca3af">&#215;</text>

  <!-- fraction (A over S-A) with parentheses -->
  <text x="152" y="82" class="sym" font-size="26">(</text>
  <!-- A on top -->
  <text x="172" y="68" class="sym" font-size="17" text-anchor="middle">A</text>
  <!-- fraction bar -->
  <line x1="160" y1="73" x2="188" y2="73" stroke="#1e1b4b" stroke-width="1.4"/>
  <!-- S-A on bottom — pakai &#8722; -->
  <text x="174" y="88" class="sym" font-size="13" text-anchor="middle">S&#8722;A</text>
  <text x="192" y="82" class="sym" font-size="26">)</text>
  <!-- exponent N -->
  <text x="211" y="62" class="sym viol" font-size="14" font-style="italic">N</text>

  <!-- ============ FRACTION LINE ============ -->
  <line x1="76" y1="102" x2="400" y2="102" stroke="#6366f1" stroke-width="2.2"/>

  <!-- ============ DENOMINATOR ============ -->
  <!-- Sigma with limits -->
  <text x="78"  y="122" class="sym blue" font-size="11" font-weight="bold">N</text>
  <text x="74"  y="140" class="sym blue" font-size="32">&#931;</text>
  <text x="76"  y="158" class="sym blue" font-size="11" font-weight="bold">i=0</text>

  <!-- C superscript (S-1) subscript i -->
  <text x="116" y="122" class="sym" font-size="11" fill="#6366f1">S&#8722;1</text>
  <text x="116" y="138" class="sym blue" font-size="22" font-weight="bold">C</text>
  <text x="136" y="147" class="sym" font-size="12">i</text>

  <!-- multiply sign -->
  <text x="155" y="138" class="sym" font-size="18" fill="#9ca3af">&#215;</text>

  <!-- fraction (A over S-A) with parentheses — denominator -->
  <text x="175" y="138" class="sym" font-size="26">(</text>
  <text x="195" y="124" class="sym" font-size="17" text-anchor="middle">A</text>
  <line x1="183" y1="129" x2="211" y2="129" stroke="#1e1b4b" stroke-width="1.4"/>
  <text x="197" y="144" class="sym" font-size="13" text-anchor="middle">S&#8722;A</text>
  <text x="215" y="138" class="sym" font-size="26">)</text>
  <!-- exponent i -->
  <text x="234" y="118" class="sym viol" font-size="14" font-style="italic">i</text>

  <!-- ============ DIVIDER ============ -->
  <line x1="30" y1="178" x2="650" y2="178" stroke="#e0e7ff" stroke-width="1.5"/>

  <!-- ============ LEGEND ============ -->
  <!-- Kiri -->
  <text x="34"  y="197" class="sym" font-size="13" font-style="italic">P</text>
  <text x="47"  y="197" class="gray"> = Probabilitas Blocking</text>

  <text x="34"  y="216" class="sym" font-size="13" font-style="italic">S</text>
  <text x="47"  y="216" class="gray"> = Jumlah Source / Pengguna</text>

  <!-- Kanan -->
  <text x="340" y="197" class="sym" font-size="13" font-style="italic">N</text>
  <text x="353" y="197" class="gray"> = Jumlah Kanal / Server</text>

  <text x="340" y="216" class="sym" font-size="13" font-style="italic">A</text>
  <text x="353" y="216" class="gray"> = Traffic Offered (Erlang)</text>
</svg>
"""


# ══════════════════════════════════════════════════════════════════════════════
# ██ DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
active_page = st.session_state.get("mobile_nav", MENU_OPTIONS[0])
if active_page == "🏠  Dashboard":

    col_main, col_side = st.columns([2, 1], gap="large")

    with col_main:
        # Hero card
        st.markdown(f"""
        <div class="hero-card">
          <div style="font-size:0.72rem;font-weight:800;letter-spacing:0.14em;
               text-transform:uppercase;opacity:0.65;margin-bottom:0.4rem;">✦ Selamat Datang</div>
          <h1 style="font-size:2rem;font-weight:900;color:#fff;margin:0 0 0.3rem;
               line-height:1.1;letter-spacing:-0.02em;">
            EngsetPro Dashboard</h1>
          <p style="font-size:0.9rem;opacity:0.65;margin:0;">
            Analisis probabilitas blocking real-time — Model Engset Finite Source</p>
          <div style="margin-top:1.6rem;display:flex;gap:0.8rem;flex-wrap:wrap;">
            <div style="background:rgba(255,255,255,0.12);border-radius:14px;padding:10px 20px;
                 border:1px solid rgba(255,255,255,0.15);backdrop-filter:blur(4px);">
              <div style="font-size:0.65rem;opacity:0.65;text-transform:uppercase;
                   letter-spacing:0.1em;font-weight:700;">Source</div>
              <div style="font-size:1.5rem;font-weight:900;font-family:'JetBrains Mono',monospace;">
                S = {S}</div>
            </div>
            <div style="background:rgba(255,255,255,0.12);border-radius:14px;padding:10px 20px;
                 border:1px solid rgba(255,255,255,0.15);backdrop-filter:blur(4px);">
              <div style="font-size:0.65rem;opacity:0.65;text-transform:uppercase;
                   letter-spacing:0.1em;font-weight:700;">Kanal</div>
              <div style="font-size:1.5rem;font-weight:900;font-family:'JetBrains Mono',monospace;">
                N = {N}</div>
            </div>
            <div style="background:rgba(255,255,255,0.12);border-radius:14px;padding:10px 20px;
                 border:1px solid rgba(255,255,255,0.15);backdrop-filter:blur(4px);">
              <div style="font-size:0.65rem;opacity:0.65;text-transform:uppercase;
                   letter-spacing:0.1em;font-weight:700;">Traffic</div>
              <div style="font-size:1.5rem;font-weight:900;font-family:'JetBrains Mono',monospace;">
                A = {A:.1f}</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        if P is not None:
            st.markdown(f"""
            <div class="chip-grid">
              <div class="chip">
                <div class="chip-icon">📡</div>
                <div class="chip-val">{P:.4f}</div>
                <div class="chip-lbl">P Blocking</div>
              </div>
              <div class="chip">
                <div class="chip-icon">✅</div>
                <div class="chip-val">{carried:.3f}</div>
                <div class="chip-lbl">Carried (Erl)</div>
              </div>
              <div class="chip">
                <div class="chip-icon">❌</div>
                <div class="chip-val">{lost:.3f}</div>
                <div class="chip-lbl">Lost (Erl)</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<p class="sec-title">📋 Ringkasan Sistem</p>', unsafe_allow_html=True)

        items = [
            ("📶","plan-icon-blue",   "Probabilitas Blocking",  f"{P*100:.3f}%" if P else "—",   f"Grade: {gos_text}"),
            ("🔄","plan-icon-green",  "Traffic Carried",         f"{carried:.4f} Erl",             f"Dari {A:.1f} Erl ditawarkan"),
            ("📉","plan-icon-amber",  "Kanal Minimum GoS 1%",   f"N = {min_n_1}",                 "Untuk kualitas baik"),
            ("⚡","plan-icon-purple", "Utilisasi Kanal",         f"{util_pct:.1f}%",               f"Rata-rata per {N} kanal"),
        ]
        for icon, icon_cls, name, val, desc in items:
            st.markdown(f"""
            <div class="plan-card">
              <div class="plan-icon-wrap {icon_cls}">{icon}</div>
              <div class="plan-info">
                <p class="plan-name">{name}</p>
                <p class="plan-desc">{desc}</p>
              </div>
              <div class="plan-val">{val}</div>
            </div>
            """, unsafe_allow_html=True)

    with col_side:
        # Donut chart
        fig, ax = plt.subplots(figsize=(3.5, 3.5))
        fig.patch.set_facecolor('#ffffff'); ax.set_facecolor('#ffffff')
        sizes = [util_pct, 100-util_pct] if P is not None else [50, 50]
        clrs  = ['#6366f1','#ede9fe']   if P is not None else ['#ede9fe','#f5f3ff']
        ax.pie(sizes, colors=clrs, startangle=90,
               wedgeprops=dict(width=0.44, edgecolor='white', linewidth=4),
               counterclock=False)
        ax.text(0, 0.08, f"{util_pct:.1f}%" if P else "—",
                ha='center', va='center', fontsize=18, fontweight='bold',
                color='#1e1b4b', fontfamily='monospace')
        ax.text(0, -0.25, "utilisasi", ha='center', va='center',
                fontsize=9, color='#9ca3af')
        ax.axis('equal')
        plt.tight_layout(pad=0.5)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        pbar_w = min(100, (P or 0) * 500)
        bar_col = '#22c55e' if (P or 1) < 0.01 else '#f59e0b' if (P or 1) < 0.05 else '#ef4444'
        st.markdown(f"""
        <div class="card" style="text-align:center;padding:1.2rem;">
          <div style="font-size:0.7rem;color:#9ca3af;text-transform:uppercase;
               letter-spacing:0.1em;margin-bottom:10px;font-weight:700;">Grade Of Service</div>
          <span class="gos {gos_cls}" style="font-size:1rem;padding:8px 24px;">{gos_text}</span>
          <div style="margin-top:14px;">
            <div class="progress-wrap">
              <div class="progress-fill" style="width:{pbar_w:.1f}%;background:{bar_col};"></div>
            </div>
          </div>
          <div style="font-size:0.78rem;color:#9ca3af;margin-top:8px;font-family:'JetBrains Mono',monospace;">
            P = {f"{P:.6f}" if P is not None else "—"}
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="card">
          <div style="font-size:0.82rem;font-weight:800;color:#1e1b4b;margin-bottom:12px;">
            🎯 Rekomendasi Kanal</div>
          <div style="display:flex;justify-content:space-between;align-items:center;
               padding:8px 0;border-bottom:1px solid #f0f4ff;">
            <span style="font-size:0.8rem;color:#9ca3af;">GoS 1%</span>
            <strong style="color:#6366f1;font-family:'JetBrains Mono',monospace;">N = {min_n_1}</strong>
          </div>
          <div style="display:flex;justify-content:space-between;align-items:center;padding-top:8px;">
            <span style="font-size:0.8rem;color:#9ca3af;">GoS 0.1%</span>
            <strong style="color:#8b5cf6;font-family:'JetBrains Mono',monospace;">N = {min_n_001}</strong>
          </div>
        </div>
        """, unsafe_allow_html=True)

        if not valid:
            st.markdown('<div class="eng-warn">⚠️ Pastikan S &gt; N dan A &lt; S</div>',
                        unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ██ KALKULATOR ENGSET
# ══════════════════════════════════════════════════════════════════════════════
elif active_page == "🧮  Kalkulator Engset":
    page_header("Rekayasa Trafik", "Kalkulator Engset",
                "Hitung probabilitas blocking dengan model finite source")

    # Rumus Engset — SVG yang sudah diperbaiki
    st.markdown(f"""
    <div class="formula-wrap">
      <span class="formula-tag">⚡ Rumus Engset — Finite Source Model</span>
      <div class="eq-container">
        {ENGSET_EQUATION_SVG}
      </div>
      <div class="formula-legend">
        <div class="fl-item"><span class="fl-sym">P</span> = Probabilitas Blocking</div>
        <div class="fl-item"><span class="fl-sym">N</span> = Jumlah Kanal / Server</div>
        <div class="fl-item"><span class="fl-sym">S</span> = Jumlah Source / Pengguna</div>
        <div class="fl-item"><span class="fl-sym">A</span> = Traffic Offered (Erlang)</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    # Input Parameter
    st.markdown("""
    <div style="font-size:0.72rem;color:#6366f1;font-weight:800;text-transform:uppercase;
         letter-spacing:0.12em;margin-bottom:1rem;">⚙️ Masukkan Parameter Sistem</div>
    """, unsafe_allow_html=True)

    col_s, col_n, col_a = st.columns(3, gap="large")
    with col_s:
        inp_S = st.number_input("S — Jumlah Source (Pengguna)", min_value=2, max_value=200,
                                 value=st.session_state["S_calc"], step=1)
    with col_n:
        inp_N = st.number_input("N — Jumlah Kanal (Server)", min_value=1, max_value=100,
                                 value=st.session_state["N_calc"], step=1)
    with col_a:
        inp_A = st.number_input("A — Traffic Offered (Erlang)", min_value=0.1,
                                 max_value=float(max(1, inp_S - 1)),
                                 value=min(st.session_state["A_calc"], float(inp_S - 2)),
                                 step=0.1, format="%.1f")

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    if st.button("🚀  Jalankan Kalkulasi", use_container_width=True):
        st.session_state["S_calc"] = inp_S
        st.session_state["N_calc"] = inp_N
        st.session_state["A_calc"] = inp_A
        st.session_state["kalkulasi_done"] = True
        st.rerun()

    st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)

    # Hasil
    if not valid:
        st.markdown('<div class="eng-warn">⚠️ Pastikan S lebih besar dari N dan A lebih kecil dari S.</div>',
                    unsafe_allow_html=True)
    else:
        col1, col2 = st.columns([1.2, 1], gap="large")

        with col1:
            st.markdown('<p class="sec-title">📊 Hasil Perhitungan</p>', unsafe_allow_html=True)
            rows = [
                ("📡","Probabilitas Blocking (P)", f"{P:.8f}",       "Probabilitas"),
                ("📈","Blocking Persen",            f"{P*100:.4f}%",  "Persentase"),
                ("🏆","Grade Of Service",           gos_text,         "Penilaian kualitas"),
                ("✅","Traffic Carried",            f"{carried:.4f} Erl","Terlayani"),
                ("❌","Traffic Lost",               f"{lost:.4f} Erl","Terblokir"),
                ("⚡","Utilisasi Kanal",            f"{util_pct:.2f}%","Per kanal"),
                ("📶","Traffic Intensity",          f"{A/N:.4f} Erl/ch","Per kanal"),
            ]
            for icon, label, val, unit in rows:
                st.markdown(f"""
                <div class="plan-card" style="padding:0.9rem 1.1rem;">
                  <div class="plan-icon-wrap plan-icon-blue"
                       style="width:38px;height:38px;border-radius:10px;font-size:1.1rem;">{icon}</div>
                  <div class="plan-info">
                    <p class="plan-name" style="font-size:0.85rem;">{label}</p>
                    <p class="plan-desc">{unit}</p>
                  </div>
                  <div class="plan-val" style="font-size:0.92rem;">{val}</div>
                </div>
                """, unsafe_allow_html=True)

        with col2:
            st.markdown('<p class="sec-title">🎯 Rekomendasi N Minimum</p>', unsafe_allow_html=True)
            targets = [0.10, 0.05, 0.02, 0.01, 0.005, 0.001]
            rec_rows = ""
            for t in targets:
                mn = find_min_N(S, A, t)
                ok = N >= (mn if mn else 9999)
                rec_rows += (f'<tr><td>{t*100:.1f}%</td>'
                             f'<td>N = {mn if mn else "&#8211;"}</td>'
                             f'<td>{"✅" if ok else "❌"}</td></tr>')
            st.markdown(f"""
            <div class="card" style="padding:1.2rem;">
              <table class="eng-table">
                <thead><tr><th>Target GoS</th><th>N Minimum</th><th>Status N={N}</th></tr></thead>
                <tbody>{rec_rows}</tbody>
              </table>
            </div>
            """, unsafe_allow_html=True)

            if P < 0.001:
                st.markdown(f'<div class="eng-ok">✅ Sangat baik — blocking hanya {P*100:.4f}%</div>',
                            unsafe_allow_html=True)
            elif P < 0.01:
                st.markdown(f'<div class="eng-ok">✅ Baik — blocking {P*100:.3f}%</div>',
                            unsafe_allow_html=True)
            elif P < 0.05:
                st.markdown(f'<div class="eng-warn">⚠️ Cukup — pertimbangkan tambah kanal</div>',
                            unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="eng-warn">🔴 Buruk — tambah kanal segera!</div>',
                            unsafe_allow_html=True)

            with st.expander("🔢 Lihat Langkah Perhitungan"):
                ratio = A / (S - A)
                st.markdown(f"""
**Langkah 1 — Hitung Rasio:**
```
A/(S-A) = {A:.2f} / ({S} - {A:.2f}) = {ratio:.6f}
```
**Langkah 2 — Hitung Pembilang:**
```
C(S-1, N) × (A/(S-A))^N
= C({S-1}, {N}) × {ratio:.6f}^{N}
```
**Langkah 3 — Hitung Penyebut:**
```
Σ[i=0..{N}] C({S-1}, i) × {ratio:.6f}^i
```
**Langkah 4 — Hasil Akhir:**
```
P = pembilang / penyebut
P = {P:.8f}
P = {P*100:.4f}%
```
                """)


# ══════════════════════════════════════════════════════════════════════════════
# ██ HITUNG TRAFFIC A
# ══════════════════════════════════════════════════════════════════════════════
elif active_page == "📐  Hitung Traffic A":
    page_header("Perhitungan Trafik", "Hitung Traffic Offered (A)",
                "Tentukan nilai A dari parameter jaringan yang diketahui")

    tab1, tab2, tab3 = st.tabs([
        "📞 Call Rate & Hold Time",
        "👥 Pengguna Aktif (BHT)",
        "🔁 Data Rate / Throughput"
    ])

    with tab1:
        st.markdown("""
        <div class="formula-wrap" style="margin-bottom:1.2rem;">
          <span class="formula-tag">Rumus Erlang</span>
          <div class="formula-body">
A = &#955; &#215; h<br><br>
&#955; = Call rate (panggilan/jam per pengguna)<br>
h = Rata-rata durasi panggilan (menit)
          </div>
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2, gap="large")
        with c1:
            call_rate  = st.number_input("λ — Call Rate (panggilan/jam per pengguna)",
                                         0.01, 1000.0, 3.0, 0.1, format="%.2f")
            hold_time  = st.number_input("h — Hold Time Rata-rata (menit)",
                                         0.1, 120.0, 2.0, 0.1, format="%.1f")
            n_users_t1 = st.number_input("Jumlah Pengguna Aktif (opsional untuk A total)",
                                         1, 10000, S)

        with c2:
            lam_s  = call_rate / 3600
            h_s    = hold_time * 60
            A_1    = lam_s * h_s
            A_tot  = A_1 * n_users_t1

            st.markdown(f"""
            <div class="card">
              <div style="font-size:0.85rem;font-weight:800;color:#1e1b4b;margin-bottom:1rem;">
                📊 Hasil Perhitungan</div>
              <div style="display:flex;justify-content:space-between;align-items:center;
                   padding:9px 0;border-bottom:1px solid #f0f4ff;">
                <span style="font-size:0.82rem;color:#9ca3af;">Traffic Per Pengguna</span>
                <span style="font-family:'JetBrains Mono';font-weight:700;color:#6366f1;">
                  {A_1:.6f} Erl</span>
              </div>
              <div style="display:flex;justify-content:space-between;align-items:center;
                   padding:9px 0;border-bottom:1px solid #f0f4ff;">
                <span style="font-size:0.82rem;color:#9ca3af;">&#955; (Konversi ke /detik)</span>
                <span style="font-family:'JetBrains Mono';font-weight:700;color:#1e1b4b;">
                  {lam_s:.6f} call/s</span>
              </div>
              <div style="display:flex;justify-content:space-between;align-items:center;
                   padding:9px 0;border-bottom:1px solid #f0f4ff;">
                <span style="font-size:0.82rem;color:#9ca3af;">h (Konversi ke detik)</span>
                <span style="font-family:'JetBrains Mono';font-weight:700;color:#1e1b4b;">
                  {h_s:.0f} detik</span>
              </div>
              <div style="margin-top:1rem;background:linear-gradient(135deg,#ede9fe,#e0e7ff);
                   border-radius:14px;padding:1.2rem;text-align:center;">
                <div style="font-size:0.7rem;color:#4c1d95;text-transform:uppercase;
                     letter-spacing:0.1em;margin-bottom:6px;font-weight:800;">
                  A Total ({n_users_t1} pengguna)</div>
                <div style="font-size:2.2rem;font-weight:900;color:#6366f1;
                     font-family:'JetBrains Mono';">{A_tot:.4f} Erl</div>
                <div style="font-size:0.78rem;color:#6d28d9;margin-top:6px;">
                  Masukkan ke parameter kalkulator sebagai nilai A</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            if 0 < A_tot < S and S > N:
                P2 = engset(S, N, A_tot)
                if P2:
                    g2, gc2 = gos_label(P2)
                    cls = "eng-ok" if P2 < 0.01 else "eng-warn"
                    st.markdown(f'<div class="{cls}"><strong>Hasil Engset</strong> dengan '
                                f'A={A_tot:.4f}, S={S}, N={N}:<br>'
                                f'P = {P2:.6f} · Blocking = {P2*100:.3f}% · GoS = {g2}</div>',
                                unsafe_allow_html=True)

    with tab2:
        st.markdown("""
        <div class="formula-wrap" style="margin-bottom:1.2rem;">
          <span class="formula-tag">Rumus BHT</span>
          <div class="formula-body">
A = U &#215; BHT<br><br>
U   = Jumlah pengguna aktif di jam sibuk<br>
BHT = Busy Hour Traffic per pengguna (Erlang)
          </div>
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2, gap="large")
        with c1:
            U_val  = st.number_input("U — Pengguna Aktif Jam Sibuk", 1, 10000, 50)
            BHT    = st.number_input("BHT — Busy Hour Traffic Per User (Erl)",
                                     0.001, 1.0, 0.1, 0.001, format="%.3f")

        with c2:
            A_t2 = U_val * BHT
            st.markdown(f"""
            <div class="card" style="text-align:center;padding:1.8rem;">
              <div style="font-size:0.8rem;color:#9ca3af;margin-bottom:8px;font-family:'JetBrains Mono';">
                A = {U_val} &#215; {BHT:.3f}</div>
              <div style="font-size:2.6rem;font-weight:900;color:#6366f1;
                   font-family:'JetBrains Mono';">{A_t2:.4f}</div>
              <div style="font-size:0.84rem;color:#9ca3af;margin-top:6px;font-weight:600;">Erlang</div>
            </div>
            """, unsafe_allow_html=True)

            if 0 < A_t2 < S and S > N:
                P3 = engset(S, N, A_t2)
                if P3:
                    g3, gc3 = gos_label(P3)
                    cls = "eng-ok" if P3 < 0.01 else "eng-warn"
                    st.markdown(f'<div class="{cls}">P = {P3:.6f} · Blocking = {P3*100:.3f}% · GoS = {g3}</div>',
                                unsafe_allow_html=True)

    with tab3:
        st.markdown("""
        <div class="formula-wrap" style="margin-bottom:1.2rem;">
          <span class="formula-tag">Rumus Data Rate</span>
          <div class="formula-body">
A = Data Rate (Mbps) / Kapasitas Per Kanal (Mbps)
          </div>
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2, gap="large")
        with c1:
            dr = st.number_input("Data Rate Total (Mbps)", 0.1, 100000.0, 100.0, 1.0)
            cc = st.number_input("Kapasitas Per Kanal (Mbps)", 0.1, 10000.0, 10.0, 0.1)

        with c2:
            A_t3 = dr / cc
            st.markdown(f"""
            <div class="card" style="text-align:center;padding:1.8rem;">
              <div style="font-size:0.8rem;color:#9ca3af;margin-bottom:8px;font-family:'JetBrains Mono';">
                A = {dr:.1f} / {cc:.1f}</div>
              <div style="font-size:2.6rem;font-weight:900;color:#6366f1;
                   font-family:'JetBrains Mono';">{A_t3:.4f}</div>
              <div style="font-size:0.84rem;color:#9ca3af;margin-top:6px;font-weight:600;">Erlang</div>
            </div>
            """, unsafe_allow_html=True)

            if 0 < A_t3 < S and S > N:
                P4 = engset(S, N, A_t3)
                if P4:
                    g4, gc4 = gos_label(P4)
                    cls = "eng-ok" if P4 < 0.01 else "eng-warn"
                    st.markdown(f'<div class="{cls}">P = {P4:.6f} · Blocking = {P4*100:.3f}% · GoS = {g4}</div>',
                                unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ██ ANALISIS DAN GRAFIK
# ══════════════════════════════════════════════════════════════════════════════
elif active_page == "📊  Analisis Dan Grafik":
    page_header("Visualisasi", "Analisis Dan Grafik",
                "Visualisasi perilaku sistem terhadap variasi parameter")

    if not valid:
        st.markdown('<div class="eng-warn">⚠️ Periksa parameter di kalkulator terlebih dahulu.</div>',
                    unsafe_allow_html=True)
    else:
        cg1, cg2 = st.columns(2, gap="large")

        with cg1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("##### 📈 Blocking Vs Jumlah Kanal (N)")
            max_n = min(S-1, 50)
            ns_   = list(range(1, max_n+1))
            ps_   = [(engset(S,n,A) or 0)*100 for n in ns_]

            fig1, ax1 = plt.subplots(figsize=(5.5, 3.8))
            fig1.patch.set_facecolor(BG); ax1.set_facecolor(BG)
            ax1.fill_between(ns_, ps_, alpha=0.15, color=INDIGO)
            ax1.plot(ns_, ps_, color=INDIGO, linewidth=2.5, zorder=3)
            ax1.scatter([N], [P*100], color=RED, s=100, zorder=5,
                        label=f'N={N}, P={P*100:.3f}%')
            ax1.axhline(1.0, color=AMBER, linestyle='--', linewidth=1.2, alpha=0.8)
            ax1.text(max_n*0.97, 1.05, 'GoS 1%', ha='right', fontsize=8, color=AMBER)
            ax1.axhline(0.1, color=TEAL, linestyle='--', linewidth=1.2, alpha=0.8)
            ax1.text(max_n*0.97, 0.15, 'GoS 0.1%', ha='right', fontsize=8, color=TEAL)
            ax1.set_xlabel('N — Jumlah Kanal', fontsize=9, color='#6b7280')
            ax1.set_ylabel('Blocking (%)', fontsize=9, color='#6b7280')
            ax1.set_title(f'S={S}, A={A:.1f} Erl', fontsize=9, color='#9ca3af')
            ax1.legend(fontsize=8.5)
            ax1.grid(True, linestyle='--', alpha=0.25)
            ax1.spines[['top','right']].set_visible(False)
            ax1.tick_params(colors='#9ca3af', labelsize=8)
            plt.tight_layout(pad=1.0)
            st.pyplot(fig1, use_container_width=True)
            plt.close(fig1)
            st.markdown('</div>', unsafe_allow_html=True)

        with cg2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("##### 📉 Blocking Vs Traffic Offered (A)")
            a_max_  = min(float(S-1), 30.0)
            av_     = np.linspace(0.1, a_max_, 300)
            pv_     = [(engset(S,N,float(a)) or 0)*100 for a in av_]

            fig2, ax2 = plt.subplots(figsize=(5.5, 3.8))
            fig2.patch.set_facecolor(BG); ax2.set_facecolor(BG)
            ax2.fill_between(av_, pv_, alpha=0.15, color=TEAL)
            ax2.plot(av_, pv_, color=TEAL, linewidth=2.5, zorder=3)
            ax2.scatter([A], [P*100], color=RED, s=100, zorder=5,
                        label=f'A={A:.1f}, P={P*100:.3f}%')
            ax2.axhline(1.0, color=AMBER, linestyle='--', linewidth=1.2, alpha=0.8)
            ax2.text(a_max_*0.97, 1.05, 'GoS 1%', ha='right', fontsize=8, color=AMBER)
            ax2.set_xlabel('A — Traffic Offered (Erlang)', fontsize=9, color='#6b7280')
            ax2.set_ylabel('Blocking (%)', fontsize=9, color='#6b7280')
            ax2.set_title(f'S={S}, N={N} Kanal', fontsize=9, color='#9ca3af')
            ax2.legend(fontsize=8.5)
            ax2.grid(True, linestyle='--', alpha=0.25)
            ax2.spines[['top','right']].set_visible(False)
            ax2.tick_params(colors='#9ca3af', labelsize=8)
            plt.tight_layout(pad=1.0)
            st.pyplot(fig2, use_container_width=True)
            plt.close(fig2)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("##### 🌐 Multi-Kurva: Blocking Vs N Untuk Berbagai Nilai A")
        palette = [INDIGO, TEAL, AMBER, RED, VIOLET, '#ec4899']
        a_list  = [round(A*m,2) for m in [0.5,0.75,1.0,1.25,1.5,2.0] if 0 < A*m < S][:6]
        max_n3  = min(S-1, 35)
        ns3_    = list(range(1, max_n3+1))

        fig3, ax3 = plt.subplots(figsize=(11, 4))
        fig3.patch.set_facecolor(BG); ax3.set_facecolor(BG)
        for idx, a_c in enumerate(a_list):
            ps3 = [(engset(S,n,a_c) or 0)*100 for n in ns3_]
            ax3.plot(ns3_, ps3, color=palette[idx%len(palette)],
                     linewidth=2.2, label=f'A={a_c:.1f} Erl')
        ax3.axvline(N, color='#9ca3af', linestyle=':', linewidth=2,
                    label=f'N Aktif = {N}')
        ax3.axhline(1.0, color=AMBER, linestyle='--', linewidth=1, alpha=0.6)
        ax3.set_xlabel('N — Jumlah Kanal', fontsize=9, color='#6b7280')
        ax3.set_ylabel('Blocking (%)', fontsize=9, color='#6b7280')
        ax3.set_title(f'Perbandingan Blocking Vs N Untuk Berbagai A (S={S})',
                      fontsize=10, color='#1e1b4b', fontweight='bold')
        ax3.legend(fontsize=8.5, ncol=min(len(a_list)+1, 4))
        ax3.grid(True, linestyle='--', alpha=0.25)
        ax3.spines[['top','right']].set_visible(False)
        ax3.tick_params(colors='#9ca3af', labelsize=8)
        plt.tight_layout(pad=1.0)
        st.pyplot(fig3, use_container_width=True)
        plt.close(fig3)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("##### 📋 Tabel Detail Blocking Vs N")
        rows_html = ""
        for n_i in range(1, min(S, N+15)):
            p_i = engset(S, n_i, A)
            if p_i is None: continue
            c_i = A*(1-p_i); l_i = A*p_i; u_i = (c_i/n_i)*100
            g_t, g_c = gos_label(p_i)
            active = 'class="active"' if n_i == N else ""
            rows_html += (f'<tr {active}>'
                          f'<td>{"&#9658; " if n_i==N else ""}{n_i}</td>'
                          f'<td>{p_i:.6f}</td><td>{p_i*100:.3f}%</td>'
                          f'<td>{c_i:.4f}</td><td>{l_i:.4f}</td>'
                          f'<td>{u_i:.1f}%</td>'
                          f'<td><span class="gos {g_c}">{g_t}</span></td></tr>')
        st.markdown(f"""
        <table class="eng-table">
          <thead>
            <tr><th>N</th><th>P Blocking</th><th>Persen</th>
                <th>Carried (Erl)</th><th>Lost (Erl)</th>
                <th>Utilisasi</th><th>GoS</th></tr>
          </thead>
          <tbody>{rows_html}</tbody>
        </table>
        <div class="eng-info" style="margin-top:10px;font-size:0.78rem;">
          🔵 Baris ungu = nilai N yang dipilih saat ini (N={N})</div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ██ EXPORT LAPORAN
# ══════════════════════════════════════════════════════════════════════════════
elif active_page == "📄  Export Laporan":
    page_header("Export", "Export Laporan PDF",
                "Generate laporan profesional hasil analisis Engset")

    if not valid:
        st.markdown('<div class="eng-warn">⚠️ Jalankan kalkulasi di menu Kalkulator Engset terlebih dahulu.</div>',
                    unsafe_allow_html=True)
    elif not PDF_OK:
        st.markdown('<div class="eng-warn">⚠️ Instal ReportLab: <code>pip install reportlab</code></div>',
                    unsafe_allow_html=True)
    else:
        c_prev, c_act = st.columns([1.5, 1], gap="large")

        with c_prev:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div style="font-size:0.92rem;font-weight:800;color:#1e1b4b;'
                        'margin-bottom:1.2rem;">📄 Preview Isi Laporan</div>',
                        unsafe_allow_html=True)
            items_prev = [
                ("📌","Judul",           "EngsetPro — Laporan Perhitungan Engset"),
                ("📅","Tanggal",         datetime.now().strftime('%d %B %Y, %H:%M')),
                ("🔢","Parameter",       f"S={S}, N={N}, A={A:.1f} Erl"),
                ("📡","P Blocking",      f"{P:.8f}"),
                ("📊","Blocking %",      f"{P*100:.4f}%"),
                ("🏆","GoS",             gos_text),
                ("✅","Traffic Carried", f"{carried:.4f} Erlang"),
                ("❌","Traffic Lost",    f"{lost:.4f} Erlang"),
                ("📈","Grafik",          "Blocking Vs N + Blocking Vs A"),
                ("📋","Tabel",           "Detail N Dari 1 Sampai N+10"),
            ]
            for icon, label, val in items_prev:
                st.markdown(f"""
                <div style="display:flex;justify-content:space-between;align-items:center;
                     padding:9px 0;border-bottom:1px solid rgba(99,102,241,0.06);">
                  <span style="font-size:0.82rem;color:#9ca3af;">{icon} {label}</span>
                  <span style="font-size:0.82rem;font-weight:700;color:#1e1b4b;
                       font-family:'JetBrains Mono',monospace;text-align:right;max-width:55%;">{val}</span>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with c_act:
            st.markdown("""
            <div class="card" style="text-align:center;padding:2.2rem 1.5rem;">
              <div style="font-size:3.5rem;margin-bottom:1rem;">📄</div>
              <div style="font-size:1.05rem;font-weight:800;color:#1e1b4b;margin-bottom:0.6rem;">
                Laporan PDF Profesional</div>
              <div style="font-size:0.84rem;color:#9ca3af;margin-bottom:1.5rem;line-height:1.7;">
                Berisi rumus, parameter, hasil perhitungan,<br>grafik analisis, dan tabel detail.
              </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("⬇️  Generate Dan Download PDF", use_container_width=True):
                with st.spinner("Membuat laporan PDF..."):
                    def cb(fig):
                        buf = io.BytesIO()
                        fig.savefig(buf, format='png', dpi=150, bbox_inches='tight',
                                    facecolor='white')
                        buf.seek(0); return buf.read()

                    max_n_ = min(S-1, 40)
                    ns__   = list(range(1, max_n_+1))
                    ps__   = [(engset(S,n,A) or 0)*100 for n in ns__]
                    f1, a1 = plt.subplots(figsize=(7, 3.5))
                    f1.patch.set_facecolor('white'); a1.set_facecolor('white')
                    a1.fill_between(ns__, ps__, alpha=0.08, color='#6366f1')
                    a1.plot(ns__, ps__, color='#6366f1', linewidth=2)
                    a1.scatter([N],[P*100], color='#ef4444', s=60, zorder=5)
                    a1.axhline(1.0, color='#f59e0b', linestyle='--', linewidth=1)
                    a1.set_xlabel('N (Jumlah Kanal)', fontsize=9)
                    a1.set_ylabel('Blocking (%)', fontsize=9)
                    a1.set_title(f'Blocking Vs N  |  S={S}, A={A:.1f} Erl', fontsize=10,
                                 fontweight='bold', color='#1e1b4b')
                    a1.grid(True, linestyle='--', alpha=0.25, color='#e0e7ff')
                    a1.spines[['top','right']].set_visible(False)
                    plt.tight_layout(); c1_bytes = cb(f1); plt.close(f1)

                    am_ = min(float(S-1), 25.0)
                    av_ = np.linspace(0.1, am_, 200)
                    pv_ = [(engset(S,N,float(a)) or 0)*100 for a in av_]
                    f2, a2 = plt.subplots(figsize=(7, 3.5))
                    f2.patch.set_facecolor('white'); a2.set_facecolor('white')
                    a2.fill_between(av_, pv_, alpha=0.08, color='#14b8a6')
                    a2.plot(av_, pv_, color='#14b8a6', linewidth=2)
                    a2.scatter([A],[P*100], color='#ef4444', s=60, zorder=5)
                    a2.axhline(1.0, color='#f59e0b', linestyle='--', linewidth=1)
                    a2.set_xlabel('A (Erlang)', fontsize=9)
                    a2.set_ylabel('Blocking (%)', fontsize=9)
                    a2.set_title(f'Blocking Vs A  |  S={S}, N={N}', fontsize=10,
                                 fontweight='bold', color='#1e1b4b')
                    a2.grid(True, linestyle='--', alpha=0.25, color='#e0e7ff')
                    a2.spines[['top','right']].set_visible(False)
                    plt.tight_layout(); c2_bytes = cb(f2); plt.close(f2)

                    buf_pdf = io.BytesIO()
                    doc = SimpleDocTemplate(buf_pdf, pagesize=A4,
                        leftMargin=2.5*cm, rightMargin=2.5*cm,
                        topMargin=2.5*cm, bottomMargin=2.5*cm)

                    BLACK    = colors.HexColor('#1e1b4b')
                    DARK     = colors.HexColor('#374151')
                    MID_GRAY = colors.HexColor('#6b7280')
                    LIGHT_GRAY = colors.HexColor('#f8f7ff')
                    BORDER   = colors.HexColor('#e0e7ff')
                    HDR_BG   = colors.HexColor('#6366f1')
                    ALT_ROW  = colors.HexColor('#f5f3ff')

                    T   = ParagraphStyle('T',  fontSize=22, textColor=BLACK,
                                         fontName='Helvetica-Bold', spaceAfter=2, leading=28)
                    Sub = ParagraphStyle('Su', fontSize=10, textColor=MID_GRAY,
                                         spaceAfter=16, leading=14)
                    H2  = ParagraphStyle('H2', fontSize=13, textColor=DARK,
                                         fontName='Helvetica-Bold', spaceBefore=16,
                                         spaceAfter=6, leading=18)
                    B   = ParagraphStyle('B',  fontSize=9.5, textColor=MID_GRAY,
                                         leading=14, spaceAfter=4)
                    M   = ParagraphStyle('M',  fontSize=9, fontName='Courier',
                                         textColor=DARK, backColor=LIGHT_GRAY,
                                         leftIndent=12, rightIndent=12,
                                         spaceBefore=6, spaceAfter=6, leading=16,
                                         borderPadding=8)
                    FC  = ParagraphStyle('FC', fontSize=8,
                                         textColor=colors.HexColor('#9ca3af'),
                                         alignment=TA_CENTER)

                    el = []
                    el.append(Paragraph("EngsetPro", T))
                    el.append(Paragraph(
                        f"Laporan Analisis Engset &nbsp;|&nbsp; {datetime.now().strftime('%d %B %Y, %H:%M')}", Sub))
                    el.append(HRFlowable(width="100%", thickness=1.5,
                                          color=HDR_BG, spaceAfter=16))

                    el.append(Paragraph("1. Rumus Engset", H2))
                    el.append(Paragraph(
                        "Model Engset digunakan untuk menghitung probabilitas blocking pada "
                        "sistem telekomunikasi dengan jumlah sumber (source) terbatas.", B))
                    el.append(Paragraph(
                        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                        "C(S-1, N) x (A/(S-A))^N<br/>"
                        "P = ─────────────────────────────────────<br/>"
                        "&nbsp;&nbsp;&nbsp;&nbsp;N<br/>"
                        "&nbsp;&nbsp;&nbsp;&#931;&nbsp; C(S-1, i) x (A/(S-A))^i<br/>"
                        "&nbsp;&nbsp;&nbsp;i=0", M))
                    el.append(Paragraph(
                        "Keterangan: &nbsp;<b>P</b> = Probabilitas Blocking &nbsp;|&nbsp; "
                        "<b>S</b> = Jumlah Source &nbsp;|&nbsp; "
                        "<b>N</b> = Jumlah Kanal &nbsp;|&nbsp; "
                        "<b>A</b> = Traffic Offered (Erlang)", B))
                    el.append(Spacer(1, 8))

                    el.append(Paragraph("2. Parameter Input", H2))
                    pd2 = [["Parameter","Simbol","Nilai","Satuan"],
                            ["Jumlah Source","S",str(S),"Pengguna"],
                            ["Jumlah Kanal","N",str(N),"Kanal"],
                            ["Traffic Offered","A",f"{A:.1f}","Erlang"]]
                    pt = Table(pd2, colWidths=[6*cm, 2.5*cm, 3*cm, 3.5*cm])
                    pt.setStyle(TableStyle([
                        ('BACKGROUND',(0,0),(-1,0), HDR_BG),
                        ('TEXTCOLOR',(0,0),(-1,0), colors.white),
                        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
                        ('FONTNAME',(0,1),(-1,-1),'Helvetica'),
                        ('FONTSIZE',(0,0),(-1,-1),9),
                        ('ALIGN',(0,0),(-1,-1),'CENTER'),
                        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, ALT_ROW]),
                        ('GRID',(0,0),(-1,-1),0.5, BORDER),
                        ('TOPPADDING',(0,0),(-1,-1),7),
                        ('BOTTOMPADDING',(0,0),(-1,-1),7),
                        ('LEFTPADDING',(0,0),(-1,-1),10),
                        ('RIGHTPADDING',(0,0),(-1,-1),10),
                    ]))
                    el.append(pt)
                    el.append(Spacer(1, 12))

                    el.append(Paragraph("3. Hasil Perhitungan", H2))
                    rd2 = [["Metrik","Nilai","Keterangan"],
                            ["Probabilitas Blocking (P)",f"{P:.8f}","Nilai probabilitas blocking"],
                            ["Blocking (%)",f"{P*100:.4f}%","Persentase trafik terblokir"],
                            ["Grade Of Service", gos_text,"Kualitas layanan sistem"],
                            ["Traffic Carried",f"{carried:.4f} Erl","Trafik yang berhasil dilayani"],
                            ["Traffic Lost",f"{lost:.4f} Erl","Trafik yang terblokir"],
                            ["Utilisasi Kanal",f"{util_pct:.2f}%","Utilisasi rata-rata per kanal"]]
                    rt = Table(rd2, colWidths=[5.5*cm, 3.5*cm, 6*cm])
                    rt.setStyle(TableStyle([
                        ('BACKGROUND',(0,0),(-1,0), HDR_BG),
                        ('TEXTCOLOR',(0,0),(-1,0), colors.white),
                        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
                        ('FONTNAME',(0,1),(-1,-1),'Helvetica'),
                        ('FONTSIZE',(0,0),(-1,-1),9),
                        ('ALIGN',(1,0),(1,-1),'CENTER'),
                        ('ALIGN',(0,0),(0,-1),'LEFT'),
                        ('ALIGN',(2,0),(2,-1),'LEFT'),
                        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, ALT_ROW]),
                        ('GRID',(0,0),(-1,-1),0.5, BORDER),
                        ('TOPPADDING',(0,0),(-1,-1),7),
                        ('BOTTOMPADDING',(0,0),(-1,-1),7),
                        ('LEFTPADDING',(0,0),(-1,-1),10),
                        ('RIGHTPADDING',(0,0),(-1,-1),10),
                    ]))
                    el.append(rt)
                    el.append(Spacer(1, 16))

                    el.append(Paragraph("4. Grafik Analisis", H2))
                    el.append(Paragraph(
                        f"Grafik berikut menunjukkan pengaruh perubahan jumlah kanal (N) "
                        f"dan traffic offered (A) terhadap probabilitas blocking pada sistem "
                        f"dengan S={S} source.", B))
                    el.append(Spacer(1, 6))
                    el.append(RLImage(io.BytesIO(c1_bytes), width=15*cm, height=7*cm))
                    el.append(Spacer(1, 8))
                    el.append(RLImage(io.BytesIO(c2_bytes), width=15*cm, height=7*cm))
                    el.append(Spacer(1, 16))

                    el.append(HRFlowable(width="100%", thickness=0.5,
                                          color=BORDER, spaceAfter=8))
                    el.append(Paragraph(
                        f"EngsetPro v2.0 &nbsp;·&nbsp; {datetime.now().strftime('%d %B %Y')} "
                        f"&nbsp;·&nbsp; Rekayasa Trafik &nbsp;·&nbsp; Model Engset Finite Source", FC))

                    doc.build(el)
                    buf_pdf.seek(0)

                st.download_button(
                    "📥  Klik Untuk Download PDF",
                    data=buf_pdf,
                    file_name=f"engset_S{S}_N{N}_A{A:.1f}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )
                st.markdown('<div class="eng-ok">✅ PDF siap! Klik tombol di atas untuk mengunduh.</div>',
                            unsafe_allow_html=True)


# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;color:#c4b5fd;font-size:0.78rem;padding:2.5rem 0 1.5rem;
     font-weight:500;letter-spacing:0.04em;">
  EngsetPro v2.0 &nbsp;·&nbsp; Kalkulator Rekayasa Trafik Engset &nbsp;·&nbsp;
  Metode: Log-space Arithmetic
</div>
""", unsafe_allow_html=True)
