<template>
  <div class="kasir-page">
    <!-- Header -->
    <div class="page-header animate-fade-in-up">
      <h1 class="page-title">Kasir</h1>
      <div class="header-date">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
        {{ todayFormatted }}
      </div>
    </div>

    <!-- Search Product -->
    <div class="search-section animate-fade-in-up delay-1">
      <div class="search-bar">
        <svg class="search-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Cari produk untuk ditambahkan..."
          class="search-input"
          id="input-search-kasir"
          @focus="showDropdown = true"
        />
      </div>

      <!-- Dropdown Results -->
      <div v-if="showDropdown && searchResults.length > 0" class="search-dropdown animate-slide-down">
        <button
          v-for="produk in searchResults"
          :key="produk.id"
          class="dropdown-item"
          @click="addToCart(produk)"
        >
          <div class="dropdown-info">
            <span class="dropdown-name">{{ produk.nama }}</span>
            <span class="dropdown-price">{{ formatRupiah(produk.harga_jual) }}/{{ produk.satuan }}</span>
          </div>
          <span class="dropdown-stock" :class="produk.stok <= 0 ? 'dropdown-stock--empty' : ''">
            Stok: {{ produk.stok }}
          </span>
        </button>
      </div>
    </div>

    <!-- Quick Add Buttons -->
    <div v-if="produkStore.produkList.length > 0 && !showDropdown" class="quick-add scroll-x animate-fade-in-up delay-2">
      <button
        v-for="produk in quickProducts"
        :key="produk.id"
        class="quick-chip"
        @click="addToCart(produk)"
      >
        {{ produk.nama }}
      </button>
    </div>

    <!-- Cart Items -->
    <div class="cart-section animate-fade-in-up delay-2">
      <div class="cart-header">
        <h2 class="cart-title">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 002 1.61h9.72a2 2 0 002-1.61L23 6H6"/></svg>
          Keranjang
        </h2>
        <span class="cart-count" v-if="cart.length > 0">{{ cart.length }} item</span>
      </div>

      <!-- Empty Cart -->
      <div v-if="cart.length === 0" class="cart-empty">
        <div class="cart-empty-icon">
          <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 002 1.61h9.72a2 2 0 002-1.61L23 6H6"/></svg>
        </div>
        <p class="cart-empty-text">Keranjang masih kosong</p>
        <p class="cart-empty-hint">Cari produk di atas untuk mulai transaksi</p>
      </div>

      <!-- Cart List -->
      <div v-else class="cart-list">
        <div
          v-for="(item, index) in cart"
          :key="index"
          class="cart-item"
        >
          <div class="cart-item-info">
            <h4 class="cart-item-name">{{ item.nama }}</h4>
            <p class="cart-item-price">{{ formatRupiah(item.harga_jual) }}/{{ item.satuan }}</p>
          </div>
          <div class="cart-item-controls">
            <button class="qty-btn" @click="decreaseQty(index)">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="5" y1="12" x2="19" y2="12"/></svg>
            </button>
            <span class="qty-value">{{ item.qty }}</span>
            <button class="qty-btn" @click="increaseQty(index)">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
            </button>
          </div>
          <div class="cart-item-subtotal">
            <span>{{ formatRupiah(item.harga_jual * item.qty) }}</span>
            <button class="cart-item-remove" @click="removeFromCart(index)">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Total & Pay -->
    <div v-if="cart.length > 0" class="pay-section animate-fade-in-up">
      <div class="pay-summary">
        <div class="pay-row">
          <span class="pay-label">Subtotal ({{ totalItems }} item)</span>
          <span class="pay-value">{{ formatRupiah(grandTotal) }}</span>
        </div>
      </div>
      <button class="btn-pay" @click="showPayModal = true" id="btn-bayar">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="4" width="22" height="16" rx="2" ry="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg>
        Bayar {{ formatRupiah(grandTotal) }}
      </button>
    </div>

    <!-- Payment Modal -->
    <Teleport to="body">
      <Transition name="modal">
        <div v-if="showPayModal" class="modal-backdrop" @click.self="showPayModal = false">
          <div class="modal-sheet">
            <div class="modal-handle"></div>
            <div class="pay-modal-content">
              <div class="pay-success-icon">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 11-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
              </div>
              <h3 class="pay-modal-title">Konfirmasi Pembayaran</h3>
              <div class="pay-modal-detail">
                <div class="pay-detail-row">
                  <span>Total Item</span>
                  <span>{{ totalItems }} item</span>
                </div>
                <div class="pay-detail-row pay-detail-row--total">
                  <span>Total Bayar</span>
                  <span>{{ formatRupiah(grandTotal) }}</span>
                </div>
              </div>
              <div class="modal-buttons">
                <button @click="showPayModal = false" class="btn-secondary" :disabled="isSubmitting">Batal</button>
                <button @click="completePay" class="btn-primary" id="btn-confirm-bayar" :disabled="isSubmitting">
                  <svg v-if="!isSubmitting" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                  <span v-else class="btn-loading-spinner"></span>
                  {{ isSubmitting ? 'Menyimpan...' : 'Selesai' }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- Success Toast -->
    <Teleport to="body">
      <Transition name="toast">
        <div v-if="showToast" class="toast-success">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
          Transaksi berhasil disimpan!
        </div>
      </Transition>
    </Teleport>

    <!-- Error Toast -->
    <Teleport to="body">
      <Transition name="toast">
        <div v-if="showErrorToast" class="toast-error">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
          {{ errorMessage }}
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from "vue";
import { useProdukStore } from "@/stores/produk";
import { useTransaksiStore } from "@/stores/transaksi";

const produkStore = useProdukStore();
const transaksiStore = useTransaksiStore();

interface CartItem {
  id: number;
  nama: string;
  satuan: string;
  harga_jual: number;
  qty: number;
}

const searchQuery = ref("");
const showDropdown = ref(false);
const cart = ref<CartItem[]>([]);
const showPayModal = ref(false);
const showToast = ref(false);
const showErrorToast = ref(false);
const errorMessage = ref("");
const isSubmitting = ref(false);

const todayFormatted = computed(() =>
  new Date().toLocaleDateString("id-ID", {
    weekday: "short",
    day: "numeric",
    month: "short",
    year: "numeric",
  })
);

const searchResults = computed(() => {
  if (!searchQuery.value) return produkStore.produkList.slice(0, 8);
  const q = searchQuery.value.toLowerCase();
  return produkStore.produkList.filter((p) => p.nama.toLowerCase().includes(q)).slice(0, 8);
});

const quickProducts = computed(() => produkStore.produkList.slice(0, 6));

const totalItems = computed(() => cart.value.reduce((sum, item) => sum + item.qty, 0));
const grandTotal = computed(() => cart.value.reduce((sum, item) => sum + item.harga_jual * item.qty, 0));

function formatRupiah(angka: number) {
  return "Rp " + angka.toLocaleString("id-ID");
}

function addToCart(produk: any) {
  const existing = cart.value.find((item) => item.id === produk.id);
  if (existing) {
    existing.qty++;
  } else {
    cart.value.push({
      id: produk.id,
      nama: produk.nama,
      satuan: produk.satuan,
      harga_jual: produk.harga_jual,
      qty: 1,
    });
  }
  searchQuery.value = "";
  showDropdown.value = false;
}

function increaseQty(index: number) {
  const item = cart.value[index];
  if (item) {
    item.qty++;
  }
}

function decreaseQty(index: number) {
  const item = cart.value[index];
  if (item) {
    if (item.qty > 1) {
      item.qty--;
    } else {
      removeFromCart(index);
    }
  }
}

function removeFromCart(index: number) {
  cart.value.splice(index, 1);
}

async function completePay() {
  if (isSubmitting.value) return;
  isSubmitting.value = true;
  try {
    const data = {
      items: cart.value.map((item) => ({
        produk_id: item.id,
        jumlah: item.qty,
      })),
      bayar: grandTotal.value,
      catatan: "",
    };
    await transaksiStore.catatTransaksi(data);
    
    // Refresh products to sync the updated stocks
    await produkStore.fetchProduk();
    
    showPayModal.value = false;
    cart.value = [];
    showToast.value = true;
    setTimeout(() => {
      showToast.value = false;
    }, 3000);
  } catch (error: any) {
    errorMessage.value = error.message || "Gagal menyimpan transaksi";
    showErrorToast.value = true;
    setTimeout(() => {
      showErrorToast.value = false;
    }, 4000);
  } finally {
    isSubmitting.value = false;
  }
}

// Close dropdown when clicking outside
watch(searchQuery, (val) => {
  if (val) showDropdown.value = true;
});

onMounted(() => {
  produkStore.fetchProduk();
  document.addEventListener("click", (e) => {
    const target = e.target as HTMLElement;
    if (!target.closest(".search-section")) {
      showDropdown.value = false;
    }
  });
});
</script>

<style scoped>
.kasir-page {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* Header */
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

.header-date {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: var(--text-secondary);
}

/* Search */
.search-section {
  position: relative;
  z-index: 50;
}

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
  padding: 14px 14px 14px 42px;
  background: var(--surface-card);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-md);
  font-size: 15px;
  color: var(--text-primary);
  outline: none;
  transition: border-color var(--duration-fast) ease, box-shadow var(--duration-fast) ease;
}

