from sqlalchemy.orm import Session
from app.productos.models.producto_model import Producto
from app.productos.schemas.producto_schema import ProductoCreate, ProductoUpdate

def crear_producto(db: Session, datos: dict, usuario: str):
    existe_parte = db.query(Producto).filter(Producto.codigo_parte == datos["codigo_parte"]).first()
    if existe_parte:
        raise ValueError("Ya existe un producto con ese código de parte.")

    if datos.get("codigo_barras"):
        existe_barras = db.query(Producto).filter(Producto.codigo_barras == datos["codigo_barras"]).first()
        if existe_barras:
            raise ValueError("Ya existe un producto con ese código de barras.")

    nuevo_producto = Producto(**datos)
    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)
    return nuevo_producto

def obtener_producto_por_id(db: Session, producto_id: int):
    return db.query(Producto).filter(Producto.id == producto_id).first()

def editar_producto(db: Session, producto_id: int, cambios: ProductoUpdate):
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        return None
    for campo, valor in cambios.dict(exclude_unset=True).items():
        setattr(producto, campo, valor)
    db.commit()
    db.refresh(producto)
    return producto

def inactivar_producto(db: Session, producto_id: int):
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        return None
    producto.inactivo = True
    db.commit()
    db.refresh(producto)
    return producto

def obtener_productos_activos(db: Session):
    return db.query(Producto).filter(Producto.inactivo == False).all()