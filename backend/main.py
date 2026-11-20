"""
KrishiAI - Main FastAPI Application & REST/WebSocket Gateway
High-performance asynchronous backend powering the KrishiAI Smart Agriculture system.
"""
import io
import asyncio
from contextlib import asynccontextmanager
from typing import Optional, Dict, Any, List

from fastapi import FastAPI, UploadFile, File, Form, Query, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import Response, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from PIL import Image

from backend.config import FRONTEND_DIR, DEFAULT_LOCATION
from backend.database import (
    init_db, seed_initial_data, get_latest_sensor_reading,
    get_sensor_history, save_crop_recommendation, save_disease_scan
)
from backend.simulator import iot_simulator
from backend.ml_crops import crop_recommender
from backend.ml_disease import disease_detector
from backend.ml_yield import predict_yield_and_profit
from backend.fertilizer import calculate_fertilizer_recommendation
from backend.calendar import generate_crop_calendar
from backend.sustainability import calculate_sustainability_metrics
from backend.weather import get_weather_advisory
from backend.chatbot import krishi_chatbot
from backend.pdf_export import generate_farm_report_pdf
from backend.demo_data import get_demo_walkthrough

# Lifespan manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("=" * 60)
    print("  Initializing KrishiAI Smart Agriculture Engine...")
    print("=" * 60)
    init_db()
    seed_initial_data()
    crop_recommender.load_or_train()
    iot_simulator.start()
    yield
    # Shutdown
    iot_simulator.stop()
    print("KrishiAI shutdown complete.")

app = FastAPI(
    title="KrishiAI - Smart Agriculture System",
    description="Precision AI & IoT platform for sustainable crop health, soil management, and yield optimization",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Models
class CropRecRequest(BaseModel):
    n: float = Field(..., ge=0, le=300, description="Nitrogen content (kg/ha)")
    p: float = Field(..., ge=0, le=200, description="Phosphorus content (kg/ha)")
    k: float = Field(..., ge=0, le=300, description="Potassium content (kg/ha)")
    ph: float = Field(..., ge=3.0, le=10.0, description="Soil pH")
    temperature: float = Field(..., ge=-5, le=55, description="Temperature (°C)")
    humidity: float = Field(..., ge=5, le=100, description="Humidity (%)")
    rainfall: float = Field(..., ge=0, le=500, description="Annual / seasonal rainfall (mm)")

class IrrigationRequest(BaseModel):
    crop: Optional[str] = "Sugarcane"
    moisture: Optional[float] = None
    area_acres: Optional[float] = 3.5
    rain_forecast_mm: Optional[float] = 0.0

class YieldRequest(BaseModel):
    crop: str = "Sugarcane"
    area_acres: float = Field(3.5, gt=0)
    season: str = "Kharif"
    soil_type: str = "Medium Black Soil"
    irrigation_type: str = "Drip Irrigation"

class FertilizerRequest(BaseModel):
    crop: str = "Sugarcane"
    soil_n: float = Field(..., ge=0)
    soil_p: float = Field(..., ge=0)
    soil_k: float = Field(..., ge=0)
    area_acres: float = Field(1.0, gt=0)

class ChatRequest(BaseModel):
    message: str
    language: str = "en"
    api_key: Optional[str] = None

# --- API ROUTES ---

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "app": "KrishiAI",
        "version": "1.0.0",
        "simulator_active": iot_simulator.running
    }

# 1. Telemetry Routes
@app.get("/api/sensors/current")
def get_current_sensors():
    return iot_simulator.get_current_readings()

@app.get("/api/sensors/history")
def get_telemetry_history(limit: int = 30):
    return get_sensor_history(limit=limit)

@app.post("/api/simulator/trigger")
def trigger_simulator(event: str = Query("normal", pattern="^(drought|heavy_rain|pest_attack|normal|irrigate)$")):
    result = iot_simulator.trigger_event(event)
    return {"message": f"Simulator mode updated to '{event}'", "current_readings": result}

