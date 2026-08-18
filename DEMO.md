# ⚡ 2-Minute Recruiter Demo: TaskFlow Platform

> **Live Demo:** [ADD LIVE DEMO URL HERE]  
> **Swagger Documentation:** [ADD SWAGGER URL HERE]  
> **GitHub Repository:** [https://github.com/HARIHRITHIK/taskflow-api](https://github.com/HARIHRITHIK/taskflow-api)

---

## ⏱️ Quick Walkthrough (Under 2 Minutes)

Follow these 9 quick steps to evaluate the end-to-end functionality of TaskFlow:

### 1. Open the Live Demo
Navigate to the **[Live Demo URL]** in your browser. The application automatically initializes the database schema and loads realistic pre-seeded sample data for `admin@taskflow.dev`.

### 2. View the Work Management Dashboard
Observe the clean, modern SaaS workspace layout featuring real-time task items, priority tags (`URGENT`, `HIGH`, `MEDIUM`, `LOW`), and inline status indicators.

### 3. Create a New Task Item
1. Click the **"➕ New Task Item"** expander.
2. Enter a title: `Implement Connection Pooling Optimization`.
3. Set the priority to **URGENT**, pick a due date, and assign tags: `database,backend`.
4. Click **Create Work Item**. Notice the instantaneous database persistence and UI refresh.

### 4. Edit Task Attributes Inline
Click the **"✏️ Edit"** popover on any task to modify the title, description, or priority level directly inline.

### 5. Search & Real-Time Priority Filtering
1. In the search box, type `PostgreSQL` or `Security` to see real-time query filtering.
2. Use the **Priority** dropdown to filter exclusively by `URGENT` or `HIGH` tasks.
3. Use the **Status** dropdown to toggle between `Pending` and `Completed` items.

### 6. Toggle Completion & Test Soft Deletes
1. Click **"Mark Done"** on any pending task—the task status updates immediately.
2. Click **"🗑️"** on a task to soft-delete it (`is_deleted = True`), preserving database auditability while removing it from active queries.

### 7. Inspect Work Velocity & Telemetry
1. Switch to the **"📊 Velocity & Analytics"** tab to view real-time completion percentages and priority distribution charts calculated directly from database rows.
2. Switch to the **"🏥 Telemetry & Health"** tab to inspect live database query latency measurements (e.g., `Query Latency: 1.2 ms`) and liveness/readiness probes.

### 8. Test Authentication & Token Generation
Switch to the **"🔑 API Developer Console"** tab to:
- Test the live **Argon2id password hasher** to see real cryptographic memory-hard hash generation.
- Generate signed **JWT Bearer Access Tokens** (`HS256`) for API integration.

### 9. Explore Interactive Swagger Documentation
Open the **[Swagger Documentation URL]** (`/docs`) to test the underlying FastAPI REST endpoints (`GET /api/v1/tasks/`, `POST /api/v1/auth/login`, `GET /health`) with interactive OpenAPI request validation.
