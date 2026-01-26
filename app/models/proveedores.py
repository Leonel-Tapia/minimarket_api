from sqlalchemy import Column, Integer, String, Boolean
from app.database.db_connection import Base

class Proveedores(Base):
    __tablename__ = "proveedores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    ruc = Column(String, nullable=False)
    direccion = Column(String)
    telefono = Column(String)
    email = Column(String)
    contacto_nombre = Column(String)
    contacto_telefono = Column(String)
    contacto_email = Column(String)
    estado = Column(Boolean, default=True)
    notas = Column(String)
