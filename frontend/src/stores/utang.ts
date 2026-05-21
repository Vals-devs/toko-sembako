import { defineStore } from "pinia";
import api from "@/api";

interface UtangItem {
  id: number;
  nama_pelanggan: string;
  jumlah: number;
  keterangan: string | null;
  tanggal: string;
  lunas: boolean;
  tanggal_lunas: string | null;
}

interface UtangRingkasan {
  total_utang: number;
  jumlah_pelanggan: number;
}

export const useUtangStore = defineStore("utang", {
  state: () => ({
    utangList: [] as UtangItem[],
    ringkasan: { total_utang: 0, jumlah_pelanggan: 0 } as UtangRingkasan,
    loading: false,
    error: null as string | null,
  }),

  actions: {
    async fetchUtang(status: string = "semua") {
      this.loading = true;
      this.error = null;
      try {
        const res = await api.get(`/api/utang/?status=${status}`);
        this.utangList = res.data;
      } catch (e) {
        this.error = "Gagal memuat data utang";
      } finally {
        this.loading = false;
      }
    },

    async fetchRingkasan() {
      try {
        const res = await api.get("/api/utang/ringkasan");
        this.ringkasan = res.data;
      } catch (e) {
        // silent
      }
    },

    async tambahUtang(data: {
      nama_pelanggan: string;
      jumlah: number;
      keterangan?: string;
    }) {
      const res = await api.post("/api/utang/", data);
      this.utangList.unshift(res.data);
      await this.fetchRingkasan();
      return res.data;
    },

    async tandaiLunas(id: number) {
      const res = await api.put(`/api/utang/${id}/lunas`);
      const index = this.utangList.findIndex((u) => u.id === id);
      if (index !== -1) {
        this.utangList[index] = res.data;
      }
      await this.fetchRingkasan();
      return res.data;
    },
  },
});
