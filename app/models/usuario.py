from sqlalchemy import Column, Integer, String
from app.database.db_base import Base  # Asegúrate de tener este archivo

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    nombre = Column(String, nullable=False)
    rol = Column(String, nullable=False)
