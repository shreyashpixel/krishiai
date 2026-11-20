"""
================================================================================
KrishiAI - One-Click Launcher & System Bootstrapper
================================================================================
Runs on any standard Windows laptop with a single command:
    python run.py

Features:
- Verifies & auto-installs missing dependencies without manual intervention
- Prepares SQLite database and seeds realistic historical telemetry
- Generates 24-crop balanced agronomic dataset and trains ML models if absent
- Boots FastAPI ASGI server on http://localhost:8000
- Opens default browser automatically for live demo evaluation
================================================================================
"""

import sys
import os
import time
import subprocess
import threading
import webbrowser
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

BANNER = r"""
================================================================================
  _  __     _     _     _          _____ 
 | |/ /    (_)   | |   (_)   /\   |_   _|
 | ' / _ __ _ ___| |__  _   /  \    | |  
 |  < | '__| / __| '_ \| | / /\ \   | |  
 | . \| |  | \__ \ | | | |/ ____ \ _| |_ 
 |_|\_\_|  |_|___/_| |_|_/_/    \_\_____|
                                         
   Smart Agriculture & AI Precision Agronomy System
   College Innovation Project Demonstration Prototype
================================================================================
"""

REQUIRED_PACKAGES = [
    ("fastapi", "fastapi"),
    ("uvicorn", "uvicorn"),
    ("pydantic", "pydantic"),
    ("sklearn", "scikit-learn"),
    ("pandas", "pandas"),
    ("numpy", "numpy"),
    ("PIL", "Pillow"),
    ("reportlab", "reportlab"),
    ("requests", "requests"),
    ("multipart", "python-multipart")
]

def check_and_install_dependencies():
    """Checks for required Python modules and installs any missing packages."""
    missing = []
    print("[1/5] Checking Python package prerequisites...")
    for mod_name, pkg_name in REQUIRED_PACKAGES:
        try:
            __import__(mod_name)
        except ImportError:
            missing.append(pkg_name)

    if missing:
        print(f"      Missing packages detected: {', '.join(missing)}")
        print(f"      Auto-installing via pip ({sys.executable})...")
        try:
            cmd = [sys.executable, "-m", "pip", "install"] + missing
            subprocess.check_call(cmd)
            print("      All prerequisite packages installed successfully!")
        except Exception as e:
            print(f"      [WARNING] Pip auto-installation encountered: {e}")
            print("      Continuing execution with available packages...")
    else:
        print("      All prerequisite packages are already installed and verified.")

def initialize_directories_and_data():
    """Ensures directories exist and seeds database and ML models."""
    print("[2/5] Initializing workspace directories & local storage...")
    (BASE_DIR / "data").mkdir(exist_ok=True)
    (BASE_DIR / "models").mkdir(exist_ok=True)

    # Add BASE_DIR to sys.path
    if str(BASE_DIR) not in sys.path:
        sys.path.insert(0, str(BASE_DIR))

    print("[3/5] Bootstrapping SQLite database & telemetry history...")
    from backend.database import init_db, seed_initial_data
    init_db()
    seed_initial_data()
    print("      Database verified at data/krishiai.db with historical telemetry.")

    print("[4/5] Checking Machine Learning models & agronomic training data...")
    from backend.ml_crops import crop_recommender
    crop_recommender.load_or_train()
    print("      Random Forest Crop Recommender ready (models/crop_rf_model.pkl).")

def open_browser_when_ready(host: str, port: int):
    """Waits for server to respond on HTTP and launches browser."""
    url = f"http://{host}:{port}"
    health_url = f"{url}/api/health"
    
    import urllib.request
    max_attempts = 30
    for _ in range(max_attempts):
        time.sleep(0.5)
        try:
            with urllib.request.urlopen(health_url, timeout=1.0) as resp:
                if resp.status == 200:
                    print(f"\n[+] Server is LIVE at {url}")
                    print(f"[+] Launching default web browser for demo...\n")
                    webbrowser.open(url)
                    return
        except Exception:
            pass

    print(f"\n[!] Server started. Open your browser at: {url}\n")

def main():
    print(BANNER)
    check_and_install_dependencies()
    initialize_directories_and_data()

    host = "127.0.0.1"
    port = 8000

    print(f"[5/5] Starting KrishiAI ASGI Server on http://{host}:{port}...")

    # Spawn background thread to open browser
    browser_thread = threading.Thread(
        target=open_browser_when_ready, 
        args=(host, port), 
        daemon=True
    )
    browser_thread.start()

    import uvicorn
    # Start server
    try:
        uvicorn.run(
            "backend.main:app",
            host=host,
            port=port,
            log_level="info",
            access_log=False
        )
    except KeyboardInterrupt:
        print("\nKrishiAI server stopped gracefully by user.")

if __name__ == "__main__":
    main()
