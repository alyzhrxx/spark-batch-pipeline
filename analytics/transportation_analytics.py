import pandas as pd

# =========================
# KPI METRICS
# =========================
def compute_kpis(df):
    total_trips = len(df)
    total_revenue = df["fare"].sum()
    avg_distance = df["distance_km"].mean()

    return total_trips, total_revenue, avg_distance


# =========================
# BAR CHARTS
# =========================
def revenue_per_city(df):
    return df.groupby("city")["fare"].sum()


def trips_per_driver(df):
    return df.groupby("driver_id")["trip_id"].count()


def vehicle_distribution(df):
    if "vehicle_type" in df.columns:
        return df["vehicle_type"].value_counts()
    else:
        return None


# =========================
# LINE CHARTS
# =========================
def realtime_trips(df):
    if "timestamp" not in df.columns:
        return None

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.dropna(subset=["timestamp"])

    if df.empty:
        return None

    df = df.set_index("timestamp")
    trips_time = df["trip_id"].resample("1min").count()

    return trips_time


def mobility_trend(df):
    if "timestamp" not in df.columns:
        return None

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.dropna(subset=["timestamp"])

    if df.empty:
        return None

    df = df.set_index("timestamp")
    mobility = df["distance_km"].resample("1min").sum()

    return mobility


# =========================
# TABLES
# =========================
def abnormal_trips(df):
    abnormal = df[
        (df["fare"] > 100000) |
        (df["distance_km"] > 20)
    ]
    return abnormal