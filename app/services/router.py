import json
from app.handlers.driver_handler import handle_driver
from app.handlers.package_handler import handle_package
from app.handlers.billing_handler import handle_billing

def process_events():
    with open("events.log") as f:
        for line in f:
            if not line.strip():   # ✅ ADD THIS LINE
                continue
            try:
                event = json.loads(line)
                etype = event["type"]

                if etype == "DRIVER_LOCATION_UPDATE":
                    handle_driver(event)
                elif etype == "PACKAGE_STATUS_CHANGE":
                    handle_package(event)
                elif etype == "BILLING_EVENT":
                    handle_billing(event)

            except Exception as e:
                print("Malformed event:", e)