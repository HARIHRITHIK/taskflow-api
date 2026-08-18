# TaskFlow API — Backend Engine

A production-inspired Python REST API platform engineered with FastAPI, PostgreSQL/SQLite, SQLAlchemy ORM, Alembic migrations, and Docker.

---

## 🚀 Live Demo & Documentation

> **Live Demo:** [ADD LIVE DEMO URL HERE]  
> **Swagger UI:** [ADD SWAGGER URL HERE]  
> **Full Documentation:** Refer to the root [README.md](../README.md) and [docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md).

---

## ⚡ Quickstart

```bash
# 1. Run database migrations
alembic upgrade head

# 2. Run database seeder
python scripts/seed.py

# 3. Start Uvicorn server
uvicorn app.main:app --reload --port 8000
```
- Swagger UI: `http://127.0.0.1:8000/docs`
- Health Probe: `http://127.0.0.1:8000/health`
- Operational Telemetry: `http://127.0.0.1:8000/api/v1/system/stats`

---

## 🧪 Automated Testing

```bash
pytest -v tests/
```
