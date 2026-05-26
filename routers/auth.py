from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from fastapi.security import OAuth2PasswordRequestForm

from db.database import get_session
from models.user import User
from schemas.user import UserCreate, UserRead
from core.security import hash_password, verify_password, create_access_token

from core.security import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

# ---------------- REGISTER ----------------
@router.post("/register", response_model=UserRead)
def register(user: UserCreate, session: Session = Depends(get_session)):
    existing_user = session.exec(select(User).where(User.email == user.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    
    # crear usuario con password hasheada
    db_user = User(
        email=user.email,
        hashed_password=hash_password(user.password),
        is_active=True
    )
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    
    return db_user

# ---------------- LOGIN ----------------
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    token = create_access_token({"sub": str(user.id), "email": user.email})
    return {"access_token": token, "token_type": "bearer"}

# ------------------- Obtiene usuario autenticado ---------------------
@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_user)
):

    return {
        "id": current_user.id,
        "email": current_user.email,
        "is_admin": current_user.is_admin
    }