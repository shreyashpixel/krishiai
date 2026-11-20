"""
KrishiAI - SQLite Database Layer & Sample Data Seeder
"""
import sqlite3
import datetime
import random
from typing import Dict, List, Any, Optional
from backend.config import DB_PATH

def get_db_connection() -> sqlite3.Connection:
    """Provides a connection with dict row factory for easy serialization."""
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes all database tables if they do not exist."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Sensor telemetry logs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sensors_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        soil_moisture REAL NOT NULL,
        temperature REAL NOT NULL,
        humidity REAL NOT NULL,
        ph REAL NOT NULL,
        nitrogen REAL NOT NULL,
        phosphorus REAL NOT NULL,
        potassium REAL NOT NULL,
        health_score INTEGER NOT NULL,
        condition_alert TEXT,
        mode TEXT DEFAULT 'normal'
    )
    """)

    # Crop recommendation history
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS crop_recommendations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        n REAL NOT NULL,
        p REAL NOT NULL,
        k REAL NOT NULL,
        ph REAL NOT NULL,
        temp REAL NOT NULL,
        humidity REAL NOT NULL,
        rainfall REAL NOT NULL,
        top1_crop TEXT NOT NULL,
        top1_prob REAL NOT NULL,
        top2_crop TEXT,
        top2_prob REAL,
        top3_crop TEXT,
        top3_prob REAL
    )
    """)

    # Disease scans history
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS disease_scans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        filename TEXT NOT NULL,
        detected_disease TEXT NOT NULL,
        confidence REAL NOT NULL,
        severity INTEGER NOT NULL,
        organic_treatment TEXT,
        chemical_treatment TEXT
    )
    """)

    # Irrigation logs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS irrigation_actions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        crop_type TEXT NOT NULL,
        moisture REAL NOT NULL,
        litres_allocated REAL NOT NULL,
        water_saved_litres REAL NOT NULL,
        trigger_type TEXT DEFAULT 'auto',
        notes TEXT
    )
    """)

    # Chat history
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        user_text TEXT NOT NULL,
        bot_reply TEXT NOT NULL,
        intent TEXT
    )
    """)

    # Farm settings / configuration
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT
    )
    """)

    conn.commit()
    conn.close()

