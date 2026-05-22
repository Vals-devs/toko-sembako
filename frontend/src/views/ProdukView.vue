<template>
  <div class="produk-page">
    <!-- Header -->
    <div class="page-header animate-fade-in-up">
      <div class="header-top">
        <h1 class="page-title">Produk</h1>
        <button @click="openForm()" class="btn-add" id="btn-tambah-produk">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
          Tambah
        </button>
      </div>

      <!-- Search -->
      <div class="search-bar">
        <svg class="search-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Cari produk..."
          class="search-input"
          id="input-search-produk"
        />
        <button v-if="searchQuery" @click="searchQuery = ''" class="search-clear">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
        </button>
      </div>
    </div>

    <!-- Stats -->
    <div class="stats-row animate-fade-in-up delay-1">
      <div class="stat-chip">
        <span class="stat-number">{{ filteredList.length }}</span>
        <span class="stat-label">Produk</span>
      </div>
      <div v-if="stokMenipis.length > 0" class="stat-chip stat-chip--warning">
        <span class="stat-number">{{ stokMenipis.length }}</span>
        <span class="stat-label">Stok Rendah</span>
      </div>
      <div class="stat-chip stat-chip--info">
        <span class="stat-number">{{ formatRupiahShort(totalNilaiStok) }}</span>
        <span class="stat-label">Nilai Stok</span>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="store.loading" class="card-list">
      <div v-for="i in 4" :key="i" class="product-card-skeleton">
        <div class="skeleton" style="width:60%; height:16px; margin-bottom:8px"></div>
        <div class="skeleton" style="width:40%; height:14px; margin-bottom:12px"></div>
        <div class="skeleton" style="width:50%; height:14px"></div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else-if="store.produkList.length === 0" class="empty-state animate-fade-in-up delay-2">
      <div class="empty-icon">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 00-1-1.73l-7-4a2 2 0 00-2 0l-7 4A2 2 0 003 8v8a2 2 0 001 1.73l7 4a2 2 0 002 0l7-4A2 2 0 0021 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg>
      </div>
      <h3 class="empty-title">Belum ada produk</h3>
      <p class="empty-desc">Tambahkan produk pertama untuk mulai mengelola stok toko Anda</p>
      <button @click="openForm()" class="btn-primary">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
        Tambah Produk Pertama
      </button>
    </div>

    <!-- No Results -->
    <div v-else-if="filteredList.length === 0 && searchQuery" class="empty-state animate-fade-in">
      <div class="empty-icon empty-icon--muted">
        <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
      </div>
      <h3 class="empty-title">Tidak ditemukan</h3>
      <p class="empty-desc">Tidak ada produk yang cocok dengan "{{ searchQuery }}"</p>
    </div>

    <!-- Product Card List -->
    <div v-else class="card-list animate-fade-in-up delay-2">
      <div
        v-for="(produk, index) in filteredList"
        :key="produk.id"
        class="product-card"
        :style="{ animationDelay: `${index * 40}ms` }"
      >
        <div class="product-main">
          <div class="product-info">
            <h3 class="product-name">{{ produk.nama }}</h3>
            <p class="product-unit">{{ produk.satuan }}</p>
          </div>
          <span
            class="stock-badge"
            :class="produk.stok <= produk.stok_minimum ? 'stock-badge--low' : 'stock-badge--ok'"
          >
            {{ produk.stok }} {{ produk.satuan }}
          </span>
        </div>
        <div class="product-prices">
          <div class="price-item">
            <span class="price-label">Beli</span>
            <span class="price-value">{{ formatRupiah(produk.harga_beli) }}</span>
          </div>
          <div class="price-divider"></div>
          <div class="price-item">
            <span class="price-label">Jual</span>
            <span class="price-value price-value--sell">{{ formatRupiah(produk.harga_jual) }}</span>
          </div>
          <div class="price-divider"></div>
          <div class="price-item">
            <span class="price-label">Margin</span>
            <span class="price-value price-value--margin">{{ formatRupiah(produk.harga_jual - produk.harga_beli) }}</span>
          </div>
        </div>
        <div class="product-actions">
          <button @click="openForm(produk)" class="btn-action btn-action--edit">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
            Edit
          </button>
          <button @click="confirmHapus(produk)" class="btn-action btn-action--delete">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2"/></svg>
            Hapus
          </button>
        </div>
      </div>
    </div>

    <!-- Modal Form -->
    <Teleport to="body">
      <Transition name="modal">
        <div v-if="showForm" class="modal-backdrop" @click.self="tutupForm">
          <div class="modal-sheet">
            <div class="modal-handle"></div>
            <h2 class="modal-title">{{ editId ? "Edit Produk" : "Tambah Produk Baru" }}</h2>

            <div class="form-fields">
              <div class="field">
                <label class="field-label">Nama Produk</label>
                <input
                  v-model="form.nama"
                  type="text"
                  placeholder="contoh: Gula Pasir"
                  class="field-input"
                  id="input-nama-produk"
                />
              </div>

              <div class="field">
                <label class="field-label">Satuan</label>
                <div class="chip-select">
                  <button
                    v-for="s in satuanOptions"
                    :key="s"
                    class="chip"
                    :class="{ 'chip--active': form.satuan === s }"
                    @click="form.satuan = s"
                  >
                    {{ s }}
                  </button>
                </div>
              </div>

              <div class="field-row">
                <div class="field">
                  <label class="field-label">Harga Beli</label>
                  <div class="field-input-wrap">
                    <span class="field-prefix">Rp</span>
                    <input
                      v-model.number="form.harga_beli"
                      type="number"
                      placeholder="0"
                      class="field-input field-input--prefixed"
                      id="input-harga-beli"
                    />
                  </div>
                </div>
                <div class="field">
                  <label class="field-label">Harga Jual</label>
                  <div class="field-input-wrap">
                    <span class="field-prefix">Rp</span>
                    <input
                      v-model.number="form.harga_jual"
                      type="number"
                      placeholder="0"
                      class="field-input field-input--prefixed"
                      id="input-harga-jual"
                    />
                  </div>
                </div>
              </div>

              <div class="field-row">
                <div class="field">
                  <label class="field-label">Stok Awal</label>
                  <input
                    v-model.number="form.stok"
                    type="number"
                    placeholder="0"
                    class="field-input"
                    id="input-stok"
                  />
                </div>
                <div class="field">
                  <label class="field-label">Stok Minimum</label>
                  <input
                    v-model.number="form.stok_minimum"
                    type="number"
                    placeholder="5"
                    class="field-input"
                    id="input-stok-minimum"
                  />
                </div>
              </div>
            </div>

            <div class="modal-buttons">
              <button @click="tutupForm" class="btn-secondary">Batal</button>
              <button @click="simpanProduk" class="btn-primary" id="btn-simpan-produk">
                {{ editId ? "Simpan Perubahan" : "Tambah Produk" }}
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- Confirm Delete Modal -->
    <Teleport to="body">
      <Transition name="modal">
        <div v-if="showDeleteConfirm" class="modal-backdrop" @click.self="showDeleteConfirm = false">
          <div class="modal-sheet modal-sheet--small">
            <div class="modal-handle"></div>
            <div class="delete-confirm-content">
              <div class="delete-icon-wrap">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2"/></svg>
              </div>
              <h3 class="delete-title">Hapus Produk?</h3>
              <p class="delete-desc">
                <strong>{{ deletingProduk?.nama }}</strong> akan dihapus secara permanen. Tindakan ini tidak bisa dibatalkan.
              </p>
            </div>
            <div class="modal-buttons">
              <button @click="showDeleteConfirm = false" class="btn-secondary">Batal</button>
              <button @click="doHapus" class="btn-danger" id="btn-confirm-hapus">Hapus</button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { useProdukStore, type Produk } from "@/stores/produk";
