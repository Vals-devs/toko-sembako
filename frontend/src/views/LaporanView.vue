<template>
  <div class="laporan-page">
    <!-- Header -->
    <div class="page-header animate-fade-in-up">
      <h1 class="page-title">Laporan</h1>
    </div>

    <!-- Period Selector -->
    <div class="period-tabs animate-fade-in-up delay-1">
      <button
        v-for="p in periods"
        :key="p.key"
        class="period-tab"
        :class="{ 'period-tab--active': activePeriod === p.key }"
        @click="activePeriod = p.key"
      >
        {{ p.label }}
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="laporanStore.loading" class="loading-state text-center py-8">
      <div class="btn-loading-spinner" style="border-top-color: var(--primary-600); width: 32px; height: 32px;"></div>
      <p style="margin-top: 8px; color: var(--text-secondary); font-size: 14px;">Memuat data laporan...</p>
    </div>

    <template v-else>
      <!-- Summary Cards -->
      <div class="summary-grid animate-fade-in-up delay-2">
        <div class="summary-card summary-card--income">
          <div class="summary-card-header">
            <span class="summary-label">Pemasukan</span>
            <div class="summary-icon-sm">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/></svg>
            </div>
          </div>
          <p class="summary-amount">{{ formatRupiah(laporanStore.ringkasan?.pemasukan || 0) }}</p>
          <p class="summary-change" style="color: var(--primary-600);">
            {{ laporanStore.ringkasan?.jumlah_transaksi || 0 }} Transaksi
          </p>
        </div>

        <div class="summary-card summary-card--expense">
          <div class="summary-card-header">
            <span class="summary-label">Pengeluaran (HPP)</span>
            <div class="summary-icon-sm summary-icon-sm--red">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 18 13.5 8.5 8.5 13.5 1 6"/></svg>
            </div>
          </div>
          <p class="summary-amount">{{ formatRupiah(laporanStore.ringkasan?.pengeluaran || 0) }}</p>
        </div>

        <div class="summary-card summary-card--profit">
          <div class="summary-card-header">
            <span class="summary-label">Laba Bersih</span>
            <div class="summary-icon-sm summary-icon-sm--green">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/></svg>
            </div>
          </div>
          <p class="summary-amount summary-amount--highlight">
            {{ formatRupiah(laporanStore.ringkasan?.laba_bersih || 0) }}
          </p>
        </div>
      </div>

      <!-- Bar Chart (Pure CSS) -->
      <div class="chart-section animate-fade-in-up delay-3">
        <h2 class="section-title">Grafik Penjualan</h2>
        <div class="chart-container">
          <div v-if="chartBars.length === 0" class="text-center w-full py-12 text-neutral-400 font-medium text-sm">
            Belum ada data penjualan pada periode ini
          </div>
          <div v-else class="chart-bars">
            <div
              v-for="(bar, index) in chartBars"
              :key="index"
              class="chart-bar-wrapper"
            >
              <div
                class="chart-bar"
                :style="{ height: bar.height + '%', animationDelay: index * 60 + 'ms' }"
                :title="formatRupiah(bar.value)"
              ></div>
              <span class="chart-bar-label">{{ bar.label }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Transactions -->
      <div class="section animate-fade-in-up delay-4">
        <h2 class="section-title">Transaksi Terakhir</h2>
        <div class="transaction-list">
          <div v-if="laporanStore.transaksiTerakhir.length === 0" class="text-center py-8 text-neutral-400 font-medium text-sm">
            Belum ada transaksi
          </div>
          <div
            v-else
            v-for="tx in laporanStore.transaksiTerakhir"
            :key="tx.id"
            class="transaction-item"
          >
            <div class="tx-icon tx-icon--sale">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="18 15 12 9 6 15"/></svg>
            </div>
            <div class="tx-info">
              <h4 class="tx-name">Penjualan #{{ tx.id }}</h4>
              <p class="tx-time">{{ formatTanggal(tx.tanggal, { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' }) }} · {{ tx.jumlah_item }} item</p>
            </div>
            <span class="tx-amount tx-amount--sale">
              +{{ formatRupiah(tx.total) }}
            </span>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from "vue";
import { useLaporanStore } from "@/stores/laporan";

type PeriodKey = "hari" | "minggu" | "bulan";

import { formatRupiah, formatTanggal } from "@/utils/format";

const activePeriod = ref<PeriodKey>("hari");
const periods = [
  { key: "hari" as PeriodKey, label: "Hari Ini" },
  { key: "minggu" as PeriodKey, label: "Minggu Ini" },
  { key: "bulan" as PeriodKey, label: "Bulan Ini" },
];

const laporanStore = useLaporanStore();

const chartBars = computed(() => {
  if (!laporanStore.grafik || laporanStore.grafik.length === 0) return [];
  const maxVal = Math.max(...laporanStore.grafik.map((g) => g.value), 1);
  return laporanStore.grafik.map((g) => ({
    label: g.label,
    height: Math.round((g.value / maxVal) * 100),
    value: g.value,
  }));
});

watch(activePeriod, (newPeriod) => {
  laporanStore.fetchAll(newPeriod);
});

onMounted(() => {
  laporanStore.fetchAll(activePeriod.value);
});
</script>

<style scoped>
.laporan-page {
  display: flex;
  flex-direction: column;
  gap: 20px;
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

/* Period Tabs */
.period-tabs {
  display: flex;
  gap: 6px;
  background: var(--neutral-100);
  padding: 4px;
  border-radius: var(--radius-md);
}

.period-tab {
  flex: 1;
  padding: 10px 12px;
  font-size: 13px;
  font-weight: 600;
  color: var(--text-secondary);
  border-radius: var(--radius-sm);
  transition: all var(--duration-fast) ease;
  text-align: center;
}

.period-tab:hover {
  color: var(--text-primary);
}

.period-tab--active {
  background: var(--surface-card);
  color: var(--primary-700);
  box-shadow: var(--shadow-sm);
}

/* Summary Grid */
.summary-grid {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.summary-card {
  padding: 16px;
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-light);
  background: var(--surface-card);
}

.summary-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}

.summary-label {
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
}

.summary-icon-sm {
  width: 28px;
  height: 28px;
  border-radius: var(--radius-sm);
  background: var(--info-50);
  color: var(--info-500);
  display: flex;
  align-items: center;
  justify-content: center;
}

.summary-icon-sm--red {
  background: var(--danger-50);
  color: var(--danger-500);
}

.summary-icon-sm--green {
  background: var(--primary-50);
  color: var(--primary-600);
}

.summary-amount {
  font-size: 22px;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.01em;
}

.summary-amount--highlight {
  color: var(--primary-700);
}

.summary-change {
  display: flex;
  align-items: center;
  gap: 3px;
  font-size: 12px;
  font-weight: 600;
  margin-top: 4px;
}

.summary-change--up {
  color: var(--primary-600);
}

.summary-change--down {
  color: var(--danger-500);
}

/* Chart */
.chart-section {
  background: var(--surface-card);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  padding: 16px;
}

.section-title {
  font-size: 15px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 16px;
}

.chart-container {
  height: 160px;
  display: flex;
  align-items: flex-end;
}

.chart-bars {
  display: flex;
  align-items: flex-end;
  gap: 8px;
  width: 100%;
  height: 100%;
}

.chart-bar-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100%;
  justify-content: flex-end;
  gap: 6px;
}

.chart-bar {
  width: 100%;
  max-width: 40px;
  border-radius: 6px 6px 2px 2px;
  background: linear-gradient(180deg, var(--primary-400) 0%, var(--primary-600) 100%);
  animation: growUp var(--duration-slow) var(--ease-out) both;
  min-height: 4px;
}

@keyframes growUp {
  from {
    height: 0 !important;
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.chart-bar-label {
  font-size: 11px;
  font-weight: 500;
  color: var(--text-tertiary);
}

/* Transactions */
.section {
  display: flex;
  flex-direction: column;
}

.transaction-list {
  display: flex;
  flex-direction: column;
  gap: 2px;
  background: var(--surface-card);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.transaction-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  border-bottom: 1px solid var(--border-light);
}

.transaction-item:last-child {
  border-bottom: none;
}

.tx-icon {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.tx-icon--sale {
  background: var(--primary-50);
  color: var(--primary-600);
}

.tx-icon--expense {
  background: var(--danger-50);
  color: var(--danger-500);
}

.tx-info {
  flex: 1;
  min-width: 0;
}

.tx-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

.tx-time {
  font-size: 12px;
  color: var(--text-tertiary);
  margin-top: 1px;
}

.tx-amount {
  font-size: 14px;
  font-weight: 700;
  white-space: nowrap;
}

.tx-amount--sale {
  color: var(--primary-700);
}

.tx-amount--expense {
  color: var(--danger-600);
}

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

/* Responsive */
@media (min-width: 640px) {
  .summary-grid {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 12px;
  }
}
</style>
