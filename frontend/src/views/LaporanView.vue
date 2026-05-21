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

    <!-- Summary Cards -->
    <div class="summary-grid animate-fade-in-up delay-2">
      <div class="summary-card summary-card--income">
        <div class="summary-card-header">
          <span class="summary-label">Pemasukan</span>
          <div class="summary-icon-sm">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/></svg>
          </div>
        </div>
        <p class="summary-amount">{{ formatRupiah(mockData[activePeriod].pemasukan) }}</p>
        <p class="summary-change summary-change--up">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="18 15 12 9 6 15"/></svg>
          {{ mockData[activePeriod].pemasukanPct }}
        </p>
      </div>

      <div class="summary-card summary-card--expense">
        <div class="summary-card-header">
          <span class="summary-label">Pengeluaran</span>
          <div class="summary-icon-sm summary-icon-sm--red">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 18 13.5 8.5 8.5 13.5 1 6"/></svg>
          </div>
        </div>
        <p class="summary-amount">{{ formatRupiah(mockData[activePeriod].pengeluaran) }}</p>
        <p class="summary-change summary-change--down">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>
          {{ mockData[activePeriod].pengeluaranPct }}
        </p>
      </div>

      <div class="summary-card summary-card--profit">
        <div class="summary-card-header">
          <span class="summary-label">Laba Bersih</span>
          <div class="summary-icon-sm summary-icon-sm--green">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/></svg>
          </div>
        </div>
        <p class="summary-amount summary-amount--highlight">
          {{ formatRupiah(mockData[activePeriod].pemasukan - mockData[activePeriod].pengeluaran) }}
        </p>
      </div>
    </div>

    <!-- Bar Chart (Pure CSS) -->
    <div class="chart-section animate-fade-in-up delay-3">
      <h2 class="section-title">Grafik Penjualan</h2>
      <div class="chart-container">
        <div class="chart-bars">
          <div
            v-for="(bar, index) in chartBars"
            :key="index"
            class="chart-bar-wrapper"
          >
            <div
              class="chart-bar"
              :style="{ height: bar.height + '%', animationDelay: index * 60 + 'ms' }"
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
        <div
          v-for="(tx, i) in recentTransactions"
          :key="i"
          class="transaction-item"
        >
          <div class="tx-icon" :class="'tx-icon--' + tx.type">
            <svg v-if="tx.type === 'sale'" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="18 15 12 9 6 15"/></svg>
            <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>
          </div>
          <div class="tx-info">
            <h4 class="tx-name">{{ tx.name }}</h4>
            <p class="tx-time">{{ tx.time }}</p>
          </div>
          <span class="tx-amount" :class="'tx-amount--' + tx.type">
            {{ tx.type === "sale" ? "+" : "-" }}{{ formatRupiah(tx.amount) }}
          </span>
        </div>
      </div>
    </div>

    <!-- Empty State Hint -->
    <div class="info-banner animate-fade-in-up delay-5">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
      <p>Data di atas adalah contoh tampilan. Laporan real akan muncul setelah transaksi dicatat melalui Kasir.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";

type PeriodKey = "hari" | "minggu" | "bulan";

const activePeriod = ref<PeriodKey>("hari");
const periods = [
  { key: "hari" as PeriodKey, label: "Hari Ini" },
  { key: "minggu" as PeriodKey, label: "Minggu Ini" },
  { key: "bulan" as PeriodKey, label: "Bulan Ini" },
];

const mockData: Record<PeriodKey, { pemasukan: number; pengeluaran: number; pemasukanPct: string; pengeluaranPct: string }> = {
  hari: { pemasukan: 850000, pengeluaran: 320000, pemasukanPct: "+12%", pengeluaranPct: "-5%" },
  minggu: { pemasukan: 4250000, pengeluaran: 1800000, pemasukanPct: "+8%", pengeluaranPct: "+3%" },
  bulan: { pemasukan: 18500000, pengeluaran: 7200000, pemasukanPct: "+15%", pengeluaranPct: "+2%" },
};

const chartBars = computed(() => {
  const labels: Record<PeriodKey, string[]> = {
    hari: ["08", "09", "10", "11", "12", "13", "14"],
    minggu: ["Sen", "Sel", "Rab", "Kam", "Jum", "Sab", "Min"],
    bulan: ["Mg1", "Mg2", "Mg3", "Mg4"],
  };
  const heights: Record<PeriodKey, number[]> = {
    hari: [30, 55, 80, 45, 90, 60, 40],
    minggu: [65, 45, 70, 85, 50, 95, 35],
    bulan: [60, 75, 85, 90],
  };
  return labels[activePeriod.value].map((label, i) => ({
    label,
    height: heights[activePeriod.value][i],
  }));
});

const recentTransactions = [
  { name: "Penjualan #047", time: "Hari ini, 14:30", amount: 125000, type: "sale" },
  { name: "Restok Gula Pasir", time: "Hari ini, 10:15", amount: 280000, type: "expense" },
  { name: "Penjualan #046", time: "Kemarin, 16:45", amount: 87000, type: "sale" },
  { name: "Penjualan #045", time: "Kemarin, 11:20", amount: 156000, type: "sale" },
  { name: "Restok Minyak Goreng", time: "Kemarin, 08:00", amount: 450000, type: "expense" },
];

function formatRupiah(angka: number) {
  return "Rp " + angka.toLocaleString("id-ID");
}
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
