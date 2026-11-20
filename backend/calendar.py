"""
KrishiAI - Smart Crop Calendar Generator
Produces dynamic growth stage timelines with actionable farming milestones,
fertigation checkpoints, pest spray reminders, and harvest windows.
"""
import datetime
from typing import Dict, List, Any

CROP_TIMELINES = {
    "sugarcane": [
        {"day": 0, "title": "Planting & Basal Dose", "desc": "Furrow planting with 2-eye bud setts; apply basal DAP + MOP.", "category": "planting"},
        {"day": 25, "title": "Germination & First Weeding", "desc": "Light irrigation; remove emergent weeds; check sett sprouting.", "category": "weeding"},
        {"day": 60, "title": "Tillering & First Urea Top-dress", "desc": "Apply 30% Urea dose; earthing up to support root tillers.", "category": "fertilizer"},
        {"day": 120, "title": "Grand Growth & Trash Mulching", "desc": "Intense vegetative growth; mulch lower dry leaves to conserve moisture.", "category": "irrigation"},
        {"day": 210, "title": "Stem Elongation & Borer Monitoring", "desc": "Install pheromone traps for top shoot borer; check internode health.", "category": "protection"},
        {"day": 330, "title": "Maturity & Pre-Harvest Brix Check", "desc": "Stop irrigation 15 days before harvest; measure juice brix (>18%).", "category": "harvest"}
    ],
    "cotton": [
        {"day": 0, "title": "Sowing & Seed Treatment", "desc": "Sow treated Bt-cotton seeds with spacing 90x60 cm; apply basal fertilizer.", "category": "planting"},
        {"day": 20, "title": "Seedling Thinning & Hoeing", "desc": "Maintain one healthy seedling per hill; shallow intercultural hoeing.", "category": "weeding"},
        {"day": 45, "title": "Squaring & First Top Dressing", "desc": "Apply Urea + 19:19:19 foliar spray; scout for sucking pests (aphids/jassids).", "category": "fertilizer"},
        {"day": 75, "title": "Flowering & Boll Formation", "desc": "Crucial moisture stage; apply Boron (1g/L) + Planofix to prevent boll drop.", "category": "protection"},
        {"day": 110, "title": "Boll Bursting & Defoliation", "desc": "Monitor pink bollworm; reduce irrigation to avoid boll rot.", "category": "protection"},
        {"day": 150, "title": "First Picking of Cotton", "desc": "Pick clean, dry bolls in morning after dew dries; store in moisture-free shed.", "category": "harvest"}
    ],
    "soybean": [
        {"day": 0, "title": "Sowing & Rhizobium Inoculation", "desc": "Seed inoculation with Rhizobium + PSB; sow at 30 cm row spacing.", "category": "planting"},
        {"day": 20, "title": "First Weeding & Pest Scouting", "desc": "Weed management; install yellow sticky traps for whitefly.", "category": "weeding"},
        {"day": 40, "title": "Flowering & Micro-nutrient Spray", "desc": "Spray 00:52:34 + micro-nutrients; ensure soil has sufficient moisture.", "category": "fertilizer"},
        {"day": 65, "title": "Pod Filling Stage", "desc": "Critical water stage; spray bio-pesticide for pod borer (Helicoverpa).", "category": "protection"},
        {"day": 95, "title": "Maturity & Harvesting", "desc": "Leaves turn golden-yellow and shed; harvest when seed moisture is 14%.", "category": "harvest"}
    ],
    "onion": [
        {"day": 0, "title": "Nursery Sowing / Transplanting", "desc": "Transplant 45-day seedlings at 15x10 cm; apply basal NPK.", "category": "planting"},
        {"day": 25, "title": "Vegetative Growth & Hand Weeding", "desc": "Light frequent irrigation; apply first dose of Urea.", "category": "weeding"},
        {"day": 50, "title": "Bulb Initiation & Thrips Control", "desc": "Spray Neem oil (5ml/L) or Fipronil for thrips; top-dress with Potash.", "category": "protection"},
        {"day": 85, "title": "Bulb Enlargement Stage", "desc": "Maintain optimum moisture; spray 00:00:50 (Potassium sulfate) for bulb size.", "category": "fertilizer"},
        {"day": 120, "title": "Neck Fall & Curing", "desc": "Stop irrigation 10 days before harvest when 50% neck falls; cure under shade.", "category": "harvest"}
    ],
    "wheat": [
        {"day": 0, "title": "Land Prep & Sowing", "desc": "Sow in lines at 20 cm spacing; apply basal DAP + MOP.", "category": "planting"},
        {"day": 21, "title": "Crown Root Initiation (CRI)", "desc": "MOST CRITICAL IRRIGATION! Apply first top dressing of Urea.", "category": "irrigation"},
        {"day": 45, "title": "Tillering Stage", "desc": "Second irrigation; broadleaf weed spray if needed.", "category": "weeding"},
        {"day": 70, "title": "Jointing & Booting", "desc": "Third irrigation; monitor for yellow/brown rust foliar symptoms.", "category": "protection"},
        {"day": 95, "title": "Grain Milking & Dough Stage", "desc": "Light irrigation during grain filling; guard against lodging winds.", "category": "irrigation"},
        {"day": 125, "title": "Golden Ripe Harvesting", "desc": "Harvest when straw turns yellow and grains crack crisply under teeth.", "category": "harvest"}
    ]
}

