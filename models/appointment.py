from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from models.client import Client

from models.appointment_service_link import(
    AppointmentServiceLink
)

class Appointment(SQLModel, table=True):
    __tablename__ = "appointments"

    id: Optional[int] = Field(default=None, primary_key=True)

    appointment_date: datetime
    status: str = Field(default="pending")
    notes: Optional[str] = None

    client_id: int = Field(foreign_key="clients.id")

    client: Optional["Client"] = Relationship(back_populates="appointments")

    is_active: bool = Field(default=True)

    services: list["Service"] = Relationship(
        back_populates="appointments",
        link_model=AppointmentServiceLink
    )
    
    payments: list["Payment"] = Relationship(
        back_populates="appointment"
    )