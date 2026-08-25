# System Architecture Specification

## Overview & Design Philosophy
The `team-data-workspace` API is designed using a **Layered Architecture (N-Tier)** pattern. This model cleanly separates HTTP route handling, business logic execution, data validation, and database interactions. 

By keeping these concerns separated, the system can scale horizontally and adapt to new storage engines or background processing queues without breaking existing API contracts.

---

## Architecture Layers

[ Client Request ] 
->       
[  API Layer (FastAPI)  ] app/api/ - Endpoints, Routing, Request/Response Serialization
->
[  Service Layer (Business)  ] app/services/ - Workspace isolation, Data normalization, Job Logic
->
[  Data Access (SQLModel/DB)  ] app/database/ - Database queries, ORM entities, Cascading deletes
->
[  Database Layer  ] - PostgreSQL Engine


1. API Layer (app/api/)
    - Handles incoming HTTP requests and routes them to appropriate endpoints.
    - Leverages FastAPI dependency injection for database sessions and request validation.
    - Returns standardized JSON responses and mapped HTTP status codes.
2. Service Layer (app/services/)
    - Contains core application business logic.
    - Enforces system invariants (e.g., CSV normalization, tag calculations, is_valid record checks).
    - Manages state transitions for processing jobs (pending → processing → completed / failed).
3. Data and Persistence Layer (app/repository.py and database/)
    - Interacts with PostgreSQL using SQLModel / SQLAlchemy.
    - Configured with cascading lifecycle rules (delete-orphan) to enforce workspace tenant isolation and cleanup dependent entities automatically upon deletion.
## Data Digestion and Background Job Flow
    - Upload: Client posts raw contact CSV data via /workspaces/{id}/records/import.
    - Normalization: csv_parser.py strips whitespace, normalizes email addresses to lowercase, and assigns initial system timestamps (created_at).
    - Ingestion: Records enter the database flagged as unprocessed (processed_at = None, is_valid = False, tag = "incomplete").
    - Processing Execution: Triggering a job updates record states asynchronously or in batches, calculating is_valid flags, attaching summary tags, and writing a processed_at timestamp.
## Scaling to Other Applications
This architectural blueprint easily scales to broader enterprise applications because:
    - Stateless API Layer: The FastAPI service retains no local state, allowing it to scale behind a load balancer.
    - Pluggable Workers: The job service layer can be decoupled from HTTP endpoints and attached directly to distributed worker queues (e.g., Celery, Redis, or AWS SQS).
    - Tenant Isolation: Workspace boundaries ensure multi-tenant safety across all database queries.