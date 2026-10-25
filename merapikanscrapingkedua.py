import csv
import glob
import html
import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# kamus singkatan dan kata gaul, tambah sendiri sesuai data
slang = {
    "gak": "tidak", "ga": "tidak", "nggak": "tidak", "ngga": "tidak", "tdk": "tidak",
    "yg": "yang", "dgn": "dengan", "dg": "dengan", "utk": "untuk",
    "krn": "karena", "karna": "karena", "udah": "sudah", "udh": "sudah", "sdh": "sudah",
    "aja": "saja", "aj": "saja", "bgt": "sekali", "banget": "sekali",
    "tp": "tapi", "jg": "juga", "sm": "sama", "org": "orang",
    "dr": "dari", "pd": "pada", "klo": "kalau", "kalo": "kalau", "emg": "memang",
}

stemmer = StemmerFactory().create_stemmer()
cache = {}


def stem_kata(kata):
    if len(kata) > 15:
        return kata
    if kata not in cache:
        cache[kata] = stemmer.stem(kata)
    return cache[kata]


# 1. baca semua CSV mentah, buang tweet dengan id sama
data = []
sudah_id = set()
for file in glob.glob("tweets-data/scraping_kedua.csv"):
    with open(file, encoding="utf-8") as f:
        for baris in csv.DictReader(f):
            if baris["id_str"] not in sudah_id:
                sudah_id.add(baris["id_str"])
                data.append(baris)
print("1. Data mentah (id unik):", len(data))

# 2. cleaning
hasil = []
sudah_teks = set()
terlalu_pendek = 0
duplikat = 0
nomor = 0

for baris in data:
    nomor = nomor + 1
    if nomor % 100 == 0:
        print("Diproses:", nomor, "dari", len(data))

    teks = html.unescape(baris["full_text"]).lower()          # huruf kecil
    teks = re.sub(r"http\S+|www\.\S+", " ", teks)             # hapus URL
    teks = re.sub(r"\S+@\S+\.\S+", " ", teks)                 # hapus email
    teks = re.sub(r"@\w+", " ", teks)                         # hapus mention
    teks = re.sub(r"[^a-z\s]", " ", teks)                     # hapus emoji, angka, simbol
    teks = re.sub(r"(.)\1{2,}", r"\1\1", teks)                # huruf berulang: haaaah jadi haah
    kata = [slang.get(k, k) for k in teks.split()]            # tokenisasi dan kamus kata gaul

    if len(kata) < 3:                                         # buang tweet terlalu pendek
        terlalu_pendek = terlalu_pendek + 1
        continue

    teks_bersih = " ".join(kata)
    if teks_bersih in sudah_teks:                             # buang duplikat
        duplikat = duplikat + 1
        continue
    sudah_teks.add(teks_bersih)

    teks_stem = " ".join(stem_kata(k) for k in kata)          # stemming
    hasil.append([baris["created_at"][:10], teks_bersih, teks_stem])

print("2. Dibuang karena terlalu pendek:", terlalu_pendek)
print("3. Dibuang karena duplikat:", duplikat)
print("4. Data bersih:", len(hasil))

# 3. simpan (tanpa username)
with open("data_bersih.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["tanggal", "teks_bersih", "teks_stem"])
    w.writerows(hasil)

print("Tersimpan: data_bersih.csv")