from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.db_connection import get_db
from app.models.usuario import Usuario
from app.auth_utils import generar_token, verificar_password
from app.auditoria import registrar_entrada

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

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

    # Devolver token y username como "nombre"
    return JSONResponse(content={
        "access_token": token,
        "token_type": "bearer",
        "nombre": user.username  # ✅ Aquí se usa el username
    })

@router.get("/login", response_class=HTMLResponse)
def mostrar_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})
