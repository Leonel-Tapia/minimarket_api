# Ruta: minimarket_api/app/models/empresa.py
from sqlalchemy import Column, Integer, String, Boolean, Float, Text
from app.database.db_connection import Base

class Empresa(Base):
    __tablename__ = "empresa"

    id = Column(Integer, primary_key=True, index=True)
    nombre_comercial = Column(String, nullable=False)
    razon_social = Column(String, nullable=False)
    rfc = Column(String, nullable=False)
    giro = Column(String)
    direccion = Column(String)
    colonia = Column(String)
    ciudad = Column(String)
    estado = Column(String)
    codigo_postal = Column(String)
    telefono_principal = Column(String)
    email_principal = Column(String)
    contacto_nombre = Column(String)
    contacto_telefono = Column(String)
    contacto_email = Column(String)
    notas = Column(Text)
    aviso_factura = Column(Boolean, default=False)
    ventas_tax_general = Column(Float, default=0.0)