.search-input:focus {
  border-color: var(--primary-400);
  box-shadow: 0 0 0 3px rgba(22, 163, 74, 0.1);
}

.search-input::placeholder {
  color: var(--neutral-400);
}

.search-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  z-index: var(--z-dropdown);
  background: var(--surface-card);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-lg);
  margin-top: 4px;
  overflow: hidden;
  max-height: 300px;
  overflow-y: auto;
}

.dropdown-item {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  text-align: left;
  transition: background var(--duration-fast) ease;
  border-bottom: 1px solid var(--border-light);
}

.dropdown-item:last-child {
  border-bottom: none;
}

.dropdown-item:hover {
  background: var(--primary-50);
}

.dropdown-item:active {
  background: var(--primary-100);
}

.dropdown-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

.dropdown-price {
  font-size: 12px;
  color: var(--text-secondary);
  margin-top: 2px;
  display: block;
}

.dropdown-stock {
  font-size: 12px;
  font-weight: 500;
  color: var(--primary-600);
  white-space: nowrap;
}

.dropdown-stock--empty {
  color: var(--danger-500);
}

/* Quick Add */
.quick-add {
  display: flex;
  gap: 8px;
  padding: 2px 0;
}

.quick-chip {
  flex-shrink: 0;
  padding: 8px 14px;
  background: var(--surface-card);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-full);
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
  transition: all var(--duration-fast) ease;
  white-space: nowrap;
}

