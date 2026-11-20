"""
KrishiAI - Open-Meteo Weather Advisory Engine
Fetches 7-day agro-meteorological forecast without API keys.
Includes robust offline simulation fallback and intelligent farming advisories.
"""
import datetime
import requests
from typing import Dict, Any, List
from backend.config import DEFAULT_LOCATION

WMO_WEATHER_MAP = {
    0: {"condition": "Clear Sky", "icon": "sun", "spray_safe": True},
    1: {"condition": "Mainly Clear", "icon": "sun-cloud", "spray_safe": True},
    2: {"condition": "Partly Cloudy", "icon": "cloud-sun", "spray_safe": True},
    3: {"condition": "Overcast", "icon": "cloud", "spray_safe": True},
    45: {"condition": "Foggy", "icon": "cloud-fog", "spray_safe": False},
    48: {"condition": "Depositing Rime Fog", "icon": "cloud-fog", "spray_safe": False},
    51: {"condition": "Light Drizzle", "icon": "cloud-drizzle", "spray_safe": False},
    53: {"condition": "Moderate Drizzle", "icon": "cloud-drizzle", "spray_safe": False},
    55: {"condition": "Dense Drizzle", "icon": "cloud-drizzle", "spray_safe": False},
    61: {"condition": "Slight Rain", "icon": "cloud-rain", "spray_safe": False},
    63: {"condition": "Moderate Rain", "icon": "cloud-rain", "spray_safe": False},
    65: {"condition": "Heavy Rain", "icon": "cloud-rain", "spray_safe": False},
    80: {"condition": "Rain Showers", "icon": "cloud-rain", "spray_safe": False},
    81: {"condition": "Moderate Showers", "icon": "cloud-rain", "spray_safe": False},
    82: {"condition": "Violent Showers", "icon": "cloud-rain", "spray_safe": False},
    95: {"condition": "Thunderstorm", "icon": "cloud-lightning", "spray_safe": False}
}

def get_weather_advisory(lat: float = None, lon: float = None) -> Dict[str, Any]:
    """Fetches real-time 7-day forecast from Open-Meteo or falls back to realistic simulation."""
    if lat is None or lon is None:
        lat = DEFAULT_LOCATION["latitude"]
        lon = DEFAULT_LOCATION["longitude"]

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,precipitation,weather_code,wind_speed_10m",
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max,wind_speed_10m_max",
        "timezone": "auto"
    }

    try:
        resp = requests.get(url, params=params, timeout=2.5)
        if resp.status_code == 200:
            data = resp.json()
            return parse_live_weather(data, lat, lon)
    except Exception as e:
        print(f"Weather API unavailable ({e}). Using offline simulation mode.")

    return get_simulated_weather(lat, lon)

def parse_live_weather(data: Dict[str, Any], lat: float, lon: float) -> Dict[str, Any]:
    """Parses Open-Meteo API payload into structured agro-forecast."""
    current = data.get("current", {})
    daily = data.get("daily", {})

    wcode = current.get("weather_code", 1)
    cond_info = WMO_WEATHER_MAP.get(wcode, {"condition": "Partly Cloudy", "icon": "cloud-sun", "spray_safe": True})

    daily_forecast = []
    dates = daily.get("time", [])
    t_max = daily.get("temperature_2m_max", [])
    t_min = daily.get("temperature_2m_min", [])
    precip = daily.get("precipitation_sum", [])
    precip_prob = daily.get("precipitation_probability_max", [])
    codes = daily.get("weather_code", [])
    wind = daily.get("wind_speed_10m_max", [])

    for i in range(min(7, len(dates))):
        c_code = codes[i] if i < len(codes) else 1
        day_cond = WMO_WEATHER_MAP.get(c_code, {"condition": "Sunny", "icon": "sun", "spray_safe": True})
        
        # Format day name
        try:
            d_obj = datetime.datetime.strptime(dates[i], "%Y-%m-%d")
            day_name = d_obj.strftime("%a (%d %b)")
        except Exception:
            day_name = f"Day {i+1}"

        daily_forecast.append({
            "date": dates[i] if i < len(dates) else "",
            "day": day_name,
            "temp_max": round(t_max[i], 1) if i < len(t_max) else 30.0,
            "temp_min": round(t_min[i], 1) if i < len(t_min) else 20.0,
            "precipitation_mm": round(precip[i], 1) if i < len(precip) else 0.0,
            "precipitation_prob": precip_prob[i] if i < len(precip_prob) else 10,
            "condition": day_cond["condition"],
            "icon": day_cond["icon"],
            "wind_kmh": round(wind[i], 1) if i < len(wind) else 12.0
        })

    advisories = generate_agri_advisories(daily_forecast, current)

    return {
        "is_live": True,
        "source": "Open-Meteo Real-time API",
        "location": {"latitude": lat, "longitude": lon, "label": "Detected Location (Pune Region)"},
        "current": {
            "temperature": round(current.get("temperature_2m", 28.0), 1),
            "humidity": round(current.get("relative_humidity_2m", 65.0), 1),
            "precipitation": round(current.get("precipitation", 0.0), 1),
            "wind_speed": round(current.get("wind_speed_10m", 10.0), 1),
            "condition": cond_info["condition"],
            "icon": cond_info["icon"]
        },
        "daily_forecast": daily_forecast,
        "advisories": advisories
    }

