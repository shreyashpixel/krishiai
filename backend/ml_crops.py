"""
KrishiAI - Crop Recommendation ML Engine
Uses Random Forest trained on agronomic features (N, P, K, pH, Temp, Humidity, Rainfall).
Includes automated realistic dataset generation and training.
"""
import os
import pickle
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Tuple
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from backend.config import (
    CROP_MODEL_PATH, 
    DATASET_PATH, 
    CROP_AGRONOMY, 
    SUPPORTED_CROPS
)

class CropRecommender:
    def __init__(self):
        self.model: RandomForestClassifier = None
        self.feature_columns = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
        self.load_or_train()

    def generate_synthetic_dataset(self, samples_per_crop: int = 100) -> pd.DataFrame:
        """
        Synthesizes a realistic agronomic dataset based on ICAR / agricultural science standards
        for 24 crops including Maharashtra cash crops.
        """
        rows = []
        np.random.seed(42)

        for crop, ranges in CROP_AGRONOMY.items():
            n_min, n_max = ranges["N"]
            p_min, p_max = ranges["P"]
            k_min, k_max = ranges["K"]
            t_min, t_max = ranges["temp"]
            h_min, h_max = ranges["humidity"]
            ph_min, ph_max = ranges["ph"]
            r_min, r_max = ranges["rainfall"]

            for _ in range(samples_per_crop):
                # Sample with slight normal jitter
                n = float(np.clip(np.random.uniform(n_min, n_max) + np.random.normal(0, 3), 5, 200))
                p = float(np.clip(np.random.uniform(p_min, p_max) + np.random.normal(0, 3), 5, 160))
                k = float(np.clip(np.random.uniform(k_min, k_max) + np.random.normal(0, 3), 5, 220))
                temp = float(np.clip(np.random.uniform(t_min, t_max) + np.random.normal(0, 1.2), 8, 45))
                humidity = float(np.clip(np.random.uniform(h_min, h_max) + np.random.normal(0, 2), 10, 100))
                ph = float(np.clip(np.random.uniform(ph_min, ph_max) + np.random.normal(0, 0.2), 4.0, 9.0))
                rainfall = float(np.clip(np.random.uniform(r_min, r_max) + np.random.normal(0, 5), 15, 350))

                rows.append({
                    "N": round(n, 2),
                    "P": round(p, 2),
                    "K": round(k, 2),
                    "temperature": round(temp, 2),
                    "humidity": round(humidity, 2),
                    "ph": round(ph, 2),
                    "rainfall": round(rainfall, 2),
                    "label": crop
                })

        df = pd.DataFrame(rows)
        df.to_csv(DATASET_PATH, index=False)
        print(f"Generated synthetic agricultural dataset with {len(df)} records at {DATASET_PATH}")
        return df

    def train_model(self) -> float:
        """Trains Random Forest Classifier on dataset and saves model pickle."""
        if not DATASET_PATH.exists():
            df = self.generate_synthetic_dataset()
        else:
            df = pd.read_csv(DATASET_PATH)

        X = df[self.feature_columns]
        y = df["label"]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

        clf = RandomForestClassifier(n_estimators=100, max_depth=14, random_state=42, n_jobs=1)
        clf.fit(X_train, y_train)

        y_pred = clf.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        print(f"Crop Recommender Model trained successfully! Test Accuracy: {acc*100:.2f}%", flush=True)

        with open(CROP_MODEL_PATH, "wb") as f:
            pickle.dump(clf, f)

        self.model = clf
        return acc

    def load_or_train(self):
        """Loads trained model if present, otherwise generates dataset and trains."""
        if CROP_MODEL_PATH.exists():
            try:
                with open(CROP_MODEL_PATH, "rb") as f:
                    self.model = pickle.load(f)
                print("Loaded pre-trained Crop Recommendation Random Forest model.")
            except Exception as e:
                print(f"Error loading model: {e}. Retraining...")
                self.train_model()
        else:
            self.train_model()

    def predict(self, n: float, p: float, k: float, ph: float, temp: float, humidity: float, rainfall: float) -> List[Dict[str, Any]]:
        """
        Predicts top 3 most suitable crops with probability percentages,
        agronomic match breakdown, and advice.
        """
        if self.model is None:
            self.load_or_train()

        features = pd.DataFrame([{
            "N": n,
            "P": p,
            "K": k,
            "temperature": temp,
            "humidity": humidity,
            "ph": ph,
            "rainfall": rainfall
        }])

        probabilities = self.model.predict_proba(features)[0]
        classes = self.model.classes_

        top_indices = np.argsort(probabilities)[::-1][:3]
        results = []

        CROP_DETAILS = {
            "sugarcane": {"season": "Annual / Kharif", "water": "High (Drip recommended)", "soil": "Deep rich loamy / Black cotton"},
            "cotton": {"season": "Kharif", "water": "Medium", "soil": "Deep black cotton soil"},
            "soybean": {"season": "Kharif", "water": "Medium", "soil": "Well-drained fertile loam"},
            "jowar": {"season": "Kharif / Rabi", "water": "Low to Drought-hardy", "soil": "Medium black or light loams"},
            "bajra": {"season": "Kharif", "water": "Low / Arid", "soil": "Sandy loam to light black soil"},
            "onion": {"season": "Rabi / Late Kharif", "water": "Moderate frequent", "soil": "Friable fertile sandy loam"},
            "grapes": {"season": "Perennial / Pruning cycle", "water": "Precision Drip", "soil": "Well-drained sandy loam / gravelly"},
            "pomegranate": {"season": "Bahar treatment", "water": "Low to moderate drip", "soil": "Well-drained light to medium"},
            "rice": {"season": "Kharif", "water": "Very High", "soil": "Clayey or heavy alluvial soils"},
            "wheat": {"season": "Rabi", "water": "Medium (3-4 irrigations)", "soil": "Well-drained loamy soil"},
            "maize": {"season": "Kharif / Rabi", "water": "Medium", "soil": "Fertile alluvial or red loam"},
            "chickpea": {"season": "Rabi", "water": "Low (moisture conservation)", "soil": "Heavy clay loam to black cotton"},
            "kidneybeans": {"season": "Kharif", "water": "Medium", "soil": "Light rich loam with organic matter"},
            "pigeonpeas": {"season": "Kharif", "water": "Low to Medium", "soil": "Deep well-drained loam"},
            "mothbeans": {"season": "Kharif", "water": "Very Low (Arid)", "soil": "Light sandy soil"},
            "mungbean": {"season": "Kharif / Summer", "water": "Low", "soil": "Well-drained loamy soil"},
            "blackgram": {"season": "Kharif / Summer", "water": "Low to Medium", "soil": "Heavier soils with good moisture retention"},
            "lentil": {"season": "Rabi", "water": "Low", "soil": "Alluvial or light loamy soil"},
            "watermelon": {"season": "Zaid / Summer", "water": "Medium drip", "soil": "Sandy loam with high organic carbon"},
            "muskmelon": {"season": "Zaid / Summer", "water": "Medium", "soil": "Well-drained sandy loam"},
            "apple": {"season": "Temperate perennial", "water": "Medium regular", "soil": "Loamy soil rich in organic matter"},
            "orange": {"season": "Subtropical", "water": "Medium drip", "soil": "Well-drained light loam to sandy loam"},
            "banana": {"season": "Annual", "water": "High regular drip", "soil": "Rich fertile clayey loam"},
            "coconut": {"season": "Perennial", "water": "High", "soil": "Coastal alluvial or laterite soil"}
        }

        for idx in top_indices:
            crop_name = classes[idx]
            prob = float(probabilities[idx])
            prob_percent = round(prob * 100, 1)

            # Fallback details if not found
            details = CROP_DETAILS.get(crop_name, {
                "season": "Kharif / Rabi", 
                "water": "Moderate", 
                "soil": "Well-drained loamy soil"
            })

            results.append({
                "crop": crop_name.capitalize(),
                "confidence": prob_percent,
                "season": details["season"],
                "water_requirement": details["water"],
                "soil_type": details["soil"],
                "rank": len(results) + 1
            })

        return results

# Singleton instance
crop_recommender = CropRecommender()
