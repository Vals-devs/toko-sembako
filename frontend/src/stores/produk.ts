import { defineStore } from "pinia";
import api from "@/api";

export interface Produk {
  id?: number;
  nama: string;
  satuan: string;
  harga_beli: number;
  harga_jual: number;
  stok: number;
  stok_minimum: number;
  aktif: boolean;
}

export const useProdukStore = defineStore("produk", {
  state: () => ({
    produkList: [] as Produk[],
    loading: false,
    error: null as string | null,
  }),

  actions: {
    async fetchProduk() {
      this.loading = true;
      this.error = null;
      try {
        const res = await api.get("/api/produk/");
        this.produkList = res.data;
      } catch (e) {
        this.error = "Gagal memuat data produk";
        console.error(e);
      } finally {
        this.loading = false;
      }
    },

    async tambahProduk(produk: Produk) {
      this.loading = true;
      this.error = null;
      try {
        const res = await api.post("/api/produk/", produk);
        this.produkList.push(res.data);
        return res.data;
      } catch (e) {
        this.error = "Gagal menambah produk";
        console.error(e);
        throw e;
      } finally {
        this.loading = false;
      }
    },

    async updateProduk(id: number, produk: Produk) {
      this.loading = true;
      this.error = null;
      try {
        const res = await api.put(`/api/produk/${id}`, produk);
        const index = this.produkList.findIndex((p) => p.id === id);
        if (index !== -1) this.produkList[index] = res.data;
        return res.data;
      } catch (e) {
        this.error = "Gagal mengupdate produk";
        console.error(e);
        throw e;
      } finally {
        this.loading = false;
      }
    },

    async hapusProduk(id: number) {
      this.loading = true;
      this.error = null;
      try {
        await api.delete(`/api/produk/${id}`);
        this.produkList = this.produkList.filter((p) => p.id !== id);
      } catch (e) {
        this.error = "Gagal menghapus produk";
        console.error(e);
        throw e;
      } finally {
        this.loading = false;
      }
    },
  },
});
