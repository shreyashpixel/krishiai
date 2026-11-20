# KrishiAI – Smart Agriculture & AI Agronomy System

> **College Innovation Project Prototype**  
> An autonomous precision agriculture platform combining IoT telemetry simulation, Machine Learning crop recommendation, foliar pathology scanning, smart irrigation scheduling, Open-Meteo weather forecasting, and APMC mandi market economics.

---

## 🌟 Key Highlights
- **1-Command Zero-Config Startup:** Run `python run.py` on any Windows machine — checks dependencies, seeds the database, trains ML models, starts the server, and launches the browser at `http://localhost:8000`.
- **100% Offline Capability:** Works without API keys, subscriptions, or internet access (uses local ML models, local SQLite database, and simulated weather fallback if disconnected).
- **Multilingual & Voice Enabled:** Complete toggle between **English**, **हिंदी (Hindi)**, and **मराठी (Marathi)** with Web Speech API voice input and speech synthesis.
- **Academic Submission Ready:** One-click automated PDF export generating a comprehensive audit report with ReportLab.

---

## 🏗️ System Architecture

```text
+-----------------------------------------------------------------------------------+
|                                 USER INTERFACE                                    |
|   Single Page App (HTML5 / Vanilla CSS3 / Modern JS / Chart.js / Web Speech API)  |
|      [Dashboard] [Crop Rec] [Disease] [Irrigation] [Weather] [Yield] [Chatbot]    |
+------------------------------------------+----------------------------------------+
                                           | HTTP REST / WebSocket (/ws/sensors)
+------------------------------------------v----------------------------------------+
|                            FASTAPI BACKEND GATEWAY                                |
|   backend/main.py : Request routing, CORS, Static SPA serving, Lifespan manager   |
+----+-------------------+--------------------+-------------------+-----------------+
     |                   |                    |                   |
     v                   v                    v                   v
+------------+   +---------------+    +---------------+   +---------------+
| IoT ENGINE |   |   ML ENGINES  |    | AGRONOMY MATH |   | EXTERNAL APIS |
| simulator  |   | ml_crops (RF) |    | fertilizer.py |   | weather.py    |
| - Diurnal  |   | ml_disease    |    | calendar.py   |   | - Open-Meteo  |
|   physics  |   | ml_yield      |    | sustain.py    |   | - Offline sim |
| - Drought/ |   | (Top 3 crops, |    | (Urea/DAP/MOP |   | - Spray alerts|
|   Rain sim |   |  Lesion HSV)  |    |  Water saved) |   |               |
+-----+------+   +-------+-------+    +-------+-------+   +-------+-------+
      |                  |                    |                   |
      +------------------+--------------------+-------------------+
                                 |
+--------------------------------v--------------------------------------------------+
|                            PERSISTENCE & EXPORT                                   |
|   SQLite DB (data/krishiai.db)  |  ReportLab Engine (data/krishiai_report.pdf)     |
|   - Telemetry logs              |  - Multi-page submission report                 |
|   - Disease scans & Irrigation  |  - Sensor metrics & Eco-audit badges             |
+-----------------------------------------------------------------------------------+
```

---

## 📋 Core & Standout Features

| # | Module | Technology | Highlights |
|---|---|---|---|
| **1** | **Farm Dashboard** | IoT Thread + Chart.js | Real-time soil moisture, temp, humidity, pH, NPK, and Farm Health Score (0-100). |
| **2** | **Crop Recommendation** | Scikit-Learn Random Forest | Predicts top 3 crops with confidence % across 24 crops (including Sugarcane, Cotton, Soybean, Onion, Grapes, Pomegranate). |
| **3** | **Plant Disease Scanner** | Computer Vision (Pillow + HSV) | Leaf image upload/camera; classifies Blight, Rust, Mildew, and Nutrient Chlorosis with severity % and dual biological/chemical treatments. |
| **4** | **IoT Field Simulator** | Thread daemon | Diurnal sine-wave environmental patterns with interactive demo triggers: **Drought**, **Heavy Rain**, **Pest Attack**, **Normal**. |
| **5** | **Smart Irrigation Planner** | Agronomic Water Budgeting | Recommends exact Litres and drip cycle minutes; tracks water conserved vs traditional flood watering (54% savings). |
| **6** | **Weather Advisory** | Open-Meteo API | 7-day agro-meteorological forecast with automatic spray window alerts (postpones chemical application before rain). |
| **7** | **Yield & Mandi Profit** | Agronomic Regression | Inputs acreage and crop to project total yield (quintals), cultivation costs, APMC gross revenue, net profit, and ROI %. |
| **8** | **Multilingual UI + Voice** | `i18n.js` + Web Speech API | English, हिंदी, and मराठी toggle for all UI elements; voice input microphone for natural queries. |
| **9** | **Krishi Sakha AI Chatbot** | Rule-based NLP + Grounding | Answers questions on pests, fertilizers, and subsidies directly grounded in the farm's live IoT sensor readings. |
| **10**| **Fertilizer Calculator** | NPK Deficit Matrix | Exact commercial 45kg/50kg bags of Urea, DAP, and MOP plus regenerative Vermicompost and Biofertilizers. |
| **11**| **Stage-wise Crop Calendar**| Dynamic Timeline Engine | Growth milestones from sowing to harvest with days remaining and critical management alerts. |
| **12**| **Sustainability Meter** | Ecological Footprint | Quantifies groundwater conserved (Litres), CO₂e greenhouse emissions mitigated, and trees equivalent planted. |
| **13**| **One-Click PDF Report** | ReportLab 5.0 | Exports a multi-page, formatted farm health audit report for academic submission. |
| **14**| **Interactive Demo Mode** | Automated Walkthrough | Guided 9-step presentation flow with sample presets to guarantee a seamless viva demonstration. |

