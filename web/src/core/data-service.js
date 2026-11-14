/**
 * KingCounty-AVM: Geospatial & Parcel Data Service
 * Provides zipcode metadata, centroid coordinates, and empirical comps records
 */

export const ZIPCODE_METRICS = {
  "98004": { name: "Bellevue Downtown & Medina", tier: "luxury", medianPrice: 1420000, ppsqft: 542, lat: 47.6101, lon: -122.2015, cluster: 2 },
  "98033": { name: "Kirkland Waterfront District", tier: "luxury", medianPrice: 1180000, ppsqft: 495, lat: 47.6769, lon: -122.2060, cluster: 2 },
  "98039": { name: "Medina Waterfront Estates", tier: "luxury", medianPrice: 2150000, ppsqft: 685, lat: 47.6253, lon: -122.2356, cluster: 3 },
  "98040": { name: "Mercer Island Island-Living", tier: "luxury", medianPrice: 1350000, ppsqft: 520, lat: 47.5707, lon: -122.2221, cluster: 3 },
  "98052": { name: "Redmond High-Tech Corridor", tier: "mid", medianPrice: 940000, ppsqft: 435, lat: 47.6740, lon: -122.1215, cluster: 2 },
  "98101": { name: "Seattle Core & Downtown", tier: "mid", medianPrice: 685000, ppsqft: 460, lat: 47.6101, lon: -122.3344, cluster: 0 },
  "98103": { name: "Green Lake & Fremont", tier: "mid", medianPrice: 745000, ppsqft: 440, lat: 47.6734, lon: -122.3426, cluster: 0 },
  "98105": { name: "University District & Laurelhurst", tier: "mid", medianPrice: 790000, ppsqft: 425, lat: 47.6614, lon: -122.2917, cluster: 0 },
  "98112": { name: "Capitol Hill & Madison Park", tier: "luxury", medianPrice: 1050000, ppsqft: 510, lat: 47.6323, lon: -122.2965, cluster: 0 },
  "98115": { name: "View Ridge & Wedgwood", tier: "mid", medianPrice: 710000, ppsqft: 415, lat: 47.6853, lon: -122.2858, cluster: 0 },
  "98055": { name: "Renton Highlands Suburban", tier: "entry", medianPrice: 425000, ppsqft: 255, lat: 47.4646, lon: -122.1979, cluster: 1 },
  "98031": { name: "Kent East Hill Residential", tier: "entry", medianPrice: 385000, ppsqft: 230, lat: 47.3792, lon: -122.1895, cluster: 1 },
  "98001": { name: "Auburn Valley Green River", tier: "entry", medianPrice: 360000, ppsqft: 215, lat: 47.3073, lon: -122.2778, cluster: 1 },
  "98002": { name: "Auburn Central Valley", tier: "entry", medianPrice: 325000, ppsqft: 205, lat: 47.3089, lon: -122.2212, cluster: 1 },
  "98011": { name: "Bothell North Shore", tier: "mid", medianPrice: 580000, ppsqft: 320, lat: 47.7618, lon: -122.2057, cluster: 4 },
  "98022": { name: "Enumclaw Plateau & Foothills", tier: "entry", medianPrice: 395000, ppsqft: 210, lat: 47.2043, lon: -121.9916, cluster: 5 }
};

export const EMPIRICAL_COMPS = [
  { id: 'C101', address: '10214 SE 18th St, Bellevue', zipcode: '98004', price: 1465000, sqft: 2480, beds: 3, baths: 2.5, grade: 9, lat: 47.6085, lon: -122.1980 },
  { id: 'C102', address: '842 Evergreen Point, Medina', zipcode: '98039', price: 1510000, sqft: 2600, beds: 4, baths: 3.0, grade: 10, lat: 47.6210, lon: -122.2290 },
  { id: 'C103', address: '11832 NE 104th St, Kirkland', zipcode: '98033', price: 1225000, sqft: 2350, beds: 3, baths: 2.0, grade: 9, lat: 47.6890, lon: -122.1890 },
  { id: 'C104', address: '4218 55th Ave NE, Seattle', zipcode: '98105', price: 810000, sqft: 2100, beds: 3, baths: 2.0, grade: 8, lat: 47.6620, lon: -122.2750 },
  { id: 'C105', address: '14210 164th Ave SE, Renton', zipcode: '98055', price: 435000, sqft: 1850, beds: 3, baths: 2.0, grade: 7, lat: 47.4580, lon: -122.1850 },
  { id: 'C106', address: '25612 110th Ave SE, Kent', zipcode: '98031', price: 395000, sqft: 1720, beds: 3, baths: 1.75, grade: 7, lat: 47.3710, lon: -122.1940 }
];

export class DataService {
  static getZipcode(zip) {
    return ZIPCODE_METRICS[zip] || ZIPCODE_METRICS['98004'];
  }

  static getAllZipcodes() {
    return Object.keys(ZIPCODE_METRICS).map(code => ({
      code,
      ...ZIPCODE_METRICS[code]
    }));
  }

  static getParcels() {
    return [...EMPIRICAL_COMPS];
  }
}
