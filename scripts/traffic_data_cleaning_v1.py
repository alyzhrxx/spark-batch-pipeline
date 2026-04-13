import pandas as pd
import os

# Path
INPUT_PATH = "data/raw/traffic_smartcity_v1.csv"
OUTPUT_PATH = "data/clean/traffic_clean.csv"

# Buat folder clean
os.makedirs("data/clean", exist_ok=True)

# Load data
df = pd.read_csv(INPUT_PATH)

print("Data sebelum cleaning:")
print(df.head())

# =========================
# CLEANING
# =========================
df = df.dropna()

# =========================
# FEATURE ENGINEERING
# =========================
if "timestamp" in df.columns:
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["hour"] = df["timestamp"].dt.hour
    df["day"] = df["timestamp"].dt.dayofweek

# =========================
# SAVE
# =========================
df.to_csv(OUTPUT_PATH, index=False)

print("\nData setelah cleaning:")
print(df.head())

print(f"\nData clean disimpan di: {OUTPUT_PATH}")
