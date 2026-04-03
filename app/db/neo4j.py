import time
from neo4j import GraphDatabase
from app.config import settings

def get_neo4j_driver():
    for i in range(10):  # retry 10 times
        try:
            driver = GraphDatabase.driver(
                settings.NEO4J_URI,
                auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
            )
            driver.verify_connectivity()
            print("✅ Connected to Neo4j")
            return driver
        except Exception as e:
            print(f"⏳ Waiting for Neo4j... ({i+1}/10)")
            time.sleep(3)

    raise Exception("❌ Neo4j not available")