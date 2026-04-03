from app.db.neo4j import get_neo4j_driver

driver = get_neo4j_driver()

def handle_driver(event):
    payload = event["payload"]

    with driver.session() as session:
        session.run("""
            MERGE (d:Driver {driverId: $driver_id})
            SET d.latitude = $lat, d.longitude = $lon
            MERGE (z:Zone {zoneId: $zone_id})
            MERGE (d)-[:LOCATED_IN]->(z)
        """, driver_id=payload["driver_id"],
             lat=payload["location"]["lat"],
             lon=payload["location"]["lon"],
             zone_id=payload["zone_id"])