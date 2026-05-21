<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold text-gray-800">Manajemen Produk</h1>
      <button
        @click="showForm = true"
        class="bg-green-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-green-700 transition"
      >
        + Tambah Produk
      </button>
    </div>

    <!-- Alert stok menipis -->
    <div
      v-if="stokMenipis.length > 0"
      class="bg-orange-50 border border-orange-300 rounded-lg p-3 mb-4 text-sm text-orange-700"
    >
      Stok menipis:
      <span class="font-bold">{{
        stokMenipis.map((p) => p.nama).join(", ")
      }}</span>
    </div>

    <!-- Loading -->
    <div v-if="store.loading" class="text-center py-10 text-gray-400">
      Memuat data...
    </div>

    <!-- Tabel produk -->
    <div v-else class="bg-white rounded-xl shadow overflow-hidden">
      <table class="w-full text-sm">
        <thead class="bg-gray-50 text-gray-600 uppercase text-xs">
          <tr>
            <th class="px-4 py-3 text-left">Nama Produk</th>
            <th class="px-4 py-3 text-left">Satuan</th>
            <th class="px-4 py-3 text-right">Harga Beli</th>
            <th class="px-4 py-3 text-right">Harga Jual</th>
            <th class="px-4 py-3 text-right">Stok</th>
            <th class="px-4 py-3 text-center">Aksi</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-if="store.produkList.length === 0">
            <td colspan="6" class="px-4 py-8 text-center text-gray-400">
              Belum ada produk. Tambah produk pertama!
            </td>
          </tr>
          <tr
            v-for="produk in store.produkList"
            :key="produk.id"
            class="hover:bg-gray-50 transition"
          >
            <td class="px-4 py-3 font-medium text-gray-800">
              {{ produk.nama }}
            </td>
            <td class="px-4 py-3 text-gray-500">{{ produk.satuan }}</td>
            <td class="px-4 py-3 text-right text-gray-600">
              {{ formatRupiah(produk.harga_beli) }}
            </td>
            <td class="px-4 py-3 text-right font-medium text-green-700">
              {{ formatRupiah(produk.harga_jual) }}
            </td>
            <td class="px-4 py-3 text-right">
              <span
                :class="
                  produk.stok <= produk.stok_minimum
                    ? 'bg-red-100 text-red-600'
                    : 'bg-green-100 text-green-700'
                "
                class="px-2 py-0.5 rounded-full text-xs font-medium"
              >
                {{ produk.stok }} {{ produk.satuan }}
              </span>
            </td>
            <td class="px-4 py-3 text-center">
              <button
                @click="editProduk(produk)"
                class="text-blue-600 hover:text-blue-800 mr-3 text-xs font-medium"
              >
                Edit
              </button>
              <button
                @click="hapusProduk(produk.id!)"
                class="text-red-500 hover:text-red-700 text-xs font-medium"
              >
                Hapus
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal form -->
    <div
      v-if="showForm"
      class="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50 p-4"
    >
      <div class="bg-white rounded-2xl shadow-xl w-full max-w-md p-6">
        <h2 class="text-lg font-bold text-gray-800 mb-4">
          {{ editId ? "Edit Produk" : "Tambah Produk" }}
        </h2>
        <div class="space-y-3">
          <div>
            <label class="text-sm text-gray-600 mb-1 block">Nama Produk</label>
            <input
              v-model="form.nama"
              type="text"
              placeholder="contoh: Gula Pasir"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
            />
          </div>
          <div>
            <label class="text-sm text-gray-600 mb-1 block">Satuan</label>
            <select
              v-model="form.satuan"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
            >
              <option>pcs</option>
              <option>kg</option>
              <option>liter</option>
              <option>dus</option>
              <option>bungkus</option>
              <option>botol</option>
            </select>
          </div>
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="text-sm text-gray-600 mb-1 block"
                >Harga Beli (Rp)</label
              >
              <input
                v-model.number="form.harga_beli"
                type="number"
                placeholder="0"
                class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
              />
            </div>
            <div>
              <label class="text-sm text-gray-600 mb-1 block"
                >Harga Jual (Rp)</label
              >
              <input
                v-model.number="form.harga_jual"
                type="number"
                placeholder="0"
                class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
              />
            </div>
          </div>
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="text-sm text-gray-600 mb-1 block">Stok Awal</label>
              <input
                v-model.number="form.stok"
                type="number"
                placeholder="0"
                class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
              />
            </div>
            <div>
              <label class="text-sm text-gray-600 mb-1 block"
                >Stok Minimum</label
              >
              <input
                v-model.number="form.stok_minimum"
                type="number"
                placeholder="5"
                class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
              />
            </div>
          </div>
        </div>
        <div class="flex gap-3 mt-5">
          <button
            @click="tutupForm"
            class="flex-1 border border-gray-300 text-gray-600 py-2 rounded-lg text-sm hover:bg-gray-50 transition"
          >
            Batal
          </button>
          <button
            @click="simpanProduk"
            class="flex-1 bg-green-600 text-white py-2 rounded-lg text-sm font-medium hover:bg-green-700 transition"
          >
            {{ editId ? "Simpan Perubahan" : "Tambah Produk" }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { useProdukStore } from "@/stores/produk";
import api from "@/api";

const store = useProdukStore();

const showForm = ref(false);
const editId = ref<number | null>(null);
const form = ref({
  nama: "",
  satuan: "pcs",
  harga_beli: 0,
  harga_jual: 0,
  stok: 0,
  stok_minimum: 5,
  aktif: true,
});

const stokMenipis = computed(() =>
  store.produkList.filter((p) => p.stok <= p.stok_minimum),
);

function formatRupiah(angka: number) {
  return "Rp " + angka.toLocaleString("id-ID");
}

function editProduk(produk: any) {
  editId.value = produk.id;
  form.value = { ...produk };
  showForm.value = true;
}

function tutupForm() {
  showForm.value = false;
  editId.value = null;
  form.value = {
    nama: "",
    satuan: "pcs",
    harga_beli: 0,
    harga_jual: 0,
    stok: 0,
    stok_minimum: 5,
    aktif: true,
  };
}

async function simpanProduk() {
  if (!form.value.nama) return alert("Nama produk wajib diisi!");
  if (form.value.harga_jual <= 0)
    return alert("Harga jual harus lebih dari 0!");

  if (editId.value) {
    await store.updateProduk(editId.value, form.value);
  } else {
    await store.tambahProduk(form.value);
  }
  tutupForm();
}

async function hapusProduk(id: number) {
  if (confirm("Yakin hapus produk ini?")) {
    await store.hapusProduk(id);
  }
}

onMounted(() => {
  store.fetchProduk();
});
</script>
