# 📄 app/models/proveedor_nuevo.py

from app.database.db_connection import obtener_conexion
from datetime import datetime

def ruc_duplicado(ruc: str) -> bool:
    """
    Verifica si el RUC ya existe en la base de datos.
    """
    conn = obtener_conexion()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM proveedores WHERE ruc = %s;", (ruc,))
        return cursor.fetchone() is not None
    except Exception:
        return False
    finally:
        cursor.close()
        conn.close()

def guardar_proveedor(datos: dict, creado_por: str = "admin") -> str:
    """
    Inserta un nuevo proveedor en la base de datos.
    Retorna 'ok' si fue exitoso, o un mensaje de error si falló.
    """
    conn = obtener_conexion()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO proveedores (
                nombre, ruc, direccion, telefono, email,
                contacto_nombre, contacto_telefono, contacto_email,
                estado, creado_por, creado_en
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
        """, (
            datos.get("nombre", ""),
            datos.get("ruc", ""),
            datos.get("direccion", ""),
            datos.get("telefono", ""),
            datos.get("email", ""),
            datos.get("contacto_nombre", ""),
            datos.get("contacto_telefono", ""),
            datos.get("contacto_email", ""),
            datos.get("estado", True),
            creado_por,
            datetime.now()
        ))
        nuevo_id = cursor.fetchone()[0]  # ✅ Recupera el ID generado
        conn.commit()
        return "ok"
    except Exception as e:
        conn.rollback()
        return f"Error al guardar proveedor: {e}"
    finally:
        cursor.close()
        conn.close()
