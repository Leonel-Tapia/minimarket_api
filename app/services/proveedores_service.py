# Ruta: minimarket_api/app/services/proveedores_service.py

from sqlalchemy import text

def obtener_proveedores(db):
    cursor = db.execute(text("""
        SELECT id, nombre, ruc, direccion, telefono, email,
               contacto_nombre, contacto_telefono, contacto_email,
               estado, notas
        FROM proveedores
        ORDER BY creado_en DESC
    """))

    proveedores = []
    for fila in cursor.fetchall():
        proveedor = {
            "id": fila[0],
            "nombre": fila[1],
            "ruc": fila[2],
            "direccion": fila[3],
            "telefono": fila[4],
            "email": fila[5],
            "contacto_nombre": fila[6],
            "contacto_telefono": fila[7],
            "contacto_email": fila[8],
            "estado": "✅" if fila[9] else "❌",
            "notas": fila[10] or ""
        }
        proveedores.append(proveedor)

    return proveedores
