```markdown
# Infrastructure & Deployment Specification

## Containerization Overview
The application uses **Docker** and **Docker Compose** to guarantee environment consistency across development, testing, and production environments.

---

## Service Components

### 1. Web Service (`web`)
- **Runtime:** Python 3.11+ running inside an isolated Linux container.
- **Server:** ASGI Uvicorn worker instance running FastAPI.
- **Port Mapping:** Exposes port `8000` locally (`http://localhost:8000`).
- **Health Checks:** Ensures the database is active and accepting connections before starting backend routes.

### 2. Database Service (`db`)
- **Engine:** PostgreSQL 16.
- **Port Mapping:** Exposes port `5432` for local database management tools (e.g., `pgAdmin` or DBeaver).
- **Persistence:** Mounts a named Docker volume (`postgres_data`) to maintain record state across container restarts.

---

## Environment Configuration

Configuration variables are managed safely via root-level `.env` files:

| Variable | Description |
| `POSTGRES_USER` | Database superuser account name |
| `POSTGRES_PASSWORD` | Database user authentication key |
| `POSTGRES_DB` | Default database container name |
| `DATABASE_URL` | SQLAlchemy connection string (`postgresql://...`) |

---

## Test Execution Infrastructure

Tests run completely isolated within the Docker container environment to prevent local dependency conflicts:

```bash
# Runs full pytest suite (Unit & Integration tests) inside the web container
docker compose exec web pytest