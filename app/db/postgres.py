import psycopg2
from app.config import settings
import time

def get_connection():
    for i in range(10):  # retry 10 times
        try:
            conn = psycopg2.connect(
                host=settings.POSTGRES_HOST,
                database=settings.POSTGRES_DB,
                user=settings.POSTGRES_USER,
                password=settings.POSTGRES_PASSWORD
            )
            print("✅ Connected to PostgreSQL")
            return conn
        except Exception as e:
            print("⏳ Waiting for PostgreSQL...", e)
            time.sleep(3)
    
    raise Exception("❌ Could not connect to PostgreSQL")

def init_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS billing (
            id SERIAL PRIMARY KEY,
            order_id VARCHAR(50),
            amount FLOAT,
            status VARCHAR(20)
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()

    print("✅ Billing table ready")

def init_invoice_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS invoices (
            id SERIAL PRIMARY KEY,
            invoice_id VARCHAR(50),
            package_id VARCHAR(50),
            customer_id VARCHAR(50),
            amount FLOAT
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()

    print("✅ Invoices table ready")