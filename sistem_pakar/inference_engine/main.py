import json

# Baca file rules.json
import os, json

base_path = os.path.dirname(__file__)
rules_path = os.path.join(base_path, "..", "rules.json")

with open(rules_path) as f:
    rules = json.load(f)


# Daftar gejala (kode + keterangan singkat)
gejala_dict = {
    "G001": "Ayam ngorok / bersin dan nafas berbunyi",
    "G002": "Jengger, pial, atau kulit perut berwarna biru keunguan",
    "G003": "Keluar cairan dari mata dan hidung",
    "G004": "Pembengkakan di daerah muka dan kepala",
    "G005": "Pendarahan di bawah kulit",
    "G006": "Pendarahan titik pada dada, kaki, atau telapak kaki",
    "G007": "Ayam mengalami diare",
    "G008": "Mati mendadak",
    "G009": "Tingkat kematian tinggi",
    "G010": "Ayam lesu",
    "G011": "Nafsu makan menurun",
    "G012": "Ayam mengantuk",
    "G013": "Leher goyang (tortikolis)",
    "G014": "Feses hijau",
    "G015": "Jengger kebiru-biruan",
    "G016": "Bintik merah di otot",
    "G017": "Bulu berdiri",
    "G018": "Kepala menunduk",
    "G019": "Diare encer hijau keputihan",
    "G020": "Daerah kloaka kotor",
    "G021": "Tremor (gemetar)",
    "G022": "Menyerang ayam umur di bawah 4 bulan",
    "G023": "Bengkak di daerah muka dan sinus",
    "G024": "Lendir kental di rongga hidung",
    "G025": "Kelopak mata lengket",
    "G026": "Radang di trakea atau bronkus",
    "G027": "Cairan hidung berbau"
}

# Tampilkan daftar gejala
print("\n=== SISTEM PAKAR PENYAKIT AYAM ===")
print("Masukkan gejala yang terlihat (pisahkan dengan koma):\n")
for kode, desc in gejala_dict.items():
    print(f"{kode}: {desc}")

# Input gejala dari user
input_gejala = input("\nMasukkan kode gejala yang dialami ayam (contoh: G001,G002,G004): ")
fakta = [g.strip().upper() for g in input_gejala.split(",")]

# Proses inferensi (Forward Chaining + CF)
hasil = {}
for rule in rules:
    if all(gejala in fakta for gejala in rule["if"]):
        penyakit = rule["penyakit"]
        cf_rule = rule["cf"]
        if penyakit not in hasil:
            hasil[penyakit] = cf_rule
        else:
            # Gabungkan CF jika ada beberapa aturan menuju penyakit sama
            hasil[penyakit] = hasil[penyakit] + cf_rule * (1 - hasil[penyakit])

# Tampilkan hasil diagnosa
if hasil:
    print("\n=== HASIL DIAGNOSA ===")
    for penyakit, cf in hasil.items():
        solusi = next((r["solusi"] for r in rules if r["penyakit"] == penyakit), "")
        print(f"\nPenyakit: {penyakit}")
        print(f"Tingkat Keyakinan: {cf * 100:.2f}%")
        print(f"Solusi: {solusi}")
else:
    print("\nTidak ditemukan penyakit yang cocok dengan gejala yang dimasukkan.")
