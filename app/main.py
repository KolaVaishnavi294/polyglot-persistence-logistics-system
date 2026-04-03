from fastapi import FastAPI
from app.services.router import process_events
from app.services.reconciler import run_reconciliation
from app.services.query_service import get_package_data
from app.db.postgres import init_table, init_invoice_table

app = FastAPI()

@app.on_event("startup")
def startup():
    init_table()
    init_invoice_table()
    process_events()
    run_reconciliation()

@app.get("/query/package/{package_id}")
def query(package_id: str):
    return get_package_data(package_id)