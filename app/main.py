from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

# Routers
from app.routers.login import router as login_router
from app.routers.proveedores_catalogo import router as proveedores_catalogo_router
from app.routers.proveedores_compras_router import router as compras_router
from app.routers.proveedores_comprasdetalle_router import router as comprasdetalle_router
from app.routers.proveedores import router as proveedores_router
from app.routers.productos import router as producto_router
from app.routers.empresa import router as empresa_router
from app.routers.proveedores_pagos import router as proveedores_pagos_router
from app.routers.proveedores_devoluciones import router as proveedores_devoluciones_router
from app.routers.proveedores_edit_purchase import router as proveedores_edit_purchase_router

# ✅ NUEVO: el router que creamos
from app.routers.proveedores_devoluciones_productos import router as proveedores_devoluciones_productos_router

# DB
from app.database.db_connection import get_db
from app.productos.services.producto_service import obtener_productos_activos

app = FastAPI(title="Minimarket API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static & templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Routers
app.include_router(login_router)
app.include_router(proveedores_catalogo_router)
app.include_router(compras_router)
app.include_router(comprasdetalle_router)
app.include_router(proveedores_router)
app.include_router(producto_router)
app.include_router(empresa_router)
app.include_router(proveedores_pagos_router)
app.include_router(proveedores_devoluciones_router)
app.include_router(proveedores_edit_purchase_router)

# ✅ NUEVO: incluir el router de devoluciones-productos
app.include_router(proveedores_devoluciones_productos_router)

# Rutas base
@app.get("/", response_class=HTMLResponse)
async def inicio():
    return RedirectResponse(url="/login")

@app.get("/menu", response_class=HTMLResponse)
async def show_menu(request: Request):
    return templates.TemplateResponse("menu.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def mostrar_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/inventario", response_class=HTMLResponse)
async def switchboard_inventario(request: Request):
    return templates.TemplateResponse("productos/inventario_switchboard.html", {"request": request})

@app.get("/inventario/lista", response_class=HTMLResponse)
async def mostrar_inventario(request: Request, q: str = "", db: Session = Depends(get_db)):
    todos = obtener_productos_activos(db)
    productos = [p for p in todos if q.lower() in p.descripcion.lower()] if q else todos
    return templates.TemplateResponse("productos/inventario_lista.html", {
        "request": request,
        "productos": productos,
        "total": len(todos),
        "filtrados": len(productos)
    })

@app.get("/inventario/switchboard", response_class=HTMLResponse)
async def redirect_switchboard():
    return RedirectResponse(url="/inventario")

@app.get("/inventario/switchbeat", response_class=HTMLResponse)
async def redirect_switchbeat():
    return RedirectResponse(url="/inventario")