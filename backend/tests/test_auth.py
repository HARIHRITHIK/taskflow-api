def test_register_user_success(client):
    """Test successful user registration."""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "Password123!"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "testuser@example.com"
    assert "id" in data
    assert "hashed_password" not in data


def test_register_duplicate_email(client):
    """Test user registration with existing email fails."""
    client.post(
        "/api/v1/auth/register",
        json={"username": "user1", "email": "duplicate@example.com", "password": "Password123!"}
    )
    response = client.post(
        "/api/v1/auth/register",
        json={"username": "user2", "email": "duplicate@example.com", "password": "Password123!"}
    )
    assert response.status_code == 400
    assert "Email is already registered" in response.json()["detail"]


def test_register_duplicate_username(client):
    """Test user registration with existing username fails."""
    client.post(
        "/api/v1/auth/register",
        json={"username": "sameuser", "email": "user1@example.com", "password": "Password123!"}
    )
    response = client.post(
        "/api/v1/auth/register",
        json={"username": "sameuser", "email": "user2@example.com", "password": "Password123!"}
    )
    assert response.status_code == 400
    assert "Username is already taken" in response.json()["detail"]


def test_login_success(client):
    """Test successful login returns valid JWT bearer access token."""
    client.post(
        "/api/v1/auth/register",
        json={"username": "loginuser", "email": "login@example.com", "password": "SecretPassword123"}
    )
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "login@example.com", "password": "SecretPassword123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client):
    """Test login with wrong password fails with 401 Unauthorized."""
    client.post(
        "/api/v1/auth/register",
        json={"username": "loginuser2", "email": "login2@example.com", "password": "SecretPassword123"}
    )
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "login2@example.com", "password": "WrongPassword"}
    )
    assert response.status_code == 401
    assert "Invalid credentials" in response.json()["detail"]
