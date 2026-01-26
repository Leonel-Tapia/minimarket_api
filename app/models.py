# Ruta: minimarket_api/app/models.py
from sqlalchemy import Column, Integer, String
from app.database.db_connection import Base


class Proveedores(Base):
    __tablename__ = "proveedores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    ruc = Column(String)
    direccion = Column(String)
    telefono = Column(String)
    email = Column(String)
    contacto_nombre = Column(String)
    contacto_telefono = Column(String)
    contacto_email = Column(String)
    estado = Column(String)