---

## ⚡ 3-Step Setup

### Step 1: Open Terminal / Command Prompt
Navigate to the project root directory:
```bash
cd c:\Users\shreyash\shivaniprj
```

### Step 2: Run the Bootstrapper
```bash
python run.py
```
*(The bootstrapper automatically installs any missing packages, creates `data/` and `models/`, seeds the database, trains the Random Forest model, and starts the server on `http://localhost:8000`)*.

### Step 3: View in Browser
The browser will open automatically to:
```text
http://localhost:8000
```

---

## ⏱️ 2-Minute Demo Presentation Script

Follow this script when demonstrating the prototype to professors or evaluators:

1. **Introduction (0:00 - 0:20)**
   - *"Hello professors. This is KrishiAI – an autonomous Precision Agriculture & AI Agronomy platform designed to optimize crop yields and conserve groundwater."*
   - Show the **Dashboard**: Highlight the **Farm Health Score (92/100)** and live streaming telemetry (Soil Moisture, Temperature, Humidity, pH, NPK).

2. **IoT Anomaly & Smart Irrigation (0:20 - 0:45)**
   - Click **"Simulate Drought"**: Show soil moisture plunging to 18%, temperature rising to 39°C, and the alert turning red.
   - Switch to **"Smart Irrigation"**: Show how the AI detects the moisture deficit and calculates that 3.5 acres of Sugarcane requires 34,000 Litres (saving over 40,000 Litres compared to flood irrigation). Click **"Trigger Micro-Drip"** to restore soil balance.

3. **Machine Learning Crop Recommendation (0:45 - 1:10)**
   - Switch to **"Crop Rec (ML)"**: Click **"Auto-fill with Live Sensors"** to pull current soil NPK and weather metrics directly into the form.
   - Click **"Predict Optimal Crops"**: Explain that our Scikit-Learn Random Forest model analyzed the profile against 24 regional crops to recommend **Sugarcane (92.4%)** and **Cotton** with agronomic compatibility tags.

4. **Leaf Disease Diagnosis & Fertilizer Calculator (1:10 - 1:35)**
   - Switch to **"Disease Detection"**: Click **"Leaf Blight"** under sample leaves. Show the detected severity (45%), necrotic lesion analysis, and dual organic (fermented buttermilk/Pseudomonas) and chemical (Mancozeb) treatments.
   - Switch to **"Fertilizer Calc"**: Click **"Import Live Soil Test"** and calculate the exact bags of Urea, DAP, and MOP required, showing the basal and top-dressing split schedule.

5. **Multilingual Chatbot, Sustainability & PDF Export (1:35 - 2:00)**
   - Switch language to **मराठी** or **हिंदी**: Click the mic or ask *"जमिनीतील ओलावा किती आहे?"* to demonstrate **Krishi Sakha** answering with the live sensor value.
   - Click **"Export PDF"**: Download and open the generated multi-page ReportLab audit report for the project submission file.

---

## 🔮 Future Scope & Scalability
1. **Hardware Integration:** Connect ESP32 / Arduino LoRaWAN sensor nodes using standard MQTT brokers.
2. **Deep Learning Vision Upgrade:** Replace the lightweight HSV feature detector with a fine-tuned MobileNetV3 / ResNet-50 CNN model for 38+ plant diseases using the existing `BaseDiseaseDetector` interface.
3. **Satellite Remote Sensing:** Integrate Sentinel-2 / Landsat NDVI (Normalized Difference Vegetation Index) APIs for canopy moisture mapping.
4. **Drone Autonomous Spraying:** Export GeoJSON flight path waypoints derived from the disease severity map for targeted pesticide delivery.

---

## 🎓 Viva Voce Q&A (10 Questions & Answers)

