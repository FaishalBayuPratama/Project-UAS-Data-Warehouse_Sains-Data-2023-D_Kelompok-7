from celery import Celery
import pandas as pd
from sqlalchemy import create_engine
import json

# Celery app (gunakan RabbitMQ sebagai broker)
app = Celery('tasks', broker='pyamqp://guest@localhost//')

# PostgreSQL connection (Ubah sesuai kredensial kamu)
db_user = "postgres"
db_password = "AyamSayur23"
db_host = "localhost"
db_port = 5432
db_name = "UAS_DWH"

# Build database URL
db_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
engine = create_engine(db_url)

@app.task
def simpan_ke_postgres(json_data, table_name):
    try:
        # Parse JSON ke DataFrame
        df = pd.read_json(json_data, orient='records')

        # Simpan ke PostgreSQL
        df.to_sql(table_name, con=engine, if_exists='replace', index=False)
        print(f"✅ Tabel '{table_name}' berhasil disimpan.")
        return f"Sukses simpan {table_name}"
    except Exception as e:
        print(f"❌ Gagal menyimpan {table_name}: {e}")
        return f"Gagal simpan {table_name}"
