import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
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
# GLOBAL CSS — Clean, modern, UNPIX-inspired blue palette
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

.stApp {
    background: #F0F4FF;
    min-height: 100vh;
}

#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
.stDeployButton { display: none !important; }

.main .block-container {
    padding-top: 2.5rem !important;
    padding-bottom: 2rem !important;
    max-width: 1180px !important;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1A3FD8 0%, #1660E8 50%, #0E9FD8 100%) !important;
    border-right: none !important;
    box-shadow: 4px 0 32px rgba(22,96,232,0.22);
}
[data-testid="stSidebar"] > div:first-child { padding-top: 0 !important; }
[data-testid="stSidebar"] * { color: rgba(255,255,255,0.92) !important; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.12) !important; }
[data-testid="stSidebar"] .stRadio > div { gap: 4px !important; }
[data-testid="stSidebar"] .stRadio label {
    background: rgba(255,255,255,0.08) !important;
    border-radius: 12px !important;
    padding: 11px 14px !important;
    cursor: pointer !important;
    transition: all 0.18s ease !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    font-size: 0.875rem !important;
    font-weight: 500 !important;
    color: rgba(255,255,255,0.72) !important;
    width: 100%;
    margin: 2px 0;
    display: flex !important;
    align-items: center !important;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(255,255,255,0.16) !important;
    color: #fff !important;
    border-color: rgba(255,255,255,0.14) !important;
}
[data-testid="stSidebar"] .stRadio [aria-checked="true"] + label,
[data-testid="stSidebar"] .stRadio label:has(input:checked) {
    background: rgba(255,255,255,0.22) !important;
    color: #fff !important;
    border-color: rgba(255,255,255,0.28) !important;
    font-weight: 600 !important;
}
[data-testid="stSidebar"] .stRadio [data-baseweb="radio"] > div:first-child {
    display: none !important;
}

/* ── CARD ── */
.card {
    background: #FFFFFF;
    border-radius: 20px;
    padding: 1.4rem 1.6rem;
    box-shadow: 0 2px 16px rgba(22,96,232,0.07), 0 1px 3px rgba(0,0,0,0.04);
    border: 1px solid rgba(22,96,232,0.06);
    margin-bottom: 1rem;
    transition: box-shadow 0.18s, transform 0.18s;
}
.card:hover {
    box-shadow: 0 6px 28px rgba(22,96,232,0.12);
    transform: translateY(-1px);
}

