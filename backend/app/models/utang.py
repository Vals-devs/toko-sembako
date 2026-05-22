from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from app.database import Base
from app.utils import get_wita_now

class Utang(Base):
    __tablename__ = "utang"

    id = Column(Integer, primary_key=True, index=True)
    nama_pelanggan = Column(String, nullable=False)
    jumlah = Column(Float, nullable=False)
    keterangan = Column(String, nullable=True)
    tanggal = Column(DateTime, default=get_wita_now)
    lunas = Column(Boolean, default=False)
    tanggal_lunas = Column(DateTime, nullable=True)