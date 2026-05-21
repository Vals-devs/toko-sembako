import { defineStore } from "pinia";
import api from "@/api";

interface ItemTransaksi {
  produk_id: number;
  jumlah: number;
}

interface TransaksiRequest {
  items: ItemTransaksi[];
  bayar: number;
  catatan?: string;
}

interface TransaksiResponse {
  id: number;
  total: number;
  bayar: number;
  kembalian: number;
  tanggal: string;
}

export const useTransaksiStore = defineStore("transaksi", {
  state: () => ({
    lastTransaksi: null as TransaksiResponse | null,
    loading: false,
    error: null as string | null,
  }),

  actions: {
    async catatTransaksi(data: TransaksiRequest): Promise<TransaksiResponse> {
      this.loading = true;
      this.error = null;
      try {
        const res = await api.post("/api/transaksi/", data);
        this.lastTransaksi = res.data;
        return res.data;
      } catch (e: any) {
        const msg =
          e.response?.data?.detail || "Gagal mencatat transaksi";
        this.error = msg;
        throw new Error(msg);
      } finally {
        this.loading = false;
      }
    },
  },
});
