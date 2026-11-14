/**
 * KingCounty-AVM: Financial Feasibility & Mortgage Mathematics Engine
 */

export function calculateMonthlyMortgage(principal, annualRatePct, years) {
  if (principal <= 0) return 0;
  const monthlyRate = (annualRatePct / 100) / 12;
  const numPayments = years * 12;

  if (monthlyRate === 0) return Math.round(principal / numPayments);

  const factor = Math.pow(1 + monthlyRate, numPayments);
  const monthlyPayment = principal * ((monthlyRate * factor) / (factor - 1));

  return Math.round(monthlyPayment);
}

export function calculateCapRate(propertyPrice, monthlyRent, opexRatio = 0.35) {
  if (propertyPrice <= 0) return 0;
  const annualGrossRent = monthlyRent * 12;
  const netOperatingIncome = annualGrossRent * (1 - opexRatio);
  return (netOperatingIncome / propertyPrice) * 100;
}

export function calculatePriceToRentRatio(propertyPrice, monthlyRent) {
  if (monthlyRent <= 0) return 0;
  return propertyPrice / (monthlyRent * 12);
}

export const RENOVATION_PACKAGES = [
  { id: 'bath', name: 'Tambah Kamar Mandi Penuh (Full Bath)', cost: 24000, appreciation: 38500, roi: 160 },
  { id: 'kitchen', name: 'Renovasi Dapur Koki Modern (Chef\'s Kitchen)', cost: 48000, appreciation: 72000, roi: 150 },
  { id: 'basement', name: 'Finishing Daylight Basement (+600 sqft)', cost: 36000, appreciation: 52000, roi: 144 },
  { id: 'deck', name: 'Dek Kayu Komposit & Outdoor Living (300 sqft)', cost: 16000, appreciation: 22500, roi: 140 },
  { id: 'grade', name: 'Peningkatan Grade Arsitektural (+1 Tingkat)', cost: 65000, appreciation: 125000, roi: 192 },
  { id: 'energy', name: 'Efisiensi Energi & Heat Pump Inverter HVAC', cost: 15000, appreciation: 19500, roi: 130 }
];
