import csv
import random
from faker import Faker
from datetime import datetime, timedelta, timezone

fake = Faker()
RECORD_COUNT = 2000
EDGE_CASE_RATE = 0.15
OUTPUT_FILE = "life_events_stress_test.csv"

EVENT_TYPES = ["marriage", "death", "trust_creation", "divorce", "ownership_transfer"]

def generate_life_event_record(is_edge_case=False):
    record = {
        "apn": f"{random.randint(100,999)}-{random.randint(100,999)}-{random.randint(100,999)}",
        "event_type": random.choice(EVENT_TYPES),
        "event_date": (datetime.now(timezone.utc) - timedelta(days=random.randint(0, 3650))).isoformat(),
        "description": fake.sentence(),
        "documents": "|".join([fake.file_name(extension='pdf') for _ in range(random.randint(0, 3))]),
        "last_updated": datetime.now(timezone.utc).isoformat()
    }

    if is_edge_case:
        case = random.choice([1, 2, 3, 4, 5])
        if case == 1:  # Schema violations
            del record["event_type"]
            record["event_date"] = "not_a_date"
        elif case == 2:  # Null handling
            record["event_date"] = ""
            record["documents"] = None
        elif case == 3:  # Invalid array
            record["documents"] = "|||"
        elif case == 4:  # Huge values
            record["description"] = fake.text(2000)
        elif case == 5:  # Mixed types
            record["event_type"] = 123
            record["apn"] = True
    
    return record

# Generation logic same as phones...
