from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    login_id: str = Field(..., min_length=3, max_length=50)
    name: str = Field(..., min_length=2, max_length=100)
    email: str = Field(..., max_length=255)
    password: str = Field(..., min_length=6)
    phone_number: Optional[str] = Field(default=None, max_length=30)
    gender: Optional[str] = Field(default=None, pattern=r"^(M|F)$")


class UserLogin(BaseModel):
    login_id: str
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    email: Optional[str] = Field(default=None, max_length=255)
    phone_number: Optional[str] = Field(default=None, max_length=30)
    gender: Optional[str] = Field(default=None, pattern=r"^(M|F)$")


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    login_id: str
    name: str
    email: str
    phone_number: Optional[str] = None
    gender: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class ProfileCreate(BaseModel):
    nickname: Optional[str] = Field(default=None, max_length=50)
    profile_image_url: Optional[str] = Field(default=None, max_length=255)
    introduction: Optional[str] = None


class ProfileResponse(ProfileCreate):
    model_config = ConfigDict(from_attributes=True)

    profile_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime


class HealthMetricCreate(BaseModel):
    height: float = Field(..., ge=0)
    weight: float = Field(..., ge=0)


class HealthMetricResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    metric_id: int
    user_id: int
    height: float
    weight: float
    measured_at: datetime


class ConstraintCreate(BaseModel):
    constraint_type: str = Field(..., min_length=1, max_length=50)
    constraint_value: str = Field(..., min_length=1, max_length=100)


class ConstraintResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    constraint_id: int
    user_id: int
    constraint_type: str
    constraint_value: str
    created_at: datetime


class DietPlanCreate(BaseModel):
    plan_details: dict


class DietPlanResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    plan_id: int
    user_id: int
    plan_details: dict
    created_at: datetime
    updated_at: datetime
