"""
KrishiAI - Configuration & System Constants
"""
import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = BASE_DIR / "backend"
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
FRONTEND_DIR = BASE_DIR / "frontend"
STATIC_DIR = FRONTEND_DIR

# Ensure directories exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DATA_DIR / "krishiai.db"
CROP_MODEL_PATH = MODELS_DIR / "crop_rf_model.pkl"
DISEASE_MODEL_PATH = MODELS_DIR / "disease_model.pkl"
DATASET_PATH = DATA_DIR / "crop_dataset.csv"

# Geographic Defaults (Pune, Maharashtra, India)
DEFAULT_LOCATION = {
    "city": "Pune",
    "state": "Maharashtra",
    "country": "India",
    "latitude": 18.5204,
    "longitude": 73.8567,
    "elevation": 560
}

# 24 Key Agricultural Crops (Comprehensive India + Maharashtra focus)
SUPPORTED_CROPS = [
    "rice", "wheat", "maize", "cotton", "sugarcane", 
    "soybean", "jowar", "bajra", "onion", "grapes", 
    "pomegranate", "chickpea", "kidneybeans", "pigeonpeas", 
    "mothbeans", "mungbean", "blackgram", "lentil", 
    "watermelon", "muskmelon", "apple", "orange", 
    "banana", "coconut"
]

# Agronomic optimal parameters (N, P, K in kg/ha, Temp in °C, Humidity %, pH, Rainfall in mm)
CROP_AGRONOMY = {
    "rice": {"N": (60, 90), "P": (35, 60), "K": (35, 45), "temp": (20, 27), "humidity": (80, 85), "ph": (5.5, 7.2), "rainfall": (180, 300)},
    "wheat": {"N": (80, 120), "P": (40, 60), "K": (40, 50), "temp": (15, 24), "humidity": (50, 70), "ph": (6.0, 7.5), "rainfall": (50, 100)},
    "maize": {"N": (70, 100), "P": (40, 60), "K": (18, 25), "temp": (20, 30), "humidity": (55, 75), "ph": (5.8, 7.5), "rainfall": (60, 120)},
    "cotton": {"N": (100, 140), "P": (40, 60), "K": (40, 60), "temp": (24, 34), "humidity": (60, 80), "ph": (6.0, 8.0), "rainfall": (60, 120)},
    "sugarcane": {"N": (120, 160), "P": (60, 85), "K": (60, 90), "temp": (22, 35), "humidity": (65, 85), "ph": (6.0, 7.8), "rainfall": (120, 250)},
    "soybean": {"N": (20, 40), "P": (60, 80), "K": (30, 45), "temp": (20, 30), "humidity": (60, 80), "ph": (6.0, 7.5), "rainfall": (65, 110)},
    "jowar": {"N": (40, 60), "P": (20, 35), "K": (20, 30), "temp": (25, 35), "humidity": (45, 65), "ph": (6.0, 8.5), "rainfall": (40, 80)},
    "bajra": {"N": (40, 60), "P": (20, 30), "K": (15, 25), "temp": (26, 36), "humidity": (40, 60), "ph": (6.5, 8.5), "rainfall": (35, 70)},
    "onion": {"N": (50, 80), "P": (40, 60), "K": (60, 85), "temp": (15, 28), "humidity": (55, 75), "ph": (6.0, 7.2), "rainfall": (50, 90)},
    "grapes": {"N": (20, 40), "P": (120, 145), "K": (195, 205), "temp": (15, 32), "humidity": (60, 85), "ph": (6.0, 7.5), "rainfall": (60, 100)},
    "pomegranate": {"N": (20, 40), "P": (10, 30), "K": (35, 50), "temp": (22, 35), "humidity": (45, 65), "ph": (6.5, 7.8), "rainfall": (50, 80)},
    "chickpea": {"N": (35, 45), "P": (55, 70), "K": (75, 85), "temp": (17, 22), "humidity": (15, 20), "ph": (6.0, 7.5), "rainfall": (65, 95)},
    "kidneybeans": {"N": (15, 35), "P": (55, 70), "K": (18, 25), "temp": (18, 24), "humidity": (55, 60), "ph": (5.5, 6.0), "rainfall": (60, 150)},
    "pigeonpeas": {"N": (18, 30), "P": (60, 75), "K": (18, 25), "temp": (25, 35), "humidity": (45, 65), "ph": (5.5, 7.5), "rainfall": (90, 180)},
    "mothbeans": {"N": (15, 30), "P": (40, 55), "K": (18, 25), "temp": (24, 32), "humidity": (40, 60), "ph": (4.5, 8.5), "rainfall": (30, 75)},
    "mungbean": {"N": (18, 30), "P": (40, 55), "K": (18, 25), "temp": (27, 30), "humidity": (80, 88), "ph": (6.2, 7.5), "rainfall": (40, 60)},
    "blackgram": {"N": (35, 45), "P": (55, 70), "K": (18, 25), "temp": (25, 35), "humidity": (60, 70), "ph": (6.5, 7.5), "rainfall": (60, 75)},
    "lentil": {"N": (15, 25), "P": (60, 75), "K": (18, 25), "temp": (18, 30), "humidity": (60, 70), "ph": (6.0, 7.5), "rainfall": (45, 55)},
    "watermelon": {"N": (80, 110), "P": (15, 30), "K": (45, 55), "temp": (24, 30), "humidity": (80, 90), "ph": (6.0, 7.0), "rainfall": (40, 60)},
    "muskmelon": {"N": (90, 120), "P": (15, 30), "K": (45, 55), "temp": (27, 30), "humidity": (90, 95), "ph": (6.0, 6.8), "rainfall": (20, 30)},
    "apple": {"N": (20, 40), "P": (130, 145), "K": (195, 205), "temp": (21, 24), "humidity": (90, 95), "ph": (5.5, 6.5), "rainfall": (100, 125)},
    "orange": {"N": (15, 30), "P": (10, 25), "K": (10, 20), "temp": (15, 35), "humidity": (85, 95), "ph": (6.0, 7.5), "rainfall": (100, 120)},
    "banana": {"N": (90, 120), "P": (70, 90), "K": (45, 55), "temp": (25, 30), "humidity": (75, 85), "ph": (5.5, 6.5), "rainfall": (90, 120)},
    "coconut": {"N": (20, 40), "P": (10, 25), "K": (25, 35), "temp": (25, 29), "humidity": (90, 99), "ph": (5.5, 6.5), "rainfall": (130, 230)}
}

