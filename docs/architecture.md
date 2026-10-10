# AI Ticket Intelligence Platform — System Architecture

## 1. Architecture Overview

The platform uses a modular architecture with separate frontend, backend, database, and machine learning components.

The MVP will use synchronous ML inference through FastAPI. Background workers and more complex infrastructure will only be introduced if necessary.

## 2. System Workflow

```text
Customer / Support Agent
          |
          v
React + TypeScript Frontend
          |
          | REST API
          v
FastAPI Backend
          |
          +--------------------------+
          |                          |
          v                          v
Ticket Management             ML Inference Service
          |                          |
          v                          v
PostgreSQL Database          Text Preprocessing
                                     |
                                     v
                             Trained ML Models
                                     |
                                     v
                         Category + Priority Prediction
                                     |
                                     v
                              Confidence Scores
          |
          v
Knowledge Retrieval Service
          |
          v
Relevant Knowledge-Base Documents
          |
          v
Support Agent Reviews Suggestions
```

## 3. Core Components

### Frontend

React and TypeScript will provide a dashboard for creating, viewing, updating, and analyzing support tickets.

### Backend

FastAPI will expose REST endpoints for ticket management, predictions, and knowledge retrieval.

### Database

PostgreSQL will store tickets, prediction results, ticket status, and knowledge-base metadata.

### Machine Learning

The initial classification pipeline will use TF-IDF and Logistic Regression.

The platform will evaluate category and priority predictions using appropriate classification metrics.

### Knowledge Retrieval

A retrieval component will identify relevant knowledge-base documents for incoming tickets.

RAG-based answer suggestions are a planned extension, subject to available compute resources and free service options.

## 4. Initial Ticket Data Model

The proposed ticket entity contains:

- id
- subject
- description
- status
- predicted_category
- category_confidence
- predicted_priority
- priority_confidence
- created_at
- updated_at

The final database schema will be defined during Week 1, Day 2.

## 5. ML Lifecycle

1. Obtain and inspect a customer support dataset.
2. Clean and validate the text data.
3. Define training, validation, and test splits.
4. Train a baseline classification model.
5. Evaluate model performance and errors.
6. Save the trained model and preprocessing pipeline.
7. Load the model into the FastAPI inference service.
8. Record predictions for analysis and future monitoring.

Priority prediction will only be trained if suitable labels are available. Otherwise, its implementation and evaluation approach must be revised.

## 6. Engineering Principles

- Modular and maintainable code
- Reproducible ML experiments
- Automated tests
- Input validation and error handling
- Structured application logging
- Secure configuration through environment variables
- No committed credentials or large datasets
- CPU-compatible development
- No paid infrastructure dependencies

## 7. Architecture Decisions

| Decision | Rationale |
|---|---|
| FastAPI | Python-native APIs and ML integration |
| PostgreSQL | Relational storage and SQL capabilities |
| React + TypeScript | Typed, maintainable frontend |
| Scikit-learn baseline | Efficient training on limited hardware |
| Synchronous inference initially | Reduces MVP complexity |
| Modular monolith | Easier development and testing within six weeks |

## 8. Open Decisions

- Final public dataset and label availability
- Exact ticket categories and priority definitions
- Knowledge retrieval implementation
- Whether local transformer inference is feasible
- Final deployment approach

These decisions will be resolved during development and recorded here.