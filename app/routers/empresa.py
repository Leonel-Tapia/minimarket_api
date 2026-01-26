from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.services import empresa_service
from app.database.db_connection import get_db
from app.schemas.empresa_schema import EmpresaSchema

# Configuración de plantillas
templates = Jinja2Templates(directory="app/templates")

# Definición del router
router = APIRouter(
    prefix="/empresa",
    tags=["empresa"]
)

# ============================
#   GET: Obtener empresa
# ============================
@router.get("/", response_model=EmpresaSchema)
def get_empresa(db: Session = Depends(get_db)):
    """
    Obtiene el registro único de la empresa.
    """
    empresa = empresa_service.get_empresa(db)
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    return empresa


# ============================
#   PUT: Actualizar empresa
# ============================
@router.put("/", response_model=dict)
async def update_empresa(request: Request, db: Session = Depends(get_db)):
    """
    Actualiza los datos de la empresa con la información enviada desde el formulario.
    """
    data = await request.json()
    updated = empresa_service.update_empresa(db, data)

    if not updated:
        raise HTTPException(status_code=400, detail="No se pudo actualizar la empresa")

    return {"message": "Datos de la empresa actualizados correctamente"}


# ============================
#   GET: Formulario HTML
# ============================
@router.get("/formulario", response_class=HTMLResponse)
async def mostrar_formulario_empresa(request: Request):
    """
    Renderiza la plantilla HTML con el formulario de datos de la empresa.
    """
    return templates.TemplateResponse(
        "empresa/empresa_form.html",
        {"request": request}
    )