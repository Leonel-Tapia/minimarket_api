# Ruta: app/services/proveedores_comprasdetalle_historial_service.py

from sqlalchemy.orm import Session
from datetime import datetime
from app.models import ProveedoresComprasDetalle, ProveedoresComprasDetalleHistorial

# 📝 Registrar cambio antes de editar
def registrar_cambio(id_detalle: int, motivo: str, usuario: str, db: Session):
    original = db.query(ProveedoresComprasDetalle).filter_by(id_detalle=id_detalle).first()
    if not original:
        return None

    historial = ProveedoresComprasDetalleHistorial(
        id_detalle=id_detalle,
        id_compra=original.id_compra,
        id_producto=original.id_producto,
        cantidad=original.cantidad,
        precio_unitario=original.precio_unitario,
        subtotal=original.subtotal,
        motivo=motivo,
        registrado_por=usuario,
        registrado_en=datetime.now()
    )
    db.add(historial)
    db.commit()
    db.refresh(historial)
    return historial

# 📋 Consultar historial por detalle
def consultar_historial_detalle(id_detalle: int, db: Session):
    return db.query(ProveedoresComprasDetalleHistorial).filter_by(id_detalle=id_detalle).all()

# 📋 Consultar historial por compra
def consultar_historial_compra(id_compra: int, db: Session):
    return db.query(ProveedoresComprasDetalleHistorial).filter_by(id_compra=id_compra).all()
