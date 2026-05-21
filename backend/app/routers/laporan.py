from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, date
from app.database import get_db
from app.models.transaksi import Transaksi, DetailTransaksi
from app.models.produk import Produk

router = APIRouter(prefix="/api/laporan", tags=["Laporan"])

@router.get("/harian")
def laporan_harian(db: Session = Depends(get_db)):
    hari_ini = date.today()
    transaksi = db.query(Transaksi).filter(
        func.date(Transaksi.tanggal) == hari_ini
    ).all()

    total_pendapatan = sum(t.total for t in transaksi)
    jumlah_transaksi = len(transaksi)

    return {
        "tanggal": hari_ini,
        "jumlah_transaksi": jumlah_transaksi,
        "total_pendapatan": total_pendapatan,
    }

@router.get("/produk-terlaris")
def produk_terlaris(db: Session = Depends(get_db)):
    hasil = db.query(
        Produk.nama,
        func.sum(DetailTransaksi.jumlah).label("total_terjual")
    ).join(DetailTransaksi, Produk.id == DetailTransaksi.produk_id
    ).group_by(Produk.id
    ).order_by(func.sum(DetailTransaksi.jumlah).desc()
    ).limit(5).all()

    return [{"nama": r.nama, "total_terjual": r.total_terjual} for r in hasil]