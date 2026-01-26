# MINIMARKET_API    10/28/25

Sistema modular para gestión de minimarket.

## Estructura de imports

- Los imports deben comenzar desde `app.` porque el punto de entrada es `uvicorn app.main:app`.
- Para que VS Code reconozca los imports:
  - Crear `.env` con `PYTHONPATH=.` en la raíz.
  - Configurar `settings.json` con:
    ```json
    {
      "python.analysis.extraPaths": ["./"],
      "python.envFile": "${workspaceFolder}/.env"
    }
    ```

## Ejecución  10/28/25

```bash
uvicorn app.main:app --reload


## 📦 Organización modular

- `app/models/proveedores.py`: define el modelo `Proveedores`
- `app/routers/proveedores.py`: define las rutas `/proveedor/...`
- `app/templates/proveedores_*.html`: vistas HTML para proveedores

Esta convención se repite para otras entidades como `productos`, `clientes`, etc.
