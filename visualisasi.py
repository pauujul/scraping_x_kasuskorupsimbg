import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud

data = pd.read_csv("data_sentimen.csv", sep=None, engine="python", encoding="utf-8-sig")
data["sentimen"] = data["sentimen"].str.lower()
data["tanggal"] = pd.to_datetime(data["tanggal"])

# kalau teks_stem belum ada di data_sentimen, ambil dari data_bersih (urutan baris sama)
if "teks_stem" not in data.columns:
    bersih = pd.read_csv("data_bersih.csv", sep=None, engine="python", encoding="utf-8-sig")
    data["teks_stem"] = bersih["teks_stem"].values

# 1. distribusi sentimen
urutan = ["positif", "netral", "negatif"]
jumlah = data["sentimen"].value_counts().reindex(urutan, fill_value=0)
persen = jumlah / jumlah.sum() * 100

plt.figure(figsize=(6, 4))
batang = plt.bar(urutan, jumlah, color=["#2e7d32", "#9e9e9e", "#c62828"])
for b, j, p in zip(batang, jumlah, persen):
    plt.text(b.get_x() + b.get_width() / 2, b.get_height(), f"{j} ({p:.1f}%)", ha="center", va="bottom")
plt.title("Distribusi Sentimen Tweet MBG")
plt.ylabel("Jumlah tweet")
plt.ylim(0, jumlah.max() * 1.15)
plt.tight_layout()
plt.savefig("grafik_sentimen.png", dpi=200)
plt.close()
print(jumlah)

# 2. jumlah tweet per bulan
per_bulan = data.groupby(data["tanggal"].dt.to_period("M")).size()

plt.figure(figsize=(7, 4))
batang = plt.bar(per_bulan.index.astype(str), per_bulan.values)
for b, j in zip(batang, per_bulan.values):
    plt.text(b.get_x() + b.get_width() / 2, b.get_height(), str(j), ha="center", va="bottom")
plt.title("Jumlah Tweet MBG per Bulan")
plt.xlabel("Bulan")
plt.ylabel("Jumlah tweet")
plt.tight_layout()
plt.savefig("grafik_per_bulan.png", dpi=200)
plt.close()
print(per_bulan)

# 3. word cloud
stop = set("""yang dan di ke dari ini itu untuk dengan tidak ada juga karena saja jadi sama atau kalau
sudah bisa mau lebih pada dalam saya kita mereka kok lagi tapi si para kan nih sih sekali akan oleh
bagi seperti buat bukan jangan banyak apa siapa kenapa ya aja nya dong pun lah kah tuh udah mbg korupsi""".split())


def kata_bersih(daftar_teks):
    return [k for t in daftar_teks for k in str(t).split() if k not in stop and len(k) > 2]


def buat_wordcloud(daftar_teks, nama_file, judul):
    kata = kata_bersih(daftar_teks)
    wc = WordCloud(width=1200, height=600, background_color="white", collocations=False).generate(" ".join(kata))
    plt.figure(figsize=(8, 4))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.title(judul)
    plt.tight_layout()
    plt.savefig(nama_file, dpi=200)
    plt.close()


buat_wordcloud(data["teks_stem"], "wordcloud.png", "Word Cloud Tweet MBG")
for s in urutan:
    buat_wordcloud(data[data["sentimen"] == s]["teks_stem"], f"wordcloud_{s}.png", f"Word Cloud Sentimen {s.capitalize()}")

print("15 kata terbanyak:", Counter(kata_bersih(data["teks_stem"])).most_common(15))
print("Selesai")