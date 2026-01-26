from app.database.db_connection import obtener_conexion as get_connection
from decimal import Decimal

# 📌 Servicio para actualizar el total de una compra
def actualizar_total_compra(id_compra: int):
    print(f"🧮 Recalculando total para compra {id_compra}")  # Diagnóstico en consola
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Subtotal de productos
        cursor.execute("""
            SELECT COALESCE(SUM(cantidad * precio_unitario), 0)
            FROM proveedores_comprasdetalle
            WHERE id_compra = %s;
        """, (id_compra,))
        subtotal_productos = cursor.fetchone()[0] or Decimal(0)

        # Impuesto y envío registrados en la compra
        cursor.execute("""
            SELECT impuesto, envio
            FROM proveedores_compras
            WHERE id_compra = %s;
        """, (id_compra,))
        impuesto, envio = cursor.fetchone()

        # Convertir todo a float antes de sumar
        subtotal_productos = float(subtotal_productos)
        impuesto = float(impuesto or 0)
        envio = float(envio or 0)

        total = subtotal_productos + impuesto + envio

        # Actualizar la compra con el total calculado
        cursor.execute("""
            UPDATE proveedores_compras
            SET total_compra = %s
            WHERE id_compra = %s;
        """, (total, id_compra))

        conn.commit()
        print(f"✅ Total actualizado en compra {id_compra}: {total:.2f}")
    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        print(f"❌ Error al actualizar total de compra {id_compra}: {e}")
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()
