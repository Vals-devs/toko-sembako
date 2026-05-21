import { defineStore } from "pinia";
import api from "@/api";

interface Ringkasan {
  periode: string;
  pemasukan: number;
  pengeluaran: number;
  laba_bersih: number;
  jumlah_transaksi: number;
}

interface GrafikItem {
  label: string;
  value: number;
}

interface TransaksiTerakhir {
  id: number;
  tanggal: string;
  total: number;
  jumlah_item: number;
  catatan: string | null;
}

interface LaporanHarian {
  tanggal: string;
  jumlah_transaksi: number;
  total_pendapatan: number;
}

export const useLaporanStore = defineStore("laporan", {
  state: () => ({
    ringkasan: null as Ringkasan | null,
    grafik: [] as GrafikItem[],
    transaksiTerakhir: [] as TransaksiTerakhir[],
    harian: null as LaporanHarian | null,
    loading: false,
    error: null as string | null,
  }),

  actions: {
    async fetchRingkasan(periode: string = "hari") {
      this.loading = true;
      this.error = null;
      try {
        const res = await api.get(`/api/laporan/ringkasan?periode=${periode}`);
        this.ringkasan = res.data;
      } catch (e) {
        this.error = "Gagal memuat ringkasan";
      } finally {
        this.loading = false;
      }
    },

    async fetchGrafik(periode: string = "hari") {
      try {
        const res = await api.get(`/api/laporan/grafik?periode=${periode}`);
        this.grafik = res.data;
      } catch (e) {
        // silent
      }
    },

    async fetchTransaksiTerakhir() {
      try {
        const res = await api.get("/api/laporan/transaksi-terakhir?limit=10");
        this.transaksiTerakhir = res.data;
      } catch (e) {
        // silent
      }
    },

    async fetchHarian() {
      try {
        const res = await api.get("/api/laporan/harian");
        this.harian = res.data;
      } catch (e) {
        // silent
      }
    },

    async fetchAll(periode: string = "hari") {
      await Promise.all([
        this.fetchRingkasan(periode),
        this.fetchGrafik(periode),
        this.fetchTransaksiTerakhir(),
      ]);
    },
  },
});
