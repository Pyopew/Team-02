from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

engine = create_engine(
    "sqlite://",
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


def test_create_and_list_health_metrics():
    register_response = client.post(
        "/api/users/register",
        json={
            "login_id": "healthuser",
            "name": "건강사용자",
            "email": "healthuser@example.com",
            "password": "abc123!",
            "phone_number": "010-1111-2222",
            "gender": "F",
        },
    )
    user_id = register_response.json()["user_id"]

    create_response = client.post(
        "/api/health-metrics",
        json={"height": 170.2, "weight": 62.5},
        headers={"X-User-Id": str(user_id)},
    )
    assert create_response.status_code == 200, create_response.text
    data = create_response.json()
    assert data["height"] == 170.2
    assert data["weight"] == 62.5

    list_response = client.get(
        "/api/health-metrics",
        headers={"X-User-Id": str(user_id)},
    )
    assert list_response.status_code == 200, list_response.text
    assert len(list_response.json()) >= 1
