/**
 * KingCounty-AVM: Market KPI Stat Cards Component
 * High-fidelity metrics matching regional housing benchmarks
 */

export function renderMarketKpiCards() {
  const wrapper = document.createElement('div');
  wrapper.className = 'grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4';

  wrapper.innerHTML = `
    <!-- Card 1: Total Sales -->
    <div class="glass-card p-4 flex flex-col justify-between gap-2.5">
      <div class="flex items-center justify-between">
        <span class="text-[10px] font-mono font-bold uppercase tracking-wider text-slate-500">Total Rumah Terjual</span>
        <span class="text-[10px] font-mono font-semibold px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200">Terverifikasi</span>
      </div>
      <div>
        <div class="text-2xl font-black text-slate-900 tracking-tight font-mono">22.847</div>
        <div class="text-[11px] text-slate-500 mt-0.5">Transaksi resmi di King County</div>
      </div>
      <div class="pt-2 border-t border-slate-100 flex items-center gap-1.5 text-[10px] font-mono text-emerald-700">
        <svg class="w-3.5 h-3.5 text-emerald-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
        <span>Pembersihan Data: <b>100% Bersih</b></span>
      </div>
    </div>

    <!-- Card 2: Median Price -->
    <div class="glass-card p-4 flex flex-col justify-between gap-2.5">
      <div class="flex items-center justify-between">
        <span class="text-[10px] font-mono font-bold uppercase tracking-wider text-slate-500">Harga Tengah (Median)</span>
        <span class="text-[10px] font-mono font-semibold px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200">+8,4% YoY</span>
      </div>
      <div>
        <div class="text-2xl font-black text-slate-900 tracking-tight font-mono">$450.000</div>
        <div class="text-[11px] text-slate-500 mt-0.5">Nilai patokan umum rumah tinggal</div>
      </div>
      <div class="pt-2 border-t border-slate-100 text-[10px] font-mono text-slate-500">
        Rentang IQR: <span class="font-bold text-slate-800">$322k &ndash; $645k</span>
      </div>
    </div>

    <!-- Card 3: Avg per sqft -->
    <div class="glass-card p-4 flex flex-col justify-between gap-2.5">
      <div class="flex items-center justify-between">
        <span class="text-[10px] font-mono font-bold uppercase tracking-wider text-slate-500">Rata-rata per Ukuran</span>
        <span class="text-[10px] font-mono font-semibold px-2 py-0.5 rounded-full bg-sky-50 text-sky-700 border border-sky-200">Per Sq.Ft</span>
      </div>
      <div>
        <div class="text-2xl font-black text-slate-900 tracking-tight font-mono">$284 <span class="text-xs font-normal text-slate-400">/ sq.ft</span></div>
        <div class="text-[11px] text-slate-500 mt-0.5">Biaya rata-rata luas bangunan</div>
      </div>
      <div class="pt-2 border-t border-slate-100 flex items-center justify-between text-[10px] font-mono text-slate-500">
        <span>Bellevue: <b class="text-slate-800">$542</b></span>
        <span>Seattle: <b class="text-slate-800">$460</b></span>
      </div>
    </div>

    <!-- Card 4: Segment Distribution -->
    <div class="glass-card p-4 flex flex-col justify-between gap-2.5">
      <div class="flex items-center justify-between">
        <span class="text-[10px] font-mono font-bold uppercase tracking-wider text-slate-500">Distribusi Segmen</span>
        <span class="text-[10px] font-mono font-semibold px-2 py-0.5 rounded-full bg-purple-50 text-purple-700 border border-purple-200">3 Tier</span>
      </div>
      <div>
        <div class="text-xl font-black text-slate-900 tracking-tight font-mono">32% <span class="text-slate-300 font-light">/</span> 48% <span class="text-slate-300 font-light">/</span> 20%</div>
        <div class="text-[10px] text-slate-500 mt-0.5">Terjangkau &bull; Menengah &bull; Mewah</div>
      </div>
      <div class="pt-2 border-t border-slate-100 flex flex-col gap-1">
        <div class="w-full h-1.5 rounded-full overflow-hidden flex bg-slate-100">
          <div class="h-full bg-teal-500" style="width: 32%"></div>
          <div class="h-full bg-sky-500" style="width: 48%"></div>
          <div class="h-full bg-purple-600" style="width: 20%"></div>
        </div>
      </div>
    </div>
  `;

  return wrapper;
}
