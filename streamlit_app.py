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
        Table, TableStyle, HRFlowable, PageBreak,
        KeepTogether, Image as RLImage
    )
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import cm, mm
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
    from reportlab.platypus.flowables import HRFlowable
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
    initial_sidebar_state="collapsed",   # collapsed by default → mobile friendly
)

# ═══════════════════════════════════════════════════════════════════════════════
# GLOBAL CSS
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
  --blue-primary: #1a56ff;
  --blue-dark:    #0e3acc;
  --blue-deeper:  #0a2aaa;
  --teal:         #00c8b4;
  --teal-light:   #4dd9cb;
  --green:        #22c55e;
  --amber:        #f59e0b;
  --red:          #ef4444;
  --bg:           #f2f5fc;
  --white:        #ffffff;
  --navy:         #0d1b3e;
  --slate:        #3a5098;
  --muted:        #8899bb;
  --border:       rgba(26,86,255,0.08);
  --shadow-sm:    0 2px 12px rgba(26,86,255,0.07);
  --shadow-md:    0 6px 24px rgba(26,86,255,0.12);
  --shadow-lg:    0 12px 40px rgba(26,86,255,0.20);
  --radius-sm:    12px;
  --radius-md:    18px;
  --radius-lg:    24px;
}

html, body, [class*="css"] {
  font-family: 'Sora', sans-serif !important;
}

/* ── viewport meta for mobile ── */
head::before {
  display: none;
  content: '<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">';
}

.stApp {
  background: var(--bg) !important;
}

#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ═══════════ SIDEBAR ═══════════ */
[data-testid="stSidebar"] {
  background: linear-gradient(175deg, #1246e8 0%, #0c35c0 45%, #072590 100%) !important;
  border-right: none !important;
  box-shadow: 6px 0 30px rgba(10,42,170,0.30);
  min-width: 260px !important;
  max-width: 310px !important;
}
[data-testid="stSidebar"] > div:first-child { padding-top: 0 !important; }
[data-testid="stSidebar"] * { color: rgba(255,255,255,0.9) !important; }
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stNumberInput label {
  color: rgba(255,255,255,0.65) !important;
  font-size: 0.72rem !important;
  letter-spacing: 0.07em;
  text-transform: uppercase;
}
[data-testid="stSidebar"] hr {
  border-color: rgba(255,255,255,0.12) !important;
}

/* Radio nav items */
[data-testid="stSidebar"] [data-testid="stRadio"] > div {
  gap: 4px !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label {
  border-radius: 12px !important;
  padding: 10px 14px !important;
  transition: background 0.2s ease !important;
  font-size: 0.88rem !important;
  font-weight: 500 !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
  background: rgba(255,255,255,0.12) !important;
}

/* Group labels in sidebar */
.nav-group-label {
  font-size: 0.65rem;
  font-weight: 700;
  color: rgba(255,255,255,0.4) !important;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  margin: 16px 0 6px 6px;
}

/* ═══════════ BASE CARDS ═══════════ */
.card {
  background: var(--white);
  border-radius: var(--radius-md);
  padding: 1.4rem 1.6rem;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border);
  margin-bottom: 1rem;
}

.card-sm {
  background: var(--white);
  border-radius: var(--radius-sm);
  padding: 1rem 1.2rem;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border);
  margin-bottom: 0.75rem;
}

/* ═══════════ HERO GRADIENT CARD ═══════════ */
.hero-card {
  background: linear-gradient(135deg, #1a56ff 0%, #0a8fe8 55%, #00c8b4 100%);
  border-radius: var(--radius-lg);
  padding: 2rem 2rem 1.8rem;
  color: white;
  margin-bottom: 1rem;
  position: relative;
  overflow: hidden;
  box-shadow: 0 10px 40px rgba(26,86,255,0.40);
}
.hero-card::before {
  content: "";
  position: absolute; top: -80px; right: -50px;
  width: 260px; height: 260px; border-radius: 50%;
  background: rgba(255,255,255,0.07);
}
.hero-card::after {
  content: "";
  position: absolute; bottom: -60px; left: 35%;
  width: 200px; height: 200px; border-radius: 50%;
  background: rgba(255,255,255,0.05);
}
.hero-badge {
  display: inline-flex; align-items: center; gap: 6px;
  background: rgba(255,255,255,0.18);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255,255,255,0.25);
  border-radius: 100px;
  padding: 4px 14px;
  font-size: 0.7rem; font-weight: 700;
  letter-spacing: 0.1em; text-transform: uppercase;
  margin-bottom: 1rem;
  color: #fff;
}
.hero-stat-pill {
  background: rgba(255,255,255,0.16);
  backdrop-filter: blur(6px);
  border: 1px solid rgba(255,255,255,0.2);
  border-radius: 14px; padding: 10px 20px;
}

/* ═══════════ METRIC CHIPS ═══════════ */
.chip-grid {
  display: grid; grid-template-columns: repeat(3, 1fr);
  gap: 10px; margin-bottom: 1rem;
}
@media (max-width: 640px) {
  .chip-grid { grid-template-columns: repeat(2, 1fr); }
  .hero-card { padding: 1.2rem 1rem 1rem; }
  .hero-stat-pill { padding: 7px 12px; }
}
.chip {
  background: var(--white);
  border-radius: var(--radius-sm);
  padding: 1.1rem 0.8rem;
  text-align: center;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border);
  position: relative; overflow: hidden;
}
.chip::before {
  content: "";
  position: absolute; top: 0; left: 0; right: 0; height: 3px;
  background: linear-gradient(90deg, var(--blue-primary), var(--teal));
  border-radius: 3px 3px 0 0;
}
.chip-icon { font-size: 1.2rem; margin-bottom: 6px; }
.chip-val  {
  font-size: 1.05rem; font-weight: 700; color: var(--navy);
  font-family: 'JetBrains Mono', monospace;
}
.chip-lbl  {
  font-size: 0.65rem; color: var(--muted);
  text-transform: uppercase; letter-spacing: 0.07em; margin-top: 3px;
}

/* ═══════════ PLAN / RESULT ROWS ═══════════ */
.plan-card {
  background: var(--white);
  border-radius: var(--radius-sm);
  padding: 0.95rem 1.2rem;
  display: flex; align-items: center; gap: 14px;
  margin-bottom: 8px;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border);
  transition: box-shadow 0.2s, transform 0.2s;
}
.plan-card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-1px);
}
.plan-icon-wrap {
  width: 44px; height: 44px; border-radius: 13px;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.2rem; flex-shrink: 0;
}
.plan-icon-blue  { background: rgba(26,86,255,0.10); }
.plan-icon-teal  { background: rgba(0,200,180,0.10); }
.plan-icon-green { background: rgba(34,197,94,0.10); }
.plan-icon-amber { background: rgba(245,158,11,0.10); }
.plan-icon-red   { background: rgba(239,68,68,0.10); }
.plan-info { flex: 1; }
.plan-name { font-size: 0.88rem; font-weight: 600; color: var(--navy); margin: 0; }
.plan-desc { font-size: 0.75rem; color: var(--muted); margin: 2px 0 0; }
.plan-val  {
  font-size: 0.95rem; font-weight: 700; color: var(--blue-primary);
  font-family: 'JetBrains Mono', monospace;
}

