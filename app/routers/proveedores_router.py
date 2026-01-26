from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.database.db_connection import obtener_conexion as get_connection

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

def obtener_datos_proveedor(id_proveedor: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, nombre, ruc, direccion, telefono, email,
                   contacto_nombre, contacto_telefono, contacto_email
            FROM proveedores
            WHERE id = %s;
        """, (id_proveedor,))
        resultado = cursor.fetchone()
        if resultado:
            return {
                "id": resultado[0],
                "nombre": resultado[1],
                "ruc": resultado[2],
                "direccion": resultado[3],
                "telefono": resultado[4],
                "email": resultado[5],
                "contacto_nombre": resultado[6],
                "contacto_telefono": resultado[7],
                "contacto_email": resultado[8]
            }
        else:
            return {"id": id_proveedor, "nombre": "Proveedor no encontrado"}
    except Exception as e:
        print(f"❌ Error al consultar proveedor: {e}")
        return {"id": id_proveedor, "nombre": "Error de conexión"}
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

def obtener_historial_compras(id_proveedor: int):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_compra, numero_factura, fecha_compra, fecha_vencimiento, forma_pago, total_compra, total_pagado
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

@router.get("/proveedores/catalogo", response_class=HTMLResponse)
async def mostrar_catalogo_proveedores(request: Request):
    proveedores = []  # Aquí puedes cargar desde la BD si lo deseas
    return templates.TemplateResponse("proveedores/proveedores_catalogo.html", {
        "request": request,
        "proveedores": proveedores
    })

@router.get("/proveedores/{id}/dashboard", response_class=HTMLResponse)
async def mostrar_dashboard_proveedor(request: Request, id: int):
    proveedor = obtener_datos_proveedor(id)
    historial = obtener_historial_compras(id)
    return templates.TemplateResponse("proveedores/proveedor_dashboard.html", {
        "request": request,
        "proveedor": proveedor,
        "historial_compras": historial
    })
