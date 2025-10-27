import tkinter as tk
from tkinter import messagebox
import json
import os

#BACA FILE RULES
rules_path = os.path.join(os.path.dirname(__file__), "..", "rules.json")
with open(rules_path) as f:
    rules = json.load(f)

#DAFTAR GEJALA (27)
gejala_list = {
    "G001": "Ayam ngorok / bersin dan nafas berbunyi",
    "G002": "Jengger, pial, atau kulit perut berwarna biru keunguan",
    "G003": "Ayam lesu dan tidak mau makan",
    "G004": "Kematian mendadak dalam jumlah besar",
    "G005": "Ayam sulit berdiri",
    "G006": "Sayap terkulai",
    "G007": "Mata berair atau keluar lendir",
    "G008": "Ayam batuk dan bersin",
    "G009": "Ayam lumpuh mendadak",
    "G010": "Ayam mengalami demam tinggi",
    "G011": "Diare berwarna kehijauan",
    "G012": "Bulu kusam dan berdiri",
    "G013": "Ayam tampak lemah dan kurang aktif",
    "G014": "Ayam gemetar",
    "G015": "Kematian meningkat pada usia muda",
    "G016": "Bulu mudah rontok",
    "G017": "Ayam susah berdiri atau berjalan",
    "G018": "Penurunan berat badan drastis",
    "G019": "Penurunan nafsu makan",
    "G020": "Penurunan produksi telur",
    "G021": "Ayam sering berkerumun di tempat hangat",
    "G022": "Sayap menggantung",
    "G023": "Bengkak di bagian muka atau kepala",
    "G024": "Keluar lendir dari hidung",
    "G025": "Ayam bersin terus menerus",
    "G026": "Sulit bernapas disertai suara",
    "G027": "Lesu dan nafsu makan menurun"
}

#FUNGSI DIAGNOSA
def diagnosa():
    gejala_dipilih = [kode for kode, var in vars_dict.items() if var.get() == 1]

    if not gejala_dipilih:
        messagebox.showwarning("Peringatan", "Pilih minimal satu gejala!")
        return

    hasil = []
    for rule in rules:
        cocok = len(set(rule["if"]) & set(gejala_dipilih))
        if cocok > 0:
            cf = rule["cf"] * (cocok / len(rule["if"]))
            hasil.append((cf, rule["penyakit"], rule["solusi"]))

    if not hasil:
        messagebox.showinfo("Hasil Diagnosa", "Tidak ada penyakit yang cocok.")
        return

    hasil.sort(reverse=True)
    cf, penyakit, solusi = hasil[0]

    messagebox.showinfo(
        "Hasil Diagnosa",
        f"Penyakit: {penyakit}\nTingkat Keyakinan: {cf*100:.2f}%\n\nSolusi:\n{solusi}"
    )

#UI TKINTER
root = tk.Tk()
root.title("Sistem Pakar Penyakit Ayam")
root.geometry("900x700")
root.configure(bg="white")

tk.Label(
    root, 
    text="Pilih Gejala Ayam yang Terlihat:", 
    font=("Arial", 13, "bold"),
    bg="white"
).pack(pady=10)

#CANVAS + SCROLLBAR
canvas = tk.Canvas(root, bg="white")
scroll_y = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scroll_x = tk.Scrollbar(root, orient="horizontal", command=canvas.xview)
frame = tk.Frame(canvas, bg="white")

frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=frame, anchor="nw")
canvas.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

vars_dict = {}
row = 0
col = 0

for i, (kode, nama) in enumerate(gejala_list.items()):
    var = tk.IntVar()
    cb = tk.Checkbutton(
        frame, 
        text=f"{kode}\n{nama}",
        variable=var,
        bg="white",
        wraplength=250,
        justify="left",
        anchor="w"
    )
    cb.grid(row=row, column=col, sticky="w", padx=10, pady=5)
    vars_dict[kode] = var

    col += 1
    if col >= 3:  
        col = 0
        row += 1

canvas.pack(side="top", fill="both", expand=True)
scroll_y.pack(side="right", fill="y")
scroll_x.pack(side="bottom", fill="x")

tk.Button(
    root,
    text="Diagnosa Sekarang",
    command=diagnosa,
    bg="#4CAF50",
    fg="white",
    font=("Arial", 12, "bold"),
    width=20,
    height=2
).pack(pady=20)

root.mainloop()
