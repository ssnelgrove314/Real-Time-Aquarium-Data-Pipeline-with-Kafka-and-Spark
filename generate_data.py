import random
from datetime import datetime

def generate_sensor_data():
    """
    Simulates sensor readings for an aquarium.
    Returns a dictionary with sensor values and a timestamp.
    """
    return {
        "timestamp": datetime.now().isoformat(),
        "sensors": {
            "temperature": round(random.uniform(72, 82), 1),  # °F
            "tds": round(random.uniform(150, 300), 1),        # ppm
            "ph": round(random.uniform(6.5, 8.0), 2),         # pH
            "nitrate": round(random.uniform(0, 40), 1),       # ppm
            "ammonia": round(random.choices([0, random.uniform(0.01, 0.1)], weights=[0.9, 0.1])[0], 2),  # ppm
            "nitrite": round(random.uniform(0, 0.5), 2),      # ppm
            "gh": round(random.uniform(4, 12), 1),            # dGH
            "kh": round(random.uniform(3, 10), 1)             # dKH
        }
    }
