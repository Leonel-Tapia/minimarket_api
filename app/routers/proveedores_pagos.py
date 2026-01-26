from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.database.db_connection import obtener_conexion as get_connection

router = APIRouter(prefix="/pagos", tags=["Pagos"])
templates = Jinja2Templates(directory="app/templates")

def obtener_historial_pagos(id_compra: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_pago, id_compra, fecha_pago, monto_pago, forma_pago, usuario, observaciones
            FROM proveedores_pagos
            WHERE id_compra = %s
            ORDER BY fecha_pago DESC;
        """, (id_compra,))
        return cursor.fetchall()
    except Exception as e:
        print(f"❌ Error al consultar pagos: {e}")
        return []
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

@router.get("/proveedores_pagos.html", response_class=HTMLResponse)
async def mostrar_pagos(request: Request, id_compra: int):
    historial = obtener_historial_pagos(id_compra)
    return templates.TemplateResponse("pagos/proveedores_pagos.html", {
        "request": request,
        "id_compra": id_compra,
        "historial_pagos": historial
    })

@router.post("/registrar", response_class=HTMLResponse)
async def registrar_pago(
    request: Request,
    id_compra: int = Form(...),
    fecha_pago: str = Form(...),
    monto_pago: float = Form(...),
    forma_pago: str = Form(""),
    usuario: str = Form(""),
    observaciones: str = Form("")
):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO proveedores_pagos (id_compra, fecha_pago, monto_pago, forma_pago, usuario, observaciones)
            VALUES (%s, %s, %s, %s, %s, %s);
        """, (id_compra, fecha_pago, monto_pago, forma_pago, usuario, observaciones))
        conn.commit()
        mensaje = "✅ Pago registrado correctamente."
    except Exception as e:
        if 'conn' in locals(): conn.rollback()
        mensaje = f"❌ Error al registrar pago: {str(e)}"
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

    historial = obtener_historial_pagos(id_compra)
    return templates.TemplateResponse("pagos/proveedores_pagos.html", {
        "request": request,
        "id_compra": id_compra,
        "historial_pagos": historial,
        "mensaje": mensaje
    })
