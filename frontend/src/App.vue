<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navbar -->
    <nav class="bg-green-700 text-white shadow-md">
      <div
        class="max-w-5xl mx-auto px-4 py-3 flex items-center justify-between"
      >
        <span class="font-bold text-lg">Toko Sembako</span>
        <div class="flex gap-2">
          <RouterLink
            v-for="menu in menus"
            :key="menu.path"
            :to="menu.path"
            class="px-3 py-1.5 rounded text-sm font-medium transition-colors"
            :class="
              $route.path === menu.path
                ? 'bg-white text-green-700'
                : 'hover:bg-green-600'
            "
          >
            {{ menu.label }}
          </RouterLink>
        </div>
      </div>
    </nav>

    <!-- Konten halaman -->
    <main class="max-w-5xl mx-auto px-4 py-6">
      <RouterView />
    </main>
  </div>
</template>

<script setup lang="ts">
const menus = [
  { path: "/", label: "Beranda" },
  { path: "/kasir", label: "Kasir" },
  { path: "/produk", label: "Produk" },
  { path: "/laporan", label: "Laporan" },
  { path: "/utang", label: "Utang" },
];
</script>
