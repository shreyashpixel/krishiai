"""
KrishiAI - Demo Walkthrough Scripts & Preset Showcases
Coordinates presentation flow for college project evaluations and viva demonstrations.
"""
from typing import Dict, List, Any

DEMO_STEPS = [
    {
        "step": 1,
        "tab": "dashboard",
        "title": "1. Live IoT Farm Dashboard",
        "narrative": "Welcome to KrishiAI! The dashboard aggregates live telemetry from our simulated LoRaWAN IoT field nodes: Soil Moisture, Temperature, Humidity, pH, and N-P-K nutrients, synthesizing an aggregate Farm Health Index (0-100).",
        "action": "highlight_overview"
    },
    {
        "step": 2,
        "tab": "dashboard",
        "title": "2. Real-time Anomaly Simulation (Drought Injection)",
        "narrative": "Watch the system respond to environmental stress! We simulate an abrupt field drought event: soil moisture drops, temperature rises, and the health index drops, triggering a critical alert.",
        "action": "trigger_drought"
    },
    {
        "step": 3,
        "tab": "irrigation",
        "title": "3. Smart Irrigation Automation",
        "narrative": "The Smart Irrigation Planner detects moisture deficit and calculates the precise micro-drip water quota needed (saving over 50% water vs flood irrigation) and schedules irrigation.",
        "action": "plan_irrigation"
    },
    {
        "step": 4,
        "tab": "crops",
        "title": "4. Machine Learning Crop Recommendation",
        "narrative": "Our Random Forest ML model analyzes current soil NPK, pH, and local agro-climatic conditions across 24 crops to recommend the top 3 optimal crops with confidence percentages.",
        "action": "run_crop_rec"
    },
    {
        "step": 5,
        "tab": "disease",
        "title": "5. Foliar Disease Pathology & Severity",
        "narrative": "Using lightweight computer vision and HSV chromatic lesion extraction, KrishiAI detects foliar leaf blight, calculates severity percentage, and provides both biological and chemical treatments.",
        "action": "scan_sample_leaf"
    },
    {
        "step": 6,
        "tab": "fertilizer",
        "title": "6. Precision Fertilizer & Eco-Protocol",
        "narrative": "Instead of blanket chemical broadcasting, KrishiAI calculates exact 45kg/50kg bags of Urea, DAP, and MOP based on soil deficits, backed by an organic regenerative protocol.",
        "action": "calc_fertilizer"
    },
    {
        "step": 7,
        "tab": "yield",
        "title": "7. Yield & APMC Mandi Profitability",
        "narrative": "Combining agronomic yield curves with live APMC mandi market prices, the model projects total yield, cultivation expenses, gross revenue, and net profit with ROI.",
        "action": "calc_yield"
    },
    {
        "step": 8,
        "tab": "weather",
        "title": "8. Open-Meteo Weather & Crop Calendar",
        "narrative": "The system pulls real-time 7-day meteorological forecasts to provide actionable spraying advisories and tracks the crop stage timeline from sowing to harvesting.",
        "action": "show_weather"
    },
    {
        "step": 9,
        "tab": "sustainability",
        "title": "9. Carbon Footprint & One-Click PDF Report",
        "narrative": "KrishiAI quantifies groundwater conserved and CO2 greenhouse emissions avoided. Finally, click 'Download PDF Report' for a submission-ready documentation package!",
        "action": "show_sustainability"
    }
]

def get_demo_walkthrough() -> List[Dict[str, Any]]:
    return DEMO_STEPS
