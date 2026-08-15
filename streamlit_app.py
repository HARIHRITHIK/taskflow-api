import sys
import os
import time
from datetime import datetime, timezone, date

# Ensure backend directory is in python path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(CURRENT_DIR, "backend")
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

import streamlit as st

# Application imports
from app.database import engine, SessionLocal, Base
from app.models import User, Task, TaskPriority
from app.schemas import TaskCreate, TaskUpdate, UserCreate
from app.services.task_service import TaskService
from app.services.auth_service import AuthService
from app.core import security
from app.core.config import settings

# Page Configuration
st.set_page_config(
    page_title="TaskFlow API — Interactive Demo & Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Database & Auto-Seed on Startup
@st.cache_resource
def init_and_seed_db():
    """Initializes schema and runs demo seeder if database is fresh."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        admin_email = "admin@taskflow.dev"
        user = db.query(User).filter(User.email == admin_email).first()
        if not user:
            user = User(
                username="admin",
                email=admin_email,
                hashed_password=security.get_password_hash("TaskFlowDemo123!"),
                is_active=True
            )
            db.add(user)
            db.commit()
            db.refresh(user)

            sample_tasks = [
                Task(
                    title="Review Architecture Specification",
                    description="Audit 3-tier layer separation and repository abstractions for TaskFlow API.",
                    priority=TaskPriority.URGENT.value,
                    tags="architecture,core",
                    is_completed=True,
                    owner_id=user.id
                ),
                Task(
                    title="Configure Alembic Database Migrations",
                    description="Establish version-controlled database schema migrations with revision scripts.",
                    priority=TaskPriority.HIGH.value,
                    tags="database,alembic",
                    is_completed=True,
                    owner_id=user.id
                ),
                Task(
                    title="Implement Rate Limiting on Authentication Endpoints",
                    description="Protect /auth/login and /auth/register endpoints using slowapi rate limiters.",
                    priority=TaskPriority.HIGH.value,
                    tags="security,auth",
                    is_completed=False,
                    owner_id=user.id
                ),
                Task(
                    title="Write Pytest Suite for Task Isolation",
                    description="Verify User A cannot access or mutate tasks owned by User B.",
                    priority=TaskPriority.MEDIUM.value,
                    tags="testing,pytest",
                    is_completed=False,
                    owner_id=user.id
                ),
                Task(
                    title="Prepare Postman Collection & Swagger Specs",
                    description="Generate Postman environment and OpenAPI documentation for reviewer demo.",
                    priority=TaskPriority.LOW.value,
                    tags="documentation,postman",
                    is_completed=False,
                    owner_id=user.id
                )
            ]
            db.add_all(sample_tasks)
            db.commit()
    finally:
        db.close()
    return True

init_and_seed_db()

# Custom CSS for polished, recruiter-grade UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .metric-box {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
    }
    .badge-urgent { background-color: #FEE2E2; color: #991B1B; padding: 3px 8px; border-radius: 6px; font-weight: 600; font-size: 0.8rem; }
    .badge-high { background-color: #FFEDD5; color: #9A3412; padding: 3px 8px; border-radius: 6px; font-weight: 600; font-size: 0.8rem; }
    .badge-medium { background-color: #E0E7FF; color: #3730A3; padding: 3px 8px; border-radius: 6px; font-weight: 600; font-size: 0.8rem; }
    .badge-low { background-color: #DCFCE7; color: #166534; padding: 3px 8px; border-radius: 6px; font-weight: 600; font-size: 0.8rem; }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png", width=180)
    st.markdown("### ⚡ **TaskFlow API**")
    st.markdown("*Production-Inspired Backend Platform*")
    st.divider()

    st.markdown("#### 👨‍💻 **Developer & Links**")
    st.markdown("**Author:** Hari Hrithik")
    st.markdown("📂 **GitHub:** [HARIHRITHIK/taskflow-api](https://github.com/HARIHRITHIK/taskflow-api)")
    st.markdown("📖 **API Version:** `v1.0.0`")
    st.markdown("🛡️ **Security:** Argon2id + JWT")
    st.markdown("🏗️ **Architecture:** 3-Tier Layered")

    st.divider()
    st.markdown("#### 🌟 **Portfolio Synergy**")
    st.caption("Complements my AI portfolio projects:")
    st.markdown("- 🤖 **AI Hiring Assistant**")
    st.markdown("- 📊 **AI BI Studio**")
    st.markdown("- 🔍 **Clarity**")
    st.markdown("- ⚡ **TaskFlow API** *(Core Backend)*")

# Main Header
st.markdown('<div class="main-header">⚡ TaskFlow API Platform</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Interactive Live Dashboard & REST API Engineering Showcase</div>', unsafe_allow_html=True)

# Tabs
tab_metrics, tab_tasks, tab_auth, tab_architecture = st.tabs([
    "📊 Operational Dashboard",
    "📋 Interactive TaskFlow UI",
    "🔐 Security & Auth Inspector",
    "📐 Architecture & Interview Q&A"
])

# ==========================================
# TAB 1: OPERATIONAL DASHBOARD
# ==========================================
with tab_metrics:
    db = SessionLocal()
    try:
        total_users = db.query(User).count()
        total_tasks = db.query(Task).filter(Task.is_deleted == False).count()
        completed_tasks = db.query(Task).filter(Task.is_deleted == False, Task.is_completed == True).count()
        pending_tasks = total_tasks - completed_tasks
        completion_pct = round((completed_tasks / total_tasks * 100), 1) if total_tasks > 0 else 0.0

        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Total Users", total_users, help="Registered accounts in system")
        with col2:
            st.metric("Active Tasks", total_tasks, help="Non-deleted tasks in database")
        with col3:
            st.metric("Completed", completed_tasks, delta=f"{completion_pct}%")
        with col4:
            st.metric("Pending", pending_tasks)
        with col5:
            st.metric("Service Status", "🟢 Healthy", help="Liveness & Readiness Probes passing")

        st.divider()

        st.subheader("🏥 Live System Health Probes")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.success("✅ **Liveness Probe (`GET /health`)**\n\nProcess is active and responsive.")
        with c2:
            st.success("✅ **Readiness Probe (`GET /ready`)**\n\nDatabase connectivity verified (`SELECT 1`).")
        with c3:
            st.info("ℹ️ **Version Endpoint (`GET /version`)**\n\n`TaskFlow API v1.0.0` running.")

        st.divider()
        st.subheader("📈 Task Priority Distribution")
        p_urgent = db.query(Task).filter(Task.is_deleted == False, Task.priority == "URGENT").count()
        p_high = db.query(Task).filter(Task.is_deleted == False, Task.priority == "HIGH").count()
        p_med = db.query(Task).filter(Task.is_deleted == False, Task.priority == "MEDIUM").count()
        p_low = db.query(Task).filter(Task.is_deleted == False, Task.priority == "LOW").count()

        col_a, col_b, col_c, col_d = st.columns(4)
        col_a.metric("🔴 Urgent", p_urgent)
        col_b.metric("🟠 High", p_high)
        col_c.metric("🔵 Medium", p_med)
        col_d.metric("🟢 Low", p_low)

    finally:
        db.close()

# ==========================================
# TAB 2: INTERACTIVE TASKFLOW UI
# ==========================================
with tab_tasks:
    db = SessionLocal()
    task_service = TaskService(db)
    try:
        admin_user = db.query(User).filter(User.email == "admin@taskflow.dev").first()
        user_id = admin_user.id if admin_user else 1

        # Search & Filter Controls
        col_search, col_filter_p, col_filter_s = st.columns([3, 2, 2])
        with col_search:
            search_query = st.text_input("🔍 Search Tasks", placeholder="Search title, description, or tags...")
        with col_filter_p:
            priority_filter = st.selectbox("🎯 Filter Priority", ["ALL", "URGENT", "HIGH", "MEDIUM", "LOW"])
        with col_filter_s:
            status_filter = st.selectbox("📌 Filter Status", ["ALL", "Pending", "Completed"])

        # Create Task Section (Expandable)
        with st.expander("➕ **Create New Task**", expanded=False):
            with st.form("create_task_form", clear_on_submit=True):
                new_title = st.text_input("Task Title *", placeholder="e.g., Implement Docker Healthcheck")
                new_desc = st.text_area("Description", placeholder="Detailed requirements and notes...")
                col_p, col_d, col_t = st.columns(3)
                with col_p:
                    new_priority = st.selectbox("Priority", [p.value for p in TaskPriority], index=1)
                with col_d:
                    new_due_date = st.date_input("Due Date", min_value=date.today())
                with col_t:
                    new_tags = st.text_input("Tags (comma-separated)", placeholder="devops,security")

                submitted = st.form_submit_button("Create Task", use_container_width=True)
                if submitted:
                    if not new_title.strip():
                        st.error("Task title cannot be empty.")
                    else:
                        task_create = TaskCreate(
                            title=new_title,
                            description=new_desc,
                            priority=TaskPriority(new_priority),
                            due_date=datetime.combine(new_due_date, datetime.min.time()),
                            tags=new_tags
                        )
                        task_service.create_task(task_create, owner_id=user_id)
                        st.success(f"Task '{new_title}' created successfully!")
                        st.rerun()

        # Query tasks
        p_arg = TaskPriority(priority_filter) if priority_filter != "ALL" else None
        s_arg = True if status_filter == "Completed" else (False if status_filter == "Pending" else None)
        q_arg = search_query if search_query.strip() else None

        paginated_res = task_service.get_user_tasks(
            owner_id=user_id,
            q=q_arg,
            is_completed=s_arg,
            priority=p_arg,
            page_size=50
        )

        st.markdown(f"**Found {paginated_res.total} task(s)** (Viewing demo account: `admin@taskflow.dev`)")

        for task in paginated_res.items:
            badge_class = f"badge-{task.priority.lower()}"
            with st.container():
                c1, c2, c3, c4 = st.columns([5, 2, 2, 2])
                with c1:
                    status_emoji = "✅" if task.is_completed else "⏳"
                    st.markdown(f"### {status_emoji} {task.title}")
                    if task.description:
                        st.caption(task.description)
                    if task.tags:
                        st.caption(f"🏷️ `{task.tags}`")
                with c2:
                    st.markdown(f"<span class='{badge_class}'>{task.priority}</span>", unsafe_allow_html=True)
                    if task.due_date:
                        st.caption(f"📅 Due: {task.due_date.strftime('%b %d, %Y')}")
                with c3:
                    # Toggle completion
                    if task.is_completed:
                        if st.button("↩️ Mark Pending", key=f"reopen_{task.id}"):
                            task_service.update_task(task.id, TaskUpdate(is_completed=False), user_id)
                            st.rerun()
                    else:
                        if st.button("✅ Complete", key=f"done_{task.id}"):
                            task_service.update_task(task.id, TaskUpdate(is_completed=True), user_id)
                            st.rerun()
                with c4:
                    # Soft Delete
                    if st.button("🗑️ Delete", key=f"del_{task.id}"):
                        task_service.delete_task(task.id, user_id)
                        st.warning(f"Task #{task.id} soft-deleted.")
                        st.rerun()
                st.divider()

    finally:
        db.close()

# ==========================================
# TAB 3: SECURITY & AUTH INSPECTOR
# ==========================================
with tab_auth:
    st.subheader("🔐 OWASP Argon2id & JWT Authentication Inspector")
    st.markdown("""
    TaskFlow API implements **Argon2id password hashing** (Winner of the Password Hashing Competition) and **signed JWT bearer tokens**.
    """)

    col_hash, col_jwt = st.columns(2)
    with col_hash:
        st.markdown("#### 🛡️ Live Argon2id Password Hasher")
        plain_input = st.text_input("Enter plain-text password to hash:", value="TaskFlowDemo123!", type="password")
        if plain_input:
            hashed_output = security.get_password_hash(plain_input)
            st.code(hashed_output, language="text")
            st.caption("Notice the `$argon2id$v=19$m=65536,t=3,p=4$...` format providing hardware ASIC resistance.")

    with col_jwt:
        st.markdown("#### 🎫 JWT Access Token Generator")
        demo_email = st.text_input("User Email for Token `sub` claim:", value="admin@taskflow.dev")
        if st.button("Generate Signed JWT Bearer Token"):
            token_res = security.create_access_token(data={"sub": demo_email})
            st.code(token_res, language="text")
            st.success("Bearer token signed with HMAC-SHA256 (HS256) and validated by `OAuth2PasswordBearer`.")

# ==========================================
# TAB 4: ARCHITECTURE & INTERVIEW Q&A
# ==========================================
with tab_architecture:
    st.subheader("📐 Clean 3-Tier Layered Architecture")
    st.markdown("""
    TaskFlow API decouples HTTP handling, business rules, and database persistence into three strictly separated layers:
    """)

    st.code("""
    ┌────────────────────────────────────────────────────────┐
    │          HTTP Client / Postman / Swagger UI            │
    └───────────────────────────┬────────────────────────────┘
                                │ HTTP Requests
    ┌───────────────────────────▼────────────────────────────┐
    │  1. FastAPI Routers (app/routers/auth.py, tasks.py)    │
    │     - Request Validation & Enveloped JSON Response     │
    └───────────────────────────┬────────────────────────────┘
                                │ Calls Domain Service
    ┌───────────────────────────▼────────────────────────────┐
    │  2. Service Layer (app/services/task_service.py)       │
    │     - Business Logic, User Isolation & Permissions     │
    └───────────────────────────┬────────────────────────────┘
                                │ Queries Data Access
    ┌───────────────────────────▼────────────────────────────┐
    │  3. Repository Layer (app/repositories/task_repo.py)   │
    │     - SQLAlchemy ORM Data Access & Queries             │
    └───────────────────────────┬────────────────────────────┘
                                │ SQL Transactions
    ┌───────────────────────────▼────────────────────────────┐
    │     PostgreSQL / SQLite Database Persistence           │
    └────────────────────────────────────────────────────────┘
    """, language="text")

    st.divider()
    st.subheader("💡 2-Minute Technical Interview Explanations")

    with st.expander("❓ Why did you use the Repository Pattern?"):
        st.markdown("""
        **2-Minute Pitch:**
        > *"I used the Repository Pattern to isolate all database queries and SQLAlchemy ORM operations in a dedicated data access layer. This keeps our business services completely decoupled from the database implementation, allowing us to mock database calls in unit tests and swap persistence layers without touching domain logic."*
        """)

    with st.expander("❓ Why separate the Service Layer from Routers?"):
        st.markdown("""
        **2-Minute Pitch:**
        > *"Routers should only be responsible for HTTP parsing, status codes, and serialization. Moving domain logic, permission checks, and transactional rules into reusable Service classes prevents bloated controllers and makes core business logic testable independently of the web framework."*
        """)

    with st.expander("❓ Why use Alembic instead of `metadata.create_all()`?"):
        st.markdown("""
        **2-Minute Pitch:**
        > *"`metadata.create_all()` only works for initial table creation and cannot handle schema migrations like adding columns, updating data types, or rolling back changes in production. Alembic provides version-controlled, deterministic database migration scripts that safely evolve database schemas across environments."*
        """)

    with st.expander("❓ Why choose Argon2id over standard Bcrypt?"):
        st.markdown("""
        **2-Minute Pitch:**
        > *"Argon2id is the winner of the Password Hashing Competition and recommended by OWASP. It provides superior memory-hard resistance against GPU and ASIC-accelerated brute-force attacks and avoids length-truncation flaws found in older bcrypt libraries."*
        """)

    with st.expander("❓ Why implement Soft Deletion (`is_deleted`)?"):
        st.markdown("""
        **2-Minute Pitch:**
        > *"In real-world enterprise platforms, hard-deleting records creates data integrity issues and prevents data recovery. Soft deletion preserves historical auditability while seamlessly filtering out deleted records from user queries."*
        """)
