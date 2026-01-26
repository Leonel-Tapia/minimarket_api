from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from app.database.db_connection import get_db
from app.services import proveedores_edit_purchase_service as service
from app.models.proveedores_compraseditar import CompraProveedor, CompraDetalle
from app.productos.models.producto_model import Producto

from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# 👉 Ruta para mostrar el formulario de edición
@router.get("/proveedores/compras/{id_compra}/editar", response_class=HTMLResponse)
def editar_compra(request: Request, id_compra: int, db: Session = Depends(get_db)):
    compra = service.get_compra_by_id(id_compra, db)
    if not compra:
        return HTMLResponse(content="❌ Compra no encontrada", status_code=404)

    detalles = db.query(CompraDetalle).filter(CompraDetalle.id_compra == id_compra).all()
    productos = db.query(Producto).all()

    return templates.TemplateResponse(
        "compras/proveedores_compraseditar.html",
        {
            "request": request,
            "compra": compra,
            "detalles": detalles,
            "productos": productos,
        },
    )

# 👉 Ruta para procesar la edición (POST)
@router.post("/proveedores/compras/{id_compra}/editar")
async def actualizar_compra(
    request: Request,
    id_compra: int,
    db: Session = Depends(get_db),
    fecha_compra: str = Form(...),
    numero_factura: str = Form(...),
    estado: str = Form(...),
    total_compra: float = Form(...),
    impuesto: float = Form(...),
    envio: float = Form(...),
    notas: str = Form(None),
):
    data = {
        "fecha": fecha_compra,
        "documento": numero_factura,
        "estado": estado,
        "total": total_compra,
        "impuesto": impuesto,
        "envio": envio,
        "notas": notas,
    }

    # ✅ corregido: await para obtener el formulario
    form_data = await request.form()

    service.update_compra(id_compra, data, db)
    service.update_detalles(id_compra, dict(form_data), db)
    service.recomputar_total_compra(id_compra, db)

    compra = service.get_compra_by_id(id_compra, db)
    return RedirectResponse(
        url=f"/proveedores/{compra.id_proveedor}/dashboard",
        status_code=303,
    )

# 👉 Ruta para borrar un detalle
@router.post("/proveedores/compras/detalle/{id_detalle}/borrar")
def borrar_detalle(id_detalle: int, db: Session = Depends(get_db)):
    ok = service.borrar_detalle(id_detalle, db)
    if ok:
        return {"status": "ok"}
    return {"status": "error", "message": "No se pudo borrar el detalle"}