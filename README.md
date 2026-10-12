# Scraping Tweet Topik Kasus Korupsi MBG
Tugas Kelompok 6 Sosial Media Analisis, Bisnis Digital UNM

## Tujuan
Mengambil tweet publik tentang kasus korupsi MBG, lalu menghitung kata kunci yang sering muncul.

## Langkah 1: scraping (tweet-harvest)
npx tweet-harvest@latest
Kata kunci pencarian: korupsi MBG lang:id
Hasil tersimpan di folder tweets-data (tidak diupload).

## Langkah 2: analisis (Python)
python scraper.py
Script membaca CSV, menghapus duplikat, dan menghitung kata kunci.

Nama Anggota Kelompok 6:
1. M. Fauzul Rozaq      (240907501003)
2. Habibi Ibnu Haris    (240907501007)
3. Muh. Rifqi Hasan     (240907502039)