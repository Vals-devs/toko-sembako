from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.models.produk import Produk
from app.models.transaksi import Transaksi, DetailTransaksi
from app.models.utang import Utang

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Toko Sembako")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.routers import produk, transaksi, utang, laporan
app.include_router(produk.router)
app.include_router(transaksi.router)
app.include_router(utang.router)
app.include_router(laporan.router)

@app.get("/api/seed")
def run_seeding():
    try:
        from seed import seed_db
        seed_db()
        return {"status": "success", "message": "Database successfully seeded or already has data!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}