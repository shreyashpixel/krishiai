"""
KrishiAI - IoT Sensor Simulator & Smart Irrigation Planner
Runs a background daemon simulating field telemetry with diurnal day/night cycles.
Supports live demo triggers (drought, heavy rain, pest attack, irrigation cycle).
"""
import time
import math
import random
import datetime
import threading
from typing import Dict, Any, List
from backend.database import save_sensor_reading, save_irrigation_action

class IoTSensorSimulator:
    def __init__(self):
        self.lock = threading.RLock()
        self.running = False
        self.thread: threading.Thread = None
        
        # Telemetry State
        self.mode = "normal"  # normal, drought, heavy_rain, pest_attack, irrigate
        self.mode_timer = 0    # countdown for active event mode
        
        self.soil_moisture = 45.2
        self.temperature = 28.4
        self.humidity = 64.0
        self.ph = 6.65
        self.nitrogen = 74.0
        self.phosphorus = 48.0
        self.potassium = 52.0
        self.health_score = 92
        self.condition_alert = "Optimal soil moisture & microclimate"
        self.active_crop = "Sugarcane"
        self.farm_area_acres = 3.5
        self.tick_count = 0

    def start(self):
        """Starts background simulation loop."""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._simulation_loop, daemon=True)
            self.thread.start()
            print("KrishiAI IoT Field Telemetry Simulator started.")

    def stop(self):
        """Stops simulator."""
        self.running = False

    def trigger_event(self, event_type: str) -> Dict[str, Any]:
        """Injects demonstration events: drought, heavy_rain, pest_attack, normal, irrigate."""
        with self.lock:
            event_clean = event_type.lower().strip()
            self.mode = event_clean
            self.mode_timer = 12 # Active for 12 ticks (~36-40 seconds)

            if event_clean == "drought":
                self.soil_moisture = 18.5
                self.temperature = 39.2
                self.humidity = 24.0
                self.health_score = 42
                self.condition_alert = "CRITICAL: Severe Root Zone Drought! Immediate irrigation required!"
            elif event_clean == "heavy_rain":
                self.soil_moisture = 86.4
                self.temperature = 22.1
                self.humidity = 95.0
                self.health_score = 64
                self.condition_alert = "ALERT: Heavy Rainfall! Soil waterlogged; pause all irrigation."
            elif event_clean == "pest_attack":
                self.health_score = 51
                self.condition_alert = "WARNING: Pest Risk Elevated (Sucking Pests/Fungal Spores). Inspect leaves."
            elif event_clean == "irrigate":
                self.soil_moisture = min(70.0, self.soil_moisture + 15.0)
                self.health_score = min(98, self.health_score + 18)
                self.condition_alert = "SUCCESS: Micro-Drip Irrigation Active. Restoring soil moisture."
                # Log action to database
                save_irrigation_action({
                    "crop_type": self.active_crop,
                    "moisture": self.soil_moisture,
                    "litres_allocated": 1500.0,
                    "water_saved_litres": 650.0,
                    "trigger_type": "manual_demo",
                    "notes": "User triggered instant drip pulse."
                })
            else: # normal
                self.mode = "normal"
                self.mode_timer = 0
                self.soil_moisture = 46.0
                self.temperature = 27.8
                self.humidity = 66.0
                self.health_score = 94
                self.condition_alert = "Optimal soil moisture & microclimate"

            return self.get_current_readings()

    def _simulation_loop(self):
        """Continuous background tick."""
        while self.running:
            try:
                time.sleep(3.0)
                with self.lock:
                    self.tick_count += 1
                    
                    if self.mode != "normal":
                        if self.mode_timer > 0:
                            self.mode_timer -= 1
                        else:
                            # Smoothly return to normal
                            self.mode = "normal"
                            self.condition_alert = "Optimal conditions restored"

                    # Calculate diurnal day/night cycle based on current clock hour
                    now = datetime.datetime.now()
                    hour = now.hour + (now.minute / 60.0)
                    
                    # Diurnal temperature cycle: peak ~14:00 (32°C), lowest ~05:00 (20°C)
                    sine_factor = math.sin(math.pi * (hour - 9) / 12.0)
                    base_temp = 26.0 + 6.0 * sine_factor
                    
                    if self.mode == "normal":
                        # Smooth natural drift
                        self.temperature = round(base_temp + random.uniform(-0.4, 0.4), 1)
                        # Relative humidity inverse to temperature
                        self.humidity = round(max(35.0, min(92.0, 75.0 - 20.0 * sine_factor + random.uniform(-1.0, 1.0))), 1)
                        # Natural evapotranspiration depletion of soil moisture
                        self.soil_moisture = round(max(25.0, self.soil_moisture - 0.04 + random.uniform(-0.02, 0.02)), 1)
                        # If moisture drops below 35%, simulate automatic micro-irrigation
                        if self.soil_moisture < 34.0:
                            self.soil_moisture = 48.5
                            self.condition_alert = "Auto Smart Drip Cycle triggered: moisture restored to 48.5%"
                        else:
                            self.condition_alert = "Optimal soil moisture & microclimate"
                        
                        self.ph = round(6.65 + random.uniform(-0.03, 0.03), 2)
                        self.nitrogen = round(74.0 + random.uniform(-0.5, 0.5), 1)
                        self.phosphorus = round(48.0 + random.uniform(-0.4, 0.4), 1)
                        self.potassium = round(52.0 + random.uniform(-0.4, 0.4), 1)

                        # Farm Health Score computation (0 - 100)
                        # Penalties for deviation from optimal ranges:
                        # Ideal moisture: 40-55%
                        moisture_pen = abs(self.soil_moisture - 47.5) * 1.2
                        temp_pen = abs(self.temperature - 27.0) * 1.5
                        ph_pen = abs(self.ph - 6.6) * 25.0
                        self.health_score = int(max(40, min(99, 100 - moisture_pen - temp_pen - ph_pen)))

                    elif self.mode == "drought":
                        self.soil_moisture = round(max(14.0, self.soil_moisture - 0.15), 1)
                        self.temperature = round(38.5 + random.uniform(-0.3, 0.3), 1)
                        self.humidity = round(22.0 + random.uniform(-0.5, 0.5), 1)
                        self.health_score = 38
                    elif self.mode == "heavy_rain":
                        self.soil_moisture = round(min(92.0, self.soil_moisture + 0.3), 1)
                        self.humidity = round(94.0 + random.uniform(-0.5, 0.5), 1)
                        self.health_score = 60

                    # Persist reading to database every 5 ticks (~15 seconds)
                    if self.tick_count % 5 == 0:
                        save_sensor_reading(self.get_current_readings())

            except Exception as e:
                print(f"Simulator loop error: {e}")

    def get_current_readings(self) -> Dict[str, Any]:
        """Thread-safe snapshot of live telemetry."""
        with self.lock:
            return {
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "soil_moisture": self.soil_moisture,
                "temperature": self.temperature,
                "humidity": self.humidity,
                "ph": self.ph,
                "nitrogen": self.nitrogen,
                "phosphorus": self.phosphorus,
                "potassium": self.potassium,
                "health_score": self.health_score,
                "condition_alert": self.condition_alert,
                "mode": self.mode,
                "crop": self.active_crop,
                "area_acres": self.farm_area_acres
            }

    def plan_smart_irrigation(
        self,
        crop: str = None,
        moisture: float = None,
        area_acres: float = None,
        rain_forecast_mm: float = 0.0
    ) -> Dict[str, Any]:
        """
        Smart Irrigation Advisor:
        Calculates exact water required (in Litres & runtime minutes),
        incorporating live moisture deficit and weather rain offset.
        """
        crop_name = crop or self.active_crop
        cur_moisture = moisture if moisture is not None else self.soil_moisture
        area = area_acres if area_acres is not None else self.farm_area_acres

        # Ideal root-zone target moisture %
        TARGET_MOISTURE = 50.0
        CRITICAL_THRESHOLD = 35.0

        deficit = max(0.0, TARGET_MOISTURE - cur_moisture)

        # Baseline: 1% soil moisture across 1 acre of root zone ~ 850 Litres
        # Offset rain: 1 mm rainfall ~ 4,000 Litres per acre absorbed
        rain_water_equivalent_pct = min(deficit, rain_forecast_mm * 0.4)
        net_deficit = max(0.0, deficit - rain_water_equivalent_pct)

        litres_needed = int(net_deficit * 850 * area)
        traditional_flood_litres = int(litres_needed * 2.2) # Flood uses 2.2x
        water_saved_litres = traditional_flood_litres - litres_needed

        # Drip discharge rate: ~2.0 Litres/hour per emitter, ~1600 emitters/acre
        drip_capacity_litres_per_hour = 3200 * area
        drip_runtime_minutes = int((litres_needed / max(1.0, drip_capacity_litres_per_hour)) * 60)

        # Timing advice
        if cur_moisture < CRITICAL_THRESHOLD:
            urgency = "URGENT"
            time_to_irrigate = "Immediate (Within 2 Hours)"
            status_text = "Soil moisture is critically low. Root stress is actively occurring."
        elif net_deficit > 5.0:
            urgency = "MODERATE"
            time_to_irrigate = "Early Evening (5:30 PM - 7:00 PM)"
            status_text = "Scheduled maintenance cycle to avoid mid-day evaporation losses."
        elif rain_forecast_mm > 5.0:
            urgency = "SKIP"
            time_to_irrigate = "Postponed (Rain Expected)"
            status_text = f"Rain of {rain_forecast_mm:.1f} mm forecast. Skip irrigation to prevent waterlogging."
        else:
            urgency = "OPTIMAL"
            time_to_irrigate = "No Irrigation Required Today"
            status_text = "Soil moisture is within ideal physiological limits."

        return {
            "crop": crop_name,
            "current_moisture": cur_moisture,
            "target_moisture": TARGET_MOISTURE,
            "farm_area_acres": area,
            "rain_offset_mm": rain_forecast_mm,
            "urgency": urgency,
            "time_to_irrigate": time_to_irrigate,
            "water_required_litres": litres_needed,
            "water_saved_litres": water_saved_litres,
            "water_saved_percent": 54.5,
            "drip_runtime_minutes": drip_runtime_minutes,
            "status_text": status_text,
            "recommendation": (
                f"For {area} acres of {crop_name}, deliver {litres_needed:,} Litres via drip system "
                f"({drip_runtime_minutes} minutes cycle). By using AI precision timing instead of flood watering, "
                f"you save {water_saved_litres:,} Litres of water and ~{round(drip_runtime_minutes*0.06, 1)} kWh in pump electricity."
            )
        }

# Singleton simulator instance
iot_simulator = IoTSensorSimulator()