def seed_initial_data():
    """Seeds realistic historical sensor telemetry, disease scans, and irrigation logs."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if already seeded
    cursor.execute("SELECT COUNT(*) as cnt FROM sensors_log")
    count = cursor.fetchone()["cnt"]

    if count == 0:
        now = datetime.datetime.now()
        # Seed 36 data points (every 30 mins over past 18 hours)
        base_moisture = 44.0
        base_temp = 27.0
        base_hum = 68.0

        for i in range(36, -1, -1):
            time_pt = (now - datetime.timedelta(minutes=i * 30)).strftime("%Y-%m-%d %H:%M:%S")
            # Diurnal sine wave simulation
            hour = (now - datetime.timedelta(minutes=i * 30)).hour
            temp_variation = 5.0 * (1.0 if 10 <= hour <= 16 else -0.5)
            hum_variation = -8.0 * (1.0 if 10 <= hour <= 16 else -0.4)

            sm = max(20.0, min(80.0, base_moisture + random.uniform(-2.5, 2.0)))
            temp = round(base_temp + temp_variation + random.uniform(-1.0, 1.2), 1)
            hum = round(max(30.0, min(95.0, base_hum + hum_variation + random.uniform(-2.0, 2.0))), 1)
            ph = round(6.6 + random.uniform(-0.15, 0.15), 2)
            n = round(74.0 + random.uniform(-3, 3), 1)
            p = round(48.0 + random.uniform(-2, 2), 1)
            k = round(52.0 + random.uniform(-2, 2), 1)
            
            # Compute health score
            score = int(max(60, min(98, 100 - abs(sm - 45)*0.8 - abs(temp - 27)*1.2 - abs(ph - 6.5)*15)))
            alert = "Optimal soil moisture & climate" if score > 80 else "Soil moisture getting low"

            cursor.execute("""
            INSERT INTO sensors_log (timestamp, soil_moisture, temperature, humidity, ph, nitrogen, phosphorus, potassium, health_score, condition_alert, mode)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (time_pt, sm, temp, hum, ph, n, p, k, score, alert, "normal"))

        # Seed sample disease scan
        cursor.execute("""
        INSERT INTO disease_scans (timestamp, filename, detected_disease, confidence, severity, organic_treatment, chemical_treatment)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            (now - datetime.timedelta(hours=5)).strftime("%Y-%m-%d %H:%M:%S"),
            "sample_leaf_inspection.jpg",
            "Leaf Blight",
            92.4,
            45,
            "Spray fermented buttermilk (Chaach) @ 50ml/L or Pseudomonas fluorescens.",
            "Apply Mancozeb 75% WP @ 2.5g/L on lower foliage."
        ))

        # Seed sample irrigation actions
        cursor.execute("""
        INSERT INTO irrigation_actions (timestamp, crop_type, moisture, litres_allocated, water_saved_litres, trigger_type, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            (now - datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S"),
            "Sugarcane",
            34.2,
            1200.0,
            450.0,
            "auto",
            "Automated micro-drip cycle completed. Target moisture 50% restored."
        ))

        # Seed default settings
        cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('language', 'en')")
        cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('theme', 'light')")
        cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('active_crop', 'sugarcane')")
        cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('farm_area_acres', '3.5')")

        conn.commit()

    conn.close()

def save_sensor_reading(data: Dict[str, Any]) -> int:
    """Inserts a new sensor reading."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO sensors_log (timestamp, soil_moisture, temperature, humidity, ph, nitrogen, phosphorus, potassium, health_score, condition_alert, mode)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get("timestamp", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        data["soil_moisture"],
        data["temperature"],
        data["humidity"],
        data["ph"],
        data["nitrogen"],
        data["phosphorus"],
        data["potassium"],
        data["health_score"],
        data.get("condition_alert", "Optimal"),
        data.get("mode", "normal")
    ))
    record_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return record_id

def get_latest_sensor_reading() -> Optional[Dict[str, Any]]:
    """Fetches the most recent sensor reading."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sensors_log ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_sensor_history(limit: int = 30) -> List[Dict[str, Any]]:
    """Fetches recent sensor telemetry history for charts."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sensors_log ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in reversed(rows)]

def save_crop_recommendation(rec: Dict[str, Any]):
    """Stores recommendation record."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO crop_recommendations (timestamp, n, p, k, ph, temp, humidity, rainfall, top1_crop, top1_prob, top2_crop, top2_prob, top3_crop, top3_prob)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        rec["n"], rec["p"], rec["k"], rec["ph"], rec["temp"], rec["humidity"], rec["rainfall"],
        rec["top1_crop"], rec["top1_prob"], rec.get("top2_crop"), rec.get("top2_prob"), rec.get("top3_crop"), rec.get("top3_prob")
    ))
    conn.commit()
    conn.close()

def save_disease_scan(scan: Dict[str, Any]):
    """Stores leaf disease scan record."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO disease_scans (timestamp, filename, detected_disease, confidence, severity, organic_treatment, chemical_treatment)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        scan["filename"], scan["detected_disease"], scan["confidence"], scan["severity"],
        scan["organic_treatment"], scan["chemical_treatment"]
    ))
    conn.commit()
    conn.close()

def get_recent_disease_scans(limit: int = 5) -> List[Dict[str, Any]]:
    """Returns recent disease scans."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM disease_scans ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def save_irrigation_action(action: Dict[str, Any]):
    """Records an irrigation cycle."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO irrigation_actions (timestamp, crop_type, moisture, litres_allocated, water_saved_litres, trigger_type, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        action["crop_type"], action["moisture"], action["litres_allocated"],
        action["water_saved_litres"], action.get("trigger_type", "auto"), action.get("notes", "")
    ))
    conn.commit()
    conn.close()

def get_recent_irrigation_actions(limit: int = 5) -> List[Dict[str, Any]]:
    """Returns recent irrigation events."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM irrigation_actions ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]
