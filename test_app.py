"""
KrishiAI - Automated Integration & Health Verification Test
"""
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

def test_database():
    print("[1] Testing database initialization & seeding...", flush=True)
    from backend.database import init_db, seed_initial_data, get_latest_sensor_reading, get_sensor_history
    init_db()
    seed_initial_data()
    latest = get_latest_sensor_reading()
    assert latest is not None, "Failed to retrieve latest sensor reading"
    history = get_sensor_history(10)
    assert len(history) > 0, "Sensor history is empty"
    print(f"    OK: Latest moisture = {latest['soil_moisture']}%, Health = {latest['health_score']}/100", flush=True)

def test_crop_recommender():
    print("[2] Testing Crop Recommendation ML model...", flush=True)
    from backend.ml_crops import crop_recommender
    crop_recommender.load_or_train()
    preds = crop_recommender.predict(75, 48, 52, 6.6, 28.5, 65.0, 120.0)
    assert len(preds) == 3, f"Expected 3 predictions, got {len(preds)}"
    print(f"    OK: Top crop = {preds[0]['crop']} ({preds[0]['confidence']}%)", flush=True)

def test_disease_detector():
    print("[3] Testing Leaf Disease Detection engine...", flush=True)
    from backend.ml_disease import disease_detector
    for sample in ["Leaf Blight", "Rust", "Powdery Mildew", "Healthy"]:
        img = disease_detector.generate_demo_leaf(sample)
        diag = disease_detector.predict(img)
        assert diag["detected_disease"] is not None
    print(f"    OK: Pathology classification operational (Last tested: {diag['detected_disease']})", flush=True)

def test_irrigation_and_fertilizer():
    print("[4] Testing Irrigation & Fertilizer engines...", flush=True)
    from backend.simulator import iot_simulator
    from backend.fertilizer import calculate_fertilizer_recommendation
    plan = iot_simulator.plan_smart_irrigation(crop="Sugarcane", moisture=35.0, area_acres=3.5)
    assert plan["water_required_litres"] > 0
    fert = calculate_fertilizer_recommendation("sugarcane", 28.0, 18.0, 22.0, 2.0)
    assert fert["commercial_recommendations"]["urea"]["total_kg"] > 0
    print(f"    OK: Water needed = {plan['water_required_litres']} L, Urea = {fert['commercial_recommendations']['urea']['total_kg']} kg", flush=True)

def test_pdf_report():
    print("[5] Testing ReportLab PDF Generation...", flush=True)
    from backend.pdf_export import generate_farm_report_pdf
    pdf_bytes = generate_farm_report_pdf()
    assert len(pdf_bytes) > 1000, f"Generated PDF is too small ({len(pdf_bytes)} bytes)"
    print(f"    OK: PDF generated successfully ({len(pdf_bytes)} bytes)", flush=True)

def test_weather_and_chat():
    print("[6] Testing Weather Advisory & Chatbot...", flush=True)
    from backend.weather import get_weather_advisory
    from backend.chatbot import krishi_chatbot
    w = get_weather_advisory()
    assert len(w["daily_forecast"]) == 7
    reply_en = krishi_chatbot.reply("What is my soil moisture?", "en")
    assert "Soil Moisture" in reply_en["reply"] or "%" in reply_en["reply"]
    reply_mr = krishi_chatbot.reply("ओलावा किती आहे?", "mr")
    assert "ओलावा" in reply_mr["reply"]
    print("    OK: 7-day weather & multilingual chat responses generated successfully", flush=True)

if __name__ == "__main__":
    print("\n--- Running KrishiAI Pre-Flight Verification Tests ---")
    test_database()
    test_crop_recommender()
    test_disease_detector()
    test_irrigation_and_fertilizer()
    test_pdf_report()
    test_weather_and_chat()
    print("\n[SUCCESS] ALL KRISHIAI COMPONENT TESTS PASSED!\n")
