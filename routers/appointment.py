from fastapi import APIRouter, HTTPException, Path, Depends
from sqlmodel import select, Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timezone
from typing import List

from core.security import get_current_user
from db.database import get_session  

from models.appointment import Appointment
from models.client import Client
from models.service import Service
from models.user import User
from schemas.appointment import AppointmentCreate, AppointmentRead, AppointmentUpdate

router = APIRouter(
    prefix="/appointments",
    tags=["appointments"]
)

# ---------------- CREATE ----------------
@router.post("/", response_model=AppointmentRead)
def create_appointment(
    appointment: AppointmentCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # Validación fecha en UTC
    appointment_date = appointment.appointment_date.replace(tzinfo=timezone.utc)
    if appointment_date < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="No puedes crear citas en el pasado")

    client = session.get(Client, appointment.client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Clienta no encontrada")

    # Evitar doble reserva global
    existing_appointment = session.exec(
        select(Appointment).where(Appointment.appointment_date == appointment.appointment_date)
    ).first()
    if existing_appointment:
        raise HTTPException(status_code=400, detail="Ya existe una cita en ese horario")

    # Evitar doble reserva para la clienta
    existing_appointment = session.exec(
        select(Appointment).where(
            Appointment.client_id == appointment.client_id,
            Appointment.appointment_date == appointment.appointment_date
        )
    ).first()
    if existing_appointment:
        raise HTTPException(status_code=400, detail="La clienta ya tiene una cita en este horario")

    db_appointment = Appointment(
        appointment_date=appointment_date,
        notes=appointment.notes,
        client_id=appointment.client_id
    )

    # Agregar al session antes de relacionar servicios
    session.add(db_appointment)

    # Agregar servicios relacionados
    for service_id in appointment.service_ids:
        service = session.get(Service, service_id)
        if not service:
            raise HTTPException(status_code=404, detail=f"Servicio {service_id} no encontrado")
        db_appointment.services.append(service)

    try:
        session.commit()
        session.refresh(db_appointment)
        return db_appointment
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Error creando cita: {str(e)}")

# ---------------- UPDATE ----------------
@router.put("/{appointment_id}", response_model=AppointmentRead)
def update_appointment(
    appointment_id: int = Path(..., gt=0),
    appointment_update: AppointmentUpdate = None,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    if appointment_update is None:
        raise HTTPException(status_code=400, detail="No hay datos para actualizar")

    db_appointment = session.get(Appointment, appointment_id)
    if not db_appointment:
        raise HTTPException(status_code=404, detail="Cita no encontrada")

    # Actualizar fecha con validación UTC
    if appointment_update.appointment_date:
        appointment_date = appointment_update.appointment_date.replace(tzinfo=timezone.utc)
        if appointment_date < datetime.now(timezone.utc):
            raise HTTPException(status_code=400, detail="No se puede asignar fecha pasada")
        db_appointment.appointment_date = appointment_date

    # Actualizar campos simples excepto appointment_date y service_ids
    for key, value in appointment_update.dict(exclude_unset=True).items():
        if key not in ["appointment_date", "service_ids"]:
            setattr(db_appointment, key, value)

    # Actualizar servicios
    if appointment_update.service_ids is not None:
        db_appointment.services.clear()
        for service_id in appointment_update.service_ids:
            service = session.get(Service, service_id)
            if not service:
                raise HTTPException(status_code=404, detail=f"Servicio {service_id} no encontrado")
            db_appointment.services.append(service)

    try:
        session.add(db_appointment)
        session.commit()
        session.refresh(db_appointment)
        return db_appointment
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Error actualizando cita: {str(e)}")

# ---------------- SOFT DELETE ----------------
@router.delete("/{appointment_id}", status_code=204)
def soft_delete_appointment(
    appointment_id: int = Path(..., gt=0),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    appointment = session.get(Appointment, appointment_id)
    if not appointment or not appointment.is_active:
        raise HTTPException(status_code=404, detail="Cita no encontrada o ya eliminada")

    # Soft delete
    appointment.is_active = False

    try:
        session.add(appointment)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Error eliminando cita: {str(e)}")

# ---------------- LIST ----------------
@router.get("/", response_model=List[AppointmentRead])
def list_appointments(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):

    # Filtrar solo citas activas
    appointments = session.exec(select(Appointment).where(Appointment.is_active == True)).all()

    results = []
    for appointment in appointments:
        total = sum(service.price for service in appointment.services)
        paid = sum(payment.amount for payment in appointment.payments)
        balance = total - paid
        results.append({
            **appointment.dict(),
            "services": appointment.services,
            "payments": appointment.payments,
            "total": total,
            "paid": paid,
            "balance": balance
        })
    return results

@router.get( "/{client_id}/appointments", response_model=List[AppointmentRead])
def get_client_appointments(
    client_id: int = Path(..., gt=0),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):

    client = session.get(
        Client,
        client_id
    )

    if not client:

        raise HTTPException(
            status_code=404,
            detail="Clienta no encontrada"
        )

    appointments = session.exec(

        select(Appointment).where(
            Appointment.client_id == client_id,
            Appointment.is_active == True
        )

    ).all()

    results = []

    for appointment in appointments:

        total = sum(
            service.price
            for service in appointment.services
        )

        paid = sum(
            payment.amount
            for payment in appointment.payments
        )

        balance = total - paid

        results.append({
            **appointment.dict(),
            "services": appointment.services,
            "payments": appointment.payments,
            "total": total,
            "paid": paid,
            "balance": balance
        })

    return results