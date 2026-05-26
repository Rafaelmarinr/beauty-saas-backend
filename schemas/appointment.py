from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from typing import List

from schemas.service import ServiceSimple
from schemas.payment import PaymentSimple

class AppointmentBase(BaseModel):
    appointment_date: datetime
    notes: Optional[str] = None
    client_id: int


class AppointmentCreate(AppointmentBase):
    service_ids: List[int] = []


class AppointmentUpdate(BaseModel):
    appointment_date: Optional[datetime] = None
    status: Optional[str] = None
    notes: Optional[str] = None
    service_ids: Optional[List[int]] = None

class AppointmentRead(BaseModel):
    id: int
    status: str
    appointment_date: datetime
    notes: Optional[str] = None
    client_id: int
    services: List[ServiceSimple] = []
    payments: List[PaymentSimple] = []
    
    total: Optional[float] = None
    paid: Optional[float] = None
    balance: Optional[float] = None

class AppointmentServicesUpdate(BaseModel):
    service_ids: List[int]