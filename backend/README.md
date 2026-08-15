# ⚡ TaskFlow API Backend Engine

[![CI Pipeline](https://github.com/HARIHRITHIK/taskflow-api/actions/workflows/ci.yml/badge.svg)](https://github.com/HARIHRITHIK/taskflow-api/actions/workflows/ci.yml)
[![Streamlit Interactive Demo](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://taskflow-api.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi&logoColor=white)

> **TaskFlow** is a production-grade Python REST API and workflow execution platform engineered with **FastAPI**, **PostgreSQL / SQLite**, **SQLAlchemy ORM**, **Alembic**, and **Docker**.

---

## 🏗️ Architecture

```mermaid
graph TD
    Client[HTTP Client / Postman / Swagger UI / Streamlit App] -->|HTTP JSON Requests| Router[FastAPI Routers app/routers]
    Router -->|Input Validation & Response Envelope| Service[Service Layer app/services]
    Service -->|Business Logic & Authorization| Repository[Repository Layer app/repositories]
    Repository -->|SQLAlchemy ORM Queries| Database[(PostgreSQL / SQLite Database)]
```

---

## ⚡ Quickstart

```bash
# Run seeder
python scripts/seed.py

# Start ASGI server
uvicorn app.main:app --reload --port 8000
```
