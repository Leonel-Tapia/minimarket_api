# Ruta: app/productos/utils/producto_utils.py

from datetime import datetime
from productos.schemas.producto_schema import ProductoUpdate

def generar_detalle_actualizacion(cambios: ProductoUpdate) -> str:
    """
    Genera una descripción textual de los cambios aplicados a un producto.
    """
    partes = []
    for campo, valor in cambios.dict(exclude_unset=True).items():
        partes.append(f"{campo} → {valor}")
    return "; ".join(partes)

def obtener_fecha_actual() -> datetime:
    """
    Devuelve la fecha y hora actual en formato datetime.
    """
    return datetime.now()
