# Polyglot Persistence Layer for a Real-Time Logistics Platform

## 📌 Overview
This project implements a **polyglot persistence system** for a logistics application using multiple databases.  
It processes events from a log file, routes them to appropriate databases, and provides a unified API to query combined results.

---

## 🧱 Architecture

The system uses three different databases based on data type:

- **MongoDB** → Stores package status events (flexible document data)
- **PostgreSQL** → Stores billing/invoice data (structured relational data)
- **Neo4j** → Stores driver-location relationships (graph data)

FastAPI is used to expose APIs, and Docker is used to run all services.

---

## ⚙️ Tech Stack

- Python (FastAPI)
- PostgreSQL
- MongoDB
- Neo4j
- Docker & Docker Compose

---

## 📂 Project Structure
```bash
polyglot-logistics/
│
├── app/
│   ├── main.py
│   ├── config.py
│   ├── db/
│   │   ├── postgres.py
│   │   ├── mongo.py
│   │   └── neo4j.py
│   ├── handlers/
│   │   ├── driver_handler.py
│   │   ├── package_handler.py
│   │   ├── billing_handler.py
│   ├── services/
│   │   ├── router.py
│   │   ├── reconciler.py
│   │   └── query_service.py
│
├── events.log
├── retry_queue.json
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── docs/
    └── ADR-001-Data-Store-Selection.md
```


---

## 🔄 Event Processing

Events are read from `events.log` and processed based on type:

| Event Type               | Database     | Description                          |
|------------------------|-------------|--------------------------------------|
| PACKAGE_STATUS_CHANGE  | MongoDB     | Stores package status history        |
| BILLING_EVENT          | PostgreSQL  | Stores invoice details               |
| DRIVER_LOCATION_UPDATE | Neo4j       | Stores driver-zone relationship      |

Malformed events are safely skipped without crashing the system.

---

## 🧠 Features Implemented

- Event ingestion from file
- Routing events to multiple databases
- Handling malformed events
- Retry mechanism for database connections
- Eventual consistency handling
- Unified API for querying data
- Dockerized multi-service setup

---

## 🚀 How to Run

```bash
docker-compose up --build
```

## 🌐 API Endpoints
Access API
```bash
https://localhost:8000
https://localhost:8000/docs
```

Get Package Details
- GET /query/package/{package_id}
Example
```bash
http://localhost:8000/query/package/pkg-1
```

This API returns combined data from:

- MongoDB (status history)
- PostgreSQL (billing info)

## 🧪 Verification
### MongoDB
```bash
docker exec -it polyglot-logistics-mongo-1 mongosh
```
```bash
use logistics
db.packages.find().pretty()
```

### PostgreSQL
```bash
docker exec -it polyglot-logistics-postgres-1 psql -U user -d logistics
```
```bash
SELECT * FROM invoices;
```

### Neo4j
Open:
```bash
http://localhost:7474
```
Login:
```bash
User: neo4j
Password: password
```

Run:
```bash
MATCH (d:Driver)-[:LOCATED_IN]->(z:Zone) RETURN d,z
```

### 📊 Output

The API returns a unified, sorted timeline of events from multiple data sources.

### ⚠️ Notes
- System uses retry logic to handle delayed database startup
- Ensures eventual consistency across all databases
- All services run inside Docker containers

---

## ✅ Conclusion

This project demonstrates:

- Polyglot persistence

- Event-driven processing

- Multi-database integration

- Fault-tolerant backend design