from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite://"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_register_user():
    response = client.post(
        "/api/users/register",
        json={
            "login_id": "user001",
            "name": "홍길동",
            "email": "user001@example.com",
            "password": "abc123!",
            "phone_number": "010-1234-5678",
            "gender": "M",
        },
    )

    assert response.status_code == 200, response.text
    data = response.json()
    assert data["login_id"] == "user001"
    assert data["email"] == "user001@example.com"
    assert "user_id" in data


def test_login_user():
    client.post(
        "/api/users/register",
        json={
            "login_id": "user002",
            "name": "김철수",
            "email": "user002@example.com",
            "password": "abc123!",
            "phone_number": "010-9876-5432",
            "gender": "F",
        },
    )

    response = client.post(
        "/api/users/login",
        json={
            "login_id": "user002",
            "password": "abc123!",
        },
    )

    assert response.status_code == 200, response.text
    assert response.json()["login_id"] == "user002"


def test_get_current_user():
    register_response = client.post(
        "/api/users/register",
        json={
            "login_id": "user003",
            "name": "박영희",
            "email": "user003@example.com",
            "password": "abc123!",
            "phone_number": "010-1111-2222",
            "gender": "F",
        },
    )
    user_id = register_response.json()["user_id"]

    me_response = client.get(
        "/api/users/me",
        headers={"X-User-Id": str(user_id)},
    )

    assert me_response.status_code == 200, me_response.text
    assert me_response.json()["name"] == "박영희"
