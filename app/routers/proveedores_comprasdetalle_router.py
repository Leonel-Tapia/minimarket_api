# app/routes/proveedores_comprasdetalle_router.py

from fastapi import APIRouter, Request, Form, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.database.db_connection import obtener_conexion as get_connection
from app.services.proveedores_compradetalle_service import actualizar_total_compra

router = APIRouter(prefix="/comprasdetalle", tags=["Detalle de Compras"])
templates = Jinja2Templates(directory="app/templates")

def obtener_productos():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, codigo_parte, descripcion
            FROM productos
            WHERE inactivo = false
            ORDER BY codigo_parte ASC;
        """)
        return cursor.fetchall()
    except Exception as e:
        print(f"❌ Error al consultar productos: {e}")
        return []
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

def obtener_detalles_compra(id_compra: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.codigo_parte, p.descripcion, d.precio_unitario, d.cantidad,
                   ROUND(d.cantidad * d.precio_unitario, 2) AS subtotal
            FROM proveedores_comprasdetalle d
            JOIN productos p ON d.id_producto = p.id
            WHERE d.id_compra = %s
            ORDER BY p.codigo_parte ASC;
        """, (id_compra,))
        return cursor.fetchall()
    except Exception as e:
        print(f"❌ Error al consultar detalles: {e}")
        return []
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

def obtener_proveedor(id_proveedor: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, nombre, direccion, telefono
            FROM proveedores
            WHERE id = %s;
        """, (id_proveedor,))
        return cursor.fetchone()
    except Exception as e:
        print(f"❌ Error al consultar proveedor: {e}")
        return None
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

def obtener_compra(id_compra: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT numero_factura, fecha_compra, forma_pago, fecha_pago, periodo_pago, fecha_vencimiento
            FROM proveedores_compras
            WHERE id_compra = %s;
        """, (id_compra,))
        return cursor.fetchone()
    except Exception as e:
        print(f"❌ Error al consultar compra: {e}")
        return None
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

@router.get("/registrar", response_class=HTMLResponse)
async def mostrar_detalle_compra(
    request: Request,
    id_compra: int = Query(...),
    id_proveedor: int = Query(...)
):
    try:
        productos = obtener_productos()
        detalles = obtener_detalles_compra(id_compra)
        total_compra = round(sum([d[4] for d in detalles]), 2)
        proveedor = obtener_proveedor(id_proveedor)
        compra = obtener_compra(id_compra)

        return templates.TemplateResponse("compras/proveedores_comprasdetalle.html", {
            "request": request,
            "id_compra": id_compra,          # ✅ agregado
            "id_proveedor": id_proveedor,
            "proveedor": proveedor,
            "compra": compra,
            "productos": productos,
            "detalles": detalles,
            "total_compra": total_compra
        })
    except Exception as e:
        print(f"❌ Error en mostrar_detalle_compra: {e}")
        return HTMLResponse(content=f"❌ Error interno: {str(e)}", status_code=500)

@router.post("/agregar", response_class=HTMLResponse)
async def agregar_producto_detalle(
    request: Request,
    id_compra: int = Form(...),
    id_proveedor: int = Form(...),
    id_producto: int = Form(...),
    cantidad: int = Form(...),
    precio_unitario: float = Form(...)
):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO proveedores_comprasdetalle (
                id_compra, id_producto, cantidad, precio_unitario
            )
            VALUES (%s, %s, %s, %s);
        """, (id_compra, id_producto, cantidad, precio_unitario))
        conn.commit()

        print(f"📦 Producto insertado en compra {id_compra}, actualizando total...")
        actualizar_total_compra(id_compra)

        mensaje = "✅ Producto agregado correctamente."
    except Exception as e:
        if 'conn' in locals(): conn.rollback()
        mensaje = f"❌ Error al agregar producto: {str(e)}"
        print(mensaje)
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

    try:
        productos = obtener_productos()
        detalles = obtener_detalles_compra(id_compra)
        total_compra = round(sum([d[4] for d in detalles]), 2)
        proveedor = obtener_proveedor(id_proveedor)
        compra = obtener_compra(id_compra)

        return templates.TemplateResponse("compras/proveedores_comprasdetalle.html", {
            "request": request,
            "id_compra": id_compra,          # ✅ agregado
            "id_proveedor": id_proveedor,
            "proveedor": proveedor,
            "compra": compra,
            "productos": productos,
            "detalles": detalles,
            "mensaje": mensaje,
            "total_compra": total_compra
        })
    except Exception as e:
        print(f"❌ Error al renderizar template después de agregar: {e}")
        return HTMLResponse(content=f"❌ Error interno: {str(e)}", status_code=500)