from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime, timezone

class Client(SQLModel, table=True):
    __tablename__ = "clients"

    id: Optional[int] = Field(default=None, primary_key=True)

    name: str
    phone: str

    email: Optional[str] = Field(
        default=None,
        sa_column_kwargs={"unique": True}
    )

    notes: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)

    created_at: datetime = Field(
    default_factory=lambda:
    datetime.now(timezone.utc)
    )

    appointments: List["Appointment"] = Relationship(
    back_populates="client"
)