def get_simulated_weather(lat: float, lon: float) -> Dict[str, Any]:
    """Generates realistic offline simulated 7-day forecast for agricultural demonstrations."""
    today = datetime.date.today()
    daily_forecast = []
    
    sim_data = [
        {"max": 31.5, "min": 21.0, "p": 0.0, "prob": 10, "code": 1, "wind": 11.0},
        {"max": 32.2, "min": 21.4, "p": 0.0, "prob": 15, "code": 2, "wind": 13.5},
        {"max": 29.8, "min": 20.5, "p": 8.5, "prob": 70, "code": 61, "wind": 18.0},
        {"max": 28.0, "min": 19.8, "p": 14.2, "prob": 85, "code": 63, "wind": 22.0},
        {"max": 30.1, "min": 20.2, "p": 1.5, "prob": 30, "code": 3, "wind": 14.0},
        {"max": 31.8, "min": 21.5, "p": 0.0, "prob": 10, "code": 0, "wind": 10.5},
        {"max": 33.0, "min": 22.0, "p": 0.0, "prob": 5, "code": 0, "wind": 9.0}
    ]

    for i, s in enumerate(sim_data):
        d_date = today + datetime.timedelta(days=i)
        cond = WMO_WEATHER_MAP.get(s["code"], {"condition": "Clear", "icon": "sun", "spray_safe": True})
        daily_forecast.append({
            "date": d_date.strftime("%Y-%m-%d"),
            "day": d_date.strftime("%a (%d %b)") if i > 0 else "Today",
            "temp_max": s["max"],
            "temp_min": s["min"],
            "precipitation_mm": s["p"],
            "precipitation_prob": s["prob"],
            "condition": cond["condition"],
            "icon": cond["icon"],
            "wind_kmh": s["wind"]
        })

    current = {
        "temperature_2m": 30.2,
        "relative_humidity_2m": 62.0,
        "precipitation": 0.0,
        "wind_speed_10m": 11.5,
        "weather_code": 1
    }

    advisories = generate_agri_advisories(daily_forecast, current)

    return {
        "is_live": False,
        "source": "KrishiAI Agro-Weather Simulator (Offline Mode)",
        "location": {"latitude": lat, "longitude": lon, "label": "Pune Agro-Climatic Zone (Offline)"},
        "current": {
            "temperature": 30.2,
            "humidity": 62.0,
            "precipitation": 0.0,
            "wind_speed": 11.5,
            "condition": "Mainly Clear",
            "icon": "sun-cloud"
        },
        "daily_forecast": daily_forecast,
        "advisories": advisories
    }

def generate_agri_advisories(forecast: List[Dict[str, Any]], current: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Synthesizes actionable agronomic advisories based on meteorological indicators."""
    advisories = []

    # Check for rain in next 2-3 days
    rain_days = [f for f in forecast[:3] if f["precipitation_mm"] > 3.0 or f["precipitation_prob"] > 60]
    if rain_days:
        day_names = ", ".join([r["day"] for r in rain_days])
        advisories.append({
            "type": "warning",
            "title": "Rain Forecasted – Postpone Sprays & Fertilizers",
            "badge": "Spraying Advisory",
            "detail": f"Significant rainfall expected on {day_names}. Avoid applying foliar insecticides and top-dressing urea to prevent chemical wash-off into drainage."
        })
    else:
        advisories.append({
            "type": "success",
            "title": "Favorable Spray Window Available",
            "badge": "Safe Window",
            "detail": "Clear weather for the next 48 hours with wind speeds below 15 km/h. Ideal window for preventive bio-sprays or micronutrient fertigation."
        })

    # High humidity disease warning
    hum = current.get("relative_humidity_2m", 60.0)
    temp = current.get("temperature_2m", 28.0)
    if hum > 75.0 and 20.0 <= temp <= 32.0:
        advisories.append({
            "type": "danger",
            "title": "Fungal Disease Warning (High Humidity)",
            "badge": "Pathogen Alert",
            "detail": f"Relative humidity is {hum}%. Microclimate is conducive for Downy Mildew in grapes, Rust in wheat, and Leaf Blight in pulses. Inspect lower canopies."
        })

    # Wind speed check
    wind = current.get("wind_speed_10m", 10.0)
    if wind > 20.0:
        advisories.append({
            "type": "warning",
            "title": "Gusty Winds Alert",
            "badge": "Mechanical Alert",
            "detail": f"Wind speeds are currently {wind} km/h. Excessive drift will occur if spraying herbicides. Provide staking to lodging-prone crops."
        })

    # Irrigation guidance based on rain
    total_rain_week = sum([f["precipitation_mm"] for f in forecast])
    if total_rain_week > 15.0:
        advisories.append({
            "type": "info",
            "title": "Reduce Irrigation Quota",
            "badge": "Water Optimization",
            "detail": f"Approximately {total_rain_week:.1f} mm rain expected this week. Decrease drip irrigation run-time by 40% to save groundwater and electricity."
        })
    else:
        advisories.append({
            "type": "info",
            "title": "Maintain Scheduled Irrigation",
            "badge": "Irrigation Plan",
            "detail": "Dry spell expected over the coming week. Maintain standard soil moisture threshold between 45% - 55%."
        })

    return advisories