import { formatRupiah, formatRupiahShort } from "@/utils/format";

const store = useProdukStore();

const showForm = ref(false);
const editId = ref<number | null>(null);
const searchQuery = ref("");
const showDeleteConfirm = ref(false);
const deletingProduk = ref<Produk | null>(null);

const satuanOptions = ["pcs", "kg", "liter", "dus", "bungkus", "botol"];

const form = ref<Produk>({
  nama: "",
  satuan: "pcs",
  harga_beli: 0,
  harga_jual: 0,
  stok: 0,
  stok_minimum: 5,
  aktif: true,
});

const filteredList = computed(() => {
  if (!searchQuery.value) return store.produkList;
  const q = searchQuery.value.toLowerCase();
  return store.produkList.filter((p) =>
    p.nama.toLowerCase().includes(q)
  );
});

const stokMenipis = computed(() =>
  store.produkList.filter((p) => p.stok <= p.stok_minimum)
);

const totalNilaiStok = computed(() =>
  store.produkList.reduce((sum, p) => sum + p.harga_jual * p.stok, 0)
);

function openForm(produk?: Produk) {
  if (produk) {
    editId.value = produk.id || null;
    form.value = { ...produk };
  } else {
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
  showForm.value = true;
}

function tutupForm() {
  showForm.value = false;
  editId.value = null;
}

async function simpanProduk() {
  if (!form.value.nama) return;
  if (form.value.harga_jual <= 0) return;

  if (editId.value) {
    await store.updateProduk(editId.value, form.value);
  } else {
    await store.tambahProduk(form.value);
  }
  tutupForm();
}

function confirmHapus(produk: Produk) {
  deletingProduk.value = produk;
  showDeleteConfirm.value = true;
}

async function doHapus() {
  if (deletingProduk.value?.id) {
    await store.hapusProduk(deletingProduk.value.id);
  }
  showDeleteConfirm.value = false;
  deletingProduk.value = null;
}

onMounted(() => {
  store.fetchProduk();
});
</script>

<style scoped>
.produk-page {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* ========================
   Header
   ======================== */
.page-header {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.header-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.page-title {
  font-size: 24px;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: -0.02em;
}

.btn-add {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 16px;
  background: var(--primary-600);
  color: white;
  font-size: 14px;
  font-weight: 600;
  border-radius: var(--radius-md);
  transition: all var(--duration-fast) ease;
}

.btn-add:hover {
  background: var(--primary-700);
}

.btn-add:active {
  transform: scale(0.96);
}

/* ========================
   Search
   ======================== */
.search-bar {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 14px;
  color: var(--neutral-400);
  pointer-events: none;
}

.search-input {
  width: 100%;
  padding: 12px 14px 12px 42px;
  background: var(--surface-card);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-md);
  font-size: 14px;
  color: var(--text-primary);
  outline: none;
  transition: border-color var(--duration-fast) ease, box-shadow var(--duration-fast) ease;
}

.search-input::placeholder {
  color: var(--neutral-400);
}

.search-input:focus {
  border-color: var(--primary-400);
  box-shadow: 0 0 0 3px rgba(22, 163, 74, 0.1);
}

.search-clear {
  position: absolute;
  right: 10px;
  width: 28px;
  height: 28px;
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--neutral-400);
  transition: all var(--duration-fast) ease;
}

.search-clear:hover {
  background: var(--neutral-100);
  color: var(--neutral-600);
}

/* ========================
   Stats
   ======================== */
.stats-row {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.stat-chip {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: var(--neutral-100);
  border-radius: var(--radius-full);
  font-size: 13px;
}

.stat-chip--warning {
  background: #fef3c7;
  color: #92400e;
}

.stat-chip--info {
  background: #dbeafe;
  color: #1e40af;
}

.stat-number {
  font-weight: 700;
}

.stat-label {
  color: var(--text-secondary);
}

.stat-chip--warning .stat-label {
  color: #b45309;
}

.stat-chip--info .stat-label {
  color: #1d4ed8;
}

/* ========================
   Product Cards
   ======================== */
.card-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.product-card {
  background: var(--surface-card);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-light);
  overflow: hidden;
  animation: fadeInUp var(--duration-slow) var(--ease-out) both;
}

.product-card-skeleton {
  background: var(--surface-card);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-light);
  padding: 16px;
}

