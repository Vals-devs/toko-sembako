from sqlalchemy import Column, Integer, String, Float, Boolean
from app.database import Base

class Produk(Base):
    __tablename__ = "produk"

    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String, nullable=False)
    satuan = Column(String, default="pcs")
    harga_beli = Column(Float, nullable=False)
    harga_jual = Column(Float, nullable=False)
    stok = Column(Integer, default=0)
    stok_minimum = Column(Integer, default=5)
    aktif = Column(Boolean, default=True)