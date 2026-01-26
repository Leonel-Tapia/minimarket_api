from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from decimal import Decimal
from app.database.db_connection import Base
from app.models.proveedores import Proveedores
from app.productos.models.producto_model import Producto

class CompraProveedor(Base):
    __tablename__ = "proveedores_compras"

    id_compra = Column(Integer, primary_key=True, index=True)
    id_proveedor = Column(Integer, ForeignKey("proveedores.id"), nullable=False)
    fecha_compra = Column(Date, nullable=False)
    numero_factura = Column(String, nullable=False)

    # Campos monetarios con Decimal
    total_compra = Column(Numeric(10, 2, asdecimal=True), default=Decimal("0.00"))
    estado = Column(String, default="pendiente")
    impuesto = Column(Numeric(10, 2, asdecimal=True), default=Decimal("0.00"))
    envio = Column(Numeric(10, 2, asdecimal=True), default=Decimal("0.00"))
    notas = Column(String, nullable=True)

    # Relaciones
    proveedor = relationship("Proveedores", backref="compras")
    detalles = relationship("CompraDetalle", backref="compra")

class CompraDetalle(Base):
    __tablename__ = "proveedores_comprasdetalle"

    id_detalle = Column(Integer, primary_key=True, index=True)
    id_compra = Column(Integer, ForeignKey("proveedores_compras.id_compra"), nullable=False)
    id_producto = Column(Integer, ForeignKey("productos.id"), nullable=False)

    # Campos numéricos con Decimal
    cantidad = Column(Numeric(10, 2, asdecimal=True), nullable=False)
    precio_unitario = Column(Numeric(10, 2, asdecimal=True), nullable=False)

    # Relación con producto
    producto = relationship("Producto", backref="detalles_compra")