.quick-chip:hover {
  border-color: var(--primary-300);
  color: var(--primary-700);
  background: var(--primary-50);
}

.quick-chip:active {
  transform: scale(0.95);
}

/* Cart */
.cart-section {
  background: var(--surface-card);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-light);
  overflow: hidden;
}

.cart-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 16px;
  border-bottom: 1px solid var(--border-light);
}

.cart-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 15px;
  font-weight: 700;
  color: var(--text-primary);
}

.cart-count {
  font-size: 12px;
  font-weight: 600;
  color: var(--primary-700);
  background: var(--primary-50);
  padding: 4px 10px;
  border-radius: var(--radius-full);
}

.cart-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px 24px;
  gap: 8px;
}

.cart-empty-icon {
  width: 64px;
  height: 64px;
  border-radius: var(--radius-lg);
  background: var(--neutral-100);
  color: var(--neutral-300);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 4px;
}

.cart-empty-text {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-secondary);
}

.cart-empty-hint {
  font-size: 13px;
  color: var(--text-tertiary);
}

/* Cart List */
.cart-list {
  divide: 1px solid var(--border-light);
}

.cart-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-bottom: 1px solid var(--border-light);
}

.cart-item:last-child {
  border-bottom: none;
}

.cart-item-info {
  flex: 1;
  min-width: 0;
}

