from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud, schemas
from .database import Base, engine, get_db

try:
    Base.metadata.create_all(bind=engine)
except Exception:
    pass

app = FastAPI(title="Wellness Profile API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/api/users/register", response_model=schemas.UserResponse)
def register_user(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        user = crud.create_user(db, user_data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return user


@app.post("/api/users/login", response_model=schemas.UserResponse)
def login_user(login_data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, login_data)
    if user is None:
        raise HTTPException(status_code=401, detail="로그인 정보가 올바르지 않습니다.")
    return user


@app.get("/api/users/me", response_model=schemas.UserResponse)
def get_my_user(
    x_user_id: Annotated[int | None, Header(alias="X-User-Id")] = None,
    db: Session = Depends(get_db),
):
    if x_user_id is None:
        raise HTTPException(status_code=400, detail="X-User-Id header is required")

    user = crud.get_user(db, x_user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    return user


@app.put("/api/users/me", response_model=schemas.UserResponse)
def update_my_user(
    user_data: schemas.UserUpdate,
    x_user_id: Annotated[int | None, Header(alias="X-User-Id")] = None,
    db: Session = Depends(get_db),
):
    if x_user_id is None:
        raise HTTPException(status_code=400, detail="X-User-Id header is required")

    try:
        user = crud.update_user(db, x_user_id, user_data)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return user


@app.get("/api/profiles/me", response_model=schemas.ProfileResponse)
def get_my_profile(
    x_user_id: Annotated[int | None, Header(alias="X-User-Id")] = None,
    db: Session = Depends(get_db),
):
    if x_user_id is None:
        raise HTTPException(status_code=400, detail="X-User-Id header is required")

    profile = crud.get_profile(db, x_user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@app.post("/api/profiles/me", response_model=schemas.ProfileResponse)
def create_my_profile(
    profile_data: schemas.ProfileCreate,
    x_user_id: Annotated[int | None, Header(alias="X-User-Id")] = None,
    db: Session = Depends(get_db),
):
    if x_user_id is None:
        raise HTTPException(status_code=400, detail="X-User-Id header is required")

    existing = crud.get_profile(db, x_user_id)
    if existing:
        raise HTTPException(status_code=409, detail="Profile already exists")

    return crud.create_profile(db, x_user_id, profile_data)


@app.put("/api/profiles/me", response_model=schemas.ProfileResponse)
def update_my_profile(
    profile_data: schemas.ProfileCreate,
    x_user_id: Annotated[int | None, Header(alias="X-User-Id")] = None,
    db: Session = Depends(get_db),
):
    if x_user_id is None:
        raise HTTPException(status_code=400, detail="X-User-Id header is required")

    return crud.update_profile(db, x_user_id, profile_data)


@app.get("/api/health-metrics", response_model=list[schemas.HealthMetricResponse])
def get_health_metrics(
    x_user_id: Annotated[int | None, Header(alias="X-User-Id")] = None,
    db: Session = Depends(get_db),
):
    if x_user_id is None:
        raise HTTPException(status_code=400, detail="X-User-Id header is required")

    metrics = crud.get_health_metrics(db, x_user_id)
    return [
        {
            "metric_id": metric.metric_id,
            "user_id": metric.user_id,
            "height": float(metric.height) if metric.height is not None else 0.0,
            "weight": float(metric.weight) if metric.weight is not None else 0.0,
            "measured_at": metric.measured_at,
        }
        for metric in metrics
    ]


@app.post("/api/health-metrics", response_model=schemas.HealthMetricResponse)
def create_health_metric(
    metric_data: schemas.HealthMetricCreate,
    x_user_id: Annotated[int | None, Header(alias="X-User-Id")] = None,
    db: Session = Depends(get_db),
):
    if x_user_id is None:
        raise HTTPException(status_code=400, detail="X-User-Id header is required")

    metric = crud.create_health_metric(db, x_user_id, metric_data)
    return {
        "metric_id": metric.metric_id,
        "user_id": metric.user_id,
        "height": float(metric.height),
        "weight": float(metric.weight),
        "measured_at": metric.measured_at,
    }


@app.get("/api/constraints", response_model=list[schemas.ConstraintResponse])
def get_constraints(
    x_user_id: Annotated[int | None, Header(alias="X-User-Id")] = None,
    db: Session = Depends(get_db),
):
    if x_user_id is None:
        raise HTTPException(status_code=400, detail="X-User-Id header is required")

    constraints = crud.get_constraints(db, x_user_id)
    return [
        {
            "constraint_id": item.constraint_id,
            "user_id": item.user_id,
            "constraint_type": item.constraint_type,
            "constraint_value": item.constraint_value,
            "created_at": item.created_at,
        }
        for item in constraints
    ]


@app.post("/api/constraints", response_model=schemas.ConstraintResponse)
def create_constraint(
    constraint_data: schemas.ConstraintCreate,
    x_user_id: Annotated[int | None, Header(alias="X-User-Id")] = None,
    db: Session = Depends(get_db),
):
    if x_user_id is None:
        raise HTTPException(status_code=400, detail="X-User-Id header is required")

    item = crud.create_constraint(db, x_user_id, constraint_data)
    return {
        "constraint_id": item.constraint_id,
        "user_id": item.user_id,
        "constraint_type": item.constraint_type,
        "constraint_value": item.constraint_value,
        "created_at": item.created_at,
    }


@app.get("/api/diet-plans", response_model=list[schemas.DietPlanResponse])
def get_diet_plans(
    x_user_id: Annotated[int | None, Header(alias="X-User-Id")] = None,
    db: Session = Depends(get_db),
):
    if x_user_id is None:
        raise HTTPException(status_code=400, detail="X-User-Id header is required")

    plans = crud.get_diet_plans(db, x_user_id)
    return [
        {
            "plan_id": plan.plan_id,
            "user_id": plan.user_id,
            "plan_details": plan.plan_details,
            "created_at": plan.created_at,
            "updated_at": plan.updated_at,
        }
        for plan in plans
    ]


@app.post("/api/diet-plans", response_model=schemas.DietPlanResponse)
def create_diet_plan(
    plan_data: schemas.DietPlanCreate,
    x_user_id: Annotated[int | None, Header(alias="X-User-Id")] = None,
    db: Session = Depends(get_db),
):
    if x_user_id is None:
        raise HTTPException(status_code=400, detail="X-User-Id header is required")

    plan = crud.create_diet_plan(db, x_user_id, plan_data)
    return {
        "plan_id": plan.plan_id,
        "user_id": plan.user_id,
        "plan_details": plan.plan_details,
        "created_at": plan.created_at,
        "updated_at": plan.updated_at,
    }
