from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone

from sqlmodel import Relationship
from typing import List

from models.appointment_service_link import (
    AppointmentServiceLink
)

class Service(SQLModel, table=True):
    __tablename__ = "services"

    id: Optional[int] = Field(
        default=None,
        primary_key=True
    )

    name: str = Field(index=True)

    description: Optional[str] = None

    price: float

    duration_minutes: int

    is_active: bool = True

    created_at: datetime = Field(
        default_factory=lambda:
        datetime.now(timezone.utc)
    )

    appointments: List["Appointment"] = Relationship(
    back_populates="services",
    link_model=AppointmentServiceLink
    )