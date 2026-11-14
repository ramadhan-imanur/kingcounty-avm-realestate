/**
 * KingCounty-AVM: Reactive State Management & Event Bus
 * Synchronizes property parameters across Map, Estimator, and Simulator
 */

class Store {
  constructor(initialState) {
    this.state = initialState;
    this.listeners = new Map();
  }

  getState() {
    return { ...this.state };
  }

  setState(partialState) {
    const prevState = { ...this.state };
    this.state = { ...this.state, ...partialState };

    Object.keys(partialState).forEach(key => {
      if (this.listeners.has(key)) {
        this.listeners.get(key).forEach(cb => cb(this.state[key], prevState[key], this.state));
      }
    });

    if (this.listeners.has('*')) {
      this.listeners.get('*').forEach(cb => cb(this.state, prevState));
    }
  }

  subscribe(key, callback) {
    if (!this.listeners.has(key)) {
      this.listeners.set(key, new Set());
    }
    this.listeners.get(key).add(callback);
    return () => this.listeners.get(key).delete(callback);
  }
}

export const appStore = new Store({
  activeTab: 'estimator', // 'estimator' | 'map' | 'analytics' | 'simulator'
  sidebarCollapsed: false,
  
  // Current active property being analyzed
  property: {
    zipcode: '98004',
    sqft_living: 2450,
    sqft_lot: 7500,
    bedrooms: 3,
    bathrooms: 2.5,
    grade: 9,
    condition: 4,
    yr_built: 1998,
    is_renovated: 1,
    waterfront: 0,
    has_view: 1,
    lat: 47.6101,
    lon: -122.2015
  },

  // Valuation model outputs
  valuation: {
    estimatedPrice: 1420000,
    p10: 1258120,
    p90: 1581880,
    pricePerSqFt: 580,
    tier: 'luxury',
    clusterId: 2,
    clusterName: 'Eastside High-Tech Corridor',
    shap: []
  },

  // Investment simulation inputs
  investment: {
    downPaymentPct: 20,
    interestRate: 6.5,
    loanTermYears: 30,
    monthlyRentEstimate: 4500,
    activeRenovations: ['kitchen']
  }
});
