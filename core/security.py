from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException
from jose import jwt, JWTError

from passlib.context import CryptContext

from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from db.database import get_session
from models.user import User

# 🔹 clave secreta para firmar JWT
SECRET_KEY = "SUPER_SECRET_KEY"

# 🔹 algoritmo de firma
ALGORITHM = "HS256"

# 🔹 duración del token en minutos
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# 🔹 contexto para hashing de contraseñas con bcrypt
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# ---------------- HASH PASSWORD ----------------
# Convierte contraseña en hash seguro
def hash_password(password: str):
    return pwd_context.hash(password)

# ---------------- VERIFY PASSWORD ----------------
# Verifica que la contraseña ingresada coincida con el hash guardado
def verify_password(
    plain_password: str,
    hashed_password: str
):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )

# ---------------- CREATE TOKEN ----------------
# Genera JWT con datos del usuario y expiración
def create_access_token(
    data: dict
):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# esquema OAuth2 para proteger endpoints con JWT
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

# ---------------- GET CURRENT USER ----------------
# Valida el token JWT y retorna el usuario autenticado
def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Token inválido"
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = session.get(User, int(user_id))
    if not user:
        raise credentials_exception

    return user

def require_admin(
    current_user: User = Depends(get_current_user)
):

    if not current_user.is_admin:

        raise HTTPException(
            status_code=403,
            detail="No autorizado"
        )

    return current_user