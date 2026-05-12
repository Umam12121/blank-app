# =========================================================
# ENGSETPRO SIMULATOR
# FINAL COMPLETE VERSION
# =========================================================
# INSTALL:
# pip install customtkinter matplotlib reportlab
#
# RUN:
# python Engset.py
# =========================================================

import customtkinter as ctk
from tkinter import ttk, messagebox
from math import factorial
from datetime import datetime

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

# =========================================================
# THEME
# =========================================================

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

PRIMARY = "#2563EB"
PRIMARY_DARK = "#1D4ED8"

BG = "#EEF4FF"
CARD = "#FFFFFF"

TEXT = "#0F172A"

SUCCESS = "#16A34A"
DANGER = "#DC2626"

# =========================================================
# KOMBINASI
# =========================================================

def nCr(n, r):

    if r > n:
        return 0

    return factorial(n) // (
        factorial(r) * factorial(n - r)
    )

# =========================================================
# ENGSET FORMULA
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
