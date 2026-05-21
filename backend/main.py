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
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.routers import produk, transaksi, utang, laporan
app.include_router(produk.router)
app.include_router(transaksi.router)
app.include_router(utang.router)
app.include_router(laporan.router)