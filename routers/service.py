from fastapi import APIRouter, Depends, HTTPException, Path
from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError
from typing import List

from core.security import get_current_user, require_admin
from db.database import get_session

from models.service import Service
from models.user import User
from schemas.service import ServiceCreate, ServiceRead, ServiceUpdate

router = APIRouter(
    prefix="/services",
    tags=["services"]
)

# ---------------- CREATE ----------------
@router.post("/", response_model=ServiceRead)
def create_service(
    service: ServiceCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(require_admin)
):
    db_service = Service(
        name=service.name,
        description=service.description,
        price=service.price,
        duration_minutes=service.duration_minutes
    )

    try:
        session.add(db_service)
        session.commit()
        session.refresh(db_service)
        return db_service
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Error creando servicio: {str(e)}"
        )

# ---------------- LIST ----------------
@router.get("/", response_model=List[ServiceRead])
def list_services(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # Solo traemos servicios activos (soft delete)
    services = session.exec(
        select(Service).where(Service.is_active == True)
    ).all()
    return services

# ---------------- GET ONE ----------------
@router.get("/{service_id}", response_model=ServiceRead)
def get_service(
    service_id: int = Path(..., gt=0),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    service = session.get(Service, service_id)

    # Validamos también is_active para ocultar servicios eliminados
    if not service or not service.is_active:
        raise HTTPException(
            status_code=404,
            detail="Servicio no encontrado"
        )
    return service

# ---------------- UPDATE ----------------
@router.put("/{service_id}", response_model=ServiceRead)
def update_service(
    service_update: ServiceUpdate,
    service_id: int = Path(..., gt=0),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    db_service = session.get(Service, service_id)

    # Validamos is_active para no actualizar servicios eliminados
    if not db_service or not db_service.is_active:
        raise HTTPException(
            status_code=404,
            detail="Servicio no encontrado"
        )

    for key, value in service_update.dict(exclude_unset=True).items():
        setattr(db_service, key, value)

    try:
        session.add(db_service)
        session.commit()
        session.refresh(db_service)
        return db_service
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Error actualizando servicio: {str(e)}"
        )

# ---------------- SOFT DELETE ----------------
@router.delete("/{service_id}", status_code=204)
def soft_delete_service(
    service_id: int = Path(..., gt=0),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    service = session.get(Service, service_id)

    # Validamos is_active para no "borrar" dos veces
    if not service or not service.is_active:
        raise HTTPException(
            status_code=404,
            detail="Servicio no encontrado"
        )

    # Soft delete: marcamos como inactivo
    service.is_active = False

    try:
        session.add(service)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Error eliminando servicio: {str(e)}"
        )