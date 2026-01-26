# 📄 app/database/db_connection.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.database.db_base import Base

# URL de conexión a PostgreSQL
DATABASE_URL = "postgresql://postgres:leotap@localhost:5432/minimarket_db"

# Crear el motor de conexión
engine = create_engine(DATABASE_URL)

# Crear la fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Función generadora para usar con Depends (por ejemplo, en endpoints con inyección de dependencias)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Función directa para obtener una sesión (usada en routers sin Depends)
def get_db_session():
    return SessionLocal()

# ✅ Conexión directa con psycopg2 (útil para operaciones fuera de SQLAlchemy)
import psycopg2

def obtener_conexion():
    return psycopg2.connect(
        dbname="minimarket_db",
        user="postgres",
        password="leotap",
        host="localhost",
        port="5432"
    )
