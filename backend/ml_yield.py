"""
KrishiAI - Crop Yield & Mandi Profit Predictor
Simulates agronomic regression & APMC market economics to calculate
expected yield, cultivation costs, market revenues, net profit, and ROI.
"""
from typing import Dict, Any
from backend.config import CROP_ECONOMICS, DEFAULT_CROP_ECONOMIC

def predict_yield_and_profit(
    crop: str,
    area_acres: float,
    season: str = "Kharif",
    soil_type: str = "Medium Black Soil",
    irrigation_type: str = "Drip Irrigation"
) -> Dict[str, Any]:
    """
    Computes expected crop yield and economic returns based on farm inputs,
    management practice, and live APMC mandi pricing models.
    """
    crop_lower = crop.lower().strip()
    econ = CROP_ECONOMICS.get(crop_lower, DEFAULT_CROP_ECONOMIC)

    # Base ranges
    min_yield, max_yield = econ["yield_range"]
    base_cost_per_acre = econ["cost_per_acre"]
    mandi_price_per_q = econ["mandi_price"]
    unit = econ["unit"]

    # Irrigation multiplier
    irrigation_mults = {
        "Drip Irrigation": {"yield": 1.18, "cost": 0.95}, # precision saving
        "Sprinkler": {"yield": 1.08, "cost": 1.00},
        "Flood / Furrow": {"yield": 1.00, "cost": 1.10}, # higher labor & weed cost
        "Rainfed / Dryland": {"yield": 0.75, "cost": 0.80}
    }
    irrig_factor = irrigation_mults.get(irrigation_type, {"yield": 1.0, "cost": 1.0})

    # Soil multiplier
    soil_mults = {
        "Deep Black Cotton Soil": 1.06,
        "Medium Black Soil": 1.02,
        "Loamy Soil": 1.05,
        "Sandy Loam": 0.96,
        "Red Soil": 0.94,
        "Clay Loam": 1.03
    }
    soil_factor = soil_mults.get(soil_type, 1.0)

    # Calculate average expected yield per acre
    avg_base_yield = (min_yield + max_yield) / 2.0
    adjusted_yield_per_acre = round(avg_base_yield * irrig_factor["yield"] * soil_factor, 2)
    total_yield = round(adjusted_yield_per_acre * area_acres, 2)

    # Cost breakdown per acre
    adjusted_cost_per_acre = round(base_cost_per_acre * irrig_factor["cost"], 2)
    total_cost = round(adjusted_cost_per_acre * area_acres, 2)

    seeds_cost = round(total_cost * 0.15, 2)
    fertilizer_cost = round(total_cost * 0.25, 2)
    irrigation_power_cost = round(total_cost * 0.12, 2)
    labor_machinery_cost = round(total_cost * 0.32, 2)
    plant_protection_cost = round(total_cost * 0.16, 2)

    # Gross revenue & profit
    gross_revenue = round(total_yield * mandi_price_per_q, 2)
    net_profit = round(gross_revenue - total_cost, 2)
    profit_per_acre = round(net_profit / max(0.1, area_acres), 2)

    roi_percent = round((net_profit / max(1.0, total_cost)) * 100, 1)
    breakeven_price = round(total_cost / max(0.1, total_yield), 1)

    # Market insights
    if net_profit > 0:
        market_sentiment = "Highly Profitable" if roi_percent > 80 else "Moderate Profitability"
    else:
        market_sentiment = "Margin Under Pressure (Consider Drip / Lower Input Costs)"

    recommendation = (
        f"Following smart precision irrigation and balanced NPK will secure approximately {total_yield} {unit}s. "
        f"Selling at current APMC mandi benchmark ₹{mandi_price_per_q}/{unit} yields a net margin of ₹{net_profit:,.0f}."
    )

    return {
        "crop": crop.capitalize(),
        "area_acres": area_acres,
        "season": season,
        "soil_type": soil_type,
        "irrigation_type": irrigation_type,
        "yield_per_acre": adjusted_yield_per_acre,
        "total_expected_yield": total_yield,
        "unit": unit,
        "mandi_price_per_unit": mandi_price_per_q,
        "cost_per_acre": adjusted_cost_per_acre,
        "total_cost": total_cost,
        "gross_revenue": gross_revenue,
        "net_profit": net_profit,
        "profit_per_acre": profit_per_acre,
        "roi_percent": roi_percent,
        "breakeven_price": breakeven_price,
        "market_sentiment": market_sentiment,
        "recommendation": recommendation,
        "cost_breakdown": {
            "Seeds & Planting": seeds_cost,
            "Fertilizers & Nutrients": fertilizer_cost,
            "Irrigation & Electricity": irrigation_power_cost,
            "Labor & Mechanization": labor_machinery_cost,
            "Crop Protection (Biocides)": plant_protection_cost
        }
    }
