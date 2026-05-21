import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      name: "home",
      component: () => import("@/views/HomeView.vue"),
    },
    {
      path: "/produk",
      name: "produk",
      component: () => import("@/views/ProdukView.vue"),
    },
    {
      path: "/kasir",
      name: "kasir",
      component: () => import("@/views/KasirView.vue"),
    },
    {
      path: "/laporan",
      name: "laporan",
      component: () => import("@/views/LaporanView.vue"),
    },
    {
      path: "/utang",
      name: "utang",
      component: () => import("@/views/UtangView.vue"),
    },
  ],
});

export default router;
