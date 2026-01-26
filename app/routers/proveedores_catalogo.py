from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.database.db_connection import obtener_conexion as get_connection

router = APIRouter(prefix="/proveedores", tags=["Proveedores"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/proveedores_catalogo.html", response_class=HTMLResponse)
async def mostrar_catalogo_proveedores(request: Request):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, nombre, ruc, direccion, telefono, email,
                   contacto_nombre, contacto_telefono, contacto_email,
                   estado, notas
            FROM proveedores
            ORDER BY LOWER(nombre) ASC;
        """)
        resultados = cursor.fetchall()

        proveedores = [
            {
                "id": fila[0],
                "nombre": fila[1],
                "ruc": fila[2],
                "direccion": fila[3],
                "telefono": fila[4],
                "email": fila[5],
                "contacto_nombre": fila[6],
                "contacto_telefono": fila[7],
                "contacto_email": fila[8],
                "estado": bool(fila[9]),
                "notas": fila[10]
            }
            for fila in resultados
        ]

        return templates.TemplateResponse("proveedores/proveedores_catalogo.html", {
            "request": request,
            "proveedores": proveedores
        })

    except Exception as e:
        print("❌ Error en catálogo de proveedores:", e)
        return templates.TemplateResponse("proveedores/proveedores_catalogo.html", {
            "request": request,
            "proveedores": [],
            "mensaje": f"❌ Error al cargar proveedores: {str(e)}"
        })

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()