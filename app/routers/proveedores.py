from typing import Optional
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database.db_connection import get_db
from app.models import Proveedores
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# 📌 Catálogo de proveedores
@router.get("/proveedor/catalogo")
def catalogo_proveedores(request: Request, db: Session = Depends(get_db)):
    proveedores = db.query(Proveedores).all()
    return templates.TemplateResponse(
        "proveedores/proveedores_catalogo.html",
        {"request": request, "proveedores": proveedores}
    )

# 📌 Guardar proveedor (nuevo o editar)
@router.post("/proveedor/guardar")
def guardar_proveedor(
    id: Optional[str] = Form(None),
    nombre: str = Form(...),
    ruc: str = Form(""),
    direccion: str = Form(""),
    telefono: str = Form(...),
    email: str = Form(...),
    contacto_nombre: str = Form(""),
    contacto_telefono: str = Form(""),
    contacto_email: str = Form(""),
    estado: bool = Form(False),
    notas: str = Form(""),
    db: Session = Depends(get_db)
):
    proveedor = None
    if id and id.strip().isdigit():
        proveedor = db.query(Proveedores).filter(Proveedores.id == int(id)).first()

    if proveedor:  # 🔄 Editar proveedor existente
        proveedor.nombre = nombre
        proveedor.ruc = ruc
        proveedor.direccion = direccion
        proveedor.telefono = telefono
        proveedor.email = email
        proveedor.contacto_nombre = contacto_nombre
        proveedor.contacto_telefono = contacto_telefono
        proveedor.contacto_email = contacto_email
        proveedor.estado = estado
        proveedor.notas = notas
        db.commit()
    else:  # ➕ Crear nuevo proveedor
        nuevo = Proveedores(
            nombre=nombre,
            ruc=ruc,
            direccion=direccion,
            telefono=telefono,
            email=email,
            contacto_nombre=contacto_nombre,
            contacto_telefono=contacto_telefono,
            contacto_email=contacto_email,
            estado=True,
            notas=notas
        )
        db.add(nuevo)
        db.commit()

    return RedirectResponse(url="/proveedor/catalogo", status_code=303)

# 📌 Inactivar proveedor
@router.post("/proveedor/inactivar/{id}")
def inactivar_proveedor(id: int, db: Session = Depends(get_db)):
    proveedor = db.query(Proveedores).filter(Proveedores.id == id).first()
    if proveedor:
        proveedor.estado = False
        db.commit()
    return RedirectResponse(url="/proveedor/catalogo", status_code=303)

# 📌 Validar nombre duplicado
@router.get("/proveedor/existe_nombre")
def existe_nombre(nombre: str, db: Session = Depends(get_db)):
    proveedor = db.query(Proveedores).filter(Proveedores.nombre == nombre).first()
    return {"existe": proveedor is not None}

# 📌 Dashboard del proveedor
@router.get("/proveedores/{id}/dashboard", response_class=HTMLResponse)
def dashboard_proveedor(id: int, request: Request, db: Session = Depends(get_db)):
    proveedor = db.query(Proveedores).filter(Proveedores.id == id).first()
    if not proveedor:
        return RedirectResponse(url="/proveedor/catalogo", status_code=303)

    # 📌 Compras del proveedor
    compras = db.execute(
        text("""
            SELECT id_compra, numero_factura, fecha_compra, estado, observaciones, total_compra, total_pagado
            FROM proveedores_compras
            WHERE id_proveedor = :id
        """),
        {"id": id}
    ).fetchall()

    # 📌 Devoluciones del proveedor
    devoluciones = db.execute(
        text("""
            SELECT id_devolucion, fecha_devolucion, motivo, total_devolucion, notas
            FROM proveedores_devoluciones
            WHERE id_proveedor = :id
            ORDER BY fecha_devolucion DESC
        """),
        {"id": id}
    ).fetchall()

    return templates.TemplateResponse("proveedores/proveedor_dashboard.html", {
        "request": request,
        "proveedor": proveedor,
        "compras": compras,
        "devoluciones": devoluciones,
        "id": id
    })

# 📌 Formulario de nuevo proveedor
@router.get("/proveedor/nuevo.html", response_class=HTMLResponse)
async def mostrar_formulario_nuevo_proveedor(request: Request):
    return templates.TemplateResponse("proveedores/proveedor_nuevo.html", {"request": request})

# 📌 Editar dashboard
@router.get("/proveedor/editar_dashboard.html", response_class=HTMLResponse)
async def editar_dashboard(request: Request, id: int, db: Session = Depends(get_db)):
    proveedor = db.execute(
        text("SELECT * FROM proveedores WHERE id = :id"), {"id": id}
    ).fetchone()
    
    return templates.TemplateResponse("proveedores/editar_dashboard.html", {
        "request": request,
        "proveedor": proveedor,
        "id": id
    })

# ---------------------------------------------------------
# ✅ FUNCIÓN NUEVA: ELIMINAR FACTURA + PRODUCTOS
# ---------------------------------------------------------
@router.post("/proveedor/eliminar_factura/{id_compra}")
def eliminar_factura(id_compra: int, db: Session = Depends(get_db)):
    try:
        # 1️⃣ Eliminar productos asociados a la factura
        db.execute(
            text("DELETE FROM proveedores_comprasdetalle WHERE id_compra = :id_compra"),
            {"id_compra": id_compra}
        )

        # 2️⃣ Eliminar la factura
        db.execute(
            text("DELETE FROM proveedores_compras WHERE id_compra = :id_compra"),
            {"id_compra": id_compra}
        )

        db.commit()

        return {"mensaje": "Factura y productos eliminados correctamente"}

    except Exception as e:
        print("❌ Error al eliminar factura:", e)
        return {"error": f"No se pudo eliminar la factura: {str(e)}"}