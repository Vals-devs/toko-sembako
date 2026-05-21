import sys
import os
from sqlalchemy.orm import Session

# Add current folder to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, Base, engine
from app.models.produk import Produk
from app.models.utang import Utang
from app.models.transaksi import Transaksi, DetailTransaksi

def seed_db():
    print("Membuat semua tabel database...")
    Base.metadata.create_all(bind=engine)
    
    db: Session = SessionLocal()
    try:
        # Cek apakah sudah ada data produk
        existing_products = db.query(Produk).count()
        if existing_products > 0:
            print(f"Database sudah terisi dengan {existing_products} produk. Lewati seeding.")
            return

        print("Menambahkan data awal produk sembako...")
        produk_items = [
            Produk(nama="Beras Kepala Premium 10kg", satuan="karung", harga_beli=120000, harga_jual=135000, stok=15, stok_minimum=5),
            Produk(nama="Minyak Goreng Bimoli 2L", satuan="pouch", harga_beli=32000, harga_jual=36000, stok=24, stok_minimum=10),
            Produk(nama="Gula Pasir Gulaku 1kg", satuan="bungkus", harga_beli=15000, harga_jual=17500, stok=30, stok_minimum=10),
            Produk(nama="Telur Ayam Ras", satuan="rak", harga_beli=48000, harga_jual=53000, stok=12, stok_minimum=5),
            Produk(nama="Indomie Goreng Spesial", satuan="bungkus", harga_beli=2800, harga_jual=3500, stok=120, stok_minimum=20),
            Produk(nama="Indomie Goreng Spesial (Karton)", satuan="karton", harga_beli=110000, harga_jual=122000, stok=4, stok_minimum=5), # stok menipis
            Produk(nama="Kopi Kapal Api 165g", satuan="bungkus", harga_beli=13000, harga_jual=15000, stok=18, stok_minimum=5),
            Produk(nama="Susu Kental Manis Frisian Flag", satuan="kaleng", harga_beli=11000, harga_jual=13000, stok=3, stok_minimum=5), # stok menipis
            Produk(nama="Tepung Terigu Segitiga Biru 1kg", satuan="bungkus", harga_beli=12000, harga_jual=14000, stok=2, stok_minimum=5), # stok menipis
            Produk(nama="Sabun Cuci Piring Mama Lemon 680ml", satuan="pouch", harga_beli=12500, harga_jual=14500, stok=15, stok_minimum=5),
        ]
        
        db.add_all(produk_items)
        db.commit()
        print("Data awal produk berhasil ditambahkan!")

        # Menambahkan data awal utang pelanggan
        print("Menambahkan data awal utang...")
        utang_items = [
            Utang(nama_pelanggan="Dg. Nojeng", jumlah=75000, keterangan="Beli beras 10kg dicatat dulu", lunas=False),
            Utang(nama_pelanggan="Tante Linda", jumlah=36000, keterangan="Minyak goreng Bimoli 2L", lunas=False),
            Utang(nama_pelanggan="Dg. Sangkala", jumlah=122000, keterangan="Indomie goreng 1 karton", lunas=True, tanggal_lunas=None),
        ]
        db.add_all(utang_items)
        db.commit()
        print("Data awal utang berhasil ditambahkan!")
        
    except Exception as e:
        print(f"Terjadi kesalahan saat seeding: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
