import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
from datetime import datetime

FAIL = "kehadiran.csv"


# =========================
# CIPTA FAIL CSV
# =========================

def cipta_fail():
    if not os.path.exists(FAIL):
        with open(FAIL, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Tarikh", "Nama", "Status"])


# =========================
# SIMPAN KEHADIRAN
# =========================

def simpan_kehadiran():
    nama = entry_nama.get().strip()
    status = combo_status.get()

    if nama == "":
        messagebox.showwarning(
            "Amaran",
            "Sila masukkan nama pelajar."
        )
        return

    if status == "":
        messagebox.showwarning(
            "Amaran",
            "Sila pilih status kehadiran."
        )
        return

    tarikh = datetime.now().strftime("%d/%m/%Y")

    with open(FAIL, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([tarikh, nama, status])

    messagebox.showinfo(
        "Berjaya",
        "Rekod kehadiran berjaya disimpan!"
    )

    entry_nama.delete(0, tk.END)
    combo_status.set("")

    papar_rekod()


# =========================
# PAPAR REKOD
# =========================

def papar_rekod():
    for item in jadual.get_children():
        jadual.delete(item)

    if not os.path.exists(FAIL):
        return

    with open(FAIL, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            jadual.insert(
                "",
                tk.END,
                values=(
                    row["Tarikh"],
                    row["Nama"],
                    row["Status"]
                )
            )


# =========================
# SEMAK KEHADIRAN
# =========================

def semak_kehadiran():
    nama_cari = entry_cari.get().strip().lower()

    if nama_cari == "":
        messagebox.showwarning(
            "Amaran",
            "Sila masukkan nama pelajar."
        )
        return

    hadir = 0
    tidak_hadir = 0

    with open(FAIL, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            nama_dalam_fail = row["Nama"].strip().lower()

            if nama_dalam_fail == nama_cari:
                if row["Status"] == "Hadir":
                    hadir += 1

                elif row["Status"] == "Tidak Hadir":
                    tidak_hadir += 1

    jumlah = hadir + tidak_hadir

    if jumlah == 0:
        messagebox.showinfo(
            "Keputusan",
            "Rekod pelajar tidak dijumpai."
        )
        return

    peratus = (hadir / jumlah) * 100

    messagebox.showinfo(
        "Rekod Kehadiran",
        "Nama: " + nama_cari.title() +
        "\n\nJumlah Rekod: " + str(jumlah) +
        "\nHadir: " + str(hadir) +
        "\nTidak Hadir: " + str(tidak_hadir) +
        "\nPeratus Kehadiran: " +
        f"{peratus:.2f}%"
    )


# =========================
# PADAM SEMUA REKOD
# =========================

def padam_semua():
    jawapan = messagebox.askyesno(
        "Padam Rekod",
        "Adakah anda pasti mahu memadam semua rekod?"
    )

    if jawapan:
        with open(FAIL, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Tarikh", "Nama", "Status"])

        papar_rekod()

        messagebox.showinfo(
            "Berjaya",
            "Semua rekod telah dipadam."
        )


# =========================
# KELUAR
# =========================

def keluar():
    jawapan = messagebox.askyesno(
        "Keluar",
        "Adakah anda pasti mahu keluar?"
    )

    if jawapan:
        root.destroy()


# =========================
# PROGRAM UTAMA
# =========================

cipta_fail()

root = tk.Tk()

root.title("Sistem Kehadiran Pelajar")
root.geometry("900x650")
root.configure(bg="#EAF2F8")


# =========================
# TAJUK
# =========================

tajuk = tk.Label(
    root,
    text="SISTEM KEHADIRAN PELAJAR",
    font=("Arial", 24, "bold"),
    bg="#EAF2F8",
    fg="#154360"
)

tajuk.pack(pady=20)


# =========================
# FRAME INPUT
# =========================

frame_input = tk.Frame(
    root,
    bg="white",
    padx=20,
    pady=20
)

frame_input.pack(
    padx=30,
    fill="x"
)


# Nama

tk.Label(
    frame_input,
    text="Nama Pelajar:",
    font=("Arial", 12),
    bg="white"
).grid(
    row=0,
    column=0,
    padx=10,
    pady=10
)

entry_nama = tk.Entry(
    frame_input,
    font=("Arial", 12),
    width=35
)

entry_nama.grid(
    row=0,
    column=1,
    padx=10,
    pady=10
)


# Status

tk.Label(
    frame_input,
    text="Status:",
    font=("Arial", 12),
    bg="white"
).grid(
    row=1,
    column=0,
    padx=10,
    pady=10
)

combo_status = ttk.Combobox(
    frame_input,
    values=[
        "Hadir",
        "Tidak Hadir"
    ],
    state="readonly",
    font=("Arial", 12),
    width=32
)

combo_status.grid(
    row=1,
    column=1,
    padx=10,
    pady=10
)


# Butang simpan

butang_simpan = tk.Button(
    frame_input,
    text="SIMPAN KEHADIRAN",
    command=simpan_kehadiran,
    bg="#28B463",
    fg="white",
    font=("Arial", 11, "bold"),
    padx=20,
    pady=8
)

butang_simpan.grid(
    row=2,
    column=0,
    columnspan=2,
    pady=15
)


# =========================
# CARIAN
# =========================

frame_cari = tk.Frame(
    root,
    bg="#EAF2F8"
)

frame_cari.pack(pady=15)


tk.Label(
    frame_cari,
    text="Semak Nama:",
    font=("Arial", 12),
    bg="#EAF2F8"
).pack(
    side="left",
    padx=5
)


entry_cari = tk.Entry(
    frame_cari,
    font=("Arial", 12),
    width=25
)

entry_cari.pack(
    side="left",
    padx=5
)


butang_semak = tk.Button(
    frame_cari,
    text="SEMAK",
    command=semak_kehadiran,
    bg="#3498DB",
    fg="white",
    font=("Arial", 11, "bold"),
    padx=15
)

butang_semak.pack(
    side="left",
    padx=5
)


# =========================
# JADUAL
# =========================

frame_jadual = tk.Frame(root)

frame_jadual.pack(
    padx=30,
    pady=10,
    fill="both",
    expand=True
)


scrollbar = ttk.Scrollbar(
    frame_jadual,
    orient="vertical"
)

scrollbar.pack(
    side="right",
    fill="y"
)


jadual = ttk.Treeview(
    frame_jadual,
    columns=(
        "Tarikh",
        "Nama",
        "Status"
    ),
    show="headings",
    yscrollcommand=scrollbar.set
)


jadual.heading(
    "Tarikh",
    text="Tarikh"
)

jadual.heading(
    "Nama",
    text="Nama Pelajar"
)

jadual.heading(
    "Status",
    text="Status"
)


jadual.column(
    "Tarikh",
    width=150,
    anchor="center"
)

jadual.column(
    "Nama",
    width=400
)

jadual.column(
    "Status",
    width=200,
    anchor="center"
)


jadual.pack(
    fill="both",
    expand=True
)


scrollbar.config(
    command=jadual.yview
)


# =========================
# BUTANG BAWAH
# =========================

frame_bawah = tk.Frame(
    root,
    bg="#EAF2F8"
)

frame_bawah.pack(
    pady=15
)


butang_padam = tk.Button(
    frame_bawah,
    text="PADAM SEMUA",
    command=padam_semua,
    bg="#F39C12",
    fg="white",
    font=("Arial", 11, "bold"),
    padx=20,
    pady=8
)

butang_padam.pack(
    side="left",
    padx=10
)


butang_keluar = tk.Button(
    frame_bawah,
    text="KELUAR",
    command=keluar,
    bg="#E74C3C",
    fg="white",
    font=("Arial", 11, "bold"),
    padx=25,
    pady=8
)

butang_keluar.pack(
    side="left",
    padx=10
)


# =========================
# PAPAR REKOD SEMASA MULA
# =========================

papar_rekod()


# =========================
# JALANKAN PROGRAM
# =========================

root.mainloop()