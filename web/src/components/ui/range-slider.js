/**
 * KingCounty-AVM: Range Slider Component
 * Standardized input slider with synchronized numeric badge
 */

export function createRangeSlider({ id, label, min, max, value, step = 1, unit = '', onChange }) {
  const container = document.createElement('div');
  container.className = 'flex flex-col gap-1.5';

  container.innerHTML = `
    <div class="flex justify-between items-center text-xs">
      <label for="${id}" class="font-medium text-slate-700">${label}</label>
      <span id="${id}-display" class="font-mono font-bold text-slate-900 bg-slate-100 px-2 py-0.5 rounded text-xs">
        ${value}${unit ? ' ' + unit : ''}
      </span>
    </div>
    <input 
      type="range" 
      id="${id}" 
      min="${min}" 
      max="${max}" 
      value="${value}" 
      step="${step}" 
      class="w-full accent-emerald-600 cursor-pointer h-2 bg-slate-200 rounded-lg"
    />
  `;

  const input = container.querySelector('input');
  const display = container.querySelector(`#${id}-display`);

  input.addEventListener('input', (e) => {
    const val = Number(e.target.value);
    display.textContent = `${val}${unit ? ' ' + unit : ''}`;
    if (onChange) onChange(val);
  });

  return container;
}
