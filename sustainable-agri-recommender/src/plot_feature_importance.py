import joblib
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Set absolute paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = PROJECT_ROOT / "models" / "rf_baseline.pkl"
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "soil_samples_synthetic_week1.csv"
OUTPUT_PATH = PROJECT_ROOT / "models" / "feature_importance.png"

# Load trained model
model = joblib.load(MODEL_PATH)

# Load data and prepare features (same as in train_model.py)
df = pd.read_csv(DATA_PATH)
feature_columns = ["pH", "N", "P", "K", "organic_carbon", "moisture", "crop"]
features = df[feature_columns].copy()
features = pd.get_dummies(features, columns=["crop"], drop_first=True)

# Get feature importances
importances = model.feature_importances_
feature_names = features.columns

# Plot
plt.figure(figsize=(10, 6))
plt.barh(feature_names, importances, color="seagreen")
plt.xlabel("Importance")
plt.title("Feature Importances — RandomForest Fertilizer Recommender")
plt.tight_layout()
plt.savefig(OUTPUT_PATH, dpi=300)
plt.show()
print(f"Feature importance plot saved as {OUTPUT_PATH}")
