from app.db.mongo import packages
from app.db.postgres import get_connection

conn = get_connection()

def get_package_data(package_id):
    result = []

    # Mongo
    pkg = packages.find_one({"package_id": package_id})
    if pkg:
        for s in pkg["status_history"]:
            result.append({
                "source_system": "document_store",
                "timestamp": s["timestamp"],
                "event_details": s
            })

    # Postgres
    cur = conn.cursor()
    cur.execute("SELECT * FROM invoices WHERE package_id=%s", (package_id,))
    for row in cur.fetchall():
        result.append({
            "source_system": "relational_store",
            "timestamp": str(row[4]),
            "event_details": {
                "invoice_id": row[0],
                "amount": row[3]
            }
        })

    return sorted(result, key=lambda x: x["timestamp"])