.cart-item-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.cart-item-price {
  font-size: 12px;
  color: var(--text-tertiary);
  margin-top: 1px;
}

.cart-item-controls {
  display: flex;
  align-items: center;
  gap: 4px;
}

.qty-btn {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
  background: var(--neutral-100);
  transition: all var(--duration-fast) ease;
}

.qty-btn:hover {
  background: var(--neutral-200);
}

.qty-btn:active {
  transform: scale(0.9);
}

.qty-value {
  width: 32px;
  text-align: center;
  font-size: 15px;
  font-weight: 700;
  color: var(--text-primary);
}

.cart-item-subtotal {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  font-weight: 600;
  color: var(--primary-700);
  white-space: nowrap;
}

.cart-item-remove {
  width: 24px;
  height: 24px;
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--neutral-400);
  transition: all var(--duration-fast) ease;
}

.cart-item-remove:hover {
  background: var(--danger-50);
  color: var(--danger-500);
}

/* Pay Section */
.pay-section {
  background: var(--surface-card);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-light);
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.pay-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.pay-label {
  font-size: 14px;
  color: var(--text-secondary);
}

.pay-value {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
}

.btn-pay {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 16px;
  background: var(--primary-600);
  color: white;
  font-size: 16px;
  font-weight: 700;
  border-radius: var(--radius-md);
  transition: all var(--duration-fast) ease;
}

.btn-pay:hover {
  background: var(--primary-700);
}

.btn-pay:active {
  transform: scale(0.98);
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

.pay-modal-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 12px;
}

.pay-success-icon {
  width: 56px;
  height: 56px;
  border-radius: var(--radius-lg);
  background: var(--primary-50);
  color: var(--primary-600);
  display: flex;
  align-items: center;
  justify-content: center;
}

.pay-modal-title {
  font-size: 20px;
  font-weight: 700;
  color: var(--text-primary);
}

.pay-modal-detail {
  width: 100%;
  background: var(--neutral-50);
  border-radius: var(--radius-md);
  padding: 14px 16px;
  margin: 4px 0;
}

.pay-detail-row {
  display: flex;
  justify-content: space-between;
  font-size: 14px;
  color: var(--text-secondary);
  padding: 4px 0;
}

.pay-detail-row--total {
  border-top: 1px solid var(--border-light);
  margin-top: 8px;
  padding-top: 10px;
  font-size: 16px;
  font-weight: 700;
  color: var(--text-primary);
}

.modal-buttons {
  display: flex;
  gap: 10px;
  width: 100%;
  margin-top: 8px;
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

/* Toast */
.toast-success {
  position: fixed;
  bottom: calc(var(--bottom-nav-height) + 20px);
  left: 50%;
  transform: translateX(-50%);
  z-index: var(--z-toast);
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 20px;
  background: var(--primary-700);
  color: white;
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-lg);
  font-size: 14px;
  font-weight: 600;
  white-space: nowrap;
}

.toast-error {
  position: fixed;
  bottom: calc(var(--bottom-nav-height) + 20px);
  left: 50%;
  transform: translateX(-50%);
  z-index: var(--z-toast);
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 20px;
  background: var(--danger-600);
  color: white;
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-lg);
  font-size: 14px;
  font-weight: 600;
  white-space: nowrap;
}

.btn-loading-spinner {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 0.8s linear infinite;
  display: inline-block;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.toast-enter-active {
  animation: slideUp var(--duration-normal) var(--ease-spring) both;
}

.toast-leave-active {
  animation: fadeIn var(--duration-fast) ease reverse both;
}

/* Responsive */
@media (min-width: 640px) {
  .modal-backdrop {
    align-items: center;
  }

  .modal-sheet {
    border-radius: var(--radius-xl);
    margin: 20px;
  }
}
</style>
