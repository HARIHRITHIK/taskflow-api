import sys
import os

# Ensure backend root directory is in sys.path
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import SessionLocal, engine, Base
from app.models import User, Task, TaskPriority
from app.core import security


def seed_database():
    """Populates database with initial demo user and realistic sample tasks."""
    print("[SEED] Initializing Database Seeder for TaskFlow API...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 1. Seed Demo Admin User
        admin_email = "admin@taskflow.dev"
        admin_user = db.query(User).filter(User.email == admin_email).first()

        if not admin_user:
            admin_user = User(
                username="admin",
                email=admin_email,
                hashed_password=security.get_password_hash("TaskFlowDemo123!"),
                is_active=True
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            print(f"[OK] Created demo user: {admin_email} (Password: TaskFlowDemo123!)")
        else:
            print(f"[INFO] Demo user {admin_email} already exists.")

        # 2. Seed Sample Tasks
        existing_tasks_count = db.query(Task).filter(Task.owner_id == admin_user.id).count()
        if existing_tasks_count == 0:
            sample_tasks = [
                Task(
                    title="Review Architecture Specification",
                    description="Audit 3-tier layer separation and repository abstractions for TaskFlow API.",
                    priority=TaskPriority.URGENT.value,
                    tags="architecture,core",
                    is_completed=True,
                    owner_id=admin_user.id
                ),
                Task(
                    title="Configure Alembic Database Migrations",
                    description="Establish version-controlled database schema migrations with revision scripts.",
                    priority=TaskPriority.HIGH.value,
                    tags="database,alembic",
                    is_completed=True,
                    owner_id=admin_user.id
                ),
                Task(
                    title="Implement Rate Limiting on Authentication Endpoints",
                    description="Protect /auth/login and /auth/register endpoints using slowapi rate limiters.",
                    priority=TaskPriority.HIGH.value,
                    tags="security,auth",
                    is_completed=False,
                    owner_id=admin_user.id
                ),
                Task(
                    title="Write Pytest Suite for Task Isolation",
                    description="Verify User A cannot access or mutate tasks owned by User B.",
                    priority=TaskPriority.MEDIUM.value,
                    tags="testing,pytest",
                    is_completed=False,
                    owner_id=admin_user.id
                ),
                Task(
                    title="Prepare Postman Collection & Swagger Specs",
                    description="Generate Postman environment and OpenAPI documentation for reviewer demo.",
                    priority=TaskPriority.LOW.value,
                    tags="documentation,postman",
                    is_completed=False,
                    owner_id=admin_user.id
                )
            ]
            db.add_all(sample_tasks)
            db.commit()
            print(f"[OK] Seeded {len(sample_tasks)} realistic demo tasks for {admin_email}.")
        else:
            print(f"[INFO] Database already contains {existing_tasks_count} tasks.")

        print("\n[SUCCESS] Seeding complete! You can now log in using:")
        print("   Email: admin@taskflow.dev")
        print("   Password: TaskFlowDemo123!\n")

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
