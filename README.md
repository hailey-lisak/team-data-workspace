# Team Data Workspace API (`team-data-workspace`)

A multi-user backend data ingestion and background processing service built with **FastAPI**, **SQLModel (SQLAlchemy)**, and **PostgreSQL**.

This application enables users to create isolated data workspaces, bulk-import raw contact records via CSV, run background processing jobs to clean and tag records, and query processed results safely within strict tenant boundaries.



## Key Features & Business Rules

- **Resource Granularity & Allowed Actions:**
  - **Users & Workspaces:** Full CRUD support (`GET`, `POST`, `PUT`, `DELETE`). Deleting a user or workspace triggers cascading lifecycle cleanup, automatically purging all dependent records and jobs (`delete-orphan`).
  - **Records:** Supports Creation, Ingestion, & Management (`POST`, `GET`, `DELETE`). Individual record mutation (`PUT`) is restricted to maintain data integrity after ingestion.
  - **Jobs:** Supports Processing Lifecycles (`POST`, `GET`, `PUT`). Jobs are created, queried, and updated with state transitions (`pending` → `processing` → `completed`/`failed`).

- **Data Ingestion & CSV Normalization:** 
  - Bulk creation (`POST`) of contact records via CSV file uploads.
  - Automatic string trimming, email lowercase normalization, and field completeness validation.
- **System-Wide Queries:**
  - Administrative retrieval (`GET`) provides system-wide visibility across all entities.

## Architecture & Tech Stack

- **Framework:** FastAPI (Python 3.11+)
- **Database & ORM:** PostgreSQL 16, SQLModel / SQLAlchemy
- **Containerization:** Docker & Docker Compose
- **Testing:** Pytest


### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/) installed.

### Running the Application
- ```bash
- docker compose up -d --build   

## Testing
- docker compose exec web pytest

## Directory Tree
.
├── app/
│   ├── api/             # Route handlers & API endpoints
│   │    ├── __init__.py
│   │    ├── jobs.py
│   │    ├── records.py
│   │    ├── users.py
│   │    ├── workspaces.py
│   ├── services/        # Service layer & business logic
│   │    ├── __init__.py
│   │    ├── job_services.py
│   │    ├── record_services.py
│   │    ├── user_services.py
│   │    ├── workspace_services.py
│   ├── __init__.py
│   ├── csv_parser.py    # Ingestion & normalization helpers
│   ├── main.py          # FastAPI application entry point
│   ├── repository.py    # Database queries & data access layer
│   └── schemas.py       # Pydantic / SQLModel models & validation
├── database/            # DB migrations or initialization scripts
│   │    ├── __init__.py
│   │    ├── connection.py
│   │    ├── create_tables.sql
│   │    ├── models.py
│   │    ├── test_connection.py
├── docker/              # Dockerfiles & container configs
│   │    ├── Dockerfile

├── set-up/              # Project setup scripts / utility files
├── tests/               # Integration & end-to-end test suite
│     ├── integration
│     │      ├── __init__.py
│     │      ├── test_end2end_workflow.py
│     │      ├── test_jobs_api.py
│     │      ├── test_negative_cases.py
│     │      ├── test_records_api.py
│     │      ├── test_users_api.py
│     │      ├── test_workspaces_api.py
│     ├── unit
│     │      ├── __init__.py
│     │      ├── conftest.py
│     │      ├── test_csv_parser.py
│     │      ├── test_csv_validation.py
│     │      ├── test_edge_cases.py
│     │      ├── test_job_services.py
│     │      ├── test_record_services.py
│     │      ├── test_repository.py
│     │      ├── test_user_services.py
│     │      ├── test_workspace_services.py
│     ├── sample_contacts.csv
│     ├── test_api_records.py
├── .dockerignore
├── .env                 # Environment variables
├── .gitignore
├── docker-compose.yml   # Docker multi-container configuration
├── README               # Project documentation
└── requirements.txt     # Python package dependencies