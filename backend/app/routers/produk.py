from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional
from app.database import get_db
from app.models.produk import Produk

router = APIRouter(prefix="/api/produk", tags=["Produk"])

class ProdukSchema(BaseModel):
    nama: str = Field(min_length=1, max_length=200)
    satuan: str = Field(default="pcs", min_length=1, max_length=50)
    harga_beli: float = Field(ge=0)
    harga_jual: float = Field(ge=0)
    stok: int = Field(default=0, ge=0)
    stok_minimum: int = Field(default=5, ge=0)
    aktif: bool = True

@router.get("/")
def get_semua_produk(db: Session = Depends(get_db)):
    return db.query(Produk).filter(Produk.aktif == True).all()

@router.get("/stok-menipis")
def get_stok_menipis(db: Session = Depends(get_db)):
    return db.query(Produk).filter(
        Produk.stok <= Produk.stok_minimum,
        Produk.aktif == True
    ).all()

@router.post("/")
def tambah_produk(produk: ProdukSchema, db: Session = Depends(get_db)):
    db_produk = Produk(**produk.model_dump())
    db.add(db_produk)
    db.commit()
    db.refresh(db_produk)
    return db_produk

@router.put("/{id}")
def update_produk(id: int, produk: ProdukSchema, db: Session = Depends(get_db)):
    db_produk = db.query(Produk).filter(Produk.id == id).first()
    if not db_produk:
        raise HTTPException(status_code=404, detail="Produk tidak ditemukan")
    for key, value in produk.model_dump().items():
        setattr(db_produk, key, value)
    db.commit()
    db.refresh(db_produk)
    return db_produk

@router.delete("/{id}")
def hapus_produk(id: int, db: Session = Depends(get_db)):
    db_produk = db.query(Produk).filter(Produk.id == id).first()
    if not db_produk:
        raise HTTPException(status_code=404, detail="Produk tidak ditemukan")
    db_produk.aktif = False
    db.commit()
    return {"message": "Produk berhasil dihapus"}