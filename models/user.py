from sqlmodel import SQLModel, Field
from typing import Optional

class User(SQLModel, table=True):

    __tablename__ = "users"

    id: Optional[int] = Field(
        default=None,
        primary_key=True
    )

    email: str = Field(
        unique=True,
        index=True
    )

    hashed_password: str

    is_active: bool = Field(default=True)

    is_admin: bool = Field(default=False)