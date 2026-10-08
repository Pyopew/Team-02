import hashlib
import secrets
from datetime import datetime

from sqlalchemy.orm import Session

from . import models, schemas


def hash_password(password: str) -> str:
    salt = secrets.token_hex(8)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 100_000)
    return f"pbkdf2_sha256${salt}${digest.hex()}"


def verify_password(password: str, password_hash: str) -> bool:
    if not password_hash or not password_hash.startswith("pbkdf2_sha256$"):
        return False
    _, salt, digest_hex = password_hash.split("$", 2)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 100_000)
    return digest.hex() == digest_hex


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.user_id == user_id).first()


def get_user_by_login_id(db: Session, login_id: str):
    return db.query(models.User).filter(models.User.login_id == login_id).first()


def create_user(db: Session, user_data: schemas.UserCreate):
    existing_login = get_user_by_login_id(db, user_data.login_id)
    if existing_login:
        raise ValueError("이미 사용 중인 로그인 ID 입니다.")

    existing_email = db.query(models.User).filter(models.User.email == user_data.email).first()
    if existing_email:
        raise ValueError("이미 사용 중인 이메일 입니다.")

    user = models.User(
        login_id=user_data.login_id,
        name=user_data.name,
        email=user_data.email,
        phone_number=user_data.phone_number,
        gender=user_data.gender,
    )
    db.add(user)
    db.flush()

    user_auth = models.UserAuth(
        user_id=user.user_id,
        password_hash=hash_password(user_data.password),
        last_login_at=None,
        failed_login_count=0,
        locked_until=None,
    )
    db.add(user_auth)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, login_data: schemas.UserLogin):
    user = get_user_by_login_id(db, login_data.login_id)
    if user is None:
        return None

    auth = db.query(models.UserAuth).filter(models.UserAuth.user_id == user.user_id).first()
    if auth is None:
        return None

    if verify_password(login_data.password, auth.password_hash):
        auth.last_login_at = datetime.now()
        db.commit()
        return user

    return None


def update_user(db: Session, user_id: int, update_data: schemas.UserUpdate):
    user = get_user(db, user_id)
    if user is None:
        raise ValueError("사용자를 찾을 수 없습니다.")

    if update_data.name is not None:
        user.name = update_data.name
    if update_data.email is not None:
        user.email = update_data.email
    if update_data.phone_number is not None:
        user.phone_number = update_data.phone_number
    if update_data.gender is not None:
        user.gender = update_data.gender

    db.commit()
    db.refresh(user)
    return user


def get_profile(db: Session, user_id: int):
    return db.query(models.Profile).filter(models.Profile.user_id == user_id).first()


def create_profile(db: Session, user_id: int, profile_data: schemas.ProfileCreate):
    profile = models.Profile(
        user_id=user_id,
        nickname=profile_data.nickname,
        profile_image_url=profile_data.profile_image_url,
        introduction=profile_data.introduction,
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


def update_profile(db: Session, user_id: int, profile_data: schemas.ProfileCreate):
    profile = get_profile(db, user_id)
    if profile is None:
        return create_profile(db, user_id, profile_data)

    if profile_data.nickname is not None:
        profile.nickname = profile_data.nickname
    if profile_data.profile_image_url is not None:
        profile.profile_image_url = profile_data.profile_image_url
    if profile_data.introduction is not None:
        profile.introduction = profile_data.introduction

    db.commit()
    db.refresh(profile)
    return profile


def get_health_metrics(db: Session, user_id: int):
    return (
        db.query(models.HealthMetric)
        .filter(models.HealthMetric.user_id == user_id)
        .order_by(models.HealthMetric.measured_at.desc())
        .all()
    )


def create_health_metric(db: Session, user_id: int, metric_data: schemas.HealthMetricCreate):
    metric = models.HealthMetric(
        user_id=user_id,
        height=float(metric_data.height),
        weight=float(metric_data.weight),
    )
    db.add(metric)
    db.commit()
    db.refresh(metric)
    return metric


def get_constraints(db: Session, user_id: int):
    return (
        db.query(models.Constraint)
        .filter(models.Constraint.user_id == user_id)
        .order_by(models.Constraint.created_at.desc())
        .all()
    )


def create_constraint(db: Session, user_id: int, constraint_data: schemas.ConstraintCreate):
    constraint = models.Constraint(
        user_id=user_id,
        constraint_type=constraint_data.constraint_type,
        constraint_value=constraint_data.constraint_value,
    )
    db.add(constraint)
    db.commit()
    db.refresh(constraint)
    return constraint


def get_diet_plans(db: Session, user_id: int):
    return (
        db.query(models.DietPlan)
        .filter(models.DietPlan.user_id == user_id)
        .order_by(models.DietPlan.created_at.desc())
        .all()
    )


def create_diet_plan(db: Session, user_id: int, plan_data: schemas.DietPlanCreate):
    plan = models.DietPlan(
        user_id=user_id,
        plan_details=plan_data.plan_details,
    )
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan
