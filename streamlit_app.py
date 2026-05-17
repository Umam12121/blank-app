import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
from math import log, exp
from datetime import datetime
import io

# ── ReportLab (PDF) ──────────────────────────────────────────────────────────
try:
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer,
        Table, TableStyle, HRFlowable
    )
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import cm
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    from reportlab.platypus import Image as RLImage
    PDF_OK = True
except ImportError:
    PDF_OK = False

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="EngsetPro — Kalkulator Engset",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════════════════════════
# GLOBAL CSS
# ═══════════════════════════════════════════════════════════════════════════════
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