/* ═══════════ GoS BADGE ═══════════ */
.gos {
  display: inline-block; padding: 4px 14px; border-radius: 100px;
  font-size: 0.75rem; font-weight: 700; letter-spacing: 0.04em;
}
.gos-great { background: #dcfce7; color: #166534; }
.gos-good  { background: #d1fae5; color: #065f46; }
.gos-ok    { background: #fef9c3; color: #713f12; }
.gos-bad   { background: #fee2e2; color: #7f1d1d; }

/* ═══════════ FORMULA BLOCK ═══════════ */
.formula-wrap {
  background: linear-gradient(135deg, #eef3ff 0%, #e4edff 100%);
  border: 1.5px solid #c7d7ff;
  border-radius: var(--radius-md);
  padding: 1.6rem 1.8rem; margin-bottom: 1rem;
}
.formula-tag {
  display: inline-block; background: var(--blue-primary); color: #fff;
  font-size: 0.65rem; font-weight: 700; letter-spacing: 0.1em;
  text-transform: uppercase; padding: 3px 12px; border-radius: 100px; margin-bottom: 1rem;
}
.formula-body {
  font-family: 'JetBrains Mono', monospace; font-size: 0.88rem;
  color: #0d2060; line-height: 2.4;
  background: rgba(255,255,255,0.65); border-radius: 10px;
  padding: 1.2rem 1.6rem;
  overflow-x: auto;
  white-space: pre;
}
.formula-legend { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-top: 1rem; }
@media (max-width: 480px) { .formula-legend { grid-template-columns: 1fr; } }
.fl-item { font-size: 0.78rem; color: var(--slate); display: flex; align-items: baseline; gap: 8px; }
.fl-sym  { font-family: 'JetBrains Mono', monospace; font-weight: 700; color: var(--blue-primary); min-width: 22px; }

/* ═══════════ SECTION TITLE ═══════════ */
.sec-title {
  font-size: 1rem; font-weight: 700; color: var(--navy); margin: 0 0 0.8rem;
  display: flex; align-items: center; gap: 6px;
}

/* ═══════════ ALERT BANNERS ═══════════ */
.eng-warn {
  background: #fff7ed; border: 1px solid #fed7aa;
  border-left: 4px solid #f59e0b;
  border-radius: var(--radius-sm); padding: 0.85rem 1.1rem;
  color: #92400e; font-size: 0.85rem; margin-bottom: 1rem;
}
.eng-info {
  background: #eff6ff; border: 1px solid #bfdbfe;
  border-left: 4px solid var(--blue-primary);
  border-radius: var(--radius-sm); padding: 0.85rem 1.1rem;
  color: #1e40af; font-size: 0.85rem; margin-bottom: 1rem;
}
.eng-ok {
  background: #f0fdf4; border: 1px solid #bbf7d0;
  border-left: 4px solid var(--green);
  border-radius: var(--radius-sm); padding: 0.85rem 1.1rem;
  color: #166534; font-size: 0.85rem; margin-bottom: 1rem;
}

/* ═══════════ TABLE ═══════════ */
.eng-table {
  width: 100%; border-collapse: collapse; font-size: 0.83rem;
  border-radius: var(--radius-sm); overflow: hidden;
}
.eng-table th {
  background: linear-gradient(90deg, var(--blue-primary), var(--blue-dark));
  color: #fff; font-size: 0.68rem;
  text-transform: uppercase; letter-spacing: 0.08em;
  padding: 10px 14px; text-align: left; font-weight: 600;
}
.eng-table td {
  padding: 9px 14px; border-bottom: 1px solid #f0f4ff;
  color: #2d3a5e; font-family: 'JetBrains Mono', monospace; font-size: 0.8rem;
}
.eng-table tr:hover td { background: #f5f8ff; }
.eng-table tr.active td { background: #eff6ff; font-weight: 600; color: var(--navy); }

/* ═══════════ BUTTONS ═══════════ */
.stButton > button {
  background: linear-gradient(135deg, #1a56ff, #0e3acc) !important;
  color: #fff !important; border: none !important;
  border-radius: var(--radius-sm) !important;
  padding: 0.65rem 1.6rem !important; font-weight: 700 !important;
  font-size: 0.88rem !important;
  box-shadow: 0 4px 16px rgba(26,86,255,0.3) !important;
  transition: all 0.2s ease !important;
  font-family: 'Sora', sans-serif !important;
}
.stButton > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 24px rgba(26,86,255,0.4) !important;
}

/* ═══════════ PROGRESS BAR ═══════════ */
.progress-wrap {
  background: #e8efff; border-radius: 100px; height: 8px;
  margin: 6px 0; overflow: hidden;
}
.progress-fill {
  height: 100%; border-radius: 100px;
  background: linear-gradient(90deg, var(--blue-primary), var(--teal));
  transition: width 0.5s ease;
}

/* ═══════════ TABS ═══════════ */
.stTabs [data-baseweb="tab-list"] {
  background: #edf1fb; border-radius: 14px; padding: 4px; gap: 4px; border: none;
  flex-wrap: wrap;
}
.stTabs [data-baseweb="tab"] {
  border-radius: 10px; font-weight: 600; font-size: 0.86rem;
  color: var(--muted); padding: 8px 20px;
  font-family: 'Sora', sans-serif;
}
.stTabs [aria-selected="true"] {
  background: var(--white) !important; color: var(--blue-primary) !important;
  box-shadow: 0 2px 10px rgba(26,86,255,0.14) !important;
}

/* ═══════════ PAGE HEADER ═══════════ */
.page-header {
  margin-bottom: 1.6rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #eaeffe;
}
.page-header-tag {
  font-size: 0.68rem; color: var(--blue-primary); font-weight: 700;
  text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 4px;
}
.page-header-title {
  font-size: 1.75rem; font-weight: 800; color: var(--navy); margin: 0;
  letter-spacing: -0.02em;
}
.page-header-sub {
  color: var(--muted); margin: 4px 0 0; font-size: 0.88rem;
}

/* ═══════════ STAT RESULT BOX ═══════════ */
.result-hero {
  background: linear-gradient(135deg, #eef3ff, #e4edff);
  border: 1.5px solid #c7d7ff;
  border-radius: var(--radius-md);
  padding: 1.4rem; text-align: center; margin-bottom: 1rem;
}
.result-hero-label {
  font-size: 0.7rem; color: var(--slate); text-transform: uppercase;
  letter-spacing: 0.08em; margin-bottom: 6px;
}
.result-hero-val {
  font-size: 2.4rem; font-weight: 800; color: var(--blue-primary);
  font-family: 'JetBrains Mono', monospace; line-height: 1;
}
.result-hero-unit {
  font-size: 0.82rem; color: var(--muted); margin-top: 6px;
}

/* ═══════════ DATA ROW ═══════════ */
.data-row {
  display: flex; justify-content: space-between; align-items: center;
  padding: 10px 0; border-bottom: 1px solid #f0f4ff;
  flex-wrap: wrap; gap: 4px;
}
.data-row:last-child { border-bottom: none; }
.data-row-label { font-size: 0.82rem; color: var(--muted); }
.data-row-val {
  font-size: 0.85rem; font-weight: 700; color: var(--navy);
  font-family: 'JetBrains Mono', monospace;
}

/* ═══════════ MOBILE RESPONSIVE FIXES ═══════════ */
@media (max-width: 768px) {
  .page-header-title { font-size: 1.3rem !important; }
  .result-hero-val   { font-size: 1.8rem !important; }
  .plan-card         { flex-wrap: wrap; }
  .eng-table         { font-size: 0.72rem; }
  .eng-table th, .eng-table td { padding: 7px 8px; }
  .formula-body      { font-size: 0.75rem; padding: 0.9rem 1rem; }
  [data-testid="stSidebar"] {
    min-width: 80vw !important;
    max-width: 90vw !important;
  }
}
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# CORE ENGSET — Numerik stabil menggunakan log-space arithmetic
# ═══════════════════════════════════════════════════════════════════════════════
def log_faktorial(n):
    """Menghitung ln(n!) secara iteratif."""
    if n <= 1:
        return 0.0
    return sum(log(i) for i in range(2, n + 1))

def log_kombinasi(n, k):
    """Menghitung ln C(n,k) = ln(n!) − ln(k!) − ln((n−k)!)."""
    if k < 0 or k > n:
        return float('-inf')
    return log_faktorial(n) - log_faktorial(k) - log_faktorial(n - k)

def engset(S, N, A):
    """
    Menghitung probabilitas blocking Engset.

    Rumus (bentuk rekursif log-space):
        P(S, N, A) = C(S-1, N) · ρ^N  /  Σ[i=0..N] C(S-1, i) · ρ^i
    di mana ρ = A / (S − A) adalah rasio intensitas trafik.

    Parameter
    ----------
    S : int   — jumlah sumber (source / pengguna)
    N : int   — jumlah kanal (server)
    A : float — trafik yang ditawarkan (Erlang)

    Kembalian
    ---------
    float : probabilitas blocking [0, 1], atau None jika parameter tidak valid.
    """
    if A <= 0 or A >= S or N <= 0 or S <= N:
        return None
    rho = A / (S - A)
    if rho <= 0:
        return None
    log_rho   = log(rho)
    log_numer = log_kombinasi(S - 1, N) + N * log_rho
    log_terms = [log_kombinasi(S - 1, i) + i * log_rho for i in range(N + 1)]
    max_t     = max(log_terms)
    log_denom = max_t + log(sum(exp(t - max_t) for t in log_terms))
    return max(0.0, min(1.0, exp(log_numer - log_denom)))

def label_gos(p):
    """Menentukan label Grade of Service berdasarkan probabilitas blocking."""
    if p < 0.001:
        return "Sangat Baik", "gos-great"
    if p < 0.01:
        return "Baik", "gos-good"
    if p < 0.05:
        return "Cukup", "gos-ok"
    return "Buruk", "gos-bad"

def cari_n_minimum(S, A, target=0.01):
    """Mencari jumlah kanal minimum agar P_blocking ≤ target."""
    for n in range(1, S):
        p = engset(S, n, A)
        if p is not None and p <= target:
            return n
    return None


# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    # Logo / brand
    st.markdown("""
    <div style="background:rgba(255,255,255,0.10);border-radius:18px;
         padding:1.4rem 1.2rem 1.1rem;margin-bottom:1.4rem;text-align:center;">
      <div style="font-size:2.2rem;margin-bottom:2px;">📡</div>
      <div style="font-size:1.35rem;font-weight:800;color:#fff;letter-spacing:-0.01em;">EngsetPro</div>
      <div style="font-size:0.65rem;color:rgba(255,255,255,0.5);letter-spacing:0.1em;
           text-transform:uppercase;margin-top:2px;">Rekayasa Trafik v2.0</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="nav-group-label">Menu Utama</div>', unsafe_allow_html=True)
    page = st.radio("nav", [
        "🏠  Dashboard",
        "🧮  Kalkulator Engset",
        "📊  Analisis & Grafik",
        "📄  Ekspor Laporan",
    ], label_visibility="collapsed")

    st.markdown('<div class="nav-group-label">Hitung Trafik A</div>', unsafe_allow_html=True)
    page_a = st.radio("nav_a", [
        "📞  A — Call Rate & Hold Time",
        "👥  A — Pengguna Aktif (BHT)",
        "🔁  A — Data Rate / Throughput",
    ], label_visibility="collapsed")

    st.markdown("---")
    st.markdown('<div class="nav-group-label">Parameter Sistem</div>', unsafe_allow_html=True)

    S = st.slider("S — Jumlah Source", 2, 200, 20, 1)
    N = st.slider("N — Jumlah Kanal",  1, 100,  5, 1)
    A = st.slider("A — Trafik yang Ditawarkan (Erl)", 0.1, float(max(1, S-1)), min(8.0, float(S-2)), 0.1)

    st.markdown("---")
    st.markdown(f"""
    <div style="background:rgba(255,255,255,0.08);border-radius:14px;padding:1rem;">
      <div style="font-size:0.65rem;color:rgba(255,255,255,0.45);text-transform:uppercase;
           letter-spacing:0.1em;margin-bottom:8px;">Sesi Saat Ini</div>
      <div style="font-size:0.82rem;color:rgba(255,255,255,0.85);line-height:2.1;">
        S = <strong>{S}</strong> pengguna<br>
        N = <strong>{N}</strong> kanal<br>
        A = <strong>{A:.1f}</strong> Erlang
      </div>
      <div style="font-size:0.68rem;color:rgba(255,255,255,0.38);margin-top:8px;">
        {datetime.now().strftime('%d %b %Y · %H:%M')}</div>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# HITUNG
# ═══════════════════════════════════════════════════════════════════════════════
valid     = S > N and 0 < A < S
P         = engset(S, N, A) if valid else None
carried   = A * (1 - P)     if P is not None else 0.0
lost      = A * P            if P is not None else 0.0
util_pct  = (carried / N) * 100 if (P is not None and N > 0) else 0.0
gos_text, gos_cls = label_gos(P) if P is not None else ("—", "gos-ok")
min_n_1   = cari_n_minimum(S, A, 0.01)  if valid else "—"
min_n_001 = cari_n_minimum(S, A, 0.001) if valid else "—"

BLUE  = '#1a56ff'
TEAL  = '#00c8b4'
AMBER = '#f59e0b'
RED   = '#ef4444'
GREEN = '#22c55e'
BG    = '#f8faff'


# ═══════════════════════════════════════════════════════════════════════════════
# PENENTUAN HALAMAN AKTIF
# ═══════════════════════════════════════════════════════════════════════════════
if "last_nav" not in st.session_state:
    st.session_state["last_nav"] = "main"

prev_page   = st.session_state.get("prev_page",   page)
prev_page_a = st.session_state.get("prev_page_a", page_a)

if page != prev_page:
    st.session_state["last_nav"] = "main"
elif page_a != prev_page_a:
    st.session_state["last_nav"] = "a"

st.session_state["prev_page"]   = page
st.session_state["prev_page_a"] = page_a

active_page = page if st.session_state["last_nav"] == "main" else page_a


# ═══════════════════════════════════════════════════════════════════════════════
# HELPER — Header halaman
# ═══════════════════════════════════════════════════════════════════════════════
def page_header(tag, title, sub):
    st.markdown(f"""
    <div class="page-header">
      <div class="page-header-tag">{tag}</div>
      <h1 class="page-header-title">{title}</h1>
      <p class="page-header-sub">{sub}</p>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# HELPER — Donut chart (matplotlib)
# ═══════════════════════════════════════════════════════════════════════════════
def donut_chart(val_pct, label_center, label_bottom, color=BLUE, bg='#e8efff'):
    fig, ax = plt.subplots(figsize=(3.8, 3.8))
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')
    sizes = [val_pct, max(0, 100 - val_pct)]
    clrs  = [color, bg]
    ax.pie(sizes, colors=clrs, startangle=90,
           wedgeprops=dict(width=0.44, edgecolor='white', linewidth=3),
           counterclock=False)
    ax.text(0, 0.08, label_center,
            ha='center', va='center', fontsize=18, fontweight='bold',
            color='#0d1b3e', fontfamily='monospace')
    ax.text(0, -0.24, label_bottom,
            ha='center', va='center', fontsize=9, color='#8899bb')
    ax.axis('equal')
    plt.tight_layout(pad=0.3)
    return fig


# ══════════════════════════════════════════════════════════════════════════════
# ██ DASHBOARD
# Menampilkan ringkasan cepat: probabilitas blocking, carried/lost traffic,
# utilisasi kanal, dan rekomendasi jumlah kanal minimum.
# ══════════════════════════════════════════════════════════════════════════════
if active_page == "🏠  Dashboard":

    col_main, col_side = st.columns([2.1, 1], gap="large")

    with col_main:
        st.markdown(f"""
        <div class="hero-card">
          <div class="hero-badge">📡 EngsetPro · Model Finite Source</div>
          <h1 style="font-size:1.65rem;font-weight:800;color:#fff;margin:0 0 0.3rem;
               line-height:1.15;">Dashboard Analisis<br>Engset</h1>
          <p style="font-size:0.85rem;opacity:0.75;margin:0 0 1.4rem;">
            Probabilitas blocking real-time — Model Engset Finite Source</p>
          <div style="display:flex;gap:10px;flex-wrap:wrap;">
            <div class="hero-stat-pill">
              <div style="font-size:0.62rem;opacity:0.7;text-transform:uppercase;
                   letter-spacing:0.08em;margin-bottom:1px;">Source</div>
              <div style="font-size:1.3rem;font-weight:800;
                   font-family:'JetBrains Mono',monospace;">S = {S}</div>
            </div>
            <div class="hero-stat-pill">
              <div style="font-size:0.62rem;opacity:0.7;text-transform:uppercase;
                   letter-spacing:0.08em;margin-bottom:1px;">Kanal</div>
              <div style="font-size:1.3rem;font-weight:800;
                   font-family:'JetBrains Mono',monospace;">N = {N}</div>
            </div>
            <div class="hero-stat-pill">
              <div style="font-size:0.62rem;opacity:0.7;text-transform:uppercase;
                   letter-spacing:0.08em;margin-bottom:1px;">Trafik</div>
              <div style="font-size:1.3rem;font-weight:800;
                   font-family:'JetBrains Mono',monospace;">A = {A:.1f}</div>
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
                <div class="chip-lbl">Trafik Terlayani (Erl)</div>
              </div>
              <div class="chip">
                <div class="chip-icon">❌</div>
                <div class="chip-val">{lost:.3f}</div>
                <div class="chip-lbl">Trafik Hilang (Erl)</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<p class="sec-title">📋 Ringkasan Sistem</p>', unsafe_allow_html=True)

        items = [
            ("📶", "plan-icon-blue",  "Probabilitas Blocking", f"{P*100:.3f}%" if P else "—",  f"Grade: {gos_text}"),
            ("🔄", "plan-icon-teal",  "Trafik Terlayani",      f"{carried:.4f} Erl",             f"dari {A:.1f} Erl yang ditawarkan"),
            ("📉", "plan-icon-amber", "N Min untuk GoS ≤ 1%",  f"N = {min_n_1}",                "untuk kualitas layanan baik"),
            ("⚡", "plan-icon-red",   "Utilisasi Kanal",        f"{util_pct:.1f}%",              f"rata-rata per {N} kanal"),
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
        fig_d = donut_chart(
            util_pct,
            f"{util_pct:.1f}%" if P else "—",
            "utilisasi kanal",
            color=BLUE,
        )
        st.pyplot(fig_d, use_container_width=True)
        plt.close(fig_d)

        pbar_w  = min(100, (P or 0) * 500)
        bar_col = GREEN if (P or 1) < 0.01 else AMBER if (P or 1) < 0.05 else RED
        st.markdown(f"""
        <div class="card" style="text-align:center;padding:1.3rem;">
          <div style="font-size:0.68rem;color:var(--muted);text-transform:uppercase;
               letter-spacing:0.08em;margin-bottom:8px;">Grade of Service</div>
          <span class="gos {gos_cls}" style="font-size:0.95rem;padding:7px 22px;">{gos_text}</span>
          <div style="margin-top:12px;">
            <div class="progress-wrap">
              <div class="progress-fill" style="width:{pbar_w:.1f}%;background:{bar_col};"></div>
            </div>
          </div>
          <div style="font-size:0.75rem;color:var(--muted);margin-top:6px;">
            P = {f"{P:.6f}" if P is not None else "—"}
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="card">
          <div style="font-size:0.85rem;font-weight:700;color:var(--navy);margin-bottom:10px;">
            🎯 Rekomendasi Kanal</div>
          <div style="font-size:0.82rem;color:var(--slate);line-height:2.3;">
            GoS ≤ 1%&nbsp;&nbsp;&nbsp;→
            <strong style="color:var(--blue-primary);">N = {min_n_1}</strong><br>
            GoS ≤ 0,1% →
            <strong style="color:var(--blue-primary);">N = {min_n_001}</strong>
          </div>
        </div>
        """, unsafe_allow_html=True)

        if not valid:
            st.markdown('<div class="eng-warn">⚠️ Pastikan S &gt; N dan A &lt; S</div>',
                        unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ██ KALKULATOR ENGSET
# Menampilkan rumus Engset lengkap, langkah-langkah perhitungan,
# hasil numerik detail, dan tabel rekomendasi N minimum.
# ══════════════════════════════════════════════════════════════════════════════
elif active_page == "🧮  Kalkulator Engset":
    page_header("Rekayasa Trafik", "Kalkulator Engset",
                "Hitung probabilitas blocking dengan model finite source Engset")

    # ── Rumus Engset standar notasi matematika ──────────────────────────────
    st.markdown("""
    <div class="formula-wrap">
      <span class="formula-tag">Rumus Engset — Model Finite Source (ITU-T)</span>
      <div class="formula-body">
              C(S−1, N) · ρᴺ
P(S, N, A) = ─────────────────────────
               N
              Σ  C(S−1, i) · ρⁱ
             i=0

                    A
di mana:  ρ = ─────────
               S − A</div>
      <div class="formula-legend">
        <div class="fl-item"><span class="fl-sym">P</span> Probabilitas blocking</div>
        <div class="fl-item"><span class="fl-sym">S</span> Jumlah sumber (pengguna)</div>
        <div class="fl-item"><span class="fl-sym">N</span> Jumlah kanal (server)</div>
        <div class="fl-item"><span class="fl-sym">A</span> Trafik yang ditawarkan (Erlang)</div>
        <div class="fl-item"><span class="fl-sym">ρ</span> Rasio intensitas trafik = A/(S−A)</div>
        <div class="fl-item"><span class="fl-sym">C(n,k)</span> Koefisien binomial = n! / (k!(n−k)!)</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if not valid:
        st.markdown('<div class="eng-warn">⚠️ Pastikan S &gt; N dan A &lt; S pada sidebar.</div>',
                    unsafe_allow_html=True)
    else:
        col1, col2 = st.columns([1.2, 1], gap="large")

        with col1:
            st.markdown('<p class="sec-title">📊 Hasil Perhitungan</p>', unsafe_allow_html=True)
            rows = [
                ("📡", "plan-icon-blue",  "Probabilitas Blocking (P)", f"{P:.8f}",        "probabilitas"),
                ("📈", "plan-icon-blue",  "Blocking (Persentase)",      f"{P*100:.4f}%",   "persentase terblokir"),
                ("🏆", "plan-icon-green", "Grade of Service",            gos_text,           "penilaian kualitas"),
                ("✅", "plan-icon-teal",  "Trafik Terlayani",            f"{carried:.4f} Erl","traffic carried"),
                ("❌", "plan-icon-red",   "Trafik Hilang",               f"{lost:.4f} Erl",  "traffic lost"),
                ("⚡", "plan-icon-amber", "Utilisasi Kanal",             f"{util_pct:.2f}%", "per kanal"),
                ("📶", "plan-icon-blue",  "Intensitas Trafik per Kanal", f"{A/N:.4f} Erl/ch","per kanal"),
            ]
            for icon, icon_cls, label, val, unit in rows:
                st.markdown(f"""
                <div class="plan-card" style="padding:0.85rem 1.1rem;">
                  <div class="plan-icon-wrap {icon_cls}"
                       style="width:38px;height:38px;border-radius:10px;font-size:1.1rem;">{icon}</div>
                  <div class="plan-info">
                    <p class="plan-name" style="font-size:0.84rem;">{label}</p>
                    <p class="plan-desc">{unit}</p>
                  </div>
                  <div class="plan-val" style="font-size:0.92rem;">{val}</div>
                </div>
                """, unsafe_allow_html=True)

        with col2:
            fig_du = donut_chart(util_pct, f"{util_pct:.1f}%", "utilisasi", color=BLUE)
            st.pyplot(fig_du, use_container_width=True)
            plt.close(fig_du)

            st.markdown('<p class="sec-title">🎯 Rekomendasi N Minimum</p>', unsafe_allow_html=True)
            targets = [0.10, 0.05, 0.02, 0.01, 0.005, 0.001]
            rec_rows = ""
            for t in targets:
                mn = cari_n_minimum(S, A, t)
                ok = N >= (mn if mn else 9999)
                rec_rows += (f'<tr><td>≤ {t*100:.1f}%</td>'
                             f'<td>N ≥ {mn if mn else "–"}</td>'
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
                st.markdown('<div class="eng-warn">⚠️ Cukup — pertimbangkan penambahan kanal</div>',
                            unsafe_allow_html=True)
            else:
                st.markdown('<div class="eng-warn">🔴 Buruk — tambah kanal segera!</div>',
                            unsafe_allow_html=True)

            with st.expander("🔢 Lihat langkah-langkah perhitungan"):
                rho = A / (S - A)
                st.markdown(f"""
**Langkah 1 — Hitung rasio intensitas trafik (ρ):**
```
ρ = A / (S − A)
  = {A:.2f} / ({S} − {A:.2f})
  = {rho:.6f}
```
**Langkah 2 — Hitung pembilang:**
```
C(S−1, N) · ρᴺ
= C({S-1}, {N}) · {rho:.6f}^{N}
```
**Langkah 3 — Hitung penyebut:**
```
N
Σ C(S−1, i) · ρⁱ   (i = 0, 1, ..., {N})
i=0
= Σ C({S-1}, i) · {rho:.6f}^i
```
**Langkah 4 — Hasil akhir:**
```
P = pembilang / penyebut
P = {P:.8f}
P = {P*100:.4f}%
```
                """)


# ══════════════════════════════════════════════════════════════════════════════
# ██ HITUNG A — CALL RATE & HOLD TIME
# Menghitung trafik Erlang dari laju panggilan (λ) dan durasi holding (h).
# ══════════════════════════════════════════════════════════════════════════════
elif active_page == "📞  A — Call Rate & Hold Time":
    page_header("Hitung Trafik A", "Call Rate & Hold Time",
                "Hitung Erlang dari λ (laju panggilan) dan h (durasi holding)")

    st.markdown("""
    <div class="formula-wrap">
      <span class="formula-tag">Rumus Erlang — Metode 1: Call Rate</span>
      <div class="formula-body">
A = λ · h

λ = laju panggilan per pengguna (panggilan/jam)
h = rata-rata durasi panggilan (menit)

Konversi satuan:
λ [call/s] = λ [call/jam] / 3600
h [detik]  = h [menit] × 60

Sehingga: A [Erl] = λ [call/s] × h [s]</div>
      <div class="formula-legend">
        <div class="fl-item"><span class="fl-sym">A</span> Trafik per pengguna (Erlang)</div>
        <div class="fl-item"><span class="fl-sym">λ</span> Laju panggilan (call/jam)</div>
        <div class="fl-item"><span class="fl-sym">h</span> Rata-rata durasi panggilan (menit)</div>
        <div class="fl-item"><span class="fl-sym">A_tot</span> Trafik total = A × jumlah pengguna</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.85rem;font-weight:700;color:#0d1b3e;margin-bottom:1rem;">⚙️ Input Parameter</div>',
                    unsafe_allow_html=True)
        call_rate  = st.number_input("λ — Laju panggilan (panggilan/jam per pengguna)",
                                     0.01, 1000.0, 3.0, 0.1, format="%.2f")
        hold_time  = st.number_input("h — Rata-rata durasi panggilan (menit)",
                                     0.1, 120.0, 2.0, 0.1, format="%.1f")
        n_users_t1 = st.number_input("Jumlah pengguna aktif (untuk A total)",
                                     1, 10000, S)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        lam_s = call_rate / 3600
        h_s   = hold_time * 60
        A_1   = lam_s * h_s
        A_tot = A_1 * n_users_t1

        st.markdown(f"""
        <div class="card">
          <div style="font-size:0.85rem;font-weight:700;color:#0d1b3e;margin-bottom:1rem;">📊 Hasil Konversi</div>
          <div class="data-row">
            <span class="data-row-label">Trafik per pengguna (A)</span>
            <span class="data-row-val" style="color:#1a56ff;">{A_1:.6f} Erl</span>
          </div>
          <div class="data-row">
            <span class="data-row-label">λ → konversi ke/detik</span>
            <span class="data-row-val">{lam_s:.6f} call/s</span>
          </div>
          <div class="data-row">
            <span class="data-row-label">h → konversi ke detik</span>
            <span class="data-row-val">{h_s:.0f} detik</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="result-hero">
          <div class="result-hero-label">A Total ({n_users_t1} pengguna)</div>
          <div class="result-hero-val">{A_tot:.4f}</div>
          <div class="result-hero-unit">Erlang — masukkan ke sidebar sebagai nilai A</div>
        </div>
        """, unsafe_allow_html=True)

        if 0 < A_tot < S and S > N:
            P2 = engset(S, N, A_tot)
            if P2:
                g2, gc2 = label_gos(P2)
                cls = "eng-ok" if P2 < 0.01 else "eng-warn"
                st.markdown(f'<div class="{cls}"><strong>Hasil Engset</strong> dengan '
                            f'A = {A_tot:.4f} Erl, S = {S}, N = {N}:<br>'
                            f'P = {P2:.6f} · Blocking = {P2*100:.3f}% · GoS = {g2}</div>',
                            unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ██ HITUNG A — PENGGUNA AKTIF (BHT)
# Menghitung trafik Erlang menggunakan metode Busy Hour Traffic (BHT).
# ══════════════════════════════════════════════════════════════════════════════
elif active_page == "👥  A — Pengguna Aktif (BHT)":
    page_header("Hitung Trafik A", "Pengguna Aktif — Metode BHT",
                "Hitung Erlang dari jumlah pengguna aktif di jam sibuk")

    st.markdown("""
    <div class="formula-wrap">
      <span class="formula-tag">Rumus BHT — Metode 2: Busy Hour Traffic</span>
      <div class="formula-body">
A = U × BHT

U   = jumlah pengguna aktif di jam sibuk
BHT = Busy Hour Traffic per pengguna (Erlang/pengguna)</div>
      <div class="formula-legend">
        <div class="fl-item"><span class="fl-sym">A</span> Trafik total yang ditawarkan (Erlang)</div>
        <div class="fl-item"><span class="fl-sym">U</span> Jumlah pengguna aktif jam sibuk</div>
        <div class="fl-item"><span class="fl-sym">BHT</span> Trafik per pengguna di jam sibuk (Erl)</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.85rem;font-weight:700;color:#0d1b3e;margin-bottom:1rem;">⚙️ Input Parameter</div>',
                    unsafe_allow_html=True)
        U_val = st.number_input("U — Pengguna aktif di jam sibuk", 1, 10000, 50)
        BHT   = st.number_input("BHT — Busy Hour Traffic per pengguna (Erl)",
                                 0.001, 1.0, 0.1, 0.001, format="%.3f")
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        A_t2 = U_val * BHT

        st.markdown(f"""
        <div class="card">
          <div style="font-size:0.85rem;font-weight:700;color:#0d1b3e;margin-bottom:1rem;">📊 Detail Perhitungan</div>
          <div class="data-row">
            <span class="data-row-label">Pengguna aktif (U)</span>
            <span class="data-row-val">{U_val} pengguna</span>
          </div>
          <div class="data-row">
            <span class="data-row-label">BHT per pengguna</span>
            <span class="data-row-val">{BHT:.3f} Erl</span>
          </div>
          <div class="data-row">
            <span class="data-row-label">A = U × BHT = {U_val} × {BHT:.3f}</span>
            <span class="data-row-val">{A_t2:.4f} Erl</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="result-hero">
          <div class="result-hero-label">A Total (Metode BHT)</div>
          <div class="result-hero-val">{A_t2:.4f}</div>
          <div class="result-hero-unit">Erlang — masukkan ke sidebar sebagai nilai A</div>
        </div>
        """, unsafe_allow_html=True)

        if 0 < A_t2 < S and S > N:
            P3 = engset(S, N, A_t2)
            if P3:
                g3, gc3 = label_gos(P3)
                cls = "eng-ok" if P3 < 0.01 else "eng-warn"
                st.markdown(f'<div class="{cls}">P = {P3:.6f} · Blocking = {P3*100:.3f}% · GoS = {g3}</div>',
                            unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ██ HITUNG A — DATA RATE / THROUGHPUT
# Menghitung trafik Erlang berdasarkan perbandingan data rate total
# terhadap kapasitas per kanal.
# ══════════════════════════════════════════════════════════════════════════════
elif active_page == "🔁  A — Data Rate / Throughput":
    page_header("Hitung Trafik A", "Data Rate / Throughput",
                "Hitung Erlang dari data rate total dan kapasitas per kanal")

    st.markdown("""
    <div class="formula-wrap">
      <span class="formula-tag">Rumus Data Rate — Metode 3: Throughput</span>
      <div class="formula-body">
          R_total
A = ─────────────
         R_ch

R_total = data rate total yang diminta (Mbps)
R_ch    = kapasitas (throughput) per kanal (Mbps)</div>
      <div class="formula-legend">
        <div class="fl-item"><span class="fl-sym">A</span> Trafik yang ditawarkan (Erlang)</div>
        <div class="fl-item"><span class="fl-sym">R_total</span> Data rate total agregat (Mbps)</div>
        <div class="fl-item"><span class="fl-sym">R_ch</span> Kapasitas throughput per kanal (Mbps)</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.85rem;font-weight:700;color:#0d1b3e;margin-bottom:1rem;">⚙️ Input Parameter</div>',
                    unsafe_allow_html=True)
        dr = st.number_input("R_total — Data Rate Total (Mbps)", 0.1, 100000.0, 100.0, 1.0)
        cc = st.number_input("R_ch — Kapasitas per Kanal (Mbps)", 0.1, 10000.0, 10.0, 0.1)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        A_t3 = dr / cc

        st.markdown(f"""
        <div class="card">
          <div style="font-size:0.85rem;font-weight:700;color:#0d1b3e;margin-bottom:1rem;">📊 Detail Perhitungan</div>
          <div class="data-row">
            <span class="data-row-label">Data Rate Total (R_total)</span>
            <span class="data-row-val">{dr:.1f} Mbps</span>
          </div>
          <div class="data-row">
            <span class="data-row-label">Kapasitas per Kanal (R_ch)</span>
            <span class="data-row-val">{cc:.1f} Mbps</span>
          </div>
          <div class="data-row">
            <span class="data-row-label">A = R_total / R_ch = {dr:.1f} / {cc:.1f}</span>
            <span class="data-row-val">{A_t3:.4f} Erl</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="result-hero">
          <div class="result-hero-label">A Total (Metode Data Rate)</div>
          <div class="result-hero-val">{A_t3:.4f}</div>
          <div class="result-hero-unit">Erlang — masukkan ke sidebar sebagai nilai A</div>
        </div>
        """, unsafe_allow_html=True)

        if 0 < A_t3 < S and S > N:
            P4 = engset(S, N, A_t3)
            if P4:
                g4, gc4 = label_gos(P4)
                cls = "eng-ok" if P4 < 0.01 else "eng-warn"
                st.markdown(f'<div class="{cls}">P = {P4:.6f} · Blocking = {P4*100:.3f}% · GoS = {g4}</div>',
                            unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ██ ANALISIS & GRAFIK
# Menampilkan tiga grafik: Blocking vs N, Blocking vs A, dan multi-kurva
# perbandingan berbagai nilai A, serta tabel detail per nilai N.
# ══════════════════════════════════════════════════════════════════════════════
elif active_page == "📊  Analisis & Grafik":
    page_header("Visualisasi", "Analisis & Grafik",
                "Visualisasi perilaku sistem terhadap variasi parameter Engset")

    if not valid:
        st.markdown('<div class="eng-warn">⚠️ Periksa parameter di sidebar.</div>',
                    unsafe_allow_html=True)
    else:
        cg1, cg2 = st.columns(2, gap="large")

        # ── Grafik 1: Blocking vs N ──────────────────────────────────────────
        with cg1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("##### 📈 Blocking vs Jumlah Kanal (N)")
            max_n = min(S-1, 50)
            ns_   = list(range(1, max_n+1))
            ps_   = [(engset(S,n,A) or 0)*100 for n in ns_]

            fig1, ax1 = plt.subplots(figsize=(5.5, 3.8))
            fig1.patch.set_facecolor(BG); ax1.set_facecolor(BG)
            ax1.fill_between(ns_, ps_, alpha=0.13, color=BLUE)
            ax1.plot(ns_, ps_, color=BLUE, linewidth=2.5, zorder=3)
            ax1.scatter([N], [P*100], color=RED, s=90, zorder=5,
                        label=f'N={N}, P={P*100:.3f}%')
            ax1.axhline(1.0, color=AMBER, linestyle='--', linewidth=1.2, alpha=0.8)
            ax1.text(max_n*0.97, 1.05, 'GoS 1%', ha='right', fontsize=8, color=AMBER)
            ax1.axhline(0.1, color=TEAL, linestyle='--', linewidth=1.2, alpha=0.8)
            ax1.text(max_n*0.97, 0.15, 'GoS 0,1%', ha='right', fontsize=8, color=TEAL)
            ax1.set_xlabel('N — Jumlah Kanal', fontsize=9, color='#5a6a8e')
            ax1.set_ylabel('Blocking (%)', fontsize=9, color='#5a6a8e')
            ax1.set_title(f'S={S}, A={A:.1f} Erl', fontsize=9, color='#8899bb')
            ax1.legend(fontsize=8.5)
            ax1.grid(True, linestyle='--', alpha=0.3)
            ax1.spines[['top','right']].set_visible(False)
            ax1.tick_params(colors='#8899bb', labelsize=8)
            plt.tight_layout(pad=1.0)
            st.pyplot(fig1, use_container_width=True)
            plt.close(fig1)
            st.markdown('</div>', unsafe_allow_html=True)

        # ── Grafik 2: Blocking vs A ──────────────────────────────────────────
        with cg2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("##### 📉 Blocking vs Trafik Ditawarkan (A)")
            a_max_ = min(float(S-1), 30.0)
            av_    = np.linspace(0.1, a_max_, 300)
            pv_    = [(engset(S,N,float(a)) or 0)*100 for a in av_]

            fig2, ax2 = plt.subplots(figsize=(5.5, 3.8))
            fig2.patch.set_facecolor(BG); ax2.set_facecolor(BG)
            ax2.fill_between(av_, pv_, alpha=0.13, color=TEAL)
            ax2.plot(av_, pv_, color=TEAL, linewidth=2.5, zorder=3)
            ax2.scatter([A], [P*100], color=RED, s=90, zorder=5,
                        label=f'A={A:.1f}, P={P*100:.3f}%')
            ax2.axhline(1.0, color=AMBER, linestyle='--', linewidth=1.2, alpha=0.8)
            ax2.text(a_max_*0.97, 1.05, 'GoS 1%', ha='right', fontsize=8, color=AMBER)
            ax2.set_xlabel('A — Trafik yang Ditawarkan (Erlang)', fontsize=9, color='#5a6a8e')
            ax2.set_ylabel('Blocking (%)', fontsize=9, color='#5a6a8e')
            ax2.set_title(f'S={S}, N={N} kanal', fontsize=9, color='#8899bb')
            ax2.legend(fontsize=8.5)
            ax2.grid(True, linestyle='--', alpha=0.3)
            ax2.spines[['top','right']].set_visible(False)
            ax2.tick_params(colors='#8899bb', labelsize=8)
            plt.tight_layout(pad=1.0)
            st.pyplot(fig2, use_container_width=True)
            plt.close(fig2)
            st.markdown('</div>', unsafe_allow_html=True)

        # ── Grafik 3: Multi-kurva ────────────────────────────────────────────
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("##### 🌐 Multi-Kurva: Blocking vs N untuk Berbagai Nilai A")
        palette = [BLUE, TEAL, AMBER, RED, '#a855f7', '#ec4899']
        a_list  = [round(A*m,2) for m in [0.5,0.75,1.0,1.25,1.5,2.0] if 0 < A*m < S][:6]
        max_n3  = min(S-1, 35)
        ns3_    = list(range(1, max_n3+1))

        fig3, ax3 = plt.subplots(figsize=(11, 4))
        fig3.patch.set_facecolor(BG); ax3.set_facecolor(BG)
        for idx, a_c in enumerate(a_list):
            ps3 = [(engset(S,n,a_c) or 0)*100 for n in ns3_]
            ax3.plot(ns3_, ps3, color=palette[idx%len(palette)],
                     linewidth=2, label=f'A={a_c:.1f} Erl')
        ax3.axvline(N, color='#64748b', linestyle=':', linewidth=1.8,
                    label=f'N aktif = {N}')
        ax3.axhline(1.0, color=AMBER, linestyle='--', linewidth=1, alpha=0.6)
        ax3.set_xlabel('N — Jumlah Kanal', fontsize=9, color='#5a6a8e')
        ax3.set_ylabel('Blocking (%)', fontsize=9, color='#5a6a8e')
        ax3.set_title(f'Perbandingan Blocking vs N untuk Berbagai Nilai A (S={S})',
                      fontsize=10, color='#0d1b3e', fontweight='bold')
        ax3.legend(fontsize=8.5, ncol=min(len(a_list)+1, 4))
        ax3.grid(True, linestyle='--', alpha=0.3)
        ax3.spines[['top','right']].set_visible(False)
        ax3.tick_params(colors='#8899bb', labelsize=8)
        plt.tight_layout(pad=1.0)
        st.pyplot(fig3, use_container_width=True)
        plt.close(fig3)
        st.markdown('</div>', unsafe_allow_html=True)

        # ── Tabel detail ─────────────────────────────────────────────────────
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("##### 📋 Tabel Detail Blocking vs N")
        rows_html = ""
        for n_i in range(1, min(S, N+15)):
            p_i = engset(S, n_i, A)
            if p_i is None:
                continue
            c_i = A*(1-p_i); l_i = A*p_i; u_i = (c_i/n_i)*100
            g_t, g_c = label_gos(p_i)
            active_cls = 'class="active"' if n_i == N else ""
            rows_html += (f'<tr {active_cls}>'
                          f'<td>{"→ " if n_i==N else ""}{n_i}</td>'
                          f'<td>{p_i:.6f}</td><td>{p_i*100:.3f}%</td>'
                          f'<td>{c_i:.4f}</td><td>{l_i:.4f}</td>'
                          f'<td>{u_i:.1f}%</td>'
                          f'<td><span class="gos {g_c}">{g_t}</span></td></tr>')
        st.markdown(f"""
        <table class="eng-table">
          <thead>
            <tr><th>N</th><th>P Blocking</th><th>%</th>
                <th>Trafik Terlayani (Erl)</th><th>Trafik Hilang (Erl)</th>
                <th>Utilisasi</th><th>GoS</th></tr>
          </thead>
          <tbody>{rows_html}</tbody>
        </table>
        <div class="eng-info" style="margin-top:8px;font-size:0.78rem;">
          🔵 Baris biru = nilai N yang dipilih saat ini (N={N})</div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ██ EKSPOR LAPORAN
# Generate laporan PDF profesional berstandar teknik telekomunikasi.
# ══════════════════════════════════════════════════════════════════════════════
elif active_page == "📄  Ekspor Laporan":
    page_header("Ekspor", "Ekspor Laporan PDF",
                "Buat laporan teknik profesional hasil analisis Engset")

    if not valid:
        st.markdown('<div class="eng-warn">⚠️ Periksa parameter di sidebar terlebih dahulu.</div>',
                    unsafe_allow_html=True)
    elif not PDF_OK:
        st.markdown('<div class="eng-warn">⚠️ Instal ReportLab terlebih dahulu: <code>pip install reportlab</code></div>',
                    unsafe_allow_html=True)
    else:
        c_prev, c_act = st.columns([1.5, 1], gap="large")

        with c_prev:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div style="font-size:0.9rem;font-weight:700;color:#0d1b3e;'
                        'margin-bottom:1rem;">📄 Isi Laporan yang Akan Dibuat</div>',
                        unsafe_allow_html=True)

            items_prev = [
                ("📌", "Judul",                 "EngsetPro — Laporan Analisis Trafik Engset"),
                ("📅", "Tanggal",               datetime.now().strftime('%d %B %Y, %H:%M')),
                ("1️⃣", "Pendahuluan",           "Latar belakang & dasar teori Engset"),
                ("2️⃣", "Landasan Teori",        "Rumus Engset, definisi, dan variabel"),
                ("3️⃣", "Parameter Input",        f"S={S}, N={N}, A={A:.1f} Erl"),
                ("4️⃣", "Hasil Perhitungan",      f"P={P:.8f}, GoS={gos_text}"),
                ("5️⃣", "Analisis Trafik",        f"Carried={carried:.4f} Erl, Lost={lost:.4f} Erl"),
                ("6️⃣", "Grafik Analisis",        "Blocking vs N + Blocking vs A"),
                ("7️⃣", "Tabel Rekomendasi N",    "N minimum per target GoS"),
                ("8️⃣", "Kesimpulan",             "Ringkasan dan rekomendasi teknis"),
            ]
            for icon, label, val in items_prev:
                st.markdown(f"""
                <div class="data-row">
                  <span class="data-row-label">{icon} {label}</span>
                  <span class="data-row-val" style="text-align:right;max-width:55%;font-size:0.78rem;">{val}</span>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with c_act:
            st.markdown("""
            <div class="card" style="text-align:center;padding:2rem 1.5rem;">
              <div style="font-size:3rem;margin-bottom:1rem;">📄</div>
              <div style="font-size:1rem;font-weight:700;color:#0d1b3e;margin-bottom:0.5rem;">
                Laporan PDF Profesional</div>
              <div style="font-size:0.82rem;color:#8899bb;margin-bottom:1.5rem;line-height:1.6;">
                Berisi pendahuluan, landasan teori, rumus standar ITU-T,
                parameter, hasil perhitungan, grafik analisis, tabel,
                dan kesimpulan teknis.
              </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("⬇️  Generate & Unduh PDF", use_container_width=True):
                with st.spinner("Membuat laporan PDF profesional..."):

                    def fig_to_bytes(fig):
                        buf = io.BytesIO()
                        fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
                        buf.seek(0)
                        return buf.read()

                    # ── Buat grafik 1: Blocking vs N ─────────────────────────
                    max_n_ = min(S-1, 40)
                    ns__   = list(range(1, max_n_+1))
                    ps__   = [(engset(S,n,A) or 0)*100 for n in ns__]
                    f1, a1 = plt.subplots(figsize=(7, 3.5))
                    f1.patch.set_facecolor(BG); a1.set_facecolor(BG)
                    a1.fill_between(ns__, ps__, alpha=0.12, color=BLUE)
                    a1.plot(ns__, ps__, color=BLUE, linewidth=2)
                    a1.scatter([N], [P*100], color=RED, s=60, zorder=5,
                               label=f'N={N}, P={P*100:.3f}%')
                    a1.axhline(1.0, color=AMBER, linestyle='--', linewidth=1, label='GoS 1%')
                    a1.axhline(0.1, color=TEAL,  linestyle='--', linewidth=1, label='GoS 0,1%')
                    a1.set_xlabel('N (Jumlah Kanal)'); a1.set_ylabel('Blocking (%)')
                    a1.set_title(f'Gambar 1. Kurva Blocking vs Jumlah Kanal N (S={S}, A={A:.1f} Erl)')
                    a1.legend(fontsize=8); a1.grid(True, linestyle='--', alpha=0.3)
                    a1.spines[['top','right']].set_visible(False)
                    plt.tight_layout()
                    c1_bytes = fig_to_bytes(f1)
                    plt.close(f1)

                    # ── Buat grafik 2: Blocking vs A ─────────────────────────
                    am_ = min(float(S-1), 25.0)
                    av_ = np.linspace(0.1, am_, 200)
                    pv_ = [(engset(S,N,float(a)) or 0)*100 for a in av_]
                    f2, a2 = plt.subplots(figsize=(7, 3.5))
                    f2.patch.set_facecolor(BG); a2.set_facecolor(BG)
                    a2.fill_between(av_, pv_, alpha=0.12, color=TEAL)
                    a2.plot(av_, pv_, color=TEAL, linewidth=2)
                    a2.scatter([A], [P*100], color=RED, s=60, zorder=5,
                               label=f'A={A:.1f}, P={P*100:.3f}%')
                    a2.axhline(1.0, color=AMBER, linestyle='--', linewidth=1, label='GoS 1%')
                    a2.set_xlabel('A (Erlang)'); a2.set_ylabel('Blocking (%)')
                    a2.set_title(f'Gambar 2. Kurva Blocking vs Trafik yang Ditawarkan A (S={S}, N={N})')
                    a2.legend(fontsize=8); a2.grid(True, linestyle='--', alpha=0.3)
                    a2.spines[['top','right']].set_visible(False)
                    plt.tight_layout()
                    c2_bytes = fig_to_bytes(f2)
                    plt.close(f2)

                    # ══════════════════════════════════════════════════════════
                    # BUILD PDF
                    # ══════════════════════════════════════════════════════════
                    buf_pdf = io.BytesIO()
                    PAGE_W, PAGE_H = A4
                    doc = SimpleDocTemplate(
                        buf_pdf, pagesize=A4,
                        leftMargin=2.5*cm, rightMargin=2*cm,
                        topMargin=2.5*cm, bottomMargin=2.5*cm,
                        title="Laporan Analisis Trafik Engset",
                        author="EngsetPro v2.0",
                    )

                    # ── Styles ────────────────────────────────────────────────
                    NAVY  = colors.HexColor('#0d1b3e')
                    BLUE_ = colors.HexColor('#1a56ff')
                    TEAL_ = colors.HexColor('#00c8b4')
                    LGRAY = colors.HexColor('#f0f4ff')
                    MGRAY = colors.HexColor('#c7d7ff')
                    DGRAY = colors.HexColor('#8899bb')

                    cover_title = ParagraphStyle('CT', fontSize=28, textColor=NAVY,
                                                 fontName='Helvetica-Bold', spaceAfter=6,
                                                 alignment=TA_CENTER)
                    cover_sub   = ParagraphStyle('CS', fontSize=13, textColor=BLUE_,
                                                 spaceAfter=6, alignment=TA_CENTER)
                    cover_info  = ParagraphStyle('CI', fontSize=9, textColor=DGRAY,
                                                 alignment=TA_CENTER, leading=16)
                    ch_title    = ParagraphStyle('CH', fontSize=13, textColor=NAVY,
                                                 fontName='Helvetica-Bold',
                                                 spaceBefore=18, spaceAfter=8,
                                                 borderPad=4)
                    body        = ParagraphStyle('BD', fontSize=9.5, textColor=colors.HexColor('#2d3a5e'),
                                                 leading=16, spaceAfter=6, alignment=TA_JUSTIFY)
                    formula_st  = ParagraphStyle('FM', fontSize=10, fontName='Courier',
                                                 textColor=colors.HexColor('#0d2060'),
                                                 backColor=LGRAY,
                                                 leftIndent=14, rightIndent=14,
                                                 spaceBefore=6, spaceAfter=6, leading=20,
                                                 alignment=TA_LEFT)
                    caption_st  = ParagraphStyle('CP', fontSize=8, textColor=DGRAY,
                                                 alignment=TA_CENTER, spaceBefore=4, spaceAfter=10)
                    footer_st   = ParagraphStyle('FT', fontSize=7.5, textColor=DGRAY,
                                                 alignment=TA_CENTER)
                    label_bold  = ParagraphStyle('LB', fontSize=9, fontName='Helvetica-Bold',
                                                 textColor=NAVY)

                    el = []

                    # ══════════════════════════════════════════════════════════
                    # HALAMAN SAMPUL
                    # ══════════════════════════════════════════════════════════
                    el.append(Spacer(1, 3*cm))
                    el.append(Paragraph("LAPORAN ANALISIS TRAFIK", cover_sub))
                    el.append(Paragraph("Model Engset Finite Source", cover_title))
                    el.append(Spacer(1, 0.5*cm))
                    el.append(HRFlowable(width="70%", thickness=2,
                                         color=BLUE_, spaceAfter=16,
                                         hAlign='CENTER'))
                    el.append(Spacer(1, 0.5*cm))

                    cover_data = [
                        ["Parameter",    "Nilai",         "Satuan"],
                        ["S — Jumlah Source",  str(S),   "pengguna"],
                        ["N — Jumlah Kanal",   str(N),   "kanal"],
                        ["A — Trafik Ditawarkan", f"{A:.1f}", "Erlang"],
                        ["P — Probabilitas Blocking", f"{P:.6f}", "—"],
                        ["Grade of Service",   gos_text, "—"],
                    ]
                    ct = Table(cover_data, colWidths=[7*cm, 4*cm, 4*cm],
                               hAlign='CENTER')
                    ct.setStyle(TableStyle([
                        ('BACKGROUND',  (0,0), (-1,0), BLUE_),
                        ('TEXTCOLOR',   (0,0), (-1,0), colors.white),
                        ('FONTNAME',    (0,0), (-1,0), 'Helvetica-Bold'),
                        ('FONTSIZE',    (0,0), (-1,-1), 9.5),
                        ('ALIGN',       (0,0), (-1,-1), 'CENTER'),
                        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LGRAY]),
                        ('GRID',        (0,0), (-1,-1), 0.5, MGRAY),
                        ('TOPPADDING',  (0,0), (-1,-1), 8),
                        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
                        ('ROUNDEDCORNERS', [4]),
                    ]))
                    el.append(ct)
                    el.append(Spacer(1, 2*cm))
                    el.append(Paragraph(
                        f"Tanggal Laporan: {datetime.now().strftime('%d %B %Y, pukul %H:%M WIB')}<br/>"
                        f"Dibuat dengan: EngsetPro v2.0 — Kalkulator Rekayasa Trafik",
                        cover_info))
                    el.append(PageBreak())

                    # ══════════════════════════════════════════════════════════
                    # BAB 1 — PENDAHULUAN
                    # ══════════════════════════════════════════════════════════
                    el.append(Paragraph("1.  Pendahuluan", ch_title))
                    el.append(HRFlowable(width="100%", thickness=1, color=MGRAY, spaceAfter=10))
                    el.append(Paragraph(
                        "Laporan ini menyajikan hasil analisis rekayasa trafik telekomunikasi "
                        "menggunakan model probabilistik <b>Engset</b> (finite source model). "
                        "Model Engset digunakan ketika jumlah sumber trafik (pengguna) bersifat "
                        "terbatas (finite), sehingga memberikan estimasi probabilitas blocking "
                        "yang lebih akurat dibandingkan model Erlang-B untuk kondisi tersebut.",
                        body))
                    el.append(Paragraph(
                        "Tujuan analisis ini adalah menentukan probabilitas blocking sistem, "
                        "mengevaluasi Grade of Service (GoS), serta memberikan rekomendasi "
                        "jumlah kanal minimum yang diperlukan untuk memenuhi standar kualitas layanan.",
                        body))
                    el.append(Spacer(1, 0.3*cm))

                    # ══════════════════════════════════════════════════════════
                    # BAB 2 — LANDASAN TEORI
                    # ══════════════════════════════════════════════════════════
                    el.append(Paragraph("2.  Landasan Teori", ch_title))
                    el.append(HRFlowable(width="100%", thickness=1, color=MGRAY, spaceAfter=10))
                    el.append(Paragraph(
                        "<b>2.1  Model Engset</b><br/>"
                        "Model Engset merupakan model antrian teletraffic yang dikembangkan "
                        "oleh T. O. Engset (1918) untuk sistem dengan sumber trafik terbatas. "
                        "Model ini mengasumsikan bahwa pengguna yang sedang ditangani sistem "
                        "tidak dapat membangkitkan permintaan baru (blocked calls cleared).",
                        body))
                    el.append(Paragraph(
                        "<b>2.2  Rumus Engset</b><br/>"
                        "Probabilitas blocking P(S, N, A) dihitung menggunakan rumus berikut:",
                        body))

                    el.append(Paragraph(
                        "              C(S-1, N) x rho^N\n"
                        "P(S,N,A) = ─────────────────────────\n"
                        "            N\n"
                        "           SUM  C(S-1, i) x rho^i\n"
                        "           i=0\n\n"
                        "          A\n"
                        "rho = ─────────\n"
                        "        S - A",
                        formula_st))

                    el.append(Paragraph(
                        "<b>Keterangan variabel:</b>",
                        body))

                    var_data = [
                        ["Simbol", "Nama",                        "Keterangan"],
                        ["P",      "Probabilitas Blocking",        "Peluang suatu panggilan terblokir"],
                        ["S",      "Jumlah Source",                "Total pengguna/sumber trafik"],
                        ["N",      "Jumlah Kanal",                 "Jumlah server/kanal tersedia"],
                        ["A",      "Traffic Offered",              "Trafik total yang ditawarkan (Erlang)"],
                        ["ρ (rho)","Rasio Intensitas Trafik",      "A / (S − A)"],
                        ["C(n,k)", "Koefisien Binomial",           "n! / (k! · (n−k)!)"],
                    ]
                    vt = Table(var_data, colWidths=[2.2*cm, 5*cm, 8.3*cm])
                    vt.setStyle(TableStyle([
                        ('BACKGROUND',   (0,0), (-1,0), NAVY),
                        ('TEXTCOLOR',    (0,0), (-1,0), colors.white),
                        ('FONTNAME',     (0,0), (-1,0), 'Helvetica-Bold'),
                        ('FONTSIZE',     (0,0), (-1,-1), 8.5),
                        ('ALIGN',        (0,0), (0,-1),  'CENTER'),
                        ('ALIGN',        (1,0), (-1,-1), 'LEFT'),
                        ('ROWBACKGROUNDS',(0,1),(-1,-1), [colors.white, LGRAY]),
                        ('GRID',         (0,0), (-1,-1), 0.4, MGRAY),
                        ('TOPPADDING',   (0,0), (-1,-1), 6),
                        ('BOTTOMPADDING',(0,0), (-1,-1), 6),
                        ('FONTNAME',     (0,1), (0,-1),  'Courier-Bold'),
                    ]))
                    el.append(vt)
                    el.append(Spacer(1, 0.4*cm))

                    el.append(Paragraph(
                        "<b>2.3  Grade of Service (GoS)</b><br/>"
                        "Grade of Service merupakan ukuran kualitas layanan telekomunikasi "
                        "yang dinyatakan sebagai probabilitas blocking. Standar umum yang "
                        "digunakan dalam rekayasa trafik adalah sebagai berikut:",
                        body))

                    gos_data = [
                        ["Rentang Blocking",  "Kategori GoS",  "Keterangan"],
                        ["P < 0,001 (0,1%)",  "Sangat Baik",   "Kualitas premium, layanan kritis"],
                        ["0,001 ≤ P < 0,01",  "Baik",          "Memenuhi standar ITU-T"],
                        ["0,01 ≤ P < 0,05",   "Cukup",         "Perlu penambahan kapasitas"],
                        ["P ≥ 0,05 (5%)",     "Buruk",         "Tidak memenuhi standar minimum"],
                    ]
                    gt = Table(gos_data, colWidths=[4.5*cm, 3.5*cm, 7.5*cm])
                    gt.setStyle(TableStyle([
                        ('BACKGROUND',   (0,0), (-1,0), TEAL_),
                        ('TEXTCOLOR',    (0,0), (-1,0), colors.white),
                        ('FONTNAME',     (0,0), (-1,0), 'Helvetica-Bold'),
                        ('FONTSIZE',     (0,0), (-1,-1), 8.5),
                        ('ALIGN',        (0,0), (-1,-1), 'LEFT'),
                        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, LGRAY]),
                        ('GRID',         (0,0), (-1,-1), 0.4, MGRAY),
                        ('TOPPADDING',   (0,0), (-1,-1), 6),
                        ('BOTTOMPADDING',(0,0), (-1,-1), 6),
                    ]))
                    el.append(gt)
                    el.append(Spacer(1, 0.4*cm))

                    # ══════════════════════════════════════════════════════════
                    # BAB 3 — PARAMETER INPUT
                    # ══════════════════════════════════════════════════════════
                    el.append(Paragraph("3.  Parameter Input", ch_title))
                    el.append(HRFlowable(width="100%", thickness=1, color=MGRAY, spaceAfter=10))
                    el.append(Paragraph(
                        "Parameter berikut digunakan sebagai masukan dalam perhitungan Engset:",
                        body))

                    pd_data = [
                        ["No.", "Parameter",           "Simbol", "Nilai",       "Satuan"],
                        ["1",   "Jumlah Source",        "S",      str(S),        "pengguna"],
                        ["2",   "Jumlah Kanal",          "N",      str(N),        "kanal"],
                        ["3",   "Traffic Offered",       "A",      f"{A:.2f}",    "Erlang"],
                        ["4",   "Rasio Intensitas (ρ)",  "ρ",      f"{A/(S-A):.6f}", "—"],
                    ]
                    pt = Table(pd_data, colWidths=[1*cm, 5.5*cm, 2*cm, 3*cm, 4*cm])
                    pt.setStyle(TableStyle([
                        ('BACKGROUND',   (0,0), (-1,0), BLUE_),
                        ('TEXTCOLOR',    (0,0), (-1,0), colors.white),
                        ('FONTNAME',     (0,0), (-1,0), 'Helvetica-Bold'),
                        ('FONTSIZE',     (0,0), (-1,-1), 9),
                        ('ALIGN',        (0,0), (-1,-1), 'CENTER'),
                        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, LGRAY]),
                        ('GRID',         (0,0), (-1,-1), 0.5, MGRAY),
                        ('TOPPADDING',   (0,0), (-1,-1), 7),
                        ('BOTTOMPADDING',(0,0), (-1,-1), 7),
                        ('FONTNAME',     (2,1), (2,-1), 'Courier-Bold'),
                    ]))
                    el.append(pt)
                    el.append(Spacer(1, 0.4*cm))

                    # ══════════════════════════════════════════════════════════
                    # BAB 4 — HASIL PERHITUNGAN
                    # ══════════════════════════════════════════════════════════
                    el.append(Paragraph("4.  Hasil Perhitungan", ch_title))
                    el.append(HRFlowable(width="100%", thickness=1, color=MGRAY, spaceAfter=10))
                    el.append(Paragraph(
                        "Perhitungan dilakukan menggunakan metode log-space arithmetic "
                        "untuk menghindari overflow numerik pada nilai S yang besar.",
                        body))

                    rd_data = [
                        ["Metrik",                  "Nilai",              "Satuan",  "Keterangan"],
                        ["Probabilitas Blocking (P)", f"{P:.8f}",          "—",       "Hasil utama Engset"],
                        ["Blocking (%)",              f"{P*100:.4f}",      "%",       "Konversi ke persentase"],
                        ["Grade of Service",          gos_text,            "—",       "Penilaian kualitas"],
                        ["Traffic Carried",           f"{carried:.4f}",   "Erlang",  "Trafik yang terlayani"],
                        ["Traffic Lost",              f"{lost:.4f}",      "Erlang",  "Trafik yang terblokir"],
                        ["Utilisasi Kanal",           f"{util_pct:.2f}",  "%",       "Rata-rata per kanal"],
                        ["N Min (GoS ≤ 1%)",         str(min_n_1),        "kanal",   "Rekomendasi minimum"],
                        ["N Min (GoS ≤ 0,1%)",       str(min_n_001),      "kanal",   "Rekomendasi premium"],
                    ]
                    rt = Table(rd_data, colWidths=[5*cm, 3.5*cm, 2.5*cm, 4.5*cm])
                    rt.setStyle(TableStyle([
                        ('BACKGROUND',   (0,0), (-1,0), NAVY),
                        ('TEXTCOLOR',    (0,0), (-1,0), colors.white),
                        ('FONTNAME',     (0,0), (-1,0), 'Helvetica-Bold'),
                        ('FONTSIZE',     (0,0), (-1,-1), 8.5),
                        ('ALIGN',        (1,0), (2,-1), 'CENTER'),
                        ('ALIGN',        (0,0), (0,-1), 'LEFT'),
                        ('ALIGN',        (3,0), (3,-1), 'LEFT'),
                        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, LGRAY]),
                        ('GRID',         (0,0), (-1,-1), 0.5, MGRAY),
                        ('TOPPADDING',   (0,0), (-1,-1), 7),
                        ('BOTTOMPADDING',(0,0), (-1,-1), 7),
                        # Highlight baris P blocking
                        ('BACKGROUND',   (0,1), (-1,1), colors.HexColor('#dce8ff')),
                        ('FONTNAME',     (1,1), (1,1),  'Helvetica-Bold'),
                    ]))
                    el.append(rt)
                    el.append(Spacer(1, 0.5*cm))

                    # ── Tabel rekomendasi N ───────────────────────────────────
                    el.append(Paragraph("<b>4.1  Tabel Rekomendasi Jumlah Kanal Minimum</b>", body))
                    targets_pdf = [0.10, 0.05, 0.02, 0.01, 0.005, 0.001]
                    rec_data = [["Target GoS", "N Minimum", "Status (N=" + str(N) + ")", "Keterangan"]]
                    for t in targets_pdf:
                        mn = cari_n_minimum(S, A, t)
                        ok = N >= (mn if mn else 9999)
                        ket = "Terpenuhi ✓" if ok else "Perlu tambah kanal ✗"
                        rec_data.append([
                            f"≤ {t*100:.1f}%",
                            f"N ≥ {mn if mn else '–'}",
                            "✓ Ya" if ok else "✗ Tidak",
                            ket,
                        ])
                    rn = Table(rec_data, colWidths=[3.5*cm, 3.5*cm, 3.5*cm, 5*cm])
                    rn.setStyle(TableStyle([
                        ('BACKGROUND',   (0,0), (-1,0), TEAL_),
                        ('TEXTCOLOR',    (0,0), (-1,0), colors.white),
                        ('FONTNAME',     (0,0), (-1,0), 'Helvetica-Bold'),
                        ('FONTSIZE',     (0,0), (-1,-1), 8.5),
                        ('ALIGN',        (0,0), (-1,-1), 'CENTER'),
                        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, LGRAY]),
                        ('GRID',         (0,0), (-1,-1), 0.5, MGRAY),
                        ('TOPPADDING',   (0,0), (-1,-1), 6),
                        ('BOTTOMPADDING',(0,0), (-1,-1), 6),
                    ]))
                    el.append(rn)
                    el.append(Spacer(1, 0.5*cm))

                    # ══════════════════════════════════════════════════════════
                    # BAB 5 — GRAFIK ANALISIS
                    # ══════════════════════════════════════════════════════════
                    el.append(Paragraph("5.  Grafik Analisis", ch_title))
                    el.append(HRFlowable(width="100%", thickness=1, color=MGRAY, spaceAfter=10))
                    el.append(Paragraph(
                        "Grafik berikut memperlihatkan hubungan antara probabilitas blocking "
                        "dengan variasi parameter N (jumlah kanal) dan A (trafik yang ditawarkan).",
                        body))

                    el.append(RLImage(io.BytesIO(c1_bytes), width=15*cm, height=7*cm))
                    el.append(Paragraph(
                        f"Gambar 1. Kurva probabilitas blocking P(%) terhadap jumlah kanal N "
                        f"(S={S}, A={A:.1f} Erlang). Titik merah menunjukkan kondisi N={N} saat ini.",
                        caption_st))
                    el.append(Spacer(1, 0.5*cm))

                    el.append(RLImage(io.BytesIO(c2_bytes), width=15*cm, height=7*cm))
                    el.append(Paragraph(
                        f"Gambar 2. Kurva probabilitas blocking P(%) terhadap trafik A yang ditawarkan "
                        f"(S={S}, N={N} kanal). Titik merah menunjukkan kondisi A={A:.1f} Erl saat ini.",
                        caption_st))
                    el.append(Spacer(1, 0.5*cm))

                    # ══════════════════════════════════════════════════════════
                    # BAB 6 — KESIMPULAN
                    # ══════════════════════════════════════════════════════════
                    el.append(Paragraph("6.  Kesimpulan dan Rekomendasi", ch_title))
                    el.append(HRFlowable(width="100%", thickness=1, color=MGRAY, spaceAfter=10))

                    if P < 0.001:
                        kesimpulan_gos = (
                            f"Sistem saat ini beroperasi pada Grade of Service kategori "
                            f"<b>Sangat Baik</b> dengan probabilitas blocking P = {P:.6f} "
                            f"({P*100:.4f}%), jauh di bawah ambang 0,1%. "
                            f"Kualitas layanan memenuhi standar premium."
                        )
                    elif P < 0.01:
                        kesimpulan_gos = (
                            f"Sistem beroperasi pada GoS kategori <b>Baik</b> dengan P = {P:.6f} "
                            f"({P*100:.4f}%). Kualitas layanan memenuhi standar ITU-T (P &lt; 1%)."
                        )
                    elif P < 0.05:
                        kesimpulan_gos = (
                            f"Sistem beroperasi pada GoS kategori <b>Cukup</b> dengan P = {P:.6f} "
                            f"({P*100:.4f}%). Disarankan menambah jumlah kanal "
                            f"minimal N = {min_n_1} untuk mencapai GoS ≤ 1%."
                        )
                    else:
                        kesimpulan_gos = (
                            f"Sistem beroperasi pada GoS kategori <b>Buruk</b> dengan P = {P:.6f} "
                            f"({P*100:.4f}%). Diperlukan penambahan kanal segera. "
                            f"Jumlah kanal minimum yang diperlukan adalah N = {min_n_1} "
                            f"(untuk GoS ≤ 1%)."
                        )

                    el.append(Paragraph(kesimpulan_gos, body))
                    el.append(Paragraph(
                        f"Dari hasil perhitungan diperoleh bahwa trafik yang terlayani "
                        f"(traffic carried) sebesar <b>{carried:.4f} Erlang</b> dan trafik "
                        f"yang hilang (traffic lost) sebesar <b>{lost:.4f} Erlang</b> dari "
                        f"total <b>{A:.1f} Erlang</b> yang ditawarkan. "
                        f"Utilisasi rata-rata per kanal adalah <b>{util_pct:.2f}%</b>.",
                        body))

                    el.append(Spacer(1, 0.3*cm))
                    rek_data = [
                        ["No.", "Rekomendasi",                          "Nilai"],
                        ["1",   "Jumlah kanal saat ini",                f"N = {N}"],
                        ["2",   "N minimum untuk GoS ≤ 1%",            f"N = {min_n_1}"],
                        ["3",   "N minimum untuk GoS ≤ 0,1%",          f"N = {min_n_001}"],
                        ["4",   "Grade of Service saat ini",            gos_text],
                        ["5",   "Utilisasi kanal",                      f"{util_pct:.2f}%"],
                    ]
                    rk = Table(rek_data, colWidths=[1*cm, 10*cm, 4.5*cm])
                    rk.setStyle(TableStyle([
                        ('BACKGROUND',   (0,0), (-1,0), BLUE_),
                        ('TEXTCOLOR',    (0,0), (-1,0), colors.white),
                        ('FONTNAME',     (0,0), (-1,0), 'Helvetica-Bold'),
                        ('FONTSIZE',     (0,0), (-1,-1), 9),
                        ('ALIGN',        (0,0), (0,-1), 'CENTER'),
                        ('ALIGN',        (2,0), (2,-1), 'CENTER'),
                        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, LGRAY]),
                        ('GRID',         (0,0), (-1,-1), 0.5, MGRAY),
                        ('TOPPADDING',   (0,0), (-1,-1), 7),
                        ('BOTTOMPADDING',(0,0), (-1,-1), 7),
                    ]))
                    el.append(rk)
                    el.append(Spacer(1, 0.8*cm))

                    el.append(HRFlowable(width="100%", thickness=0.5,
                                          color=MGRAY, spaceAfter=10))
                    el.append(Paragraph(
                        f"EngsetPro v2.0  ·  Kalkulator Rekayasa Trafik Telekomunikasi  ·  "
                        f"Metode: Log-space Arithmetic  ·  "
                        f"Referensi: ITU-T E.501 / T. O. Engset (1918)  ·  "
                        f"Dicetak: {datetime.now().strftime('%d %B %Y')}",
                        footer_st))

                    # ── Build PDF ─────────────────────────────────────────────
                    doc.build(el)
                    buf_pdf.seek(0)

                st.download_button(
                    "📥  Klik untuk Mengunduh PDF",
                    data=buf_pdf,
                    file_name=f"laporan_engset_S{S}_N{N}_A{A:.1f}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )
                st.markdown('<div class="eng-ok">✅ PDF siap! Klik tombol di atas untuk mengunduh.</div>',
                            unsafe_allow_html=True)


# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;color:#aab5cc;font-size:0.75rem;
     padding:2.5rem 0 1rem;letter-spacing:0.04em;">
  EngsetPro v2.0 &nbsp;·&nbsp; Kalkulator Rekayasa Trafik Engset &nbsp;·&nbsp;
  Metode: Log-space Arithmetic &nbsp;·&nbsp; Referensi: ITU-T E.501
</div>
""", unsafe_allow_html=True)# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
  --blue-primary: #1a56ff;
  --blue-dark:    #0e3acc;
  --blue-deeper:  #0a2aaa;
  --teal:         #00c8b4;
  --teal-light:   #4dd9cb;
  --green:        #22c55e;
  --amber:        #f59e0b;
  --red:          #ef4444;
  --bg:           #f2f5fc;
  --white:        #ffffff;
  --navy:         #0d1b3e;
  --slate:        #3a5098;
  --muted:        #8899bb;
  --border:       rgba(26,86,255,0.08);
  --shadow-sm:    0 2px 12px rgba(26,86,255,0.07);
  --shadow-md:    0 6px 24px rgba(26,86,255,0.12);
  --shadow-lg:    0 12px 40px rgba(26,86,255,0.20);
  --radius-sm:    12px;
  --radius-md:    18px;
  --radius-lg:    24px;
}

html, body, [class*="css"] {
  font-family: 'Sora', sans-serif !important;
}

/* ── viewport meta for mobile ── */
head::before {
  display: none;
  content: '<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">';
}

.stApp {
  background: var(--bg) !important;
}

#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ═══════════ SIDEBAR ═══════════ */
[data-testid="stSidebar"] {
  background: linear-gradient(175deg, #1246e8 0%, #0c35c0 45%, #072590 100%) !important;
  border-right: none !important;
  box-shadow: 6px 0 30px rgba(10,42,170,0.30);
  min-width: 260px !important;
  max-width: 310px !important;
}
[data-testid="stSidebar"] > div:first-child { padding-top: 0 !important; }
[data-testid="stSidebar"] * { color: rgba(255,255,255,0.9) !important; }
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stNumberInput label {
  color: rgba(255,255,255,0.65) !important;
  font-size: 0.72rem !important;
  letter-spacing: 0.07em;
  text-transform: uppercase;
}
[data-testid="stSidebar"] hr {
  border-color: rgba(255,255,255,0.12) !important;
}

/* Radio nav items */
[data-testid="stSidebar"] [data-testid="stRadio"] > div {
  gap: 4px !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label {
  border-radius: 12px !important;
  padding: 10px 14px !important;
  transition: background 0.2s ease !important;
  font-size: 0.88rem !important;
  font-weight: 500 !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
  background: rgba(255,255,255,0.12) !important;
}

/* Group labels in sidebar */
.nav-group-label {
  font-size: 0.65rem;
  font-weight: 700;
  color: rgba(255,255,255,0.4) !important;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  margin: 16px 0 6px 6px;
}

/* ═══════════ BASE CARDS ═══════════ */
.card {
  background: var(--white);
  border-radius: var(--radius-md);
  padding: 1.4rem 1.6rem;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border);
  margin-bottom: 1rem;
}

.card-sm {
  background: var(--white);
  border-radius: var(--radius-sm);
  padding: 1rem 1.2rem;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border);
  margin-bottom: 0.75rem;
}

/* ═══════════ HERO GRADIENT CARD ═══════════ */
.hero-card {
  background: linear-gradient(135deg, #1a56ff 0%, #0a8fe8 55%, #00c8b4 100%);
  border-radius: var(--radius-lg);
  padding: 2rem 2rem 1.8rem;
  color: white;
  margin-bottom: 1rem;
  position: relative;
  overflow: hidden;
  box-shadow: 0 10px 40px rgba(26,86,255,0.40);
}
.hero-card::before {
  content: "";
  position: absolute; top: -80px; right: -50px;
  width: 260px; height: 260px; border-radius: 50%;
  background: rgba(255,255,255,0.07);
}
.hero-card::after {
  content: "";
  position: absolute; bottom: -60px; left: 35%;
  width: 200px; height: 200px; border-radius: 50%;
  background: rgba(255,255,255,0.05);
}
.hero-badge {
  display: inline-flex; align-items: center; gap: 6px;
  background: rgba(255,255,255,0.18);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255,255,255,0.25);
  border-radius: 100px;
  padding: 4px 14px;
  font-size: 0.7rem; font-weight: 700;
  letter-spacing: 0.1em; text-transform: uppercase;
  margin-bottom: 1rem;
  color: #fff;
}
.hero-stat-pill {
  background: rgba(255,255,255,0.16);
  backdrop-filter: blur(6px);
  border: 1px solid rgba(255,255,255,0.2);
  border-radius: 14px; padding: 10px 20px;
}

/* ═══════════ METRIC CHIPS ═══════════ */
.chip-grid {
  display: grid; grid-template-columns: repeat(3, 1fr);
  gap: 10px; margin-bottom: 1rem;
}
@media (max-width: 640px) {
  .chip-grid { grid-template-columns: repeat(2, 1fr); }
  .hero-card { padding: 1.2rem 1rem 1rem; }
  .hero-stat-pill { padding: 7px 12px; }
}
.chip {
  background: var(--white);
  border-radius: var(--radius-sm);
  padding: 1.1rem 0.8rem;
  text-align: center;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border);
  position: relative; overflow: hidden;
}
.chip::before {
  content: "";
  position: absolute; top: 0; left: 0; right: 0; height: 3px;
  background: linear-gradient(90deg, var(--blue-primary), var(--teal));
  border-radius: 3px 3px 0 0;
}
.chip-icon { font-size: 1.2rem; margin-bottom: 6px; }
.chip-val  {
  font-size: 1.05rem; font-weight: 700; color: var(--navy);
  font-family: 'JetBrains Mono', monospace;
}
.chip-lbl  {
  font-size: 0.65rem; color: var(--muted);
  text-transform: uppercase; letter-spacing: 0.07em; margin-top: 3px;
}

/* ═══════════ PLAN / RESULT ROWS ═══════════ */
.plan-card {
  background: var(--white);
  border-radius: var(--radius-sm);
  padding: 0.95rem 1.2rem;
  display: flex; align-items: center; gap: 14px;
  margin-bottom: 8px;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border);
  transition: box-shadow 0.2s, transform 0.2s;
}
.plan-card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-1px);
}
.plan-icon-wrap {
  width: 44px; height: 44px; border-radius: 13px;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.2rem; flex-shrink: 0;
}
.plan-icon-blue  { background: rgba(26,86,255,0.10); }
.plan-icon-teal  { background: rgba(0,200,180,0.10); }
.plan-icon-green { background: rgba(34,197,94,0.10); }
.plan-icon-amber { background: rgba(245,158,11,0.10); }
.plan-icon-red   { background: rgba(239,68,68,0.10); }
.plan-info { flex: 1; }
.plan-name { font-size: 0.88rem; font-weight: 600; color: var(--navy); margin: 0; }
.plan-desc { font-size: 0.75rem; color: var(--muted); margin: 2px 0 0; }
.plan-val  {
  font-size: 0.95rem; font-weight: 700; color: var(--blue-primary);
  font-family: 'JetBrains Mono', monospace;
}

/* ═══════════ GoS BADGE ═══════════ */
.gos {
  display: inline-block; padding: 4px 14px; border-radius: 100px;
  font-size: 0.75rem; font-weight: 700; letter-spacing: 0.04em;
}
.gos-great { background: #dcfce7; color: #166534; }
.gos-good  { background: #d1fae5; color: #065f46; }
.gos-ok    { background: #fef9c3; color: #713f12; }
.gos-bad   { background: #fee2e2; color: #7f1d1d; }

/* ═══════════ FORMULA BLOCK ═══════════ */
.formula-wrap {
  background: linear-gradient(135deg, #eef3ff 0%, #e4edff 100%);
  border: 1.5px solid #c7d7ff;
  border-radius: var(--radius-md);
  padding: 1.6rem 1.8rem; margin-bottom: 1rem;
}
.formula-tag {
  display: inline-block; background: var(--blue-primary); color: #fff;
  font-size: 0.65rem; font-weight: 700; letter-spacing: 0.1em;
  text-transform: uppercase; padding: 3px 12px; border-radius: 100px; margin-bottom: 1rem;
}
.formula-body {
  font-family: 'JetBrains Mono', monospace; font-size: 0.88rem;
  color: #0d2060; line-height: 2.4;
  background: rgba(255,255,255,0.65); border-radius: 10px;
  padding: 1.2rem 1.6rem;
  overflow-x: auto;
  white-space: pre;
}
.formula-legend { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-top: 1rem; }
@media (max-width: 480px) { .formula-legend { grid-template-columns: 1fr; } }
.fl-item { font-size: 0.78rem; color: var(--slate); display: flex; align-items: baseline; gap: 8px; }
.fl-sym  { font-family: 'JetBrains Mono', monospace; font-weight: 700; color: var(--blue-primary); min-width: 22px; }

/* ═══════════ SECTION TITLE ═══════════ */
.sec-title {
  font-size: 1rem; font-weight: 700; color: var(--navy); margin: 0 0 0.8rem;
  display: flex; align-items: center; gap: 6px;
}

/* ═══════════ ALERT BANNERS ═══════════ */
.eng-warn {
  background: #fff7ed; border: 1px solid #fed7aa;
  border-left: 4px solid #f59e0b;
  border-radius: var(--radius-sm); padding: 0.85rem 1.1rem;
  color: #92400e; font-size: 0.85rem; margin-bottom: 1rem;
}
.eng-info {
  background: #eff6ff; border: 1px solid #bfdbfe;
  border-left: 4px solid var(--blue-primary);
  border-radius: var(--radius-sm); padding: 0.85rem 1.1rem;
  color: #1e40af; font-size: 0.85rem; margin-bottom: 1rem;
}
.eng-ok {
  background: #f0fdf4; border: 1px solid #bbf7d0;
  border-left: 4px solid var(--green);
  border-radius: var(--radius-sm); padding: 0.85rem 1.1rem;
  color: #166534; font-size: 0.85rem; margin-bottom: 1rem;
}

/* ═══════════ TABLE ═══════════ */
.eng-table {
  width: 100%; border-collapse: collapse; font-size: 0.83rem;
  border-radius: var(--radius-sm); overflow: hidden;
}
.eng-table th {
  background: linear-gradient(90deg, var(--blue-primary), var(--blue-dark));
  color: #fff; font-size: 0.68rem;
  text-transform: uppercase; letter-spacing: 0.08em;
  padding: 10px 14px; text-align: left; font-weight: 600;
}
.eng-table td {
  padding: 9px 14px; border-bottom: 1px solid #f0f4ff;
  color: #2d3a5e; font-family: 'JetBrains Mono', monospace; font-size: 0.8rem;
}
.eng-table tr:hover td { background: #f5f8ff; }
.eng-table tr.active td { background: #eff6ff; font-weight: 600; color: var(--navy); }

/* ═══════════ BUTTONS ═══════════ */
.stButton > button {
  background: linear-gradient(135deg, #1a56ff, #0e3acc) !important;
  color: #fff !important; border: none !important;
  border-radius: var(--radius-sm) !important;
  padding: 0.65rem 1.6rem !important; font-weight: 700 !important;
  font-size: 0.88rem !important;
  box-shadow: 0 4px 16px rgba(26,86,255,0.3) !important;
  transition: all 0.2s ease !important;
  font-family: 'Sora', sans-serif !important;
}
.stButton > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 24px rgba(26,86,255,0.4) !important;
}

/* ═══════════ PROGRESS BAR ═══════════ */
.progress-wrap {
  background: #e8efff; border-radius: 100px; height: 8px;
  margin: 6px 0; overflow: hidden;
}
.progress-fill {
  height: 100%; border-radius: 100px;
  background: linear-gradient(90deg, var(--blue-primary), var(--teal));
  transition: width 0.5s ease;
}

/* ═══════════ TABS ═══════════ */
.stTabs [data-baseweb="tab-list"] {
  background: #edf1fb; border-radius: 14px; padding: 4px; gap: 4px; border: none;
  flex-wrap: wrap;
}
.stTabs [data-baseweb="tab"] {
  border-radius: 10px; font-weight: 600; font-size: 0.86rem;
  color: var(--muted); padding: 8px 20px;
  font-family: 'Sora', sans-serif;
}
.stTabs [aria-selected="true"] {
  background: var(--white) !important; color: var(--blue-primary) !important;
  box-shadow: 0 2px 10px rgba(26,86,255,0.14) !important;
}

/* ═══════════ PAGE HEADER ═══════════ */
.page-header {
  margin-bottom: 1.6rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #eaeffe;
}
.page-header-tag {
  font-size: 0.68rem; color: var(--blue-primary); font-weight: 700;
  text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 4px;
}
.page-header-title {
  font-size: 1.75rem; font-weight: 800; color: var(--navy); margin: 0;
  letter-spacing: -0.02em;
}
.page-header-sub {
  color: var(--muted); margin: 4px 0 0; font-size: 0.88rem;
}

/* ═══════════ STAT RESULT BOX ═══════════ */
.result-hero {
  background: linear-gradient(135deg, #eef3ff, #e4edff);
  border: 1.5px solid #c7d7ff;
  border-radius: var(--radius-md);
  padding: 1.4rem; text-align: center; margin-bottom: 1rem;
}
.result-hero-label {
  font-size: 0.7rem; color: var(--slate); text-transform: uppercase;
  letter-spacing: 0.08em; margin-bottom: 6px;
}
.result-hero-val {
  font-size: 2.4rem; font-weight: 800; color: var(--blue-primary);
  font-family: 'JetBrains Mono', monospace; line-height: 1;
}
.result-hero-unit {
  font-size: 0.82rem; color: var(--muted); margin-top: 6px;
}

/* ═══════════ DATA ROW ═══════════ */
.data-row {
  display: flex; justify-content: space-between; align-items: center;
  padding: 10px 0; border-bottom: 1px solid #f0f4ff;
  flex-wrap: wrap; gap: 4px;
}
.data-row:last-child { border-bottom: none; }
.data-row-label { font-size: 0.82rem; color: var(--muted); }
.data-row-val {
  font-size: 0.85rem; font-weight: 700; color: var(--navy);
  font-family: 'JetBrains Mono', monospace;
}

/* ═══════════ MOBILE RESPONSIVE FIXES ═══════════ */
@media (max-width: 768px) {
  .page-header-title { font-size: 1.3rem !important; }
  .result-hero-val   { font-size: 1.8rem !important; }
  .plan-card         { flex-wrap: wrap; }
  .eng-table         { font-size: 0.72rem; }
  .eng-table th, .eng-table td { padding: 7px 8px; }
  .formula-body      { font-size: 0.75rem; padding: 0.9rem 1rem; }
  [data-testid="stSidebar"] {
    min-width: 80vw !important;
    max-width: 90vw !important;
  }
}
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# CORE ENGSET — Numerik stabil menggunakan log-space arithmetic
# ═══════════════════════════════════════════════════════════════════════════════
def log_faktorial(n):
    """Menghitung ln(n!) secara iteratif."""
    if n <= 1:
        return 0.0
    return sum(log(i) for i in range(2, n + 1))

def log_kombinasi(n, k):
    """Menghitung ln C(n,k) = ln(n!) − ln(k!) − ln((n−k)!)."""
    if k < 0 or k > n:
        return float('-inf')
    return log_faktorial(n) - log_faktorial(k) - log_faktorial(n - k)

def engset(S, N, A):
    """
    Menghitung probabilitas blocking Engset.

    Rumus (bentuk rekursif log-space):
        P(S, N, A) = C(S-1, N) · ρ^N  /  Σ[i=0..N] C(S-1, i) · ρ^i
    di mana ρ = A / (S − A) adalah rasio intensitas trafik.

    Parameter
    ----------
    S : int   — jumlah sumber (source / pengguna)
    N : int   — jumlah kanal (server)
    A : float — trafik yang ditawarkan (Erlang)

    Kembalian
    ---------
    float : probabilitas blocking [0, 1], atau None jika parameter tidak valid.
    """
    if A <= 0 or A >= S or N <= 0 or S <= N:
        return None
    rho = A / (S - A)
    if rho <= 0:
        return None
    log_rho   = log(rho)
    log_numer = log_kombinasi(S - 1, N) + N * log_rho
    log_terms = [log_kombinasi(S - 1, i) + i * log_rho for i in range(N + 1)]
    max_t     = max(log_terms)
    log_denom = max_t + log(sum(exp(t - max_t) for t in log_terms))
    return max(0.0, min(1.0, exp(log_numer - log_denom)))

def label_gos(p):
    """Menentukan label Grade of Service berdasarkan probabilitas blocking."""
    if p < 0.001:
        return "Sangat Baik", "gos-great"
    if p < 0.01:
        return "Baik", "gos-good"
    if p < 0.05:
        return "Cukup", "gos-ok"
    return "Buruk", "gos-bad"

def cari_n_minimum(S, A, target=0.01):
    """Mencari jumlah kanal minimum agar P_blocking ≤ target."""
    for n in range(1, S):
        p = engset(S, n, A)
        if p is not None and p <= target:
            return n
    return None


# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    # Logo / brand
    st.markdown("""
    <div style="background:rgba(255,255,255,0.10);border-radius:18px;
         padding:1.4rem 1.2rem 1.1rem;margin-bottom:1.4rem;text-align:center;">
      <div style="font-size:2.2rem;margin-bottom:2px;">📡</div>
      <div style="font-size:1.35rem;font-weight:800;color:#fff;letter-spacing:-0.01em;">EngsetPro</div>
      <div style="font-size:0.65rem;color:rgba(255,255,255,0.5);letter-spacing:0.1em;
           text-transform:uppercase;margin-top:2px;">Rekayasa Trafik v2.0</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="nav-group-label">Menu Utama</div>', unsafe_allow_html=True)
    page = st.radio("nav", [
        "🏠  Dashboard",
        "🧮  Kalkulator Engset",
        "📊  Analisis & Grafik",
        "📄  Ekspor Laporan",
    ], label_visibility="collapsed")

    st.markdown('<div class="nav-group-label">Hitung Trafik A</div>', unsafe_allow_html=True)
    page_a = st.radio("nav_a", [
        "📞  A — Call Rate & Hold Time",
        "👥  A — Pengguna Aktif (BHT)",
        "🔁  A — Data Rate / Throughput",
    ], label_visibility="collapsed")

    st.markdown("---")
    st.markdown('<div class="nav-group-label">Parameter Sistem</div>', unsafe_allow_html=True)

    S = st.slider("S — Jumlah Source", 2, 200, 20, 1)
    N = st.slider("N — Jumlah Kanal",  1, 100,  5, 1)
    A = st.slider("A — Trafik yang Ditawarkan (Erl)", 0.1, float(max(1, S-1)), min(8.0, float(S-2)), 0.1)

    st.markdown("---")
    st.markdown(f"""
    <div style="background:rgba(255,255,255,0.08);border-radius:14px;padding:1rem;">
      <div style="font-size:0.65rem;color:rgba(255,255,255,0.45);text-transform:uppercase;
           letter-spacing:0.1em;margin-bottom:8px;">Sesi Saat Ini</div>
      <div style="font-size:0.82rem;color:rgba(255,255,255,0.85);line-height:2.1;">
        S = <strong>{S}</strong> pengguna<br>
        N = <strong>{N}</strong> kanal<br>
        A = <strong>{A:.1f}</strong> Erlang
      </div>
      <div style="font-size:0.68rem;color:rgba(255,255,255,0.38);margin-top:8px;">
        {datetime.now().strftime('%d %b %Y · %H:%M')}</div>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# HITUNG
# ═══════════════════════════════════════════════════════════════════════════════
valid     = S > N and 0 < A < S
P         = engset(S, N, A) if valid else None
carried   = A * (1 - P)     if P is not None else 0.0
lost      = A * P            if P is not None else 0.0
util_pct  = (carried / N) * 100 if (P is not None and N > 0) else 0.0
gos_text, gos_cls = label_gos(P) if P is not None else ("—", "gos-ok")
min_n_1   = cari_n_minimum(S, A, 0.01)  if valid else "—"
min_n_001 = cari_n_minimum(S, A, 0.001) if valid else "—"

BLUE  = '#1a56ff'
TEAL  = '#00c8b4'
AMBER = '#f59e0b'
RED   = '#ef4444'
GREEN = '#22c55e'
BG    = '#f8faff'


# ═══════════════════════════════════════════════════════════════════════════════
# PENENTUAN HALAMAN AKTIF
# ═══════════════════════════════════════════════════════════════════════════════
if "last_nav" not in st.session_state:
    st.session_state["last_nav"] = "main"

prev_page   = st.session_state.get("prev_page",   page)
prev_page_a = st.session_state.get("prev_page_a", page_a)

if page != prev_page:
    st.session_state["last_nav"] = "main"
elif page_a != prev_page_a:
    st.session_state["last_nav"] = "a"

st.session_state["prev_page"]   = page
st.session_state["prev_page_a"] = page_a

active_page = page if st.session_state["last_nav"] == "main" else page_a


# ═══════════════════════════════════════════════════════════════════════════════
# HELPER — Header halaman
# ═══════════════════════════════════════════════════════════════════════════════
def page_header(tag, title, sub):
    st.markdown(f"""
    <div class="page-header">
      <div class="page-header-tag">{tag}</div>
      <h1 class="page-header-title">{title}</h1>
      <p class="page-header-sub">{sub}</p>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# HELPER — Donut chart (matplotlib)
# ═══════════════════════════════════════════════════════════════════════════════
def donut_chart(val_pct, label_center, label_bottom, color=BLUE, bg='#e8efff'):
    fig, ax = plt.subplots(figsize=(3.8, 3.8))
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')
    sizes = [val_pct, max(0, 100 - val_pct)]
    clrs  = [color, bg]
    ax.pie(sizes, colors=clrs, startangle=90,
           wedgeprops=dict(width=0.44, edgecolor='white', linewidth=3),
           counterclock=False)
    ax.text(0, 0.08, label_center,
            ha='center', va='center', fontsize=18, fontweight='bold',
            color='#0d1b3e', fontfamily='monospace')
    ax.text(0, -0.24, label_bottom,
            ha='center', va='center', fontsize=9, color='#8899bb')
    ax.axis('equal')
    plt.tight_layout(pad=0.3)
    return fig


# ══════════════════════════════════════════════════════════════════════════════
# ██ DASHBOARD
# Menampilkan ringkasan cepat: probabilitas blocking, carried/lost traffic,
# utilisasi kanal, dan rekomendasi jumlah kanal minimum.
# ══════════════════════════════════════════════════════════════════════════════
if active_page == "🏠  Dashboard":

    col_main, col_side = st.columns([2.1, 1], gap="large")

    with col_main:
        st.markdown(f"""
        <div class="hero-card">
          <div class="hero-badge">📡 EngsetPro · Model Finite Source</div>
          <h1 style="font-size:1.65rem;font-weight:800;color:#fff;margin:0 0 0.3rem;
               line-height:1.15;">Dashboard Analisis<br>Engset</h1>
          <p style="font-size:0.85rem;opacity:0.75;margin:0 0 1.4rem;">
            Probabilitas blocking real-time — Model Engset Finite Source</p>
          <div style="display:flex;gap:10px;flex-wrap:wrap;">
            <div class="hero-stat-pill">
              <div style="font-size:0.62rem;opacity:0.7;text-transform:uppercase;
                   letter-spacing:0.08em;margin-bottom:1px;">Source</div>
              <div style="font-size:1.3rem;font-weight:800;
                   font-family:'JetBrains Mono',monospace;">S = {S}</div>
            </div>
            <div class="hero-stat-pill">
              <div style="font-size:0.62rem;opacity:0.7;text-transform:uppercase;
                   letter-spacing:0.08em;margin-bottom:1px;">Kanal</div>
              <div style="font-size:1.3rem;font-weight:800;
                   font-family:'JetBrains Mono',monospace;">N = {N}</div>
            </div>
            <div class="hero-stat-pill">
              <div style="font-size:0.62rem;opacity:0.7;text-transform:uppercase;
                   letter-spacing:0.08em;margin-bottom:1px;">Trafik</div>
              <div style="font-size:1.3rem;font-weight:800;
                   font-family:'JetBrains Mono',monospace;">A = {A:.1f}</div>
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
                <div class="chip-lbl">Trafik Terlayani (Erl)</div>
              </div>
              <div class="chip">
                <div class="chip-icon">❌</div>
                <div class="chip-val">{lost:.3f}</div>
                <div class="chip-lbl">Trafik Hilang (Erl)</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<p class="sec-title">📋 Ringkasan Sistem</p>', unsafe_allow_html=True)

        items = [
            ("📶", "plan-icon-blue",  "Probabilitas Blocking", f"{P*100:.3f}%" if P else "—",  f"Grade: {gos_text}"),
            ("🔄", "plan-icon-teal",  "Trafik Terlayani",      f"{carried:.4f} Erl",             f"dari {A:.1f} Erl yang ditawarkan"),
            ("📉", "plan-icon-amber", "N Min untuk GoS ≤ 1%",  f"N = {min_n_1}",                "untuk kualitas layanan baik"),
            ("⚡", "plan-icon-red",   "Utilisasi Kanal",        f"{util_pct:.1f}%",              f"rata-rata per {N} kanal"),
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
        fig_d = donut_chart(
            util_pct,
            f"{util_pct:.1f}%" if P else "—",
            "utilisasi kanal",
            color=BLUE,
        )
        st.pyplot(fig_d, use_container_width=True)
        plt.close(fig_d)

        pbar_w  = min(100, (P or 0) * 500)
        bar_col = GREEN if (P or 1) < 0.01 else AMBER if (P or 1) < 0.05 else RED
        st.markdown(f"""
        <div class="card" style="text-align:center;padding:1.3rem;">
          <div style="font-size:0.68rem;color:var(--muted);text-transform:uppercase;
               letter-spacing:0.08em;margin-bottom:8px;">Grade of Service</div>
          <span class="gos {gos_cls}" style="font-size:0.95rem;padding:7px 22px;">{gos_text}</span>
          <div style="margin-top:12px;">
            <div class="progress-wrap">
              <div class="progress-fill" style="width:{pbar_w:.1f}%;background:{bar_col};"></div>
            </div>
          </div>
          <div style="font-size:0.75rem;color:var(--muted);margin-top:6px;">
            P = {f"{P:.6f}" if P is not None else "—"}
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="card">
          <div style="font-size:0.85rem;font-weight:700;color:var(--navy);margin-bottom:10px;">
            🎯 Rekomendasi Kanal</div>
          <div style="font-size:0.82rem;color:var(--slate);line-height:2.3;">
            GoS ≤ 1%&nbsp;&nbsp;&nbsp;→
            <strong style="color:var(--blue-primary);">N = {min_n_1}</strong><br>
            GoS ≤ 0,1% →
            <strong style="color:var(--blue-primary);">N = {min_n_001}</strong>
          </div>
        </div>
        """, unsafe_allow_html=True)

        if not valid:
            st.markdown('<div class="eng-warn">⚠️ Pastikan S &gt; N dan A &lt; S</div>',
                        unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ██ KALKULATOR ENGSET
# Menampilkan rumus Engset lengkap, langkah-langkah perhitungan,
# hasil numerik detail, dan tabel rekomendasi N minimum.
# ══════════════════════════════════════════════════════════════════════════════
elif active_page == "🧮  Kalkulator Engset":
    page_header("Rekayasa Trafik", "Kalkulator Engset",
                "Hitung probabilitas blocking dengan model finite source Engset")

    # ── Rumus Engset standar notasi matematika ──────────────────────────────
    st.markdown("""
    <div class="formula-wrap">
      <span class="formula-tag">Rumus Engset — Model Finite Source (ITU-T)</span>
      <div class="formula-body">
              C(S−1, N) · ρᴺ
P(S, N, A) = ─────────────────────────
               N
              Σ  C(S−1, i) · ρⁱ
             i=0

                    A
di mana:  ρ = ─────────
               S − A</div>
      <div class="formula-legend">
        <div class="fl-item"><span class="fl-sym">P</span> Probabilitas blocking</div>
        <div class="fl-item"><span class="fl-sym">S</span> Jumlah sumber (pengguna)</div>
        <div class="fl-item"><span class="fl-sym">N</span> Jumlah kanal (server)</div>
        <div class="fl-item"><span class="fl-sym">A</span> Trafik yang ditawarkan (Erlang)</div>
        <div class="fl-item"><span class="fl-sym">ρ</span> Rasio intensitas trafik = A/(S−A)</div>
        <div class="fl-item"><span class="fl-sym">C(n,k)</span> Koefisien binomial = n! / (k!(n−k)!)</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if not valid:
        st.markdown('<div class="eng-warn">⚠️ Pastikan S &gt; N dan A &lt; S pada sidebar.</div>',
                    unsafe_allow_html=True)
    else:
        col1, col2 = st.columns([1.2, 1], gap="large")

        with col1:
            st.markdown('<p class="sec-title">📊 Hasil Perhitungan</p>', unsafe_allow_html=True)
            rows = [
                ("📡", "plan-icon-blue",  "Probabilitas Blocking (P)", f"{P:.8f}",        "probabilitas"),
                ("📈", "plan-icon-blue",  "Blocking (Persentase)",      f"{P*100:.4f}%",   "persentase terblokir"),
                ("🏆", "plan-icon-green", "Grade of Service",            gos_text,           "penilaian kualitas"),
                ("✅", "plan-icon-teal",  "Trafik Terlayani",            f"{carried:.4f} Erl","traffic carried"),
                ("❌", "plan-icon-red",   "Trafik Hilang",               f"{lost:.4f} Erl",  "traffic lost"),
                ("⚡", "plan-icon-amber", "Utilisasi Kanal",             f"{util_pct:.2f}%", "per kanal"),
                ("📶", "plan-icon-blue",  "Intensitas Trafik per Kanal", f"{A/N:.4f} Erl/ch","per kanal"),
            ]
            for icon, icon_cls, label, val, unit in rows:
                st.markdown(f"""
                <div class="plan-card" style="padding:0.85rem 1.1rem;">
                  <div class="plan-icon-wrap {icon_cls}"
                       style="width:38px;height:38px;border-radius:10px;font-size:1.1rem;">{icon}</div>
                  <div class="plan-info">
                    <p class="plan-name" style="font-size:0.84rem;">{label}</p>
                    <p class="plan-desc">{unit}</p>
                  </div>
                  <div class="plan-val" style="font-size:0.92rem;">{val}</div>
                </div>
                """, unsafe_allow_html=True)

        with col2:
            fig_du = donut_chart(util_pct, f"{util_pct:.1f}%", "utilisasi", color=BLUE)
            st.pyplot(fig_du, use_container_width=True)
            plt.close(fig_du)

            st.markdown('<p class="sec-title">🎯 Rekomendasi N Minimum</p>', unsafe_allow_html=True)
            targets = [0.10, 0.05, 0.02, 0.01, 0.005, 0.001]
            rec_rows = ""
            for t in targets:
                mn = cari_n_minimum(S, A, t)
                ok = N >= (mn if mn else 9999)
                rec_rows += (f'<tr><td>≤ {t*100:.1f}%</td>'
                             f'<td>N ≥ {mn if mn else "–"}</td>'
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
                st.markdown('<div class="eng-warn">⚠️ Cukup — pertimbangkan penambahan kanal</div>',
                            unsafe_allow_html=True)
            else:
                st.markdown('<div class="eng-warn">🔴 Buruk — tambah kanal segera!</div>',
                            unsafe_allow_html=True)

            with st.expander("🔢 Lihat langkah-langkah perhitungan"):
                rho = A / (S - A)
                st.markdown(f"""
**Langkah 1 — Hitung rasio intensitas trafik (ρ):**
```
ρ = A / (S − A)
  = {A:.2f} / ({S} − {A:.2f})
  = {rho:.6f}
```
**Langkah 2 — Hitung pembilang:**
```
C(S−1, N) · ρᴺ
= C({S-1}, {N}) · {rho:.6f}^{N}
```
**Langkah 3 — Hitung penyebut:**
```
N
Σ C(S−1, i) · ρⁱ   (i = 0, 1, ..., {N})
i=0
= Σ C({S-1}, i) · {rho:.6f}^i
```
**Langkah 4 — Hasil akhir:**
```
P = pembilang / penyebut
P = {P:.8f}
P = {P*100:.4f}%
```
                """)


# ══════════════════════════════════════════════════════════════════════════════
# ██ HITUNG A — CALL RATE & HOLD TIME
# Menghitung trafik Erlang dari laju panggilan (λ) dan durasi holding (h).
# ══════════════════════════════════════════════════════════════════════════════
elif active_page == "📞  A — Call Rate & Hold Time":
    page_header("Hitung Trafik A", "Call Rate & Hold Time",
                "Hitung Erlang dari λ (laju panggilan) dan h (durasi holding)")

    st.markdown("""
    <div class="formula-wrap">
      <span class="formula-tag">Rumus Erlang — Metode 1: Call Rate</span>
      <div class="formula-body">
A = λ · h

λ = laju panggilan per pengguna (panggilan/jam)
h = rata-rata durasi panggilan (menit)

Konversi satuan:
λ [call/s] = λ [call/jam] / 3600
h [detik]  = h [menit] × 60

Sehingga: A [Erl] = λ [call/s] × h [s]</div>
      <div class="formula-legend">
        <div class="fl-item"><span class="fl-sym">A</span> Trafik per pengguna (Erlang)</div>
        <div class="fl-item"><span class="fl-sym">λ</span> Laju panggilan (call/jam)</div>
        <div class="fl-item"><span class="fl-sym">h</span> Rata-rata durasi panggilan (menit)</div>
        <div class="fl-item"><span class="fl-sym">A_tot</span> Trafik total = A × jumlah pengguna</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.85rem;font-weight:700;color:#0d1b3e;margin-bottom:1rem;">⚙️ Input Parameter</div>',
                    unsafe_allow_html=True)
        call_rate  = st.number_input("λ — Laju panggilan (panggilan/jam per pengguna)",
                                     0.01, 1000.0, 3.0, 0.1, format="%.2f")
        hold_time  = st.number_input("h — Rata-rata durasi panggilan (menit)",
                                     0.1, 120.0, 2.0, 0.1, format="%.1f")
        n_users_t1 = st.number_input("Jumlah pengguna aktif (untuk A total)",
                                     1, 10000, S)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        lam_s = call_rate / 3600
        h_s   = hold_time * 60
        A_1   = lam_s * h_s
        A_tot = A_1 * n_users_t1

        st.markdown(f"""
        <div class="card">
          <div style="font-size:0.85rem;font-weight:700;color:#0d1b3e;margin-bottom:1rem;">📊 Hasil Konversi</div>
          <div class="data-row">
            <span class="data-row-label">Trafik per pengguna (A)</span>
            <span class="data-row-val" style="color:#1a56ff;">{A_1:.6f} Erl</span>
          </div>
          <div class="data-row">
            <span class="data-row-label">λ → konversi ke/detik</span>
            <span class="data-row-val">{lam_s:.6f} call/s</span>
          </div>
          <div class="data-row">
            <span class="data-row-label">h → konversi ke detik</span>
            <span class="data-row-val">{h_s:.0f} detik</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="result-hero">
          <div class="result-hero-label">A Total ({n_users_t1} pengguna)</div>
          <div class="result-hero-val">{A_tot:.4f}</div>
          <div class="result-hero-unit">Erlang — masukkan ke sidebar sebagai nilai A</div>
        </div>
        """, unsafe_allow_html=True)

        if 0 < A_tot < S and S > N:
            P2 = engset(S, N, A_tot)
            if P2:
                g2, gc2 = label_gos(P2)
                cls = "eng-ok" if P2 < 0.01 else "eng-warn"
                st.markdown(f'<div class="{cls}"><strong>Hasil Engset</strong> dengan '
                            f'A = {A_tot:.4f} Erl, S = {S}, N = {N}:<br>'
                            f'P = {P2:.6f} · Blocking = {P2*100:.3f}% · GoS = {g2}</div>',
                            unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ██ HITUNG A — PENGGUNA AKTIF (BHT)
# Menghitung trafik Erlang menggunakan metode Busy Hour Traffic (BHT).
# ══════════════════════════════════════════════════════════════════════════════
elif active_page == "👥  A — Pengguna Aktif (BHT)":
    page_header("Hitung Trafik A", "Pengguna Aktif — Metode BHT",
                "Hitung Erlang dari jumlah pengguna aktif di jam sibuk")

    st.markdown("""
    <div class="formula-wrap">
      <span class="formula-tag">Rumus BHT — Metode 2: Busy Hour Traffic</span>
      <div class="formula-body">
A = U × BHT

U   = jumlah pengguna aktif di jam sibuk
BHT = Busy Hour Traffic per pengguna (Erlang/pengguna)</div>
      <div class="formula-legend">
        <div class="fl-item"><span class="fl-sym">A</span> Trafik total yang ditawarkan (Erlang)</div>
        <div class="fl-item"><span class="fl-sym">U</span> Jumlah pengguna aktif jam sibuk</div>
        <div class="fl-item"><span class="fl-sym">BHT</span> Trafik per pengguna di jam sibuk (Erl)</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.85rem;font-weight:700;color:#0d1b3e;margin-bottom:1rem;">⚙️ Input Parameter</div>',
                    unsafe_allow_html=True)
        U_val = st.number_input("U — Pengguna aktif di jam sibuk", 1, 10000, 50)
        BHT   = st.number_input("BHT — Busy Hour Traffic per pengguna (Erl)",
                                 0.001, 1.0, 0.1, 0.001, format="%.3f")
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        A_t2 = U_val * BHT

        st.markdown(f"""
        <div class="card">
          <div style="font-size:0.85rem;font-weight:700;color:#0d1b3e;margin-bottom:1rem;">📊 Detail Perhitungan</div>
          <div class="data-row">
            <span class="data-row-label">Pengguna aktif (U)</span>
            <span class="data-row-val">{U_val} pengguna</span>
          </div>
          <div class="data-row">
            <span class="data-row-label">BHT per pengguna</span>
            <span class="data-row-val">{BHT:.3f} Erl</span>
          </div>
          <div class="data-row">
            <span class="data-row-label">A = U × BHT = {U_val} × {BHT:.3f}</span>
            <span class="data-row-val">{A_t2:.4f} Erl</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="result-hero">
          <div class="result-hero-label">A Total (Metode BHT)</div>
          <div class="result-hero-val">{A_t2:.4f}</div>
          <div class="result-hero-unit">Erlang — masukkan ke sidebar sebagai nilai A</div>
        </div>
        """, unsafe_allow_html=True)

        if 0 < A_t2 < S and S > N:
            P3 = engset(S, N, A_t2)
            if P3:
                g3, gc3 = label_gos(P3)
                cls = "eng-ok" if P3 < 0.01 else "eng-warn"
                st.markdown(f'<div class="{cls}">P = {P3:.6f} · Blocking = {P3*100:.3f}% · GoS = {g3}</div>',
                            unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ██ HITUNG A — DATA RATE / THROUGHPUT
# Menghitung trafik Erlang berdasarkan perbandingan data rate total
# terhadap kapasitas per kanal.
# ══════════════════════════════════════════════════════════════════════════════
elif active_page == "🔁  A — Data Rate / Throughput":
    page_header("Hitung Trafik A", "Data Rate / Throughput",
                "Hitung Erlang dari data rate total dan kapasitas per kanal")

    st.markdown("""
    <div class="formula-wrap">
      <span class="formula-tag">Rumus Data Rate — Metode 3: Throughput</span>
      <div class="formula-body">
          R_total
A = ─────────────
         R_ch

R_total = data rate total yang diminta (Mbps)
R_ch    = kapasitas (throughput) per kanal (Mbps)</div>
      <div class="formula-legend">
        <div class="fl-item"><span class="fl-sym">A</span> Trafik yang ditawarkan (Erlang)</div>
        <div class="fl-item"><span class="fl-sym">R_total</span> Data rate total agregat (Mbps)</div>
        <div class="fl-item"><span class="fl-sym">R_ch</span> Kapasitas throughput per kanal (Mbps)</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.85rem;font-weight:700;color:#0d1b3e;margin-bottom:1rem;">⚙️ Input Parameter</div>',
                    unsafe_allow_html=True)
        dr = st.number_input("R_total — Data Rate Total (Mbps)", 0.1, 100000.0, 100.0, 1.0)
        cc = st.number_input("R_ch — Kapasitas per Kanal (Mbps)", 0.1, 10000.0, 10.0, 0.1)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        A_t3 = dr / cc

        st.markdown(f"""
        <div class="card">
          <div style="font-size:0.85rem;font-weight:700;color:#0d1b3e;margin-bottom:1rem;">📊 Detail Perhitungan</div>
          <div class="data-row">
            <span class="data-row-label">Data Rate Total (R_total)</span>
            <span class="data-row-val">{dr:.1f} Mbps</span>
          </div>
          <div class="data-row">
            <span class="data-row-label">Kapasitas per Kanal (R_ch)</span>
            <span class="data-row-val">{cc:.1f} Mbps</span>
          </div>
          <div class="data-row">
            <span class="data-row-label">A = R_total / R_ch = {dr:.1f} / {cc:.1f}</span>
            <span class="data-row-val">{A_t3:.4f} Erl</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="result-hero">
          <div class="result-hero-label">A Total (Metode Data Rate)</div>
          <div class="result-hero-val">{A_t3:.4f}</div>
          <div class="result-hero-unit">Erlang — masukkan ke sidebar sebagai nilai A</div>
        </div>
        """, unsafe_allow_html=True)

        if 0 < A_t3 < S and S > N:
            P4 = engset(S, N, A_t3)
            if P4:
                g4, gc4 = label_gos(P4)
                cls = "eng-ok" if P4 < 0.01 else "eng-warn"
                st.markdown(f'<div class="{cls}">P = {P4:.6f} · Blocking = {P4*100:.3f}% · GoS = {g4}</div>',
                            unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ██ ANALISIS & GRAFIK
# Menampilkan tiga grafik: Blocking vs N, Blocking vs A, dan multi-kurva
# perbandingan berbagai nilai A, serta tabel detail per nilai N.
# ══════════════════════════════════════════════════════════════════════════════
elif active_page == "📊  Analisis & Grafik":
    page_header("Visualisasi", "Analisis & Grafik",
                "Visualisasi perilaku sistem terhadap variasi parameter Engset")

    if not valid:
        st.markdown('<div class="eng-warn">⚠️ Periksa parameter di sidebar.</div>',
                    unsafe_allow_html=True)
    else:
        cg1, cg2 = st.columns(2, gap="large")

        # ── Grafik 1: Blocking vs N ──────────────────────────────────────────
        with cg1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("##### 📈 Blocking vs Jumlah Kanal (N)")
            max_n = min(S-1, 50)
            ns_   = list(range(1, max_n+1))
            ps_   = [(engset(S,n,A) or 0)*100 for n in ns_]

            fig1, ax1 = plt.subplots(figsize=(5.5, 3.8))
            fig1.patch.set_facecolor(BG); ax1.set_facecolor(BG)
            ax1.fill_between(ns_, ps_, alpha=0.13, color=BLUE)
            ax1.plot(ns_, ps_, color=BLUE, linewidth=2.5, zorder=3)
            ax1.scatter([N], [P*100], color=RED, s=90, zorder=5,
                        label=f'N={N}, P={P*100:.3f}%')
            ax1.axhline(1.0, color=AMBER, linestyle='--', linewidth=1.2, alpha=0.8)
            ax1.text(max_n*0.97, 1.05, 'GoS 1%', ha='right', fontsize=8, color=AMBER)
            ax1.axhline(0.1, color=TEAL, linestyle='--', linewidth=1.2, alpha=0.8)
            ax1.text(max_n*0.97, 0.15, 'GoS 0,1%', ha='right', fontsize=8, color=TEAL)
            ax1.set_xlabel('N — Jumlah Kanal', fontsize=9, color='#5a6a8e')
            ax1.set_ylabel('Blocking (%)', fontsize=9, color='#5a6a8e')
            ax1.set_title(f'S={S}, A={A:.1f} Erl', fontsize=9, color='#8899bb')
            ax1.legend(fontsize=8.5)
            ax1.grid(True, linestyle='--', alpha=0.3)
            ax1.spines[['top','right']].set_visible(False)
            ax1.tick_params(colors='#8899bb', labelsize=8)
            plt.tight_layout(pad=1.0)
            st.pyplot(fig1, use_container_width=True)
            plt.close(fig1)
            st.markdown('</div>', unsafe_allow_html=True)

        # ── Grafik 2: Blocking vs A ──────────────────────────────────────────
        with cg2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("##### 📉 Blocking vs Trafik Ditawarkan (A)")
            a_max_ = min(float(S-1), 30.0)
            av_    = np.linspace(0.1, a_max_, 300)
            pv_    = [(engset(S,N,float(a)) or 0)*100 for a in av_]

            fig2, ax2 = plt.subplots(figsize=(5.5, 3.8))
            fig2.patch.set_facecolor(BG); ax2.set_facecolor(BG)
            ax2.fill_between(av_, pv_, alpha=0.13, color=TEAL)
            ax2.plot(av_, pv_, color=TEAL, linewidth=2.5, zorder=3)
            ax2.scatter([A], [P*100], color=RED, s=90, zorder=5,
                        label=f'A={A:.1f}, P={P*100:.3f}%')
            ax2.axhline(1.0, color=AMBER, linestyle='--', linewidth=1.2, alpha=0.8)
            ax2.text(a_max_*0.97, 1.05, 'GoS 1%', ha='right', fontsize=8, color=AMBER)
            ax2.set_xlabel('A — Trafik yang Ditawarkan (Erlang)', fontsize=9, color='#5a6a8e')
            ax2.set_ylabel('Blocking (%)', fontsize=9, color='#5a6a8e')
            ax2.set_title(f'S={S}, N={N} kanal', fontsize=9, color='#8899bb')
            ax2.legend(fontsize=8.5)
            ax2.grid(True, linestyle='--', alpha=0.3)
            ax2.spines[['top','right']].set_visible(False)
            ax2.tick_params(colors='#8899bb', labelsize=8)
            plt.tight_layout(pad=1.0)
            st.pyplot(fig2, use_container_width=True)
            plt.close(fig2)
            st.markdown('</div>', unsafe_allow_html=True)

        # ── Grafik 3: Multi-kurva ────────────────────────────────────────────
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("##### 🌐 Multi-Kurva: Blocking vs N untuk Berbagai Nilai A")
        palette = [BLUE, TEAL, AMBER, RED, '#a855f7', '#ec4899']
        a_list  = [round(A*m,2) for m in [0.5,0.75,1.0,1.25,1.5,2.0] if 0 < A*m < S][:6]
        max_n3  = min(S-1, 35)
        ns3_    = list(range(1, max_n3+1))

        fig3, ax3 = plt.subplots(figsize=(11, 4))
        fig3.patch.set_facecolor(BG); ax3.set_facecolor(BG)
        for idx, a_c in enumerate(a_list):
            ps3 = [(engset(S,n,a_c) or 0)*100 for n in ns3_]
            ax3.plot(ns3_, ps3, color=palette[idx%len(palette)],
                     linewidth=2, label=f'A={a_c:.1f} Erl')
        ax3.axvline(N, color='#64748b', linestyle=':', linewidth=1.8,
                    label=f'N aktif = {N}')
        ax3.axhline(1.0, color=AMBER, linestyle='--', linewidth=1, alpha=0.6)
        ax3.set_xlabel('N — Jumlah Kanal', fontsize=9, color='#5a6a8e')
        ax3.set_ylabel('Blocking (%)', fontsize=9, color='#5a6a8e')
        ax3.set_title(f'Perbandingan Blocking vs N untuk Berbagai Nilai A (S={S})',
                      fontsize=10, color='#0d1b3e', fontweight='bold')
        ax3.legend(fontsize=8.5, ncol=min(len(a_list)+1, 4))
        ax3.grid(True, linestyle='--', alpha=0.3)
        ax3.spines[['top','right']].set_visible(False)
        ax3.tick_params(colors='#8899bb', labelsize=8)
        plt.tight_layout(pad=1.0)
        st.pyplot(fig3, use_container_width=True)
        plt.close(fig3)
        st.markdown('</div>', unsafe_allow_html=True)

        # ── Tabel detail ─────────────────────────────────────────────────────
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("##### 📋 Tabel Detail Blocking vs N")
        rows_html = ""
        for n_i in range(1, min(S, N+15)):
            p_i = engset(S, n_i, A)
            if p_i is None:
                continue
            c_i = A*(1-p_i); l_i = A*p_i; u_i = (c_i/n_i)*100
            g_t, g_c = label_gos(p_i)
            active_cls = 'class="active"' if n_i == N else ""
            rows_html += (f'<tr {active_cls}>'
                          f'<td>{"→ " if n_i==N else ""}{n_i}</td>'
                          f'<td>{p_i:.6f}</td><td>{p_i*100:.3f}%</td>'
                          f'<td>{c_i:.4f}</td><td>{l_i:.4f}</td>'
                          f'<td>{u_i:.1f}%</td>'
                          f'<td><span class="gos {g_c}">{g_t}</span></td></tr>')
        st.markdown(f"""
        <table class="eng-table">
          <thead>
            <tr><th>N</th><th>P Blocking</th><th>%</th>
                <th>Trafik Terlayani (Erl)</th><th>Trafik Hilang (Erl)</th>
                <th>Utilisasi</th><th>GoS</th></tr>
          </thead>
          <tbody>{rows_html}</tbody>
        </table>
        <div class="eng-info" style="margin-top:8px;font-size:0.78rem;">
          🔵 Baris biru = nilai N yang dipilih saat ini (N={N})</div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ██ EKSPOR LAPORAN
# Generate laporan PDF profesional berstandar teknik telekomunikasi.
# ══════════════════════════════════════════════════════════════════════════════
elif active_page == "📄  Ekspor Laporan":
    page_header("Ekspor", "Ekspor Laporan PDF",
                "Buat laporan teknik profesional hasil analisis Engset")

    if not valid:
        st.markdown('<div class="eng-warn">⚠️ Periksa parameter di sidebar terlebih dahulu.</div>',
                    unsafe_allow_html=True)
    elif not PDF_OK:
        st.markdown('<div class="eng-warn">⚠️ Instal ReportLab terlebih dahulu: <code>pip install reportlab</code></div>',
                    unsafe_allow_html=True)
    else:
        c_prev, c_act = st.columns([1.5, 1], gap="large")

        with c_prev:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div style="font-size:0.9rem;font-weight:700;color:#0d1b3e;'
                        'margin-bottom:1rem;">📄 Isi Laporan yang Akan Dibuat</div>',
                        unsafe_allow_html=True)

            items_prev = [
                ("📌", "Judul",                 "EngsetPro — Laporan Analisis Trafik Engset"),
                ("📅", "Tanggal",               datetime.now().strftime('%d %B %Y, %H:%M')),
                ("1️⃣", "Pendahuluan",           "Latar belakang & dasar teori Engset"),
                ("2️⃣", "Landasan Teori",        "Rumus Engset, definisi, dan variabel"),
                ("3️⃣", "Parameter Input",        f"S={S}, N={N}, A={A:.1f} Erl"),
                ("4️⃣", "Hasil Perhitungan",      f"P={P:.8f}, GoS={gos_text}"),
                ("5️⃣", "Analisis Trafik",        f"Carried={carried:.4f} Erl, Lost={lost:.4f} Erl"),
                ("6️⃣", "Grafik Analisis",        "Blocking vs N + Blocking vs A"),
                ("7️⃣", "Tabel Rekomendasi N",    "N minimum per target GoS"),
                ("8️⃣", "Kesimpulan",             "Ringkasan dan rekomendasi teknis"),
            ]
            for icon, label, val in items_prev:
                st.markdown(f"""
                <div class="data-row">
                  <span class="data-row-label">{icon} {label}</span>
                  <span class="data-row-val" style="text-align:right;max-width:55%;font-size:0.78rem;">{val}</span>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with c_act:
            st.markdown("""
            <div class="card" style="text-align:center;padding:2rem 1.5rem;">
              <div style="font-size:3rem;margin-bottom:1rem;">📄</div>
              <div style="font-size:1rem;font-weight:700;color:#0d1b3e;margin-bottom:0.5rem;">
                Laporan PDF Profesional</div>
              <div style="font-size:0.82rem;color:#8899bb;margin-bottom:1.5rem;line-height:1.6;">
                Berisi pendahuluan, landasan teori, rumus standar ITU-T,
                parameter, hasil perhitungan, grafik analisis, tabel,
                dan kesimpulan teknis.
              </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("⬇️  Generate & Unduh PDF", use_container_width=True):
                with st.spinner("Membuat laporan PDF profesional..."):

                    def fig_to_bytes(fig):
                        buf = io.BytesIO()
                        fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
                        buf.seek(0)
                        return buf.read()

                    # ── Buat grafik 1: Blocking vs N ─────────────────────────
                    max_n_ = min(S-1, 40)
                    ns__   = list(range(1, max_n_+1))
                    ps__   = [(engset(S,n,A) or 0)*100 for n in ns__]
                    f1, a1 = plt.subplots(figsize=(7, 3.5))
                    f1.patch.set_facecolor(BG); a1.set_facecolor(BG)
                    a1.fill_between(ns__, ps__, alpha=0.12, color=BLUE)
                    a1.plot(ns__, ps__, color=BLUE, linewidth=2)
                    a1.scatter([N], [P*100], color=RED, s=60, zorder=5,
                               label=f'N={N}, P={P*100:.3f}%')
                    a1.axhline(1.0, color=AMBER, linestyle='--', linewidth=1, label='GoS 1%')
                    a1.axhline(0.1, color=TEAL,  linestyle='--', linewidth=1, label='GoS 0,1%')
                    a1.set_xlabel('N (Jumlah Kanal)'); a1.set_ylabel('Blocking (%)')
                    a1.set_title(f'Gambar 1. Kurva Blocking vs Jumlah Kanal N (S={S}, A={A:.1f} Erl)')
                    a1.legend(fontsize=8); a1.grid(True, linestyle='--', alpha=0.3)
                    a1.spines[['top','right']].set_visible(False)
                    plt.tight_layout()
                    c1_bytes = fig_to_bytes(f1)
                    plt.close(f1)

                    # ── Buat grafik 2: Blocking vs A ─────────────────────────
                    am_ = min(float(S-1), 25.0)
                    av_ = np.linspace(0.1, am_, 200)
                    pv_ = [(engset(S,N,float(a)) or 0)*100 for a in av_]
                    f2, a2 = plt.subplots(figsize=(7, 3.5))
                    f2.patch.set_facecolor(BG); a2.set_facecolor(BG)
                    a2.fill_between(av_, pv_, alpha=0.12, color=TEAL)
                    a2.plot(av_, pv_, color=TEAL, linewidth=2)
                    a2.scatter([A], [P*100], color=RED, s=60, zorder=5,
                               label=f'A={A:.1f}, P={P*100:.3f}%')
                    a2.axhline(1.0, color=AMBER, linestyle='--', linewidth=1, label='GoS 1%')
                    a2.set_xlabel('A (Erlang)'); a2.set_ylabel('Blocking (%)')
                    a2.set_title(f'Gambar 2. Kurva Blocking vs Trafik yang Ditawarkan A (S={S}, N={N})')
                    a2.legend(fontsize=8); a2.grid(True, linestyle='--', alpha=0.3)
                    a2.spines[['top','right']].set_visible(False)
                    plt.tight_layout()
                    c2_bytes = fig_to_bytes(f2)
                    plt.close(f2)

                    # ══════════════════════════════════════════════════════════
                    # BUILD PDF
                    # ══════════════════════════════════════════════════════════
                    buf_pdf = io.BytesIO()
                    PAGE_W, PAGE_H = A4
                    doc = SimpleDocTemplate(
                        buf_pdf, pagesize=A4,
                        leftMargin=2.5*cm, rightMargin=2*cm,
                        topMargin=2.5*cm, bottomMargin=2.5*cm,
                        title="Laporan Analisis Trafik Engset",
                        author="EngsetPro v2.0",
                    )

                    # ── Styles ────────────────────────────────────────────────
                    NAVY  = colors.HexColor('#0d1b3e')
                    BLUE_ = colors.HexColor('#1a56ff')
                    TEAL_ = colors.HexColor('#00c8b4')
                    LGRAY = colors.HexColor('#f0f4ff')
                    MGRAY = colors.HexColor('#c7d7ff')
                    DGRAY = colors.HexColor('#8899bb')

                    cover_title = ParagraphStyle('CT', fontSize=28, textColor=NAVY,
                                                 fontName='Helvetica-Bold', spaceAfter=6,
                                                 alignment=TA_CENTER)
                    cover_sub   = ParagraphStyle('CS', fontSize=13, textColor=BLUE_,
                                                 spaceAfter=6, alignment=TA_CENTER)
                    cover_info  = ParagraphStyle('CI', fontSize=9, textColor=DGRAY,
                                                 alignment=TA_CENTER, leading=16)
                    ch_title    = ParagraphStyle('CH', fontSize=13, textColor=NAVY,
                                                 fontName='Helvetica-Bold',
                                                 spaceBefore=18, spaceAfter=8,
                                                 borderPad=4)
                    body        = ParagraphStyle('BD', fontSize=9.5, textColor=colors.HexColor('#2d3a5e'),
                                                 leading=16, spaceAfter=6, alignment=TA_JUSTIFY)
                    formula_st  = ParagraphStyle('FM', fontSize=10, fontName='Courier',
                                                 textColor=colors.HexColor('#0d2060'),
                                                 backColor=LGRAY,
                                                 leftIndent=14, rightIndent=14,
                                                 spaceBefore=6, spaceAfter=6, leading=20,
                                                 alignment=TA_LEFT)
                    caption_st  = ParagraphStyle('CP', fontSize=8, textColor=DGRAY,
                                                 alignment=TA_CENTER, spaceBefore=4, spaceAfter=10)
                    footer_st   = ParagraphStyle('FT', fontSize=7.5, textColor=DGRAY,
                                                 alignment=TA_CENTER)
                    label_bold  = ParagraphStyle('LB', fontSize=9, fontName='Helvetica-Bold',
                                                 textColor=NAVY)

                    el = []

                    # ══════════════════════════════════════════════════════════
                    # HALAMAN SAMPUL
                    # ══════════════════════════════════════════════════════════
                    el.append(Spacer(1, 3*cm))
                    el.append(Paragraph("LAPORAN ANALISIS TRAFIK", cover_sub))
                    el.append(Paragraph("Model Engset Finite Source", cover_title))
                    el.append(Spacer(1, 0.5*cm))
                    el.append(HRFlowable(width="70%", thickness=2,
                                         color=BLUE_, spaceAfter=16,
                                         hAlign='CENTER'))
                    el.append(Spacer(1, 0.5*cm))

                    cover_data = [
                        ["Parameter",    "Nilai",         "Satuan"],
                        ["S — Jumlah Source",  str(S),   "pengguna"],
                        ["N — Jumlah Kanal",   str(N),   "kanal"],
                        ["A — Trafik Ditawarkan", f"{A:.1f}", "Erlang"],
                        ["P — Probabilitas Blocking", f"{P:.6f}", "—"],
                        ["Grade of Service",   gos_text, "—"],
                    ]
                    ct = Table(cover_data, colWidths=[7*cm, 4*cm, 4*cm],
                               hAlign='CENTER')
                    ct.setStyle(TableStyle([
                        ('BACKGROUND',  (0,0), (-1,0), BLUE_),
                        ('TEXTCOLOR',   (0,0), (-1,0), colors.white),
                        ('FONTNAME',    (0,0), (-1,0), 'Helvetica-Bold'),
                        ('FONTSIZE',    (0,0), (-1,-1), 9.5),
                        ('ALIGN',       (0,0), (-1,-1), 'CENTER'),
                        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LGRAY]),
                        ('GRID',        (0,0), (-1,-1), 0.5, MGRAY),
                        ('TOPPADDING',  (0,0), (-1,-1), 8),
                        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
                        ('ROUNDEDCORNERS', [4]),
                    ]))
                    el.append(ct)
                    el.append(Spacer(1, 2*cm))
                    el.append(Paragraph(
                        f"Tanggal Laporan: {datetime.now().strftime('%d %B %Y, pukul %H:%M WIB')}<br/>"
                        f"Dibuat dengan: EngsetPro v2.0 — Kalkulator Rekayasa Trafik",
                        cover_info))
                    el.append(PageBreak())

                    # ══════════════════════════════════════════════════════════
                    # BAB 1 — PENDAHULUAN
                    # ══════════════════════════════════════════════════════════
                    el.append(Paragraph("1.  Pendahuluan", ch_title))
                    el.append(HRFlowable(width="100%", thickness=1, color=MGRAY, spaceAfter=10))
                    el.append(Paragraph(
                        "Laporan ini menyajikan hasil analisis rekayasa trafik telekomunikasi "
                        "menggunakan model probabilistik <b>Engset</b> (finite source model). "
                        "Model Engset digunakan ketika jumlah sumber trafik (pengguna) bersifat "
                        "terbatas (finite), sehingga memberikan estimasi probabilitas blocking "
                        "yang lebih akurat dibandingkan model Erlang-B untuk kondisi tersebut.",
                        body))
                    el.append(Paragraph(
                        "Tujuan analisis ini adalah menentukan probabilitas blocking sistem, "
                        "mengevaluasi Grade of Service (GoS), serta memberikan rekomendasi "
                        "jumlah kanal minimum yang diperlukan untuk memenuhi standar kualitas layanan.",
                        body))
                    el.append(Spacer(1, 0.3*cm))

                    # ══════════════════════════════════════════════════════════
                    # BAB 2 — LANDASAN TEORI
                    # ══════════════════════════════════════════════════════════
                    el.append(Paragraph("2.  Landasan Teori", ch_title))
                    el.append(HRFlowable(width="100%", thickness=1, color=MGRAY, spaceAfter=10))
                    el.append(Paragraph(
                        "<b>2.1  Model Engset</b><br/>"
                        "Model Engset merupakan model antrian teletraffic yang dikembangkan "
                        "oleh T. O. Engset (1918) untuk sistem dengan sumber trafik terbatas. "
                        "Model ini mengasumsikan bahwa pengguna yang sedang ditangani sistem "
                        "tidak dapat membangkitkan permintaan baru (blocked calls cleared).",
                        body))
                    el.append(Paragraph(
                        "<b>2.2  Rumus Engset</b><br/>"
                        "Probabilitas blocking P(S, N, A) dihitung menggunakan rumus berikut:",
                        body))

                    el.append(Paragraph(
                        "              C(S-1, N) x rho^N\n"
                        "P(S,N,A) = ─────────────────────────\n"
                        "            N\n"
                        "           SUM  C(S-1, i) x rho^i\n"
                        "           i=0\n\n"
                        "          A\n"
                        "rho = ─────────\n"
                        "        S - A",
                        formula_st))

                    el.append(Paragraph(
                        "<b>Keterangan variabel:</b>",
                        body))

                    var_data = [
                        ["Simbol", "Nama",                        "Keterangan"],
                        ["P",      "Probabilitas Blocking",        "Peluang suatu panggilan terblokir"],
                        ["S",      "Jumlah Source",                "Total pengguna/sumber trafik"],
                        ["N",      "Jumlah Kanal",                 "Jumlah server/kanal tersedia"],
                        ["A",      "Traffic Offered",              "Trafik total yang ditawarkan (Erlang)"],
                        ["ρ (rho)","Rasio Intensitas Trafik",      "A / (S − A)"],
                        ["C(n,k)", "Koefisien Binomial",           "n! / (k! · (n−k)!)"],
                    ]
                    vt = Table(var_data, colWidths=[2.2*cm, 5*cm, 8.3*cm])
                    vt.setStyle(TableStyle([
                        ('BACKGROUND',   (0,0), (-1,0), NAVY),
                        ('TEXTCOLOR',    (0,0), (-1,0), colors.white),
                        ('FONTNAME',     (0,0), (-1,0), 'Helvetica-Bold'),
                        ('FONTSIZE',     (0,0), (-1,-1), 8.5),
                        ('ALIGN',        (0,0), (0,-1),  'CENTER'),
                        ('ALIGN',        (1,0), (-1,-1), 'LEFT'),
                        ('ROWBACKGROUNDS',(0,1),(-1,-1), [colors.white, LGRAY]),
                        ('GRID',         (0,0), (-1,-1), 0.4, MGRAY),
                        ('TOPPADDING',   (0,0), (-1,-1), 6),
                        ('BOTTOMPADDING',(0,0), (-1,-1), 6),
                        ('FONTNAME',     (0,1), (0,-1),  'Courier-Bold'),
                    ]))
                    el.append(vt)
                    el.append(Spacer(1, 0.4*cm))

                    el.append(Paragraph(
                        "<b>2.3  Grade of Service (GoS)</b><br/>"
                        "Grade of Service merupakan ukuran kualitas layanan telekomunikasi "
                        "yang dinyatakan sebagai probabilitas blocking. Standar umum yang "
                        "digunakan dalam rekayasa trafik adalah sebagai berikut:",
                        body))

                    gos_data = [
                        ["Rentang Blocking",  "Kategori GoS",  "Keterangan"],
                        ["P < 0,001 (0,1%)",  "Sangat Baik",   "Kualitas premium, layanan kritis"],
                        ["0,001 ≤ P < 0,01",  "Baik",          "Memenuhi standar ITU-T"],
                        ["0,01 ≤ P < 0,05",   "Cukup",         "Perlu penambahan kapasitas"],
                        ["P ≥ 0,05 (5%)",     "Buruk",         "Tidak memenuhi standar minimum"],
                    ]
                    gt = Table(gos_data, colWidths=[4.5*cm, 3.5*cm, 7.5*cm])
                    gt.setStyle(TableStyle([
                        ('BACKGROUND',   (0,0), (-1,0), TEAL_),
                        ('TEXTCOLOR',    (0,0), (-1,0), colors.white),
                        ('FONTNAME',     (0,0), (-1,0), 'Helvetica-Bold'),
                        ('FONTSIZE',     (0,0), (-1,-1), 8.5),
                        ('ALIGN',        (0,0), (-1,-1), 'LEFT'),
                        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, LGRAY]),
                        ('GRID',         (0,0), (-1,-1), 0.4, MGRAY),
                        ('TOPPADDING',   (0,0), (-1,-1), 6),
                        ('BOTTOMPADDING',(0,0), (-1,-1), 6),
                    ]))
                    el.append(gt)
                    el.append(Spacer(1, 0.4*cm))

                    # ══════════════════════════════════════════════════════════
                    # BAB 3 — PARAMETER INPUT
                    # ══════════════════════════════════════════════════════════
                    el.append(Paragraph("3.  Parameter Input", ch_title))
                    el.append(HRFlowable(width="100%", thickness=1, color=MGRAY, spaceAfter=10))
                    el.append(Paragraph(
                        "Parameter berikut digunakan sebagai masukan dalam perhitungan Engset:",
                        body))

                    pd_data = [
                        ["No.", "Parameter",           "Simbol", "Nilai",       "Satuan"],
                        ["1",   "Jumlah Source",        "S",      str(S),        "pengguna"],
                        ["2",   "Jumlah Kanal",          "N",      str(N),        "kanal"],
                        ["3",   "Traffic Offered",       "A",      f"{A:.2f}",    "Erlang"],
                        ["4",   "Rasio Intensitas (ρ)",  "ρ",      f"{A/(S-A):.6f}", "—"],
                    ]
                    pt = Table(pd_data, colWidths=[1*cm, 5.5*cm, 2*cm, 3*cm, 4*cm])
                    pt.setStyle(TableStyle([
                        ('BACKGROUND',   (0,0), (-1,0), BLUE_),
                        ('TEXTCOLOR',    (0,0), (-1,0), colors.white),
                        ('FONTNAME',     (0,0), (-1,0), 'Helvetica-Bold'),
                        ('FONTSIZE',     (0,0), (-1,-1), 9),
                        ('ALIGN',        (0,0), (-1,-1), 'CENTER'),
                        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, LGRAY]),
                        ('GRID',         (0,0), (-1,-1), 0.5, MGRAY),
                        ('TOPPADDING',   (0,0), (-1,-1), 7),
                        ('BOTTOMPADDING',(0,0), (-1,-1), 7),
                        ('FONTNAME',     (2,1), (2,-1), 'Courier-Bold'),
                    ]))
                    el.append(pt)
                    el.append(Spacer(1, 0.4*cm))

                    # ══════════════════════════════════════════════════════════
                    # BAB 4 — HASIL PERHITUNGAN
                    # ══════════════════════════════════════════════════════════
                    el.append(Paragraph("4.  Hasil Perhitungan", ch_title))
                    el.append(HRFlowable(width="100%", thickness=1, color=MGRAY, spaceAfter=10))
                    el.append(Paragraph(
                        "Perhitungan dilakukan menggunakan metode log-space arithmetic "
                        "untuk menghindari overflow numerik pada nilai S yang besar.",
                        body))

                    rd_data = [
                        ["Metrik",                  "Nilai",              "Satuan",  "Keterangan"],
                        ["Probabilitas Blocking (P)", f"{P:.8f}",          "—",       "Hasil utama Engset"],
                        ["Blocking (%)",              f"{P*100:.4f}",      "%",       "Konversi ke persentase"],
                        ["Grade of Service",          gos_text,            "—",       "Penilaian kualitas"],
                        ["Traffic Carried",           f"{carried:.4f}",   "Erlang",  "Trafik yang terlayani"],
                        ["Traffic Lost",              f"{lost:.4f}",      "Erlang",  "Trafik yang terblokir"],
                        ["Utilisasi Kanal",           f"{util_pct:.2f}",  "%",       "Rata-rata per kanal"],
                        ["N Min (GoS ≤ 1%)",         str(min_n_1),        "kanal",   "Rekomendasi minimum"],
                        ["N Min (GoS ≤ 0,1%)",       str(min_n_001),      "kanal",   "Rekomendasi premium"],
                    ]
                    rt = Table(rd_data, colWidths=[5*cm, 3.5*cm, 2.5*cm, 4.5*cm])
                    rt.setStyle(TableStyle([
                        ('BACKGROUND',   (0,0), (-1,0), NAVY),
                        ('TEXTCOLOR',    (0,0), (-1,0), colors.white),
                        ('FONTNAME',     (0,0), (-1,0), 'Helvetica-Bold'),
                        ('FONTSIZE',     (0,0), (-1,-1), 8.5),
                        ('ALIGN',        (1,0), (2,-1), 'CENTER'),
                        ('ALIGN',        (0,0), (0,-1), 'LEFT'),
                        ('ALIGN',        (3,0), (3,-1), 'LEFT'),
                        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, LGRAY]),
                        ('GRID',         (0,0), (-1,-1), 0.5, MGRAY),
                        ('TOPPADDING',   (0,0), (-1,-1), 7),
                        ('BOTTOMPADDING',(0,0), (-1,-1), 7),
                        # Highlight baris P blocking
                        ('BACKGROUND',   (0,1), (-1,1), colors.HexColor('#dce8ff')),
                        ('FONTNAME',     (1,1), (1,1),  'Helvetica-Bold'),
                    ]))
                    el.append(rt)
                    el.append(Spacer(1, 0.5*cm))

                    # ── Tabel rekomendasi N ───────────────────────────────────
                    el.append(Paragraph("<b>4.1  Tabel Rekomendasi Jumlah Kanal Minimum</b>", body))
                    targets_pdf = [0.10, 0.05, 0.02, 0.01, 0.005, 0.001]
                    rec_data = [["Target GoS", "N Minimum", "Status (N=" + str(N) + ")", "Keterangan"]]
                    for t in targets_pdf:
                        mn = cari_n_minimum(S, A, t)
                        ok = N >= (mn if mn else 9999)
                        ket = "Terpenuhi ✓" if ok else "Perlu tambah kanal ✗"
                        rec_data.append([
                            f"≤ {t*100:.1f}%",
                            f"N ≥ {mn if mn else '–'}",
                            "✓ Ya" if ok else "✗ Tidak",
                            ket,
                        ])
                    rn = Table(rec_data, colWidths=[3.5*cm, 3.5*cm, 3.5*cm, 5*cm])
                    rn.setStyle(TableStyle([
                        ('BACKGROUND',   (0,0), (-1,0), TEAL_),
                        ('TEXTCOLOR',    (0,0), (-1,0), colors.white),
                        ('FONTNAME',     (0,0), (-1,0), 'Helvetica-Bold'),
                        ('FONTSIZE',     (0,0), (-1,-1), 8.5),
                        ('ALIGN',        (0,0), (-1,-1), 'CENTER'),
                        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, LGRAY]),
                        ('GRID',         (0,0), (-1,-1), 0.5, MGRAY),
                        ('TOPPADDING',   (0,0), (-1,-1), 6),
                        ('BOTTOMPADDING',(0,0), (-1,-1), 6),
                    ]))
                    el.append(rn)
                    el.append(Spacer(1, 0.5*cm))

                    # ══════════════════════════════════════════════════════════
                    # BAB 5 — GRAFIK ANALISIS
                    # ══════════════════════════════════════════════════════════
                    el.append(Paragraph("5.  Grafik Analisis", ch_title))
                    el.append(HRFlowable(width="100%", thickness=1, color=MGRAY, spaceAfter=10))
                    el.append(Paragraph(
                        "Grafik berikut memperlihatkan hubungan antara probabilitas blocking "
                        "dengan variasi parameter N (jumlah kanal) dan A (trafik yang ditawarkan).",
                        body))

                    el.append(RLImage(io.BytesIO(c1_bytes), width=15*cm, height=7*cm))
                    el.append(Paragraph(
                        f"Gambar 1. Kurva probabilitas blocking P(%) terhadap jumlah kanal N "
                        f"(S={S}, A={A:.1f} Erlang). Titik merah menunjukkan kondisi N={N} saat ini.",
                        caption_st))
                    el.append(Spacer(1, 0.5*cm))

                    el.append(RLImage(io.BytesIO(c2_bytes), width=15*cm, height=7*cm))
                    el.append(Paragraph(
                        f"Gambar 2. Kurva probabilitas blocking P(%) terhadap trafik A yang ditawarkan "
                        f"(S={S}, N={N} kanal). Titik merah menunjukkan kondisi A={A:.1f} Erl saat ini.",
                        caption_st))
                    el.append(Spacer(1, 0.5*cm))

                    # ══════════════════════════════════════════════════════════
                    # BAB 6 — KESIMPULAN
                    # ══════════════════════════════════════════════════════════
                    el.append(Paragraph("6.  Kesimpulan dan Rekomendasi", ch_title))
                    el.append(HRFlowable(width="100%", thickness=1, color=MGRAY, spaceAfter=10))

                    if P < 0.001:
                        kesimpulan_gos = (
                            f"Sistem saat ini beroperasi pada Grade of Service kategori "
                            f"<b>Sangat Baik</b> dengan probabilitas blocking P = {P:.6f} "
                            f"({P*100:.4f}%), jauh di bawah ambang 0,1%. "
                            f"Kualitas layanan memenuhi standar premium."
                        )
                    elif P < 0.01:
                        kesimpulan_gos = (
                            f"Sistem beroperasi pada GoS kategori <b>Baik</b> dengan P = {P:.6f} "
                            f"({P*100:.4f}%). Kualitas layanan memenuhi standar ITU-T (P &lt; 1%)."
                        )
                    elif P < 0.05:
                        kesimpulan_gos = (
                            f"Sistem beroperasi pada GoS kategori <b>Cukup</b> dengan P = {P:.6f} "
                            f"({P*100:.4f}%). Disarankan menambah jumlah kanal "
                            f"minimal N = {min_n_1} untuk mencapai GoS ≤ 1%."
                        )
                    else:
                        kesimpulan_gos = (
                            f"Sistem beroperasi pada GoS kategori <b>Buruk</b> dengan P = {P:.6f} "
                            f"({P*100:.4f}%). Diperlukan penambahan kanal segera. "
                            f"Jumlah kanal minimum yang diperlukan adalah N = {min_n_1} "
                            f"(untuk GoS ≤ 1%)."
                        )

                    el.append(Paragraph(kesimpulan_gos, body))
                    el.append(Paragraph(
                        f"Dari hasil perhitungan diperoleh bahwa trafik yang terlayani "
                        f"(traffic carried) sebesar <b>{carried:.4f} Erlang</b> dan trafik "
                        f"yang hilang (traffic lost) sebesar <b>{lost:.4f} Erlang</b> dari "
                        f"total <b>{A:.1f} Erlang</b> yang ditawarkan. "
                        f"Utilisasi rata-rata per kanal adalah <b>{util_pct:.2f}%</b>.",
                        body))

                    el.append(Spacer(1, 0.3*cm))
                    rek_data = [
                        ["No.", "Rekomendasi",                          "Nilai"],
                        ["1",   "Jumlah kanal saat ini",                f"N = {N}"],
                        ["2",   "N minimum untuk GoS ≤ 1%",            f"N = {min_n_1}"],
                        ["3",   "N minimum untuk GoS ≤ 0,1%",          f"N = {min_n_001}"],
                        ["4",   "Grade of Service saat ini",            gos_text],
                        ["5",   "Utilisasi kanal",                      f"{util_pct:.2f}%"],
                    ]
                    rk = Table(rek_data, colWidths=[1*cm, 10*cm, 4.5*cm])
                    rk.setStyle(TableStyle([
                        ('BACKGROUND',   (0,0), (-1,0), BLUE_),
                        ('TEXTCOLOR',    (0,0), (-1,0), colors.white),
                        ('FONTNAME',     (0,0), (-1,0), 'Helvetica-Bold'),
                        ('FONTSIZE',     (0,0), (-1,-1), 9),
                        ('ALIGN',        (0,0), (0,-1), 'CENTER'),
                        ('ALIGN',        (2,0), (2,-1), 'CENTER'),
                        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, LGRAY]),
                        ('GRID',         (0,0), (-1,-1), 0.5, MGRAY),
                        ('TOPPADDING',   (0,0), (-1,-1), 7),
                        ('BOTTOMPADDING',(0,0), (-1,-1), 7),
                    ]))
                    el.append(rk)
                    el.append(Spacer(1, 0.8*cm))

                    el.append(HRFlowable(width="100%", thickness=0.5,
                                          color=MGRAY, spaceAfter=10))
                    el.append(Paragraph(
                        f"EngsetPro v2.0  ·  Kalkulator Rekayasa Trafik Telekomunikasi  ·  "
                        f"Metode: Log-space Arithmetic  ·  "
                        f"Referensi: ITU-T E.501 / T. O. Engset (1918)  ·  "
                        f"Dicetak: {datetime.now().strftime('%d %B %Y')}",
                        footer_st))

                    # ── Build PDF ─────────────────────────────────────────────
                    doc.build(el)
                    buf_pdf.seek(0)

                st.download_button(
                    "📥  Klik untuk Mengunduh PDF",
                    data=buf_pdf,
                    file_name=f"laporan_engset_S{S}_N{N}_A{A:.1f}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )
                st.markdown('<div class="eng-ok">✅ PDF siap! Klik tombol di atas untuk mengunduh.</div>',
                            unsafe_allow_html=True)


# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;color:#aab5cc;font-size:0.75rem;
     padding:2.5rem 0 1rem;letter-spacing:0.04em;">
  EngsetPro v2.0 &nbsp;·&nbsp; Kalkulator Rekayasa Trafik Engset &nbsp;·&nbsp;
  Metode: Log-space Arithmetic &nbsp;·&nbsp; Referensi: ITU-T E.501
</div>
""", unsafe_allow_html=True)st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
  --blue-primary: #1a56ff;
  --blue-dark:    #0e3acc;
  --blue-deeper:  #0a2aaa;
  --teal:         #00c8b4;
  --teal-light:   #4dd9cb;
  --green:        #22c55e;
  --amber:        #f59e0b;
  --red:          #ef4444;
  --bg:           #f2f5fc;
  --white:        #ffffff;
  --navy:         #0d1b3e;
  --slate:        #3a5098;
  --muted:        #8899bb;
  --border:       rgba(26,86,255,0.08);
  --shadow-sm:    0 2px 12px rgba(26,86,255,0.07);
  --shadow-md:    0 6px 24px rgba(26,86,255,0.12);
  --shadow-lg:    0 12px 40px rgba(26,86,255,0.20);
  --radius-sm:    12px;
  --radius-md:    18px;
  --radius-lg:    24px;
}

html, body, [class*="css"] {
  font-family: 'Sora', sans-serif !important;
}

.stApp {
  background: var(--bg) !important;
}

#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ═══════════ SIDEBAR ═══════════ */
[data-testid="stSidebar"] {
  background: linear-gradient(175deg, #1246e8 0%, #0c35c0 45%, #072590 100%) !important;
  border-right: none !important;
  box-shadow: 6px 0 30px rgba(10,42,170,0.30);
}
[data-testid="stSidebar"] > div:first-child { padding-top: 0 !important; }
[data-testid="stSidebar"] * { color: rgba(255,255,255,0.9) !important; }
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stNumberInput label {
  color: rgba(255,255,255,0.65) !important;
  font-size: 0.72rem !important;
  letter-spacing: 0.07em;
  text-transform: uppercase;
}
[data-testid="stSidebar"] hr {
  border-color: rgba(255,255,255,0.12) !important;
}

/* Radio nav items */
[data-testid="stSidebar"] [data-testid="stRadio"] > div {
  gap: 4px !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label {
  border-radius: 12px !important;
  padding: 10px 14px !important;
  transition: background 0.2s ease !important;
  font-size: 0.88rem !important;
  font-weight: 500 !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
  background: rgba(255,255,255,0.12) !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] [aria-checked="true"] + div label,
[data-testid="stSidebar"] [data-testid="stRadio"] input:checked + div {
  background: rgba(255,255,255,0.18) !important;
  font-weight: 700 !important;
}

/* Group labels in sidebar */
.nav-group-label {
  font-size: 0.65rem;
  font-weight: 700;
  color: rgba(255,255,255,0.4) !important;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  margin: 16px 0 6px 6px;
}

/* ═══════════ BASE CARDS ═══════════ */
.card {
  background: var(--white);
  border-radius: var(--radius-md);
  padding: 1.4rem 1.6rem;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border);
  margin-bottom: 1rem;
}

.card-sm {
  background: var(--white);
  border-radius: var(--radius-sm);
  padding: 1rem 1.2rem;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border);
  margin-bottom: 0.75rem;
}

/* ═══════════ HERO GRADIENT CARD ═══════════ */
.hero-card {
  background: linear-gradient(135deg, #1a56ff 0%, #0a8fe8 55%, #00c8b4 100%);
  border-radius: var(--radius-lg);
  padding: 2rem 2rem 1.8rem;
  color: white;
  margin-bottom: 1rem;
  position: relative;
  overflow: hidden;
  box-shadow: 0 10px 40px rgba(26,86,255,0.40);
}
.hero-card::before {
  content: "";
  position: absolute; top: -80px; right: -50px;
  width: 260px; height: 260px; border-radius: 50%;
  background: rgba(255,255,255,0.07);
}
.hero-card::after {
  content: "";
  position: absolute; bottom: -60px; left: 35%;
  width: 200px; height: 200px; border-radius: 50%;
  background: rgba(255,255,255,0.05);
}
.hero-badge {
  display: inline-flex; align-items: center; gap: 6px;
  background: rgba(255,255,255,0.18);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255,255,255,0.25);
  border-radius: 100px;
  padding: 4px 14px;
  font-size: 0.7rem; font-weight: 700;
  letter-spacing: 0.1em; text-transform: uppercase;
  margin-bottom: 1rem;
  color: #fff;
}
.hero-stat-pill {
  background: rgba(255,255,255,0.16);
  backdrop-filter: blur(6px);
  border: 1px solid rgba(255,255,255,0.2);
  border-radius: 14px; padding: 10px 20px;
}

/* ═══════════ METRIC CHIPS ═══════════ */
.chip-grid {
  display: grid; grid-template-columns: 1fr 1fr 1fr;
  gap: 10px; margin-bottom: 1rem;
}
.chip {
  background: var(--white);
  border-radius: var(--radius-sm);
  padding: 1.1rem 0.8rem;
  text-align: center;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border);
  position: relative; overflow: hidden;
}
.chip::before {
  content: "";
  position: absolute; top: 0; left: 0; right: 0; height: 3px;
  background: linear-gradient(90deg, var(--blue-primary), var(--teal));
  border-radius: 3px 3px 0 0;
}
.chip-icon { font-size: 1.2rem; margin-bottom: 6px; }
.chip-val  {
  font-size: 1.05rem; font-weight: 700; color: var(--navy);
  font-family: 'JetBrains Mono', monospace;
}
.chip-lbl  {
  font-size: 0.65rem; color: var(--muted);
  text-transform: uppercase; letter-spacing: 0.07em; margin-top: 3px;
}

/* ═══════════ PLAN / RESULT ROWS ═══════════ */
.plan-card {
  background: var(--white);
  border-radius: var(--radius-sm);
  padding: 0.95rem 1.2rem;
  display: flex; align-items: center; gap: 14px;
  margin-bottom: 8px;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border);
  transition: box-shadow 0.2s, transform 0.2s;
}
.plan-card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-1px);
}
.plan-icon-wrap {
  width: 44px; height: 44px; border-radius: 13px;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.2rem; flex-shrink: 0;
}
.plan-icon-blue  { background: rgba(26,86,255,0.10); }
.plan-icon-teal  { background: rgba(0,200,180,0.10); }
.plan-icon-green { background: rgba(34,197,94,0.10); }
.plan-icon-amber { background: rgba(245,158,11,0.10); }
.plan-icon-red   { background: rgba(239,68,68,0.10); }
.plan-info { flex: 1; }
.plan-name { font-size: 0.88rem; font-weight: 600; color: var(--navy); margin: 0; }
.plan-desc { font-size: 0.75rem; color: var(--muted); margin: 2px 0 0; }
.plan-val  {
  font-size: 0.95rem; font-weight: 700; color: var(--blue-primary);
  font-family: 'JetBrains Mono', monospace;
}

/* ═══════════ GoS BADGE ═══════════ */
.gos {
  display: inline-block; padding: 4px 14px; border-radius: 100px;
  font-size: 0.75rem; font-weight: 700; letter-spacing: 0.04em;
}
.gos-great { background: #dcfce7; color: #166534; }
.gos-good  { background: #d1fae5; color: #065f46; }
.gos-ok    { background: #fef9c3; color: #713f12; }
.gos-bad   { background: #fee2e2; color: #7f1d1d; }

/* ═══════════ FORMULA BLOCK ═══════════ */
.formula-wrap {
  background: linear-gradient(135deg, #eef3ff 0%, #e4edff 100%);
  border: 1.5px solid #c7d7ff;
  border-radius: var(--radius-md);
  padding: 1.6rem 1.8rem; margin-bottom: 1rem;
}
.formula-tag {
  display: inline-block; background: var(--blue-primary); color: #fff;
  font-size: 0.65rem; font-weight: 700; letter-spacing: 0.1em;
  text-transform: uppercase; padding: 3px 12px; border-radius: 100px; margin-bottom: 1rem;
}
.formula-body {
  font-family: 'JetBrains Mono', monospace; font-size: 0.85rem;
  color: #0d2060; line-height: 2.2;
  background: rgba(255,255,255,0.65); border-radius: 10px;
  padding: 1rem 1.4rem;
}
.formula-legend { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-top: 1rem; }
.fl-item { font-size: 0.78rem; color: var(--slate); display: flex; align-items: baseline; gap: 8px; }
.fl-sym  { font-family: 'JetBrains Mono', monospace; font-weight: 700; color: var(--blue-primary); min-width: 22px; }

/* ═══════════ SECTION TITLE ═══════════ */
.sec-title {
  font-size: 1rem; font-weight: 700; color: var(--navy); margin: 0 0 0.8rem;
  display: flex; align-items: center; gap: 6px;
}

/* ═══════════ ALERT BANNERS ═══════════ */
.eng-warn {
  background: #fff7ed; border: 1px solid #fed7aa;
  border-left: 4px solid #f59e0b;
  border-radius: var(--radius-sm); padding: 0.85rem 1.1rem;
  color: #92400e; font-size: 0.85rem; margin-bottom: 1rem;
}
.eng-info {
  background: #eff6ff; border: 1px solid #bfdbfe;
  border-left: 4px solid var(--blue-primary);
  border-radius: var(--radius-sm); padding: 0.85rem 1.1rem;
  color: #1e40af; font-size: 0.85rem; margin-bottom: 1rem;
}
.eng-ok {
  background: #f0fdf4; border: 1px solid #bbf7d0;
  border-left: 4px solid var(--green);
  border-radius: var(--radius-sm); padding: 0.85rem 1.1rem;
  color: #166534; font-size: 0.85rem; margin-bottom: 1rem;
}

/* ═══════════ TABLE ═══════════ */
.eng-table {
  width: 100%; border-collapse: collapse; font-size: 0.83rem;
  border-radius: var(--radius-sm); overflow: hidden;
}
.eng-table th {
  background: linear-gradient(90deg, var(--blue-primary), var(--blue-dark));
  color: #fff; font-size: 0.68rem;
  text-transform: uppercase; letter-spacing: 0.08em;
  padding: 10px 14px; text-align: left; font-weight: 600;
}
.eng-table td {
  padding: 9px 14px; border-bottom: 1px solid #f0f4ff;
  color: #2d3a5e; font-family: 'JetBrains Mono', monospace; font-size: 0.8rem;
}
.eng-table tr:hover td { background: #f5f8ff; }
.eng-table tr.active td { background: #eff6ff; font-weight: 600; color: var(--navy); }

/* ═══════════ BUTTONS ═══════════ */
.stButton > button {
  background: linear-gradient(135deg, #1a56ff, #0e3acc) !important;
  color: #fff !important; border: none !important;
  border-radius: var(--radius-sm) !important;
  padding: 0.65rem 1.6rem !important; font-weight: 700 !important;
  font-size: 0.88rem !important;
  box-shadow: 0 4px 16px rgba(26,86,255,0.3) !important;
  transition: all 0.2s ease !important;
  font-family: 'Sora', sans-serif !important;
}
.stButton > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 24px rgba(26,86,255,0.4) !important;
}

/* ═══════════ PROGRESS BAR ═══════════ */
.progress-wrap {
  background: #e8efff; border-radius: 100px; height: 8px;
  margin: 6px 0; overflow: hidden;
}
.progress-fill {
  height: 100%; border-radius: 100px;
  background: linear-gradient(90deg, var(--blue-primary), var(--teal));
  transition: width 0.5s ease;
}

/* ═══════════ TABS ═══════════ */
.stTabs [data-baseweb="tab-list"] {
  background: #edf1fb; border-radius: 14px; padding: 4px; gap: 4px; border: none;
}
.stTabs [data-baseweb="tab"] {
  border-radius: 10px; font-weight: 600; font-size: 0.86rem;
  color: var(--muted); padding: 8px 20px;
  font-family: 'Sora', sans-serif;
}
.stTabs [aria-selected="true"] {
  background: var(--white) !important; color: var(--blue-primary) !important;
  box-shadow: 0 2px 10px rgba(26,86,255,0.14) !important;
}

/* ═══════════ PAGE HEADER ═══════════ */
.page-header {
  margin-bottom: 1.6rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #eaeffe;
}
.page-header-tag {
  font-size: 0.68rem; color: var(--blue-primary); font-weight: 700;
  text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 4px;
}
.page-header-title {
  font-size: 1.75rem; font-weight: 800; color: var(--navy); margin: 0;
  letter-spacing: -0.02em;
}
.page-header-sub {
  color: var(--muted); margin: 4px 0 0; font-size: 0.88rem;
}

/* ═══════════ STAT RESULT BOX ═══════════ */
.result-hero {
  background: linear-gradient(135deg, #eef3ff, #e4edff);
  border: 1.5px solid #c7d7ff;
  border-radius: var(--radius-md);
  padding: 1.4rem; text-align: center; margin-bottom: 1rem;
}
.result-hero-label {
  font-size: 0.7rem; color: var(--slate); text-transform: uppercase;
  letter-spacing: 0.08em; margin-bottom: 6px;
}
.result-hero-val {
  font-size: 2.4rem; font-weight: 800; color: var(--blue-primary);
  font-family: 'JetBrains Mono', monospace; line-height: 1;
}
.result-hero-unit {
  font-size: 0.82rem; color: var(--muted); margin-top: 6px;
}

/* ═══════════ DATA ROW ═══════════ */
.data-row {
  display: flex; justify-content: space-between; align-items: center;
  padding: 10px 0; border-bottom: 1px solid #f0f4ff;
}
.data-row:last-child { border-bottom: none; }
.data-row-label { font-size: 0.82rem; color: var(--muted); }
.data-row-val {
  font-size: 0.85rem; font-weight: 700; color: var(--navy);
  font-family: 'JetBrains Mono', monospace;
}
</style>
""", unsafe_allow_html=True)


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
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    # Logo / brand
    st.markdown("""
    <div style="background:rgba(255,255,255,0.10);border-radius:18px;
         padding:1.4rem 1.2rem 1.1rem;margin-bottom:1.4rem;text-align:center;">
      <div style="font-size:2.2rem;margin-bottom:2px;">📡</div>
      <div style="font-size:1.35rem;font-weight:800;color:#fff;letter-spacing:-0.01em;">EngsetPro</div>
      <div style="font-size:0.65rem;color:rgba(255,255,255,0.5);letter-spacing:0.1em;
           text-transform:uppercase;margin-top:2px;">Rekayasa Trafik v2.0</div>
    </div>
    """, unsafe_allow_html=True)

    # ── MAIN MENU ──────────────────────────────────────────────
    st.markdown('<div class="nav-group-label">Menu Utama</div>', unsafe_allow_html=True)
    page = st.radio("nav", [
        "🏠  Dashboard",
        "🧮  Kalkulator Engset",
        "📊  Analisis & Grafik",
        "📄  Export Laporan",
    ], label_visibility="collapsed")

    # ── HITUNG TRAFFIC A (sub-menu) ────────────────────────────
    st.markdown('<div class="nav-group-label">Hitung Traffic A</div>', unsafe_allow_html=True)
    page_a = st.radio("nav_a", [
        "📞  A — Call Rate & Hold Time",
        "👥  A — Pengguna Aktif (BHT)",
        "🔁  A — Data Rate / Throughput",
    ], label_visibility="collapsed")

    # Override page if one of the A-sub-pages is "selected but default page active"
    if page not in ["🏠  Dashboard","🧮  Kalkulator Engset","📊  Analisis & Grafik","📄  Export Laporan"]:
        pass  # page_a drives

    st.markdown("---")
    # ── PARAMETER ─────────────────────────────────────────────
    st.markdown('<div class="nav-group-label">Parameter Sistem</div>', unsafe_allow_html=True)

    S = st.slider("S — Jumlah Source", 2, 200, 20, 1)
    N = st.slider("N — Jumlah Kanal",  1, 100,  5, 1)
    A = st.slider("A — Traffic Offered (Erl)", 0.1, float(max(1, S-1)), min(8.0, float(S-2)), 0.1)

    st.markdown("---")
    st.markdown(f"""
    <div style="background:rgba(255,255,255,0.08);border-radius:14px;padding:1rem;">
      <div style="font-size:0.65rem;color:rgba(255,255,255,0.45);text-transform:uppercase;
           letter-spacing:0.1em;margin-bottom:8px;">Sesi Saat Ini</div>
      <div style="font-size:0.82rem;color:rgba(255,255,255,0.85);line-height:2.1;">
        S = <strong>{S}</strong> pengguna<br>
        N = <strong>{N}</strong> kanal<br>
        A = <strong>{A:.1f}</strong> Erlang
      </div>
      <div style="font-size:0.68rem;color:rgba(255,255,255,0.38);margin-top:8px;">
        {datetime.now().strftime('%d %b %Y · %H:%M')}</div>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# COMPUTE
# ═══════════════════════════════════════════════════════════════════════════════
valid    = S > N and 0 < A < S
P        = engset(S, N, A) if valid else None
carried  = A * (1 - P) if P is not None else 0.0
lost     = A * P       if P is not None else 0.0
util_pct = (carried / N) * 100 if (P is not None and N > 0) else 0.0
gos_text, gos_cls = gos_label(P) if P is not None else ("—", "gos-ok")
min_n_1   = find_min_N(S, A, 0.01)  if valid else "—"
min_n_001 = find_min_N(S, A, 0.001) if valid else "—"

BLUE  = '#1a56ff'
TEAL  = '#00c8b4'
AMBER = '#f59e0b'
RED   = '#ef4444'
GREEN = '#22c55e'
BG    = '#f8faff'


# ═══════════════════════════════════════════════════════════════════════════════
# HELPER — Page header
# ═══════════════════════════════════════════════════════════════════════════════
def page_header(tag, title, sub):
    st.markdown(f"""
    <div class="page-header">
      <div class="page-header-tag">{tag}</div>
      <h1 class="page-header-title">{title}</h1>
      <p class="page-header-sub">{sub}</p>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# HELPER — Donut chart (matplotlib)
# ═══════════════════════════════════════════════════════════════════════════════
def donut_chart(val_pct, label_center, label_bottom, color=BLUE, bg='#e8efff'):
    fig, ax = plt.subplots(figsize=(3.8, 3.8))
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')
    sizes = [val_pct, max(0, 100 - val_pct)]
    clrs  = [color, bg]
    ax.pie(sizes, colors=clrs, startangle=90,
           wedgeprops=dict(width=0.44, edgecolor='white', linewidth=3),
           counterclock=False)
    ax.text(0, 0.08, label_center,
            ha='center', va='center', fontsize=18, fontweight='bold',
            color='#0d1b3e', fontfamily='monospace')
    ax.text(0, -0.24, label_bottom,
            ha='center', va='center', fontsize=9, color='#8899bb')
    ax.axis('equal')
    plt.tight_layout(pad=0.3)
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
# DETERMINE ACTIVE PAGE
# ═══════════════════════════════════════════════════════════════════════════════
# Traffic A pages override when clicked
A_PAGES = [
    "📞  A — Call Rate & Hold Time",
    "👥  A — Pengguna Aktif (BHT)",
    "🔁  A — Data Rate / Throughput",
]

# Use session_state to track last-clicked group
if "last_nav" not in st.session_state:
    st.session_state["last_nav"] = "main"

# Detect which radio was most recently changed using previous values
prev_page   = st.session_state.get("prev_page",   page)
prev_page_a = st.session_state.get("prev_page_a", page_a)

if page != prev_page:
    st.session_state["last_nav"] = "main"
elif page_a != prev_page_a:
    st.session_state["last_nav"] = "a"

st.session_state["prev_page"]   = page
st.session_state["prev_page_a"] = page_a

active_page = page if st.session_state["last_nav"] == "main" else page_a


# ══════════════════════════════════════════════════════════════════════════════
# ██ DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
if active_page == "🏠  Dashboard":

    col_main, col_side = st.columns([2.1, 1], gap="large")

    with col_main:
        # Hero card
        st.markdown(f"""
        <div class="hero-card">
          <div class="hero-badge">📡 EngsetPro · Finite Source Model</div>
          <h1 style="font-size:1.65rem;font-weight:800;color:#fff;margin:0 0 0.3rem;
               line-height:1.15;">Dashboard Analisis<br>Engset</h1>
          <p style="font-size:0.85rem;opacity:0.75;margin:0 0 1.4rem;">
            Probabilitas blocking real-time — Model Engset Finite Source</p>
          <div style="display:flex;gap:10px;flex-wrap:wrap;">
            <div class="hero-stat-pill">
              <div style="font-size:0.62rem;opacity:0.7;text-transform:uppercase;
                   letter-spacing:0.08em;margin-bottom:1px;">Source</div>
              <div style="font-size:1.3rem;font-weight:800;
                   font-family:'JetBrains Mono',monospace;">S = {S}</div>
            </div>
            <div class="hero-stat-pill">
              <div style="font-size:0.62rem;opacity:0.7;text-transform:uppercase;
                   letter-spacing:0.08em;margin-bottom:1px;">Kanal</div>
              <div style="font-size:1.3rem;font-weight:800;
                   font-family:'JetBrains Mono',monospace;">N = {N}</div>
            </div>
            <div class="hero-stat-pill">
              <div style="font-size:0.62rem;opacity:0.7;text-transform:uppercase;
                   letter-spacing:0.08em;margin-bottom:1px;">Traffic</div>
              <div style="font-size:1.3rem;font-weight:800;
                   font-family:'JetBrains Mono',monospace;">A = {A:.1f}</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        if P is not None:
            # Metric chips
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
            ("📶", "plan-icon-blue",  "Probabilitas Blocking", f"{P*100:.3f}%" if P else "—",  f"Grade: {gos_text}"),
            ("🔄", "plan-icon-teal",  "Traffic Carried",       f"{carried:.4f} Erl",             f"dari {A:.1f} Erl ditawarkan"),
            ("📉", "plan-icon-amber", "Kanal Min GoS ≤ 1%",   f"N = {min_n_1}",                "untuk kualitas baik"),
            ("⚡", "plan-icon-red",   "Utilisasi Kanal",       f"{util_pct:.1f}%",              f"rata-rata per {N} kanal"),
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
        # Utilisasi donut
        fig_d = donut_chart(
            util_pct,
            f"{util_pct:.1f}%" if P else "—",
            "utilisasi kanal",
            color=BLUE,
        )
        st.pyplot(fig_d, use_container_width=True)
        plt.close(fig_d)

        # GoS badge card
        pbar_w  = min(100, (P or 0) * 500)
        bar_col = GREEN if (P or 1) < 0.01 else AMBER if (P or 1) < 0.05 else RED
        st.markdown(f"""
        <div class="card" style="text-align:center;padding:1.3rem;">
          <div style="font-size:0.68rem;color:var(--muted);text-transform:uppercase;
               letter-spacing:0.08em;margin-bottom:8px;">Grade of Service</div>
          <span class="gos {gos_cls}" style="font-size:0.95rem;padding:7px 22px;">{gos_text}</span>
          <div style="margin-top:12px;">
            <div class="progress-wrap">
              <div class="progress-fill" style="width:{pbar_w:.1f}%;background:{bar_col};"></div>
            </div>
          </div>
          <div style="font-size:0.75rem;color:var(--muted);margin-top:6px;">
            P = {f"{P:.6f}" if P is not None else "—"}
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Rekomendasi kanal
        st.markdown(f"""
        <div class="card">
          <div style="font-size:0.85rem;font-weight:700;color:var(--navy);margin-bottom:10px;">
            🎯 Rekomendasi Kanal</div>
          <div style="font-size:0.82rem;color:var(--slate);line-height:2.3;">
            GoS ≤ 1%&nbsp;&nbsp;&nbsp;→
            <strong style="color:var(--blue-primary);">N = {min_n_1}</strong><br>
            GoS ≤ 0.1% →
            <strong style="color:var(--blue-primary);">N = {min_n_001}</strong>
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

    st.markdown("""
    <div class="formula-wrap">
      <span class="formula-tag">Rumus Engset — Finite Source</span>
      <div class="formula-body">
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;C(S-1, N) · (A/(S-A))^N<br>
P = ─────────────────────────────────────<br>
&nbsp;&nbsp;&nbsp;&nbsp;N<br>
&nbsp;&nbsp;&nbsp;Σ  C(S-1, i) · (A/(S-A))^i<br>
&nbsp;&nbsp;i=0
      </div>
      <div class="formula-legend">
        <div class="fl-item"><span class="fl-sym">P</span> Probabilitas blocking</div>
        <div class="fl-item"><span class="fl-sym">S</span> Jumlah source / pengguna</div>
        <div class="fl-item"><span class="fl-sym">N</span> Jumlah server / kanal</div>
        <div class="fl-item"><span class="fl-sym">A</span> Traffic offered (Erlang)</div>
        <div class="fl-item"><span class="fl-sym">C(n,k)</span> Kombinasi binomial</div>
        <div class="fl-item"><span class="fl-sym">Σ</span> Sigma penjumlahan i=0 s/d N</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if not valid:
        st.markdown('<div class="eng-warn">⚠️ Pastikan S &gt; N dan A &lt; S pada sidebar.</div>',
                    unsafe_allow_html=True)
    else:
        col1, col2 = st.columns([1.2, 1], gap="large")

        with col1:
            st.markdown('<p class="sec-title">📊 Hasil Perhitungan</p>', unsafe_allow_html=True)
            rows = [
                ("📡", "plan-icon-blue",  "Probabilitas Blocking (P)", f"{P:.8f}",        "probabilitas"),
                ("📈", "plan-icon-blue",  "Blocking Persen",           f"{P*100:.4f}%",   "persentase"),
                ("🏆", "plan-icon-green", "Grade of Service",          gos_text,           "penilaian kualitas"),
                ("✅", "plan-icon-teal",  "Traffic Carried",           f"{carried:.4f} Erl","terlayani"),
                ("❌", "plan-icon-red",   "Traffic Lost",              f"{lost:.4f} Erl",  "terblokir"),
                ("⚡", "plan-icon-amber", "Utilisasi Kanal",           f"{util_pct:.2f}%", "per kanal"),
                ("📶", "plan-icon-blue",  "Traffic Intensity",         f"{A/N:.4f} Erl/ch","per kanal"),
            ]
            for icon, icon_cls, label, val, unit in rows:
                st.markdown(f"""
                <div class="plan-card" style="padding:0.85rem 1.1rem;">
                  <div class="plan-icon-wrap {icon_cls}"
                       style="width:38px;height:38px;border-radius:10px;font-size:1.1rem;">{icon}</div>
                  <div class="plan-info">
                    <p class="plan-name" style="font-size:0.84rem;">{label}</p>
                    <p class="plan-desc">{unit}</p>
                  </div>
                  <div class="plan-val" style="font-size:0.92rem;">{val}</div>
                </div>
                """, unsafe_allow_html=True)

        with col2:
            # Donut utilisasi
            fig_du = donut_chart(util_pct, f"{util_pct:.1f}%", "utilisasi", color=BLUE)
            st.pyplot(fig_du, use_container_width=True)
            plt.close(fig_du)

            st.markdown('<p class="sec-title">🎯 Rekomendasi N Minimum</p>', unsafe_allow_html=True)
            targets = [0.10, 0.05, 0.02, 0.01, 0.005, 0.001]
            rec_rows = ""
            for t in targets:
                mn = find_min_N(S, A, t)
                ok = N >= (mn if mn else 9999)
                rec_rows += (f'<tr><td>≤ {t*100:.1f}%</td>'
                             f'<td>N ≥ {mn if mn else "–"}</td>'
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

            with st.expander("🔢 Lihat langkah perhitungan"):
                ratio = A / (S - A)
                st.markdown(f"""
**Langkah 1 — Hitung rasio:**
```
A/(S-A) = {A:.2f} / ({S} - {A:.2f}) = {ratio:.6f}
```
**Langkah 2 — Hitung pembilang:**
```
C(S-1, N) × (A/(S-A))^N
= C({S-1}, {N}) × {ratio:.6f}^{N}
```
**Langkah 3 — Hitung penyebut:**
```
Σ[i=0..{N}] C({S-1}, i) × {ratio:.6f}^i
```
**Langkah 4 — Hasil akhir:**
```
P = pembilang / penyebut
P = {P:.8f}
P = {P*100:.4f}%
```
                """)


# ══════════════════════════════════════════════════════════════════════════════
# ██ HITUNG A — CALL RATE & HOLD TIME
# ══════════════════════════════════════════════════════════════════════════════
elif active_page == "📞  A — Call Rate & Hold Time":
    page_header("Hitung Traffic A", "Call Rate & Hold Time",
                "Hitung Erlang dari λ (call rate) dan h (hold time)")

    st.markdown("""
    <div class="formula-wrap">
      <span class="formula-tag">Rumus Erlang — Method 1</span>
      <div class="formula-body">
A = λ × h<br>
<br>
λ = call rate (panggilan/jam per pengguna)<br>
h = rata-rata durasi panggilan (menit)
      </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.85rem;font-weight:700;color:#0d1b3e;margin-bottom:1rem;">⚙️ Input Parameter</div>',
                    unsafe_allow_html=True)
        call_rate  = st.number_input("λ — Call Rate (panggilan/jam per pengguna)",
                                     0.01, 1000.0, 3.0, 0.1, format="%.2f")
        hold_time  = st.number_input("h — Hold Time rata-rata (menit)",
                                     0.1, 120.0, 2.0, 0.1, format="%.1f")
        n_users_t1 = st.number_input("Jumlah pengguna aktif (untuk A total)",
                                     1, 10000, S)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        lam_s = call_rate / 3600
        h_s   = hold_time * 60
        A_1   = lam_s * h_s
        A_tot = A_1 * n_users_t1

        st.markdown(f"""
        <div class="card">
          <div style="font-size:0.85rem;font-weight:700;color:#0d1b3e;margin-bottom:1rem;">📊 Hasil Konversi</div>
          <div class="data-row">
            <span class="data-row-label">Traffic per pengguna</span>
            <span class="data-row-val" style="color:#1a56ff;">{A_1:.6f} Erl</span>
          </div>
          <div class="data-row">
            <span class="data-row-label">λ → konversi /detik</span>
            <span class="data-row-val">{lam_s:.6f} call/s</span>
          </div>
          <div class="data-row">
            <span class="data-row-label">h → konversi detik</span>
            <span class="data-row-val">{h_s:.0f} detik</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="result-hero">
          <div class="result-hero-label">A Total ({n_users_t1} pengguna)</div>
          <div class="result-hero-val">{A_tot:.4f}</div>
          <div class="result-hero-unit">Erlang — masukkan ke sidebar sebagai nilai A</div>
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


# ══════════════════════════════════════════════════════════════════════════════
# ██ HITUNG A — PENGGUNA AKTIF (BHT)
# ══════════════════════════════════════════════════════════════════════════════
elif active_page == "👥  A — Pengguna Aktif (BHT)":
    page_header("Hitung Traffic A", "Pengguna Aktif — Metode BHT",
                "Hitung Erlang dari jumlah pengguna aktif di jam sibuk")

    st.markdown("""
    <div class="formula-wrap">
      <span class="formula-tag">Rumus BHT — Method 2</span>
      <div class="formula-body">
A = U × BHT<br>
<br>
U   = jumlah pengguna aktif di jam sibuk<br>
BHT = Busy Hour Traffic per pengguna (Erlang)
      </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.85rem;font-weight:700;color:#0d1b3e;margin-bottom:1rem;">⚙️ Input Parameter</div>',
                    unsafe_allow_html=True)
        U_val = st.number_input("U — Pengguna aktif jam sibuk", 1, 10000, 50)
        BHT   = st.number_input("BHT — Busy Hour Traffic per user (Erl)",
                                 0.001, 1.0, 0.1, 0.001, format="%.3f")
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        A_t2 = U_val * BHT

        st.markdown(f"""
        <div class="card">
          <div style="font-size:0.85rem;font-weight:700;color:#0d1b3e;margin-bottom:1rem;">📊 Detail Perhitungan</div>
          <div class="data-row">
            <span class="data-row-label">Pengguna aktif (U)</span>
            <span class="data-row-val">{U_val} pengguna</span>
          </div>
          <div class="data-row">
            <span class="data-row-label">BHT per pengguna</span>
            <span class="data-row-val">{BHT:.3f} Erl</span>
          </div>
          <div class="data-row">
            <span class="data-row-label">Rumus: A = U × BHT</span>
            <span class="data-row-val">{U_val} × {BHT:.3f}</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="result-hero">
          <div class="result-hero-label">A Total (BHT Method)</div>
          <div class="result-hero-val">{A_t2:.4f}</div>
          <div class="result-hero-unit">Erlang — masukkan ke sidebar sebagai nilai A</div>
        </div>
        """, unsafe_allow_html=True)

        if 0 < A_t2 < S and S > N:
            P3 = engset(S, N, A_t2)
            if P3:
                g3, gc3 = gos_label(P3)
                cls = "eng-ok" if P3 < 0.01 else "eng-warn"
                st.markdown(f'<div class="{cls}">P = {P3:.6f} · Blocking = {P3*100:.3f}% · GoS = {g3}</div>',
                            unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ██ HITUNG A — DATA RATE / THROUGHPUT
# ══════════════════════════════════════════════════════════════════════════════
elif active_page == "🔁  A — Data Rate / Throughput":
    page_header("Hitung Traffic A", "Data Rate / Throughput",
                "Hitung Erlang dari data rate total dan kapasitas per kanal")

    st.markdown("""
    <div class="formula-wrap">
      <span class="formula-tag">Rumus Data Rate — Method 3</span>
      <div class="formula-body">
A = Data Rate Total (Mbps) / Kapasitas per Kanal (Mbps)<br>
<br>
A = R_total / R_channel
      </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.85rem;font-weight:700;color:#0d1b3e;margin-bottom:1rem;">⚙️ Input Parameter</div>',
                    unsafe_allow_html=True)
        dr = st.number_input("Data Rate total (Mbps)", 0.1, 100000.0, 100.0, 1.0)
        cc = st.number_input("Kapasitas per kanal (Mbps)", 0.1, 10000.0, 10.0, 0.1)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        A_t3 = dr / cc

        st.markdown(f"""
        <div class="card">
          <div style="font-size:0.85rem;font-weight:700;color:#0d1b3e;margin-bottom:1rem;">📊 Detail Perhitungan</div>
          <div class="data-row">
            <span class="data-row-label">Data Rate Total</span>
            <span class="data-row-val">{dr:.1f} Mbps</span>
          </div>
          <div class="data-row">
            <span class="data-row-label">Kapasitas per Kanal</span>
            <span class="data-row-val">{cc:.1f} Mbps</span>
          </div>
          <div class="data-row">
            <span class="data-row-label">Rumus: A = R_total / R_ch</span>
            <span class="data-row-val">{dr:.1f} / {cc:.1f}</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="result-hero">
          <div class="result-hero-label">A Total (Data Rate Method)</div>
          <div class="result-hero-val">{A_t3:.4f}</div>
          <div class="result-hero-unit">Erlang — masukkan ke sidebar sebagai nilai A</div>
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
# ██ ANALISIS & GRAFIK
# ══════════════════════════════════════════════════════════════════════════════
elif active_page == "📊  Analisis & Grafik":
    page_header("Visualisasi", "Analisis & Grafik",
                "Visualisasi perilaku sistem terhadap variasi parameter")

    if not valid:
        st.markdown('<div class="eng-warn">⚠️ Periksa parameter di sidebar.</div>',
                    unsafe_allow_html=True)
    else:
        cg1, cg2 = st.columns(2, gap="large")

        # ── Grafik 1: Blocking vs N ──────────────────────────────────────────
        with cg1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("##### 📈 Blocking vs Jumlah Kanal (N)")
            max_n = min(S-1, 50)
            ns_   = list(range(1, max_n+1))
            ps_   = [(engset(S,n,A) or 0)*100 for n in ns_]

            fig1, ax1 = plt.subplots(figsize=(5.5, 3.8))
            fig1.patch.set_facecolor(BG); ax1.set_facecolor(BG)
            ax1.fill_between(ns_, ps_, alpha=0.13, color=BLUE)
            ax1.plot(ns_, ps_, color=BLUE, linewidth=2.5, zorder=3)
            ax1.scatter([N], [P*100], color=RED, s=90, zorder=5,
                        label=f'N={N}, P={P*100:.3f}%')
            ax1.axhline(1.0, color=AMBER, linestyle='--', linewidth=1.2, alpha=0.8)
            ax1.text(max_n*0.97, 1.05, 'GoS 1%', ha='right', fontsize=8, color=AMBER)
            ax1.axhline(0.1, color=TEAL, linestyle='--', linewidth=1.2, alpha=0.8)
            ax1.text(max_n*0.97, 0.15, 'GoS 0.1%', ha='right', fontsize=8, color=TEAL)
            ax1.set_xlabel('N — Jumlah Kanal', fontsize=9, color='#5a6a8e')
            ax1.set_ylabel('Blocking (%)', fontsize=9, color='#5a6a8e')
            ax1.set_title(f'S={S}, A={A:.1f} Erl', fontsize=9, color='#8899bb')
            ax1.legend(fontsize=8.5)
            ax1.grid(True, linestyle='--', alpha=0.3)
            ax1.spines[['top','right']].set_visible(False)
            ax1.tick_params(colors='#8899bb', labelsize=8)
            plt.tight_layout(pad=1.0)
            st.pyplot(fig1, use_container_width=True)
            plt.close(fig1)
            st.markdown('</div>', unsafe_allow_html=True)

        # ── Grafik 2: Blocking vs A ──────────────────────────────────────────
        with cg2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("##### 📉 Blocking vs Traffic Offered (A)")
            a_max_ = min(float(S-1), 30.0)
            av_    = np.linspace(0.1, a_max_, 300)
            pv_    = [(engset(S,N,float(a)) or 0)*100 for a in av_]

            fig2, ax2 = plt.subplots(figsize=(5.5, 3.8))
            fig2.patch.set_facecolor(BG); ax2.set_facecolor(BG)
            ax2.fill_between(av_, pv_, alpha=0.13, color=TEAL)
            ax2.plot(av_, pv_, color=TEAL, linewidth=2.5, zorder=3)
            ax2.scatter([A], [P*100], color=RED, s=90, zorder=5,
                        label=f'A={A:.1f}, P={P*100:.3f}%')
            ax2.axhline(1.0, color=AMBER, linestyle='--', linewidth=1.2, alpha=0.8)
            ax2.text(a_max_*0.97, 1.05, 'GoS 1%', ha='right', fontsize=8, color=AMBER)
            ax2.set_xlabel('A — Traffic Offered (Erlang)', fontsize=9, color='#5a6a8e')
            ax2.set_ylabel('Blocking (%)', fontsize=9, color='#5a6a8e')
            ax2.set_title(f'S={S}, N={N} kanal', fontsize=9, color='#8899bb')
            ax2.legend(fontsize=8.5)
            ax2.grid(True, linestyle='--', alpha=0.3)
            ax2.spines[['top','right']].set_visible(False)
            ax2.tick_params(colors='#8899bb', labelsize=8)
            plt.tight_layout(pad=1.0)
            st.pyplot(fig2, use_container_width=True)
            plt.close(fig2)
            st.markdown('</div>', unsafe_allow_html=True)

        # ── Grafik 3: Multi-kurva ────────────────────────────────────────────
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("##### 🌐 Multi-kurva: Blocking vs N untuk Berbagai Nilai A")
        palette = [BLUE, TEAL, AMBER, RED, '#a855f7', '#ec4899']
        a_list  = [round(A*m,2) for m in [0.5,0.75,1.0,1.25,1.5,2.0] if 0 < A*m < S][:6]
        max_n3  = min(S-1, 35)
        ns3_    = list(range(1, max_n3+1))

        fig3, ax3 = plt.subplots(figsize=(11, 4))
        fig3.patch.set_facecolor(BG); ax3.set_facecolor(BG)
        for idx, a_c in enumerate(a_list):
            ps3 = [(engset(S,n,a_c) or 0)*100 for n in ns3_]
            ax3.plot(ns3_, ps3, color=palette[idx%len(palette)],
                     linewidth=2, label=f'A={a_c:.1f} Erl')
        ax3.axvline(N, color='#64748b', linestyle=':', linewidth=1.8,
                    label=f'N aktif = {N}')
        ax3.axhline(1.0, color=AMBER, linestyle='--', linewidth=1, alpha=0.6)
        ax3.set_xlabel('N — Jumlah Kanal', fontsize=9, color='#5a6a8e')
        ax3.set_ylabel('Blocking (%)', fontsize=9, color='#5a6a8e')
        ax3.set_title(f'Perbandingan Blocking vs N untuk Berbagai A (S={S})',
                      fontsize=10, color='#0d1b3e', fontweight='bold')
        ax3.legend(fontsize=8.5, ncol=min(len(a_list)+1, 4))
        ax3.grid(True, linestyle='--', alpha=0.3)
        ax3.spines[['top','right']].set_visible(False)
        ax3.tick_params(colors='#8899bb', labelsize=8)
        plt.tight_layout(pad=1.0)
        st.pyplot(fig3, use_container_width=True)
        plt.close(fig3)
        st.markdown('</div>', unsafe_allow_html=True)

        # ── Tabel detail ─────────────────────────────────────────────────────
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("##### 📋 Tabel Detail Blocking vs N")
        rows_html = ""
        for n_i in range(1, min(S, N+15)):
            p_i = engset(S, n_i, A)
            if p_i is None: continue
            c_i = A*(1-p_i); l_i = A*p_i; u_i = (c_i/n_i)*100
            g_t, g_c = gos_label(p_i)
            active_cls = 'class="active"' if n_i == N else ""
            rows_html += (f'<tr {active_cls}>'
                          f'<td>{"→ " if n_i==N else ""}{n_i}</td>'
                          f'<td>{p_i:.6f}</td><td>{p_i*100:.3f}%</td>'
                          f'<td>{c_i:.4f}</td><td>{l_i:.4f}</td>'
                          f'<td>{u_i:.1f}%</td>'
                          f'<td><span class="gos {g_c}">{g_t}</span></td></tr>')
        st.markdown(f"""
        <table class="eng-table">
          <thead>
            <tr><th>N</th><th>P Blocking</th><th>%</th>
                <th>Carried (Erl)</th><th>Lost (Erl)</th>
                <th>Utilisasi</th><th>GoS</th></tr>
          </thead>
          <tbody>{rows_html}</tbody>
        </table>
        <div class="eng-info" style="margin-top:8px;font-size:0.78rem;">
          🔵 Baris biru = nilai N yang dipilih saat ini (N={N})</div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ██ EXPORT LAPORAN
# ══════════════════════════════════════════════════════════════════════════════
elif active_page == "📄  Export Laporan":
    page_header("Export", "Export Laporan PDF",
                "Generate laporan profesional hasil analisis Engset")

    if not valid:
        st.markdown('<div class="eng-warn">⚠️ Periksa parameter di sidebar terlebih dahulu.</div>',
                    unsafe_allow_html=True)
    elif not PDF_OK:
        st.markdown('<div class="eng-warn">⚠️ Instal ReportLab: <code>pip install reportlab</code></div>',
                    unsafe_allow_html=True)
    else:
        c_prev, c_act = st.columns([1.5, 1], gap="large")

        with c_prev:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div style="font-size:0.9rem;font-weight:700;color:#0d1b3e;'
                        'margin-bottom:1rem;">📄 Preview Isi Laporan</div>',
                        unsafe_allow_html=True)
            items_prev = [
                ("📌", "Judul",           "EngsetPro — Laporan Perhitungan Engset"),
                ("📅", "Tanggal",         datetime.now().strftime('%d %B %Y, %H:%M')),
                ("🔢", "Parameter",       f"S={S}, N={N}, A={A:.1f} Erl"),
                ("📡", "P Blocking",      f"{P:.8f}"),
                ("📊", "Blocking %",      f"{P*100:.4f}%"),
                ("🏆", "GoS",             gos_text),
                ("✅", "Traffic Carried", f"{carried:.4f} Erlang"),
                ("❌", "Traffic Lost",    f"{lost:.4f} Erlang"),
                ("📈", "Grafik",          "Blocking vs N + Blocking vs A"),
                ("📋", "Tabel",           "Detail N dari 1 sampai N+10"),
            ]
            for icon, label, val in items_prev:
                st.markdown(f"""
                <div class="data-row">
                  <span class="data-row-label">{icon} {label}</span>
                  <span class="data-row-val" style="text-align:right;max-width:55%;">{val}</span>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with c_act:
            st.markdown("""
            <div class="card" style="text-align:center;padding:2rem 1.5rem;">
              <div style="font-size:3rem;margin-bottom:1rem;">📄</div>
              <div style="font-size:1rem;font-weight:700;color:#0d1b3e;margin-bottom:0.5rem;">
                Laporan PDF Profesional</div>
              <div style="font-size:0.82rem;color:#8899bb;margin-bottom:1.5rem;line-height:1.6;">
                Berisi rumus, parameter, hasil perhitungan, grafik analisis, dan tabel detail.
              </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("⬇️  Generate & Download PDF", use_container_width=True):
                with st.spinner("Membuat laporan PDF..."):
                    def cb(fig):
                        buf = io.BytesIO()
                        fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
                        buf.seek(0); return buf.read()

                    max_n_ = min(S-1, 40)
                    ns__   = list(range(1, max_n_+1))
                    ps__   = [(engset(S,n,A) or 0)*100 for n in ns__]
                    f1,a1  = plt.subplots(figsize=(7,3.5))
                    f1.patch.set_facecolor(BG); a1.set_facecolor(BG)
                    a1.fill_between(ns__, ps__, alpha=0.12, color=BLUE)
                    a1.plot(ns__, ps__, color=BLUE, linewidth=2)
                    a1.scatter([N],[P*100],color=RED,s=60,zorder=5)
                    a1.axhline(1.0,color=AMBER,linestyle='--',linewidth=1)
                    a1.set_xlabel('N (Jumlah Kanal)'); a1.set_ylabel('Blocking (%)')
                    a1.set_title(f'Blocking vs N | S={S}, A={A:.1f} Erl')
                    a1.grid(True,linestyle='--',alpha=0.3)
                    a1.spines[['top','right']].set_visible(False)
                    plt.tight_layout(); c1_bytes = cb(f1); plt.close(f1)

                    am_ = min(float(S-1),25.0)
                    av_ = np.linspace(0.1,am_,200)
                    pv_ = [(engset(S,N,float(a)) or 0)*100 for a in av_]
                    f2,a2 = plt.subplots(figsize=(7,3.5))
                    f2.patch.set_facecolor(BG); a2.set_facecolor(BG)
                    a2.fill_between(av_,pv_,alpha=0.12,color=TEAL)
                    a2.plot(av_,pv_,color=TEAL,linewidth=2)
                    a2.scatter([A],[P*100],color=RED,s=60,zorder=5)
                    a2.axhline(1.0,color=AMBER,linestyle='--',linewidth=1)
                    a2.set_xlabel('A (Erlang)'); a2.set_ylabel('Blocking (%)')
                    a2.set_title(f'Blocking vs A | S={S}, N={N}')
                    a2.grid(True,linestyle='--',alpha=0.3)
                    a2.spines[['top','right']].set_visible(False)
                    plt.tight_layout(); c2_bytes = cb(f2); plt.close(f2)

                    buf_pdf = io.BytesIO()
                    doc = SimpleDocTemplate(buf_pdf, pagesize=A4,
                        leftMargin=2*cm, rightMargin=2*cm,
                        topMargin=2*cm, bottomMargin=2*cm)
                    styles = getSampleStyleSheet()
                    el = []

                    T   = ParagraphStyle('T',  fontSize=20, textColor=colors.HexColor('#0d1b3e'),
                                         fontName='Helvetica-Bold', spaceAfter=4)
                    Sub = ParagraphStyle('Su', fontSize=10, textColor=colors.HexColor('#1a56ff'),
                                         spaceAfter=14)
                    H2  = ParagraphStyle('H2', fontSize=13, textColor=colors.HexColor('#0d1b3e'),
                                         fontName='Helvetica-Bold', spaceBefore=12, spaceAfter=6)
                    B   = ParagraphStyle('B',  fontSize=9.5, textColor=colors.HexColor('#2d3a5e'),
                                         leading=14)
                    M   = ParagraphStyle('M',  fontSize=9, fontName='Courier',
                                         textColor=colors.HexColor('#0d2060'),
                                         backColor=colors.HexColor('#f0f4ff'),
                                         leftIndent=10, rightIndent=10,
                                         spaceBefore=4, spaceAfter=4, leading=16)
                    FC  = ParagraphStyle('FC', fontSize=8,
                                         textColor=colors.HexColor('#8492ab'),
                                         alignment=TA_CENTER)

                    el.append(Paragraph("EngsetPro", T))
                    el.append(Paragraph(
                        f"Laporan Analisis Engset — {datetime.now().strftime('%d %B %Y, %H:%M')}", Sub))
                    el.append(HRFlowable(width="100%", thickness=1.5,
                                          color=colors.HexColor('#1a56ff'), spaceAfter=14))

                    el.append(Paragraph("Rumus Engset", H2))
                    el.append(Paragraph(
                        "       C(S-1,N) × (A/(S-A))^N<br/>"
                        "P = ─────────────────────────────<br/>"
                        "    N<br/>"
                        "   Σ  C(S-1,i) × (A/(S-A))^i<br/>"
                        "  i=0", M))
                    el.append(Paragraph(
                        "<b>P</b>=blocking | <b>S</b>=source | <b>N</b>=kanal | <b>A</b>=traffic", B))
                    el.append(Spacer(1,10))

                    el.append(Paragraph("Parameter Input", H2))
                    pd2 = [["Parameter","Simbol","Nilai","Satuan"],
                            ["Jumlah Source","S",str(S),"pengguna"],
                            ["Jumlah Kanal","N",str(N),"kanal"],
                            ["Traffic Offered","A",f"{A:.1f}","Erlang"]]
                    pt = Table(pd2, colWidths=[5.5*cm,2*cm,2.5*cm,3.5*cm])
                    pt.setStyle(TableStyle([
                        ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#1a56ff')),
                        ('TEXTCOLOR',(0,0),(-1,0),colors.white),
                        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
                        ('FONTSIZE',(0,0),(-1,-1),9),
                        ('ALIGN',(0,0),(-1,-1),'CENTER'),
                        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f0f4ff')]),
                        ('GRID',(0,0),(-1,-1),0.5,colors.HexColor('#c7d7ff')),
                        ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
                    ]))
                    el.append(pt); el.append(Spacer(1,10))

                    el.append(Paragraph("Hasil Perhitungan", H2))
                    rd2 = [["Metrik","Nilai","Keterangan"],
                            ["P Blocking",f"{P:.8f}","Probabilitas blocking"],
                            ["Blocking %",f"{P*100:.4f}%","Persentase terblokir"],
                            ["Grade of Service",gos_text,"Kualitas layanan"],
                            ["Traffic Carried",f"{carried:.4f} Erl","Terlayani"],
                            ["Traffic Lost",f"{lost:.4f} Erl","Terblokir"],
                            ["Utilisasi",f"{util_pct:.2f}%","Rata-rata per kanal"]]
                    rt = Table(rd2, colWidths=[5.5*cm,3.5*cm,6*cm])
                    rt.setStyle(TableStyle([
                        ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#0d1b3e')),
                        ('TEXTCOLOR',(0,0),(-1,0),colors.white),
                        ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
                        ('FONTSIZE',(0,0),(-1,-1),9),
                        ('ALIGN',(0,0),(-1,-1),'LEFT'),
                        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#eff6ff')]),
                        ('GRID',(0,0),(-1,-1),0.5,colors.HexColor('#c7d7ff')),
                        ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
                    ]))
                    el.append(rt); el.append(Spacer(1,14))

                    el.append(Paragraph("Grafik Analisis", H2))
                    el.append(RLImage(io.BytesIO(c1_bytes), width=16*cm, height=7*cm))
                    el.append(Spacer(1,10))
                    el.append(RLImage(io.BytesIO(c2_bytes), width=16*cm, height=7*cm))
                    el.append(Spacer(1,14))
                    el.append(HRFlowable(width="100%",thickness=0.5,
                                          color=colors.HexColor('#e8ecf4'),spaceAfter=8))
                    el.append(Paragraph(
                        f"EngsetPro v2.0 · {datetime.now().strftime('%d %B %Y')} · Rekayasa Trafik",FC))

                    doc.build(el)
                    buf_pdf.seek(0)

                st.download_button(
                    "📥  Klik untuk Download PDF",
                    data=buf_pdf,
                    file_name=f"engset_S{S}_N{N}_A{A:.1f}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )
                st.markdown('<div class="eng-ok">✅ PDF siap! Klik tombol di atas untuk mengunduh.</div>',
                            unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;color:#aab5cc;font-size:0.75rem;
     padding:2.5rem 0 1rem;letter-spacing:0.04em;">
  EngsetPro v2.0 &nbsp;·&nbsp; Kalkulator Rekayasa Trafik Engset &nbsp;·&nbsp;
  Metode: Log-space Arithmetic
</div>
""", unsafe_allow_html=True)# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,300&family=DM+Mono:wght@400;500&family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,700;1,9..144,300&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0a0f1e !important;
    border-right: 1px solid #1e2840;
}
[data-testid="stSidebar"] * {
    color: #c8d4f0 !important;
}
[data-testid="stSidebar"] .stSlider > label,
[data-testid="stSidebar"] .stNumberInput > label {
    color: #7b91c9 !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #e8eeff !important;
    font-family: 'Fraunces', serif !important;
}

/* ── Main ── */
.main .block-container {
    padding-top: 2rem;
    max-width: 1200px;
}

/* ── Header ── */
.eng-header {
    background: linear-gradient(135deg, #0d1b3e 0%, #112357 60%, #0f2b5e 100%);
    border-radius: 16px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    border: 1px solid #1e3270;
    position: relative;
    overflow: hidden;
}
.eng-header::before {
    content: "";
    position: absolute;
    top: -60px; right: -60px;
    width: 260px; height: 260px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(56,120,255,0.18) 0%, transparent 70%);
}
.eng-header::after {
    content: "";
    position: absolute;
    bottom: -40px; left: 40%;
    width: 180px; height: 180px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(0,200,180,0.12) 0%, transparent 70%);
}
.eng-title {
    font-family: 'Fraunces', serif;
    font-size: 2.6rem;
    font-weight: 700;
    color: #ffffff;
    margin: 0 0 0.3rem;
    letter-spacing: -0.02em;
    line-height: 1.1;
}
.eng-subtitle {
    font-size: 1rem;
    color: #7ba4f0;
    margin: 0;
    font-weight: 300;
}
.eng-badge {
    display: inline-block;
    background: rgba(56,120,255,0.2);
    border: 1px solid rgba(56,120,255,0.4);
    color: #7ab2ff;
    font-size: 0.72rem;
    font-family: 'DM Mono', monospace;
    padding: 3px 10px;
    border-radius: 100px;
    margin-bottom: 1rem;
    letter-spacing: 0.1em;
}

/* ── Metric Cards ── */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-bottom: 1.5rem;
}
.metric-card {
    background: #ffffff;
    border: 1px solid #e8ecf4;
    border-radius: 14px;
    padding: 1.25rem 1.5rem;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: "";
    position: absolute;
    top: 0; left: 0;
    width: 4px; height: 100%;
    border-radius: 14px 0 0 14px;
}
.metric-card.blue::before  { background: #3878ff; }
.metric-card.teal::before  { background: #00c8b4; }
.metric-card.amber::before { background: #f59e0b; }
.metric-card.red::before   { background: #ef4444; }
.metric-card.green::before { background: #22c55e; }
.metric-card.slate::before { background: #64748b; }

.metric-label {
    font-size: 0.72rem;
    font-weight: 500;
    color: #8492ab;
    text-transform: uppercase;
    letter-spacing: 0.09em;
    margin-bottom: 0.5rem;
}
.metric-value {
    font-size: 2rem;
    font-weight: 600;
    color: #0d1b3e;
    line-height: 1;
    font-family: 'DM Mono', monospace;
}
.metric-unit {
    font-size: 0.8rem;
    color: #8492ab;
    margin-top: 0.35rem;
}

/* ── Formula Box ── */
.formula-box {
    background: #f8faff;
    border: 1px solid #d6e0ff;
    border-radius: 14px;
    padding: 1.5rem 2rem;
    margin-bottom: 1.5rem;
    font-family: 'DM Mono', monospace;
    font-size: 0.85rem;
    color: #1e2f6b;
    line-height: 2.2;
}
.formula-title {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #3878ff;
    margin-bottom: 0.75rem;
}

/* ── Section Title ── */
.sec-title {
    font-family: 'Fraunces', serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: #0d1b3e;
    margin: 0 0 1rem;
}

/* ── Warning / Info banners ── */
.eng-warn {
    background: #fff7ed;
    border: 1px solid #fed7aa;
    border-radius: 10px;
    padding: 0.85rem 1.2rem;
    color: #92400e;
    font-size: 0.88rem;
    margin-bottom: 1rem;
}
.eng-info {
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    border-radius: 10px;
    padding: 0.85rem 1.2rem;
    color: #1e40af;
    font-size: 0.88rem;
    margin-bottom: 1rem;
}
.eng-success {
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    border-radius: 10px;
    padding: 0.85rem 1.2rem;
    color: #166534;
    font-size: 0.88rem;
    margin-bottom: 1rem;
}

/* ── GoS Badge ── */
.gos-badge {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 100px;
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.05em;
}
.gos-great  { background: #dcfce7; color: #166534; }
.gos-good   { background: #d1fae5; color: #065f46; }
.gos-ok     { background: #fef9c3; color: #713f12; }
.gos-bad    { background: #fee2e2; color: #7f1d1d; }

/* ── Table ── */
.eng-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.88rem;
}
.eng-table th {
    background: #f1f5ff;
    color: #3878ff;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    padding: 10px 14px;
    text-align: left;
    border-bottom: 1px solid #dde5ff;
}
.eng-table td {
    padding: 9px 14px;
    border-bottom: 1px solid #f1f3f8;
    color: #2d3a5e;
    font-family: 'DM Mono', monospace;
}
.eng-table tr:hover td { background: #f8faff; }

/* ── Divider ── */
.eng-divider {
    border: none;
    border-top: 1px solid #e8ecf4;
    margin: 2rem 0;
}

/* ── Responsive metric grid ── */
@media (max-width: 768px) {
    .metric-grid { grid-template-columns: 1fr 1fr; }
    .eng-title   { font-size: 1.8rem; }
}
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# ENGSET CORE (log-space untuk stabilitas numerik)
# ═══════════════════════════════════════════════════════════════════════════════
def log_factorial(n: int) -> float:
    if n <= 1:
        return 0.0
    return sum(log(i) for i in range(2, n + 1))

def log_comb(n: int, k: int) -> float:
    if k < 0 or k > n:
        return float('-inf')
    return log_factorial(n) - log_factorial(k) - log_factorial(n - k)

def engset(S: int, N: int, A: float) -> float | None:
    """
    Rumus Engset dari dosen:
        P = C(S-1,N)*(A/(S-A))^N  /  sum_{i=0}^{N} C(S-1,i)*(A/(S-A))^i
    """
    if A <= 0 or A >= S or N <= 0 or S <= N:
        return None
    ratio = A / (S - A)
    if ratio <= 0:
        return None

    log_ratio = log(ratio)
    log_numer = log_comb(S - 1, N) + N * log_ratio

    log_terms = [log_comb(S - 1, i) + i * log_ratio for i in range(N + 1)]
    max_t = max(log_terms)
    log_denom = max_t + log(sum(exp(t - max_t) for t in log_terms))

    p = exp(log_numer - log_denom)
    return max(0.0, min(1.0, p))

def gos_label(p: float) -> tuple[str, str]:
    if p < 0.001:
        return "Sangat Baik", "gos-great"
    if p < 0.01:
        return "Baik", "gos-good"
    if p < 0.05:
        return "Cukup", "gos-ok"
    return "Buruk", "gos-bad"


# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 📡 EngsetPro")
    st.markdown("**Kalkulator Engset** — Rekayasa Trafik Telekomunikasi")
    st.markdown("---")

    st.markdown("### Parameter Utama")

    S = st.slider(
        "S — Jumlah Source / Pengguna",
        min_value=2, max_value=200, value=20, step=1,
        help="Jumlah total pengguna yang bisa membangkitkan trafik"
    )
    N = st.slider(
        "N — Jumlah Server / Kanal",
        min_value=1, max_value=100, value=5, step=1,
        help="Jumlah kanal atau server yang tersedia"
    )
    A = st.slider(
        "A — Traffic Offered (Erlang)",
        min_value=0.1, max_value=float(S - 1), value=min(8.0, float(S - 2)),
        step=0.1,
        help="Total traffic yang ditawarkan ke grup server"
    )

    st.markdown("---")
    st.markdown("### Opsi Grafik")
    show_multi = st.checkbox("Tampilkan multi-kurva A", value=False)
    show_table = st.checkbox("Tampilkan tabel detail", value=True)

    st.markdown("---")
    st.markdown("### Tentang Rumus")
    st.markdown("""
Rumus **Engset** digunakan untuk menghitung probabilitas blocking
pada sistem telekomunikasi dengan sumber trafik terbatas (*finite source*).

Berbeda dengan Erlang-B yang mengasumsikan sumber tak terbatas,
Engset memperhitungkan jumlah source **S** yang terbatas.
""")

    st.markdown("---")
    now = datetime.now().strftime("%d %b %Y, %H:%M")
    st.caption(f"🕐 {now}")
    st.caption("EngsetPro v2.0 · Rekayasa Trafik")


# ═══════════════════════════════════════════════════════════════════════════════
# VALIDASI
# ═══════════════════════════════════════════════════════════════════════════════
valid = True
if S <= N:
    st.markdown('<div class="eng-warn">⚠️ <strong>Error:</strong> Jumlah source <em>S</em> harus lebih besar dari jumlah kanal <em>N</em> (S > N).</div>', unsafe_allow_html=True)
    valid = False
if A >= S:
    st.markdown('<div class="eng-warn">⚠️ <strong>Error:</strong> Traffic offered <em>A</em> harus lebih kecil dari jumlah source <em>S</em> (A < S).</div>', unsafe_allow_html=True)
    valid = False


# ═══════════════════════════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="eng-header">
  <div class="eng-badge">REKAYASA TRAFIK TELEKOMUNIKASI</div>
  <h1 class="eng-title">EngsetPro</h1>
  <p class="eng-subtitle">Kalkulator Probabilitas Blocking — Model Engset (Finite Source)</p>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# RUMUS BOX
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="formula-box">
  <div class="formula-title">Rumus Engset</div>
  <div>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;C(S-1, N) &times; (A / (S-A))&sup;N<br>
  P &nbsp;= &nbsp; ─────────────────────────────────────────<br>
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;N<br>
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &Sigma;  C(S-1, i) &times; (A / (S-A))&sup;i<br>
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;i=0
  </div>
  <div style="margin-top:1rem; font-family:'DM Sans',sans-serif; font-size:0.82rem; color:#4a5680; line-height:2;">
    <strong>P</strong> = Probabilitas blocking &nbsp;|&nbsp;
    <strong>S</strong> = Jumlah source / pengguna &nbsp;|&nbsp;
    <strong>N</strong> = Jumlah server / kanal &nbsp;|&nbsp;
    <strong>A</strong> = Traffic offered (Erlang)
  </div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PERHITUNGAN UTAMA
# ═══════════════════════════════════════════════════════════════════════════════
if valid:
    P = engset(S, N, A)

    if P is None:
        st.markdown('<div class="eng-warn">⚠️ Perhitungan gagal — periksa kembali nilai parameter.</div>', unsafe_allow_html=True)
        st.stop()

    carried    = A * (1 - P)
    lost       = A * P
    util_pct   = (carried / N) * 100
    traffic_intensity = A / N
    gos_text, gos_cls = gos_label(P)

    # ── Metric Cards ─────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="metric-grid">
      <div class="metric-card blue">
        <div class="metric-label">Blocking Probability (P)</div>
        <div class="metric-value">{P:.6f}</div>
        <div class="metric-unit">probabilitas</div>
      </div>
      <div class="metric-card teal">
        <div class="metric-label">Blocking (%)</div>
        <div class="metric-value">{P*100:.3f}%</div>
        <div class="metric-unit">persentase blocking</div>
      </div>
      <div class="metric-card {'green' if P < 0.01 else 'amber' if P < 0.05 else 'red'}">
        <div class="metric-label">Grade of Service</div>
        <div class="metric-value" style="font-size:1.4rem;">{gos_text}</div>
        <div class="metric-unit">penilaian kualitas layanan</div>
      </div>
      <div class="metric-card slate">
        <div class="metric-label">Traffic Carried</div>
        <div class="metric-value">{carried:.4f}</div>
        <div class="metric-unit">Erlang terlayani</div>
      </div>
      <div class="metric-card amber">
        <div class="metric-label">Traffic Lost</div>
        <div class="metric-value">{lost:.4f}</div>
        <div class="metric-unit">Erlang terblokir</div>
      </div>
      <div class="metric-card green">
        <div class="metric-label">Utilisasi Kanal</div>
        <div class="metric-value">{util_pct:.1f}%</div>
        <div class="metric-unit">rata-rata per kanal</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Info banner ───────────────────────────────────────────────────────────
    if P < 0.001:
        st.markdown(f'<div class="eng-success">✅ Sistem dalam kondisi <strong>sangat baik</strong> — probabilitas blocking hanya {P*100:.4f}%. Jaringan sangat memadai untuk trafik saat ini.</div>', unsafe_allow_html=True)
    elif P < 0.01:
        st.markdown(f'<div class="eng-success">✅ Sistem dalam kondisi <strong>baik</strong> — probabilitas blocking {P*100:.3f}%. Masih dalam batas kualitas layanan yang dapat diterima.</div>', unsafe_allow_html=True)
    elif P < 0.05:
        st.markdown(f'<div class="eng-warn">⚠️ Sistem dalam kondisi <strong>cukup</strong> — probabilitas blocking {P*100:.3f}%. Pertimbangkan penambahan kanal untuk meningkatkan kualitas layanan.</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="eng-warn">🔴 Sistem dalam kondisi <strong>buruk</strong> — probabilitas blocking {P*100:.2f}%. Perlu penambahan kanal segera!</div>', unsafe_allow_html=True)

    st.markdown('<hr class="eng-divider">', unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════════════════
    # GRAFIK
    # ═══════════════════════════════════════════════════════════════════════════
    st.markdown('<p class="sec-title">📈 Grafik Analisis</p>', unsafe_allow_html=True)

    col_g1, col_g2 = st.columns(2)

    # ── Grafik 1 : Blocking vs N ──────────────────────────────────────────────
    with col_g1:
        max_n_plot = min(S - 1, 40)
        ns   = list(range(1, max_n_plot + 1))
        ps   = [engset(S, n, A) or 0 for n in ns]
        pcts = [p * 100 for p in ps]

        fig1, ax1 = plt.subplots(figsize=(6, 4))
        fig1.patch.set_facecolor('#f8faff')
        ax1.set_facecolor('#f8faff')

        ax1.fill_between(ns, pcts, alpha=0.15, color='#3878ff')
        ax1.plot(ns, pcts, color='#3878ff', linewidth=2.5, zorder=3)

        # titik aktif
        ax1.scatter([N], [P * 100], color='#ef4444', s=80, zorder=5,
                    label=f'N={N}  →  P={P*100:.3f}%')

        # referensi GoS
        for ref, lbl, col in [(1.0, 'GoS 1%', '#f59e0b'), (0.1, 'GoS 0.1%', '#22c55e')]:
            ax1.axhline(ref, color=col, linestyle='--', linewidth=1.2, alpha=0.7)
            ax1.text(max_n_plot * 0.98, ref + 0.02, lbl,
                     ha='right', va='bottom', fontsize=8, color=col)

        ax1.set_xlabel('N — Jumlah Kanal', fontsize=10, color='#2d3a5e')
        ax1.set_ylabel('Blocking Probability (%)', fontsize=10, color='#2d3a5e')
        ax1.set_title(f'Blocking vs Jumlah Kanal\n(S={S}, A={A:.1f} Erl)', fontsize=11,
                      color='#0d1b3e', fontweight='bold')
        ax1.legend(fontsize=9, framealpha=0.9)
        ax1.grid(True, linestyle='--', alpha=0.4)
        ax1.spines[['top', 'right']].set_visible(False)
        ax1.tick_params(colors='#5a6a8e')
        plt.tight_layout()

        st.pyplot(fig1)
        plt.close(fig1)

    # ── Grafik 2 : Blocking vs A ──────────────────────────────────────────────
    with col_g2:
        a_max  = max(1.0, min(S - 1, 30.0))
        a_vals = np.linspace(0.1, a_max, 200)
        p_vals = [engset(S, N, float(a)) or 0 for a in a_vals]
        p_pcts = [p * 100 for p in p_vals]

        fig2, ax2 = plt.subplots(figsize=(6, 4))
        fig2.patch.set_facecolor('#f8faff')
        ax2.set_facecolor('#f8faff')

        ax2.fill_between(a_vals, p_pcts, alpha=0.15, color='#00c8b4')
        ax2.plot(a_vals, p_pcts, color='#00c8b4', linewidth=2.5, zorder=3)
        ax2.scatter([A], [P * 100], color='#ef4444', s=80, zorder=5,
                    label=f'A={A:.1f}  →  P={P*100:.3f}%')

        ax2.axhline(1.0, color='#f59e0b', linestyle='--', linewidth=1.2, alpha=0.7)
        ax2.text(a_max * 0.98, 1.0 + 0.02, 'GoS 1%',
                 ha='right', va='bottom', fontsize=8, color='#f59e0b')

        ax2.set_xlabel('A — Traffic Offered (Erlang)', fontsize=10, color='#2d3a5e')
        ax2.set_ylabel('Blocking Probability (%)', fontsize=10, color='#2d3a5e')
        ax2.set_title(f'Blocking vs Traffic Offered\n(S={S}, N={N} kanal)', fontsize=11,
                      color='#0d1b3e', fontweight='bold')
        ax2.legend(fontsize=9, framealpha=0.9)
        ax2.grid(True, linestyle='--', alpha=0.4)
        ax2.spines[['top', 'right']].set_visible(False)
        ax2.tick_params(colors='#5a6a8e')
        plt.tight_layout()

        st.pyplot(fig2)
        plt.close(fig2)

    # ── Grafik 3 : Multi-kurva (opsional) ────────────────────────────────────
    if show_multi:
        st.markdown("##### Multi-kurva: Blocking vs N untuk berbagai nilai A")
        palette = ['#3878ff', '#00c8b4', '#f59e0b', '#ef4444', '#a855f7']
        a_list  = [max(0.1, A * m) for m in [0.5, 0.75, 1.0, 1.25, 1.5]
                   if A * m < S][:5]

        fig3, ax3 = plt.subplots(figsize=(10, 4))
        fig3.patch.set_facecolor('#f8faff')
        ax3.set_facecolor('#f8faff')

        for idx, a_cur in enumerate(a_list):
            if a_cur >= S:
                continue
            ns_m  = list(range(1, min(S - 1, 30) + 1))
            ps_m  = [engset(S, n, a_cur) or 0 for n in ns_m]
            pcts_m = [p * 100 for p in ps_m]
            ax3.plot(ns_m, pcts_m, color=palette[idx % len(palette)],
                     linewidth=2, label=f'A = {a_cur:.1f} Erl')

        ax3.axvline(N, color='#64748b', linestyle=':', linewidth=1.5,
                    label=f'N saat ini = {N}')
        ax3.set_xlabel('N — Jumlah Kanal', fontsize=10, color='#2d3a5e')
        ax3.set_ylabel('Blocking (%)', fontsize=10, color='#2d3a5e')
        ax3.set_title(f'Perbandingan Blocking untuk Berbagai A (S={S})',
                      fontsize=11, color='#0d1b3e', fontweight='bold')
        ax3.legend(fontsize=9, framealpha=0.9)
        ax3.grid(True, linestyle='--', alpha=0.4)
        ax3.spines[['top', 'right']].set_visible(False)
        plt.tight_layout()
        st.pyplot(fig3)
        plt.close(fig3)

    # ═══════════════════════════════════════════════════════════════════════════
    # TABEL DETAIL
    # ═══════════════════════════════════════════════════════════════════════════
    if show_table:
        st.markdown('<hr class="eng-divider">', unsafe_allow_html=True)
        st.markdown('<p class="sec-title">📋 Tabel Detail — Blocking vs Jumlah Kanal</p>',
                    unsafe_allow_html=True)

        rows_html = ""
        for n_i in range(max(1, N - 5), min(S, N + 11)):
            p_i = engset(S, n_i, A)
            if p_i is None:
                continue
            c_i = A * (1 - p_i)
            l_i = A * p_i
            u_i = (c_i / n_i) * 100
            g_text, g_cls = gos_label(p_i)
            highlight = 'background:#eff6ff;' if n_i == N else ''
            rows_html += f"""
            <tr style="{highlight}">
              <td>{'<strong>' if n_i==N else ''}{n_i}{'</strong>' if n_i==N else ''}</td>
              <td>{p_i:.6f}</td>
              <td>{p_i*100:.3f}%</td>
              <td>{c_i:.4f}</td>
              <td>{l_i:.4f}</td>
              <td>{u_i:.1f}%</td>
              <td><span class="gos-badge {g_cls}">{g_text}</span></td>
            </tr>"""

        st.markdown(f"""
        <table class="eng-table">
          <thead>
            <tr>
              <th>N (Kanal)</th>
              <th>P Blocking</th>
              <th>Blocking %</th>
              <th>Traffic Carried</th>
              <th>Traffic Lost</th>
              <th>Utilisasi</th>
              <th>Grade of Service</th>
            </tr>
          </thead>
          <tbody>{rows_html}</tbody>
        </table>
        """, unsafe_allow_html=True)

        st.markdown('<div class="eng-info" style="margin-top:0.75rem;">🔵 Baris biru = parameter N yang saat ini dipilih.</div>',
                    unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════════════════
    # EXPORT PDF
    # ═══════════════════════════════════════════════════════════════════════════
    st.markdown('<hr class="eng-divider">', unsafe_allow_html=True)
    st.markdown('<p class="sec-title">📄 Export Laporan</p>', unsafe_allow_html=True)

    if not PDF_OK:
        st.markdown('<div class="eng-warn">⚠️ Library <code>reportlab</code> tidak terinstal. Jalankan: <code>pip install reportlab</code></div>', unsafe_allow_html=True)
    else:
        if st.button("⬇️ Download Laporan PDF", type="primary"):

            # buat gambar untuk PDF
            def make_chart_bytes(fig) -> bytes:
                buf = io.BytesIO()
                fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
                buf.seek(0)
                return buf.read()

            fig_p1, ax_p1 = plt.subplots(figsize=(7, 3.5))
            ax_p1.fill_between(ns, pcts, alpha=0.15, color='#3878ff')
            ax_p1.plot(ns, pcts, color='#3878ff', linewidth=2)
            ax_p1.scatter([N], [P * 100], color='#ef4444', s=60, zorder=5)
            ax_p1.set_xlabel('N (Jumlah Kanal)')
            ax_p1.set_ylabel('Blocking (%)')
            ax_p1.set_title(f'Blocking vs Jumlah Kanal (S={S}, A={A:.1f})')
            ax_p1.grid(True, linestyle='--', alpha=0.4)
            plt.tight_layout()
            chart1_bytes = make_chart_bytes(fig_p1)
            plt.close(fig_p1)

            fig_p2, ax_p2 = plt.subplots(figsize=(7, 3.5))
            ax_p2.fill_between(a_vals, p_pcts, alpha=0.15, color='#00c8b4')
            ax_p2.plot(a_vals, p_pcts, color='#00c8b4', linewidth=2)
            ax_p2.scatter([A], [P * 100], color='#ef4444', s=60, zorder=5)
            ax_p2.set_xlabel('A - Traffic Offered (Erlang)')
            ax_p2.set_ylabel('Blocking (%)')
            ax_p2.set_title(f'Blocking vs Traffic Offered (S={S}, N={N})')
            ax_p2.grid(True, linestyle='--', alpha=0.4)
            plt.tight_layout()
            chart2_bytes = make_chart_bytes(fig_p2)
            plt.close(fig_p2)

            # build PDF
            buf_pdf = io.BytesIO()
            doc = SimpleDocTemplate(
                buf_pdf, pagesize=A4,
                leftMargin=2*cm, rightMargin=2*cm,
                topMargin=2*cm, bottomMargin=2*cm
            )
            styles = getSampleStyleSheet()
            elements = []

            title_style = ParagraphStyle(
                'Title2', parent=styles['Title'],
                fontSize=20, textColor=colors.HexColor('#0d1b3e'),
                spaceAfter=4, fontName='Helvetica-Bold'
            )
            sub_style = ParagraphStyle(
                'Sub', parent=styles['Normal'],
                fontSize=10, textColor=colors.HexColor('#3878ff'),
                spaceAfter=16
            )
            h2_style = ParagraphStyle(
                'H2', parent=styles['Heading2'],
                fontSize=13, textColor=colors.HexColor('#0d1b3e'),
                fontName='Helvetica-Bold', spaceBefore=14, spaceAfter=6
            )
            body_style = ParagraphStyle(
                'Body2', parent=styles['Normal'],
                fontSize=9.5, textColor=colors.HexColor('#2d3a5e'),
                leading=14
            )
            mono_style = ParagraphStyle(
                'Mono', parent=styles['Normal'],
                fontSize=9, fontName='Courier',
                textColor=colors.HexColor('#1e2f6b'),
                backColor=colors.HexColor('#f8faff'),
                leftIndent=12, rightIndent=12,
                spaceBefore=4, spaceAfter=4, leading=16
            )

            elements.append(Paragraph("EngsetPro", title_style))
            elements.append(Paragraph(
                f"Laporan Perhitungan Probabilitas Blocking — {datetime.now().strftime('%d %B %Y, %H:%M')}",
                sub_style
            ))
            elements.append(HRFlowable(width="100%", thickness=1,
                                        color=colors.HexColor('#3878ff'), spaceAfter=14))

            elements.append(Paragraph("Rumus Engset", h2_style))
            elements.append(Paragraph(
                "C(S-1, N) × (A/(S-A))^N<br/>"
                "P = ──────────────────────────────<br/>"
                "Σ[i=0..N] C(S-1, i) × (A/(S-A))^i",
                mono_style
            ))
            elements.append(Paragraph(
                "<b>P</b> = Probabilitas blocking &nbsp; | &nbsp;"
                "<b>S</b> = Jumlah source &nbsp; | &nbsp;"
                "<b>N</b> = Jumlah kanal &nbsp; | &nbsp;"
                "<b>A</b> = Traffic offered (Erlang)",
                body_style
            ))
            elements.append(Spacer(1, 12))

            elements.append(Paragraph("Parameter Input", h2_style))
            param_data = [
                ["Parameter", "Simbol", "Nilai", "Satuan"],
                ["Jumlah Source / Pengguna", "S", str(S), "pengguna"],
                ["Jumlah Server / Kanal", "N", str(N), "kanal"],
                ["Traffic Offered", "A", f"{A:.1f}", "Erlang"],
            ]
            param_tbl = Table(param_data, colWidths=[5.5*cm, 2*cm, 2.5*cm, 3.5*cm])
            param_tbl.setStyle(TableStyle([
                ('BACKGROUND',   (0, 0), (-1, 0),  colors.HexColor('#3878ff')),
                ('TEXTCOLOR',    (0, 0), (-1, 0),  colors.white),
                ('FONTNAME',     (0, 0), (-1, 0),  'Helvetica-Bold'),
                ('FONTSIZE',     (0, 0), (-1, 0),  9),
                ('ALIGN',        (0, 0), (-1, -1), 'CENTER'),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8faff')]),
                ('GRID',         (0, 0), (-1, -1),  0.5, colors.HexColor('#dde5ff')),
                ('FONTSIZE',     (0, 1), (-1, -1),  9),
                ('TOPPADDING',   (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING',(0, 0), (-1, -1), 6),
            ]))
            elements.append(param_tbl)
            elements.append(Spacer(1, 12))

            elements.append(Paragraph("Hasil Perhitungan", h2_style))
            result_data = [
                ["Metrik", "Nilai", "Keterangan"],
                ["Probabilitas Blocking (P)", f"{P:.8f}", "Probabilitas panggilan diblokir"],
                ["Blocking (%)", f"{P*100:.4f}%", "Persentase panggilan terblokir"],
                ["Grade of Service", gos_text, "Penilaian kualitas layanan"],
                ["Traffic Carried", f"{carried:.4f} Erl", "Traffic yang berhasil dilayani"],
                ["Traffic Lost", f"{lost:.4f} Erl", "Traffic yang terblokir"],
                ["Utilisasi Kanal", f"{util_pct:.2f}%", "Rata-rata utilisasi per kanal"],
            ]
            res_tbl = Table(result_data, colWidths=[5.5*cm, 3.5*cm, 6*cm])
            res_tbl.setStyle(TableStyle([
                ('BACKGROUND',   (0, 0), (-1, 0),  colors.HexColor('#0d1b3e')),
                ('TEXTCOLOR',    (0, 0), (-1, 0),  colors.white),
                ('FONTNAME',     (0, 0), (-1, 0),  'Helvetica-Bold'),
                ('FONTSIZE',     (0, 0), (-1, 0),  9),
                ('ALIGN',        (0, 0), (-1, -1), 'LEFT'),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#eff6ff')]),
                ('GRID',         (0, 0), (-1, -1),  0.5, colors.HexColor('#dde5ff')),
                ('FONTSIZE',     (0, 1), (-1, -1),  9),
                ('TOPPADDING',   (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING',(0, 0), (-1, -1), 6),
            ]))
            elements.append(res_tbl)
            elements.append(Spacer(1, 14))

            elements.append(Paragraph("Grafik Analisis", h2_style))

            img1_buf = io.BytesIO(chart1_bytes)
            img1 = RLImage(img1_buf, width=16*cm, height=7*cm)
            elements.append(img1)
            elements.append(Spacer(1, 10))

            img2_buf = io.BytesIO(chart2_bytes)
            img2 = RLImage(img2_buf, width=16*cm, height=7*cm)
            elements.append(img2)
            elements.append(Spacer(1, 14))

            elements.append(HRFlowable(width="100%", thickness=0.5,
                                        color=colors.HexColor('#e8ecf4'), spaceAfter=8))
            elements.append(Paragraph(
                f"Digenerate oleh EngsetPro · {datetime.now().strftime('%d %B %Y')} · "
                "Rekayasa Trafik Telekomunikasi",
                ParagraphStyle('Footer', parent=styles['Normal'],
                               fontSize=8, textColor=colors.HexColor('#8492ab'),
                               alignment=TA_CENTER)
            ))

            doc.build(elements)
            buf_pdf.seek(0)

            st.download_button(
                label="📥 Klik di sini untuk mengunduh PDF",
                data=buf_pdf,
                file_name=f"engset_S{S}_N{N}_A{A:.1f}.pdf",
                mime="application/pdf"
            )
            st.markdown('<div class="eng-success">✅ Laporan PDF berhasil dibuat!</div>',
                        unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════════════════
    # FOOTER
    # ═══════════════════════════════════════════════════════════════════════════
    st.markdown('<hr class="eng-divider">', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center; color:#8492ab; font-size:0.8rem; padding-bottom:2rem;">
      EngsetPro v2.0 &nbsp;·&nbsp; Kalkulator Rekayasa Trafik Engset &nbsp;·&nbsp;
      Metode: Log-space Arithmetic (numerically stable)
    </div>
    """, unsafe_allow_html=True)
