import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

print("==========================================")
print("     PROGRAM FUZZY NILAI MATA KULIAH DSS")
print("==========================================")

jumlah_tugas = int(input("Jumlah tugas yang dikerjakan (0-10): "))

if jumlah_tugas < 0 or jumlah_tugas > 10:
    print("Jumlah tugas harus 0 sampai 10.")
    exit()

nilai_tugas = []

for i in range(jumlah_tugas):
    nilai = float(input(f"Nilai tugas ke-{i + 1}: "))

    if nilai < 0 or nilai > 100:
        print("Nilai tugas harus 0 sampai 100.")
        exit()

    nilai_tugas.append(nilai)

if jumlah_tugas > 0:
    rata_tugas = sum(nilai_tugas) / jumlah_tugas
else:
    rata_tugas = 0

if jumlah_tugas == 10:
    porsi_tugas = 50
elif jumlah_tugas == 9:
    porsi_tugas = 47.5
elif jumlah_tugas == 8:
    porsi_tugas = 45
elif jumlah_tugas == 7:
    porsi_tugas = 40
elif jumlah_tugas == 0:
    porsi_tugas = 0
else:
    porsi_tugas = (jumlah_tugas / 7) * 40

kontribusi_tugas = (rata_tugas / 100) * porsi_tugas

uts = float(input("Inputan UTS (0-100): "))
uas = float(input("Inputan UAS (0-100): "))

if uts < 0 or uts > 100:
    print("Nilai UTS harus 0 sampai 100.")
    exit()

if uas < 0 or uas > 100:
    print("Nilai UAS harus 0 sampai 100.")
    exit()

kontribusi_uts = (uts / 100) * 20
kontribusi_uas = (uas / 100) * 30

nilai_akhir = kontribusi_tugas + kontribusi_uts + kontribusi_uas

nilai = ctrl.Antecedent(
    np.arange(0, 101, 1),
    "nilai"
)

nilai["cukup"] = fuzz.trimf(
    nilai.universe,
    [0, 0, 60]
)

nilai["sedang"] = fuzz.trimf(
    nilai.universe,
    [40, 65, 90]
)

nilai["tinggi"] = fuzz.trimf(
    nilai.universe,
    [70, 100, 100]
)

hasil = ctrl.Consequent(
    np.arange(0, 101, 1),
    "hasil"
)

hasil["cukup"] = fuzz.trimf(
    hasil.universe,
    [0, 0, 60]
)

hasil["sedang"] = fuzz.trimf(
    hasil.universe,
    [40, 65, 90]
)

hasil["tinggi"] = fuzz.trimf(
    hasil.universe,
    [70, 100, 100]
)

rule_cukup = ctrl.Rule(
    nilai["cukup"],
    hasil["cukup"]
)

rule_sedang = ctrl.Rule(
    nilai["sedang"],
    hasil["sedang"]
)

rule_tinggi = ctrl.Rule(
    nilai["tinggi"],
    hasil["tinggi"]
)

sistem = ctrl.ControlSystem([
    rule_cukup,
    rule_sedang,
    rule_tinggi
])

simulasi = ctrl.ControlSystemSimulation(sistem)

simulasi.input["nilai"] = nilai_akhir
simulasi.compute()

hasil_fuzzy = simulasi.output["hasil"]

derajat_cukup = fuzz.interp_membership(
    nilai.universe,
    nilai["cukup"].mf,
    nilai_akhir
)

derajat_sedang = fuzz.interp_membership(
    nilai.universe,
    nilai["sedang"].mf,
    nilai_akhir
)

derajat_tinggi = fuzz.interp_membership(
    nilai.universe,
    nilai["tinggi"].mf,
    nilai_akhir
)

if hasil_fuzzy >= 70:
    kategori = "A - Tinggi"
elif hasil_fuzzy >= 40:
    kategori = "B - Sedang"
else:
    kategori = "C - Cukup"

print()
print("==========================================")
print("          HASIL PERHITUNGAN")
print("==========================================")

print(f"Jumlah Tugas          : {jumlah_tugas}")
print(f"Nilai Tugas           : {nilai_tugas}")
print(f"Rata2 Nilai Tugas     : {rata_tugas:.2f}")
print(f"Porsi Tugas           : {porsi_tugas:.2f}%")
print(f"Kontribusi Tugas      : {kontribusi_tugas:.2f}")

print("------------------------------------------")

print(f"Nilai UTS             : {uts:.2f}")
print(f"Kontribusi UTS        : {kontribusi_uts:.2f}")
print(f"Nilai UAS             : {uas:.2f}")
print(f"Kontribusi UAS        : {kontribusi_uas:.2f}")

print("------------------------------------------")

print(f"Nilai Akhir           : {nilai_akhir:.2f}")

print()
print("==========================================")
print("             PROSES FUZZY")
print("==========================================")

print()
print("1. FUZZIFIKASI")
print(f"Nilai input fuzzy     : {nilai_akhir:.2f}")

print()
print("Derajat Keanggotaan:")
print(f"Cukup                 : {derajat_cukup:.4f}")
print(f"Sedang                : {derajat_sedang:.4f}")
print(f"Tinggi                : {derajat_tinggi:.4f}")

print()
print("2. RULE FUZZY")
print("IF nilai CUKUP  THEN hasil CUKUP")
print("IF nilai SEDANG THEN hasil SEDANG")
print("IF nilai TINGGI THEN hasil TINGGI")

print()
print("3. DEFUZZIFIKASI")
print(f"Hasil Fuzzy           : {hasil_fuzzy:.2f}")

print()
print("4. KATEGORI")
print(f"Kategori              : {kategori}")

print("==========================================")