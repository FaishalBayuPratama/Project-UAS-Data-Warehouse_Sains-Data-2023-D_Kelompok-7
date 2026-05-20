# 📊 Data Warehouse & Komputasi Terdistribusi — Economic Freedom of the World

> Proyek UAS Mata Kuliah Data Warehouse dan Komputasi Terdistribusi  
> Program Studi Sains Data — Universitas Negeri Surabaya (UNESA) 2025

---

## 👥 Anggota Kelompok 7

| Nama | NIM |
|------|-----|
| Muhammad Dafa Alvian Ramadhani | 23031554017 |
| Faishal Bayu Pratama | 23031554092 |
| Iqbal Wahyufirmansyah | 23031554106 |

---

## 📌 Deskripsi Project

Proyek ini menerapkan konsep **Data Warehouse** dan **Komputasi Terdistribusi** menggunakan dataset **Economic Freedom of the World (EFW) 2024** yang diterbitkan oleh Fraser Institute.

Dataset EFW mengukur kebebasan ekonomi di 165 negara berdasarkan 5 area utama: ukuran pemerintah, sistem hukum & hak kepemilikan, stabilitas moneter, kebebasan perdagangan internasional, dan regulasi. Data mencakup periode **1950–2022**.

Pipeline yang dibangun mencakup:
- **Preprocessing** — integrasi 3 sheet Excel (EFW 2024, Panel Data, EFW 1950–1965) menggunakan Pandas
- **Processing** — analisis multidimensi / OLAP menggunakan **Atoti** (Data Cube)
- **Post-processing** — distribusi hasil via **RabbitMQ** + **Celery**, disimpan ke **PostgreSQL** sebagai Data Warehouse

### Pertanyaan Analisis yang Dijawab
1. Nilai EFW Indonesia dari tahun 1950–2022
2. Rata-rata EFW setiap negara dari 1950–2022
3. World Bank Region dengan EFW terkecil beserta negaranya tiap tahun
4. Rata-rata EFW untuk setiap World Bank Region (1950–2022)
5. Negara dengan nilai EFW terbesar per area (1970–2022)
6. Nilai setiap area EFW di Indonesia (1970–2022)

---

## 🗂️ Struktur File

```
📦 repo/
├── 📓 UAS_DWH_Kelompok7.ipynb                          # Notebook utama
├── 🐍 task.py                                           # Celery worker → PostgreSQL
├── 📊 efotw-2024-master-index-data-for-researchers-iso.xlsx  # Dataset asli (Fraser Institute)
├── 📄 Data_Bersih.csv                                   # Hasil preprocessing: Sheet 1 + Sheet 3
├── 📄 Data_Bersih2.csv                                  # Hasil preprocessing: Sheet 2 Panel Data
├── 📋 requirements.txt                                  # Dependensi Python
├── 🔒 .gitignore                                        # File yang dikecualikan dari Git
└── 📖 README.md                                         # Dokumentasi ini
```

### Penjelasan CSV
| File | Isi | Dipakai untuk |
|------|-----|---------------|
| `Data_Bersih.csv` | Gabungan Sheet 1 + Sheet 3 — kolom: `Year`, `Country`, `Economic_Freedom_Summary_Index`, `World_Bank_Region` | Sesi Atoti 1 → Soal 1–4 |
| `Data_Bersih2.csv` | Sheet 2 Panel Data — kolom: `Countries`, `Year`, `Area_1` s/d `Area_5`, dll. | Sesi Atoti 2 → Soal 5–6 |

> 💡 Kedua CSV sudah tersedia di repo sebagai hasil preprocessing. Kalau ingin menjalankan ulang bagian preprocessing dari awal, dataset `.xlsx` aslinya juga sudah disertakan.

---

## ⚙️ Prasyarat Sistem

| Komponen | Versi Minimum |
|----------|--------------| 
| Python | 3.9+ |
| PostgreSQL | 13+ |
| RabbitMQ | 3.9+ |
| Erlang (untuk RabbitMQ) | 24+ |

