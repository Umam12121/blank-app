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
# GLOBAL CSS — Green/Blue/Cyan palette (like reference)
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@300;400;500;600;700;800;900&family=Nunito+Sans:wght@300;400;600;700&family=Fira+Code:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'Nunito Sans', sans-serif !important; }

.stApp {
    background: #EEF2FF;
    min-height: 100vh;
}

#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
header    { visibility: hidden; }
.stDeployButton { display: none !important; }

.main .block-container {
    padding-top: 1.8rem !important;
    padding-bottom: 2rem !important;
    max-width: 1160px !important;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1740C9 0%, #1558D6 40%, #0E90C8 100%) !important;
    border-right: none !important;
    box-shadow: 6px 0 40px rgba(21,88,214,0.18);
}
[data-testid="stSidebar"] > div:first-child { padding-top: 0 !important; }
[data-testid="stSidebar"] * { color: rgba(255,255,255,0.9) !important; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.1) !important; }
[data-testid="stSidebar"] .stRadio > div { gap: 3px !important; }
[data-testid="stSidebar"] .stRadio label {
    background: rgba(255,255,255,0.08) !important;
    border-radius: 14px !important;
    padding: 11px 14px !important;
    cursor: pointer !important;
    transition: all 0.18s ease !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    font-size: 0.875rem !important;
    font-weight: 600 !important;
    color: rgba(255,255,255,0.7) !important;
    width: 100%;
    margin: 2px 0;
    backdrop-filter: blur(4px);
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(255,255,255,0.16) !important;
    color: #fff !important;
    border-color: rgba(255,255,255,0.2) !important;
}
[data-testid="stSidebar"] .stRadio [data-baseweb="radio"] > div:first-child {
    display: none !important;
}

/* CARD */
.card {
    background: #FFFFFF;
    border-radius: 22px;
    padding: 1.5rem 1.75rem;
    box-shadow: 0 4px 24px rgba(21,88,214,0.07), 0 1px 4px rgba(0,0,0,0.04);
    border: none;
    margin-bottom: 1rem;
    transition: box-shadow 0.2s, transform 0.2s;
}
.card:hover {
    box-shadow: 0 8px 36px rgba(21,88,214,0.12);
    transform: translateY(-1px);
}

/* HERO */
.hero-card {
    background: linear-gradient(135deg, #1548D3 0%, #1668E0 45%, #0CA8D4 100%);
    border-radius: 26px;
    padding: 2.5rem 2.4rem 2.2rem;
    color: white;
    margin-bottom: 1.25rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 16px 56px rgba(21,88,214,0.35), 0 4px 12px rgba(0,0,0,0.08);
}
.hero-card::before {
    content:""; position:absolute; top:-120px; right:-90px;
    width:380px; height:380px; border-radius:50%;
    background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 60%);
    pointer-events: none;
}
.hero-card::after {
    content:""; position:absolute; bottom:-80px; left:5%;
    width:260px; height:260px; border-radius:50%;
    background: radial-gradient(circle, rgba(12,168,212,0.25) 0%, transparent 65%);
    pointer-events: none;
}

