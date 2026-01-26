# Ruta: app/productos/schemas/producto_schema.py

from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class ProductoBase(BaseModel):
    codigo_parte: str
    descripcion: Optional[str] = None
    costo: float
    precio_venta: float
    categoria: Optional[str] = None
    unidad_medida: Optional[str] = None
    ubicacion: Optional[str] = None
    stock_minimo: Optional[int] = None
    proveedor: Optional[str] = None
    codigo_barras: Optional[str] = None
    tipo_producto: Optional[str] = None
    fecha_vigencia: Optional[date] = None
    notas: Optional[str] = None
    imagen: Optional[str] = None
    ventas_tax: Optional[float] = None

class ProductoCreate(ProductoBase):
    creado_por: str

class ProductoUpdate(BaseModel):
    descripcion: Optional[str] = None
    costo: Optional[float] = None
    precio_venta: Optional[float] = None
    categoria: Optional[str] = None
    unidad_medida: Optional[str] = None
    ubicacion: Optional[str] = None
    stock_minimo: Optional[int] = None
    proveedor: Optional[str] = None
    codigo_barras: Optional[str] = None
    tipo_producto: Optional[str] = None
    fecha_vigencia: Optional[date] = None
    fecha_actualizacion: Optional[datetime] = None
    inactivo: Optional[bool] = None
    notas: Optional[str] = None
    imagen: Optional[str] = None
    ventas_tax: Optional[float] = None

class ProductoOut(ProductoBase):
    id: int
    creado_por: str
    fecha_creacion: Optional[datetime] = None
    inactivo: Optional[bool] = None

    class Config:
        orm_mode = True
