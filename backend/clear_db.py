import sys
import os
from sqlalchemy.orm import Session

# Add current folder to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, Base, engine
from app.models.produk import Produk
from app.models.utang import Utang
from app.models.transaksi import Transaksi, DetailTransaksi

def clear_db():
    print("Memulai pembersihan database...")
    db: Session = SessionLocal()
    try:
        # Hapus data detail transaksi dulu karena ada foreign key
        print("Menghapus detail_transaksi...")
        db.query(DetailTransaksi).delete()
        
        print("Menghapus transaksi...")
        db.query(Transaksi).delete()
        
        print("Menghapus produk...")
        db.query(Produk).delete()
        
        print("Menghapus utang...")
        db.query(Utang).delete()
        
        db.commit()
        print("Semua data berhasil dihapus! Database sekarang kosong dan bersih.")
    except Exception as e:
        print(f"Terjadi kesalahan saat membersihkan database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    clear_db()
