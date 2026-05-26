from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ServiceBase(BaseModel):

    name: str

    description: Optional[str] = None

    price: float

    duration_minutes: int


class ServiceCreate(ServiceBase):
    pass


class ServiceUpdate(BaseModel):

    name: Optional[str] = None

    description: Optional[str] = None

    price: Optional[float] = None

    duration_minutes: Optional[int] = None

    is_active: Optional[bool] = None


class ServiceRead(ServiceBase):

    id: int

    is_active: bool

    created_at: datetime

class ServiceSimple(BaseModel):

    id: int

    name: str

    price: float