# Mandi Economics (Yield quintals/acre, Cost ₹/acre, APMC Mandi Avg Price ₹/quintal)
CROP_ECONOMICS = {
    "sugarcane": {"yield_range": (350, 480), "cost_per_acre": 42000, "mandi_price": 340, "unit": "quintal"},
    "cotton": {"yield_range": (10, 16), "cost_per_acre": 26000, "mandi_price": 7200, "unit": "quintal"},
    "soybean": {"yield_range": (8, 14), "cost_per_acre": 16000, "mandi_price": 4800, "unit": "quintal"},
    "onion": {"yield_range": (80, 140), "cost_per_acre": 35000, "mandi_price": 1800, "unit": "quintal"},
    "grapes": {"yield_range": (70, 110), "cost_per_acre": 75000, "mandi_price": 4200, "unit": "quintal"},
    "pomegranate": {"yield_range": (40, 70), "cost_per_acre": 60000, "mandi_price": 6500, "unit": "quintal"},
    "jowar": {"yield_range": (10, 18), "cost_per_acre": 11000, "mandi_price": 3200, "unit": "quintal"},
    "bajra": {"yield_range": (12, 20), "cost_per_acre": 10500, "mandi_price": 2500, "unit": "quintal"},
    "wheat": {"yield_range": (16, 25), "cost_per_acre": 15000, "mandi_price": 2450, "unit": "quintal"},
    "rice": {"yield_range": (18, 28), "cost_per_acre": 18000, "mandi_price": 2300, "unit": "quintal"},
    "maize": {"yield_range": (22, 32), "cost_per_acre": 14000, "mandi_price": 2150, "unit": "quintal"},
    "chickpea": {"yield_range": (7, 12), "cost_per_acre": 13000, "mandi_price": 5400, "unit": "quintal"},
    "banana": {"yield_range": (120, 200), "cost_per_acre": 55000, "mandi_price": 1600, "unit": "quintal"},
    "watermelon": {"yield_range": (120, 180), "cost_per_acre": 28000, "mandi_price": 900, "unit": "quintal"}
}

