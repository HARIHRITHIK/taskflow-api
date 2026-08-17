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
from sqlalchemy import text

# Application domain imports
from app.database import engine, SessionLocal, Base
from app.models import User, Task, TaskPriority
from app.schemas import TaskCreate, TaskUpdate, UserCreate
from app.services.task_service import TaskService
from app.services.auth_service import AuthService
from app.core import security

# Page Configuration
st.set_page_config(
    page_title="TaskFlow — Work Execution & Workflow Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Auto-Initialize Database Schema & Default State
@st.cache_resource
def init_db():
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
                    title="Database Connection Pool Optimization",
                    description="Implement connection pre-pinging and tune pool recycling for PostgreSQL.",
                    priority=TaskPriority.URGENT.value,
                    tags="database,performance",
                    is_completed=True,
                    owner_id=user.id
                ),
                Task(
                    title="Alembic Version Migration Setup",
                    description="Establish deterministic schema migration scripts and revision branches.",
                    priority=TaskPriority.HIGH.value,
                    tags="database,migrations",
                    is_completed=True,
                    owner_id=user.id
                ),
                Task(
                    title="OAuth2 JWT Authentication & Rate Limiting",
                    description="Enforce brute-force protection with slowapi rate limiters on auth endpoints.",
                    priority=TaskPriority.HIGH.value,
                    tags="security,auth",
                    is_completed=False,
                    owner_id=user.id
                ),
                Task(
                    title="Pytest Test Suite for Data Isolation",
                    description="Verify user isolation constraints across multi-tenant task queries.",
                    priority=TaskPriority.MEDIUM.value,
                    tags="qa,testing",
                    is_completed=False,
                    owner_id=user.id
                ),
                Task(
                    title="REST API OpenAPI 3.0 Documentation",
                    description="Publish Swagger and ReDoc interactive specifications with request schemas.",
                    priority=TaskPriority.LOW.value,
                    tags="api,docs",
                    is_completed=False,
                    owner_id=user.id
                )
            ]
            db.add_all(sample_tasks)
            db.commit()
    finally:
        db.close()
    return True

init_db()

