from fastapi import APIRouter, Request, Form, Path
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime
from app.database.db_connection import get_db_session
from app.productos.models.producto_model import Producto

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# ✅ Mostrar catálogo de productos
@router.get("/catalogo", response_class=HTMLResponse)
async def ver_catalogo_productos(request: Request):
    db: Session = get_db_session()
    productos = db.query(Producto).all()
    return templates.TemplateResponse("productos/catalogo_productos.html", {
        "request": request,
        "productos": productos
    })

# ✅ Mostrar formulario de edición
@router.get("/productos/editar/{producto_id}", response_class=HTMLResponse)
async def formulario_editar_producto(request: Request, producto_id: int = Path(...)):
    db: Session = get_db_session()
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        productos = db.query(Producto).all()
        return templates.TemplateResponse("productos/catalogo_productos.html", {
            "request": request,
            "error": f"No se encontró el producto con ID {producto_id}",
            "productos": productos
        })
    return templates.TemplateResponse("productos/editar_producto.html", {
        "request": request,
        "producto": producto
    })

# ✅ Guardar cambios del producto editado
@router.post("/productos/actualizar/{producto_id}")
async def actualizar_producto(
    request: Request,
    producto_id: int = Path(...),
    codigo_parte: str = Form(...),
    descripcion: str = Form(...),
    costo: float = Form(...),
    precio_venta: float = Form(...),
    categoria: str = Form(""),
    unidad_medida: str = Form(""),
    ubicacion: str = Form(""),
    stock_minimo: int = Form(0),
    proveedor: str = Form(""),
    codigo_barras: str = Form(""),
    tipo_producto: str = Form(""),
    fecha_vigencia: str = Form(""),
    fecha_actualizacion: str = Form(""),
    inactivo: bool = Form(False),
    notas: str = Form(""),
    imagen: str = Form(""),
    ventas_tax: float = Form(0.0)
):
    db: Session = get_db_session()
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        productos = db.query(Producto).all()
        return templates.TemplateResponse("productos/catalogo_productos.html", {
            "request": request,
            "error": f"No se encontró el producto con ID {producto_id}",
            "productos": productos
        })

    producto.codigo_parte = codigo_parte
    producto.descripcion = descripcion
    producto.costo = costo
    producto.precio_venta = precio_venta
    producto.categoria = categoria
    producto.unidad_medida = unidad_medida
    producto.ubicacion = ubicacion
    producto.stock_minimo = stock_minimo
    producto.proveedor = proveedor
    producto.codigo_barras = codigo_barras
    producto.tipo_producto = tipo_producto
    producto.fecha_vigencia = fecha_vigencia or None
    producto.fecha_actualizacion = fecha_actualizacion or None
    producto.inactivo = inactivo
    producto.notas = notas
    producto.imagen = imagen
    producto.ventas_tax = ventas_tax

    db.commit()
    return RedirectResponse("/catalogo", status_code=303)

# ✅ Mostrar formulario para registrar nuevo producto
@router.get("/productos/nuevo", response_class=HTMLResponse)
async def nuevo_producto(request: Request):
    return templates.TemplateResponse("productos/nuevo_producto.html", {"request": request})

# ✅ Guardar nuevo producto en la base de datos
@router.post("/productos/nuevo")
async def guardar_nuevo_producto(
    request: Request,
    codigo_parte: str = Form(...),
    codigo_barras: str = Form(""),
    descripcion: str = Form(...),
    notas: str = Form(""),
    precio_venta: float = Form(...),
    costo: float = Form(0),
    stock_minimo: int = Form(...),
    fecha_vigencia: str = Form(...),
    proveedor: str = Form(""),
    tipo_producto: str = Form(""),
    imagen: str = Form(""),
    categoria: str = Form(""),
    unidad_medida: str = Form(""),
    ubicacion: str = Form(""),
    ventas_tax: float = Form(...)
):
    db: Session = get_db_session()

    nuevo_producto = Producto(
        codigo_parte=codigo_parte,
        codigo_barras=codigo_barras,
        descripcion=descripcion,
        notas=notas,
        precio_venta=precio_venta,
        costo=costo,
        stock_minimo=stock_minimo,
        fecha_vigencia=fecha_vigencia,
        proveedor=proveedor,
        tipo_producto=tipo_producto,
        imagen=imagen,
        categoria=categoria,
        unidad_medida=unidad_medida,
        ubicacion=ubicacion,
        ventas_tax=ventas_tax,
        fecha_actualizacion=datetime.now(),
        fecha_creacion=datetime.now(),
        creado_por="sistema",  # ✅ valor por defecto para evitar errores
        inactivo=False
    )

    db.add(nuevo_producto)
    db.commit()
    return RedirectResponse(url="/inventario", status_code=303)

# ✅ Inactivar producto desde el catálogo
@router.get("/productos/inactivar/{producto_id}")
async def inactivar_producto(producto_id: int):
    db: Session = get_db_session()
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if producto and not producto.inactivo:
        producto.inactivo = True
        producto.fecha_actualizacion = datetime.now()
        db.commit()
    return RedirectResponse(url="/catalogo", status_code=303)
