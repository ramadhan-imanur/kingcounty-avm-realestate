/**
 * Reactive State Bus for Cross-Feature Synchronization
 * Provides predictable Pub/Sub without global pollution
 */

class AppStore {
  constructor() {
    this.state = {
      activeTab: 'tab-valuator',
      isSidebarCollapsed: false,
      valuation: {
        zip: '98004',
        sqft: 2450,
        grade: 8,
        baths: 2.5,
        beds: 3,
        condition: 3,
        view: 0,
        isWaterfront: false,
        estimatedPrice: 0,
        p10: 0,
        p90: 0,
        effectivePpsqft: 0
      },
      selectedSubmarket: '98004',
      renovation: {
        baseValue: 650000,
        totalCost: 0,
        totalAppreciation: 0,
        netProfit: 0,
        roiPct: 0,
        projectedVal: 650000
      }
    };
    this.listeners = new Map();
  }

  getState() {
    return this.state;
  }

  get(key) {
    return this.state[key];
  }

  set(key, partialValue, silent = false) {
    if (typeof partialValue === 'object' && partialValue !== null && !Array.isArray(partialValue)) {
      this.state[key] = { ...this.state[key], ...partialValue };
    } else {
      this.state[key] = partialValue;
    }
    if (!silent) {
      this.emit(key, this.state[key]);
      this.emit('*', this.state);
    }
  }

  subscribe(event, callback) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, new Set());
    }
    this.listeners.get(event).add(callback);
    return () => this.unsubscribe(event, callback);
  }

  unsubscribe(event, callback) {
    if (this.listeners.has(event)) {
      this.listeners.get(event).delete(callback);
    }
  }

  emit(event, data) {
    if (this.listeners.has(event)) {
      this.listeners.get(event).forEach(cb => {
        try { cb(data); } catch (err) { console.error(`State listener error [${event}]:`, err); }
      });
    }
  }
}

export const store = new AppStore();