# Generic fallback for other crops
DEFAULT_TIMELINE = [
    {"day": 0, "title": "Sowing / Land Preparation", "desc": "Prepare seedbed, apply basal compost and NPK nutrients.", "category": "planting"},
    {"day": 25, "title": "Vegetative Establishment", "desc": "First weeding, light irrigation, and nitrogen booster application.", "category": "fertilizer"},
    {"day": 50, "title": "Mid-Season Bloom & Protection", "desc": "Monitor for fungal leaf spots and pests; maintain root moisture.", "category": "protection"},
    {"day": 80, "title": "Fruit / Pod Development", "desc": "Potassium supplementation to support fruit sizing and quality.", "category": "fertilizer"},
    {"day": 110, "title": "Pre-Harvest & Ripening", "desc": "Taper off heavy watering; prepare storage crates/silos.", "category": "harvest"}
]

def generate_crop_calendar(crop: str, start_date_str: str = None) -> Dict[str, Any]:
    """Generates dates, active status, and days remaining for crop events."""
    if not start_date_str:
        start_date = datetime.date.today() - datetime.timedelta(days=28) # Seed as active in-progress
    else:
        try:
            start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
        except Exception:
            start_date = datetime.date.today() - datetime.timedelta(days=28)

    today = datetime.date.today()
    days_elapsed = (today - start_date).days

    crop_key = crop.lower().strip()
    raw_milestones = CROP_TIMELINES.get(crop_key, DEFAULT_TIMELINE)

    total_duration = raw_milestones[-1]["day"]
    progress_percent = min(100, max(0, int((days_elapsed / total_duration) * 100)))

    stages = []
    current_active_stage = None

    for i, m in enumerate(raw_milestones):
        m_day = m["day"]
        target_date = start_date + datetime.timedelta(days=m_day)
        
        if days_elapsed >= m_day:
            status = "completed"
        elif current_active_stage is None:
            status = "current"
            current_active_stage = m["title"]
        else:
            status = "upcoming"

        days_diff = (target_date - today).days

        stages.append({
            "stage_number": i + 1,
            "day": m_day,
            "date": target_date.strftime("%d %b %Y"),
            "title": m["title"],
            "description": m["desc"],
            "category": m["category"],
            "status": status,
            "days_diff": days_diff,
            "alert": f"In {days_diff} days" if days_diff > 0 else (f"{abs(days_diff)} days ago" if days_diff < 0 else "Today!")
        })

    # If all stages completed
    if current_active_stage is None:
        current_active_stage = stages[-1]["title"]

    return {
        "crop": crop.capitalize(),
        "sowing_date": start_date.strftime("%d %b %Y"),
        "days_since_sowing": max(0, days_elapsed),
        "total_crop_days": total_duration,
        "progress_percent": progress_percent,
        "current_active_stage": current_active_stage,
        "timeline": stages
    }
