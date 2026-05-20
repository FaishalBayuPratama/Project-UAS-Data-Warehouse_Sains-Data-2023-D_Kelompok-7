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

Pipeline yang dibangun mencakup:
- **Preprocessing** data dari 3 sheet Excel (EFW 2024, Panel Data, dan Data 1950–1965) menggunakan Pandas
- **Processing** dan analisis multidimensi menggunakan **Atoti** (MOLAP / Data Cube)
- **Post-processing** dengan pengiriman data via **RabbitMQ** (message broker) dan penyimpanan ke **PostgreSQL** sebagai Data Warehouse menggunakan **Celery** (distributed task queue)

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
📦 project/
├── 📓 UAS_DWH_Kelompok7.ipynb   # Notebook utama (preprocessing, processing, post-processing)
├── 🐍 task.py                    # Celery worker — menerima data dari RabbitMQ & simpan ke PostgreSQL
├── 📄 Data_Bersih.csv            # Output preprocessing: gabungan Sheet 1 + Sheet 3 (1950–2022)
├── 📄 Data_Bersih2.csv           # Output preprocessing: Sheet 2 Panel Data
├── 📋 requirements.txt           # Daftar dependensi Python
└── 📖 README.md                  # Dokumentasi ini
```

> ⚠️ **Dataset asli** (`efotw-2024-master-index-data-for-researchers-iso.xlsx`) tidak disertakan di repo karena ukurannya. Unduh dari [Fraser Institute](https://www.fraserinstitute.org/studies/economic-freedom-of-the-world-2024-annual-report) dan letakkan di folder root project.

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

# Tambah repo RabbitMQ dan install
sudo apt install rabbitmq-server -y
sudo systemctl enable rabbitmq-server
sudo systemctl start rabbitmq-server

# (Opsional) Aktifkan management UI di http://localhost:15672
sudo rabbitmq-plugins enable rabbitmq_management
```

**Windows:** Unduh installer dari [rabbitmq.com](https://www.rabbitmq.com/download.html), pastikan Erlang terinstall lebih dulu.

Cek status RabbitMQ:
```bash
sudo systemctl status rabbitmq-server
```

### 5. Siapkan Database PostgreSQL

Buat database baru di PostgreSQL:
```sql
CREATE DATABASE "UAS_DWH";
```

Lalu, **update kredensial** di `task.py`:
```python
db_user = "postgres"        # ← ganti dengan username PostgreSQL kamu
db_password = "password"    # ← ganti dengan password kamu
db_host = "localhost"
db_port = 5432
db_name = "UAS_DWH"
```

### 6. Jalankan Celery Worker

Buka terminal baru, aktifkan virtual environment, lalu jalankan:
```bash
celery -A task worker --loglevel=info
```

Biarkan terminal ini tetap berjalan.

### 7. Siapkan Dataset

Unduh file `efotw-2024-master-index-data-for-researchers-iso.xlsx` dari [Fraser Institute](https://www.fraserinstitute.org/studies/economic-freedom-of-the-world-2024-annual-report) dan letakkan di folder root project (sejajar dengan `UAS_DWH_Kelompok7.ipynb`).

### 8. Jalankan Notebook

Buka Jupyter Notebook / JupyterLab:
```bash
jupyter notebook
```

Buka `UAS_DWH_Kelompok7.ipynb` dan jalankan sel dari atas ke bawah (**Run All**).

> 💡 Notebook dibagi menjadi 3 bagian utama: **Pre-Processing**, **Processing** (Atoti), dan **Post-Processing** (RabbitMQ → PostgreSQL).

---

## 📦 Daftar Dependensi

Lihat `requirements.txt` untuk daftar lengkap. Dependensi utama:

| Library | Fungsi |
|---------|--------|
| `pandas` | Manipulasi dan preprocessing data |
| `atoti` | Analisis multidimensi / OLAP / Data Cube |
| `pika` | Koneksi ke RabbitMQ (AMQP protocol) |
| `celery` | Distributed task queue |
| `sqlalchemy` | ORM untuk koneksi ke PostgreSQL |
| `psycopg2-binary` | Driver PostgreSQL untuk Python |
| `tabulate` | Penyajian data dalam format tabel |
| `jupyter` | Menjalankan notebook |

---

## 🔒 Catatan Keamanan

> File `task.py` pada versi asli menyertakan kredensial database secara hardcode. Untuk keperluan produksi atau berbagi di GitHub publik, **gunakan environment variable**:

```python
import os
db_user = os.getenv("DB_USER", "postgres")
db_password = os.getenv("DB_PASSWORD", "")
db_host = os.getenv("DB_HOST", "localhost")
db_port = int(os.getenv("DB_PORT", 5432))
db_name = os.getenv("DB_NAME", "UAS_DWH")
```

Buat file `.env` (dan tambahkan ke `.gitignore`):
```
DB_USER=postgres
DB_PASSWORD=passwordkamu
DB_HOST=localhost
DB_PORT=5432
DB_NAME=UAS_DWH
```

---

## 🗃️ Sumber Dataset

- **Economic Freedom of the World 2024 Annual Report** — Fraser Institute  
  [https://www.fraserinstitute.org](https://www.fraserinstitute.org/studies/economic-freedom-of-the-world-2024-annual-report)

---

## 📄 Lisensi

Proyek ini dibuat untuk keperluan akademis UAS mata kuliah Data Warehouse dan Komputasi Terdistribusi, Program Studi Sains Data, FMIPA Universitas Negeri Surabaya, 2025.
