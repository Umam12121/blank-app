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
    from reportlab.lib.enums import TA_CENTER
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
# GLOBAL CSS — Inspired by modern telecom UI (blue-teal gradient, clean cards)
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

/* ── Proper fraction layout ── */
.formula-fraction-wrap {
  display: flex; flex-direction: column; align-items: flex-start; gap: 1rem;
}
.formula-eq-label {
  font-size: 1rem; font-weight: 700; color: #0d2060;
  font-family: 'JetBrains Mono', monospace;
}
.formula-fraction {
  display: flex; flex-direction: column; align-items: center;
  margin-left: 2rem;
}
.formula-num {
  padding: 6px 16px; font-size: 1rem; font-weight: 600;
  color: #0d2060; text-align: center;
  font-family: 'JetBrains Mono', monospace;
}
.formula-divider {
  width: 100%; height: 2px;
  background: linear-gradient(90deg, var(--blue-primary), var(--teal));
  border-radius: 2px; margin: 2px 0;
}
.formula-den {
  padding: 6px 16px; font-size: 1rem; font-weight: 600;
  color: #0d2060; text-align: center;
  display: flex; align-items: center; gap: 8px;
  font-family: 'JetBrains Mono', monospace;
}
.formula-sigma {
  display: inline-flex; flex-direction: column; align-items: center;
  font-size: 0.75rem; line-height: 1.15; margin-right: 4px;
  color: var(--blue-primary); font-weight: 700;
}
.formula-rho-def {
  display: flex; align-items: center; gap: 8px;
  font-size: 0.9rem; color: #3a5098; margin-left: 2rem;
  font-family: 'JetBrains Mono', monospace;
}
.formula-rho-frac {
  display: inline-flex; flex-direction: column; align-items: center;
  margin-left: 4px;
}
.formula-rho-num { font-size: 0.85rem; font-weight: 700; color: #0d2060; }
.formula-rho-bar {
  display: block; width: 100%; height: 1.5px;
  background: var(--blue-primary); margin: 2px 0;
}
.formula-rho-den { font-size: 0.85rem; font-weight: 700; color: #0d2060; }

.formula-legend { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-top: 1rem; }
.fl-item { font-size: 0.78rem; color: var(--slate); display: flex; align-items: baseline; gap: 8px; }
.fl-sym  { font-family: 'JetBrains Mono', monospace; font-weight: 700; color: var(--blue-primary); min-width: 22px; }

/* ═══════════ DASHBOARD TOP ROW (chips + GoS) ═══════════ */
.dash-top-row {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1.4fr;
  gap: 10px; margin-bottom: 1rem;
}
.chip-gos { text-align: center; }
@media (max-width: 768px) {
  .dash-top-row { grid-template-columns: 1fr 1fr !important; }
}

/* ═══════════ MOBILE RESPONSIVE ═══════════ */
#mobile-menu-btn {
  display: none;
  position: fixed; top: 10px; left: 10px; z-index: 99999;
  background: linear-gradient(135deg, #1a56ff, #0e3acc);
  color: white; border: none; border-radius: 10px;
  width: 42px; height: 42px;
  align-items: center; justify-content: center;
  font-size: 1.25rem; cursor: pointer;
  box-shadow: 0 4px 14px rgba(26,86,255,0.45);
}
@media (max-width: 768px) {
  #mobile-menu-btn { display: flex !important; }
  .main .block-container {
    padding-left: 0.75rem !important;
    padding-right: 0.75rem !important;
    padding-top: 3.5rem !important;
  }
  .chip-grid { grid-template-columns: 1fr 1fr !important; }
  .formula-legend { grid-template-columns: 1fr !important; }
}

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

# ── Mobile hamburger menu button ──────────────────────────────────────────────
st.markdown("""
<button id="mobile-menu-btn" title="Buka/Tutup Menu">&#9776;</button>
<script>
(function() {
  // Tunggu DOM siap lalu attach event ke tombol hamburger kita
  function attachBtn() {
    var myBtn = document.getElementById('mobile-menu-btn');
    if (!myBtn) { setTimeout(attachBtn, 300); return; }
    myBtn.addEventListener('click', function() {
      // Cari tombol collapse/expand sidebar bawaan Streamlit
      var selectors = [
        'button[data-testid="stSidebarNavToggleButton"]',
        'button[data-testid="collapsedControl"]',
        '[data-testid="stSidebar"] + div button',
        'section[data-testid="stSidebar"] ~ div button',
        '.st-emotion-cache-zq5wmm',
        'button[kind="header"]'
      ];
      var found = null;
      for (var i = 0; i < selectors.length; i++) {
        found = document.querySelector(selectors[i]);
        if (found) break;
      }
      if (found) {
        found.click();
      } else {
        // Fallback: toggle class pada sidebar langsung
        var sb = document.querySelector('[data-testid="stSidebar"]');
        if (sb) sb.style.transform = sb.style.transform ? '' : 'translateX(-100%)';
      }
    });
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', attachBtn);
  } else {
    attachBtn();
  }
})();
</script>
""", unsafe_allow_html=True)
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

    st.markdown('<div style="height:1px;background:rgba(255,255,255,0.12);margin:10px 0;border-radius:1px;"></div>', unsafe_allow_html=True)
    # ── PARAMETER ─────────────────────────────────────────────
    st.markdown('<div class="nav-group-label">Parameter Sistem</div>', unsafe_allow_html=True)

    S = st.slider("S  Jumlah Source", 2, 200, 20, 1)
    N = st.slider("N  Jumlah Kanal",  1, 100,  5, 1)
    A = st.slider("A  Traffic Offered (Erl)", 0.1, float(max(1, S-1)), min(8.0, float(S-2)), 0.1)

    st.markdown('<div style="height:1px;background:rgba(255,255,255,0.12);margin:10px 0;border-radius:1px;"></div>', unsafe_allow_html=True)
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

    pbar_w  = min(100, (P or 0) * 500)
    bar_col = GREEN if (P or 1) < 0.01 else AMBER if (P or 1) < 0.05 else RED

    # ── Hero card (full width) ────────────────────────────────────────────────
    st.markdown(f"""
    <div class="hero-card">
      <div class="hero-badge">📡 EngsetPro · Finite Source Model</div>
      <h1 style="font-size:1.65rem;font-weight:800;color:#fff;margin:0 0 0.3rem;
           line-height:1.15;">Dashboard Analisis Engset</h1>
      <p style="font-size:0.85rem;opacity:0.75;margin:0 0 1.4rem;">
        Probabilitas blocking real-time · Model Engset Finite Source</p>
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

    # ── Metric chips + GoS row (full width, responsive) ───────────────────────
    if P is not None:
        st.markdown(f"""
        <div class="dash-top-row">
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
          <div class="chip chip-gos">
            <div class="chip-icon">🏆</div>
            <span class="gos {gos_cls}" style="font-size:0.85rem;padding:4px 14px;margin:4px 0;">{gos_text}</span>
            <div class="progress-wrap" style="margin:6px 0 2px;">
              <div class="progress-fill" style="width:{pbar_w:.1f}%;background:{bar_col};"></div>
            </div>
            <div class="chip-lbl">Grade of Service · P={P:.4f}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Main content: Ringkasan kiri + Donut+Rekomendasi kanan ───────────────
    col_main, col_side = st.columns([2.2, 1], gap="large")

    with col_main:
        st.markdown('<p class="sec-title">📋 Ringkasan Sistem</p>', unsafe_allow_html=True)
        items = [
            ("📶", "plan-icon-blue",  "Probabilitas Blocking", f"{P*100:.3f}%" if P else "—",  f"Grade: {gos_text}"),
            ("🔄", "plan-icon-teal",  "Traffic Carried",       f"{carried:.4f} Erl",            f"dari {A:.1f} Erl ditawarkan"),
            ("📉", "plan-icon-amber", "Kanal Min GoS ≤ 1%",   f"N = {min_n_1}",               "untuk kualitas baik"),
            ("⚡", "plan-icon-red",   "Utilisasi Kanal",       f"{util_pct:.1f}%",             f"rata-rata per {N} kanal"),
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
        # Donut lebih kecil agar tidak terlalu besar
        fig_d = donut_chart(
            util_pct,
            f"{util_pct:.1f}%" if P else "—",
            "utilisasi kanal",
            color=BLUE,
        )
        st.pyplot(fig_d, use_container_width=True)
        plt.close(fig_d)

        # Rekomendasi kanal
        st.markdown(f"""
        <div class="card" style="padding:1rem 1.1rem;">
          <div style="font-size:0.82rem;font-weight:700;color:var(--navy);margin-bottom:10px;">
            🎯 Rekomendasi Kanal</div>
          <div style="font-size:0.82rem;color:var(--slate);line-height:2.2;">
            GoS ≤ 1%
            <strong style="color:var(--blue-primary);float:right;">N = {min_n_1}</strong><br>
            GoS ≤ 0.1%
            <strong style="color:var(--blue-primary);float:right;">N = {min_n_001}</strong>
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
      <span class="formula-tag">Rumus Engset — Finite Source (ITU-T)</span>
      <div class="formula-body">
        <div class="formula-fraction-wrap">
          <div class="formula-eq-label">P(S, N, A) =</div>
          <div class="formula-fraction">
            <div class="formula-num">C(S&minus;1, N) &middot; &rho;<sup>N</sup></div>
            <div class="formula-divider"></div>
            <div class="formula-den">
              <span class="formula-sigma">N<br>&Sigma;<br><small>i=0</small></span>
              C(S&minus;1, i) &middot; &rho;<sup>i</sup>
            </div>
          </div>
          <div class="formula-rho-def">
            di mana &nbsp;&nbsp;&rho; = <span class="formula-rho-frac">
              <span class="formula-rho-num">A</span>
              <span class="formula-rho-bar"></span>
              <span class="formula-rho-den">S &minus; A</span>
            </span>
          </div>
        </div>
      </div>
      <div class="formula-legend">
        <div class="fl-item"><span class="fl-sym">P</span> Probabilitas blocking</div>
        <div class="fl-item"><span class="fl-sym">S</span> Jumlah source / pengguna</div>
        <div class="fl-item"><span class="fl-sym">N</span> Jumlah server / kanal</div>
        <div class="fl-item"><span class="fl-sym">A</span> Traffic offered (Erlang)</div>
        <div class="fl-item"><span class="fl-sym">C(n,k)</span> Kombinasi binomial</div>
        <div class="fl-item"><span class="fl-sym">&rho;</span> Intensitas per sumber</div>
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
      <span class="formula-tag">Rumus Erlang — Metode 1: Call Rate</span>
      <div class="formula-body">
        <div class="formula-fraction-wrap">
          <div style="font-size:1.1rem;font-weight:700;color:#0d2060;margin-bottom:0.5rem;">
            A = &lambda; &times; h
          </div>
          <div style="font-size:0.82rem;color:#3a5098;line-height:2;">
            &lambda; &nbsp;= call rate (panggilan per jam per pengguna)<br>
            h &nbsp;&nbsp;= rata-rata durasi panggilan (dalam jam)
          </div>
        </div>
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
      <span class="formula-tag">Rumus BHT — Metode 2: Pengguna Aktif</span>
      <div class="formula-body">
        <div class="formula-fraction-wrap">
          <div style="font-size:1.1rem;font-weight:700;color:#0d2060;margin-bottom:0.5rem;">
            A = U &times; BHT
          </div>
          <div style="font-size:0.82rem;color:#3a5098;line-height:2;">
            U &nbsp;&nbsp;&nbsp;= jumlah pengguna aktif di jam sibuk<br>
            BHT = Busy Hour Traffic per pengguna (Erlang)
          </div>
        </div>
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
      <span class="formula-tag">Rumus Data Rate — Metode 3: Throughput</span>
      <div class="formula-body">
        <div class="formula-fraction-wrap">
          <div style="display:flex;align-items:center;gap:1rem;">
            <div style="font-size:1.1rem;font-weight:700;color:#0d2060;">A =</div>
            <div class="formula-fraction" style="margin-left:0;">
              <div class="formula-num">R<sub>total</sub> (Mbps)</div>
              <div class="formula-divider"></div>
              <div class="formula-den">R<sub>channel</sub> (Mbps)</div>
            </div>
          </div>
          <div style="font-size:0.82rem;color:#3a5098;line-height:2;margin-top:0.5rem;">
            R<sub>total</sub> &nbsp;&nbsp;&nbsp;= data rate total sistem<br>
            R<sub>channel</sub> = kapasitas per kanal
          </div>
        </div>
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
""", unsafe_allow_html=True)
