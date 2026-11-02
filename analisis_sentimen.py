import pandas as pd
from transformers import pipeline
from collections import Counter

# 1. Nama model IndoBERT
MODEL = "mdhugol/indonesia-bert-sentiment-classification"

# 2. Membaca data
df = pd.read_csv(
    "data_bersih.csv",
    sep=None,
    engine="python",
    encoding="utf-8-sig"
)

# 3. Memastikan kolom tersedia
if "teks_bersih" not in df.columns:
    raise ValueError("Kolom teks_bersih tidak ditemukan!")

# 4. Mengambil teks bersih
teks = df["teks_bersih"].fillna("").astype(str).tolist()

# 5. Memuat model
print("Memuat model IndoBERT...")
sentiment_model = pipeline(
    "sentiment-analysis",
    model=MODEL,
    device=-1
)

# 6. Pemetaan label model
label_index = {
    "LABEL_0": "positif",
    "LABEL_1": "netral",
    "LABEL_2": "negatif"
}

# 7. Prediksi sentimen
hasil = []
confidence = []

batch_size = 16

for i in range(0, len(teks), batch_size):
    batch = teks[i:i + batch_size]

    # Teks kosong tidak diprediksi
    valid_text = [
        t if t.strip() else " "
        for t in batch
    ]

    prediksi = sentiment_model(
        valid_text,
        truncation=True,
        batch_size=batch_size
    )

    for text, pred in zip(batch, prediksi):
        if not text.strip():
            hasil.append("tidak ada teks")
            confidence.append(0.0)
        else:
            hasil.append(label_index[pred["label"]])
            confidence.append(pred["score"])

    print(
        f"Diproses: {min(i + batch_size, len(teks))}"
        f" dari {len(teks)}"
    )

# 8. Menambahkan hasil ke data
df["sentimen"] = hasil
df["confidence"] = confidence

# 9. Menyimpan hasil
df.to_csv(
    "data_sentimen.csv",
    index=False,
    sep=";",
    encoding="utf-8-sig"
)

# 10. Menampilkan distribusi sentimen
jumlah = Counter(
    s for s in hasil
    if s in ["positif", "netral", "negatif"]
)

print("\nHASIL ANALISIS SENTIMEN")
print("=======================")
print("Positif :", jumlah["positif"])
print("Netral  :", jumlah["netral"])
print("Negatif :", jumlah["negatif"])

print("\nFile berhasil disimpan: data_sentimen.csv")
