from sqlalchemy import Column, Integer, String, DateTime
from app.database.db_connection import Base

class Auditoria(Base):
    __tablename__ = "auditoria"

    id = Column(Integer, primary_key=True, index=True)
    usuario = Column(String(50), nullable=False)
    accion = Column(String(20), nullable=False)
    timestamp = Column(DateTime, nullable=False)
