from pydantic import BaseModel

class EmpresaSchema(BaseModel):
    id: int
    nombre_comercial: str
    razon_social: str
    rfc: str
    giro: str | None = None
    direccion: str | None = None
    colonia: str | None = None
    ciudad: str | None = None
    estado: str | None = None
    codigo_postal: str | None = None
    telefono_principal: str | None = None
    email_principal: str | None = None
    contacto_nombre: str | None = None
    contacto_telefono: str | None = None
    contacto_email: str | None = None
    notas: str | None = None
    aviso_factura: bool
    ventas_tax_general: float

    class Config:
        from_attributes = True  # ✅ reemplaza orm_mode en Pydantic v2
