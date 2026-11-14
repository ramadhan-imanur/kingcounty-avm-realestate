/**
 * KingCounty-AVM: Pure SVG Bar Chart & Distribution Wrapper
 * Zero external dependencies; lightweight and resilient
 */

export function renderHorizontalBarChart(items, maxValue = null) {
  if (!items || items.length === 0) return '';
  const max = maxValue || Math.max(...items.map(d => Math.abs(d.value)));

  return `
    <div class="flex flex-col gap-2.5 w-full text-xs">
      ${items.map(item => {
        const pct = Math.min(100, Math.round((Math.abs(item.value) / (max || 1)) * 100));
        const isPos = item.value >= 0;
        const color = isPos ? 'bg-emerald-600' : 'bg-rose-600';

        return `
          <div class="flex flex-col gap-1">
            <div class="flex justify-between items-center text-[11px]">
              <span class="font-medium text-slate-700 truncate max-w-[200px]">${item.label}</span>
              <span class="font-mono font-bold ${isPos ? 'text-emerald-700' : 'text-rose-700'}">
                ${isPos ? '+' : ''}${item.displayValue || item.value}
              </span>
            </div>
            <div class="w-full bg-slate-100 rounded-full h-2 overflow-hidden">
              <div class="${color} h-full rounded-full transition-all duration-300" style="width: ${pct}%"></div>
            </div>
          </div>
        `;
      }).join('')}
    </div>
  `;
}

export function renderSparkline(values, width = 120, height = 30) {
  if (!values || values.length < 2) return '';
  const min = Math.min(...values);
  const max = Math.max(...values);
  const range = max - min || 1;

  const points = values.map((v, i) => {
    const x = (i / (values.length - 1)) * width;
    const y = height - ((v - min) / range) * (height - 6) - 3;
    return `${x.toFixed(1)},${y.toFixed(1)}`;
  }).join(' ');

  return `
    <svg width="${width}" height="${height}" class="overflow-visible">
      <polyline fill="none" stroke="#006948" stroke-width="2" points="${points}" />
    </svg>
  `;
}
