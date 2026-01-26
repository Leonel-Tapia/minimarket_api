from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from utils.jwt_handler import verificar_token

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def obtener_usuario_actual(token: str = Depends(oauth2_scheme)):
    datos = verificar_token(token)
    if datos is None:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
    return datos

@router.get("/dashboard")
def mostrar_dashboard(usuario: dict = Depends(obtener_usuario_actual)):
    return {"mensaje": f"Bienvenido {usuario['sub']}"}
