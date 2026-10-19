import csv
import glob
import html
import re

# baca semua file hasil scraping, buang tweet dengan id yang sama
semua = []
sudah_id = set()

for file in glob.glob("tweets-data/scraping_kedua.csv"):
    with open(file, encoding="utf-8") as f:
        for baris in csv.DictReader(f):
            if baris["id_str"] in sudah_id:
                continue
            sudah_id.add(baris["id_str"])
            semua.append(baris)

print("Tweet mentah (tanpa id ganda):", len(semua))

# rapikan teks
hasil = []
sudah_teks = set()

for baris in semua:
    teks = html.unescape(baris["full_text"])
    teks = re.sub(r"https?://\S+", "", teks)
    teks = re.sub(r"@\w+", "", teks)
    teks = teks.replace("#", "")
    teks = teks.lower()
    teks = re.sub(r"[^a-z0-9\s]", " ", teks)
    teks = " ".join(teks.split())

    if len(teks) < 5:
        continue
    if teks in sudah_teks:
        continue
    sudah_teks.add(teks)
    hasil.append([baris["created_at"][:10], baris["favorite_count"], teks])

print("Setelah dirapikan:", len(hasil))

# simpan (username tidak ikut)
with open("data_bersih.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f, delimiter=";", quoting=csv.QUOTE_ALL)
    w.writerow(["tanggal", "like", "tweet"])
    w.writerows(hasil)

tanggal = [h[0] for h in hasil]
print("Tanggal terlama:", min(tanggal))
print("Tanggal terbaru:", max(tanggal))