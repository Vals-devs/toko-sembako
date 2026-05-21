<template>
  <div class="home">
    <!-- Greeting -->
    <section class="greeting animate-fade-in-up">
      <div class="greeting-text">
        <h1 class="greeting-title">{{ greeting }}, Bos! 👋</h1>
        <p class="greeting-date">{{ todayFormatted }}</p>
      </div>
    </section>

    <!-- Summary Cards -->
    <section class="summary-row scroll-x animate-fade-in-up delay-1">
      <div class="summary-card summary-card--green">
        <div class="summary-icon">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/></svg>
        </div>
        <p class="summary-label">Penjualan Hari Ini</p>
        <p class="summary-value">Rp 0</p>
      </div>
      <div class="summary-card summary-card--blue">
        <div class="summary-icon">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 00-1-1.73l-7-4a2 2 0 00-2 0l-7 4A2 2 0 003 8v8a2 2 0 001 1.73l7 4a2 2 0 002 0l7-4A2 2 0 0021 16z"/></svg>
        </div>
        <p class="summary-label">Total Produk</p>
        <p class="summary-value">{{ produkStore.produkList.length }}</p>
      </div>
      <div class="summary-card summary-card--amber" v-if="stokMenipis.length > 0">
        <div class="summary-icon">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
        </div>
        <p class="summary-label">Stok Menipis</p>
        <p class="summary-value">{{ stokMenipis.length }} item</p>
      </div>
      <div class="summary-card summary-card--red">
        <div class="summary-icon">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
        </div>
        <p class="summary-label">Utang Belum Lunas</p>
        <p class="summary-value">Rp 0</p>
      </div>
    </section>

    <!-- Quick Actions -->
    <section class="section animate-fade-in-up delay-2">
      <h2 class="section-title">Menu Utama</h2>
      <div class="quick-actions">
        <RouterLink to="/kasir" class="action-card action-card--kasir">
          <div class="action-icon-wrap">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 002 1.61h9.72a2 2 0 002-1.61L23 6H6"/></svg>
          </div>
          <div class="action-text">
            <h3 class="action-title">Kasir</h3>
            <p class="action-desc">Catat transaksi penjualan</p>
          </div>
          <svg class="action-arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg>
        </RouterLink>
        <RouterLink to="/produk" class="action-card action-card--produk">
          <div class="action-icon-wrap">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 00-1-1.73l-7-4a2 2 0 00-2 0l-7 4A2 2 0 003 8v8a2 2 0 001 1.73l7 4a2 2 0 002 0l7-4A2 2 0 0021 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg>
          </div>
          <div class="action-text">
            <h3 class="action-title">Produk</h3>
            <p class="action-desc">Kelola stok & harga</p>
          </div>
          <svg class="action-arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg>
        </RouterLink>
        <RouterLink to="/laporan" class="action-card action-card--laporan">
          <div class="action-icon-wrap">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
          </div>
          <div class="action-text">
            <h3 class="action-title">Laporan</h3>
            <p class="action-desc">Lihat untung & rugi</p>
          </div>
          <svg class="action-arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg>
        </RouterLink>
        <RouterLink to="/utang" class="action-card action-card--utang">
          <div class="action-icon-wrap">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
          </div>
          <div class="action-text">
            <h3 class="action-title">Utang</h3>
            <p class="action-desc">Catatan utang pelanggan</p>
          </div>
          <svg class="action-arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg>
        </RouterLink>
      </div>
    </section>

    <!-- Stok Alert -->
    <section v-if="stokMenipis.length > 0" class="section animate-fade-in-up delay-3">
      <h2 class="section-title">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
        Stok Menipis
      </h2>
      <div class="alert-list">
        <div
          v-for="produk in stokMenipis"
          :key="produk.id"
          class="alert-item"
        >
          <div class="alert-info">
            <p class="alert-name">{{ produk.nama }}</p>
            <p class="alert-detail">Sisa {{ produk.stok }} {{ produk.satuan }} · Min. {{ produk.stok_minimum }}</p>
          </div>
          <span class="alert-badge">Rendah</span>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from "vue";
