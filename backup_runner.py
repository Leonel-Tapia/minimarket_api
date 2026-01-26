# 📄 Archivo: backup_runner.py

import os
import shutil
from datetime import datetime, timedelta
import subprocess

# 📁 Ruta del proyecto original
ORIGEN = os.path.abspath("C:\\minimarket_api")

# 📁 Carpeta externa donde se guardarán los backups
DESTINO = os.path.abspath("C:\\scripts_backup")
os.makedirs(DESTINO, exist_ok=True)

# 🕒 Nombre del backup con fecha y hora
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
backup_folder_name = f"minimarket_api_{timestamp}"
backup_path = os.path.join(DESTINO, backup_folder_name)

# 🧹 Exclusiones: carpetas y archivos que no deben copiarse
EXCLUIR = ["__pycache__"]

def ignorar_elementos(folder, contents):
    return [item for item in contents if any(ex in item for ex in EXCLUIR)]

# 📤 Copiar el folder completo (excluyendo __pycache__)
shutil.copytree(ORIGEN, backup_path, ignore=ignorar_elementos)

# 📄 Generar requirements.txt dentro del backup
venv_python = os.path.join(ORIGEN, "venv", "Scripts", "python.exe")
requirements_path = os.path.join(backup_path, "requirements.txt")

if not os.path.exists(venv_python):
    print("⚠️ Entorno virtual no encontrado. No se puede generar requirements.txt.")
else:
    try:
        subprocess.run([venv_python, "-m", "pip", "freeze"], stdout=open(requirements_path, "w"), check=True)
        print(f"✅ Backup creado en: {backup_path}")
    except Exception as e:
        print(f"⚠️ Error al generar requirements.txt: {e}")

# 🧹 Eliminar backups con más de 30 días
limite_dias = 30
limite_fecha = datetime.now() - timedelta(days=limite_dias)

for folder in os.listdir(DESTINO):
    folder_path = os.path.join(DESTINO, folder)
    if os.path.isdir(folder_path):
        fecha_creacion = datetime.fromtimestamp(os.path.getctime(folder_path))
        if fecha_creacion < limite_fecha:
            try:
                shutil.rmtree(folder_path)
                print(f"🗑️ Backup eliminado por antigüedad: {folder_path}")
            except Exception as e:
                print(f"⚠️ No se pudo eliminar {folder_path}: {e}")
