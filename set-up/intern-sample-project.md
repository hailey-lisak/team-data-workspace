# Project Brief

## Goal

This project is split into two stages:

1. build a medium-sized Python application with clean structure and business logic
2. then add database tables, ORM models, and persistence behavior

The goal is to complete the application first, then add persistence without changing the core behavior.

## Recommended Project

**Project name:** `team-data-workspace`

Build a small multi-user data workspace app where users can own workspaces, import generic records, and run a processing job over those records.

Use a simple domain like `customer contacts`.

Each record can contain:

- `name`
- `email`
- `company`
- `city`
- `notes`

The processing rules stay generic:

- trim whitespace
- lowercase emails
- mark records valid or invalid
- assign tags like `complete`, `missing_email`, `missing_company`, `incomplete`

## Project Focus

This project focuses on:

- multi-user boundaries
- code organization
- API shape
- background processing
- safe data handling
- test quality

It intentionally avoids:

- finance-specific logic
- too many services
- event choreography overhead
- external APIs

## Part 1: Application Layer

### Objective

Build the application first **without PostgreSQL or ORM work**.

Use in-memory storage or simple file-backed storage. Part 1 should focus on:

- project structure
- API design
- business logic separation
- ownership checks
- job orchestration
- testing quality

### Scope

Users can:

1. create a user
2. create a workspace for that user
3. import CSV records into the workspace
4. list records in the workspace
5. trigger a processing job
6. view job status

### Suggested Structure

Keep this to one main application plus one worker-like component inside the same project.

Recommended structure:

- `app/api/`
- `app/services/`
- `app/models/`
- `app/storage/`
- `app/jobs/`
- `tests/`

The worker does not need to be a separate deployable service in Part 1.

It can be:

- an internal background task
- a simple queue abstraction
- or a polling worker started from the app process

### Suggested Endpoints

- `POST /users`
- `POST /workspaces`
- `POST /workspaces/{workspace_id}/records/import`
- `GET /workspaces/{workspace_id}/records`
- `POST /workspaces/{workspace_id}/jobs/process`
- `GET /jobs/{job_id}`
- `GET /health`

### Storage Approach

Use one of these:

- in-memory dictionaries
- JSON files
- repository classes backed by local files

Recommended approach:

- use repository interfaces
- start with in-memory repository implementations

This will make Part 2 easier to implement.

### Functional Rules

#### Ownership Rules

- a workspace belongs to one user
- a user can only act on their own workspace
- record listing must always be scoped to the workspace

#### Import Rules

- blank rows are ignored
- each imported row belongs to exactly one workspace
- duplicate handling must be documented clearly

#### Processing Rules

For each record:

- trim string fields
- lowercase `email`
- mark invalid if email is missing
- assign a tag

### What To Build In Part 1

#### Code

- working Python project
- FastAPI app
- clean folder structure
- in-memory or file-backed repositories
- background processing flow
- sample CSV fixture

#### Tests

- unit tests for record normalization and tagging
- tests for ownership checks
- one end-to-end test using the API

#### Documentation

- README
- local run instructions
- short explanation of architecture
- known limitations

### Part 1 Completion Criteria

- app starts locally with one command
- users and workspaces can be created
- CSV data imports correctly
- processing updates records correctly
- job status can be queried
- user/workspace boundaries are enforced
- tests cover happy path and a few failure cases

## Part 2: Persistence Layer

### Objective

Take the Part 1 application and replace the temporary storage layer with a real persistence layer.

In Part 2, add:

- database tables
- SQLAlchemy ORM models
- migrations or schema setup
- persistence-safe query behavior

### Scope

Part 2 should preserve the Part 1 behavior while changing the storage implementation underneath.

That means:

- same core endpoints
- same processing rules
- same ownership rules
- same job status model

### Required Additions

- PostgreSQL
- SQLAlchemy
- schema creation or Alembic migrations
- repository implementations backed by the database
- Docker Compose for local DB startup

### Suggested Tables

- `users`
- `workspaces`
- `records`
- `processing_jobs`

### Minimum Fields

`users`

- `user_id`
- `email`
- `name`
- `created_at`

`workspaces`

- `workspace_id`
- `user_id`
- `name`
- `created_at`

`records`

- `record_id`
- `workspace_id`
- `name`
- `email`
- `company`
- `city`
- `notes`
- `is_valid`
- `tag`
- `processed_at`
- `created_at`

`processing_jobs`

- `job_id`
- `workspace_id`
- `status`
- `total_records`
- `processed_records`
- `error_message`
- `created_at`
- `started_at`
- `completed_at`

### Part 2 Testing

Add:

- integration tests against PostgreSQL
- tests for DB-backed ownership rules
- tests for import and processing persistence
- one end-to-end test with real DB state

### Part 2 Completion Criteria

- database-backed version works with Docker Compose
- the app behavior matches Part 1
- data persists across restarts
- tables and relationships are clear
- tests cover the DB-backed paths
- code remains organized after adding ORM

## Suggested Timeline

### Week 1

- Day 1: app skeleton and routes
- Day 2: user and workspace flow
- Day 3: CSV import flow
- Day 4: processing job flow
- Day 5: tests and cleanup for Part 1

### Week 2

- Day 6: PostgreSQL setup and schema design
- Day 7: ORM models and repositories
- Day 8: migrate Part 1 storage to DB-backed storage
- Day 9: DB integration tests
- Day 10: cleanup, docs, and demo

## Deliverables

### After Part 1

- working app without DB
- tests
- README

### After Part 2

- PostgreSQL-backed app
- ORM models
- schema or migrations
- updated tests
- updated README

## What To Avoid

Do not add these items to the project:

- authentication
- React frontend
- Kubernetes deployment
- websocket updates
- external APIs
- advanced permissions

These will make the project larger without improving the core learning goals.

## Project Summary

Build a small multi-user backend application in two phases. In Part 1, create a medium-sized FastAPI Python app where users can create workspaces, import CSV records, and run a background processing job over those records using in-memory or file-backed storage. In Part 2, replace that storage layer with PostgreSQL and SQLAlchemy ORM models while preserving the app behavior. The system must enforce user-to-workspace ownership boundaries, expose clear APIs, track job status, and include unit tests plus end-to-end coverage.
