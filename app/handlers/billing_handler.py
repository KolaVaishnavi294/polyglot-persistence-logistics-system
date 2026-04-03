import json
from app.db.postgres import get_connection
conn = get_connection()
from app.db.mongo import packages

def handle_billing(event):
    payload = event["payload"]

    pkg = packages.find_one({"package_id": payload["package_id"]})

    delivered = False
    if pkg:
        delivered = any(s["status"] == "DELIVERED" for s in pkg["status_history"])

    if not delivered:
        with open("retry_queue.json", "a") as f:
            f.write(json.dumps(event) + "\n")
        return

    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO invoices (invoice_id, package_id, customer_id, amount)
            VALUES (%s,%s,%s,%s)
        """, (
            payload["invoice_id"],
            payload["package_id"],
            payload["customer_id"],
            payload["amount"]
        ))
        conn.commit()
    except Exception as e:
        print("Duplicate or DB error:", e)