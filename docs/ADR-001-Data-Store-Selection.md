### Context
Need different DBs for relationships, history, and transactions.

### Decision
- Neo4j → Graph relationships
- MongoDB → Flexible history
- PostgreSQL → Transactions

### Consequences
Pros:
- Best performance per use case
- Scalable

Cons:
- Increased complexity
- Eventual consistency needed