"""
KrishiAI - Carbon & Water Sustainability Footprint Meter
Quantifies ecological resources conserved (water, fertilizer, electricity)
and calculates carbon emission mitigation (kg CO2e).
"""
from typing import Dict, Any

def calculate_sustainability_metrics(
    farm_area_acres: float = 3.5,
    crop: str = "sugarcane",
    irrigation_cycles_count: int = 42
) -> Dict[str, Any]:
    """
    Computes environmental footprint reduction through AI sensor precision farming.
    """
    # 1. Water Conservation:
    # Flood irrigation typically uses ~60,000 litres/acre/cycle.
    # Precision sensor-driven drip uses ~28,000 litres/acre/cycle.
    # Water saved = ~32,000 litres/acre/cycle.
    water_saved_per_acre_cycle = 32000
    total_water_saved_litres = int(water_saved_per_acre_cycle * farm_area_acres * (irrigation_cycles_count * 0.75))

    # Water savings percentage
    water_saving_pct = 52.5

    # 2. Chemical Fertilizer Reduction:
    # Soil testing avoids average 40 kg excess urea/acre over-application.
    nitrogen_saved_kg = round(40.0 * farm_area_acres, 1)

    # 3. Energy & Carbon Footprint Calculation:
    # Pumping energy saved: 0.35 kWh per 1000L = kWh saved
    pumping_kwh_saved = round((total_water_saved_litres / 1000.0) * 0.35, 1)
    co2_pump_saved = pumping_kwh_saved * 0.82 # 0.82 kg CO2 per kWh grid electricity

    # Urea manufacturing & N2O soil emission footprint:
    # ~2.98 kg CO2e per kg excess urea avoided
    co2_urea_saved = nitrogen_saved_kg * 2.98

    total_co2e_saved_kg = round(co2_pump_saved + co2_urea_saved, 1)

    # Equivalent trees planted (1 mature tree absorbs ~22 kg CO2/year)
    trees_equivalent = round(total_co2e_saved_kg / 22.0, 1)

    # Sustainability Index (0 - 100)
    sustainability_index = min(98, int(72 + (water_saving_pct * 0.3) + min(15, total_co2e_saved_kg / 200)))

    # Eco Badges earned
    badges = [
        {"name": "Water Guardian", "desc": f"Saved {total_water_saved_litres:,} Litres of groundwater", "icon": "droplet"},
        {"name": "Climate Smart Farmer", "desc": f"Avoided {total_co2e_saved_kg:,.0f} kg greenhouse CO2 emissions", "icon": "leaf"},
        {"name": "Soil Regenerator", "desc": f"Prevented {nitrogen_saved_kg} kg nitrate runoff", "icon": "shield-check"}
    ]

    return {
        "farm_area_acres": farm_area_acres,
        "crop": crop.capitalize(),
        "sustainability_index": sustainability_index,
        "water_saved_litres": total_water_saved_litres,
        "water_saved_m3": round(total_water_saved_litres / 1000.0, 1),
        "water_saving_percent": water_saving_pct,
        "nitrogen_saved_kg": nitrogen_saved_kg,
        "pumping_kwh_saved": pumping_kwh_saved,
        "total_co2e_saved_kg": total_co2e_saved_kg,
        "trees_equivalent": trees_equivalent,
        "badges": badges,
        "eco_summary": (
            f"By utilizing KrishiAI IoT precision irrigation and soil-test-based fertilizer dosage across {farm_area_acres} acres, "
            f"your farm has conserved {total_water_saved_litres:,} litres of freshwater and offset {total_co2e_saved_kg:,.0f} kg of CO2e. "
            f"This ecological impact is equivalent to planting {trees_equivalent} mature trees!"
        )
    }
