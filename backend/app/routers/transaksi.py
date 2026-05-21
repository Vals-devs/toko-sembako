from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from app.database import get_db
from app.models.transaksi import Transaksi, DetailTransaksi
from app.models.produk import Produk

router = APIRouter(prefix="/api/transaksi", tags=["Transaksi"])

class ItemTransaksi(BaseModel):
    produk_id: int
    jumlah: int

class TransaksiSchema(BaseModel):
    items: List[ItemTransaksi]
    bayar: float
    catatan: Optional[str] = None

@router.post("/")
def catat_transaksi(data: TransaksiSchema, db: Session = Depends(get_db)):
    total = 0
    detail_list = []

    for item in data.items:
        produk = db.query(Produk).filter(Produk.id == item.produk_id).first()
        if not produk:
            raise HTTPException(status_code=404, detail=f"Produk id {item.produk_id} tidak ditemukan")
        if produk.stok < item.jumlah:
            raise HTTPException(status_code=400, detail=f"Stok {produk.nama} tidak cukup (sisa {produk.stok})")

        subtotal = produk.harga_jual * item.jumlah
        total += subtotal
        detail_list.append({
            "produk_id": item.produk_id,
            "jumlah": item.jumlah,
            "harga_satuan": produk.harga_jual,
            "subtotal": subtotal
        })
        produk.stok -= item.jumlah

    if data.bayar < total:
        raise HTTPException(status_code=400, detail="Uang bayar kurang")

    transaksi = Transaksi(
        total=total,
        bayar=data.bayar,
        kembalian=data.bayar - total,
        catatan=data.catatan
    )
    db.add(transaksi)
    db.flush()

    for detail in detail_list:
        db.add(DetailTransaksi(transaksi_id=transaksi.id, **detail))

    db.commit()
    db.refresh(transaksi)
    return {
        "id": transaksi.id,
        "total": total,
        "bayar": data.bayar,
        "kembalian": transaksi.kembalian,
        "tanggal": transaksi.tanggal
    }

@router.get("/")
def get_transaksi(db: Session = Depends(get_db)):
    results = db.query(Transaksi).options(
        joinedload(Transaksi.items)
    ).order_by(Transaksi.tanggal.desc()).limit(50).all()

    output = []
    for t in results:
        output.append({
            "id": t.id,
            "tanggal": t.tanggal,
            "total": t.total,
            "bayar": t.bayar,
            "kembalian": t.kembalian,
            "catatan": t.catatan,
            "items": [
                {
                    "id": item.id,
                    "produk_id": item.produk_id,
                    "jumlah": item.jumlah,
                    "harga_satuan": item.harga_satuan,
                    "subtotal": item.subtotal,
                }
                for item in t.items
            ],
        })
    return output