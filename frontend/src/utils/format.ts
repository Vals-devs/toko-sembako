export function formatRupiah(angka: number): string {
  return "Rp " + (angka || 0).toLocaleString("id-ID");
}

export function formatRupiahShort(angka: number): string {
  if (angka >= 1_000_000) return "Rp " + (angka / 1_000_000).toFixed(1) + "jt";
  if (angka >= 1_000) return "Rp " + (angka / 1_000).toFixed(0) + "rb";
  return "Rp " + angka;
}

export function formatTanggal(isoString: string, opts?: Intl.DateTimeFormatOptions): string {
  if (!isoString) return "";
  return new Date(isoString).toLocaleDateString("id-ID", opts);
}
