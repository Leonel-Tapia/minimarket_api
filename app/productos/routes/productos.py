# 📁 Ruta: app/productos/routes/productos.py

from fastapi import APIRouter, Depends, HTTPException, status, Request, Path
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.productos.schemas.producto_schema import ProductoCreate, ProductoUpdate, ProductoOut
from app.productos.services.producto_service import (
    crear_producto,
    obtener_producto_por_id,
    editar_producto,
    inactivar_producto,
    obtener_productos_activos
)
from app.database.db_connection import get_db

router = APIRouter(prefix="/productos", tags=["Productos"])
templates = Jinja2Templates(directory="app/templates")

# 📝 Formulario para nuevo producto
@router.get("/nuevo", response_class=HTMLResponse)
async def mostrar_formulario_nuevo_producto(request: Request):
    return templates.TemplateResponse("productos/nuevo_producto.html", {"request": request})

@router.post("/nuevo", response_class=HTMLResponse)
async def procesar_formulario_nuevo_producto(request: Request):
    form = await request.form()

    try:
        datos = {
            "codigo_parte": form.get("codigo_parte"),
            "codigo_barras": form.get("codigo_barras"),
            "descripcion": form.get("descripcion"),
            "notas": form.get("notas"),
            "precio_venta": float(form.get("precio_venta") or 0),
            "costo": float(form.get("costo") or 0),
            "stock_minimo": int(form.get("stock_minimo") or 0),
            "fecha_vigencia": form.get("fecha_vigencia"),
            "proveedor": form.get("proveedor"),
            "tipo_producto": form.get("tipo_producto"),
            "imagen": form.get("imagen"),
            "categoria": form.get("categoria"),
            "unidad_medida": form.get("unidad_medida"),
            "ubicacion": form.get("ubicacion"),
            "ventas_tax": float(form.get("ventas_tax") or 0),
            "inactivo": False,
            "creado_por": "admin"
        }

        db = next(get_db())
        crear_producto(db, datos, usuario=datos["creado_por"])

        return templates.TemplateResponse("productos/nuevo_producto.html", {
            "request": request,
            "mensaje": "✅ Producto registrado correctamente."
        })

    except ValueError as e:
        return templates.TemplateResponse("productos/nuevo_producto.html", {
            "request": request,
            "mensaje": f"⚠️ {str(e)}"
        })

    except Exception as e:
        return templates.TemplateResponse("productos/nuevo_producto.html", {
            "request": request,
            "mensaje": f"❌ Error al registrar producto: {str(e)}"
        })

# ✏️ Formulario para editar producto
@router.get("/editar/{producto_id}", response_class=HTMLResponse)
async def formulario_editar_producto(request: Request, producto_id: int = Path(...)):
    db: Session = next(get_db())
    producto = obtener_producto_por_id(db, producto_id)
    if not producto:
        return JSONResponse(status_code=404, content={"error": "Producto no encontrado"})
    return templates.TemplateResponse("productos/editar_producto.html", {
        "request": request,
        "producto": producto
    })

@router.post("/actualizar/{producto_id}", response_class=HTMLResponse)
async def actualizar_producto(request: Request, producto_id: int):
    form = await request.form()

    try:
        cambios = {
            "descripcion": form.get("descripcion"),
            "precio_venta": float(form.get("precio_venta") or 0),
            "notas": form.get("notas"),
            "inactivo": form.get("inactivo") == "on"
        }

        db = next(get_db())
        producto = editar_producto(db, producto_id, cambios)

        if not producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado")

        return templates.TemplateResponse("productos/editar_producto.html", {
            "request": request,
            "producto": producto,
            "mensaje": "✅ Cambios guardados correctamente."
        })

    except Exception as e:
        db = next(get_db())
        producto = obtener_producto_por_id(db, producto_id)
        return templates.TemplateResponse("productos/editar_producto.html", {
            "request": request,
            "producto": producto,
            "mensaje": f"❌ Error al guardar cambios: {str(e)}"
        })

# 📦 Rutas API
@router.post("/", response_model=ProductoOut, status_code=status.HTTP_201_CREATED)
def crear(datos: ProductoCreate, db: Session = Depends(get_db)):
    return crear_producto(db, datos, usuario="admin")

@router.get("/{producto_id}", response_model=ProductoOut)
def obtener_por_id(producto_id: int, db: Session = Depends(get_db)):
    producto = obtener_producto_por_id(db, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@router.put("/{producto_id}", response_model=ProductoOut)
def editar(producto_id: int, cambios: ProductoUpdate, db: Session = Depends(get_db)):
    producto = editar_producto(db, producto_id, cambios)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@router.patch("/{producto_id}/inactivar", response_model=ProductoOut)
def inactivar(producto_id: int, db: Session = Depends(get_db)):
    producto = inactivar_producto(db, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@router.get("/", response_model=list[ProductoOut])
def listar_activos(db: Session = Depends(get_db)):
    return obtener_productos_activos(db)

# 📋 Mostrar catálogo de productos con botones por fila
@router.get("/catalogo", response_class=HTMLResponse)
async def mostrar_catalogo_productos(request: Request):
    db = next(get_db())
    productos = obtener_productos_activos(db)
    return templates.TemplateResponse("productos/catalogo_productos.html", {
        "request": request,
        "productos": productos
    })
