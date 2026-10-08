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


def test_create_and_list_diet_plans():
    register_response = client.post(
        "/api/users/register",
        json={
            "login_id": "dietplanuser",
            "name": "식단사용자",
            "email": "dietplanuser@example.com",
            "password": "abc123!",
            "phone_number": "010-4444-5555",
            "gender": "F",
        },
    )
    assert register_response.status_code == 200, register_response.text
    user_id = register_response.json()["user_id"]

    create_response = client.post(
        "/api/diet-plans",
        json={"plan_details": {"breakfast": "오트밀", "lunch": "닭가슴살 샐러드", "dinner": "연어와 채소"}},
        headers={"X-User-Id": str(user_id)},
    )
    assert create_response.status_code == 200, create_response.text
    data = create_response.json()
    assert data["plan_details"]["breakfast"] == "오트밀"

    list_response = client.get(
        "/api/diet-plans",
        headers={"X-User-Id": str(user_id)},
    )
    assert list_response.status_code == 200, list_response.text
    assert len(list_response.json()) >= 1