.product-main {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  padding: 14px 16px 10px;
  gap: 12px;
}

.product-name {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1.3;
}

.product-unit {
  font-size: 12px;
  color: var(--text-tertiary);
  margin-top: 2px;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.stock-badge {
  font-size: 12px;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: var(--radius-full);
  white-space: nowrap;
  flex-shrink: 0;
}

.stock-badge--ok {
  background: var(--primary-50);
  color: var(--primary-700);
}

.stock-badge--low {
  background: var(--danger-50);
  color: var(--danger-600);
  animation: pulse-soft 2s infinite;
}

.product-prices {
  display: flex;
  align-items: center;
  padding: 0 16px 10px;
  gap: 0;
}

.price-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1px;
}

.price-divider {
  width: 1px;
  height: 28px;
  background: var(--border-light);
}

.price-label {
  font-size: 10px;
  font-weight: 500;
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.price-value {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-secondary);
}

.price-value--sell {
  color: var(--primary-700);
}

.price-value--margin {
  color: var(--info-600);
}

.product-actions {
  display: flex;
  border-top: 1px solid var(--border-light);
}

.btn-action {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 10px;
  font-size: 13px;
  font-weight: 500;
  transition: background var(--duration-fast) ease;
}

.btn-action--edit {
  color: var(--info-600);
  border-right: 1px solid var(--border-light);
}

