from datetime import datetime, timedelta
from jose import JWTError, jwt

# Clave secreta y algoritmo
SECRET_KEY = "tu_clave_secreta_segura"
ALGORITHM = "HS256"
EXPIRACION_MINUTOS = 60

def crear_token(datos: dict):
    datos_a_codificar = datos.copy()
    expiracion = datetime.utcnow() + timedelta(minutes=EXPIRACION_MINUTOS)
    datos_a_codificar.update({"exp": expiracion})
    token_jwt = jwt.encode(datos_a_codificar, SECRET_KEY, algorithm=ALGORITHM)
    return token_jwt

def verificar_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
