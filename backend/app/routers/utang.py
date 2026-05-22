from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.database import get_db
from app.models.utang import Utang
from app.utils import get_wita_now

router = APIRouter(prefix="/api/utang", tags=["Utang"])

class UtangSchema(BaseModel):
    nama_pelanggan: str = Field(min_length=1, max_length=200)
    jumlah: float = Field(ge=0)
    keterangan: Optional[str] = Field(default=None, max_length=500)

class UtangResponse(BaseModel):
    id: int
    nama_pelanggan: str
    jumlah: float
    keterangan: Optional[str]
    tanggal: Optional[datetime]
    lunas: bool
    tanggal_lunas: Optional[datetime]

    class Config:
        from_attributes = True

@router.get("/")
def get_utang(status: str = Query("semua", pattern="^(semua|belum|lunas)$"), db: Session = Depends(get_db)):
    query = db.query(Utang)
    if status == "belum":
        query = query.filter(Utang.lunas == False)
    elif status == "lunas":
        query = query.filter(Utang.lunas == True)
    return query.order_by(Utang.tanggal.desc()).all()

@router.get("/ringkasan")
def get_ringkasan_utang(db: Session = Depends(get_db)):
    belum_lunas = db.query(Utang).filter(Utang.lunas == False).all()
    total = sum(u.jumlah for u in belum_lunas)
    return {
        "total_utang": total,
        "jumlah_pelanggan": len(belum_lunas),
    }

@router.post("/")
def tambah_utang(utang: UtangSchema, db: Session = Depends(get_db)):
    db_utang = Utang(**utang.model_dump())
    db.add(db_utang)
    db.commit()
    db.refresh(db_utang)
    return db_utang

@router.put("/{id}/lunas")
def tandai_lunas(id: int, db: Session = Depends(get_db)):
    db_utang = db.query(Utang).filter(Utang.id == id).first()
    if not db_utang:
        raise HTTPException(status_code=404, detail="Data utang tidak ditemukan")
    
    db_utang.lunas = True
    db_utang.tanggal_lunas = get_wita_now()
    db.commit()
    db.refresh(db_utang)
    return db_utang