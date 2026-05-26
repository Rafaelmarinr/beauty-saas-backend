from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from sqlalchemy.exc import SQLAlchemyError

from core.security import get_current_user
from db.database import get_session 

from models.payment import Payment
from models.appointment import Appointment
from models.user import User
from schemas.payment import PaymentCreate, PaymentRead

router = APIRouter(
    prefix="/payments",
    tags=["payments"]
)

# ---------------- CREATE PAYMENT ----------------
@router.post("/", response_model=PaymentRead)
def create_payment(
    payment: PaymentCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # obtener la cita
    appointment = session.get(Appointment, payment.appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Cita no encontrada")

    # calcular total servicios
    total = sum(service.price for service in appointment.services)

    # calcular total ya pagado
    paid = sum(p.amount for p in appointment.payments)

    # validar sobrepago
    if paid + payment.amount > total:
        raise HTTPException(
            status_code=400,
            detail=f"Pago excede el total de la cita. Total: {total}, ya pagado: {paid}"
        )

    # crear objeto Payment
    db_payment = Payment(
        amount=payment.amount,
        payment_method=payment.payment_method,
        notes=payment.notes,
        appointment_id=payment.appointment_id
    )

    # actualizar balance incluyendo pago actual
    paid += payment.amount
    balance = total - paid

    if balance <= 0:
        appointment.status = "completed" 

    try:
        session.add(db_payment)
        session.add(appointment)
        session.commit()
        session.refresh(db_payment)
        return db_payment
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Error creando pago: {str(e)}"
        )