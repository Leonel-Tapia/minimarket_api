# Ruta: minimarket_api/app/services/empresa_service.py
from sqlalchemy.orm import Session
from app.models.empresa import Empresa

# Obtener empresa
def get_empresa(db: Session):
    """
    Consulta el registro único de la empresa.
    """
    return db.query(Empresa).first()

# Actualizar empresa
def update_empresa(db: Session, data: dict):
    """
    Actualiza los campos de la empresa.
    """
    empresa = db.query(Empresa).first()
    if not empresa:
        return None

    # Actualizar solo campos válidos
    for key, value in data.items():
        if hasattr(Empresa, key):
            setattr(empresa, key, value)

    db.commit()
    db.refresh(empresa)
    return empresa