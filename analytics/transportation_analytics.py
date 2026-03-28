import pandas as pd

def compute_kpis(df):
    total_trips = len(df)
    total_revenue = df["fare"].sum()
    avg_distance = df["distance_km"].mean()

    return total_trips, total_revenue, avg_distance

def revenue_per_city(df):
    return df.groupby("city")["fare"].sum()

def trips_per_driver(df):
    return df.groupby("driver_id")["trip_id"].count()