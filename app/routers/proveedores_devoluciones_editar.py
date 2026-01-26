# 📄 Ruta: app/routers/proveedores_devoluciones_editar.py

from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.database.db_connection import obtener_conexion as get_connection

router = APIRouter(prefix="/devoluciones", tags=["Devoluciones"])
templates = Jinja2Templates(directory="app/templates")


# ✅ GET: Cargar pantalla de edición de devolución
@router.get("/editar", response_class=HTMLResponse)
async def editar_devolucion(request: Request, id_devolucion: int):

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # ✅ Obtener cabecera de la devolución
        cursor.execute("""
            SELECT d.*, p.nombre AS nombre_proveedor
            FROM proveedores_devoluciones d
            INNER JOIN proveedores p ON p.id = d.id_proveedor
            WHERE d.id_devolucion = %s;
        """, (id_devolucion,))
        devolucion = cursor.fetchone()

        if not devolucion:
            return HTMLResponse("❌ Devolución no encontrada", status_code=404)

        # ✅ Obtener detalle de productos devueltos
        cursor.execute("""
            SELECT dd.*, prod.nombre AS nombre_producto
            FROM proveedores_devoluciones_detalle dd
            INNER JOIN productos prod ON prod.id = dd.id_producto
            WHERE dd.id_devolucion = %s;
        """, (id_devolucion,))
        detalle = cursor.fetchall()

    except Exception as e:
        print(f"❌ Error al cargar devolución: {e}")
        return HTMLResponse("Error interno", status_code=500)

    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

    return templates.TemplateResponse("devoluciones/proveedores_devoluciones_editar.html", {
        "request": request,
        "devolucion": devolucion,
        "detalle": detalle
    })


# ✅ POST: Guardar cambios en la devolución
@router.post("/editar", response_class=HTMLResponse)
async def guardar_edicion_devolucion(
    request: Request,
    id_devolucion: int = Form(...),
    motivo: str = Form(...),
    notas: str = Form(""),
    ajustar_inventario: str = Form(None),
    ajustar_saldo: str = Form(None),
    ids_detalle: list[int] = Form(...),
    cantidades_devuelta_nueva: list[int] = Form(...)
):

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # ✅ Obtener detalle actual
        cursor.execute("""
            SELECT * FROM proveedores_devoluciones_detalle
            WHERE id_devolucion = %s;
        """, (id_devolucion,))
        detalle_actual = cursor.fetchall()

        detalle_por_id = {item["id_detalle"]: item for item in detalle_actual}

        total_nuevo = 0

        # ✅ Recorrer cada producto devuelto
        for idx, id_detalle in enumerate(ids_detalle):
            nueva_cantidad = int(cantidades_devuelta_nueva[idx])
            item = detalle_por_id[id_detalle]

            cantidad_anterior = item["cantidad_devuelta"]
            diferencia = nueva_cantidad - cantidad_anterior

            # ✅ Ajustar inventario si corresponde
            if ajustar_inventario:
                cursor.execute("""
                    UPDATE productos
                    SET stock_actual = stock_actual + %s
                    WHERE id = %s;
                """, (diferencia, item["id_producto"]))

            # ✅ Actualizar detalle
            nuevo_subtotal = nueva_cantidad * float(item["precio_unitario"])

            cursor.execute("""
                UPDATE proveedores_devoluciones_detalle
                SET cantidad_devuelta = %s,
                    subtotal = %s
                WHERE id_detalle = %s;
            """, (nueva_cantidad, nuevo_subtotal, id_detalle))

            total_nuevo += nuevo_subtotal

        # ✅ Actualizar cabecera
        cursor.execute("""
            UPDATE proveedores_devoluciones
            SET motivo = %s,
                notas = %s,
                total_devolucion = %s
            WHERE id_devolucion = %s;
        """, (motivo, notas, total_nuevo, id_devolucion))

        conn.commit()

    except Exception as e:
        if 'conn' in locals(): conn.rollback()
        print(f"❌ Error al actualizar devolución: {e}")
        return HTMLResponse("Error interno", status_code=500)

    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

    # ✅ Redirigir al dashboard del proveedor
    return RedirectResponse(url=f"/proveedores/dashboard?id_proveedor={item['id_proveedor']}", status_code=303)