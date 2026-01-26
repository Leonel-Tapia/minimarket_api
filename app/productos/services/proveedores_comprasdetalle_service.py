# Ruta: app/services/proveedores_comprasdetalle_service.py

from sqlalchemy.orm import Session
from datetime import datetime
from app.models import ProveedoresComprasDetalle, Productos

# 📋 Listar detalles de una compra
def listar_detalles(id_compra: int, db: Session):
    detalles = (
        db.query(ProveedoresComprasDetalle, Productos.codigo_parte, Productos.descripcion)
        .join(Productos, ProveedoresComprasDetalle.id_producto == Productos.id)
        .filter(ProveedoresComprasDetalle.id_compra == id_compra)
        .all()
    )
    return detalles

# ➕ Agregar un nuevo detalle
def agregar_detalle(id_compra: int, id_producto: int, cantidad: float,
                    precio_unitario: float, usuario: str, db: Session):
    subtotal = cantidad * precio_unitario
    nuevo_detalle = ProveedoresComprasDetalle(
        id_compra=id_compra,
        id_producto=id_producto,
        cantidad=cantidad,
        precio_unitario=precio_unitario,
        subtotal=subtotal,
        creado_por=usuario,
        creado_en=datetime.now(),
        estado="activo"
    )
    db.add(nuevo_detalle)
    db.commit()
    db.refresh(nuevo_detalle)
    return nuevo_detalle

# ✏️ Editar un detalle existente
def editar_detalle(id_detalle: int, id_producto: int, cantidad: float,
                   precio_unitario: float, usuario: str, db: Session):
    detalle = db.query(ProveedoresComprasDetalle).filter(
        ProveedoresComprasDetalle.id_detalle == id_detalle
    ).first()

    if detalle:
        detalle.id_producto = id_producto
        detalle.cantidad = cantidad
        detalle.precio_unitario = precio_unitario
        detalle.subtotal = cantidad * precio_unitario
        detalle.actualizado_por = usuario
        detalle.actualizado_en = datetime.now()
        db.commit()
        db.refresh(detalle)
        return detalle
    return None

# 🗑️ Eliminar un detalle
def eliminar_detalle(id_detalle: int, db: Session):
    detalle = db.query(ProveedoresComprasDetalle).filter(
        ProveedoresComprasDetalle.id_detalle == id_detalle
    ).first()

    if detalle:
        db.delete(detalle)
        db.commit()
        return True
    return False

# 🧮 Calcular totales extendidos
def calcular_totales(id_compra: int, db: Session):
    detalles = db.query(ProveedoresComprasDetalle).filter(
        ProveedoresComprasDetalle.id_compra == id_compra
    ).all()

    total = sum([d.subtotal for d in detalles])
    total_items = sum([d.cantidad for d in detalles])
    return {"total": total, "total_items": total_items}
