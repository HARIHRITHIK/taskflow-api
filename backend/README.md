# ⚡ TaskFlow API Backend Service

[![CI Pipeline](https://github.com/HARIHRITHIK/taskflow-api/actions/workflows/ci.yml/badge.svg)](https://github.com/HARIHRITHIK/taskflow-api/actions/workflows/ci.yml)
[![Streamlit Interactive Demo](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://taskflow-api.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi&logoColor=white)

> **TaskFlow API** is a production-inspired Python REST API platform demonstrating how modern backend services are designed, secured, tested, documented, and deployed. Built with **FastAPI**, **PostgreSQL / SQLite**, **SQLAlchemy ORM**, **Alembic**, and **Docker**, it showcases clean 3-tier architecture, security controls, and operational observability.

---

## 📐 System Architecture

```mermaid
graph TD
    Client[HTTP Client / Postman / Swagger UI / Streamlit UI] -->|HTTP Requests| Router[FastAPI Routers app/routers]
    Router -->|Validates Input & Formats JSON| Service[Service Layer app/services]
    Service -->|Executes Business Logic & Auth| Repository[Repository Layer app/repositories]
    Repository -->|SQLAlchemy ORM Queries| Database[(PostgreSQL / SQLite Database)]
```

---

## ⚡ Quickstart Guide

```bash
# 1. Run Database Seeder (Creates Demo Admin User & Sample Tasks)
python scripts/seed.py

# 2. Launch FastAPI ASGI Server
uvicorn app.main:app --reload --port 8000
```

- Interactive Swagger Documentation: `http://localhost:8000/docs`
- Operational Metrics Dashboard: `http://localhost:8000/api/v1/system/stats`

---

## 🧪 Running Automated Tests

```bash
python -m pytest -v
```
