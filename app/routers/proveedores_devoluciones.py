from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.database.db_connection import obtener_conexion as get_connection

router = APIRouter(prefix="/devoluciones", tags=["Devoluciones"])
templates = Jinja2Templates(directory="app/templates")

# 📌 Función auxiliar: obtener historial de devoluciones de un proveedor
def obtener_historial_devoluciones(id_proveedor: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_devolucion, fecha_devolucion, motivo, total_devolucion, notas
            FROM proveedores_devoluciones
            WHERE id_proveedor = %s
            ORDER BY fecha_devolucion DESC;
        """, (id_proveedor,))
        return cursor.fetchall()
    except Exception as e:
        print(f"❌ Error al consultar devoluciones: {e}")
        return []
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

# 📌 Función auxiliar: obtener nombre del proveedor
def obtener_nombre_proveedor(id_proveedor: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT nombre FROM proveedores WHERE id = %s;
        """, (id_proveedor,))
        resultado = cursor.fetchone()
        return resultado[0] if resultado else "Desconocido"
    except Exception as e:
        print(f"❌ Error al consultar nombre del proveedor: {e}")
        return "Desconocido"
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

# 📌 GET: Mostrar historial de devoluciones
@router.get("/proveedores_devoluciones.html", response_class=HTMLResponse)
async def mostrar_devoluciones(request: Request, id_proveedor: int):
    historial = obtener_historial_devoluciones(id_proveedor)
    nombre_proveedor = obtener_nombre_proveedor(id_proveedor)
    return templates.TemplateResponse("devoluciones/proveedores_devoluciones.html", {
        "request": request,
        "id_proveedor": id_proveedor,
        "nombre_proveedor": nombre_proveedor,
        "historial_devoluciones": historial
    })

# 📌 POST: Registrar nueva devolución
@router.post("/registrar", response_class=HTMLResponse)
async def registrar_devolucion(
    request: Request,
    id_proveedor: int = Form(...),
    fecha_devolucion: str = Form(...),
    motivo: str = Form(...),
    total_devolucion: float = Form(...),
    notas: str = Form("")
):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO proveedores_devoluciones (id_proveedor, fecha_devolucion, motivo, total_devolucion, notas)
            VALUES (%s, %s, %s, %s, %s);
        """, (id_proveedor, fecha_devolucion, motivo, total_devolucion, notas))
        conn.commit()
        mensaje = "✅ Devolución registrada correctamente."
    except Exception as e:
        if 'conn' in locals(): conn.rollback()
        mensaje = f"❌ Error al registrar devolución: {str(e)}"
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

    historial = obtener_historial_devoluciones(id_proveedor)
    nombre_proveedor = obtener_nombre_proveedor(id_proveedor)
    return templates.TemplateResponse("devoluciones/proveedores_devoluciones.html", {
        "request": request,
        "id_proveedor": id_proveedor,
        "nombre_proveedor": nombre_proveedor,
        "historial_devoluciones": historial,
        "mensaje": mensaje
    })