from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.sql import func
from app.database import Base

class Utang(Base):
    __tablename__ = "utang"

    id = Column(Integer, primary_key=True, index=True)
    nama_pelanggan = Column(String, nullable=False)
    jumlah = Column(Float, nullable=False)
    keterangan = Column(String, nullable=True)
    tanggal = Column(DateTime, default=func.now())
    lunas = Column(Boolean, default=False)
    tanggal_lunas = Column(DateTime, nullable=True)