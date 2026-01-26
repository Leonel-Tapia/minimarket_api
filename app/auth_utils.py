from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from app.models.usuario import Usuario

# Configuración del token
SECRET_KEY = "1961"  # ⚠️ Cámbiala por una clave segura en producción
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Contexto para encriptar/verificar contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generar_token(usuario: Usuario):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": usuario.username,
        "rol": usuario.rol,
        "exp": expire
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verificar_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)