### Q1: Why did you choose Random Forest for crop recommendation instead of a Deep Neural Network?
**Answer:** Random Forest is an ensemble of decision trees that handles non-linear boundaries between soil nutrients (NPK), climate (temperature, rainfall), and pH exceptionally well. It does not suffer from vanishing gradients on tabular data, requires low inference latency (<15ms), prevents overfitting through bagging and feature subsampling, and provides interpretable feature importances for farmers.

### Q2: How does the Smart Irrigation Planner calculate the exact water volume?
**Answer:** The algorithm calculates the moisture deficit between current volumetric soil moisture and the crop-specific physiological target (typically 50%). Based on agronomic standards, 1% moisture deficit across 1 acre of root-zone requires approximately 850 Litres of water. The system then factors in the Open-Meteo 24-hour rainfall forecast to offset precipitation, preventing over-watering and saving ~54% water compared to conventional flood irrigation.

### Q3: How does the plant disease detection work without large cloud deep learning weights?
**Answer:** We implemented a modular computer vision pipeline (`BaseDiseaseDetector`). The lightweight engine converts leaf RGB pixels into the HSV (Hue, Saturation, Value) chromatic space to isolate green chlorophyll from necrotic brown blight, orange rust pustules, and white fungal mycelium. It computes spot coverage ratios, color variance, and contrast to score disease classes. The architecture is deliberately designed with an abstract interface so a PyTorch/TensorFlow CNN can be plugged in without changing backend routes.

### Q4: How is live IoT sensor telemetry streamed to the frontend?
**Answer:** The backend runs an asynchronous background simulation daemon implementing day-night diurnal physics. Telemetry is streamed over a persistent **WebSocket connection (`/ws/sensors`)** every 2-3 seconds. If the client experiences network interruptions or WebSocket failures, `api.js` automatically engages an HTTP polling fallback mechanism (`/api/sensors/current`) every 3 seconds to guarantee resilience.

### Q5: How does the system work completely offline?
**Answer:** The backend uses local SQLite storage (`krishiai.db`), serialized Scikit-Learn models (`crop_rf_model.pkl`), and bundled JavaScript assets. For the weather module, if the Open-Meteo external API is unreachable or internet connectivity drops, the system automatically falls back to an internal agro-meteorological simulation generator without throwing errors.

### Q6: What is the significance of N-P-K nutrient balancing in agriculture?
**Answer:** Nitrogen (N) drives vegetative leafy growth and chlorophyll synthesis, Phosphorus (P) accelerates root development and early flowering, while Potassium (K) regulates stomatal opening, water retention, and fruit disease resistance. KrishiAI's Fertilizer Calculator calculates exact commercial bags (Urea 46% N, DAP 18:46:0, MOP 60% K₂O) based on soil test deficits to prevent nitrogen leaching and soil acidification.

### Q7: How does KrishiAI calculate the Sustainability & Carbon Footprint score?
**Answer:** Groundwater pumping consumes electrical power (~0.35 kWh per 1,000 Litres), which translates to ~0.82 kg CO₂e grid emissions. Furthermore, producing and over-applying synthetic urea generates ~2.98 kg CO₂e per kg of excess fertilizer through Haber-Bosch manufacturing and soil N₂O volatilization. KrishiAI tracks the exact water and fertilizer conserved and converts them into net CO₂e mitigation and equivalent trees planted.

### Q8: How is the multilingual feature implemented?
**Answer:** The frontend uses a dictionary mapping in `i18n.js` with declarative `data-i18n` DOM attributes. When a user switches between English, Hindi, and Marathi, text is swapped dynamically and stored in `localStorage`. The voice assistant configures the Web Speech API recognition language (`en-IN`, `hi-IN`, `mr-IN`) to accurately capture regional dialects.

### Q9: What happens if an anomalous condition like a severe drought or flood occurs?
**Answer:** The system dynamically recalculates the Farm Health Score (penalizing moisture deviations beyond 40-55%). When moisture drops below 35%, an emergency alert banner triggers on the UI and the Smart Irrigation Planner adjusts urgency from "OPTIMAL" to "URGENT", scheduling immediate drip irrigation.

### Q10: How are market economics and mandi profits projected?
**Answer:** The Yield Engine (`ml_yield.py`) combines average regional yield baselines (quintals/acre) with management multipliers (e.g., drip irrigation increases yield by 18% while reducing water costs). It subtracts total cultivation expenses (seeds, fertilizer, labor, mechanization) from gross market revenue at APMC benchmark rates to output Net Profit, Break-Even Price, and Return on Investment (ROI %).

---

## 📄 License & Attribution
Developed for College Innovation Project Demonstration. Built with FastAPI, Scikit-Learn, ReportLab, and Chart.js.
