import json
from app.handlers.billing_handler import handle_billing

def run_reconciliation():
    try:
        with open("retry_queue.json") as f:
            events = f.readlines()
    except:
        return

    remaining = []

    for line in events:
        event = json.loads(line)
        before = open("retry_queue.json").read()

        handle_billing(event)

        after = open("retry_queue.json").read()
        if before == after:
            remaining.append(line)

    with open("retry_queue.json", "w") as f:
        f.writelines(remaining)