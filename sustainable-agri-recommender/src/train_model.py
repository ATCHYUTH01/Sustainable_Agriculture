#!/usr/bin/env python3
"""
Automated training script for RandomForestRegressor baseline model.

Workflow:
- Load synthetic soil dataset from data/raw/soil_samples_synthetic_week1.csv
  (generate it if the file does not exist)
- Use BaselineFertilizerRecommender.recommend_for_row to create target columns
  (N_need, P_need, K_need) in kg/ha
- Split into train/test
- Train RandomForestRegressor to predict N_need
- Print MAE
- Save trained model to models/rf_baseline.pkl
"""

from pathlib import Path
import sys
from typing import Tuple

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
import joblib

# Ensure project root is on sys.path for imports when executed from any CWD
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.recommender import BaselineFertilizerRecommender  # noqa: E402
from src.generate_synthetic_data import (  # noqa: E402
    generate_synthetic_soil_data,
    save_data_to_csv,
)


DATA_PATH = PROJECT_ROOT / "data" / "raw" / "soil_samples_synthetic_week1.csv"
MODELS_DIR = PROJECT_ROOT / "models"
MODEL_PATH = MODELS_DIR / "rf_baseline.pkl"


def load_or_generate_dataset(data_csv_path: Path) -> pd.DataFrame:
    """Load the dataset from CSV or generate it if missing."""
    data_csv_path.parent.mkdir(parents=True, exist_ok=True)
    if not data_csv_path.exists():
        df_generated = generate_synthetic_soil_data(n_samples=500, random_seed=42)
        save_data_to_csv(df_generated, str(data_csv_path))
    return pd.read_csv(data_csv_path)


def add_target_columns_using_recommender(df: pd.DataFrame) -> pd.DataFrame:
    """Compute N/P/K targets using the baseline recommender and append as columns."""
    recommender = BaselineFertilizerRecommender()

    def compute_row_targets(row: pd.Series) -> pd.Series:
        recs = recommender.recommend_for_row(row.to_dict())
        return pd.Series(
            {
                "N_need": recs.get("N_need_kg_ha", 0.0),
                "P_need": recs.get("P_need_kg_ha", 0.0),
                "K_need": recs.get("K_need_kg_ha", 0.0),
            }
        )

    targets_df = df.apply(compute_row_targets, axis=1)
    return pd.concat([df, targets_df], axis=1)


def build_features_and_target(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    """Prepare model features and target for training."""
    required_columns = [
        "pH",
        "N",
        "P",
        "K",
        "organic_carbon",
        "moisture",
        "crop",
        "N_need",
    ]
    for column_name in required_columns:
        if column_name not in df.columns:
            raise ValueError(f"Missing required column '{column_name}' in dataframe")

    feature_columns = ["pH", "N", "P", "K", "organic_carbon", "moisture", "crop"]
    features = df[feature_columns].copy()
    features = pd.get_dummies(features, columns=["crop"], drop_first=True)

    target = df["N_need"].astype(float)
    return features, target


def train_random_forest_regressor(
    features_train: pd.DataFrame, target_train: pd.Series, n_estimators: int = 200, random_state: int = 42
) -> RandomForestRegressor:
    """Train a RandomForestRegressor model."""
    model = RandomForestRegressor(
        n_estimators=n_estimators,
        random_state=random_state,
        n_jobs=-1,
    )
    model.fit(features_train, target_train)
    return model


def evaluate_model_mae(model: RandomForestRegressor, features_test: pd.DataFrame, target_test: pd.Series) -> float:
    """Evaluate model using Mean Absolute Error (MAE)."""
    predictions = model.predict(features_test)
    mae = mean_absolute_error(target_test, predictions)
    return mae


def main() -> None:
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    # Load/generate dataset
    df = load_or_generate_dataset(DATA_PATH)

    # Add target columns from rule-based recommender
    df = add_target_columns_using_recommender(df)

    # Build features/target and split
    features, target = build_features_and_target(df)
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

    # Train model
    model = train_random_forest_regressor(X_train, y_train)

    # Evaluate
    mae = evaluate_model_mae(model, X_test, y_test)
    print(f"MAE: {mae:.4f}")

    # Save
    joblib.dump(model, MODEL_PATH)
    print(f"Saved model to: {MODEL_PATH}")


if __name__ == "__main__":
    main()

