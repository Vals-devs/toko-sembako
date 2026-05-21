<template>
  <div class="utang-page">
    <!-- Header -->
    <div class="page-header animate-fade-in-up">
      <h1 class="page-title">Utang Pelanggan</h1>
      <button @click="showForm = true" class="btn-add" id="btn-tambah-utang">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
        Tambah
      </button>
    </div>

    <!-- Summary -->
    <div class="summary-cards animate-fade-in-up delay-1">
      <div class="summary-card summary-card--debt">
        <p class="summary-label">Total Utang Belum Lunas</p>
        <p class="summary-amount">{{ formatRupiah(utangStore.ringkasan.total_utang) }}</p>
      </div>
      <div class="summary-card summary-card--count">
        <p class="summary-label">Pelanggan Berutang</p>
        <p class="summary-amount">{{ utangStore.ringkasan.jumlah_pelanggan }} orang</p>
      </div>
    </div>

    <!-- Filter Tabs -->
    <div class="filter-tabs animate-fade-in-up delay-2">
      <button
        v-for="f in filters"
        :key="f.key"
        class="filter-tab"
        :class="{ 'filter-tab--active': activeFilter === f.key }"
        @click="activeFilter = f.key"
      >
        {{ f.label }}
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="utangStore.loading" class="text-center py-12 animate-fade-in">
      <div class="btn-loading-spinner" style="border-top-color: var(--primary-600); width: 32px; height: 32px;"></div>
      <p style="margin-top: 8px; color: var(--text-secondary); font-size: 14px;">Memuat catatan utang...</p>
    </div>

    <!-- Utang List -->
    <div v-else class="utang-list animate-fade-in-up delay-3">
      <div v-if="utangStore.utangList.length === 0" class="empty-state">
        <div class="empty-icon">
          <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
        </div>
        <h3 class="empty-title">{{ activeFilter === 'lunas' ? 'Belum ada yang lunas' : 'Tidak ada catatan utang' }}</h3>
        <p class="empty-desc">{{ activeFilter === 'semua' ? 'Tambahkan catatan utang pelanggan baru' : '' }}</p>
      </div>

      <div
        v-for="item in utangStore.utangList"
        :key="item.id"
        class="utang-card"
        :class="{ 'utang-card--lunas': item.lunas }"
      >
        <div class="utang-main">
          <div class="utang-avatar">
            {{ item.nama_pelanggan.charAt(0).toUpperCase() }}
          </div>
          <div class="utang-info">
            <h3 class="utang-name">{{ item.nama_pelanggan }}</h3>
            <p class="utang-date">{{ formatTanggal(item.tanggal) }}</p>
            <p v-if="item.keterangan" class="utang-note">{{ item.keterangan }}</p>
          </div>
          <div class="utang-right">
            <span class="utang-amount" :class="item.lunas ? 'utang-amount--lunas' : ''">
              {{ formatRupiah(item.jumlah) }}
            </span>
            <span class="utang-status" :class="item.lunas ? 'utang-status--lunas' : 'utang-status--pending'">
              {{ item.lunas ? 'Lunas' : 'Belum Lunas' }}
            </span>
          </div>
        </div>
        <div v-if="!item.lunas" class="utang-actions">
          <button @click="tandaiLunas(item.id)" class="btn-lunas" :disabled="isPaying === item.id">
            <svg v-if="isPaying !== item.id" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
            <span v-else class="btn-loading-spinner" style="width: 14px; height: 14px; border-width: 1.5px; border-top-color: var(--primary-600); margin-right: 6px;"></span>
            {{ isPaying === item.id ? 'Memproses...' : 'Tandai Lunas' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Add Utang Modal -->
    <Teleport to="body">
      <Transition name="modal">
        <div v-if="showForm" class="modal-backdrop" @click.self="showForm = false">
          <div class="modal-sheet">
            <div class="modal-handle"></div>
            <h2 class="modal-title">Tambah Utang Baru</h2>
            <div class="form-fields">
              <div class="field">
                <label class="field-label">Nama Pelanggan</label>
                <input
                  v-model="newUtang.nama"
                  type="text"
                  placeholder="contoh: Pak Ahmad"
                  class="field-input"
                  id="input-nama-pelanggan"
                />
              </div>
              <div class="field">
                <label class="field-label">Jumlah Utang</label>
                <div class="field-input-wrap">
                  <span class="field-prefix">Rp</span>
                  <input
                    v-model.number="newUtang.jumlah"
                    type="number"
                    placeholder="0"
                    class="field-input field-input--prefixed"
                    id="input-jumlah-utang"
                  />
                </div>
              </div>
              <div class="field">
                <label class="field-label">Catatan (opsional)</label>
                <input
                  v-model="newUtang.catatan"
                  type="text"
                  placeholder="contoh: Beli 2kg gula + 1 minyak"
                  class="field-input"
                  id="input-catatan-utang"
                />
              </div>
            </div>
            <div class="modal-buttons">
              <button @click="showForm = false" class="btn-secondary" :disabled="isSubmitting">Batal</button>
              <button @click="simpanUtang" class="btn-primary" id="btn-simpan-utang" :disabled="isSubmitting">
                <span v-if="isSubmitting" class="btn-loading-spinner" style="margin-right: 6px; width: 14px; height: 14px;"></span>
                {{ isSubmitting ? 'Menyimpan...' : 'Tambah Utang' }}
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from "vue";
import { useUtangStore } from "@/stores/utang";

type FilterKey = "semua" | "belum" | "lunas";

const activeFilter = ref<FilterKey>("semua");
const showForm = ref(false);

const utangStore = useUtangStore();

const newUtang = ref({
  nama: "",
  jumlah: 0,
  catatan: "",
});

const filters = [
  { key: "semua" as FilterKey, label: "Semua" },
  { key: "belum" as FilterKey, label: "Belum Lunas" },
  { key: "lunas" as FilterKey, label: "Lunas" },
];

function formatRupiah(angka: number) {
  return "Rp " + (angka || 0).toLocaleString("id-ID");
}

function formatTanggal(isoString: string) {
  if (!isoString) return "";
  const d = new Date(isoString);
  return d.toLocaleDateString("id-ID", {
    day: "numeric",
    month: "short",
    year: "numeric",
  });
}

const isPaying = ref<number | null>(null);

async function tandaiLunas(id: number) {
  if (isPaying.value !== null) return;
  isPaying.value = id;
  try {
    await utangStore.tandaiLunas(id);
    await utangStore.fetchUtang(activeFilter.value);
  } catch (error) {
    alert("Gagal menandai lunas");
  } finally {
    isPaying.value = null;
  }
}

const isSubmitting = ref(false);

async function simpanUtang() {
  if (!newUtang.value.nama || newUtang.value.jumlah <= 0 || isSubmitting.value) return;
  isSubmitting.value = true;
  try {
    await utangStore.tambahUtang({
      nama_pelanggan: newUtang.value.nama,
      jumlah: newUtang.value.jumlah,
      keterangan: newUtang.value.catatan,
    });
    newUtang.value = { nama: "", jumlah: 0, catatan: "" };
    showForm.value = false;
    await utangStore.fetchUtang(activeFilter.value);
  } catch (error) {
    alert("Gagal menambahkan utang");
  } finally {
    isSubmitting.value = false;
  }
}

watch(activeFilter, (newFilter) => {
  utangStore.fetchUtang(newFilter);
});

onMounted(() => {
  utangStore.fetchUtang(activeFilter.value);
  utangStore.fetchRingkasan();
});
</script>

<style scoped>
.utang-page {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.page-header {
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

.btn-add:hover { background: var(--primary-700); }
.btn-add:active { transform: scale(0.96); }

/* Summary */
.summary-cards {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.summary-card {
  padding: 16px;
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-light);
}

.summary-card--debt {
  background: linear-gradient(135deg, #fef3c7, #fde68a);
  border-color: #fcd34d;
}

.summary-card--count {
  background: var(--surface-card);
}

.summary-label {
  font-size: 12px;
  font-weight: 500;
  color: var(--text-secondary);
  margin-bottom: 6px;
}

.summary-card--debt .summary-label {
  color: #92400e;
}

.summary-amount {
  font-size: 20px;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.01em;
}

.summary-card--debt .summary-amount {
  color: #78350f;
}

/* Filter Tabs */
.filter-tabs {
  display: flex;
  gap: 6px;
  background: var(--neutral-100);
  padding: 4px;
  border-radius: var(--radius-md);
}

.filter-tab {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 10px 8px;
  font-size: 13px;
  font-weight: 600;
  color: var(--text-secondary);
  border-radius: var(--radius-sm);
  transition: all var(--duration-fast) ease;
  text-align: center;
}

.filter-tab--active {
  background: var(--surface-card);
  color: var(--primary-700);
  box-shadow: var(--shadow-sm);
}

.filter-count {
  font-size: 11px;
  font-weight: 700;
  background: var(--neutral-200);
  color: var(--text-secondary);
  padding: 1px 6px;
  border-radius: var(--radius-full);
}

.filter-tab--active .filter-count {
  background: var(--primary-100);
  color: var(--primary-700);
}

/* Utang List */
.utang-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.utang-card {
  background: var(--surface-card);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  overflow: hidden;
  transition: all var(--duration-fast) ease;
}

.utang-card--lunas {
  opacity: 0.7;
}

.utang-main {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 14px 16px;
}

.utang-avatar {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-full);
  background: linear-gradient(135deg, var(--primary-100), var(--primary-200));
  color: var(--primary-700);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  font-weight: 700;
  flex-shrink: 0;
}

.utang-info {
  flex: 1;
  min-width: 0;
}

.utang-name {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
}

.utang-date {
  font-size: 12px;
  color: var(--text-tertiary);
  margin-top: 2px;
}

.utang-note {
  font-size: 12px;
  color: var(--text-secondary);
  margin-top: 4px;
  padding: 4px 8px;
  background: var(--neutral-50);
  border-radius: var(--radius-sm);
  display: inline-block;
}

.utang-right {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 4px;
  flex-shrink: 0;
}

.utang-amount {
  font-size: 15px;
  font-weight: 700;
  color: #b45309;
}

.utang-amount--lunas {
  color: var(--primary-600);
  text-decoration: line-through;
}

.utang-status {
  font-size: 11px;
  font-weight: 600;
  padding: 3px 8px;
  border-radius: var(--radius-full);
}

.utang-status--pending {
  background: #fef3c7;
  color: #92400e;
}

.utang-status--lunas {
  background: var(--primary-50);
  color: var(--primary-700);
}

.utang-actions {
  padding: 0 16px 12px;
}

.btn-lunas {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 16px;
  width: 100%;
  justify-content: center;
  background: var(--primary-50);
  color: var(--primary-700);
  font-size: 13px;
  font-weight: 600;
  border-radius: var(--radius-md);
  transition: all var(--duration-fast) ease;
}

.btn-lunas:hover {
  background: var(--primary-100);
}

.btn-lunas:active {
  transform: scale(0.97);
}

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 40px 24px;
  gap: 10px;
}

.empty-icon {
  width: 72px;
  height: 72px;
  border-radius: var(--radius-xl);
  background: var(--neutral-100);
  color: var(--neutral-300);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 4px;
}

.empty-title {
  font-size: 16px;
  font-weight: 700;
  color: var(--text-primary);
}

.empty-desc {
  font-size: 13px;
  color: var(--text-secondary);
}

/* Modal */
.modal-backdrop {
  position: fixed;
  inset: 0;
  z-index: var(--z-modal-backdrop);
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: flex-end;
  justify-content: center;
}

.modal-sheet {
  width: 100%;
  max-width: 480px;
  max-height: 90vh;
  overflow-y: auto;
  background: var(--surface-card);
  border-radius: var(--radius-xl) var(--radius-xl) 0 0;
  padding: 12px 24px 32px;
  z-index: var(--z-modal);
}

.modal-handle {
  width: 36px;
  height: 4px;
  background: var(--neutral-300);
  border-radius: var(--radius-full);
  margin: 0 auto 20px;
}

.modal-title {
  font-size: 20px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 20px;
}

.modal-enter-active {
  transition: opacity var(--duration-normal) ease;
}

.modal-enter-active .modal-sheet {
  animation: slideUp var(--duration-slow) var(--ease-out) both;
}

.modal-leave-active {
  transition: opacity var(--duration-fast) ease;
}

.modal-leave-to {
  opacity: 0;
}

/* Form */
.form-fields {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.field-label {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-secondary);
}

.field-input {
  padding: 12px 14px;
  background: var(--neutral-50);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-md);
  font-size: 15px;
  color: var(--text-primary);
  outline: none;
  transition: border-color var(--duration-fast) ease, box-shadow var(--duration-fast) ease;
  width: 100%;
}

.field-input:focus {
  border-color: var(--primary-400);
  box-shadow: 0 0 0 3px rgba(22, 163, 74, 0.1);
  background: var(--surface-card);
}

.field-input::placeholder {
  color: var(--neutral-400);
}

.field-input-wrap {
  position: relative;
  display: flex;
  align-items: center;
}

.field-prefix {
  position: absolute;
  left: 14px;
  font-size: 14px;
  font-weight: 500;
  color: var(--text-tertiary);
  pointer-events: none;
}

.field-input--prefixed {
  padding-left: 38px;
}

.modal-buttons {
  display: flex;
  gap: 10px;
  margin-top: 24px;
}

.btn-primary {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 14px 20px;
  background: var(--primary-600);
  color: white;
  font-size: 15px;
  font-weight: 600;
  border-radius: var(--radius-md);
  transition: all var(--duration-fast) ease;
}

.btn-primary:hover { background: var(--primary-700); }
.btn-primary:active { transform: scale(0.97); }

.btn-secondary {
  flex: 1;
  padding: 14px 20px;
  background: var(--neutral-100);
  color: var(--text-secondary);
  font-size: 15px;
  font-weight: 600;
  border-radius: var(--radius-md);
  transition: all var(--duration-fast) ease;
}

.btn-secondary:hover { background: var(--neutral-200); }

/* Info Banner */
.info-banner {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 14px 16px;
  background: var(--info-50);
  border: 1px solid #bfdbfe;
  border-radius: var(--radius-md);
  color: var(--info-600);
  font-size: 13px;
  line-height: 1.5;
}

.info-banner svg {
  flex-shrink: 0;
  margin-top: 1px;
}
</style>
