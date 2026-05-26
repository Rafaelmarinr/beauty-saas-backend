from sqlmodel import (
    SQLModel,
    Field,
    Relationship
)

from typing import Optional
from datetime import datetime, timezone


class Payment(SQLModel, table=True):

    __tablename__ = "payments"

    id: Optional[int] = Field(
        default=None,
        primary_key=True
    )

    amount: float

    payment_method: str

    notes: Optional[str] = None

    created_at: datetime = Field(
        default_factory=lambda:
        datetime.now(timezone.utc)
    )

    appointment_id: int = Field(
        foreign_key="appointments.id"
    )

    appointment: Optional["Appointment"] = Relationship(
        back_populates="payments"
    )