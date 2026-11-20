"""
KrishiAI - Precision Fertilizer & Nutrient Calculator
Calculates exact chemical fertilizer requirements (Urea, DAP, MOP) based on soil test deficits
along with sustainable, eco-friendly organic alternatives.
"""
from typing import Dict, Any
from backend.config import CROP_AGRONOMY

def calculate_fertilizer_recommendation(
    crop: str,
    soil_n: float,
    soil_p: float,
    soil_k: float,
    area_acres: float = 1.0
) -> Dict[str, Any]:
    """
    Computes chemical fertilizer quantities (kg & bags) and sustainable bio-organic replacements.
    """
    crop_lower = crop.lower().strip()
    agronomy = CROP_AGRONOMY.get(crop_lower, {
        "N": (70, 100), "P": (40, 60), "K": (40, 60)
    })

    target_n = (agronomy["N"][0] + agronomy["N"][1]) / 2.0
    target_p = (agronomy["P"][0] + agronomy["P"][1]) / 2.0
    target_k = (agronomy["K"][0] + agronomy["K"][1]) / 2.0

    # Deficits per acre (converted from kg/ha: 1 ha ~ 2.47 acres)
    # Target values in CROP_AGRONOMY are kg/ha
    HA_TO_ACRE = 0.4047

    target_n_acre = target_n * HA_TO_ACRE
    target_p_acre = target_p * HA_TO_ACRE
    target_k_acre = target_k * HA_TO_ACRE

    def_n = max(0.0, target_n_acre - soil_n)
    def_p = max(0.0, target_p_acre - soil_p)
    def_k = max(0.0, target_k_acre - soil_k)

    # 1. DAP (18% N, 46% P2O5)
    # Satisfies Phosphorus first
    dap_kg_per_acre = round(def_p / 0.46, 1) if def_p > 0 else 0.0
    n_supplied_by_dap = dap_kg_per_acre * 0.18

    # 2. Urea (46% N)
    remaining_n = max(0.0, def_n - n_supplied_by_dap)
    urea_kg_per_acre = round(remaining_n / 0.46, 1)

    # 3. MOP (Muriate of Potash, 60% K2O)
    mop_kg_per_acre = round(def_k / 0.60, 1) if def_k > 0 else 0.0

    # Total farm requirements
    total_dap_kg = round(dap_kg_per_acre * area_acres, 1)
    total_urea_kg = round(urea_kg_per_acre * area_acres, 1)
    total_mop_kg = round(mop_kg_per_acre * area_acres, 1)

    # In 50kg standard bags
    dap_bags = round(total_dap_kg / 50.0, 1)
    urea_bags = round(total_urea_kg / 45.0, 1) # Urea is standard 45kg bag in India
    mop_bags = round(total_mop_kg / 50.0, 1)

    # Status assessment
    n_status = "Optimal" if def_n <= 5 else ("Deficient" if def_n > 15 else "Slightly Low")
    p_status = "Optimal" if def_p <= 3 else ("Deficient" if def_p > 10 else "Slightly Low")
    k_status = "Optimal" if def_k <= 4 else ("Deficient" if def_k > 12 else "Slightly Low")

    return {
        "crop": crop.capitalize(),
        "area_acres": area_acres,
        "soil_test": {"N": soil_n, "P": soil_p, "K": soil_k},
        "target_nutrients_per_acre": {
            "N": round(target_n_acre, 1),
            "P": round(target_p_acre, 1),
            "K": round(target_k_acre, 1)
        },
        "nutrient_status": {
            "nitrogen": n_status,
            "phosphorus": p_status,
            "potassium": k_status
        },
        "deficits_per_acre": {
            "N": round(def_n, 1),
            "P": round(def_p, 1),
            "K": round(def_k, 1)
        },
        "commercial_recommendations": {
            "urea": {
                "kg_per_acre": urea_kg_per_acre,
                "total_kg": total_urea_kg,
                "bags_45kg": urea_bags,
                "nutrient": "Nitrogen (46% N)"
            },
            "dap": {
                "kg_per_acre": dap_kg_per_acre,
                "total_kg": total_dap_kg,
                "bags_50kg": dap_bags,
                "nutrient": "Phosphorus (46% P2O5) + 18% N"
            },
            "mop": {
                "kg_per_acre": mop_kg_per_acre,
                "total_kg": total_mop_kg,
                "bags_50kg": mop_bags,
                "nutrient": "Potash (60% K2O)"
            }
        },
        "split_application_schedule": [
            {
                "stage": "Basal Dose (At Sowing / Transplanting)",
                "application": f"100% DAP ({dap_kg_per_acre} kg/ac) + 50% MOP ({round(mop_kg_per_acre*0.5, 1)} kg/ac) + 25% Urea ({round(urea_kg_per_acre*0.25, 1)} kg/ac)"
            },
            {
                "stage": "First Top Dressing (30 Days - Vegetative)",
                "application": f"50% Urea ({round(urea_kg_per_acre*0.5, 1)} kg/ac) through fertigation or side placement."
            },
            {
                "stage": "Second Top Dressing (60 Days - Flowering / Panicle)",
                "application": f"Remaining 25% Urea ({round(urea_kg_per_acre*0.25, 1)} kg/ac) + 50% MOP ({round(mop_kg_per_acre*0.5, 1)} kg/ac)."
            }
        ],
        "eco_friendly_alternative": {
            "title": "Natural Soil Regeneration & Biofertilizer Protocol",
            "fym_vermicompost": f"{round(1.5 * area_acres, 1)} tons of well-decomposed Vermicompost / FYM enriched with Trichoderma.",
            "neem_cake": f"{int(100 * area_acres)} kg Neem Seed Cake (slows nitrogen leaching and acts as bio-nematicide).",
            "biofertilizers": [
                "Azotobacter / Rhizobium: 2 kg/acre (Fixes 20-30 kg atmospheric N naturally)",
                "PSB (Phosphate Solubilizing Bacteria): 2 kg/acre (Solubilizes fixed insoluble phosphorus in soil)",
                "KMB (Potash Mobilizing Bacteria): 2 kg/acre (Mobilizes mineral potash for root absorption)"
            ],
            "liquid_tonics": "Spray Jeevamrutha or Panchagavya @ 3% concentration every 15-20 days."
        }
    }