# Fallback default for any remaining crops
DEFAULT_CROP_ECONOMIC = {"yield_range": (12, 20), "cost_per_acre": 18000, "mandi_price": 3000, "unit": "quintal"}

# Plant Leaf Disease Database
DISEASE_INFO = {
    "Healthy": {
        "title": "Healthy Foliage",
        "severity": 0,
        "description": "Leaf exhibits uniform chlorophyll distribution, healthy turgor, and zero fungal or necrotic lesions.",
        "organic_treatment": "Continue regular preventive bio-sprays (Neem oil 0.5% or Jeevamrutha). Maintain balanced drip fertigation.",
        "chemical_treatment": "No chemical intervention needed. Avoid preventive chemical sprays to conserve beneficial insects.",
        "prevention": "Ensure proper spacing, crop rotation, and avoid overhead sprinkler watering in late evenings."
    },
    "Leaf Blight": {
        "title": "Leaf Blight (Alternaria / Cercospora)",
        "severity": 65,
        "description": "Concentric necrotic brown rings and yellow halos visible on foliage, causing premature defoliation.",
        "organic_treatment": "Spray Pseudomonas fluorescens @ 5g/L or fermented butter-milk (Chaach) spray (50ml/L). Remove affected lower leaves.",
        "chemical_treatment": "Mancozeb 75% WP @ 2.5g/L or Azoxystrobin + Difenoconazole @ 1ml/L at early infection stage.",
        "prevention": "Avoid waterlogging, maintain canopy aeration, and destroy diseased crop residues after harvest."
    },
    "Rust": {
        "title": "Foliar Rust (Puccinia spp.)",
        "severity": 75,
        "description": "Elevated orange-red to reddish-brown powdery pustules on the lower and upper leaf surfaces.",
        "organic_treatment": "Foliar spray of Dashaparni kashayam or wettable sulfur (bio-grade) @ 3g/L. Dusting with fine wood ash and neem powder.",
        "chemical_treatment": "Propiconazole 25% EC @ 1ml/L or Tebuconazole 250 EC @ 1ml/L every 12-14 days.",
        "prevention": "Plant resistant cultivars, monitor early in morning dew conditions, avoid excessive nitrogen application."
    },
    "Powdery Mildew": {
        "title": "Powdery Mildew (Erysiphales)",
        "severity": 55,
        "description": "White talcum-powder-like fungal patches spreading across leaf surface, inhibiting photosynthesis.",
        "organic_treatment": "Milk-water solution (1:9 ratio) spray under full sunlight, or Potassium Bicarbonate @ 3g/L.",
        "chemical_treatment": "Dinocap 48% EC @ 1ml/L or Hexaconazole 5% SC @ 2ml/L.",
        "prevention": "Prune dense canopies for morning sunlight penetration; monitor grapes, peas, and cucurbits closely."
    },
    "Nutrient Deficiency": {
        "title": "Nutrient Deficiency (Interveinal Chlorosis)",
        "severity": 40,
        "description": "Yellowing of leaf blade while veins remain green (Iron/Magnesium deficiency) or general pale chlorosis (Nitrogen).",
        "organic_treatment": "Foliar spray of Panchagavya (3%) or seaweed liquid extract (2ml/L) + vermiwash.",
        "chemical_treatment": "Chelated Micronutrient grade (Fe-EDTA 12% + Zn + Mg) @ 1.5g/L foliar spray.",
        "prevention": "Correct soil pH (maintain 6.2 - 7.2) to unlock soil nutrient availability; add enriched compost."
    }
}
