<template>
  <div>
    <h1 class="text-2xl font-bold text-gray-800 mb-6">Selamat datang!</h1>
    <div class="grid grid-cols-2 gap-4">
      <RouterLink
        to="/kasir"
        class="bg-green-600 text-white rounded-xl p-6 text-center hover:bg-green-700 transition"
      >
        <div class="text-3xl mb-2">🛒</div>
        <div class="font-bold text-lg">Kasir</div>
        <div class="text-sm opacity-80">Catat transaksi</div>
      </RouterLink>
      <RouterLink
        to="/produk"
        class="bg-blue-600 text-white rounded-xl p-6 text-center hover:bg-blue-700 transition"
      >
        <div class="text-3xl mb-2">📦</div>
        <div class="font-bold text-lg">Produk</div>
        <div class="text-sm opacity-80">Kelola stok & harga</div>
      </RouterLink>
      <RouterLink
        to="/laporan"
        class="bg-purple-600 text-white rounded-xl p-6 text-center hover:bg-purple-700 transition"
      >
        <div class="text-3xl mb-2">📊</div>
        <div class="font-bold text-lg">Laporan</div>
        <div class="text-sm opacity-80">Lihat untung/rugi</div>
      </RouterLink>
      <RouterLink
        to="/utang"
        class="bg-orange-500 text-white rounded-xl p-6 text-center hover:bg-orange-600 transition"
      >
        <div class="text-3xl mb-2">📋</div>
        <div class="font-bold text-lg">Utang</div>
        <div class="text-sm opacity-80">Catatan utang pelanggan</div>
      </RouterLink>
    </div>
  </div>
</template>
