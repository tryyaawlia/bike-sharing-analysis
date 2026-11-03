# Bike Sharing Analysis Dashboard 🚲

## Deskripsi Proyek

Proyek ini bertujuan untuk menganalisis data penyewaan sepeda (*Bike Sharing Dataset*) selama periode 2011–2012. Analisis dilakukan untuk memahami pola penyewaan sepeda berdasarkan waktu, kondisi cuaca, musim, serta jenis pengguna.

Hasil analisis disajikan dalam bentuk visualisasi data dan dashboard interaktif menggunakan Streamlit.

## Struktur Direktori

```text
submission/
├── dashboard/
│   ├── dashboard.py
│   └── main_data.csv
├── data/
│   ├── hour.csv
│   └── day.csv
├── notebook.ipynb
├── README.md
├── requirements.txt
└── url.txt
```

## Pertanyaan Bisnis

1. Bagaimana pola rata-rata jumlah penyewaan sepeda berdasarkan jam dalam sehari dan jenis hari (hari kerja dan hari non-kerja) selama periode 2011–2012?
2. Bagaimana perbedaan rata-rata jumlah penyewaan sepeda berdasarkan kondisi cuaca dan musim selama periode 2011–2012?
3. Bagaimana perbandingan jumlah penyewaan sepeda antara pengguna casual dan registered selama periode 2011–2012?

## Setup Environment - Anaconda

```bash
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal

Buat folder proyek dan masuk ke direktori proyek:

```bash
mkdir bike-sharing-analysis
cd bike-sharing-analysis
```

Buat virtual environment:

```bash
python -m venv .venv
```

Aktifkan virtual environment:

**Windows:**
```bash
.venv\Scripts\activate
```

**Mac/Linux:**
```bash
source .venv/bin/activate
```

Install library yang dibutuhkan:

```bash
pip install -r requirements.txt
```

## Run Streamlit Dashboard

Pastikan terminal berada di direktori utama proyek (`submission/`), kemudian jalankan perintah berikut:

```bash
streamlit run dashboard/dashboard.py
```

Dashboard akan terbuka secara otomatis melalui browser.

## Tools & Libraries

- Python
- Pandas
- Matplotlib
- Seaborn
- Streamlit
- Jupyter Notebook

## Dashboard

Dashboard interaktif dapat diakses melalui tautan berikut:

[Masukkan URL Streamlit Cloud di sini]