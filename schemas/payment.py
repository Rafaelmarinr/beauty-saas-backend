from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PaymentBase(BaseModel):

    amount: float

    payment_method: str

    notes: Optional[str] = None


class PaymentCreate(PaymentBase):

    appointment_id: int


class PaymentUpdate(BaseModel):

    amount: Optional[float] = None

    payment_method: Optional[str] = None

    notes: Optional[str] = None


class PaymentRead(PaymentBase):

    id: int

    created_at: datetime

    appointment_id: int

class PaymentSimple(BaseModel):

    id: int

    amount: float

    payment_method: str