import pandas as pd
import os
import pickle

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

# =========================
# LOAD DATA
# =========================
INPUT_PATH = "data/clean/traffic_clean.csv"
MODEL_PATH = "models/traffic_model.pkl"

df = pd.read_csv(INPUT_PATH)

print("Data Loaded:")
print(df.head())

# =========================
# FEATURE ENGINEERING
# =========================

# Convert datetime
df["datetime"] = pd.to_datetime(df["datetime"])

# Tambah fitur waktu
df["hour"] = df["datetime"].dt.hour
df["day"] = df["datetime"].dt.dayofweek

# =========================
# FEATURES & TARGET
# =========================
features = ["hour", "day"]
target = "traffic"

X = df[features]
y = df[target]

# =========================
# SPLIT DATA
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =========================
# TRAIN MODEL
# =========================
model = RandomForestRegressor(n_estimators=100)

model.fit(X_train, y_train)

# =========================
# EVALUATION
# =========================
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)

print(f"\nMAE: {mae}")

# =========================
# SAVE MODEL
# =========================
os.makedirs("models", exist_ok=True)

with open(MODEL_PATH, "wb") as f:
    pickle.dump(model, f)

print(f"\nModel berhasil disimpan di: {MODEL_PATH}")
