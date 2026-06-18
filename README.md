# 🔵 Chelsea FC Moneyball Analytics Dashboard (Season 2024/2025)

![Chelsea Logo](https://ssl.gstatic.com/onebox/media/sports/logos/optimized/fhBITrIlbQxhVB6IjxUO6Q_64x64.png)

Dashboard analitik interaktif berbasis Python yang menerapkan metode **Sabermetrics / Moneyball** untuk mengevaluasi performa Chelsea FC sepanjang musim 2024/2025. Proyek ini memvalidasi intuisi taktis (*eye test*) menggunakan data statistik murni (seperti *Expected Goals* (xG) dan *Expected Assists* (xA) per 90 menit) untuk mengambil keputusan bursa transfer yang objektif dan efisien.

## 🚀 Fitur Utama
1. **📊 Seasonal Overview & Google-Style Standings**: Rekapan lengkap performa Chelsea selama 38 pertandingan dengan visualisasi klasemen interaktif yang meniru gaya pencarian Google.
2. **📈 10 Key Benchmarking Metrics**: Analisis mendalam mencakup efektivitas taktis klub se-Premier League, peta pergerakan klasemen (*trend analysis*), profiling ancaman pemain (xG90 vs xA90), konversi gol individu, agresivitas bertahan (Moisés Caicedo benchmark), hingga indeks kedisiplinan liga.
3. **👥 Interactive Tactics Board (4-2-3-1)**: Visualisasi susunan *Starting XI* utama di atas grafis lapangan sepak bola interaktif lengkap dengan panel *Substitutes* dinamis yang diurutkan berdasarkan menit bermain.
4. **🧠 Moneyball Transfer Strategy Report**: Laporan tingkat eksekutif (*Executive Summary*) yang memberikan rekomendasi strategis pemain mana saja yang wajib **Dipertahankan**, **Dijual demi Keuntungan Finansial (*Peak Market Value*)**, **Dijual Segera (*Surplus*)**, dan **Dipinjamkan** beserta nama pemain pengganti spesifik dari klub lain (*undervalued targets*).

## 🛠️ Tech Stack
- **Core Engine**: Python 3.10+, Pandas, NumPy
- **Visualization**: Plotly Express, Plotly Graph Objects
- **Web Framework**: Streamlit & Streamlit Components
- **DevOps**: Docker

## 📁 Struktur Proyek
```text
chelsea-moneyball-analytics-24-25/
│
├── data/
│   ├── raw/                 # File CSV mentah (premier_player_info, gameweek_38, dll)
│   └── processed/           # Dataset hasil pipeline cleaning yang siap dianalisis
│
├── scripts/
│   ├── 01_clean_data.py     # Pipeline pembersihan data mentah
│   └── 02_analyze_data.py   # Modul kalkulasi metrik sepak bola (per 90 menit)
│
├── dashboard/
│   └── app.py               # Kode utama antarmuka dashboard Streamlit
│
├── Dockerfile               # Konfigurasi containerization untuk deployment
├── .gitignore               # Daftar file yang diabaikan oleh Git
└── requirements.txt         # Daftar library Python dependency proyek