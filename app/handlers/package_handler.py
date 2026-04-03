from app.db.mongo import packages

def handle_package(event):
    payload = event["payload"]

    packages.update_one(
        {"package_id": payload["package_id"]},
        {"$push": {
            "status_history": {
                "status": payload["status"],
                "timestamp": event["timestamp"],
                "driver_id": payload.get("driver_id")
            }
        }},
        upsert=True
    )