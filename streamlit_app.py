import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from math import factorial
from datetime import datetime
import io
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm

st.set_page_config(page_title='Kalkulator Engset', page_icon='\U0001f310', layout='wide')

st.markdown('''
<style>
body { background-color: #f1f5f9; }
.unpix-header {
    background: linear-gradient(135deg, #2563eb, #06b6d4);
    padding: 30px; border-radius: 25px; margin-bottom: 25px;
    box-shadow: 0px 6px 25px rgba(0,0,0,0.2);
}
.header-title { font-size: 38px; font-weight: bold; color: white; }
.header-subtitle { font-size: 15px; color: #e0f2fe; margin-top: 8px; }
.section-title {
    font-size: 28px; font-weight: bold; color: #2563eb;
    margin-top: 20px; margin-bottom: 15px;
}
.metric-grid { display: grid; grid-template-columns: repeat(2,1fr); gap: 20px; }
.metric-card {
    background: white; padding: 20px; border-radius: 20px;
    text-align: center; box-shadow: 0px 4px 20px rgba(0,0,0,0.1);
}
.metric-value { font-size: 28px; font-weight: bold; color: #2563eb; }
.metric-label { font-size: 15px; color: #334155; margin-top: 10px; }
.input-card {
    background: white; padding: 20px; border-radius: 20px;
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