---

## 🚀 Cara Menjalankan

### 1. Clone Repository

```bash
git clone https://github.com/<username>/<repo-name>.git
cd <repo-name>
```

### 2. Buat Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

### 3. Install Dependensi Python

```bash
pip install -r requirements.txt
```

### 4. Install & Jalankan RabbitMQ

**Linux (Ubuntu/Debian):**
```bash
# Install Erlang dulu
sudo apt install erlang -y

# Install RabbitMQ
sudo apt install rabbitmq-server -y
sudo systemctl enable rabbitmq-server
sudo systemctl start rabbitmq-server

# (Opsional) Aktifkan management UI → http://localhost:15672
sudo rabbitmq-plugins enable rabbitmq_management
```

**Windows:** Unduh installer dari [rabbitmq.com](https://www.rabbitmq.com/download.html), pastikan Erlang terinstall lebih dulu.

Cek status:
```bash
sudo systemctl status rabbitmq-server
```

### 5. Siapkan Database PostgreSQL

Buat database baru:
```sql
CREATE DATABASE "UAS_DWH";
```

Lalu **update kredensial** di `task.py` sesuai milik kamu:
```python
db_user = "postgres"        # ← ganti
db_password = "password"    # ← ganti
db_host = "localhost"
db_port = 5432
db_name = "UAS_DWH"
```

### 6. Jalankan Celery Worker

Buka **terminal baru**, aktifkan venv, lalu:
```bash
celery -A task worker --loglevel=info
```

Biarkan terminal ini tetap berjalan selama notebook dieksekusi.

### 7. Jalankan Notebook

```bash
jupyter notebook
```

Buka `UAS_DWH_Kelompok7.ipynb` dan jalankan dari atas ke bawah.

> 💡 Notebook terdiri dari 3 bagian:
> - **Pre-Processing** — baca `.xlsx`, bersihkan & gabungkan data, export ke CSV
> - **Processing** — load CSV ke Atoti, buat Data Cube, jawab 6 pertanyaan analisis
> - **Post-Processing** — kirim hasil ke RabbitMQ → Celery worker simpan ke PostgreSQL

---

## 📦 Dependensi Utama

| Library | Fungsi |
|---------|--------|
| `pandas` | Manipulasi dan preprocessing data |
| `atoti` | Analisis multidimensi / OLAP / Data Cube |
| `pika` | Koneksi ke RabbitMQ (protokol AMQP) |
| `celery` | Distributed task queue |
| `sqlalchemy` | ORM koneksi ke PostgreSQL |
| `psycopg2-binary` | Driver PostgreSQL untuk Python |
| `openpyxl` | Membaca file `.xlsx` |
| `tabulate` | Pretty print tabel di terminal |
| `jupyter` | Menjalankan notebook |

---

## 🔒 Catatan Keamanan

File `task.py` menyimpan kredensial database. Sebelum push ke repo **publik**, ganti dengan environment variable:

```python
import os
from dotenv import load_dotenv
load_dotenv()

db_user     = os.getenv("DB_USER", "postgres")
db_password = os.getenv("DB_PASSWORD", "")
db_host     = os.getenv("DB_HOST", "localhost")
db_port     = int(os.getenv("DB_PORT", 5432))
db_name     = os.getenv("DB_NAME", "UAS_DWH")
```

Buat file `.env` di root project (sudah masuk `.gitignore`, tidak akan ter-push):
```
DB_USER=postgres
DB_PASSWORD=passwordkamu
DB_HOST=localhost
DB_PORT=5432
DB_NAME=UAS_DWH
```

---

## 🗃️ Sumber Dataset

**Economic Freedom of the World 2024 Annual Report** — Fraser Institute  
https://www.fraserinstitute.org/studies/economic-freedom-of-the-world-2024-annual-report

---

## 📄 Lisensi

Proyek akademis — UAS Mata Kuliah Data Warehouse dan Komputasi Terdistribusi  
Program Studi Sains Data, FMIPA, Universitas Negeri Surabaya, 2025.
