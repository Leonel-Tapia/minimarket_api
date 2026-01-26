import os
import shutil

# Desde tu PC hacia la laptop (carpeta compartida en red)
ORIGEN = "C:/minimarket_api"
DESTINO = r"\\TAPIA\Public Python\minimarket_api"

def copiar_proyecto(origen, destino):
    if not os.path.exists(origen):
        print("❌ Ruta de origen no encontrada.")
        return
    if os.path.exists(destino):
        print("🔄 Eliminando copia anterior...")
        shutil.rmtree(destino)
    print("📦 Copiando proyecto...")
    shutil.copytree(origen, destino)
    print("✅ Proyecto copiado correctamente.")

if __name__ == "__main__":
    copiar_proyecto(ORIGEN, DESTINO)
