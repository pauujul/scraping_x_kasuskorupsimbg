# Scraping dan Cleaning Tweet Topik Kasus Korupsi MBG

Tugas Kelompok 6 Sosial Media Analisis, Bisnis Digital UNM

## Tujuan
Mengumpulkan tweet publik di X tentang kasus korupsi MBG, lalu membersihkannya agar siap dianalisis pada tahap berikutnya. Topik ini berkaitan dengan ekonomi dan bisnis digital karena menyangkut anggaran negara dan lain lain.

## Data
- Sumber: platform X
- Kata kunci: `Korupsi MBG`
- Rentang waktu: 19 Mei 2026 sampai 20 Oktober 2026
- Alat scraping: tweet-harvest
- Jumlah data mentah: [angka] tweet

## Langkah 1: scraping (tweet-harvest)
```
npx tweet-harvest@latest --from 19-05-2026 --to 20-10-2026 --tab "LATEST"
```
Isi `auth_token`, kata kunci `Korupsi MBG`, dan jumlah tweet saat diminta. Hasil tersimpan di folder `tweets-data` (tidak diupload karena memuat username).

## Langkah 2: cleaning (Python)
```
pip install Sastrawi
python merapikanscrapingkedua.py
```
Tahapan cleaning:
1. Menggabungkan semua CSV dan membuang tweet dengan id yang sama
2. Mengubah semua huruf menjadi huruf kecil
3. Menghapus URL, email, mention, emoji, angka, dan simbol
4. Memadatkan huruf berulang (contoh: "haaaah" menjadi "haah")
5. Mengganti singkatan dan kata gaul memakai kamus (contoh: "gak" menjadi "tidak")
6. Tokenisasi (memecah kalimat menjadi kata)
7. Membuang tweet yang terlalu pendek (kurang dari 3 kata) dan tweet duplikat
8. Stemming ke kata dasar memakai Sastrawi

## Nama Anggota Kelompok 6
1. M. Fauzul Rozaq (240907501003)
2. Habibi Ibnu Haris (240907501007)
3. Muh. Rifqi Hasan (240907502039)