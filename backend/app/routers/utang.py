from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.database import get_db
from app.models.utang import Utang

router = APIRouter(prefix="/api/utang", tags=["Utang"])

class UtangSchema(BaseModel):
    nama_pelanggan: str
    jumlah: float
    keterangan: Optional[str] = None

@router.get("/")
def get_utang(db: Session = Depends(get_db)):
    return db.query(Utang).filter(Utang.lunas == False).all()

@router.post("/")
def tambah_utang(utang: UtangSchema, db: Session = Depends(get_db)):
    db_utang = Utang(**utang.dict())
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
    db_utang.tanggal_lunas = datetime.now()
    db.commit()
    return {"message": "Utang telah ditandai lunas"}