/* CHIPS */
.chip-grid {
    display: grid; grid-template-columns: 1fr 1fr 1fr;
    gap: 12px; margin-bottom: 1.25rem;
}
.chip {
    background: #FFFFFF;
    border-radius: 18px; padding: 1.2rem 0.9rem;
    text-align: center;
    box-shadow: 0 4px 20px rgba(21,88,214,0.08), 0 1px 4px rgba(0,0,0,0.03);
    border: none;
    transition: transform 0.18s, box-shadow 0.18s;
}
.chip:hover { transform: translateY(-3px); box-shadow: 0 8px 28px rgba(21,88,214,0.14); }
.chip-icon { font-size: 1.3rem; margin-bottom: 6px; }
.chip-val  { font-size: 1rem; font-weight: 800; color: #0F1F4B; font-family: 'Fira Code', monospace; }
.chip-lbl  { font-size: 0.62rem; color: #9BAACB; text-transform: uppercase; letter-spacing: 0.08em; margin-top: 3px; font-weight: 600; }

/* LIST ROWS */
.plan-card {
    background: #FFFFFF;
    border-radius: 16px; padding: 0.9rem 1.2rem;
    display: flex; align-items: center; gap: 14px; margin-bottom: 10px;
    box-shadow: 0 2px 14px rgba(21,88,214,0.06);
    border: none;
    transition: all 0.18s;
}
.plan-card:hover {
    box-shadow: 0 6px 28px rgba(21,88,214,0.12);
    transform: translateX(3px);
}
.plan-icon-wrap {
    width: 42px; height: 42px; border-radius: 13px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.15rem; flex-shrink: 0;
}
.plan-icon-blue   { background: linear-gradient(135deg, #E8F0FE, #D2E3FC); }
.plan-icon-green  { background: linear-gradient(135deg, #E3F9EE, #C7F2DA); }
.plan-icon-amber  { background: linear-gradient(135deg, #FEF6E0, #FDE9B2); }
.plan-icon-red    { background: linear-gradient(135deg, #FEECEC, #FCD5D5); }
.plan-icon-teal   { background: linear-gradient(135deg, #E0F7FE, #B3EFFE); }
.plan-name { font-size: 0.875rem; font-weight: 700; color: #0F1F4B; margin: 0; }
.plan-desc { font-size: 0.73rem; color: #9BAACB; margin: 2px 0 0; font-weight: 500; }
.plan-val  { font-size: 0.95rem; font-weight: 800; color: #1558D6; font-family: 'Fira Code', monospace; margin-left: auto; }

/* GoS BADGE */
.gos { display: inline-block; padding: 5px 18px; border-radius: 100px; font-size: 0.77rem; font-weight: 700; letter-spacing: 0.03em; }
.gos-great { background: #D4F8E8; color: #0A7A45; }
.gos-good  { background: #E3F9EE; color: #0D6E3A; }
.gos-ok    { background: #FEF6E0; color: #906A10; }
.gos-bad   { background: #FEECEC; color: #A02828; }

/* FORMULA */
.formula-wrap {
    background: #FFFFFF;
    border: none;
    border-radius: 22px;
    padding: 1.8rem 2.1rem;
    margin-bottom: 1.25rem;
    box-shadow: 0 4px 24px rgba(21,88,214,0.07);
}
.formula-tag {
    display: inline-block;
    background: linear-gradient(135deg, #1558D6, #0CA8D4);
    color: #fff;
    font-size: 0.68rem; font-weight: 700; letter-spacing: 0.1em;
    text-transform: uppercase; padding: 5px 16px; border-radius: 100px; margin-bottom: 1.3rem;
    box-shadow: 0 4px 16px rgba(21,88,214,0.3);
}
.formula-body {
    font-family: 'Fira Code', monospace; font-size: 0.85rem; color: #0F1F4B;
    line-height: 2.2;
    background: #F2F6FF;
    border-radius: 14px;
    padding: 1.2rem 1.5rem;
    border: none;
}
.formula-legend { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 1rem; }
.fl-item { font-size: 0.8rem; color: #3A4F8C; display: flex; align-items: baseline; gap: 8px; }
.fl-sym  { font-family: 'Fira Code', monospace; font-weight: 700; color: #1558D6; min-width: 18px; }

/* EQUATION */
.eq-container {
    display: flex; justify-content: center; align-items: center;
    padding: 1.6rem 1rem; margin: 0.5rem 0;
    background: #F2F6FF;
    border-radius: 16px;
    border: none;
}

/* SECTION TITLE */
.sec-title {
    font-size: 0.72rem; font-weight: 800; color: #9BAACB;
    text-transform: uppercase; letter-spacing: 0.1em;
    margin: 0 0 0.8rem;
}

/* BANNERS */
.eng-warn {
    background: #FEF6E0; border: 1.5px solid #F5C842;
    border-radius: 14px; padding: 0.85rem 1.15rem;
    color: #7A5510; font-size: 0.84rem; margin-bottom: 0.9rem; font-weight: 600;
}
.eng-info {
    background: #EEF4FF; border: 1.5px solid #B3CEFF;
    border-radius: 14px; padding: 0.85rem 1.15rem;
    color: #1A3C8F; font-size: 0.84rem; margin-bottom: 0.9rem; font-weight: 600;
}
.eng-ok {
    background: #E3F9EE; border: 1.5px solid #6FE0A6;
    border-radius: 14px; padding: 0.85rem 1.15rem;
    color: #0A5F35; font-size: 0.84rem; margin-bottom: 0.9rem; font-weight: 600;
}

/* TABLE */
.eng-table { width: 100%; border-collapse: collapse; font-size: 0.83rem; border-radius: 16px; overflow: hidden; }
.eng-table th {
    background: linear-gradient(135deg, #1548D3, #1668E0);
    color: rgba(255,255,255,0.92); font-size: 0.68rem;
    text-transform: uppercase; letter-spacing: 0.09em;
    padding: 12px 16px; text-align: left; font-weight: 700;
}
.eng-table td {
    padding: 10px 16px; border-bottom: 1px solid #EEF2FF;
    color: #3A4F8C; font-family: 'Fira Code', monospace; font-size: 0.79rem;
}
.eng-table tr:last-child td { border-bottom: none; }
.eng-table tr:hover td { background: #F5F8FF; }
.eng-table tr.active td { background: #EEF4FF; font-weight: 700; color: #1558D6; }

/* BUTTONS */
.stButton > button {
    background: linear-gradient(135deg, #1558D6, #0CA8D4) !important;
    color: #fff !important; border: none !important; border-radius: 14px !important;
    padding: 0.7rem 2rem !important; font-weight: 700 !important;
    font-size: 0.9rem !important;
    box-shadow: 0 6px 22px rgba(21,88,214,0.32) !important;
    transition: all 0.18s !important;
    letter-spacing: 0.01em !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #1245B8, #0A96BC) !important;
    box-shadow: 0 10px 32px rgba(21,88,214,0.42) !important;
    transform: translateY(-2px) !important;
}

/* PROGRESS */
.progress-wrap {
    background: #E8EEFF; border-radius: 100px; height: 7px; margin: 10px 0; overflow: hidden;
}
.progress-fill {
    height: 100%; border-radius: 100px;
    background: linear-gradient(90deg, #1558D6, #0CA8D4);
    transition: width 0.5s ease;
}

/* TABS */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(21,88,214,0.06); border-radius: 16px;
    padding: 5px; gap: 3px; border: none;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 12px; font-weight: 700; font-size: 0.875rem;
    color: #9BAACB; padding: 9px 22px; transition: all 0.18s;
}
.stTabs [aria-selected="true"] {
    background: #fff !important; color: #1558D6 !important;
    box-shadow: 0 3px 14px rgba(21,88,214,0.14) !important;
}

/* INPUTS */
[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input {
    border-radius: 12px !important;
    border: 2px solid #E8EEFF !important;
    background: #F5F8FF !important;
    font-family: 'Fira Code', monospace !important;
    font-weight: 500 !important;
    color: #0F1F4B !important;
    transition: border-color 0.15s !important;
}
[data-testid="stNumberInput"] input:focus,
[data-testid="stTextInput"] input:focus {
    border-color: #1558D6 !important;
    box-shadow: 0 0 0 3px rgba(21,88,214,0.12) !important;
    background: #fff !important;
}

/* MOBILE NAV */
@media (max-width: 768px) {
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="stSidebarCollapsedControl"] { display: none !important; }
    div[data-testid="stSelectbox"] {
        display: block !important;
        background: linear-gradient(135deg, #1548D3, #1668E0) !important;
        border-radius: 0 0 20px 20px !important; padding: 0.6rem 0.9rem 0.8rem !important;
        margin-bottom: 1rem !important; box-shadow: 0 6px 24px rgba(21,88,214,0.35) !important;
        position: fixed !important; top: 0 !important; left: 0 !important; right: 0 !important;
        z-index: 99999 !important; width: 100% !important;
    }
    div[data-testid="stSelectbox"] label {
        color: rgba(255,255,255,0.55) !important; font-size: 0.68rem !important;
        font-weight: 700 !important; text-transform: uppercase !important; letter-spacing: 0.1em !important;
    }
    div[data-testid="stSelectbox"] > div > div {
        background: rgba(255,255,255,0.1) !important; border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 12px !important; color: #fff !important;
    }
    div[data-testid="stSelectbox"] > div > div > div { color: #fff !important; font-weight: 700 !important; font-size: 1rem !important; }
    div[data-testid="stSelectbox"] svg { fill: #fff !important; }
    .main .block-container { padding-left: 0.75rem !important; padding-right: 0.75rem !important; padding-top: 5.5rem !important; max-width: 100% !important; }
}
@media (min-width: 769px) {
    div[data-testid="stSelectbox"] { display: none !important; }
    #mobile-params-label { display: none !important; }
    .main .block-container { padding-top: 1.8rem !important; max-width: 1160px !important; }
}

/* SCROLLBAR */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #EEF2FF; }
::-webkit-scrollbar-thumb { background: #B3CEFF; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #1558D6; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# MENU
# ═══════════════════════════════════════════════════════════════════════════════
MENU_OPTIONS = [
    "🏠  Dashboard",
    "🧮  Kalkulator Engset",
    "📐  Hitung Traffic A",
    "📊  Analisis Dan Grafik",
    "📄  Export Laporan"
]

# Mobile selectbox — disembunyikan di desktop via CSS media query
mobile_page = st.selectbox("📋 Menu", MENU_OPTIONS, key="mobile_nav")


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
# ENGSET EQUATION SVG — standalone string (BUKAN f-string, tidak pakai {})
# Semua kurung kurawal SVG dihindari, pakai style attribute langsung
# ═══════════════════════════════════════════════════════════════════════════════
ENGSET_SVG = (
    # ─────────────────────────────────────────────────────────────────────────
    # Rumus Engset sesuai notasi dosen:
    #
    #          (S-1)!          (  A  )^N
    #       ─────────────── × (──────)
    #        N! (S-1-N)!      ( S-A  )
    # P = ──────────────────────────────────────────────────────
    #       N   (S-1)!          (  A  )^i
    #      Σ  ─────────────── × (──────)
    #      i=0  i! (S-1-i)!     ( S-A  )
    #
    # ViewBox: 700 x 310  (lebar cukup untuk notasi faktorial penuh)
    # ─────────────────────────────────────────────────────────────────────────
    '<svg viewBox="0 0 700 310" xmlns="http://www.w3.org/2000/svg" '
    'style="max-width:700px;width:100%;display:block;margin:0 auto;">'

    '<defs><style>'
    '.es  { font-family: Georgia, "Times New Roman", serif; }'
    '.ec  { fill: #0288D1; }'
    '.ed  { fill: #0a2540; }'
    '.ef  { fill: #0a2540; font-family: Georgia, serif; font-style: italic; }'
    '.eg  { fill: #546e7a; font-family: sans-serif; font-size: 12px; }'
    '.esm { font-family: Georgia, "Times New Roman", serif; fill: #0a2540; }'
    '</style></defs>'

    # ══════════════════════════════════════════════════════
    # P  =
    # ══════════════════════════════════════════════════════
    '<text x="28" y="148" class="es ed" font-size="30" font-style="italic" font-weight="bold">P</text>'
    '<text x="58" y="148" class="es ed" font-size="28">=</text>'

    # ══════════════════════════════════════════════════════
    # GARIS PECAHAN UTAMA  (x=88 .. x=670, y=150)
    # ══════════════════════════════════════════════════════
    '<line x1="88" y1="150" x2="670" y2="150" stroke="#0288D1" stroke-width="2.8"/>'

    # ══════════════════════════════════════════════════════
    # PEMBILANG  (di atas garis utama, tengah sekitar y=50-140)
    # Struktur:   [ (S-1)! / N!(S-1-N)! ]  ×  [ A/(S-A) ]^N
    # ══════════════════════════════════════════════════════

    # ── Sub-pecahan kiri pembilang: (S-1)! / N!(S-1-N)! ──
    # Pusat sub-pecahan ini di x=200

    # Pembilang sub-pecahan: (S-1)!
    '<text x="200" y="68" class="es ed" font-size="15" text-anchor="middle">(S&#8722;1)!</text>'

    # Garis sub-pecahan kiri (pembilang)
    '<line x1="140" y1="76" x2="260" y2="76" stroke="#0a2540" stroke-width="1.6"/>'

    # Penyebut sub-pecahan: N! (S-1-N)!
    '<text x="200" y="100" class="es ed" font-size="14" text-anchor="middle">N! (S&#8722;1&#8722;N)!</text>'

    # ── Tanda kali ──
    '<text x="282" y="88" class="es" fill="#90a4ae" font-size="22">&#215;</text>'

    # ── Sub-pecahan kanan pembilang: A / (S-A)  dengan pangkat N ──
    # Pusat di x=380

    # Kurung buka besar
    '<text x="308" y="98" class="es ed" font-size="44" font-weight="200">(</text>'

    # A (atas)
    '<text x="358" y="68" class="es ed" font-size="17" text-anchor="middle">A</text>'
    # Garis pecahan kecil
    '<line x1="340" y1="74" x2="376" y2="74" stroke="#0a2540" stroke-width="1.5"/>'
    # S-A (bawah)
    '<text x="358" y="96" class="es ed" font-size="14" text-anchor="middle">S&#8722;A</text>'

    # Kurung tutup besar
    '<text x="382" y="98" class="es ed" font-size="44" font-weight="200">)</text>'

    # Pangkat N (superscript)
    '<text x="416" y="50" class="es ec" font-size="17" font-style="italic" font-weight="bold">N</text>'

    # ══════════════════════════════════════════════════════
    # PENYEBUT  (di bawah garis utama)
    # Struktur:  Σ(i=0..N)  [ (S-1)! / i!(S-1-i)! ]  ×  [ A/(S-A) ]^i
    # ══════════════════════════════════════════════════════

    # ── Sigma dengan batas ──
    # N (batas atas sigma)
    '<text x="109" y="172" class="es ec" font-size="13" font-weight="bold" text-anchor="middle">N</text>'
    # Sigma besar
    '<text x="100" y="200" class="es ec" font-size="42">&#931;</text>'
    # i=0 (batas bawah sigma)
    '<text x="109" y="225" class="es ec" font-size="13" font-weight="bold" text-anchor="middle">i&#61;0</text>'

    # ── Sub-pecahan penyebut: (S-1)! / i!(S-1-i)! ──
    # Pusat di x=250

    # Pembilang sub-pecahan penyebut: (S-1)!
    '<text x="250" y="185" class="es ed" font-size="15" text-anchor="middle">(S&#8722;1)!</text>'

    # Garis sub-pecahan penyebut
    '<line x1="188" y1="193" x2="312" y2="193" stroke="#0a2540" stroke-width="1.6"/>'

    # Penyebut sub-pecahan: i! (S-1-i)!
    '<text x="250" y="217" class="es ed" font-size="14" text-anchor="middle">i! (S&#8722;1&#8722;i)!</text>'

    # ── Tanda kali penyebut ──
    '<text x="332" y="206" class="es" fill="#90a4ae" font-size="22">&#215;</text>'

    # ── Sub-pecahan kanan penyebut: A / (S-A)  pangkat i ──
    # Pusat di x=430

    # Kurung buka besar penyebut
    '<text x="358" y="215" class="es ed" font-size="44" font-weight="200">(</text>'

    # A (atas penyebut)
    '<text x="408" y="185" class="es ed" font-size="17" text-anchor="middle">A</text>'
    # Garis pecahan kecil penyebut
    '<line x1="390" y1="191" x2="426" y2="191" stroke="#0a2540" stroke-width="1.5"/>'
    # S-A (bawah penyebut)
    '<text x="408" y="213" class="es ed" font-size="14" text-anchor="middle">S&#8722;A</text>'

    # Kurung tutup besar penyebut
    '<text x="432" y="215" class="es ed" font-size="44" font-weight="200">)</text>'

    # Pangkat i (superscript)
    '<text x="468" y="162" class="es ec" font-size="17" font-style="italic" font-weight="bold">i</text>'

    # ══════════════════════════════════════════════════════
    # GARIS PEMISAH LEGENDA
    # ══════════════════════════════════════════════════════
    '<line x1="20" y1="256" x2="680" y2="256" stroke="#b2ebf2" stroke-width="1.5"/>'

    # ══════════════════════════════════════════════════════
    # LEGENDA  (2 kolom)
    # ══════════════════════════════════════════════════════
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
# SIDEBAR (desktop)
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(
        '<div style="background:linear-gradient(135deg,rgba(2,136,209,0.25),rgba(0,188,212,0.1));'
        'border-radius:20px;padding:1.4rem 1.2rem 1.2rem;margin-bottom:1.6rem;'
        'text-align:center;border:1px solid rgba(32,178,170,0.25);">'
        '<div style="font-size:2.4rem;margin-bottom:6px;">📡</div>'
        '<div style="font-size:1.4rem;font-weight:900;color:#fff;letter-spacing:-0.02em;">EngsetPro</div>'
        '<div style="font-size:0.68rem;color:rgba(255,255,255,0.45);letter-spacing:0.14em;'
        'margin-top:3px;text-transform:uppercase;font-weight:600;">Rekayasa Trafik v2.0</div>'
        '</div>',
        unsafe_allow_html=True
    )

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

    st.markdown("<hr>", unsafe_allow_html=True)

    # Parameter aktif — diambil dari session state
    s_disp = st.session_state.get('S_calc', 20)
    n_disp = st.session_state.get('N_calc', 5)
    a_disp = st.session_state.get('A_calc', 7.0)
    st.markdown(
        '<div style="background:rgba(255,255,255,0.06);border-radius:16px;padding:1.1rem;'
        'border:1px solid rgba(32,178,170,0.15);">'
        '<div style="font-size:0.68rem;color:rgba(255,255,255,0.4);text-transform:uppercase;'
        'letter-spacing:0.1em;margin-bottom:10px;font-weight:800;">&#9889; Parameter Aktif</div>'
        '<div style="font-size:0.85rem;color:rgba(255,255,255,0.85);line-height:2.2;">'
        f'S = <strong style="color:#A8C4FF;">{s_disp}</strong> pengguna<br>'
        f'N = <strong style="color:#A8C4FF;">{n_disp}</strong> kanal<br>'
        f'A = <strong style="color:#A8C4FF;">{a_disp:.1f}</strong> Erlang'
        '</div></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div style="margin-top:2rem;padding-top:1rem;text-align:center;'
        'font-size:0.7rem;color:rgba(255,255,255,0.2);line-height:1.8;">'
        'EngsetPro v2.0<br>Metode Log-space Arithmetic</div>',
        unsafe_allow_html=True
    )


# ═══════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════════════════════════════════════════════
if "S_calc" not in st.session_state: st.session_state["S_calc"] = 20
if "N_calc" not in st.session_state: st.session_state["N_calc"] = 5
if "A_calc" not in st.session_state: st.session_state["A_calc"] = 7.0
if "kalkulasi_done" not in st.session_state: st.session_state["kalkulasi_done"] = True

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

BLUE  = '#1558D6'
TEAL  = '#0CA8D4'
GREEN = '#0A7A45'
AMBER = '#F59E0B'
RED   = '#EF4444'
BG    = '#EEF2FF'


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE HEADER
# ═══════════════════════════════════════════════════════════════════════════════
def page_header(tag, title, sub):
    st.markdown(
        f'<div style="margin-bottom:1.8rem;">'
        f'<div style="font-size:0.7rem;color:#1558D6;font-weight:800;text-transform:uppercase;'
        f'letter-spacing:0.14em;margin-bottom:6px;">{tag}</div>'
        f'<h1 style="font-size:2rem;font-weight:900;color:#0F1F4B;margin:0;letter-spacing:-0.02em;">{title}</h1>'
        f'<p style="color:#9BAACB;margin:6px 0 0;font-size:0.9rem;">{sub}</p>'
        f'</div>',
        unsafe_allow_html=True
    )


# ══════════════════════════════════════════════════════════════════════════════
# ██ PAGE ROUTER
# ══════════════════════════════════════════════════════════════════════════════
active_page = st.session_state.get("mobile_nav", MENU_OPTIONS[0])


# ══════════════════════════════════════════════════════════════════════════════
# ██ DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
if active_page == "🏠  Dashboard":
    col_main, col_side = st.columns([2, 1], gap="large")

    with col_main:
        # Hero
        hero_html = (
            '<div class="hero-card">'
            '<div style="font-size:0.72rem;font-weight:800;letter-spacing:0.14em;'
            'text-transform:uppercase;opacity:0.65;margin-bottom:0.4rem;">✦ Selamat Datang</div>'
            '<h1 style="font-size:2rem;font-weight:900;color:#fff;margin:0 0 0.3rem;'
            'line-height:1.1;letter-spacing:-0.02em;">EngsetPro Dashboard</h1>'
            '<p style="font-size:0.9rem;opacity:0.65;margin:0;">'
            'Analisis probabilitas blocking real-time · Model Engset Finite Source</p>'
            '<div style="margin-top:1.6rem;display:flex;gap:0.8rem;flex-wrap:wrap;">'
            # chip S
            '<div style="background:rgba(255,255,255,0.15);border-radius:14px;padding:10px 20px;'
            'border:1px solid rgba(255,255,255,0.2);backdrop-filter:blur(4px);">'
            '<div style="font-size:0.65rem;opacity:0.65;text-transform:uppercase;'
            'letter-spacing:0.1em;font-weight:700;">Source</div>'
            f'<div style="font-size:1.5rem;font-weight:900;font-family:\'JetBrains Mono\',monospace;">S = {S}</div>'
            '</div>'
            # chip N
            '<div style="background:rgba(255,255,255,0.15);border-radius:14px;padding:10px 20px;'
            'border:1px solid rgba(255,255,255,0.2);backdrop-filter:blur(4px);">'
            '<div style="font-size:0.65rem;opacity:0.65;text-transform:uppercase;'
            'letter-spacing:0.1em;font-weight:700;">Kanal</div>'
            f'<div style="font-size:1.5rem;font-weight:900;font-family:\'JetBrains Mono\',monospace;">N = {N}</div>'
            '</div>'
            # chip A
            '<div style="background:rgba(255,255,255,0.15);border-radius:14px;padding:10px 20px;'
            'border:1px solid rgba(255,255,255,0.2);backdrop-filter:blur(4px);">'
            '<div style="font-size:0.65rem;opacity:0.65;text-transform:uppercase;'
            'letter-spacing:0.1em;font-weight:700;">Traffic</div>'
            f'<div style="font-size:1.5rem;font-weight:900;font-family:\'JetBrains Mono\',monospace;">A = {A:.1f}</div>'
            '</div>'
            '</div></div>'
        )
        st.markdown(hero_html, unsafe_allow_html=True)

        # Chips
        if P is not None:
            chips_html = (
                '<div class="chip-grid">'
                '<div class="chip">'
                '<div class="chip-icon">📡</div>'
                f'<div class="chip-val">{P:.4f}</div>'
                '<div class="chip-lbl">P Blocking</div>'
                '</div>'
                '<div class="chip">'
                '<div class="chip-icon">✅</div>'
                f'<div class="chip-val">{carried:.3f}</div>'
                '<div class="chip-lbl">Carried (Erl)</div>'
                '</div>'
                '<div class="chip">'
                '<div class="chip-icon">❌</div>'
                f'<div class="chip-val">{lost:.3f}</div>'
                '<div class="chip-lbl">Lost (Erl)</div>'
                '</div>'
                '</div>'
            )
            st.markdown(chips_html, unsafe_allow_html=True)

        st.markdown('<p class="sec-title">📋 Ringkasan Sistem</p>', unsafe_allow_html=True)

        items = [
            ("📶", "plan-icon-blue",  "Probabilitas Blocking",  f"{P*100:.3f}%" if P else "N/A",  f"Grade: {gos_text}"),
            ("🔄", "plan-icon-green", "Traffic Carried",         f"{carried:.4f} Erl",            f"Dari {A:.1f} Erl ditawarkan"),
            ("📉", "plan-icon-amber", "Kanal Minimum GoS 1%",   f"N = {min_n_1}",                "Untuk kualitas baik"),
            ("⚡", "plan-icon-teal",  "Utilisasi Kanal",         f"{util_pct:.1f}%",              f"Rata-rata per {N} kanal"),
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

    with col_side:
        # Donut
        fig, ax = plt.subplots(figsize=(3.5, 3.5))
        fig.patch.set_facecolor('#ffffff'); ax.set_facecolor('#ffffff')
        sizes = [util_pct, 100 - util_pct] if P is not None else [50, 50]
        clrs  = ['#1558D6', '#E8EEFF']    if P is not None else ['#e0f7fa', '#f0f9ff']
        ax.pie(sizes, colors=clrs, startangle=90,
               wedgeprops=dict(width=0.44, edgecolor='white', linewidth=4),
               counterclock=False)
        ax.text(0, 0.08, f"{util_pct:.1f}%" if P else "N/A",
                ha='center', va='center', fontsize=17, fontweight='bold',
                color='#0a2540', fontfamily='monospace')
        ax.text(0, -0.25, "utilisasi", ha='center', va='center',
                fontsize=9, color='#90a4ae')
        ax.axis('equal')
        plt.tight_layout(pad=0.5)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        # GoS card
        pbar_w = min(100, (P or 0) * 500)
        bar_col = '#0A7A45' if (P or 1) < 0.01 else '#C8860A' if (P or 1) < 0.05 else '#B02020'
        st.markdown(
            '<div class="card" style="text-align:center;padding:1.2rem;">'
            '<div style="font-size:0.7rem;color:#90a4ae;text-transform:uppercase;'
            'letter-spacing:0.1em;margin-bottom:10px;font-weight:700;">Grade Of Service</div>'
            f'<span class="gos {gos_cls}" style="font-size:1rem;padding:8px 24px;">{gos_text}</span>'
            '<div style="margin-top:14px;">'
            '<div class="progress-wrap">'
            f'<div class="progress-fill" style="width:{pbar_w:.1f}%;background:{bar_col};"></div>'
            '</div></div>'
            '<div style="font-size:0.78rem;color:#90a4ae;margin-top:8px;font-family:\'JetBrains Mono\',monospace;">'
            f'P = {f"{P:.6f}" if P is not None else "N/A"}'
            '</div></div>',
            unsafe_allow_html=True
        )

        # Rekomendasi
        st.markdown(
            '<div class="card">'
            '<div style="font-size:0.82rem;font-weight:800;color:#0a2540;margin-bottom:12px;">🎯 Rekomendasi Kanal</div>'
            '<div style="display:flex;justify-content:space-between;align-items:center;'
            'padding:8px 0;border-bottom:1px solid #e0f7fa;">'
            '<span style="font-size:0.8rem;color:#90a4ae;">GoS 1%</span>'
            f'<strong style="color:#1558D6;font-family:\'JetBrains Mono\',monospace;">N = {min_n_1}</strong>'
            '</div>'
            '<div style="display:flex;justify-content:space-between;align-items:center;padding-top:8px;">'
            '<span style="font-size:0.8rem;color:#90a4ae;">GoS 0.1%</span>'
            f'<strong style="color:#1558D6;font-family:\'JetBrains Mono\',monospace;">N = {min_n_001}</strong>'
            '</div></div>',
            unsafe_allow_html=True
        )

        if not valid:
            st.markdown('<div class="eng-warn">⚠️ Pastikan S &gt; N dan A &lt; S</div>',
                        unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ██ KALKULATOR ENGSET
# ══════════════════════════════════════════════════════════════════════════════
elif active_page == "🧮  Kalkulator Engset":
    page_header("Rekayasa Trafik", "Kalkulator Engset",
                "Hitung probabilitas blocking dengan model finite source")

    # Formula wrap — SVG dan wrapper digabung dalam satu markdown call
    st.markdown(
        '<div class="formula-wrap">'
        '<span class="formula-tag">&#9889; Rumus Engset · Finite Source Model</span>'
        '<div class="eq-container">'
        + ENGSET_SVG +
        '</div></div>',
        unsafe_allow_html=True
    )

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    # Input parameter
    st.markdown(
        '<div style="font-size:0.72rem;color:#0288D1;font-weight:800;text-transform:uppercase;'
        'letter-spacing:0.12em;margin-bottom:1rem;">&#9881;&#65039; Masukkan Parameter Sistem</div>',
        unsafe_allow_html=True
    )

    col_s, col_n, col_a = st.columns(3, gap="large")
    with col_s:
        st.markdown('<div style="font-size:0.82rem;font-weight:700;color:#0a2540;margin-bottom:4px;">S &nbsp;<span style="color:#0288D1;">Jumlah Source (Pengguna)</span></div>', unsafe_allow_html=True)
        inp_S = st.number_input("S", min_value=2, max_value=200,
                                 value=st.session_state["S_calc"], step=1, label_visibility="collapsed")
    with col_n:
        st.markdown('<div style="font-size:0.82rem;font-weight:700;color:#0a2540;margin-bottom:4px;">N &nbsp;<span style="color:#0288D1;">Jumlah Kanal (Server)</span></div>', unsafe_allow_html=True)
        inp_N = st.number_input("N", min_value=1, max_value=100,
                                 value=st.session_state["N_calc"], step=1, label_visibility="collapsed")
    with col_a:
        st.markdown('<div style="font-size:0.82rem;font-weight:700;color:#0a2540;margin-bottom:4px;">A &nbsp;<span style="color:#0288D1;">Traffic Offered (Erlang)</span></div>', unsafe_allow_html=True)
        inp_A = st.number_input("A", min_value=0.1,
                                 max_value=float(max(1, inp_S - 1)),
                                 value=min(st.session_state["A_calc"], float(inp_S - 2)),
                                 step=0.1, format="%.1f", label_visibility="collapsed")

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
    if st.button("🚀  Jalankan Kalkulasi", use_container_width=True):
        st.session_state["S_calc"] = inp_S
        st.session_state["N_calc"] = inp_N
        st.session_state["A_calc"] = inp_A
        st.session_state["kalkulasi_done"] = True
        st.rerun()

    st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)

    if not valid:
        st.markdown('<div class="eng-warn">⚠️ Pastikan S lebih besar dari N dan A lebih kecil dari S.</div>',
                    unsafe_allow_html=True)
    else:
        col1, col2 = st.columns([1.2, 1], gap="large")

        with col1:
            st.markdown('<p class="sec-title">📊 Hasil Perhitungan</p>', unsafe_allow_html=True)
            rows = [
                ("📡", "Probabilitas Blocking (P)", f"{P:.8f}",       "Probabilitas"),
                ("📈", "Blocking Persen",            f"{P*100:.4f}%",  "Persentase"),
                ("🏆", "Grade Of Service",           gos_text,         "Penilaian kualitas"),
                ("✅", "Traffic Carried",            f"{carried:.4f} Erl", "Terlayani"),
                ("❌", "Traffic Lost",               f"{lost:.4f} Erl",    "Terblokir"),
                ("⚡", "Utilisasi Kanal",            f"{util_pct:.2f}%",   "Per kanal"),
                ("📶", "Traffic Intensity",          f"{A/N:.4f} Erl/ch",  "Per kanal"),
            ]
            for icon, label, val, unit in rows:
                st.markdown(
                    '<div class="plan-card" style="padding:0.9rem 1.1rem;">'
                    f'<div class="plan-icon-wrap plan-icon-blue" '
                    f'style="width:38px;height:38px;border-radius:10px;font-size:1.1rem;">{icon}</div>'
                    f'<div class="plan-info">'
                    f'<p class="plan-name" style="font-size:0.85rem;">{label}</p>'
                    f'<p class="plan-desc">{unit}</p>'
                    f'</div>'
                    f'<div class="plan-val" style="font-size:0.92rem;">{val}</div>'
                    '</div>',
                    unsafe_allow_html=True
                )

        with col2:
            st.markdown('<p class="sec-title">🎯 Rekomendasi N Minimum</p>', unsafe_allow_html=True)
            targets = [0.10, 0.05, 0.02, 0.01, 0.005, 0.001]
            rec_rows = ""
            for t in targets:
                mn = find_min_N(S, A, t)
                ok = N >= (mn if mn else 9999)
                rec_rows += (
                    f'<tr><td>{t*100:.1f}%</td>'
                    f'<td>N = {mn if mn else "&#8211;"}</td>'
                    f'<td>{"&#10003;" if ok else "&#10007;"}</td></tr>'
                )
            st.markdown(
                '<div class="card" style="padding:1.2rem;">'
                '<table class="eng-table">'
                '<thead><tr><th>Target GoS</th><th>N Minimum</th>'
                f'<th>Status N={N}</th></tr></thead>'
                f'<tbody>{rec_rows}</tbody>'
                '</table></div>',
                unsafe_allow_html=True
            )

            if P < 0.001:
                st.markdown(f'<div class="eng-ok">✅ Sangat baik · blocking hanya {P*100:.4f}%</div>',
                            unsafe_allow_html=True)
            elif P < 0.01:
                st.markdown(f'<div class="eng-ok">✅ Baik · blocking {P*100:.3f}%</div>',
                            unsafe_allow_html=True)
            elif P < 0.05:
                st.markdown('<div class="eng-warn">⚠️ Cukup · pertimbangkan tambah kanal</div>',
                            unsafe_allow_html=True)
            else:
                st.markdown('<div class="eng-warn">🔴 Buruk · tambah kanal segera!</div>',
                            unsafe_allow_html=True)

            with st.expander("🔢 Lihat Langkah Perhitungan"):
                ratio = A / (S - A)
                st.markdown(f"""
**Langkah 1 · Hitung Rasio:**
```
A / (S-A) = {A:.2f} / ({S} - {A:.2f}) = {ratio:.6f}
```
**Langkah 2 · Hitung Pembilang:**
```
C(S-1, N) x (A/(S-A))^N
= C({S-1}, {N}) x {ratio:.6f}^{N}
```
**Langkah 3 · Hitung Penyebut:**
```
sum[i=0..{N}] C({S-1}, i) x {ratio:.6f}^i
```
**Langkah 4 · Hasil Akhir:**
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
        st.markdown(
            '<div class="formula-wrap" style="margin-bottom:1.2rem;">'
            '<span class="formula-tag">Rumus Erlang</span>'
            '<div class="formula-body">'
            'A = &#955; &#215; h<br><br>'
            '&#955; = Call rate (panggilan/jam per pengguna)<br>'
            'h = Rata-rata durasi panggilan (menit)'
            '</div></div>',
            unsafe_allow_html=True
        )

        c1, c2 = st.columns(2, gap="large")
        with c1:
            call_rate  = st.number_input("&#955; · Call Rate (panggilan/jam per pengguna)",
                                         0.01, 1000.0, 3.0, 0.1, format="%.2f")
            hold_time  = st.number_input("h · Hold Time Rata-rata (menit)",
                                         0.1, 120.0, 2.0, 0.1, format="%.1f")
            n_users_t1 = st.number_input("Jumlah Pengguna Aktif (opsional untuk A total)",
                                         1, 10000, S)

        with c2:
            lam_s = call_rate / 3600
            h_s   = hold_time * 60
            A_1   = lam_s * h_s
            A_tot = A_1 * n_users_t1

            st.markdown(
                '<div class="card">'
                '<div style="font-size:0.85rem;font-weight:800;color:#0a2540;margin-bottom:1rem;">'
                '📊 Hasil Perhitungan</div>'
                '<div style="display:flex;justify-content:space-between;align-items:center;'
                'padding:9px 0;border-bottom:1px solid #e0f7fa;">'
                '<span style="font-size:0.82rem;color:#90a4ae;">Traffic Per Pengguna</span>'
                f'<span style="font-family:\'JetBrains Mono\';font-weight:700;color:#0288D1;">'
                f'{A_1:.6f} Erl</span></div>'
                '<div style="display:flex;justify-content:space-between;align-items:center;'
                'padding:9px 0;border-bottom:1px solid #e0f7fa;">'
                '<span style="font-size:0.82rem;color:#90a4ae;">&#955; (Konversi ke /detik)</span>'
                f'<span style="font-family:\'JetBrains Mono\';font-weight:700;color:#0a2540;">'
                f'{lam_s:.6f} call/s</span></div>'
                '<div style="display:flex;justify-content:space-between;align-items:center;'
                'padding:9px 0;border-bottom:1px solid #e0f7fa;">'
                '<span style="font-size:0.82rem;color:#90a4ae;">h (Konversi ke detik)</span>'
                f'<span style="font-family:\'JetBrains Mono\';font-weight:700;color:#0a2540;">'
                f'{h_s:.0f} detik</span></div>'
                '<div style="margin-top:1rem;background:linear-gradient(135deg,#e0f7fa,#e3f2fd);'
                'border-radius:14px;padding:1.2rem;text-align:center;">'
                '<div style="font-size:0.7rem;color:#006064;text-transform:uppercase;'
                f'letter-spacing:0.1em;margin-bottom:6px;font-weight:800;">A Total ({n_users_t1} pengguna)</div>'
                f'<div style="font-size:2.2rem;font-weight:900;color:#1558D6;'
                f'font-family:\'JetBrains Mono\';">{A_tot:.4f} Erl</div>'
                '<div style="font-size:0.78rem;color:#006064;margin-top:6px;">'
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
                        f'A={A_tot:.4f}, S={S}, N={N}:<br>'
                        f'P = {P2:.6f} &#183; Blocking = {P2*100:.3f}% &#183; GoS = {g2}</div>',
                        unsafe_allow_html=True
                    )

    with tab2:
        st.markdown(
            '<div class="formula-wrap" style="margin-bottom:1.2rem;">'
            '<span class="formula-tag">Rumus BHT</span>'
            '<div class="formula-body">'
            'A = U &#215; BHT<br><br>'
            'U   = Jumlah pengguna aktif di jam sibuk<br>'
            'BHT = Busy Hour Traffic per pengguna (Erlang)'
            '</div></div>',
            unsafe_allow_html=True
        )

        c1, c2 = st.columns(2, gap="large")
        with c1:
            U_val = st.number_input("U · Pengguna Aktif Jam Sibuk", 1, 10000, 50)
            BHT   = st.number_input("BHT · Busy Hour Traffic Per User (Erl)",
                                    0.001, 1.0, 0.1, 0.001, format="%.3f")
        with c2:
            A_t2 = U_val * BHT
            st.markdown(
                '<div class="card" style="text-align:center;padding:1.8rem;">'
                f'<div style="font-size:0.8rem;color:#90a4ae;margin-bottom:8px;'
                f'font-family:\'JetBrains Mono\';">A = {U_val} &#215; {BHT:.3f}</div>'
                f'<div style="font-size:2.6rem;font-weight:900;color:#0288D1;'
                f'font-family:\'JetBrains Mono\';">{A_t2:.4f}</div>'
                '<div style="font-size:0.84rem;color:#90a4ae;margin-top:6px;font-weight:600;">Erlang</div>'
                '</div>',
                unsafe_allow_html=True
            )
            if 0 < A_t2 < S and S > N:
                P3 = engset(S, N, A_t2)
                if P3:
                    g3, gc3 = gos_label(P3)
                    cls = "eng-ok" if P3 < 0.01 else "eng-warn"
                    st.markdown(
                        f'<div class="{cls}">P = {P3:.6f} &#183; '
                        f'Blocking = {P3*100:.3f}% &#183; GoS = {g3}</div>',
                        unsafe_allow_html=True
                    )

    with tab3:
        st.markdown(
            '<div class="formula-wrap" style="margin-bottom:1.2rem;">'
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
                '<div class="card" style="text-align:center;padding:1.8rem;">'
                f'<div style="font-size:0.8rem;color:#90a4ae;margin-bottom:8px;'
                f'font-family:\'JetBrains Mono\';">A = {dr:.1f} / {cc:.1f}</div>'
                f'<div style="font-size:2.6rem;font-weight:900;color:#0288D1;'
                f'font-family:\'JetBrains Mono\';">{A_t3:.4f}</div>'
                '<div style="font-size:0.84rem;color:#90a4ae;margin-top:6px;font-weight:600;">Erlang</div>'
                '</div>',
                unsafe_allow_html=True
            )
            if 0 < A_t3 < S and S > N:
                P4 = engset(S, N, A_t3)
                if P4:
                    g4, gc4 = gos_label(P4)
                    cls = "eng-ok" if P4 < 0.01 else "eng-warn"
                    st.markdown(
                        f'<div class="{cls}">P = {P4:.6f} &#183; '
                        f'Blocking = {P4*100:.3f}% &#183; GoS = {g4}</div>',
                        unsafe_allow_html=True
                    )


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
            st.markdown('<div style="font-size:0.95rem;font-weight:800;color:#0a2540;margin-bottom:0.5rem;">📈 Blocking Vs Jumlah Kanal (N)</div>', unsafe_allow_html=True)
            max_n = min(S - 1, 50)
            ns_   = list(range(1, max_n + 1))
            ps_   = [(engset(S, n, A) or 0) * 100 for n in ns_]

            fig1, ax1 = plt.subplots(figsize=(5.5, 3.8))
            fig1.patch.set_facecolor(BG); ax1.set_facecolor(BG)
            ax1.fill_between(ns_, ps_, alpha=0.15, color=BLUE)
            ax1.plot(ns_, ps_, color=BLUE, linewidth=2.5, zorder=3)
            ax1.scatter([N], [P*100], color=RED, s=100, zorder=5,
                        label=f'N={N}, P={P*100:.3f}%')
            ax1.axhline(1.0, color=AMBER, linestyle='--', linewidth=1.2, alpha=0.8)
            ax1.text(max_n*0.97, 1.05, 'GoS 1%', ha='right', fontsize=8, color=AMBER)
            ax1.axhline(0.1, color=GREEN, linestyle='--', linewidth=1.2, alpha=0.8)
            ax1.text(max_n*0.97, 0.15, 'GoS 0.1%', ha='right', fontsize=8, color=GREEN)
            ax1.set_xlabel('N (Jumlah Kanal)', fontsize=9, color='#78909c')
            ax1.set_ylabel('Blocking (%)', fontsize=9, color='#78909c')
            ax1.set_title(f'S={S}, A={A:.1f} Erl', fontsize=9, color='#90a4ae')
            ax1.legend(fontsize=8.5)
            ax1.grid(True, linestyle='--', alpha=0.2)
            ax1.spines[['top', 'right']].set_visible(False)
            ax1.tick_params(colors='#90a4ae', labelsize=8)
            plt.tight_layout(pad=1.0)
            st.pyplot(fig1, use_container_width=True)
            plt.close(fig1)

        with cg2:
            st.markdown('<div style="font-size:0.95rem;font-weight:800;color:#0a2540;margin-bottom:0.5rem;">📉 Blocking Vs Traffic Offered (A)</div>', unsafe_allow_html=True)
            a_max_ = min(float(S - 1), 30.0)
            av_    = np.linspace(0.1, a_max_, 300)
            pv_    = [(engset(S, N, float(a)) or 0) * 100 for a in av_]

            fig2, ax2 = plt.subplots(figsize=(5.5, 3.8))
            fig2.patch.set_facecolor(BG); ax2.set_facecolor(BG)
            ax2.fill_between(av_, pv_, alpha=0.15, color=TEAL)
            ax2.plot(av_, pv_, color=TEAL, linewidth=2.5, zorder=3)
            ax2.scatter([A], [P*100], color=RED, s=100, zorder=5,
                        label=f'A={A:.1f}, P={P*100:.3f}%')
            ax2.axhline(1.0, color=AMBER, linestyle='--', linewidth=1.2, alpha=0.8)
            ax2.text(a_max_*0.97, 1.05, 'GoS 1%', ha='right', fontsize=8, color=AMBER)
            ax2.set_xlabel('A (Traffic Offered, Erlang)', fontsize=9, color='#78909c')
            ax2.set_ylabel('Blocking (%)', fontsize=9, color='#78909c')
            ax2.set_title(f'S={S}, N={N} Kanal', fontsize=9, color='#90a4ae')
            ax2.legend(fontsize=8.5)
            ax2.grid(True, linestyle='--', alpha=0.2)
            ax2.spines[['top', 'right']].set_visible(False)
            ax2.tick_params(colors='#90a4ae', labelsize=8)
            plt.tight_layout(pad=1.0)
            st.pyplot(fig2, use_container_width=True)
            plt.close(fig2)

        st.markdown('<div style="font-size:0.95rem;font-weight:800;color:#0a2540;margin:1.2rem 0 0.5rem;">🌐 Multi-Kurva: Blocking Vs N Untuk Berbagai Nilai A</div>', unsafe_allow_html=True)
        palette = [BLUE, TEAL, GREEN, AMBER, RED, '#8B5CF6']
        a_list  = [round(A * m, 2) for m in [0.5, 0.75, 1.0, 1.25, 1.5, 2.0] if 0 < A * m < S][:6]
        max_n3  = min(S - 1, 35)
        ns3_    = list(range(1, max_n3 + 1))

        fig3, ax3 = plt.subplots(figsize=(11, 4))
        fig3.patch.set_facecolor(BG); ax3.set_facecolor(BG)
        for idx, a_c in enumerate(a_list):
            ps3 = [(engset(S, n, a_c) or 0) * 100 for n in ns3_]
            ax3.plot(ns3_, ps3, color=palette[idx % len(palette)],
                     linewidth=2.2, label=f'A={a_c:.1f} Erl')
        ax3.axvline(N, color='#90a4ae', linestyle=':', linewidth=2,
                    label=f'N Aktif = {N}')
        ax3.axhline(1.0, color=AMBER, linestyle='--', linewidth=1, alpha=0.6)
        ax3.set_xlabel('N (Jumlah Kanal)', fontsize=9, color='#78909c')
        ax3.set_ylabel('Blocking (%)', fontsize=9, color='#78909c')
        ax3.set_title(f'Perbandingan Blocking Vs N Untuk Berbagai A (S={S})',
                      fontsize=10, color='#0a2540', fontweight='bold')
        ax3.legend(fontsize=8.5, ncol=min(len(a_list) + 1, 4))
        ax3.grid(True, linestyle='--', alpha=0.2)
        ax3.spines[['top', 'right']].set_visible(False)
        ax3.tick_params(colors='#90a4ae', labelsize=8)
        plt.tight_layout(pad=1.0)
        st.pyplot(fig3, use_container_width=True)
        plt.close(fig3)

        st.markdown('<div style="font-size:0.95rem;font-weight:800;color:#0a2540;margin:1.2rem 0 0.5rem;">📋 Tabel Detail Blocking Vs N</div>', unsafe_allow_html=True)
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
            f'<div class="eng-info" style="margin-top:10px;font-size:0.78rem;">'
            f'&#128309; Baris biru = nilai N yang dipilih saat ini (N={N})</div>',
            unsafe_allow_html=True
        )


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
            st.markdown('<div style="font-size:0.92rem;font-weight:800;color:#0a2540;margin-bottom:1.2rem;">📄 Preview Isi Laporan</div>',
                        unsafe_allow_html=True)
            items_prev = [
                ("📌", "Judul",           "EngsetPro · Laporan Perhitungan Engset"),
                ("📅", "Tanggal",         datetime.now().strftime('%d %B %Y, %H:%M')),
                ("🔢", "Parameter",       f"S={S}, N={N}, A={A:.1f} Erl"),
                ("📡", "P Blocking",      f"{P:.8f}"),
                ("📊", "Blocking %",      f"{P*100:.4f}%"),
                ("🏆", "GoS",             gos_text),
                ("✅", "Traffic Carried", f"{carried:.4f} Erlang"),
                ("❌", "Traffic Lost",    f"{lost:.4f} Erlang"),
                ("📈", "Grafik",          "Blocking Vs N + Blocking Vs A"),
                ("📋", "Tabel",           "Detail N dari 1 sampai N+10"),
            ]
            for icon, label, val in items_prev:
                st.markdown(
                    '<div style="display:flex;justify-content:space-between;align-items:center;'
                    'padding:9px 0;border-bottom:1px solid rgba(2,136,209,0.06);">'
                    f'<span style="font-size:0.82rem;color:#90a4ae;">{icon} {label}</span>'
                    f'<span style="font-size:0.82rem;font-weight:700;color:#0a2540;'
                    f'font-family:\'JetBrains Mono\',monospace;text-align:right;max-width:55%;">{val}</span>'
                    '</div>',
                    unsafe_allow_html=True
                )

        with c_act:
            st.markdown(
                '<div style="text-align:center;padding:1.5rem 1rem;">'
                '<div style="font-size:3rem;margin-bottom:0.8rem;">📄</div>'
                '<div style="font-size:1rem;font-weight:800;color:#0a2540;margin-bottom:0.5rem;">'
                'Laporan PDF Profesional</div>'
                '<div style="font-size:0.82rem;color:#90a4ae;margin-bottom:1rem;line-height:1.7;">'
                'Berisi parameter, hasil perhitungan,<br>grafik analisis, dan tabel detail.'
                '</div></div>',
                unsafe_allow_html=True
            )

            if st.button("⬇️  Generate Dan Download PDF", use_container_width=True):
                with st.spinner("Membuat laporan PDF..."):
                    def cb(fig):
                        buf = io.BytesIO()
                        fig.savefig(buf, format='png', dpi=150, bbox_inches='tight',
                                    facecolor='white')
                        buf.seek(0); return buf.read()

                    max_n_ = min(S - 1, 40)
                    ns__   = list(range(1, max_n_ + 1))
                    ps__   = [(engset(S, n, A) or 0) * 100 for n in ns__]
                    f1, a1 = plt.subplots(figsize=(7, 3.5))
                    f1.patch.set_facecolor('white'); a1.set_facecolor('white')
                    a1.fill_between(ns__, ps__, alpha=0.12, color='#1558D6')
                    a1.plot(ns__, ps__, color='#1558D6', linewidth=2.2)
                    a1.scatter([N], [P*100], color='#ef4444', s=60, zorder=5)
                    a1.axhline(1.0, color='#f59e0b', linestyle='--', linewidth=1)
                    a1.set_xlabel('N (Jumlah Kanal)', fontsize=9)
                    a1.set_ylabel('Blocking (%)', fontsize=9)
                    a1.set_title(f'Blocking Vs N  |  S={S}, A={A:.1f} Erl',
                                 fontsize=10, fontweight='bold', color='#0a2540')
                    a1.grid(True, linestyle='--', alpha=0.2, color='#e0f7fa')
                    a1.spines[['top', 'right']].set_visible(False)
                    plt.tight_layout(); c1_bytes = cb(f1); plt.close(f1)

                    am_ = min(float(S - 1), 25.0)
                    av_ = np.linspace(0.1, am_, 200)
                    pv_ = [(engset(S, N, float(a)) or 0) * 100 for a in av_]
                    f2, a2 = plt.subplots(figsize=(7, 3.5))
                    f2.patch.set_facecolor('white'); a2.set_facecolor('white')
                    a2.fill_between(av_, pv_, alpha=0.12, color='#0CA8D4')
                    a2.plot(av_, pv_, color='#0CA8D4', linewidth=2.2)
                    a2.scatter([A], [P*100], color='#ef4444', s=60, zorder=5)
                    a2.axhline(1.0, color='#f59e0b', linestyle='--', linewidth=1)
                    a2.set_xlabel('A (Erlang)', fontsize=9)
                    a2.set_ylabel('Blocking (%)', fontsize=9)
                    a2.set_title(f'Blocking Vs A  |  S={S}, N={N}',
                                 fontsize=10, fontweight='bold', color='#0a2540')
                    a2.grid(True, linestyle='--', alpha=0.2, color='#e0f7fa')
                    a2.spines[['top', 'right']].set_visible(False)
                    plt.tight_layout(); c2_bytes = cb(f2); plt.close(f2)

                    buf_pdf = io.BytesIO()
                    doc = SimpleDocTemplate(buf_pdf, pagesize=A4,
                        leftMargin=2.5*cm, rightMargin=2.5*cm,
                        topMargin=2.5*cm, bottomMargin=2.5*cm)

                    BLACK     = colors.HexColor('#0a2540')
                    DARK      = colors.HexColor('#37474f')
                    MID_GRAY  = colors.HexColor('#78909c')
                    LIGHT_BG  = colors.HexColor('#F2F6FF')
                    BORDER    = colors.HexColor('#B3CEFF')
                    HDR_BG    = colors.HexColor('#1558D6')
                    ALT_ROW   = colors.HexColor('#EEF2FF')

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
                                         textColor=DARK, backColor=LIGHT_BG,
                                         leftIndent=12, rightIndent=12,
                                         spaceBefore=6, spaceAfter=6, leading=16,
                                         borderPadding=8)
                    FC  = ParagraphStyle('FC', fontSize=8,
                                         textColor=colors.HexColor('#90a4ae'),
                                         alignment=TA_CENTER)

                    el = []
                    el.append(Paragraph("EngsetPro", T))
                    el.append(Paragraph(
                        f"Laporan Analisis Engset &nbsp;|&nbsp; {datetime.now().strftime('%d %B %Y, %H:%M')}", Sub))
                    el.append(HRFlowable(width="100%", thickness=1.5, color=HDR_BG, spaceAfter=16))

                    el.append(Paragraph("1. Parameter Input", H2))
                    pd2 = [["Parameter", "Simbol", "Nilai", "Satuan"],
                            ["Jumlah Source", "S", str(S), "Pengguna"],
                            ["Jumlah Kanal", "N", str(N), "Kanal"],
                            ["Traffic Offered", "A", f"{A:.1f}", "Erlang"]]
                    pt = Table(pd2, colWidths=[6*cm, 2.5*cm, 3*cm, 3.5*cm])
                    pt.setStyle(TableStyle([
                        ('BACKGROUND', (0,0), (-1,0), HDR_BG),
                        ('TEXTCOLOR',  (0,0), (-1,0), colors.white),
                        ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
                        ('FONTNAME',   (0,1), (-1,-1), 'Helvetica'),
                        ('FONTSIZE',   (0,0), (-1,-1), 9),
                        ('ALIGN',      (0,0), (-1,-1), 'CENTER'),
                        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, ALT_ROW]),
                        ('GRID',       (0,0), (-1,-1), 0.5, BORDER),
                        ('TOPPADDING',    (0,0), (-1,-1), 7),
                        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
                        ('LEFTPADDING',   (0,0), (-1,-1), 10),
                        ('RIGHTPADDING',  (0,0), (-1,-1), 10),
                    ]))
                    el.append(pt)
                    el.append(Spacer(1, 12))

                    el.append(Paragraph("2. Hasil Perhitungan", H2))
                    rd2 = [["Metrik", "Nilai", "Keterangan"],
                            ["Probabilitas Blocking (P)", f"{P:.8f}", "Nilai probabilitas blocking"],
                            ["Blocking (%)", f"{P*100:.4f}%", "Persentase trafik terblokir"],
                            ["Grade Of Service", gos_text, "Kualitas layanan sistem"],
                            ["Traffic Carried", f"{carried:.4f} Erl", "Trafik yang berhasil dilayani"],
                            ["Traffic Lost", f"{lost:.4f} Erl", "Trafik yang terblokir"],
                            ["Utilisasi Kanal", f"{util_pct:.2f}%", "Utilisasi rata-rata per kanal"]]
                    rt = Table(rd2, colWidths=[5.5*cm, 3.5*cm, 6*cm])
                    rt.setStyle(TableStyle([
                        ('BACKGROUND', (0,0), (-1,0), HDR_BG),
                        ('TEXTCOLOR',  (0,0), (-1,0), colors.white),
                        ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
                        ('FONTNAME',   (0,1), (-1,-1), 'Helvetica'),
                        ('FONTSIZE',   (0,0), (-1,-1), 9),
                        ('ALIGN',      (1,0), (1,-1), 'CENTER'),
                        ('ALIGN',      (0,0), (0,-1), 'LEFT'),
                        ('ALIGN',      (2,0), (2,-1), 'LEFT'),
                        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, ALT_ROW]),
                        ('GRID',       (0,0), (-1,-1), 0.5, BORDER),
                        ('TOPPADDING',    (0,0), (-1,-1), 7),
                        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
                        ('LEFTPADDING',   (0,0), (-1,-1), 10),
                        ('RIGHTPADDING',  (0,0), (-1,-1), 10),
                    ]))
                    el.append(rt)
                    el.append(Spacer(1, 16))

                    el.append(Paragraph("3. Grafik Analisis", H2))
                    el.append(Paragraph(
                        f"Grafik berikut menunjukkan pengaruh perubahan jumlah kanal (N) "
                        f"dan traffic offered (A) terhadap probabilitas blocking (S={S}).", B))
                    el.append(Spacer(1, 6))
                    el.append(RLImage(io.BytesIO(c1_bytes), width=15*cm, height=7*cm))
                    el.append(Spacer(1, 8))
                    el.append(RLImage(io.BytesIO(c2_bytes), width=15*cm, height=7*cm))
                    el.append(Spacer(1, 16))

                    el.append(HRFlowable(width="100%", thickness=0.5, color=BORDER, spaceAfter=8))
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
st.markdown(
    '<div style="text-align:center;color:#A8C4FF;font-size:0.78rem;'
    'padding:2.5rem 0 1.5rem;font-weight:500;letter-spacing:0.04em;">'
    'EngsetPro v2.0 &nbsp;&#183;&nbsp; Kalkulator Rekayasa Trafik Engset &nbsp;&#183;&nbsp; '
    'Metode: Log-space Arithmetic'
    '</div>',
    unsafe_allow_html=True
)
