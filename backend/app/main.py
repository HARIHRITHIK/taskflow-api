from fastapi import FastAPI
import models
from database import engine

# --- FIXED IMPORTS BELOW ---
# We use "from routers import..." because your files are in the routers/ folder
from routers import auth, tasks 

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize the application
app = FastAPI(
    title="Task Management System",
    description="A FastAPI application with Authentication and CRUD for Tasks",
    version="1.0.0"
)

# --- FIXED ROUTER INCLUDES ---
app.include_router(auth.router)
app.include_router(tasks.router)

@app.get("/", tags=["Health"])
def health_check():
    """
    Root endpoint to check API health.
    """
    return {"status": "ok", "message": "System is running"}