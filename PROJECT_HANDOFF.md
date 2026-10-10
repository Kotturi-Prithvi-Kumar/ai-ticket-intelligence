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

## Collaboration Rules

- ChatGPT: Planning, explanations, architecture, and code review
- Codex: Implementation assistance, refactoring, and debugging
- GitHub: Authoritative source code
- Verify each step before proceeding
- Update this file at the end of each development session

## Current Blockers

None confirmed.

## Last Updated

2026-10-10