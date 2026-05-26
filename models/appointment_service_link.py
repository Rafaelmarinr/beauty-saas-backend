from sqlmodel import SQLModel, Field
from typing import Optional


class AppointmentServiceLink(SQLModel, table=True):

    __tablename__ = "appointment_service_links"

    appointment_id: Optional[int] = Field(
        default=None,
        foreign_key="appointments.id",
        primary_key=True
    )

    service_id: Optional[int] = Field(
        default=None,
        foreign_key="services.id",
        primary_key=True
    )