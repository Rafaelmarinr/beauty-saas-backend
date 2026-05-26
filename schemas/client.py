from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class ClientCreate(BaseModel):
    name: str
    phone: str
    email: Optional[EmailStr] = None
    notes: Optional[str] = None

class ClientRead(ClientCreate):
    id: int
    created_at: datetime

class ClientUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    notes: Optional[str] = None