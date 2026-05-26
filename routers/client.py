from fastapi import APIRouter, Depends, HTTPException, Path
from sqlmodel import select, Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from typing import List

from core.security import get_current_user
from db.database import get_session  

from models.client import Client
from models.appointment import Appointment
from models.user import User
from schemas.client import ClientCreate, ClientRead, ClientUpdate
from schemas.appointment import AppointmentRead

router = APIRouter(prefix="/clients", tags=["clients"])

# ---------------- CREATE ----------------
@router.post("/", response_model=ClientRead)
def create_client(
    client: ClientCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    db_client = Client.from_orm(client)

    try:
        session.add(db_client)
        session.commit()
        session.refresh(db_client)
        return db_client
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="El correo ya existe")
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Error al guardar clienta: {str(e)}")

# ---------------- LIST ----------------
@router.get("/", response_model=List[ClientRead])
def list_clients(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    clients = session.exec(select(Client)).all()
    return clients

# ---------------- UPDATE ----------------
@router.put("/{client_id}", response_model=ClientRead)
def update_client(
    client_id: int = Path(..., description="ID de la clienta a actualizar"),
    client_update: ClientUpdate = None,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    db_client = session.get(Client, client_id)
    if not db_client:
        raise HTTPException(status_code=404, detail="Clienta no encontrada")

    # Actualizar solo los campos enviados
    for key, value in client_update.dict(exclude_unset=True).items():
        setattr(db_client, key, value)

    try:
        session.add(db_client)
        session.commit()
        session.refresh(db_client)
        return db_client
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="El correo ya existe")
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Error al actualizar clienta: {str(e)}")

# ---------------- SOFT DELETE ----------------
@router.delete("/{client_id}", status_code=204)
def soft_delete_client(
    client_id: int = Path(..., description="ID de la clienta a eliminar"),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    db_client = session.get(Client, client_id)
    if not db_client:
        raise HTTPException(status_code=404, detail="Clienta no encontrada")

    db_client.is_active = False

    try:
        session.add(db_client)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Error al eliminar clienta: {str(e)}")

# ---------------- GET APPOINTMENTS ----------------
@router.get("/{client_id}/appointments", response_model=List[AppointmentRead])
def get_client_appointments(
    client_id: int = Path(..., gt=0),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    client = session.get(Client, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Clienta no encontrada")

    # Filtrar solo citas activas si aplicamos soft delete
    appointments = session.exec(
        select(Appointment).where(
            Appointment.client_id == client_id,
            Appointment.is_active == True 
        )
    ).all()

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