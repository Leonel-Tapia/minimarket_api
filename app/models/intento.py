from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base
from datetime import datetime

class Intento(Base):
    __tablename__ = "intentos"

    id = Column(Integer, primary_key=True, index=True)
    usuario = Column(String(50), nullable=False)
    tipo = Column(String(30), nullable=False)       # "login", "modulo", "prueba"
    resultado = Column(String(20), nullable=False)   # "exitoso", "fallido"
    descripcion = Column(String(255), nullable=True) # Detalles opcionales
    timestamp = Column(DateTime, default=datetime.now, nullable=False)
