from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime

from app.database.db_connection import get_db
from app.models.usuario import Usuario
from app.models.auditoria import Auditoria
from app.auth_utils import generar_token, verificar_password

router = APIRouter()

def registrar_entrada(db: Session, username: str):
    entrada = Auditoria(
        usuario=username,
        accion="login",
        timestamp=datetime.now()
    )
    db.add(entrada)
    db.commit()

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.username == form_data.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado"
        )

    if not verificar_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Contraseña incorrecta"
        )

    # Registrar entrada en auditoría
    registrar_entrada(db, user.username)

    # Generar token
    token = generar_token(user)

    return {
        "access_token": token,
        "token_type": "bearer"
    }
