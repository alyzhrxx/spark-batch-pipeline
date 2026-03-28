def check_alerts(df):
    alerts = []

    if df["fare"].max() > 90000:
        alerts.append("High fare detected")

    if df["distance_km"].max() > 15:
        alerts.append("Long distance trip detected")

    if len(df) > 50:
        alerts.append("High trip volume")

    return alerts