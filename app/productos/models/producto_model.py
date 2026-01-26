# Ruta: app/productos/models/producto.py

from sqlalchemy import Column, Integer, Text, Numeric, Boolean, Date, TIMESTAMP
from app.database.db_base import Base

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    codigo_parte = Column(Text, nullable=False)
    descripcion = Column(Text, nullable=True)
    costo = Column(Numeric, nullable=False)
    precio_venta = Column(Numeric, nullable=False)
    categoria = Column(Text, nullable=True)
    unidad_medida = Column(Text, nullable=True)
    ubicacion = Column(Text, nullable=True)
    stock_minimo = Column(Integer, nullable=True)
    proveedor = Column(Text, nullable=True)
    codigo_barras = Column(Text, nullable=True)
    tipo_producto = Column(Text, nullable=True)
    fecha_vigencia = Column(Date, nullable=True)
    fecha_actualizacion = Column(TIMESTAMP, nullable=True)
    inactivo = Column(Boolean, nullable=True)
    notas = Column(Text, nullable=True)
    imagen = Column(Text, nullable=True)
    creado_por = Column(Text, nullable=False)
    fecha_creacion = Column(TIMESTAMP, nullable=True)
    ventas_tax = Column(Numeric, nullable=True)
