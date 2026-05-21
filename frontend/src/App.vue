<template>
  <div class="app-shell">
    <!-- Top Bar -->
    <header class="top-bar">
      <div class="top-bar-inner">
        <div class="top-bar-brand">
          <div class="brand-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z"/>
              <line x1="3" y1="6" x2="21" y2="6"/>
              <path d="M16 10a4 4 0 01-8 0"/>
            </svg>
          </div>
          <div>
            <h1 class="brand-name">Toko Sembako</h1>
          </div>
        </div>
        <div class="top-bar-actions">
          <button class="action-btn" aria-label="Notifikasi">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M18 8A6 6 0 006 8c0 7-3 9-3 9h18s-3-2-3-9"/>
              <path d="M13.73 21a2 2 0 01-3.46 0"/>
            </svg>
          </button>
        </div>
      </div>
    </header>

    <!-- Page Content -->
    <main class="main-content">
      <RouterView v-slot="{ Component }">
        <transition name="page" mode="out-in">
          <component :is="Component" />
        </transition>
      </RouterView>
    </main>

    <!-- Bottom Navigation -->
    <nav class="bottom-nav">
      <RouterLink
        v-for="item in navItems"
        :key="item.path"
        :to="item.path"
        class="nav-item"
        :class="{ 'nav-item--active': $route.path === item.path }"
      >
        <div class="nav-icon" v-html="item.icon"></div>
        <span class="nav-label">{{ item.label }}</span>
        <div v-if="$route.path === item.path" class="nav-indicator"></div>
      </RouterLink>
    </nav>
  </div>
</template>

<script setup lang="ts">
const navItems = [
  {
    path: "/",
    label: "Beranda",
    icon: `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>`,
  },
  {
    path: "/kasir",
    label: "Kasir",
    icon: `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 002 1.61h9.72a2 2 0 002-1.61L23 6H6"/></svg>`,
  },
  {
    path: "/produk",
    label: "Produk",
    icon: `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 00-1-1.73l-7-4a2 2 0 00-2 0l-7 4A2 2 0 003 8v8a2 2 0 001 1.73l7 4a2 2 0 002 0l7-4A2 2 0 0021 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg>`,
  },
  {
    path: "/laporan",
    label: "Laporan",
    icon: `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>`,
  },
  {
    path: "/utang",
    label: "Utang",
    icon: `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>`,
  },
];
</script>

<style scoped>
.app-shell {
  min-height: 100vh;
  min-height: 100dvh;
  display: flex;
  flex-direction: column;
  background: var(--surface-body);
}

/* ========================
   Top Bar
   ======================== */
.top-bar {
  position: sticky;
  top: 0;
  z-index: var(--z-sticky);
  background: var(--primary-700);
  color: var(--text-inverse);
}

.top-bar-inner {
  max-width: var(--content-max-width);
  margin: 0 auto;
  padding: 0 20px;
  height: var(--top-bar-height);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.top-bar-brand {
  display: flex;
  align-items: center;
  gap: 10px;
}

.brand-icon {
  width: 36px;
  height: 36px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
}

.brand-name {
  font-size: 17px;
  font-weight: 700;
  letter-spacing: -0.01em;
}

.action-btn {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-inverse);
  transition: background var(--duration-fast) ease;
}

.action-btn:hover {
  background: rgba(255, 255, 255, 0.12);
}

.action-btn:active {
  background: rgba(255, 255, 255, 0.2);
}

/* ========================
   Main Content
   ======================== */
.main-content {
  flex: 1;
  max-width: var(--content-max-width);
  margin: 0 auto;
  width: 100%;
  padding: 20px 20px calc(var(--bottom-nav-height) + 20px);
}

/* ========================
   Bottom Navigation
   ======================== */
.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: var(--z-bottom-nav);
  height: var(--bottom-nav-height);
  background: var(--surface-card);
  border-top: 1px solid var(--border-light);
  box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.06);
  display: flex;
  align-items: center;
  justify-content: space-around;
  padding: 0 8px;
  padding-bottom: env(safe-area-inset-bottom, 0px);
}

.nav-item {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 2px;
  padding: 8px 12px;
  border-radius: var(--radius-md);
  color: var(--neutral-400);
  transition: color var(--duration-fast) ease;
  -webkit-tap-highlight-color: transparent;
  min-width: 56px;
}

.nav-item:active {
  transform: scale(0.92);
}

.nav-item--active {
  color: var(--primary-700);
}

.nav-item--active .nav-icon {
  transform: translateY(-1px);
}

.nav-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform var(--duration-fast) var(--ease-spring);
}

.nav-label {
  font-size: 11px;
  font-weight: 500;
  line-height: 1;
  letter-spacing: 0.01em;
}

.nav-item--active .nav-label {
  font-weight: 600;
}

.nav-indicator {
  position: absolute;
  top: 4px;
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: var(--primary-600);
  animation: scaleIn var(--duration-fast) var(--ease-spring) both;
}

@keyframes scaleIn {
  from { transform: scale(0); }
  to { transform: scale(1); }
}

/* ========================
   Desktop Enhancement
   ======================== */
@media (min-width: 768px) {
  .main-content {
    padding-bottom: calc(var(--bottom-nav-height) + 32px);
  }
  
  .bottom-nav {
    max-width: 480px;
    left: 50%;
    transform: translateX(-50%);
    bottom: 16px;
    border-radius: var(--radius-xl);
    border: 1px solid var(--border-light);
    box-shadow: var(--shadow-xl);
  }
}
</style>
