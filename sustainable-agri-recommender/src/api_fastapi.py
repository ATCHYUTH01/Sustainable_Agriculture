#!/usr/bin/env python3
"""
FastAPI application that serves fertilizer recommendations.

- Loads the trained RandomForestRegressor model from models/rf_baseline.pkl
- POST /predict accepts JSON with: pH, N, P, K, organic_carbon, moisture, crop
- Returns fertilizer recommendations: N_need (ML), P_need/K_need (baseline)
"""

from pathlib import Path
import sys
from typing import List, Dict, Any

import pandas as pd
import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# Ensure project root on path for module imports
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.recommender import BaselineFertilizerRecommender  # noqa: E402
from src.generate_synthetic_data import (  # noqa: E402
    generate_synthetic_soil_data,
    save_data_to_csv,
)

DATA_PATH = PROJECT_ROOT / "data" / "raw" / "soil_samples_synthetic_week1.csv"
MODEL_PATH = PROJECT_ROOT / "models" / "rf_baseline.pkl"


def load_or_generate_dataset(data_csv_path: Path) -> pd.DataFrame:
    data_csv_path.parent.mkdir(parents=True, exist_ok=True)
    if not data_csv_path.exists():
        df_generated = generate_synthetic_soil_data(n_samples=500, random_seed=42)
        save_data_to_csv(df_generated, str(data_csv_path))
    return pd.read_csv(data_csv_path)


def derive_training_feature_columns(dataset: pd.DataFrame) -> List[str]:
    feature_columns = ["pH", "N", "P", "K", "organic_carbon", "moisture", "crop"]
    features = dataset[feature_columns].copy()
    features = pd.get_dummies(features, columns=["crop"], drop_first=True)
    return list(features.columns)


app = FastAPI(title="Fertilizer Recommender API", version="0.1.0")

# Load model
try:
    model = joblib.load(MODEL_PATH)
except Exception as exc:
    model = None
    model_load_error = exc
else:
    model_load_error = None

# Prepare reference training feature columns for encoding consistency
try:
    _dataset_for_columns = load_or_generate_dataset(DATA_PATH)
    TRAIN_FEATURE_COLUMNS = derive_training_feature_columns(_dataset_for_columns)
except Exception as exc:
    TRAIN_FEATURE_COLUMNS = None
    columns_build_error = exc
else:
    columns_build_error = None

baseline_recommender = BaselineFertilizerRecommender()


class SoilSample(BaseModel):
    pH: float = Field(..., description="Soil pH")
    N: float = Field(..., description="Nitrogen (mg/kg)")
    P: float = Field(..., description="Phosphorus (mg/kg)")
    K: float = Field(..., description="Potassium (mg/kg)")
    organic_carbon: float = Field(..., description="Organic carbon (%)")
    moisture: float = Field(..., description="Soil moisture (%)")
    crop: str = Field(..., description="Crop name")


class Recommendation(BaseModel):
    N_need: float
    P_need: float
    K_need: float
    ph_warning: str | None = None


@app.get("/")
def read_root() -> Dict[str, Any]:
    return {"status": "ok", "model_loaded": model is not None}


@app.post("/predict", response_model=Recommendation)
def predict(sample: SoilSample) -> Recommendation:
    if model is None:
        raise HTTPException(status_code=500, detail=f"Model not loaded: {model_load_error}")
    if TRAIN_FEATURE_COLUMNS is None:
        raise HTTPException(status_code=500, detail=f"Feature columns unavailable: {columns_build_error}")

    # Build model features aligned to training columns
    input_df = pd.DataFrame([{**sample.dict()}])
    input_features = input_df[["pH", "N", "P", "K", "organic_carbon", "moisture", "crop"]].copy()
    input_features = pd.get_dummies(input_features, columns=["crop"], drop_first=True)
    input_features = input_features.reindex(columns=TRAIN_FEATURE_COLUMNS, fill_value=0.0)

    # Predict N requirement
    try:
        n_need_pred = float(model.predict(input_features)[0])
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {exc}")

    # Baseline for P/K and warning
    baseline_recs = baseline_recommender.recommend_for_row(sample.dict())

    return Recommendation(
        N_need=max(0.0, n_need_pred),
        P_need=float(baseline_recs.get("P_need_kg_ha", 0.0)),
        K_need=float(baseline_recs.get("K_need_kg_ha", 0.0)),
        ph_warning=baseline_recs.get("ph_warning") or None,
    )


if __name__ == "__main__":
    try:
        import uvicorn
    except Exception:
        raise SystemExit("uvicorn is required to run the API locally: pip install uvicorn fastapi")
    uvicorn.run("src.api_fastapi:app", host="0.0.0.0", port=8000, reload=False)
