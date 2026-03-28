import json
import time
import random
import os
from datetime import datetime

OUTPUT_FOLDER = "stream_data/transportation"

cities = ["Jakarta", "Bandung", "Surabaya", "Medan", "Banjarmasin"]
drivers = ["D001", "D002", "D003", "D004", "D005"]
passengers = ["P001", "P002", "P003", "P004", "P005"]

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

i = 0

while True:
    trip = {
        "trip_id": i,
        "driver_id": random.choice(drivers),
        "passenger_id": random.choice(passengers),
        "city": random.choice(cities),
        "distance_km": round(random.uniform(1, 20), 2),
        "fare": round(random.uniform(10000, 100000), 2),
        "timestamp": datetime.now().isoformat()
    }

    filename = f"{OUTPUT_FOLDER}/trip_{i}.json"
    with open(filename, "w") as f:
        json.dump(trip, f)

    print(f"Generated {filename}")
    i += 1
    time.sleep(2)