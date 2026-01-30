from fastapi import FastAPI
import models
from database import engine
# Assuming the router files are named auth_routes.py and task_routes.py
import auth_routes
import task_routes

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize the application
app = FastAPI(
    title="Task Management System",
    description="A FastAPI application with Authentication and CRUD for Tasks",
    version="1.0.0"
)

# Include routers
app.include_router(auth_routes.router)
app.include_router(task_routes.router)

@app.get("/", tags=["Health"])
def health_check():
    """
    Root endpoint to check API health.
    """
    return {"status": "ok", "message": "System is running"}