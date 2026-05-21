from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Transaksi(Base):
    __tablename__ = "transaksi"

    id = Column(Integer, primary_key=True, index=True)
    tanggal = Column(DateTime, default=func.now())
    total = Column(Float, nullable=False)
    bayar = Column(Float, nullable=False)
    kembalian = Column(Float, nullable=False)
    catatan = Column(String, nullable=True)

    items = relationship("DetailTransaksi", back_populates="transaksi")

class DetailTransaksi(Base):
    __tablename__ = "detail_transaksi"

    id = Column(Integer, primary_key=True, index=True)
    transaksi_id = Column(Integer, ForeignKey("transaksi.id"))
    produk_id = Column(Integer, ForeignKey("produk.id"))
    jumlah = Column(Integer, nullable=False)
    harga_satuan = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)

    transaksi = relationship("Transaksi", back_populates="items")