.btn-action--edit:hover {
  background: var(--info-50);
}

.btn-action--delete {
  color: var(--danger-500);
}

.btn-action--delete:hover {
  background: var(--danger-50);
}

/* ========================
   Empty State
   ======================== */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 48px 24px;
  gap: 12px;
}

.empty-icon {
  width: 80px;
  height: 80px;
  border-radius: var(--radius-xl);
  background: var(--primary-50);
  color: var(--primary-400);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 4px;
}

.empty-icon--muted {
  background: var(--neutral-100);
  color: var(--neutral-400);
}

.empty-title {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
}

.empty-desc {
  font-size: 14px;
  color: var(--text-secondary);
  max-width: 280px;
  line-height: 1.5;
}

/* Modal Overrides/Specifics */
.modal-sheet {
  max-height: 90vh;
  overflow-y: auto;
}

.modal-sheet--small {
  padding-bottom: 24px;
}

.modal-title {
  font-size: 20px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 20px;
}

/* Chip Select */
.chip-select {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.chip {
  padding: 8px 14px;
  border-radius: var(--radius-full);
  font-size: 13px;
  font-weight: 500;
  background: var(--neutral-100);
  color: var(--text-secondary);
  border: 1px solid transparent;
  transition: all var(--duration-fast) ease;
}

.chip:hover {
  background: var(--neutral-200);
}

.chip--active {
  background: var(--primary-50);
  color: var(--primary-700);
  border-color: var(--primary-300);
}

/* Delete Confirm */
.delete-confirm-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 8px 0;
  gap: 10px;
}

.delete-icon-wrap {
  width: 56px;
  height: 56px;
  border-radius: var(--radius-lg);
  background: var(--danger-50);
  color: var(--danger-500);
  display: flex;
  align-items: center;
  justify-content: center;
}

.delete-title {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
}

.delete-desc {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.5;
  max-width: 300px;
}

/* Responsive Overrides */
@media (min-width: 640px) {
  .card-list {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
  }
}
</style>
