import csv

# ganti dengan nama file CSV hasil tweet-harvest
NAMA_FILE = "tweets-data/kasus_korupsi_MBG_12-10-2026_19-34-10.csv"

kata_kunci = ["korupsi", "anggaran", "dana", "proyek", "hukum", "umkm"]

# baca file
tweet = []
with open(NAMA_FILE, encoding="utf-8") as f:
    baca = csv.DictReader(f)
    for baris in baca:
        tweet.append(baris["full_text"].lower())

print("Jumlah tweet:", len(tweet))

# hapus duplikat
tweet = list(set(tweet))
print("Setelah hapus duplikat:", len(tweet))

# hitung kata kunci
for kata in kata_kunci:
    jumlah = 0
    for t in tweet:
        if kata in t:
            jumlah = jumlah + 1
    print(kata, ":", jumlah)