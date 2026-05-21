from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from app.database import Base
from datetime import datetime, timedelta, timezone

def get_wita_now():
    return datetime.now(timezone(timedelta(hours=8))).replace(tzinfo=None)

class Utang(Base):
    __tablename__ = "utang"

    id = Column(Integer, primary_key=True, index=True)
    nama_pelanggan = Column(String, nullable=False)
    jumlah = Column(Float, nullable=False)
    keterangan = Column(String, nullable=True)
    tanggal = Column(DateTime, default=get_wita_now)
    lunas = Column(Boolean, default=False)
    tanggal_lunas = Column(DateTime, nullable=True)