import { useProdukStore } from "@/stores/produk";

const produkStore = useProdukStore();

const stokMenipis = computed(() =>
  produkStore.produkList.filter((p) => p.stok <= p.stok_minimum)
);

const greeting = computed(() => {
  const hour = new Date().getHours();
  if (hour < 11) return "Selamat Pagi";
  if (hour < 15) return "Selamat Siang";
  if (hour < 18) return "Selamat Sore";
  return "Selamat Malam";
});

const todayFormatted = computed(() => {
  return new Date().toLocaleDateString("id-ID", {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
  });
});

onMounted(() => {
  produkStore.fetchProduk();
});
</script>

<style scoped>
.home {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* ========================
   Greeting
   ======================== */
.greeting {
  padding: 4px 0;
}

.greeting-title {
  font-size: 24px;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: -0.02em;
  line-height: 1.2;
}

.greeting-date {
  font-size: 14px;
  color: var(--text-secondary);
  margin-top: 4px;
}

/* ========================
   Summary Cards
   ======================== */
.summary-row {
  display: flex;
  gap: 12px;
  padding: 2px 0;
}

.summary-card {
  min-width: 150px;
  flex-shrink: 0;
  padding: 16px;
  border-radius: var(--radius-lg);
  position: relative;
  overflow: hidden;
}

.summary-card--green {
  background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
  color: var(--primary-800);
}

.summary-card--blue {
  background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
  color: #1e40af;
}

.summary-card--amber {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  color: #92400e;
}

.summary-card--red {
  background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
  color: #991b1b;
}

.summary-icon {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-sm);
  background: rgba(255, 255, 255, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 12px;
}

.summary-label {
  font-size: 12px;
  font-weight: 500;
  opacity: 0.8;
  margin-bottom: 2px;
}

.summary-value {
  font-size: 20px;
  font-weight: 700;
  letter-spacing: -0.01em;
}

/* ========================
   Section
   ======================== */
.section {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.section-title {
  font-size: 16px;
  font-weight: 700;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  gap: 8px;
}

/* ========================
   Quick Actions
   ======================== */
.quick-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.action-card {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 16px;
  background: var(--surface-card);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-light);
  transition: all var(--duration-fast) ease;
  text-decoration: none;
  color: inherit;
}

.action-card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-1px);
}

.action-card:active {
  transform: scale(0.98);
  box-shadow: var(--shadow-xs);
}

.action-icon-wrap {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.action-card--kasir .action-icon-wrap {
  background: linear-gradient(135deg, #dcfce7, #bbf7d0);
  color: var(--primary-700);
}

.action-card--produk .action-icon-wrap {
  background: linear-gradient(135deg, #dbeafe, #bfdbfe);
  color: #2563eb;
}

.action-card--laporan .action-icon-wrap {
  background: linear-gradient(135deg, #f3e8ff, #e9d5ff);
  color: #7c3aed;
}

.action-card--utang .action-icon-wrap {
  background: linear-gradient(135deg, #fef3c7, #fde68a);
  color: #d97706;
}

.action-text {
  flex: 1;
  min-width: 0;
}

.action-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
}

.action-desc {
  font-size: 13px;
  color: var(--text-secondary);
  margin-top: 1px;
}

.action-arrow {
  color: var(--neutral-300);
  flex-shrink: 0;
}

/* ========================
   Alert List
   ======================== */
.alert-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.alert-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 16px;
  background: var(--surface-card);
  border-radius: var(--radius-md);
  border: 1px solid #fde68a;
  border-left: 4px solid #f59e0b;
}

.alert-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

.alert-detail {
  font-size: 12px;
  color: var(--text-secondary);
  margin-top: 2px;
}

.alert-badge {
  font-size: 11px;
  font-weight: 600;
  color: #92400e;
  background: #fef3c7;
  padding: 4px 10px;
  border-radius: var(--radius-full);
  white-space: nowrap;
}

/* ========================
   Responsive
   ======================== */
@media (min-width: 640px) {
  .quick-actions {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
  }
}
</style>
