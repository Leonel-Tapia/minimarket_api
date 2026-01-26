from jose import jwt
from datetime import datetime, timedelta

# 🔐 Configuración del token
SECRET_KEY = "clave_super_secreta"  # Cámbiala por una más segura en producción
ALGORITHM = "HS256"
EXPIRATION_MINUTES = 60

# 🎟️ Generar token JWT
def create_access_token(data: dict):
    data_copy = data.copy()
    expiration = datetime.utcnow() + timedelta(minutes=EXPIRATION_MINUTES)
    data_copy.update({"exp": expiration})
    token = jwt.encode(data_copy, SECRET_KEY, algorithm=ALGORITHM)
    return token

# 🔍 Verificar token JWT
def verify_token(token: str):
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return data
    except jwt.JWTError:
        return None