/* ── HERO ── */
.hero-card {
    background: linear-gradient(135deg, #1548E0 0%, #1770F0 50%, #0EAAE0 100%);
    border-radius: 24px;
    padding: 2.2rem 2.2rem 2rem;
    color: white;
    margin-bottom: 1.2rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 12px 48px rgba(22,96,232,0.32);
}
.hero-card::before {
    content:""; position:absolute; top:-100px; right:-70px;
    width:340px; height:340px; border-radius:50%;
    background: radial-gradient(circle, rgba(255,255,255,0.09) 0%, transparent 65%);
    pointer-events: none;
}
.hero-card::after {
    content:""; position:absolute; bottom:-60px; left:3%;
    width:220px; height:220px; border-radius:50%;
    background: radial-gradient(circle, rgba(14,170,224,0.22) 0%, transparent 65%);
    pointer-events: none;
}

/* ── RESULT CHIPS ── */
.chip-grid {
    display: grid; grid-template-columns: 1fr 1fr 1fr;
    gap: 10px; margin-bottom: 1.1rem;
}
.chip {
    background: #FFFFFF;
    border-radius: 16px; padding: 1.1rem 0.8rem;
    text-align: center;
    box-shadow: 0 2px 14px rgba(22,96,232,0.08);
    border: 1px solid rgba(22,96,232,0.06);
    transition: transform 0.15s, box-shadow 0.15s;
}
.chip:hover { transform: translateY(-2px); box-shadow: 0 6px 22px rgba(22,96,232,0.13); }
.chip-icon { font-size: 1.4rem; margin-bottom: 5px; color: #1660E8; font-weight: 300; line-height: 1; }
.chip-val  { font-size: 1rem; font-weight: 700; color: #0D1E50; font-family: 'JetBrains Mono', monospace; }
.chip-lbl  { font-size: 0.6rem; color: #9BAAD0; text-transform: uppercase; letter-spacing: 0.08em; margin-top: 3px; font-weight: 600; }

/* ── LIST ROW CARDS ── */
.plan-card {
    background: #FFFFFF;
    border-radius: 14px; padding: 0.85rem 1.1rem;
    display: flex; align-items: center; gap: 12px; margin-bottom: 8px;
    box-shadow: 0 1px 10px rgba(22,96,232,0.06);
    border: 1px solid rgba(22,96,232,0.05);
    transition: all 0.15s;
}
.plan-card:hover {
    box-shadow: 0 4px 20px rgba(22,96,232,0.11);
    transform: translateX(2px);
}
.plan-icon-wrap {
    width: 38px; height: 38px; border-radius: 11px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem; flex-shrink: 0;
    color: #1660E8; font-weight: 400;
}
.plan-icon-blue   { background: #EBF0FE; }
.plan-icon-green  { background: #E4F9EF; }
.plan-icon-amber  { background: #FEF6DF; }
.plan-icon-red    { background: #FEEDED; }
.plan-icon-teal   { background: #E0F6FE; }
.plan-name { font-size: 0.84rem; font-weight: 600; color: #0D1E50; margin: 0; }
.plan-desc { font-size: 0.71rem; color: #9BAAD0; margin: 1px 0 0; font-weight: 400; }
.plan-val  { font-size: 0.92rem; font-weight: 700; color: #1660E8; font-family: 'JetBrains Mono', monospace; margin-left: auto; }

/* ── GoS BADGE ── */
.gos { display: inline-block; padding: 4px 16px; border-radius: 100px; font-size: 0.74rem; font-weight: 600; letter-spacing: 0.02em; }
.gos-great { background: #D6F7EA; color: #0A7040; }
.gos-good  { background: #E2F9EE; color: #0C6838; }
.gos-ok    { background: #FEF5DC; color: #865C0A; }
.gos-bad   { background: #FEECEC; color: #9C2020; }

/* ── FORMULA WRAP ── */
.formula-wrap {
    background: #FFFFFF;
    border-radius: 20px;
    padding: 1.6rem 1.9rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 2px 16px rgba(22,96,232,0.07);
    border: 1px solid rgba(22,96,232,0.06);
}
.formula-tag {
    display: inline-block;
    background: linear-gradient(135deg, #1660E8, #0EAAE0);
    color: #fff;
    font-size: 0.66rem; font-weight: 700; letter-spacing: 0.1em;
    text-transform: uppercase; padding: 4px 14px; border-radius: 100px; margin-bottom: 1.2rem;
}
.formula-body {
    font-family: 'JetBrains Mono', monospace; font-size: 0.84rem; color: #0D1E50;
    line-height: 2;
    background: #F4F7FF;
    border-radius: 12px;
    padding: 1.1rem 1.4rem;
}
.formula-legend { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 1rem; }
.fl-item { font-size: 0.79rem; color: #3A4F90; display: flex; align-items: baseline; gap: 8px; }
.fl-sym  { font-family: 'JetBrains Mono', monospace; font-weight: 700; color: #1660E8; min-width: 18px; }

/* ── EQUATION ── */
.eq-container {
    display: flex; justify-content: center; align-items: center;
    padding: 1.4rem 1rem; margin: 0.4rem 0;
    background: #F4F7FF;
    border-radius: 14px;
}

/* ── SECTION TITLE ── */
.sec-title {
    font-size: 0.68rem; font-weight: 700; color: #9BAAD0;
    text-transform: uppercase; letter-spacing: 0.1em;
    margin: 0 0 0.7rem;
}

/* ── ALERT BANNERS ── */
.eng-warn {
    background: #FEF7DF; border: 1px solid #F5CC50;
    border-radius: 12px; padding: 0.8rem 1rem;
    color: #6E4A0C; font-size: 0.83rem; margin-bottom: 0.85rem; font-weight: 500;
}
.eng-info {
    background: #EEF3FF; border: 1px solid #B3C8FF;
    border-radius: 12px; padding: 0.8rem 1rem;
    color: #1A3C90; font-size: 0.83rem; margin-bottom: 0.85rem; font-weight: 500;
}
.eng-ok {
    background: #E2F9EE; border: 1px solid #72DCA8;
    border-radius: 12px; padding: 0.8rem 1rem;
    color: #0A5830; font-size: 0.83rem; margin-bottom: 0.85rem; font-weight: 500;
}

/* ── TABLE ── */
.eng-table { width: 100%; border-collapse: collapse; font-size: 0.82rem; border-radius: 14px; overflow: hidden; }
.eng-table th {
    background: linear-gradient(135deg, #1548E0, #1770F0);
    color: rgba(255,255,255,0.95); font-size: 0.67rem;
    text-transform: uppercase; letter-spacing: 0.08em;
    padding: 11px 14px; text-align: left; font-weight: 600;
}
.eng-table td {
    padding: 9px 14px; border-bottom: 1px solid #EEF2FF;
    color: #3A4F90; font-family: 'JetBrains Mono', monospace; font-size: 0.78rem;
}
.eng-table tr:last-child td { border-bottom: none; }
.eng-table tr:hover td { background: #F6F8FF; }
.eng-table tr.active td { background: #EEF3FF; font-weight: 700; color: #1660E8; }

/* ── BUTTONS ── */
.stButton > button {
    background: linear-gradient(135deg, #1660E8, #0EAAE0) !important;
    color: #fff !important; border: none !important; border-radius: 12px !important;
    padding: 0.65rem 2rem !important; font-weight: 600 !important;
    font-size: 0.88rem !important;
    box-shadow: 0 4px 18px rgba(22,96,232,0.28) !important;
    transition: all 0.15s !important;
    letter-spacing: 0.01em !important;
    font-family: 'Inter', sans-serif !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #1248C8, #0A98C8) !important;
    box-shadow: 0 8px 26px rgba(22,96,232,0.38) !important;
    transform: translateY(-1px) !important;
}

/* ── PROGRESS ── */
.progress-wrap {
    background: #E6ECFF; border-radius: 100px; height: 6px; margin: 8px 0; overflow: hidden;
}
.progress-fill {
    height: 100%; border-radius: 100px;
    background: linear-gradient(90deg, #1660E8, #0EAAE0);
    transition: width 0.4s ease;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(22,96,232,0.06); border-radius: 14px;
    padding: 4px; gap: 2px; border: none;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px; font-weight: 600; font-size: 0.85rem;
    color: #9BAAD0; padding: 8px 20px; transition: all 0.15s;
    font-family: 'Inter', sans-serif;
}
.stTabs [aria-selected="true"] {
    background: #fff !important; color: #1660E8 !important;
    box-shadow: 0 2px 10px rgba(22,96,232,0.12) !important;
}

/* ── INPUTS ── */
[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input {
    border-radius: 10px !important;
    border: 1.5px solid #E2E8FF !important;
    background: #F6F8FF !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 500 !important;
    color: #0D1E50 !important;
    transition: border-color 0.15s !important;
    font-size: 0.9rem !important;
}
[data-testid="stNumberInput"] input:focus,
[data-testid="stTextInput"] input:focus {
    border-color: #1660E8 !important;
    box-shadow: 0 0 0 3px rgba(22,96,232,0.1) !important;
    background: #fff !important;
}
label {
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    color: #4A5680 !important;
}

/* ── PAGE HEADER ── */
.ph-tag {
    font-size: 0.67rem; color: #1660E8; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.14em; margin-bottom: 4px;
}
.ph-title {
    font-size: 1.75rem; font-weight: 800; color: #0D1E50;
    margin: 0; letter-spacing: -0.02em; line-height: 1.15;
}
.ph-sub {
    color: #9BAAD0; margin: 5px 0 0; font-size: 0.88rem; font-weight: 400;
}

/* ── RESPONSIVE ── */
@media (max-width: 768px) {
    .main .block-container {
        padding-left: 0.75rem !important;
        padding-right: 0.75rem !important;
        padding-top: 1.6rem !important;
        max-width: 100% !important;
    }
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #F0F4FF; }
::-webkit-scrollbar-thumb { background: #B8CAFF; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #1660E8; }

/* ── DELETE BUTTON ── */
[data-testid="stButton"] button[kind="secondary"] {
    background: transparent !important;
    color: #D0D8F0 !important;
    border: 1px solid #E2E8FF !important;
    border-radius: 10px !important;
    padding: 0.5rem 0.7rem !important;
    font-size: 0.8rem !important;
    box-shadow: none !important;
    font-weight: 500 !important;
}
[data-testid="stButton"] button[kind="secondary"]:hover {
    background: #FEEDED !important;
    color: #B02020 !important;
    border-color: #F5C0C0 !important;
    transform: none !important;
    box-shadow: none !important;
}
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# MENU + SESSION STATE — semua inisialisasi SEBELUM sidebar dirender
# ═══════════════════════════════════════════════════════════════════════════════
MENU_OPTIONS = [
    "Dashboard",
    "Kalkulator Engset",
    "Hitung Traffic A",
    "Analisis Dan Grafik",
    "Export Laporan"
]

# SVG icons untuk menu — profesional & konsisten
MENU_ICONS_SVG = {
    "Dashboard": (
        '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" '
        'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/>'
        '<rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/>'
        '</svg>'
    ),
    "Kalkulator Engset": (
        '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" '
        'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<rect x="4" y="2" width="16" height="20" rx="2"/>'
        '<line x1="8" y1="6" x2="16" y2="6"/>'
        '<line x1="8" y1="10" x2="10" y2="10"/><line x1="14" y1="10" x2="16" y2="10"/>'
        '<line x1="8" y1="14" x2="10" y2="14"/><line x1="14" y1="14" x2="16" y2="14"/>'
        '<line x1="8" y1="18" x2="10" y2="18"/><line x1="14" y1="18" x2="16" y2="18"/>'
        '</svg>'
    ),
    "Hitung Traffic A": (
        '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" '
        'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>'
        '</svg>'
    ),
    "Analisis Dan Grafik": (
        '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" '
        'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<line x1="18" y1="20" x2="18" y2="10"/>'
        '<line x1="12" y1="20" x2="12" y2="4"/>'
        '<line x1="6" y1="20" x2="6" y2="14"/>'
        '<line x1="2" y1="20" x2="22" y2="20"/>'
        '</svg>'
    ),
    "Export Laporan": (
        '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" '
        'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>'
        '<polyline points="7 10 12 15 17 10"/>'
        '<line x1="12" y1="15" x2="12" y2="3"/>'
        '</svg>'
    ),
}

# Session state — HARUS sebelum sidebar
if "active_page"     not in st.session_state: st.session_state["active_page"]     = MENU_OPTIONS[0]
if "S_calc"          not in st.session_state: st.session_state["S_calc"]          = 20
if "N_calc"          not in st.session_state: st.session_state["N_calc"]          = 5
if "A_calc"          not in st.session_state: st.session_state["A_calc"]          = 7.0
if "kalkulasi_done"  not in st.session_state: st.session_state["kalkulasi_done"]  = False
if "history"         not in st.session_state: st.session_state["history"]         = []


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
# ENGSET EQUATION SVG
# ═══════════════════════════════════════════════════════════════════════════════
ENGSET_SVG = (
    '<svg viewBox="0 0 700 310" xmlns="http://www.w3.org/2000/svg" '
    'style="max-width:680px;width:100%;display:block;margin:0 auto;">'

    '<defs><style>'
    '.es  { font-family: Georgia, "Times New Roman", serif; }'
    '.ec  { fill: #1660E8; }'
    '.ed  { fill: #0D1E50; }'
    '.ef  { fill: #0D1E50; font-family: Georgia, serif; font-style: italic; }'
    '.eg  { fill: #546e7a; font-family: sans-serif; font-size: 12px; }'
    '.esm { font-family: Georgia, "Times New Roman", serif; fill: #0D1E50; }'
    '</style></defs>'

    '<text x="28" y="148" class="es ed" font-size="30" font-style="italic" font-weight="bold">P</text>'
    '<text x="58" y="148" class="es ed" font-size="28">=</text>'
    '<line x1="88" y1="150" x2="670" y2="150" stroke="#1660E8" stroke-width="2.6"/>'

    '<text x="200" y="68" class="es ed" font-size="15" text-anchor="middle">(S&#8722;1)!</text>'
    '<line x1="140" y1="76" x2="260" y2="76" stroke="#0D1E50" stroke-width="1.5"/>'
    '<text x="200" y="100" class="es ed" font-size="14" text-anchor="middle">N! (S&#8722;1&#8722;N)!</text>'
    '<text x="282" y="88" class="es" fill="#90a4ae" font-size="22">&#215;</text>'

    '<text x="308" y="98" class="es ed" font-size="44" font-weight="200">(</text>'
    '<text x="358" y="68" class="es ed" font-size="17" text-anchor="middle">A</text>'
    '<line x1="340" y1="74" x2="376" y2="74" stroke="#0D1E50" stroke-width="1.5"/>'
    '<text x="358" y="96" class="es ed" font-size="14" text-anchor="middle">S&#8722;A</text>'
    '<text x="382" y="98" class="es ed" font-size="44" font-weight="200">)</text>'
    '<text x="416" y="50" class="es ec" font-size="17" font-style="italic" font-weight="bold">N</text>'

    '<text x="109" y="172" class="es ec" font-size="13" font-weight="bold" text-anchor="middle">N</text>'
    '<text x="100" y="200" class="es ec" font-size="42">&#931;</text>'
    '<text x="109" y="225" class="es ec" font-size="13" font-weight="bold" text-anchor="middle">i&#61;0</text>'

    '<text x="250" y="185" class="es ed" font-size="15" text-anchor="middle">(S&#8722;1)!</text>'
    '<line x1="188" y1="193" x2="312" y2="193" stroke="#0D1E50" stroke-width="1.5"/>'
    '<text x="250" y="217" class="es ed" font-size="14" text-anchor="middle">i! (S&#8722;1&#8722;i)!</text>'
    '<text x="332" y="206" class="es" fill="#90a4ae" font-size="22">&#215;</text>'

    '<text x="358" y="215" class="es ed" font-size="44" font-weight="200">(</text>'
    '<text x="408" y="185" class="es ed" font-size="17" text-anchor="middle">A</text>'
    '<line x1="390" y1="191" x2="426" y2="191" stroke="#0D1E50" stroke-width="1.5"/>'
    '<text x="408" y="213" class="es ed" font-size="14" text-anchor="middle">S&#8722;A</text>'
    '<text x="432" y="215" class="es ed" font-size="44" font-weight="200">)</text>'
    '<text x="468" y="162" class="es ec" font-size="17" font-style="italic" font-weight="bold">i</text>'

    '<line x1="20" y1="256" x2="680" y2="256" stroke="#DDE5FF" stroke-width="1.2"/>'

    '<text x="28" y="273" class="es ed" font-size="13" font-style="italic">P</text>'
    '<text x="42" y="273" class="eg">= Probabilitas blocking (blocking probability)</text>'
    '<text x="28" y="291" class="es ed" font-size="13" font-style="italic">S</text>'
    '<text x="42" y="291" class="eg">= Jumlah source / pengguna</text>'
    '<text x="370" y="273" class="es ed" font-size="13" font-style="italic">N</text>'
    '<text x="384" y="273" class="eg">= Jumlah server / kanal</text>'
    '<text x="370" y="291" class="es ed" font-size="13" font-style="italic">A</text>'
    '<text x="384" y="291" class="eg">= Traffic offered to group</text>'

    '</svg>'
)


# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    # Brand header
    st.markdown(
        '<div style="background:rgba(255,255,255,0.12);border-radius:18px;padding:1.4rem 1.2rem 1.2rem;'
        'margin-bottom:1.6rem;text-align:center;border:1px solid rgba(255,255,255,0.18);">'
        '<div style="margin-bottom:8px;">'
        '<svg xmlns="http://www.w3.org/2000/svg" width="34" height="34" viewBox="0 0 24 24" '
        'fill="none" stroke="rgba(255,255,255,0.90)" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">'
        '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>'
        '</svg>'
        '</div>'
        '<div style="font-size:1.35rem;font-weight:800;color:#fff;letter-spacing:-0.01em;'
        'font-family:Inter,sans-serif;line-height:1;">EngsetPro</div>'
        '<div style="font-size:0.62rem;color:rgba(255,255,255,0.42);letter-spacing:0.14em;'
        'margin-top:5px;text-transform:uppercase;font-weight:600;">Rekayasa Trafik v2.0</div>'
        '</div>',
        unsafe_allow_html=True
    )

    # Navigation label
    st.markdown(
        '<div style="font-size:0.62rem;font-weight:700;color:rgba(255,255,255,0.35);'
        'text-transform:uppercase;letter-spacing:0.12em;margin-bottom:0.5rem;padding:0 4px;">Navigasi</div>',
        unsafe_allow_html=True
    )

    # Menu items sebagai HTML buttons via radio trick
    current_idx = MENU_OPTIONS.index(st.session_state["active_page"])

    # Buat label dengan SVG icon inline
    menu_labels_display = []
    for m in MENU_OPTIONS:
        svg = MENU_ICONS_SVG[m]
        menu_labels_display.append(f"{m}")  # radio label teks saja

    selected = st.radio(
        "nav",
        MENU_OPTIONS,
        index=current_idx,
        label_visibility="collapsed",
        format_func=lambda x: x,
    )
    if selected != st.session_state["active_page"]:
        st.session_state["active_page"] = selected
        st.rerun()

    # Inject CSS untuk icon di tiap radio label via JS workaround
    icons_js = ""
    for i, m in enumerate(MENU_OPTIONS):
        svg_b64 = MENU_ICONS_SVG[m]
        icons_js += f"""
        labels[{i}].innerHTML = `<span style="display:flex;align-items:center;gap:10px;">
            <span style="opacity:0.75;flex-shrink:0;">{svg_b64}</span>
            <span style="font-size:0.875rem;font-weight:500;">{m}</span>
        </span>`;
        """

    st.markdown(
        f"""<script>
        (function inject() {{
            const radios = window.parent.document.querySelectorAll('[data-testid="stSidebar"] [data-testid="stRadio"] label');
            if (radios.length < {len(MENU_OPTIONS)}) {{ setTimeout(inject, 80); return; }}
            const labels = Array.from(radios);
            {icons_js}
        }})();
        </script>""",
        unsafe_allow_html=True,
    )

    st.markdown("<hr>", unsafe_allow_html=True)

    # Parameter Aktif — hanya muncul jika kalkulasi sudah dijalankan
    if st.session_state.get("kalkulasi_done", False):
        s_disp = st.session_state.get('S_calc', 20)
        n_disp = st.session_state.get('N_calc', 5)
        a_disp = st.session_state.get('A_calc', 7.0)
        hist_count = len(st.session_state.get("history", []))
        st.markdown(
            '<div style="background:rgba(255,255,255,0.09);border-radius:14px;padding:0.9rem 1rem;'
            'border:1px solid rgba(255,255,255,0.1);">'
            '<div style="font-size:0.6rem;color:rgba(255,255,255,0.38);text-transform:uppercase;'
            'letter-spacing:0.1em;margin-bottom:9px;font-weight:700;display:flex;align-items:center;gap:6px;">'
            '<svg xmlns="http://www.w3.org/2000/svg" width="11" height="11" viewBox="0 0 24 24" '
            'fill="none" stroke="rgba(255,255,255,0.4)" stroke-width="2.2">'
            '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>'
            '</svg> Parameter Aktif</div>'
            '<div style="font-size:0.82rem;color:rgba(255,255,255,0.82);line-height:2.2;font-family:\'JetBrains Mono\',monospace;">'
            f'S = <strong style="color:#A8CCFF;">{s_disp}</strong>&nbsp;&nbsp;pengguna<br>'
            f'N = <strong style="color:#A8CCFF;">{n_disp}</strong>&nbsp;&nbsp;kanal<br>'
            f'A = <strong style="color:#A8CCFF;">{a_disp:.1f}</strong>&nbsp;&nbsp;Erlang'
            '</div>'
            f'<div style="margin-top:9px;padding-top:9px;border-top:1px solid rgba(255,255,255,0.1);'
            f'font-size:0.7rem;color:rgba(255,255,255,0.42);">'
            f'<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10" viewBox="0 0 24 24" '
            f'fill="none" stroke="rgba(255,255,255,0.35)" stroke-width="2.2">'
            f'<polyline points="9 11 12 14 22 4"/>'
            f'<path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>'
            f'</svg> {hist_count} histori tersimpan'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )

    st.markdown(
        '<div style="margin-top:2rem;padding-top:1rem;text-align:center;'
        'font-size:0.66rem;color:rgba(255,255,255,0.16);line-height:2;">'
        'EngsetPro v2.0<br>Metode Log-space Arithmetic</div>',
        unsafe_allow_html=True
    )


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
gos_text, gos_cls = gos_label(P) if P is not None else ("N/A", "gos-ok")
min_n_1   = find_min_N(S, A, 0.01)  if valid else "N/A"
min_n_001 = find_min_N(S, A, 0.001) if valid else "N/A"

BLUE  = '#1660E8'
TEAL  = '#0EAAE0'
GREEN = '#0A7040'
AMBER = '#F59E0B'
RED   = '#EF4444'
BG    = '#F0F4FF'

kalkulasi_done = st.session_state.get("kalkulasi_done", False)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE HEADER
# ═══════════════════════════════════════════════════════════════════════════════
def page_header(tag, title, sub):
    st.markdown(
        f'<div style="margin-bottom:1.6rem;">'
        f'<div class="ph-tag">{tag}</div>'
        f'<h1 class="ph-title">{title}</h1>'
        f'<p class="ph-sub">{sub}</p>'
        f'</div>',
        unsafe_allow_html=True
    )


# ══════════════════════════════════════════════════════════════════════════════
# PAGE ROUTER
# ══════════════════════════════════════════════════════════════════════════════
active_page = st.session_state.get("active_page", MENU_OPTIONS[0])


# ══════════════════════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
if active_page == MENU_OPTIONS[0]:
    col_main, col_side = st.columns([2, 1], gap="large")

    with col_main:
        # Hero — parameter chips hanya muncul jika kalkulasi sudah pernah dijalankan
        if kalkulasi_done and P is not None:
            param_chips = (
                '<div style="margin-top:1.4rem;display:flex;gap:0.7rem;flex-wrap:wrap;">'
                '<div style="background:rgba(255,255,255,0.15);border-radius:12px;padding:9px 18px;'
                'border:1px solid rgba(255,255,255,0.18);">'
                '<div style="font-size:0.6rem;opacity:0.6;text-transform:uppercase;'
                'letter-spacing:0.1em;font-weight:700;">Source</div>'
                f'<div style="font-size:1.3rem;font-weight:800;font-family:\'JetBrains Mono\',monospace;">S = {S}</div>'
                '</div>'
                '<div style="background:rgba(255,255,255,0.15);border-radius:12px;padding:9px 18px;'
                'border:1px solid rgba(255,255,255,0.18);">'
                '<div style="font-size:0.6rem;opacity:0.6;text-transform:uppercase;'
                'letter-spacing:0.1em;font-weight:700;">Kanal</div>'
                f'<div style="font-size:1.3rem;font-weight:800;font-family:\'JetBrains Mono\',monospace;">N = {N}</div>'
                '</div>'
                '<div style="background:rgba(255,255,255,0.15);border-radius:12px;padding:9px 18px;'
                'border:1px solid rgba(255,255,255,0.18);">'
                '<div style="font-size:0.6rem;opacity:0.6;text-transform:uppercase;'
                'letter-spacing:0.1em;font-weight:700;">Traffic</div>'
                f'<div style="font-size:1.3rem;font-weight:800;font-family:\'JetBrains Mono\',monospace;">A = {A:.1f}</div>'
                '</div>'
                '</div>'
            )
        else:
            param_chips = (
                '<div style="margin-top:1.4rem;">'
                '<div style="font-size:0.82rem;opacity:0.6;background:rgba(255,255,255,0.12);'
                'border-radius:10px;padding:8px 14px;display:inline-block;">'
                'Jalankan kalkulasi untuk melihat hasil di sini</div>'
                '</div>'
            )

        hero_html = (
            '<div class="hero-card">'
            '<div style="font-size:0.68rem;font-weight:700;letter-spacing:0.12em;'
            'text-transform:uppercase;opacity:0.6;margin-bottom:0.35rem;">Selamat Datang</div>'
            '<h1 style="font-size:1.85rem;font-weight:800;color:#fff;margin:0 0 0.25rem;'
            'line-height:1.15;letter-spacing:-0.02em;font-family:Inter,sans-serif;">EngsetPro Dashboard</h1>'
            '<p style="font-size:0.87rem;opacity:0.6;margin:0;font-weight:400;">'
            'Analisis probabilitas blocking · Model Engset Finite Source</p>'
            + param_chips +
            '</div>'
        )
        st.markdown(hero_html, unsafe_allow_html=True)

        # Result chips — hanya muncul kalau sudah ada hasil
        if kalkulasi_done and P is not None:
            chips_html = (
                '<div class="chip-grid">'
                '<div class="chip">'
                '<div class="chip-icon">◉</div>'
                f'<div class="chip-val">{P:.4f}</div>'
                '<div class="chip-lbl">P Blocking</div>'
                '</div>'
                '<div class="chip">'
                '<div class="chip-icon">⌬</div>'
                f'<div class="chip-val">{carried:.3f}</div>'
                '<div class="chip-lbl">Carried (Erl)</div>'
                '</div>'
                '<div class="chip">'
                '<div class="chip-icon">◎</div>'
                f'<div class="chip-val">{lost:.3f}</div>'
                '<div class="chip-lbl">Lost (Erl)</div>'
                '</div>'
                '</div>'
            )
            st.markdown(chips_html, unsafe_allow_html=True)

            st.markdown('<p class="sec-title">Ringkasan Sistem</p>', unsafe_allow_html=True)

            items = [
                ("◉", "plan-icon-blue",  "Probabilitas Blocking",  f"{P*100:.3f}%" if P else "N/A",  f"Grade: {gos_text}"),
                ("⌬", "plan-icon-green", "Traffic Carried",         f"{carried:.4f} Erl",            f"Dari {A:.1f} Erl ditawarkan"),
                ("▦", "plan-icon-amber", "Kanal Minimum GoS 1%",   f"N = {min_n_1}",                "Untuk kualitas baik"),
                ("◎", "plan-icon-teal",  "Utilisasi Kanal",         f"{util_pct:.1f}%",              f"Rata-rata per {N} kanal"),
            ]
            for icon, icon_cls, name, val, desc in items:
                st.markdown(
                    f'<div class="plan-card">'
                    f'<div class="plan-icon-wrap {icon_cls}">{icon}</div>'
                    f'<div class="plan-info">'
                    f'<p class="plan-name">{name}</p>'
                    f'<p class="plan-desc">{desc}</p>'
                    f'</div>'
                    f'<div class="plan-val">{val}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )
        else:
            st.markdown(
                '<div class="card" style="text-align:center;padding:2rem;">'
                '<div style="font-size:2rem;margin-bottom:0.8rem;color:#C0CCFF;font-weight:300;">≡</div>'
                '<div style="font-size:1rem;font-weight:700;color:#0D1E50;margin-bottom:0.4rem;">Belum Ada Data</div>'
                '<div style="font-size:0.85rem;color:#9BAAD0;">Masuk ke menu <strong>Kalkulator Engset</strong> dan jalankan kalkulasi terlebih dahulu.</div>'
                '</div>',
                unsafe_allow_html=True
            )

    with col_side:
        # Donut chart
        fig, ax = plt.subplots(figsize=(3.5, 3.5))
        fig.patch.set_facecolor('#ffffff'); ax.set_facecolor('#ffffff')
        if kalkulasi_done and P is not None:
            sizes = [util_pct, 100 - util_pct]
            clrs  = [BLUE, '#E6ECFF']
            label_txt = f"{util_pct:.1f}%"
        else:
            sizes = [50, 50]
            clrs  = ['#DDE5FF', '#F0F4FF']
            label_txt = "0%"
        ax.pie(sizes, colors=clrs, startangle=90,
               wedgeprops=dict(width=0.42, edgecolor='white', linewidth=3.5),
               counterclock=False)
        ax.text(0, 0.06, label_txt,
                ha='center', va='center', fontsize=16, fontweight='bold',
                color='#0D1E50', fontfamily='monospace')
        ax.text(0, -0.22, "utilisasi", ha='center', va='center',
                fontsize=8.5, color='#9BAAD0')
        ax.axis('equal')
        plt.tight_layout(pad=0.5)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        # GoS card
        if kalkulasi_done and P is not None:
            pbar_w = min(100, (P or 0) * 500)
            bar_col = '#0A7040' if (P or 1) < 0.01 else '#C8860A' if (P or 1) < 0.05 else '#B02020'
            st.markdown(
                '<div class="card" style="text-align:center;padding:1.1rem;">'
                '<div style="font-size:0.66rem;color:#9BAAD0;text-transform:uppercase;'
                'letter-spacing:0.1em;margin-bottom:9px;font-weight:700;">Grade Of Service</div>'
                f'<span class="gos {gos_cls}" style="font-size:0.95rem;padding:6px 22px;">{gos_text}</span>'
                '<div style="margin-top:12px;">'
                '<div class="progress-wrap">'
                f'<div class="progress-fill" style="width:{pbar_w:.1f}%;background:{bar_col};"></div>'
                '</div></div>'
                '<div style="font-size:0.76rem;color:#9BAAD0;margin-top:7px;font-family:\'JetBrains Mono\',monospace;">'
                f'P = {f"{P:.6f}" if P is not None else "N/A"}'
                '</div></div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="card">'
                '<div style="font-size:0.8rem;font-weight:700;color:#0D1E50;margin-bottom:10px;">Rekomendasi Kanal</div>'
                '<div style="display:flex;justify-content:space-between;align-items:center;'
                'padding:7px 0;border-bottom:1px solid #EEF2FF;">'
                '<span style="font-size:0.78rem;color:#9BAAD0;">GoS 1%</span>'
                f'<strong style="color:#1660E8;font-family:\'JetBrains Mono\',monospace;font-size:0.88rem;">N = {min_n_1}</strong>'
                '</div>'
                '<div style="display:flex;justify-content:space-between;align-items:center;padding-top:7px;">'
                '<span style="font-size:0.78rem;color:#9BAAD0;">GoS 0.1%</span>'
                f'<strong style="color:#1660E8;font-family:\'JetBrains Mono\',monospace;font-size:0.88rem;">N = {min_n_001}</strong>'
                '</div></div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<div class="card" style="text-align:center;padding:1.2rem;">'
                '<div style="font-size:0.66rem;color:#9BAAD0;text-transform:uppercase;'
                'letter-spacing:0.1em;margin-bottom:9px;font-weight:700;">Grade Of Service</div>'
                '<div style="font-size:0.85rem;color:#C8D0E8;padding:1rem 0;">Belum ada data</div>'
                '</div>',
                unsafe_allow_html=True
            )

        if not valid and kalkulasi_done:
            st.markdown('<div class="eng-warn">Pastikan S > N dan A < S</div>',
                        unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# KALKULATOR ENGSET
# ══════════════════════════════════════════════════════════════════════════════
elif active_page == MENU_OPTIONS[1]:
    page_header("Rekayasa Trafik", "Kalkulator Engset",
                "Hitung probabilitas blocking dengan model finite source")

    st.markdown(
        '<div style="font-size:0.8rem;color:#4A5680;font-weight:600;margin-bottom:0.9rem;">'
        'Masukkan Parameter Sistem</div>',
        unsafe_allow_html=True
    )

    col_s, col_n, col_a = st.columns(3, gap="large")
    with col_s:
        inp_S = st.number_input("S  Jumlah Source (Pengguna)", min_value=2, max_value=200,
                                 value=st.session_state["S_calc"], step=1)
    with col_n:
        inp_N = st.number_input("N  Jumlah Kanal (Server)", min_value=1, max_value=100,
                                 value=st.session_state["N_calc"], step=1)
    with col_a:
        inp_A = st.number_input("A  Traffic Offered (Erlang)", min_value=0.1,
                                 max_value=float(max(1, inp_S - 1)),
                                 value=min(st.session_state["A_calc"], float(inp_S - 2)),
                                 step=0.1, format="%.1f")

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    if st.button("▶  Jalankan Kalkulasi", use_container_width=True):
        st.session_state["S_calc"] = inp_S
        st.session_state["N_calc"] = inp_N
        st.session_state["A_calc"] = inp_A
        st.session_state["kalkulasi_done"] = True
        # Hitung dan simpan ke history
        _S, _N, _A = inp_S, inp_N, inp_A
        _valid = _S > _N and 0 < _A < _S
        if _valid:
            _P = engset(_S, _N, _A)
            if _P is not None:
                _carried = _A * (1 - _P)
                _lost    = _A * _P
                _util    = (_carried / _N) * 100
                _gos, _  = gos_label(_P)
                _entry = {
                    "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "S": _S, "N": _N, "A": _A,
                    "P": _P,
                    "P_pct": _P * 100,
                    "carried": _carried,
                    "lost": _lost,
                    "util": _util,
                    "gos": _gos,
                }
                # Cek duplikat (S, N, A sama)
                existing = [(h["S"], h["N"], h["A"]) for h in st.session_state["history"]]
                if (_S, _N, _A) not in existing:
                    st.session_state["history"].append(_entry)
        st.rerun()

    st.markdown("<div style='height:0.7rem'></div>", unsafe_allow_html=True)

    if not kalkulasi_done:
        st.markdown(
            '<div class="card" style="text-align:center;padding:2.5rem 1.5rem;">'
            '<div style="font-size:2rem;color:#C0CCFF;margin-bottom:0.8rem;">⌬</div>'
            '<div style="font-size:1rem;font-weight:700;color:#0D1E50;margin-bottom:0.4rem;">Belum Ada Hasil</div>'
            '<div style="font-size:0.85rem;color:#9BAAD0;">Masukkan parameter S, N, dan A di atas,<br>lalu tekan <strong>Jalankan Kalkulasi</strong>.</div>'
            '</div>',
            unsafe_allow_html=True
        )
    elif not valid:
        st.markdown('<div class="eng-warn">Pastikan S lebih besar dari N dan A lebih kecil dari S.</div>',
                    unsafe_allow_html=True)
    else:
        col1, col2 = st.columns([1.2, 1], gap="large")

        with col1:
            st.markdown('<p class="sec-title">Hasil Perhitungan</p>', unsafe_allow_html=True)
            rows = [
                ("◉", "Probabilitas Blocking (P)", f"{P:.8f}",       "Probabilitas"),
                ("◎", "Blocking Persen",            f"{P*100:.4f}%",  "Persentase"),
                ("▦", "Grade Of Service",           gos_text,         "Penilaian kualitas"),
                ("⌬", "Traffic Carried",            f"{carried:.4f} Erl", "Terlayani"),
                ("⤓", "Traffic Lost",               f"{lost:.4f} Erl",    "Terblokir"),
                ("◈", "Utilisasi Kanal",            f"{util_pct:.2f}%",   "Per kanal"),
                ("⊹", "Traffic Intensity",          f"{A/N:.4f} Erl/ch",  "Per kanal"),
            ]
            for icon, label, val, unit in rows:
                st.markdown(
                    '<div class="plan-card" style="padding:0.8rem 1rem;">'
                    f'<div class="plan-icon-wrap plan-icon-blue" '
                    f'style="width:36px;height:36px;border-radius:10px;font-size:1rem;">{icon}</div>'
                    f'<div class="plan-info">'
                    f'<p class="plan-name" style="font-size:0.83rem;">{label}</p>'
                    f'<p class="plan-desc">{unit}</p>'
                    f'</div>'
                    f'<div class="plan-val" style="font-size:0.88rem;">{val}</div>'
                    '</div>',
                    unsafe_allow_html=True
                )

        with col2:
            st.markdown('<p class="sec-title">Rekomendasi N Minimum</p>', unsafe_allow_html=True)
            targets = [0.10, 0.05, 0.02, 0.01, 0.005, 0.001]
            rec_rows = ""
            for t in targets:
                mn = find_min_N(S, A, t)
                ok = N >= (mn if mn else 9999)
                rec_rows += (
                    f'<tr><td>{t*100:.1f}%</td>'
                    f'<td>N = {mn if mn else "N/A"}</td>'
                    f'<td>{"&#10003;" if ok else "&#10007;"}</td></tr>'
                )
            st.markdown(
                '<div class="card" style="padding:1.1rem;">'
                '<table class="eng-table">'
                '<thead><tr><th>Target GoS</th><th>N Minimum</th>'
                f'<th>Status N={N}</th></tr></thead>'
                f'<tbody>{rec_rows}</tbody>'
                '</table></div>',
                unsafe_allow_html=True
            )

            if P < 0.001:
                st.markdown(f'<div class="eng-ok">Sangat baik · blocking hanya {P*100:.4f}%</div>',
                            unsafe_allow_html=True)
            elif P < 0.01:
                st.markdown(f'<div class="eng-ok">Baik · blocking {P*100:.3f}%</div>',
                            unsafe_allow_html=True)
            elif P < 0.05:
                st.markdown('<div class="eng-warn">Cukup · pertimbangkan tambah kanal</div>',
                            unsafe_allow_html=True)
            else:
                st.markdown('<div class="eng-warn">Buruk · tambah kanal segera!</div>',
                            unsafe_allow_html=True)

            with st.expander("Lihat Langkah Perhitungan"):
                ratio = A / (S - A)
                st.markdown(f"""
**Langkah 1 — Hitung Rasio:**
```
A / (S-A) = {A:.2f} / ({S} - {A:.2f}) = {ratio:.6f}
```
**Langkah 2 — Hitung Pembilang:**
```
C(S-1, N) x (A/(S-A))^N
= C({S-1}, {N}) x {ratio:.6f}^{N}
```
**Langkah 3 — Hitung Penyebut:**
```
sum[i=0..{N}] C({S-1}, i) x {ratio:.6f}^i
```
**Langkah 4 — Hasil Akhir:**
```
P = pembilang / penyebut
P = {P:.8f}
P = {P*100:.4f}%
```
                """)


# ══════════════════════════════════════════════════════════════════════════════
# HITUNG TRAFFIC A
# ══════════════════════════════════════════════════════════════════════════════
elif active_page == MENU_OPTIONS[2]:
    page_header("Perhitungan Trafik", "Hitung Traffic Offered (A)",
                "Tentukan nilai A dari parameter jaringan yang diketahui")

    tab1, tab2, tab3 = st.tabs([
        "Call Rate & Hold Time",
        "Pengguna Aktif (BHT)",
        "Data Rate / Throughput"
    ])

    with tab1:
        st.markdown(
            '<div class="formula-wrap" style="margin-bottom:1.1rem;">'
            '<span class="formula-tag">Rumus Erlang</span>'
            '<div class="formula-body">'
            'A = &lambda; &times; h<br><br>'
            '&lambda; = Call rate (panggilan/jam per pengguna)<br>'
            'h = Rata-rata durasi panggilan (menit)'
            '</div></div>',
            unsafe_allow_html=True
        )

        c1, c2 = st.columns(2, gap="large")
        with c1:
            call_rate  = st.number_input("Call Rate  panggilan/jam per pengguna",
                                         0.01, 1000.0, 3.0, 0.1, format="%.2f")
            hold_time  = st.number_input("Hold Time rata-rata (menit)",
                                         0.1, 120.0, 2.0, 0.1, format="%.1f")
            n_users_t1 = st.number_input("Jumlah pengguna aktif (opsional untuk A total)",
                                         1, 10000, S)

        with c2:
            lam_s = call_rate / 3600
            h_s   = hold_time * 60
            A_1   = lam_s * h_s
            A_tot = A_1 * n_users_t1

            st.markdown(
                '<div class="card">'
                '<div style="font-size:0.83rem;font-weight:700;color:#0D1E50;margin-bottom:0.9rem;">'
                'Hasil Perhitungan</div>'
                '<div style="display:flex;justify-content:space-between;align-items:center;'
                'padding:8px 0;border-bottom:1px solid #EEF2FF;">'
                '<span style="font-size:0.8rem;color:#9BAAD0;">Traffic Per Pengguna</span>'
                f'<span style="font-family:\'JetBrains Mono\';font-weight:700;color:#1660E8;font-size:0.88rem;">'
                f'{A_1:.6f} Erl</span></div>'
                '<div style="display:flex;justify-content:space-between;align-items:center;'
                'padding:8px 0;border-bottom:1px solid #EEF2FF;">'
                '<span style="font-size:0.8rem;color:#9BAAD0;">&lambda; (konversi ke /detik)</span>'
                f'<span style="font-family:\'JetBrains Mono\';font-weight:700;color:#0D1E50;font-size:0.88rem;">'
                f'{lam_s:.6f} call/s</span></div>'
                '<div style="display:flex;justify-content:space-between;align-items:center;'
                'padding:8px 0;border-bottom:1px solid #EEF2FF;">'
                '<span style="font-size:0.8rem;color:#9BAAD0;">h (konversi ke detik)</span>'
                f'<span style="font-family:\'JetBrains Mono\';font-weight:700;color:#0D1E50;font-size:0.88rem;">'
                f'{h_s:.0f} detik</span></div>'
                '<div style="margin-top:0.9rem;background:linear-gradient(135deg,#EBF4FF,#E0F3FF);'
                'border-radius:12px;padding:1.1rem;text-align:center;">'
                '<div style="font-size:0.66rem;color:#005580;text-transform:uppercase;'
                f'letter-spacing:0.1em;margin-bottom:5px;font-weight:700;">A Total ({n_users_t1} pengguna)</div>'
                f'<div style="font-size:2rem;font-weight:800;color:#1660E8;'
                f'font-family:\'JetBrains Mono\';">{A_tot:.4f} Erl</div>'
                '<div style="font-size:0.76rem;color:#005580;margin-top:4px;font-weight:500;">'
                'Masukkan ke parameter kalkulator sebagai nilai A</div>'
                '</div></div>',
                unsafe_allow_html=True
            )

            if 0 < A_tot < S and S > N:
                P2 = engset(S, N, A_tot)
                if P2:
                    g2, gc2 = gos_label(P2)
                    cls = "eng-ok" if P2 < 0.01 else "eng-warn"
                    st.markdown(
                        f'<div class="{cls}"><strong>Hasil Engset</strong> dengan '
                        f'A={A_tot:.4f}, S={S}, N={N}: '
                        f'P = {P2:.6f} &middot; Blocking = {P2*100:.3f}% &middot; GoS = {g2}</div>',
                        unsafe_allow_html=True
                    )

    with tab2:
        st.markdown(
            '<div class="formula-wrap" style="margin-bottom:1.1rem;">'
            '<span class="formula-tag">Rumus BHT</span>'
            '<div class="formula-body">'
            'A = U &times; BHT<br><br>'
            'U   = Jumlah pengguna aktif di jam sibuk<br>'
            'BHT = Busy Hour Traffic per pengguna (Erlang)'
            '</div></div>',
            unsafe_allow_html=True
        )

        c1, c2 = st.columns(2, gap="large")
        with c1:
            U_val = st.number_input("U  Pengguna Aktif Jam Sibuk", 1, 10000, 50)
            BHT   = st.number_input("BHT  Busy Hour Traffic Per User (Erl)",
                                    0.001, 1.0, 0.1, 0.001, format="%.3f")
        with c2:
            A_t2 = U_val * BHT
            st.markdown(
                '<div class="card" style="text-align:center;padding:1.6rem;">'
                f'<div style="font-size:0.78rem;color:#9BAAD0;margin-bottom:6px;'
                f'font-family:\'JetBrains Mono\';">A = {U_val} &times; {BHT:.3f}</div>'
                f'<div style="font-size:2.4rem;font-weight:800;color:#1660E8;'
                f'font-family:\'JetBrains Mono\';">{A_t2:.4f}</div>'
                '<div style="font-size:0.82rem;color:#9BAAD0;margin-top:5px;font-weight:500;">Erlang</div>'
                '</div>',
                unsafe_allow_html=True
            )
            if 0 < A_t2 < S and S > N:
                P3 = engset(S, N, A_t2)
                if P3:
                    g3, gc3 = gos_label(P3)
                    cls = "eng-ok" if P3 < 0.01 else "eng-warn"
                    st.markdown(
                        f'<div class="{cls}">P = {P3:.6f} &middot; '
                        f'Blocking = {P3*100:.3f}% &middot; GoS = {g3}</div>',
                        unsafe_allow_html=True
                    )

    with tab3:
        st.markdown(
            '<div class="formula-wrap" style="margin-bottom:1.1rem;">'
            '<span class="formula-tag">Rumus Data Rate</span>'
            '<div class="formula-body">'
            'A = Data Rate (Mbps) / Kapasitas Per Kanal (Mbps)'
            '</div></div>',
            unsafe_allow_html=True
        )
        c1, c2 = st.columns(2, gap="large")
        with c1:
            dr = st.number_input("Data Rate Total (Mbps)", 0.1, 100000.0, 100.0, 1.0)
            cc = st.number_input("Kapasitas Per Kanal (Mbps)", 0.1, 10000.0, 10.0, 0.1)
        with c2:
            A_t3 = dr / cc
            st.markdown(
                '<div class="card" style="text-align:center;padding:1.6rem;">'
                f'<div style="font-size:0.78rem;color:#9BAAD0;margin-bottom:6px;'
                f'font-family:\'JetBrains Mono\';">A = {dr:.1f} / {cc:.1f}</div>'
                f'<div style="font-size:2.4rem;font-weight:800;color:#1660E8;'
                f'font-family:\'JetBrains Mono\';">{A_t3:.4f}</div>'
                '<div style="font-size:0.82rem;color:#9BAAD0;margin-top:5px;font-weight:500;">Erlang</div>'
                '</div>',
                unsafe_allow_html=True
            )
            if 0 < A_t3 < S and S > N:
                P4 = engset(S, N, A_t3)
                if P4:
                    g4, gc4 = gos_label(P4)
                    cls = "eng-ok" if P4 < 0.01 else "eng-warn"
                    st.markdown(
                        f'<div class="{cls}">P = {P4:.6f} &middot; '
                        f'Blocking = {P4*100:.3f}% &middot; GoS = {g4}</div>',
                        unsafe_allow_html=True
                    )


# ══════════════════════════════════════════════════════════════════════════════
# ANALISIS DAN GRAFIK
# ══════════════════════════════════════════════════════════════════════════════
elif active_page == MENU_OPTIONS[3]:
    page_header("Visualisasi", "Analisis Dan Grafik",
                "Visualisasi perilaku sistem terhadap variasi parameter")

    if not kalkulasi_done:
        st.markdown(
            '<div class="card" style="text-align:center;padding:2.5rem 1.5rem;">'
            '<div style="font-size:2rem;color:#C0CCFF;margin-bottom:0.8rem;">▦</div>'
            '<div style="font-size:1rem;font-weight:700;color:#0D1E50;margin-bottom:0.4rem;">Belum Ada Data</div>'
            '<div style="font-size:0.85rem;color:#9BAAD0;">Jalankan kalkulasi di menu <strong>Kalkulator Engset</strong> terlebih dahulu.</div>'
            '</div>',
            unsafe_allow_html=True
        )
    elif not valid:
        st.markdown('<div class="eng-warn">Periksa parameter di kalkulator terlebih dahulu.</div>',
                    unsafe_allow_html=True)
    else:
        # ── Diagram Batang: Blocking Vs N ──────────────────────────────────────
        cg1, cg2 = st.columns(2, gap="large")

        with cg1:
            st.markdown(
                '<div style="font-size:0.88rem;font-weight:700;color:#0D1E50;margin-bottom:0.5rem;">'
                'Blocking Vs Jumlah Kanal (N)</div>',
                unsafe_allow_html=True
            )
            max_n = min(S - 1, 30)
            ns_   = list(range(1, max_n + 1))
            ps_   = [(engset(S, n, A) or 0) * 100 for n in ns_]

            fig1, ax1 = plt.subplots(figsize=(5.5, 4))
            fig1.patch.set_facecolor('white'); ax1.set_facecolor('white')

            bar_colors = [RED if n == N else BLUE for n in ns_]
            bars = ax1.bar(ns_, ps_, color=bar_colors, width=0.7, zorder=3,
                           edgecolor='white', linewidth=0.5)
            ax1.axhline(1.0, color=AMBER, linestyle='--', linewidth=1.2, alpha=0.8, zorder=4)
            ax1.axhline(0.1, color=GREEN, linestyle='--', linewidth=1.2, alpha=0.8, zorder=4)
            ax1.text(max_n * 0.97, 1.08, 'GoS 1%', ha='right', fontsize=7.5, color=AMBER)
            ax1.text(max_n * 0.97, 0.18, 'GoS 0.1%', ha='right', fontsize=7.5, color=GREEN)

            legend_patches = [
                mpatches.Patch(color=BLUE, label=f'Blocking (%)'),
                mpatches.Patch(color=RED,  label=f'N Aktif = {N}'),
            ]
            ax1.legend(handles=legend_patches, fontsize=8, frameon=False)

            ax1.set_xlabel('N (Jumlah Kanal)', fontsize=9, color='#78909c', labelpad=6)
            ax1.set_ylabel('Blocking (%)', fontsize=9, color='#78909c', labelpad=6)
            ax1.set_title(f'S={S}, A={A:.1f} Erl', fontsize=9, color='#9BAAD0', pad=8)
            ax1.grid(True, axis='y', linestyle='--', alpha=0.2, color='#c8d4ff')
            ax1.spines[['top', 'right', 'left', 'bottom']].set_visible(False)
            ax1.tick_params(colors='#9BAAD0', labelsize=7.5, length=0)
            plt.tight_layout(pad=1.2)
            st.pyplot(fig1, use_container_width=True)
            plt.close(fig1)

        with cg2:
            st.markdown(
                '<div style="font-size:0.88rem;font-weight:700;color:#0D1E50;margin-bottom:0.5rem;">'
                'Blocking Vs Traffic Offered (A)</div>',
                unsafe_allow_html=True
            )
            a_max_ = min(float(S - 1), 30.0)
            # Buat bucket A untuk diagram batang
            n_bars = min(30, int(a_max_ / 0.5))
            av_bars = np.linspace(0.1, a_max_, n_bars)
            pv_bars = [(engset(S, N, float(a)) or 0) * 100 for a in av_bars]

            fig2, ax2 = plt.subplots(figsize=(5.5, 4))
            fig2.patch.set_facecolor('white'); ax2.set_facecolor('white')

            bar_width = (a_max_ - 0.1) / n_bars * 0.8
            bar_colors2 = [RED if abs(a - A) == min(abs(x - A) for x in av_bars) else TEAL for a in av_bars]
            ax2.bar(av_bars, pv_bars, width=bar_width, color=bar_colors2, zorder=3,
                    edgecolor='white', linewidth=0.4)
            ax2.axhline(1.0, color=AMBER, linestyle='--', linewidth=1.2, alpha=0.8, zorder=4)
            ax2.text(a_max_ * 0.97, 1.08, 'GoS 1%', ha='right', fontsize=7.5, color=AMBER)

            legend_patches2 = [
                mpatches.Patch(color=TEAL, label=f'Blocking (%)'),
                mpatches.Patch(color=RED,  label=f'A Aktif = {A:.1f}'),
            ]
            ax2.legend(handles=legend_patches2, fontsize=8, frameon=False)

            ax2.set_xlabel('A (Traffic Offered, Erlang)', fontsize=9, color='#78909c', labelpad=6)
            ax2.set_ylabel('Blocking (%)', fontsize=9, color='#78909c', labelpad=6)
            ax2.set_title(f'S={S}, N={N} Kanal', fontsize=9, color='#9BAAD0', pad=8)
            ax2.grid(True, axis='y', linestyle='--', alpha=0.2, color='#c8d4ff')
            ax2.spines[['top', 'right', 'left', 'bottom']].set_visible(False)
            ax2.tick_params(colors='#9BAAD0', labelsize=7.5, length=0)
            plt.tight_layout(pad=1.2)
            st.pyplot(fig2, use_container_width=True)
            plt.close(fig2)

        # ── Diagram Batang: Multi-Nilai A ──────────────────────────────────────
        st.markdown(
            '<div style="font-size:0.88rem;font-weight:700;color:#0D1E50;margin:1.2rem 0 0.5rem;">'
            'Perbandingan Blocking Vs N untuk Berbagai Nilai A</div>',
            unsafe_allow_html=True
        )
        palette = [BLUE, TEAL, GREEN, AMBER, RED, '#8B5CF6']
        a_list  = [round(A * m, 2) for m in [0.5, 0.75, 1.0, 1.25, 1.5, 2.0] if 0 < A * m < S][:6]
        max_n3  = min(S - 1, 25)
        ns3_    = list(range(1, max_n3 + 1))

        fig3, ax3 = plt.subplots(figsize=(11, 4.2))
        fig3.patch.set_facecolor('white'); ax3.set_facecolor('white')

        bar_total = len(ns3_)
        group_width = 0.8
        bar_w = group_width / len(a_list)
        x_base = np.array(ns3_)

        for idx, a_c in enumerate(a_list):
            ps3 = [(engset(S, n, a_c) or 0) * 100 for n in ns3_]
            offset = (idx - len(a_list) / 2 + 0.5) * bar_w
            ax3.bar(x_base + offset, ps3, width=bar_w * 0.92,
                    color=palette[idx % len(palette)], label=f'A={a_c:.1f} Erl',
                    zorder=3, edgecolor='white', linewidth=0.3)

        ax3.axvline(N, color='#9BAAD0', linestyle=':', linewidth=1.8, label=f'N Aktif = {N}')
        ax3.axhline(1.0, color=AMBER, linestyle='--', linewidth=1, alpha=0.6)
        ax3.set_xlabel('N (Jumlah Kanal)', fontsize=9, color='#78909c', labelpad=6)
        ax3.set_ylabel('Blocking (%)', fontsize=9, color='#78909c', labelpad=6)
        ax3.set_title(f'Perbandingan Blocking Vs N untuk Berbagai A  (S={S})',
                      fontsize=10, color='#0D1E50', fontweight='bold', pad=10)
        ax3.legend(fontsize=8, ncol=min(len(a_list) + 1, 4), frameon=False)
        ax3.grid(True, axis='y', linestyle='--', alpha=0.18, color='#c8d4ff')
        ax3.spines[['top', 'right', 'left', 'bottom']].set_visible(False)
        ax3.tick_params(colors='#9BAAD0', labelsize=8, length=0)
        ax3.set_xticks(ns3_)
        plt.tight_layout(pad=1.2)
        st.pyplot(fig3, use_container_width=True)
        plt.close(fig3)

        # ── Tabel Detail ────────────────────────────────────────────────────────
        st.markdown(
            '<div style="font-size:0.88rem;font-weight:700;color:#0D1E50;margin:1.2rem 0 0.5rem;">'
            'Tabel Detail Blocking Vs N</div>',
            unsafe_allow_html=True
        )
        rows_html = ""
        for n_i in range(1, min(S, N + 15)):
            p_i = engset(S, n_i, A)
            if p_i is None: continue
            c_i = A * (1 - p_i); l_i = A * p_i; u_i = (c_i / n_i) * 100
            g_t, g_c = gos_label(p_i)
            active = 'class="active"' if n_i == N else ""
            rows_html += (
                f'<tr {active}>'
                f'<td>{"&#9658; " if n_i == N else ""}{n_i}</td>'
                f'<td>{p_i:.6f}</td><td>{p_i*100:.3f}%</td>'
                f'<td>{c_i:.4f}</td><td>{l_i:.4f}</td>'
                f'<td>{u_i:.1f}%</td>'
                f'<td><span class="gos {g_c}">{g_t}</span></td></tr>'
            )
        st.markdown(
            '<table class="eng-table">'
            '<thead><tr>'
            '<th>N</th><th>P Blocking</th><th>Persen</th>'
            '<th>Carried (Erl)</th><th>Lost (Erl)</th>'
            '<th>Utilisasi</th><th>GoS</th>'
            f'</tr></thead><tbody>{rows_html}</tbody></table>'
            f'<div class="eng-info" style="margin-top:8px;font-size:0.76rem;">'
            f'Baris biru = nilai N yang dipilih saat ini (N={N})</div>',
            unsafe_allow_html=True
        )



# ══════════════════════════════════════════════════════════════════════════════
# EXPORT LAPORAN — dengan riwayat hitungan & delete per item
# ══════════════════════════════════════════════════════════════════════════════
elif active_page == MENU_OPTIONS[4]:
    page_header("Export", "Export & Riwayat Kalkulasi",
                "Kelola histori perhitungan dan unduh laporan PDF")

    history = st.session_state.get("history", [])

    if not history:
        st.markdown(
            '<div class="card" style="text-align:center;padding:3rem 1.5rem;">'
            '<div style="margin-bottom:1rem;">'
            '<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" '
            'fill="none" stroke="#C0CCFF" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>'
            '<polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/>'
            '</svg></div>'
            '<div style="font-size:1rem;font-weight:700;color:#0D1E50;margin-bottom:0.4rem;">Belum Ada Riwayat</div>'
            '<div style="font-size:0.85rem;color:#9BAAD0;">Jalankan kalkulasi di menu <strong>Kalkulator Engset</strong><br>untuk menyimpan riwayat hitungan.</div>'
            '</div>',
            unsafe_allow_html=True
        )
    else:
        # ── Header dengan jumlah history dan tombol hapus semua ──────────────
        col_htitle, col_hdel = st.columns([3, 1])
        with col_htitle:
            st.markdown(
                f'<div style="font-size:0.68rem;font-weight:700;color:#9BAAD0;text-transform:uppercase;'
                f'letter-spacing:0.1em;margin-bottom:0.3rem;">Riwayat Perhitungan</div>'
                f'<div style="font-size:0.9rem;font-weight:600;color:#0D1E50;">'
                f'{len(history)} sesi kalkulasi tersimpan</div>',
                unsafe_allow_html=True
            )
        with col_hdel:
            if st.button("🗑 Hapus Semua", use_container_width=True):
                st.session_state["history"] = []
                st.session_state["kalkulasi_done"] = False
                st.rerun()

        st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)

        # ── Tabel riwayat dengan tombol hapus per item ────────────────────────
        for i, h in enumerate(history):
            gos_c_map = {"Sangat Baik": "gos-great", "Baik": "gos-good", "Cukup": "gos-ok", "Buruk": "gos-bad"}
            g_cls = gos_c_map.get(h["gos"], "gos-ok")
            col_h1, col_h2 = st.columns([10, 1])
            with col_h1:
                st.markdown(
                    f'<div class="plan-card" style="padding:0.9rem 1.1rem;">'
                    f'<div style="background:#EBF0FE;width:36px;height:36px;border-radius:10px;'
                    f'display:flex;align-items:center;justify-content:center;flex-shrink:0;'
                    f'font-family:\'JetBrains Mono\';font-weight:700;color:#1660E8;font-size:0.8rem;">#{i+1}</div>'
                    f'<div style="flex:1;">'
                    f'<div style="display:flex;gap:1.4rem;flex-wrap:wrap;align-items:baseline;">'
                    f'<span style="font-size:0.85rem;font-weight:700;color:#0D1E50;font-family:\'JetBrains Mono\';">'
                    f'S={h["S"]} · N={h["N"]} · A={h["A"]:.1f} Erl</span>'
                    f'<span class="gos {g_cls}" style="font-size:0.7rem;">{h["gos"]}</span>'
                    f'</div>'
                    f'<div style="display:flex;gap:1.6rem;margin-top:4px;flex-wrap:wrap;">'
                    f'<span style="font-size:0.75rem;color:#9BAAD0;">P = <strong style="color:#1660E8;font-family:\'JetBrains Mono\';">{h["P"]:.6f}</strong></span>'
                    f'<span style="font-size:0.75rem;color:#9BAAD0;">Blocking = <strong style="color:#1660E8;">{h["P_pct"]:.3f}%</strong></span>'
                    f'<span style="font-size:0.75rem;color:#9BAAD0;">Util = <strong style="color:#0D1E50;">{h["util"]:.1f}%</strong></span>'
                    f'<span style="font-size:0.7rem;color:#C0CCFF;">{h["timestamp"]}</span>'
                    f'</div></div></div>',
                    unsafe_allow_html=True
                )
            with col_h2:
                if st.button("✕", key=f"del_{i}", help=f"Hapus sesi #{i+1}"):
                    st.session_state["history"].pop(i)
                    if not st.session_state["history"]:
                        st.session_state["kalkulasi_done"] = False
                    st.rerun()

        st.markdown("<div style='height:1.4rem'></div>", unsafe_allow_html=True)
        st.markdown('<div style="height:1px;background:#EEF2FF;margin-bottom:1.4rem;"></div>', unsafe_allow_html=True)

        # ── Export PDF History ────────────────────────────────────────────────
        if not PDF_OK:
            st.markdown('<div class="eng-warn">Instal ReportLab: <code>pip install reportlab</code></div>',
                        unsafe_allow_html=True)
        else:
            col_exp_l, col_exp_r = st.columns([3, 2], gap="large")

            with col_exp_l:
                st.markdown(
                    '<div style="font-size:0.68rem;font-weight:700;color:#9BAAD0;'
                    'text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.8rem;">Isi Laporan PDF</div>',
                    unsafe_allow_html=True
                )
                items_info = [
                    ("#EBF0FE", "Ringkasan Header", "Informasi aplikasi dan tanggal export"),
                    ("#E4F9EF", "Tabel Riwayat Lengkap", f"Seluruh {len(history)} sesi perhitungan"),
                    ("#FEF6DF", "Grafik Perbandingan", "P Blocking dari setiap sesi"),
                    ("#FEEDED", "Detail Tiap Sesi", "Parameter, hasil, GoS per sesi"),
                ]
                for bg, title_, desc_ in items_info:
                    st.markdown(
                        f'<div class="plan-card">'
                        f'<div class="plan-icon-wrap" style="background:{bg};width:38px;height:38px;border-radius:10px;'
                        f'font-size:0.9rem;color:#1660E8;">'
                        f'<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" '
                        f'fill="none" stroke="#1660E8" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>'
                        f'</div>'
                        f'<div class="plan-info"><p class="plan-name">{title_}</p><p class="plan-desc">{desc_}</p></div>'
                        f'</div>',
                        unsafe_allow_html=True
                    )

            with col_exp_r:
                st.markdown(
                    '<div class="card" style="padding:1.8rem;text-align:center;">'
                    '<div style="width:64px;height:64px;border-radius:18px;'
                    'background:linear-gradient(135deg,#1660E8,#0EAAE0);'
                    'display:flex;align-items:center;justify-content:center;'
                    'margin:0 auto 1rem;">'
                    '<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" '
                    'fill="none" stroke="white" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
                    '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>'
                    '<polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/>'
                    '</svg></div>'
                    '<div style="font-size:1rem;font-weight:800;color:#0D1E50;margin-bottom:0.35rem;">Export PDF Riwayat</div>'
                    f'<div style="font-size:0.8rem;color:#9BAAD0;line-height:1.7;margin-bottom:1.2rem;">'
                    f'Laporan A4 lengkap berisi semua {len(history)} sesi kalkulasi, siap cetak.</div>'
                    f'<div style="font-size:0.7rem;color:#B8C8E8;margin-bottom:1.2rem;">'
                    f'{datetime.now().strftime("%d %b %Y, %H:%M")}</div>'
                    '</div>',
                    unsafe_allow_html=True
                )

                if st.button("⬇  Generate & Download PDF Riwayat", use_container_width=True):
                    with st.spinner("Membuat laporan PDF riwayat..."):
                        def cb_hist(fig_):
                            buf_ = io.BytesIO()
                            fig_.savefig(buf_, format='png', dpi=150, bbox_inches='tight', facecolor='white')
                            buf_.seek(0); return buf_.read()

                        # ── Chart ringkasan: P Blocking per sesi ──────────────
                        labels_ = [f"#{j+1}\nS={h['S']},N={h['N']},A={h['A']:.1f}" for j, h in enumerate(history)]
                        pvals_  = [h["P"] * 100 for h in history]
                        bar_cols_ = [RED if p > 5 else AMBER if p > 1 else BLUE for p in pvals_]
                        fh, ah = plt.subplots(figsize=(max(6, len(history) * 1.2), 4))
                        fh.patch.set_facecolor('white'); ah.set_facecolor('white')
                        ah.bar(range(len(pvals_)), pvals_, color=bar_cols_, width=0.6,
                               edgecolor='white', linewidth=0.5, zorder=3)
                        ah.axhline(1.0, color=AMBER, linestyle='--', linewidth=1.2, label='GoS 1%')
                        ah.set_xticks(range(len(labels_))); ah.set_xticklabels(labels_, fontsize=7)
                        ah.set_ylabel('Blocking (%)', fontsize=9)
                        ah.set_title('Perbandingan P Blocking per Sesi Kalkulasi',
                                     fontsize=10, fontweight='bold', color='#0D1E50')
                        ah.legend(fontsize=8, frameon=False)
                        ah.grid(True, axis='y', linestyle='--', alpha=0.2)
                        ah.spines[['top', 'right']].set_visible(False)
                        plt.tight_layout()
                        chart_bytes_ = cb_hist(fh); plt.close(fh)

                        # ── Build PDF ──────────────────────────────────────────
                        buf_pdf = io.BytesIO()
                        doc = SimpleDocTemplate(
                            buf_pdf, pagesize=A4,
                            leftMargin=2.4*cm, rightMargin=2.4*cm,
                            topMargin=2.4*cm, bottomMargin=2.4*cm
                        )
                        C_DARK   = colors.HexColor('#0D1E50')
                        C_MEDIUM = colors.HexColor('#4A5680')
                        C_LIGHT  = colors.HexColor('#9BAAD0')
                        C_BG     = colors.HexColor('#F0F4FF')
                        C_BORDER = colors.HexColor('#C0CCFF')
                        C_HDR    = colors.HexColor('#1660E8')
                        C_ALT    = colors.HexColor('#EEF3FF')
                        C_WHITE  = colors.white

                        sTitle  = ParagraphStyle('sTitle', fontName='Helvetica-Bold', fontSize=20,
                                                  textColor=C_DARK, spaceAfter=4, leading=26)
                        sSub    = ParagraphStyle('sSub', fontName='Helvetica', fontSize=9,
                                                  textColor=C_LIGHT, spaceAfter=14, leading=13)
                        sH2     = ParagraphStyle('sH2', fontName='Helvetica-Bold', fontSize=12,
                                                  textColor=C_DARK, spaceBefore=14, spaceAfter=6, leading=16)
                        sH3     = ParagraphStyle('sH3', fontName='Helvetica-Bold', fontSize=10,
                                                  textColor=C_DARK, spaceBefore=10, spaceAfter=5, leading=14)
                        sBody   = ParagraphStyle('sBody', fontName='Helvetica', fontSize=9,
                                                  textColor=C_MEDIUM, leading=14, spaceAfter=4)
                        sFooter = ParagraphStyle('sFooter', fontName='Helvetica', fontSize=7.5,
                                                  textColor=C_LIGHT, alignment=TA_CENTER)

                        el = []
                        el.append(Paragraph("EngsetPro", sTitle))
                        el.append(Paragraph(
                            f"Laporan Riwayat Kalkulasi &nbsp;&middot;&nbsp; "
                            f"{datetime.now().strftime('%d %B %Y, %H:%M')} &nbsp;&middot;&nbsp; "
                            f"{len(history)} sesi tersimpan", sSub
                        ))
                        el.append(HRFlowable(width="100%", thickness=1.5, color=C_HDR, spaceAfter=14))

                        # 1. Tabel Ringkasan
                        el.append(Paragraph("1. Ringkasan Seluruh Sesi", sH2))
                        sum_data = [["#", "S", "N", "A (Erl)", "P Blocking", "Blocking%", "Carried", "GoS", "Waktu"]]
                        for j, h in enumerate(history):
                            sum_data.append([
                                str(j+1), str(h["S"]), str(h["N"]), f"{h['A']:.1f}",
                                f"{h['P']:.6f}", f"{h['P_pct']:.3f}%",
                                f"{h['carried']:.4f}", h["gos"],
                                h["timestamp"]
                            ])
                        tbl_sum = Table(sum_data, colWidths=[0.7*cm,1*cm,1*cm,1.3*cm,2.2*cm,1.6*cm,1.6*cm,1.4*cm,2.8*cm])
                        tbl_sum.setStyle(TableStyle([
                            ('BACKGROUND',    (0,0), (-1,0), C_HDR),
                            ('TEXTCOLOR',     (0,0), (-1,0), C_WHITE),
                            ('FONTNAME',      (0,0), (-1,0), 'Helvetica-Bold'),
                            ('FONTNAME',      (0,1), (-1,-1), 'Helvetica'),
                            ('FONTSIZE',      (0,0), (-1,-1), 7.5),
                            ('ALIGN',         (0,0), (-1,-1), 'CENTER'),
                            ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
                            ('ROWBACKGROUNDS',(0,1), (-1,-1), [C_WHITE, C_ALT]),
                            ('GRID',          (0,0), (-1,-1), 0.4, C_BORDER),
                            ('TOPPADDING',    (0,0), (-1,-1), 5),
                            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
                            ('LEFTPADDING',   (0,0), (-1,-1), 5),
                            ('RIGHTPADDING',  (0,0), (-1,-1), 5),
                        ]))
                        el.append(tbl_sum)
                        el.append(Spacer(1, 14))

                        # 2. Grafik perbandingan
                        el.append(Paragraph("2. Grafik Perbandingan P Blocking", sH2))
                        el.append(RLImage(io.BytesIO(chart_bytes_), width=14.6*cm, height=7*cm))
                        el.append(Spacer(1, 14))

                        # 3. Detail per sesi
                        el.append(Paragraph("3. Detail Per Sesi", sH2))
                        for j, h in enumerate(history):
                            el.append(Paragraph(f"Sesi #{j+1} — {h['timestamp']}", sH3))
                            det_data = [
                                ["Parameter", "Nilai"], ["S (Pengguna)", str(h["S"])],
                                ["N (Kanal)", str(h["N"])], ["A (Erlang)", f"{h['A']:.1f}"],
                                ["P Blocking", f"{h['P']:.8f}"], ["Blocking (%)", f"{h['P_pct']:.4f}%"],
                                ["Grade of Service", h["gos"]], ["Traffic Carried", f"{h['carried']:.4f} Erl"],
                                ["Traffic Lost", f"{h['lost']:.4f} Erl"], ["Utilisasi Kanal", f"{h['util']:.2f}%"],
                            ]
                            td = Table(det_data, colWidths=[5*cm, 9.6*cm])
                            td.setStyle(TableStyle([
                                ('BACKGROUND',    (0,0), (-1,0), C_HDR),
                                ('TEXTCOLOR',     (0,0), (-1,0), C_WHITE),
                                ('FONTNAME',      (0,0), (-1,0), 'Helvetica-Bold'),
                                ('FONTNAME',      (0,1), (-1,-1), 'Helvetica'),
                                ('FONTSIZE',      (0,0), (-1,-1), 8.5),
                                ('ALIGN',         (0,0), (0,-1), 'LEFT'),
                                ('ALIGN',         (1,0), (1,-1), 'LEFT'),
                                ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
                                ('ROWBACKGROUNDS',(0,1), (-1,-1), [C_WHITE, C_ALT]),
                                ('GRID',          (0,0), (-1,-1), 0.4, C_BORDER),
                                ('TOPPADDING',    (0,0), (-1,-1), 5),
                                ('BOTTOMPADDING', (0,0), (-1,-1), 5),
                                ('LEFTPADDING',   (0,0), (-1,-1), 8),
                                ('RIGHTPADDING',  (0,0), (-1,-1), 8),
                            ]))
                            el.append(td)
                            el.append(Spacer(1, 8))

                        el.append(HRFlowable(width="100%", thickness=0.5, color=C_BORDER, spaceAfter=7))
                        el.append(Paragraph(
                            f"EngsetPro v2.0 &nbsp;&middot;&nbsp; {datetime.now().strftime('%d %B %Y')} "
                            f"&nbsp;&middot;&nbsp; Rekayasa Trafik &nbsp;&middot;&nbsp; Model Engset Finite Source",
                            sFooter
                        ))
                        doc.build(el)
                        buf_pdf.seek(0)

                    st.download_button(
                        "⬇ Klik untuk Download PDF Riwayat",
                        data=buf_pdf,
                        file_name=f"engset_history_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                        mime="application/pdf",
                        use_container_width=True,
                    )
                    st.markdown('<div class="eng-ok">PDF riwayat siap! Klik tombol di atas untuk mengunduh.</div>',
                                unsafe_allow_html=True)


# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown(
    '<div style="text-align:center;color:#B8C8E8;font-size:0.74rem;'
    'padding:2.2rem 0 1.4rem;font-weight:400;letter-spacing:0.03em;">'
    'EngsetPro v2.0 &nbsp;&middot;&nbsp; Kalkulator Rekayasa Trafik Engset &nbsp;&middot;&nbsp; '
    'Metode: Log-space Arithmetic'
    '</div>',
    unsafe_allow_html=True
)
