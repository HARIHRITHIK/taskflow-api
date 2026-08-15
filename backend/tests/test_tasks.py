def get_auth_headers(client, email="user@example.com", username="user", password="Password123!"):
    """Helper fixture function returning authorization headers for a registered user."""
    client.post(
        "/api/v1/auth/register",
        json={"username": username, "email": email, "password": password}
    )
    response = client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": password}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_task_authenticated(client):
    """Test authenticated task creation."""
    headers = get_auth_headers(client)
    response = client.post(
        "/api/v1/tasks/",
        headers=headers,
        json={
            "title": "Build FastAPI Test Suite",
            "description": "Write clean Pytest cases",
            "priority": "HIGH",
            "tags": "testing,python"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Build FastAPI Test Suite"
    assert data["priority"] == "HIGH"
    assert data["is_completed"] is False
    assert data["is_deleted"] is False


def test_create_task_unauthenticated(client):
    """Test creating a task without auth token fails with 401 Unauthorized."""
    response = client.post(
        "/api/v1/tasks/",
        json={"title": "Unauthorized Task"}
    )
    assert response.status_code == 401


def test_user_isolation(client):
    """Test User A cannot read or modify User B's task."""
    headers_a = get_auth_headers(client, email="usera@example.com", username="usera")
    headers_b = get_auth_headers(client, email="userb@example.com", username="userb")

    # User A creates a task
    create_res = client.post(
        "/api/v1/tasks/",
        headers=headers_a,
        json={"title": "User A Private Task"}
    )
    task_id = create_res.json()["id"]

    # User B attempts to access User A's task
    read_res = client.get(f"/api/v1/tasks/{task_id}", headers=headers_b)
    assert read_res.status_code == 404

    # User B attempts to delete User A's task
    delete_res = client.delete(f"/api/v1/tasks/{task_id}", headers=headers_b)
    assert delete_res.status_code == 404


def test_search_and_filter_tasks(client):
    """Test searching and filtering task endpoints."""
    headers = get_auth_headers(client)
    client.post(
        "/api/v1/tasks/",
        headers=headers,
        json={"title": "Fix Auth Bug", "priority": "URGENT", "is_completed": False}
    )
    client.post(
        "/api/v1/tasks/",
        headers=headers,
        json={"title": "Write Docs", "priority": "LOW", "is_completed": True}
    )

    # Search for 'Auth'
    search_res = client.get("/api/v1/tasks/?q=Auth", headers=headers)
    assert search_res.status_code == 200
    data = search_res.json()
    assert data["total"] == 1
    assert data["items"][0]["title"] == "Fix Auth Bug"

    # Filter by completion status
    filter_res = client.get("/api/v1/tasks/?is_completed=true", headers=headers)
    assert filter_res.status_code == 200
    filter_data = filter_res.json()
    assert filter_data["total"] == 1
    assert filter_data["items"][0]["title"] == "Write Docs"


def test_soft_delete_task(client):
    """Test soft deletion hides task from list queries."""
    headers = get_auth_headers(client)
    create_res = client.post(
        "/api/v1/tasks/",
        headers=headers,
        json={"title": "Task to Delete"}
    )
    task_id = create_res.json()["id"]

    # Delete task
    delete_res = client.delete(f"/api/v1/tasks/{task_id}", headers=headers)
    assert delete_res.status_code == 200
    assert delete_res.json()["is_deleted"] is True

    # Confirm task no longer appears in default list
    list_res = client.get("/api/v1/tasks/", headers=headers)
    assert list_res.json()["total"] == 0
