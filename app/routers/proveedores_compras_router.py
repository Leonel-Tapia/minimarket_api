from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.database.db_connection import obtener_conexion as get_connection
from datetime import datetime, timedelta

router = APIRouter(prefix="/compras", tags=["Compras"])
templates = Jinja2Templates(directory="app/templates")

# 🔹 Función auxiliar: obtener datos del proveedor
def obtener_datos_proveedor(id_proveedor: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre FROM proveedores WHERE id = %s;", (id_proveedor,))
        resultado = cursor.fetchone()
        return {"id": resultado[0], "nombre": resultado[1]} if resultado else {"id": id_proveedor, "nombre": "Proveedor no encontrado"}
    except Exception as e:
        print(f"❌ Error al consultar proveedor: {e}")
        return {"id": id_proveedor, "nombre": "Error de conexión"}
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

# 🔹 Función auxiliar: historial de compras
def obtener_historial_compras(id_proveedor: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_compra, numero_factura, fecha_compra, fecha_vencimiento, forma_pago, total_compra
            FROM proveedores_compras
            WHERE id_proveedor = %s
            ORDER BY id_compra DESC;
        """, (id_proveedor,))
        return cursor.fetchall()
    except Exception as e:
        print(f"❌ Error al consultar historial: {e}")
        return []
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

# 🔹 Validación de fechas
def validar_fechas(fecha_compra: str, fecha_pago: str, fecha_vencimiento: str):
    hoy = datetime.today().date()
    seis_meses_atras = hoy - timedelta(days=180)
    seis_meses_adelante = hoy + timedelta(days=180)

    fechas = {
        "Fecha de compra": fecha_compra,
        "Fecha de pago": fecha_pago,
        "Fecha de vencimiento": fecha_vencimiento
    }

    for nombre, valor in fechas.items():
        if not valor:
            continue
        try:
            f = datetime.strptime(valor, "%Y-%m-%d").date()
        except ValueError:
            return False, f"❌ {nombre} inválida: {valor}"

        if f < seis_meses_atras or f > seis_meses_adelante:
            return False, f"❌ {nombre} fuera del rango permitido (±6 meses)."

    return True, None

# 🔹 GET: mostrar formulario de compra
@router.get("/proveedores_compras.html", response_class=HTMLResponse)
async def mostrar_formulario_compra(request: Request, id_proveedor: int):
    proveedor = obtener_datos_proveedor(id_proveedor)
    historial = obtener_historial_compras(id_proveedor)
    return templates.TemplateResponse("compras/proveedores_compras.html", {
        "request": request,
        "id_proveedor": proveedor["id"],
        "nombre_proveedor": proveedor["nombre"],
        "historial_compras": historial,
        "id_compra": None
    })

# 🔹 POST: registrar compra
@router.post("/registrar", response_class=HTMLResponse)
async def registrar_compra(
    request: Request,
    id_proveedor: int = Form(...),
    numero_factura: str = Form(...),
    fecha_compra: str = Form(...),
    forma_pago: str = Form(...),
    fecha_pago: str = Form(...),
    periodo_pago: int = Form(...),
    fecha_vencimiento: str = Form(...),
    observaciones: str = Form(""),
    notas: str = Form(""),
    impuesto: float = Form(0.0),
    envio: float = Form(0.0)
):
    try:
        valido, mensaje_error = validar_fechas(fecha_compra, fecha_pago, fecha_vencimiento)
        if not valido:
            proveedor = obtener_datos_proveedor(id_proveedor)
            historial = obtener_historial_compras(id_proveedor)
            return templates.TemplateResponse("compras/proveedores_compras.html", {
                "request": request,
                "id_proveedor": proveedor["id"],
                "nombre_proveedor": proveedor["nombre"],
                "historial_compras": historial,
                "id_compra": None,
                "mensaje": mensaje_error
            })

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO proveedores_compras (
                id_proveedor, numero_factura, fecha_compra, forma_pago,
                fecha_pago, periodo_pago, fecha_vencimiento,
                impuesto, envio, total_compra, observaciones, notas
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            RETURNING id_compra;
        """, (
            id_proveedor, numero_factura, fecha_compra, forma_pago,
            fecha_pago, periodo_pago, fecha_vencimiento,
            impuesto, envio, 0.0, observaciones, notas
        ))
        id_compra = cursor.fetchone()[0]
        conn.commit()
        return RedirectResponse(
            url=f"/comprasdetalle/registrar?id_compra={id_compra}&id_proveedor={id_proveedor}",
            status_code=303
        )
    except Exception as e:
        if 'conn' in locals(): conn.rollback()
        proveedor = obtener_datos_proveedor(id_proveedor)
        historial = obtener_historial_compras(id_proveedor)
        return templates.TemplateResponse("compras/proveedores_compras.html", {
            "request": request,
            "id_proveedor": proveedor["id"],
            "nombre_proveedor": proveedor["nombre"],
            "historial_compras": historial,
            "id_compra": None,
            "mensaje": f"❌ Error al registrar compra: {str(e)}"
        })
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()