# 2. Crop Recommendation
@app.post("/api/crop/recommend")
def recommend_crop(req: CropRecRequest):
    predictions = crop_recommender.predict(
        n=req.n, p=req.p, k=req.k, ph=req.ph,
        temp=req.temperature, humidity=req.humidity, rainfall=req.rainfall
    )
    if predictions:
        top1 = predictions[0]
        top2 = predictions[1] if len(predictions) > 1 else None
        top3 = predictions[2] if len(predictions) > 2 else None
        save_crop_recommendation({
            "n": req.n, "p": req.p, "k": req.k, "ph": req.ph,
            "temp": req.temperature, "humidity": req.humidity, "rainfall": req.rainfall,
            "top1_crop": top1["crop"], "top1_prob": top1["confidence"],
            "top2_crop": top2["crop"] if top2 else None, "top2_prob": top2["confidence"] if top2 else None,
            "top3_crop": top3["crop"] if top3 else None, "top3_prob": top3["confidence"] if top3 else None
        })
    return {"predictions": predictions, "inputs": req.model_dump()}

# 3. Disease Detection
@app.post("/api/disease/detect")
async def detect_leaf_disease(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        diagnosis = disease_detector.predict(image)
        
        # Save record
        save_disease_scan({
            "filename": file.filename or "uploaded_leaf.jpg",
            "detected_disease": diagnosis["detected_disease"],
            "confidence": diagnosis["confidence"],
            "severity": diagnosis["severity"],
            "organic_treatment": diagnosis["organic_treatment"],
            "chemical_treatment": diagnosis["chemical_treatment"]
        })
        return diagnosis
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Image processing failed: {str(e)}")

@app.get("/api/disease/sample-leaf")
def test_sample_leaf(disease_type: str = "Leaf Blight"):
    try:
        sample_img = disease_detector.generate_demo_leaf(disease_type)
        diagnosis = disease_detector.predict(sample_img)
        save_disease_scan({
            "filename": f"sample_{disease_type.lower().replace(' ', '_')}.jpg",
            "detected_disease": diagnosis["detected_disease"],
            "confidence": diagnosis["confidence"],
            "severity": diagnosis["severity"],
            "organic_treatment": diagnosis["organic_treatment"],
            "chemical_treatment": diagnosis["chemical_treatment"]
        })
        return diagnosis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 4. Smart Irrigation
@app.post("/api/irrigation/plan")
def plan_irrigation(req: IrrigationRequest):
    return iot_simulator.plan_smart_irrigation(
        crop=req.crop,
        moisture=req.moisture,
        area_acres=req.area_acres,
        rain_forecast_mm=req.rain_forecast_mm
    )

# 5. Weather Advisory
@app.get("/api/weather")
def get_weather(lat: Optional[float] = None, lon: Optional[float] = None):
    return get_weather_advisory(lat=lat, lon=lon)

# 6. Yield & Mandi Profit
@app.post("/api/yield/predict")
def predict_yield(req: YieldRequest):
    return predict_yield_and_profit(
        crop=req.crop,
        area_acres=req.area_acres,
        season=req.season,
        soil_type=req.soil_type,
        irrigation_type=req.irrigation_type
    )

# 7. Fertilizer Calculator
@app.post("/api/fertilizer/calculate")
def calculate_fertilizer(req: FertilizerRequest):
    return calculate_fertilizer_recommendation(
        crop=req.crop,
        soil_n=req.soil_n,
        soil_p=req.soil_p,
        soil_k=req.soil_k,
        area_acres=req.area_acres
    )

# 8. Crop Calendar
@app.get("/api/calendar")
def get_calendar(crop: str = "Sugarcane", start_date: Optional[str] = None):
    return generate_crop_calendar(crop=crop, start_date_str=start_date)

# 9. Sustainability Footprint
@app.get("/api/sustainability")
def get_sustainability(area: float = 3.5, crop: str = "Sugarcane"):
    return calculate_sustainability_metrics(farm_area_acres=area, crop=crop)

# 10. AI Chatbot
@app.post("/api/chat")
def chat_with_assistant(req: ChatRequest):
    if req.api_key:
        krishi_chatbot.set_api_key(req.api_key)
    return krishi_chatbot.reply(req.message, language=req.language)

# 11. PDF Report Download
@app.get("/api/report/pdf")
def download_pdf_report():
    try:
        pdf_bytes = generate_farm_report_pdf()
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=KrishiAI_Farm_Report.pdf"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")

# 12. Demo Walkthrough
@app.get("/api/demo/steps")
def get_demo():
    return {"steps": get_demo_walkthrough()}

# 13. WebSocket for live IoT streaming
@app.websocket("/ws/sensors")
async def websocket_telemetry(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            telemetry = iot_simulator.get_current_readings()
            await websocket.send_json(telemetry)
            await asyncio.sleep(2.0)
    except WebSocketDisconnect:
        pass
    except Exception:
        pass

# Mount static frontend files
app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
