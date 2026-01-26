from fastapi import APIRouter, HTTPException
from schemas.login_schema import LoginSchema
from utils.jwt_handler import crear_token

router = APIRouter()

def validar_usuario(datos: LoginSchema):
    if datos.username == "admin" and datos.password == "1234":
        return {"username": datos.username}
    return None

@router.post("/auth/login")
def login(datos: LoginSchema):  # 👈 Este parámetro debe ir directo, sin Depends ni Body
    usuario = validar_usuario(datos)
    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    token = crear_token({"sub": usuario["username"]})
    return {
        "access_token": token,
        "token_type": "bearer"
    }
