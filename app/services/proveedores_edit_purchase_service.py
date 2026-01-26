from sqlalchemy.orm import Session
from app.models.proveedores_compraseditar import CompraProveedor, CompraDetalle
from datetime import datetime

# Obtener una compra por ID
def get_compra_by_id(id: int, db: Session):
    return db.query(CompraProveedor).filter(CompraProveedor.id_compra == id).first()

# Actualizar datos generales de la compra
def update_compra(id: int, data: dict, db: Session):
    compra = get_compra_by_id(id, db)
    if not compra:
        return None

    compra.numero_factura = data.get("documento")
    compra.fecha_compra = data.get("fecha")
    compra.estado = data.get("estado")
    compra.total_compra = data.get("total")
    compra.impuesto = data.get("impuesto")
    compra.envio = data.get("envio")
    compra.notas = data.get("notas")

    db.commit()
    db.refresh(compra)
    return compra

# Actualizar detalles de la compra
def update_detalles(id_compra: int, form_data, db: Session):
    # Actualizar detalles existentes
    detalles = db.query(CompraDetalle).filter(CompraDetalle.id_compra == id_compra).all()

    for detalle in detalles:
        cantidad = form_data.get(f"cantidad_{detalle.id_detalle}")
        precio = form_data.get(f"precio_{detalle.id_detalle}")
        producto_id = form_data.get(f"producto_{detalle.id_detalle}")

        if cantidad is not None:
            try:
                detalle.cantidad = float(cantidad)
            except ValueError:
                pass
        if precio is not None:
            try:
                detalle.precio_unitario = float(precio)
            except ValueError:
                pass
        if producto_id is not None:
            try:
                detalle.id_producto = int(producto_id)
            except ValueError:
                pass

        detalle.actualizado_en = datetime.now()

    # Insertar nuevo detalle si existe en el formulario
    nuevo_producto = form_data.get("producto_nuevo")
    nueva_cantidad = form_data.get("cantidad_nuevo")
    nuevo_precio = form_data.get("precio_nuevo")

    if nuevo_producto and nueva_cantidad and nuevo_precio:
        try:
            nuevo_detalle = CompraDetalle(
                id_compra=id_compra,
                id_producto=int(nuevo_producto),
                cantidad=float(nueva_cantidad),
                precio_unitario=float(nuevo_precio),
            )
            db.add(nuevo_detalle)
        except ValueError:
            pass  # Ignorar si los datos no son válidos

    db.commit()

# Recalcular el total de la compra
def recomputar_total_compra(id_compra: int, db: Session):
    detalles = db.query(CompraDetalle).filter(CompraDetalle.id_compra == id_compra).all()
    total = sum(float(detalle.cantidad) * float(detalle.precio_unitario) for detalle in detalles)

    compra = get_compra_by_id(id_compra, db)
    if compra:
        compra.total_compra = total
        db.commit()

# Cancelar edición (placeholder)
def cancelar_edicion():
    pass

# Borrar un detalle de la compra
def borrar_detalle(id_detalle: int, db: Session):
    detalle = db.query(CompraDetalle).filter(CompraDetalle.id_detalle == id_detalle).first()
    if not detalle:
        return False

    db.delete(detalle)
    db.commit()
    return True