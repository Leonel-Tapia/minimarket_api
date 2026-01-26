from fastapi import APIRouter, Request, Form, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.database.db_connection import obtener_conexion as get_connection

router = APIRouter(prefix="/comprasdetalle", tags=["Detalle de Compras"])
templates = Jinja2Templates(directory="app/templates")

# 📌 Consulta productos disponibles
def obtener_productos():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, descripcion FROM productos WHERE inactivo = false ORDER BY descripcion ASC;")
        return cursor.fetchall()
    except Exception as e:
        print(f"❌ Error al consultar productos: {e}")
        return []
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

# 📌 Consulta detalle actual de la compra
def obtener_detalles_compra(id_compra: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT d.id_detalle, p.descripcion, d.cantidad, d.precio_unitario,
                   (d.cantidad * d.precio_unitario) AS subtotal
            FROM proveedores_comprasdetalle d
            JOIN productos p ON d.id_producto = p.id
            WHERE d.id_compra = %s
            ORDER BY d.id_detalle ASC;
        """, (id_compra,))
        return cursor.fetchall()
    except Exception as e:
        print(f"❌ Error al consultar detalles: {e}")
        return []
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

# 🧾 Vista para mostrar detalle de compra y formulario
@router.get("/registrar", response_class=HTMLResponse)
async def mostrar_detalle_compra(request: Request, id_compra: int = Query(...)):
    productos = obtener_productos()
    detalles = obtener_detalles_compra(id_compra)

    # Depuración en consola
    print("📦 Productos recibidos:", productos)

    return templates.TemplateResponse("compras/proveedores_comprasdetalle.html", {
        "request": request,
        "id_compra": id_compra,
        "productos": productos,
        "detalles": detalles
    })

# 💾 Registro de producto en el detalle
@router.post("/agregar", response_class=HTMLResponse)
async def agregar_producto_detalle(
    request: Request,
    id_compra: int = Form(...),
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
        mensaje = "✅ Producto agregado correctamente."

    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        mensaje = f"❌ Error al agregar producto: {str(e)}"

    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

    productos = obtener_productos()
    detalles = obtener_detalles_compra(id_compra)

    return templates.TemplateResponse("compras/proveedores_comprasdetalle.html", {
        "request": request,
        "id_compra": id_compra,
        "productos": productos,
        "detalles": detalles,
        "mensaje": mensaje
    })
