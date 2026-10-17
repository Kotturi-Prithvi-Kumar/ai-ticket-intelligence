# AI Ticket Intelligence — Project Handoff

## Project Overview

**Project:** AI-Powered Customer Support & Ticket Intelligence Platform

**Primary objective:** Demonstrate practical ML engineering skills through an end-to-end customer support application.

**Timeline:** 6 weeks (approximately 216 development hours)

**Current milestone:** Week 1 — Day 1

## Development Environment

- OS: Windows 11
- IDE: Visual Studio Code
- Python: 3.14.3
- Git: 2.53.0
- Docker CLI: 29.6.2
- Python virtual environment: `.venv`
- Hardware: Intel i5-1035G1, 8 GB RAM, integrated graphics
- Budget: Free tools and services only

## Completed

- [x] Verified Python installation
- [x] Verified Git installation
- [x] Verified Docker CLI installation
- [x] Verified VS Code installation
- [x] Created project directory
- [x] Initialized Git repository on `main`
- [x] Created Python virtual environment
- [x] Verified virtual environment interpreter
- [x] Created initial directory structure
- [x] Created `.gitignore`
- [x] Created `README.md`
- [x] Created `docs/architecture.md`

## Pending — Day 1

- [ ] Create and verify `PROJECT_HANDOFF.md`
- [ ] Verify `.gitignore` rules
- [ ] Add placeholder files for empty directories
- [ ] Create first Git commit
- [ ] Connect repository to GitHub

## Architecture Decisions

- Modular monolith for the MVP
- FastAPI backend
- PostgreSQL database
- React + TypeScript frontend
- Scikit-learn baseline using TF-IDF and Logistic Regression
- CPU-only ML training and inference
- No paid infrastructure
- Model evaluation required before deployment
- RAG and advanced NLP after core ML functionality

## Open Questions

- Python 3.14 compatibility with the full ML dependency stack
- Final dataset and label availability
- Priority prediction implementation
- Vector retrieval approach
- Deployment feasibility

## Next Milestone

**Week 1 — Day 2: PostgreSQL database design**

Planned activities:

1. Finalize the ticket database schema.
2. Define database relationships and constraints.
3. Configure local PostgreSQL.
4. Prepare the database migration approach.

## Week 1 — Day 2: Backend Foundation

**Status:** Implementation completed; final Git verification pending.

### Completed
- Created modular FastAPI backend structure.
- Installed FastAPI and Uvicorn.
- Implemented the `/health` endpoint.
- Added centralized application configuration.
- Configured Python application logging.
- Installed pytest and HTTPX.
- Implemented and passed the first automated health endpoint test.
- Investigated and resolved module import and API response issues.

### Technical Decisions
- FastAPI for REST API development.
- Uvicorn as the ASGI server.
- Python's built-in logging for initial application logging.
- pytest and FastAPI TestClient for automated API testing.
- Modular directories for APIs, models, schemas, services, and core infrastructure.

### Next Steps
- Define ticket database models.
- Configure PostgreSQL connectivity.
- Introduce SQLAlchemy and database migrations.
- Begin implementing ticket CRUD endpoints.

### Known Considerations
- Python 3.14.3 is being used; future ML dependencies require compatibility verification.
- Production logging configuration and database connectivity are not yet implemented.

## Collaboration Rules

- ChatGPT: Planning, explanations, architecture, and code review
- Codex: Implementation assistance, refactoring, and debugging
- GitHub: Authoritative source code
- Verify each step before proceeding
- Update this file at the end of each development session

## Week 1 — Day 3: Docker and PostgreSQL

**Status:** Implementation complete; final verification and Git commit pending.

### Completed
- Verified Docker Engine and container execution.
- Started PostgreSQL 17 using Docker Compose.
- Configured persistent database storage.
- Resolved Windows port binding issue by using localhost port 5433.
- Integrated SQLAlchemy 2.x and psycopg 3 with FastAPI.
- Implemented database session management.
- Created the Ticket ORM model with seven columns.
- Configured Alembic migrations.
- Applied initial migration `6eac92b9d00d`.
- Verified PostgreSQL table schema.
- Confirmed `.env` is Git-ignored.

### Architecture decisions
- PostgreSQL is the primary relational database.
- SQLAlchemy provides ORM and database connection management.
- Alembic manages schema migrations.
- Database credentials are loaded from environment variables.
- FastAPI remains outside Docker during local development.

### Next steps
- Complete final tests and Git commit.
- Implement ticket creation and retrieval endpoints.
- Add Pydantic request and response schemas.
- Add API integration tests.

## Week 1 — Day 4: Ticket CRUD API

**Status:** Implementation and automated testing complete.

### Implemented
- Created Pydantic schemas for ticket creation, updates, and responses.
- Implemented REST API endpoints for creating, listing, retrieving, updating, and deleting tickets.
- Added pagination for ticket listing.
- Added input validation and HTTP error handling.
- Integrated FastAPI endpoints with PostgreSQL through SQLAlchemy.
- Added database-backed integration tests using an isolated test database and transaction rollback.

### Verification
- Full backend test suite: **16 passed, 3 warnings**.
- CRUD operations manually verified through Swagger UI.
- Confirmed test database isolation and rollback behavior.
- Three non-blocking dependency deprecation warnings remain.

### Next Steps
1. Review and commit the completed CRUD API.
2. Begin Week 1 Day 5: API improvements and backend hardening.
3. Continue toward ML dataset preparation and model development in subsequent milestones.

### Week 1 — Day 5: Ticket Validation and API Hardening

**Status:** Implementation and testing completed.

**Completed:**
- Added whitespace validation and trimming for ticket subjects and descriptions.
- Preserved restricted priority and status values using `Literal`.
- Added 17 schema validation test cases.
- Added 9 API validation integration test cases.
- Verified that rejected PATCH requests preserve existing database records.
- Confirmed 42 passing tests with 3 warnings.

**Engineering decisions:**
- Reused Pydantic validators instead of adding validation logic to individual API endpoints.
- Retained PostgreSQL transaction isolation for integration tests.
- Kept existing API contracts and database schema unchanged.

**Follow-up:**
- Review the three pytest warnings.
- Review input-length boundaries and PATCH null handling.
- Prepare the dataset and ML classification pipeline.

**Latest verification:** `42 passed, 3 warnings in 1.82s`.

### Week 1 — Day 6: API Reliability and Transaction Testing

**Status:** Implementation and testing complete.

**Completed:**
- Reviewed existing ticket CRUD endpoints and DELETE implementation.
- Verified HTTP 204, empty response body, and HTTP 404 deletion behavior.
- Added simulated database commit-failure tests for POST, PATCH, and DELETE.
- Verified HTTP 500 responses, safe error messages, and rollback invocation.
- Confirmed PostgreSQL 17 Docker container is healthy.
- Ran the complete regression suite: **45 passed, 3 warnings**.

**Technical decisions:**
- Retained hard deletion for the MVP.
- Used `unittest.mock` to simulate SQLAlchemy commit failures.
- Reused the existing isolated PostgreSQL test fixtures.
- Avoided adding dependencies or modifying working production endpoints.

**Known limitations:**
- Commit-failure tests use mocks rather than real PostgreSQL outages.
- Three existing test warnings remain to be investigated.
- GET endpoint database-error handling has not been explicitly tested.

**Next steps:**
- Review API reliability and remaining test coverage.
- Finalize Week 1 documentation.
- Prepare for Week 2 ML data ingestion and preprocessing.
## Current Blockers

None confirmed.

## Last Updated

2026-10-17