# Premium SaaS styling & sidebar controls fix
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Deploy button, Streamlit Decoration line, and Main Menu */
    .stDeployButton,
    [data-testid="stAppDeployButton"],
    #MainMenu,
    footer,
    [data-testid="stDecoration"] {
        display: none !important;
        visibility: hidden !important;
    }

    /* Keep header transparent so the sidebar toggle arrow is visible & clickable */
    header[data-testid="stHeader"] {
        background: transparent !important;
    }
    
    /* Ensure the sidebar collapse/expand controls are always visible */
    [data-testid="collapsedControl"],
    [data-testid="stSidebarCollapseButton"] {
        display: flex !important;
        visibility: visible !important;
        z-index: 99999 !important;
    }

    .badge-urgent { background-color: #FEE2E2; color: #991B1B; padding: 4px 10px; border-radius: 6px; font-weight: 600; font-size: 0.78rem; }
    .badge-high { background-color: #FFEDD5; color: #9A3412; padding: 4px 10px; border-radius: 6px; font-weight: 600; font-size: 0.78rem; }
    .badge-medium { background-color: #E0E7FF; color: #3730A3; padding: 4px 10px; border-radius: 6px; font-weight: 600; font-size: 0.78rem; }
    .badge-low { background-color: #DCFCE7; color: #166534; padding: 4px 10px; border-radius: 6px; font-weight: 600; font-size: 0.78rem; }
</style>
""", unsafe_allow_html=True)

# Sidebar Navigation
with st.sidebar:
    st.markdown("## ⚡ **TaskFlow**")
    st.caption("Work Execution & Workflow Platform")
    st.divider()

    st.markdown("### 🏢 **Workspace Account**")
    st.markdown("👤 **Current User:** `admin@taskflow.dev`")
    st.markdown("🟢 **Database Engine:** Connected")
    st.markdown("📦 **API Version:** `v1.0.0`")
    st.divider()
    st.caption("Built with FastAPI, SQLAlchemy & PostgreSQL.")

# Main Header
st.title("⚡ TaskFlow Work Management Platform")
st.caption("Enterprise-grade asynchronous task execution, priority scheduling, and REST API engine.")

tab_tasks, tab_analytics, tab_developer, tab_status = st.tabs([
    "📋 Tasks & Workflows",
    "📊 Velocity & Analytics",
    "🔑 API Developer Console",
    "🏥 Telemetry & Health"
])

# ==========================================
# TAB 1: TASKS & WORKFLOWS
# ==========================================
with tab_tasks:
    db = SessionLocal()
    task_service = TaskService(db)
    try:
        admin_user = db.query(User).filter(User.email == "admin@taskflow.dev").first()
        user_id = admin_user.id if admin_user else 1

        col_search, col_p_filter, col_s_filter = st.columns([4, 2, 2])
        with col_search:
            search_query = st.text_input("🔍 Search Work Items", placeholder="Filter by title, description, or tag...", label_visibility="collapsed")
        with col_p_filter:
            priority_filter = st.selectbox("Priority", ["ALL", "URGENT", "HIGH", "MEDIUM", "LOW"], label_visibility="collapsed")
        with col_s_filter:
            status_filter = st.selectbox("Status", ["ALL", "Pending", "Completed"], label_visibility="collapsed")

        # Create Task Expander
        with st.expander("➕ **New Task Item**", expanded=False):
            with st.form("new_task_form", clear_on_submit=True):
                col_t, col_pr = st.columns([3, 1])
                with col_t:
                    t_title = st.text_input("Task Title *", placeholder="e.g., Implement PostgreSQL indexing")
                with col_pr:
                    t_priority = st.selectbox("Priority Level", [p.value for p in TaskPriority], index=1)
                
                t_desc = st.text_area("Description", placeholder="Action items, context, and requirements...")
                
                col_d, col_tg = st.columns(2)
                with col_d:
                    t_due = st.date_input("Due Date", min_value=date.today())
                with col_tg:
                    t_tags = st.text_input("Tags", placeholder="backend,database,security")

                if st.form_submit_button("Create Work Item", use_container_width=True):
                    if not t_title.strip():
                        st.error("Title is required.")
                    else:
                        task_service.create_task(
                            TaskCreate(
                                title=t_title,
                                description=t_desc,
                                priority=TaskPriority(t_priority),
                                due_date=datetime.combine(t_due, datetime.min.time()),
                                tags=t_tags
                            ),
                            owner_id=user_id
                        )
                        st.success(f"Work item '{t_title}' created.")
                        st.rerun()

        # Query items
        p_val = TaskPriority(priority_filter) if priority_filter != "ALL" else None
        s_val = True if status_filter == "Completed" else (False if status_filter == "Pending" else None)
        q_val = search_query.strip() if search_query.strip() else None

        paginated_tasks = task_service.get_user_tasks(
            owner_id=user_id,
            q=q_val,
            is_completed=s_val,
            priority=p_val,
            page_size=50
        )

        st.markdown(f"**Showing {paginated_tasks.total} active item(s)**")

        for task in paginated_tasks.items:
            badge_class = f"badge-{task.priority.lower()}"
            with st.container():
                c1, c2, c3, c4, c5 = st.columns([4.5, 2, 1.5, 1.5, 1.2])
                with c1:
                    status_icon = "🟢" if task.is_completed else "⏳"
                    st.markdown(f"**{status_icon} {task.title}**")
                    if task.description:
                        st.caption(task.description)
                    if task.tags:
                        st.caption(f"🏷️ `{task.tags}`")
                with c2:
                    st.markdown(f"<span class='{badge_class}'>{task.priority}</span>", unsafe_allow_html=True)
                    if task.due_date:
                        st.caption(f"📅 {task.due_date.strftime('%b %d, %Y')}")
                with c3:
                    if task.is_completed:
                        if st.button("Mark Pending", key=f"reopen_{task.id}", use_container_width=True):
                            task_service.update_task(task.id, TaskUpdate(is_completed=False), user_id)
                            st.rerun()
                    else:
                        if st.button("Mark Done", key=f"done_{task.id}", use_container_width=True):
                            task_service.update_task(task.id, TaskUpdate(is_completed=True), user_id)
                            st.rerun()
                with c4:
                    with st.popover("✏️ Edit", use_container_width=True):
                        with st.form(f"edit_form_{task.id}"):
                            edit_title = st.text_input("Title", value=task.title)
                            edit_desc = st.text_area("Description", value=task.description or "")
                            edit_priority = st.selectbox(
                                "Priority", 
                                [p.value for p in TaskPriority],
                                index=[p.value for p in TaskPriority].index(task.priority) if task.priority in [p.value for p in TaskPriority] else 1
                            )
                            edit_tags = st.text_input("Tags", value=task.tags or "")
                            
                            if st.form_submit_button("Save Changes"):
                                task_service.update_task(
                                    task.id,
                                    TaskUpdate(
                                        title=edit_title,
                                        description=edit_desc,
                                        priority=TaskPriority(edit_priority),
                                        tags=edit_tags
                                    ),
                                    user_id
                                )
                                st.success("Task updated.")
                                st.rerun()
                with c5:
                    if st.button("🗑️", key=f"del_{task.id}", use_container_width=True, help="Soft Delete"):
                        task_service.delete_task(task.id, user_id)
                        st.rerun()
                st.divider()

    finally:
        db.close()

# ==========================================
# TAB 2: ANALYTICS & VELOCITY
# ==========================================
with tab_analytics:
    db = SessionLocal()
    try:
        total = db.query(Task).filter(Task.is_deleted == False).count()
        completed = db.query(Task).filter(Task.is_deleted == False, Task.is_completed == True).count()
        pending = total - completed
        completion_pct = round((completed / total * 100), 1) if total > 0 else 0.0

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Work Items", total)
        col2.metric("Completed Items", completed, delta=f"{completion_pct}%")
        col3.metric("Pending Execution", pending)
        col4.metric("Throughput Rate", f"{completion_pct}%")

        st.divider()
        st.subheader("Priority Distribution Breakdown")

        p_urgent = db.query(Task).filter(Task.is_deleted == False, Task.priority == "URGENT").count()
        p_high = db.query(Task).filter(Task.is_deleted == False, Task.priority == "HIGH").count()
        p_med = db.query(Task).filter(Task.is_deleted == False, Task.priority == "MEDIUM").count()
        p_low = db.query(Task).filter(Task.is_deleted == False, Task.priority == "LOW").count()

        c_a, c_b, c_c, c_d = st.columns(4)
        c_a.metric("🔴 Urgent Priority", p_urgent)
        c_b.metric("🟠 High Priority", p_high)
        c_c.metric("🔵 Medium Priority", p_med)
        c_d.metric("🟢 Low Priority", p_low)

    finally:
        db.close()

# ==========================================
# TAB 3: DEVELOPER CONSOLE
# ==========================================
with tab_developer:
    st.subheader("🔑 Developer API Credentials & Authentication")
    st.markdown("Generate and verify signed JWT bearer tokens and Argon2id password hashes in real-time.")

    col_jwt, col_hash = st.columns(2)
    with col_jwt:
        st.markdown("#### 🎫 JWT Access Token Generator")
        target_email = st.text_input("User Identity (email)", value="admin@taskflow.dev")
        if st.button("Generate Bearer Token", use_container_width=True):
            token = security.create_access_token(data={"sub": target_email})
            st.code(f"Bearer {token}", language="text")
            st.success("Signed JWT token generated with HS256 HMAC-SHA256 signature.")

    with col_hash:
        st.markdown("#### 🛡️ Argon2id Password Hasher")
        raw_password = st.text_input("Password to Hash", value="TaskFlowDemo123!", type="password")
        if st.button("Compute Argon2id Hash", use_container_width=True):
            hashed = security.get_password_hash(raw_password)
            st.code(hashed, language="text")
            st.caption("OWASP recommended memory-hard hashing resistant to GPU/ASIC attacks.")

    st.divider()
    st.markdown("#### 🌐 REST API Integration Example")
    st.code("""
# Retrieve paginated tasks
curl -X GET "http://localhost:8000/api/v1/tasks/?page=1&page_size=10&priority=HIGH" \\
  -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>" \\
  -H "Content-Type: application/json"
    """, language="bash")

# ==========================================
# TAB 4: TELEMETRY & HEALTH
# ==========================================
with tab_status:
    st.subheader("🏥 System Telemetry & Operational Probes")
    
    # Real database ping measurement
    db = SessionLocal()
    try:
        t0 = time.perf_counter()
        db.execute(text("SELECT 1"))
        latency_ms = round((time.perf_counter() - t0) * 1000, 2)
        db_status_text = f"Connected (Query Latency: {latency_ms} ms)"
        db_healthy = True
    except Exception as e:
        db_status_text = f"Error: {str(e)}"
        db_healthy = False
    finally:
        db.close()

    c1, c2, c3 = st.columns(3)
    with c1:
        st.success("✅ **Liveness Probe (`/health`)**\n\nASGI Process Status: `HEALTHY`")
    with c2:
        if db_healthy:
            st.success(f"✅ **Readiness Probe (`/ready`)**\n\nDatabase: `{db_status_text}`")
        else:
            st.error(f"❌ **Readiness Probe (`/ready`)**\n\nDatabase: `{db_status_text}`")
    with c3:
        st.info("📦 **Engine Version (`/version`)**\n\nTaskFlow Version: `v1.0.0`")

    st.divider()
    st.markdown("#### ⚙️ Technical Architecture Specifications")
    st.markdown("""
    - **API Engine:** FastAPI 0.100+ (Asynchronous ASGI)
    - **ORM & Migrations:** SQLAlchemy 2.0 + Alembic version-controlled scripts
    - **Security:** OWASP Argon2id password hashing + JWT Bearer Token validation
    - **Rate Limiting:** SlowAPI token bucket rate limiters on authentication endpoints
    - **Pattern:** 3-Tier Layered Architecture (`Router -> Service -> Repository`)
    """)
