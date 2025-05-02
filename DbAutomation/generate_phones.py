import csv
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()
RECORD_COUNT = 2000
EDGE_CASE_RATE = 0.15
OUTPUT_FILE = "phones_stress_test.csv"
FORCED_DUPLICATE_NUMBER = "9998887777"

SOURCES = ["Tracers", "Versium", "TLO", "Whitepages", "Manual Entry"]
STATUSES = ["verified", "invalid", "pending", "dnc", "wrong_number"]

def generate_phone_number():
    return f"{random.randint(200,999)}{random.randint(200,999)}{random.randint(1000,9999)}"

def generate_owner_apn():
    return f"{random.randint(100,999)}-{random.randint(100,999)}-{random.randint(100,999)}"

def generate_phone_record(is_edge_case=False):
    record = {
        "number": generate_phone_number(),
        "owner_apn": generate_owner_apn(),
        "source": random.choice(SOURCES),
        "status": random.choice(STATUSES),
        "verified": random.choice([True, False]),
        "sequence": random.randint(1, 5),
        "traced_at": (datetime.now() - timedelta(days=random.randint(0, 180))).isoformat(),
        "enriched_at": (datetime.now() - timedelta(days=random.randint(0, 180))).isoformat(),
        "tags": "|".join(random.sample(["skip", "high_priority", "needs_review", "ai_flagged"], random.randint(0, 2)))
    }

    if is_edge_case:
        case = random.choice([1, 2, 3, 4, 5])
        if case == 1:  # Missing fields
            del record["status"]
            record["number"] = ""
        elif case == 2:  # Type issues
            record["verified"] = random.choice(["yes", "false", "maybe"])
            record["sequence"] = random.choice(["one", None])
        elif case == 3:  # Special characters or formatting
            record["number"] = random.choice(["(555) 123-4567", "+1-800-FAKE", "12.34.5678"])
        elif case == 4:  # Forced duplicate
            record["number"] = FORCED_DUPLICATE_NUMBER
        elif case == 5:  # Array issue
            record["tags"] = "|||"
    
    return record

# Generate records
records = []
unique_numbers = set()
edge_case_count = int(RECORD_COUNT * EDGE_CASE_RATE)

while len(records) < RECORD_COUNT:
    is_edge = len(records) < edge_case_count
    record = generate_phone_record(is_edge_case=is_edge)

    if not is_edge:
        if record["number"] not in unique_numbers:
            unique_numbers.add(record["number"])
            records.append(record)
    else:
        records.append(record)

# Write to CSV
with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=records[0].keys())
    writer.writeheader()
    writer.writerows(records)

print(f"Generated {len(records)} phone records for stress testing")
print(f"- Edge cases: {edge_case_count}")
print(f"- Normal records: {RECORD_COUNT - edge_case_count}")
