from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from datetime import date
from app.database.db_connection import obtener_conexion
from decimal import Decimal

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# ============================================================
#   RUTA GET — MOSTRAR PANTALLA DE DEVOLUCIONES (SIN HISTORIAL)
# ============================================================
@router.get("/devoluciones/proveedor_productos", response_class=HTMLResponse)
async def mostrar_devoluciones_productos(request: Request, id_proveedor: int):

    conn = obtener_conexion()
    cur = conn.cursor()

    # Obtener nombre del proveedor
    cur.execute("SELECT nombre FROM proveedores WHERE id = %s", (id_proveedor,))
    nombre_proveedor = cur.fetchone()[0]

    # Obtener productos comprados al proveedor
    cur.execute("""
        SELECT c.id_compra, cd.id_producto, p.descripcion,
               cd.cantidad, cd.precio_unitario
        FROM proveedores_compras c
        JOIN proveedores_comprasdetalle cd ON c.id_compra = cd.id_compra
        JOIN productos p ON cd.id_producto = p.id
        WHERE c.id_proveedor = %s
    """, (id_proveedor,))
    compras = cur.fetchall()

    Devoluciones_detalle = []

    for compra in compras:
        id_compra, id_producto, nombre_producto, cantidad_comprada, precio_unitario = compra

        # Calcular cantidad devuelta previamente
        cur.execute("""
            SELECT COALESCE(SUM(cantidad), 0)
            FROM proveedores_devolucionesdetalle
            WHERE id_producto = %s AND id_devolucion IN (
                SELECT id_devolucion FROM proveedores_devoluciones
                WHERE id_proveedor = %s AND id_compra = %s
            )
        """, (id_producto, id_proveedor, id_compra))
        cantidad_devuelta = cur.fetchone()[0]

        cantidad_disponible = cantidad_comprada - cantidad_devuelta

        if cantidad_disponible > 0:
            Devoluciones_detalle.append({
                "id_compra": id_compra,
                "id_producto": id_producto,
                "nombre_producto": nombre_producto,
                "cantidad_comprada": cantidad_comprada,
                "cantidad_devuelta": cantidad_devuelta,
                "cantidad_disponible": cantidad_disponible,
                "precio_unitario": precio_unitario
            })

    conn.close()

    return templates.TemplateResponse("devoluciones/proveedores_devoluciones_productos.html", {
        "request": request,
        "id_proveedor": id_proveedor,
        "nombre_proveedor": nombre_proveedor,
        "Devoluciones_detalle": Devoluciones_detalle
    })


# ============================================================
#   RUTA POST — REGISTRAR DEVOLUCIÓN
# ============================================================
@router.post("/devoluciones/registrar")
async def registrar_devolucion(
    request: Request,
    id_proveedor: int = Form(...),
    fecha_devolucion: date = Form(...),
    motivo: str = Form(...),
    notas: str = Form(""),
    total_devolucion: Decimal = Form(...),
    id_compra: list[int] = Form(...),
    id_producto: list[int] = Form(...),
    cantidad_disponible: list[Decimal] = Form(...),
    cantidad_devolver: list[Decimal] = Form(...),
    precio_unitario: list[Decimal] = Form(...),
    subtotal: list[Decimal] = Form(...)
):

    conn = obtener_conexion()
    cur = conn.cursor()

    # Insertar encabezado
    cur.execute("""
        INSERT INTO proveedores_devoluciones (
            id_proveedor, id_compra, fecha_devolucion, motivo, notas, total_devolucion, fecha_registro
        ) VALUES (%s, %s, %s, %s, %s, %s, NOW())
        RETURNING id_devolucion
    """, (id_proveedor, id_compra[0], fecha_devolucion, motivo, notas, total_devolucion))
    id_devolucion = cur.fetchone()[0]

    # Insertar detalle
    for i in range(len(id_producto)):
        if cantidad_devolver[i] > 0:
            cur.execute("""
                INSERT INTO proveedores_devolucionesdetalle (
                    id_devolucion, id_producto, cantidad, precio_unitario, subtotal, creado_en
                ) VALUES (%s, %s, %s, %s, %s, NOW())
            """, (
                id_devolucion,
                id_producto[i],
                cantidad_devolver[i],
                precio_unitario[i],
                subtotal[i]
            ))

    conn.commit()
    conn.close()

    return RedirectResponse(url=f"/devoluciones/proveedor_productos?id_proveedor={id_proveedor}", status_code=303)