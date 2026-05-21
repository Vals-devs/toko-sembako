from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, date, timedelta, timezone
from app.database import get_db
from app.models.transaksi import Transaksi, DetailTransaksi
from app.models.produk import Produk

router = APIRouter(prefix="/api/laporan", tags=["Laporan"])

def get_wita_today():
    return datetime.now(timezone(timedelta(hours=8))).date()

def _get_date_range(periode: str):
    """Return (start_date, end_date) for a given period."""
    today = get_wita_today()
    if periode == "minggu":
        start = today - timedelta(days=today.weekday())  # Monday
        return start, today
    elif periode == "bulan":
        start = today.replace(day=1)
        return start, today
    else:  # hari
        return today, today


@router.get("/harian")
def laporan_harian(db: Session = Depends(get_db)):
    hari_ini = get_wita_today()
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


@router.get("/ringkasan")
def laporan_ringkasan(
    periode: str = Query("hari", pattern="^(hari|minggu|bulan)$"),
    db: Session = Depends(get_db),
):
    start, end = _get_date_range(periode)

    transaksi_list = db.query(Transaksi).filter(
        func.date(Transaksi.tanggal) >= start,
        func.date(Transaksi.tanggal) <= end,
    ).all()

    pemasukan = sum(t.total for t in transaksi_list)

    # Hitung pengeluaran (HPP) = harga_beli × jumlah untuk setiap detail
    transaksi_ids = [t.id for t in transaksi_list]
    pengeluaran = 0.0
    if transaksi_ids:
        details = db.query(DetailTransaksi).filter(
            DetailTransaksi.transaksi_id.in_(transaksi_ids)
        ).all()
        for d in details:
            produk = db.query(Produk).filter(Produk.id == d.produk_id).first()
            if produk:
                pengeluaran += produk.harga_beli * d.jumlah

    return {
        "periode": periode,
        "pemasukan": pemasukan,
        "pengeluaran": pengeluaran,
        "laba_bersih": pemasukan - pengeluaran,
        "jumlah_transaksi": len(transaksi_list),
    }


@router.get("/grafik")
def laporan_grafik(
    periode: str = Query("hari", pattern="^(hari|minggu|bulan)$"),
    db: Session = Depends(get_db),
):
    today = get_wita_today()
    data = []

    if periode == "hari":
        # Per jam (08:00 - 20:00)
        for hour in range(8, 21):
            start_dt = datetime(today.year, today.month, today.day, hour, 0, 0)
            end_dt = datetime(today.year, today.month, today.day, hour, 59, 59)
            total = db.query(func.coalesce(func.sum(Transaksi.total), 0)).filter(
                Transaksi.tanggal >= start_dt,
                Transaksi.tanggal <= end_dt,
            ).scalar()
            data.append({"label": f"{hour:02d}:00", "value": float(total)})

    elif periode == "minggu":
        # Per hari (Senin - Minggu)
        day_names = ["Sen", "Sel", "Rab", "Kam", "Jum", "Sab", "Min"]
        start_of_week = today - timedelta(days=today.weekday())
        for i in range(7):
            d = start_of_week + timedelta(days=i)
            total = db.query(func.coalesce(func.sum(Transaksi.total), 0)).filter(
                func.date(Transaksi.tanggal) == d,
            ).scalar()
            data.append({"label": day_names[i], "value": float(total)})

    elif periode == "bulan":
        # Per minggu (Mg1 - Mg4/5)
        first_day = today.replace(day=1)
        week = 1
        current = first_day
        while current.month == today.month and week <= 5:
            week_end = current + timedelta(days=6)
            if week_end.month != today.month:
                week_end = today
            total = db.query(func.coalesce(func.sum(Transaksi.total), 0)).filter(
                func.date(Transaksi.tanggal) >= current,
                func.date(Transaksi.tanggal) <= week_end,
            ).scalar()
            data.append({"label": f"Mg{week}", "value": float(total)})
            current = week_end + timedelta(days=1)
            week += 1

    return data


@router.get("/transaksi-terakhir")
def transaksi_terakhir(limit: int = 10, db: Session = Depends(get_db)):
    transaksi_list = db.query(Transaksi).order_by(
        Transaksi.tanggal.desc()
    ).limit(limit).all()

    result = []
    for t in transaksi_list:
        details = db.query(DetailTransaksi).filter(
            DetailTransaksi.transaksi_id == t.id
        ).all()
        item_count = sum(d.jumlah for d in details)
        result.append({
            "id": t.id,
            "tanggal": t.tanggal,
            "total": t.total,
            "jumlah_item": item_count,
            "catatan": t.catatan,
        })

    return result


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