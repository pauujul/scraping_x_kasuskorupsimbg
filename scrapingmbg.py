import csv
from itertools import islice
from youtube_comment_downloader import YoutubeCommentDownloader

URL = "https://youtu.be/wde5Ialu0D0?si=55wsqmqBDLNBNEPg"
JUMLAH = 500
KATA_KUNCI = ["korupsi", "anggaran", "dana", "kontraktor", "vendor", "proyek", "usut", "tangkap", "hukum", "umkm"]


def ambil_komentar(url, jumlah):
    """Ambil komentar dari video YouTube (username tidak disimpan)."""
    downloader = YoutubeCommentDownloader()
    hasil = []
    for c in islice(downloader.get_comments_from_url(url), jumlah):
        hasil.append({
            "waktu": c["time"],
            "like": c["votes"],
            "komentar": " ".join(c["text"].split()),
        })
    return hasil


def bersihkan(data):
    """Hapus komentar kosong dan duplikat."""
    sudah_ada = set()
    bersih = []
    for d in data:
        teks = d["komentar"].lower()
        if teks and teks not in sudah_ada:
            sudah_ada.add(teks)
            bersih.append(d)
    return bersih


def hitung_kata_kunci(data):
    """Hitung berapa komentar yang menyebut tiap kata kunci."""
    hitungan = {k: 0 for k in KATA_KUNCI}
    for d in data:
        teks = d["komentar"].lower()
        for k in KATA_KUNCI:
            if k in teks:
                hitungan[k] += 1
    return hitungan


def simpan_csv(data, nama_file):
    with open(nama_file, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=["waktu", "like", "komentar"], delimiter=";", quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(data)


if __name__ == "__main__":
    mentah = ambil_komentar(URL, JUMLAH)
    bersih = bersihkan(mentah)
    simpan_csv(bersih, "komentar_mbg.csv")

    print("Komentar diambil :", len(mentah))
    print("Setelah dibersihkan:", len(bersih))
    print("Kata kunci:")
    for kata, jumlah in hitung_kata_kunci(bersih).items():
        print(" -", kata, ":", jumlah)