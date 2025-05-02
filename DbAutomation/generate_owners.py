import csv
import random
from faker import Faker

fake = Faker()
RECORD_COUNT = 2000
OUTPUT_FILE = "owners_stress_test.csv"
EDGE_CASE_RATE = 0.15
FORCED_DUPLICATE_APN = "123-45-678"  # Cleans to 00000012345678 -> last 10: 0001234567

# Data configuration
LIFE_EVENTS = ["Bankruptcy", "Inheritance", "Divorce", "", "Tax Lien", "Probate"]
UPLOAD_SOURCES = ["REISift", "Stewart Title", "County Records", "Manual Entry"]
LISTS = ["List A", "List B", "List C", "VIP Clients", "High Risk", "Pre-foreclosure"]
DOMAINS = ["example.com", "test.com", "fake.org"]

def generate_apn():
    """Generate APN with potential formatting variations"""
    base = f"{random.randint(1,9999):04}-{random.randint(1,999):03}"
    if random.random() < 0.3:
        return f"{base}-{random.choice(['A', 'B', ''])}"
    return base

def generate_phone():
    return random.choice([
        f"{random.randint(200,999)}{random.randint(200,999)}{random.randint(1000,9999)}",  # Plain
        f"({random.randint(200,999)}) {random.randint(200,999)}-{random.randint(1000,9999)}",  # Formatted
        f"+1-{random.randint(200,999)}-{random.randint(200,999)}-{random.randint(1000,9999)}"  # Intl
    ])

def inject_edge_cases(record):
    """Inject edge cases with mailing address variations"""
    case = random.choice([1, 2, 3, 4, 5, 6])
    is_forced_duplicate = False
    
    if case == 1:  # Missing critical fields
        empty_field = random.choice(["apn", "full_name", "mailing_street"])
        record[empty_field] = ""
        
    elif case == 2:  # Invalid mailing address
        record.update({
            "mailing_street": "Invalid Street 123",
            "mailing_city": "",
            "mailing_state": random.choice(["XX", "Washington", "WA-WA"]),
            "mailing_zip": random.choice(["00000", "ABCDE", "98001-12345"])
        })
        
    elif case == 3:  # Mixed format arrays
        record["phones"] = random.choice([
            "123| |invalid|555-1234",
            "mixed-formats|(555) 123-4567|+1-800-1234",
            "|||"  # All empty
        ])
        
    elif case == 4:  # Special characters
        record.update({
            "full_name": random.choice([
                "María Doñe-Smith (CEO)",
                "张伟",
                "O'Connor–Johnson"
            ]),
            "mailing_street": "123 Ümlaut Ln #" + str(random.randint(1,100))
        })
        
    elif case == 5:  # True duplicates (all dedup keys match)
        record.update({
            "apn": FORCED_DUPLICATE_APN,
            "full_name": "FORCED DUPLICATE OWNER",
            "mailing_street": "123 Duplicate Lane",
            "mailing_city": "Seattle",
            "mailing_state": "WA",
            "mailing_zip": "98001"
        })
        is_forced_duplicate = True
        
    elif case == 6:  # Valid but complex address
        record.update({
            "mailing_street": f"{random.randint(1,99999)}th Ave NE Apt {random.randint(1,5000)}",
            "mailing_zip": f"{random.randint(98001, 99403)}-{random.randint(1000,9999)}"
        })
        
    return record, is_forced_duplicate

def generate_record(is_edge_case):
    # Generate base valid record
    first_name = fake.first_name()
    last_name = fake.last_name()
    
    record = {
        "apn": generate_apn(),
        "full_name": f"{first_name} {last_name}",
        "first_name": first_name,
        "last_name": last_name,
        "mailing_street": fake.street_address(),
        "mailing_city": fake.city(),
        "mailing_state": "WA",
        "mailing_zip": fake.postcode_in_state(state_abbr="WA"),
        "phones": "|".join([generate_phone() for _ in range(random.randint(1,3))]),
        "emails": "|".join([
            f"{first_name.lower()}.{last_name.lower()}@{random.choice(DOMAINS)}",
            f"{last_name.lower()}{random.randint(10,99)}@{random.choice(DOMAINS)}"
        ][:random.randint(1,2)]),
        "relatives": "|".join([f"{fake.first_name()} {last_name}" 
                             for _ in range(random.randint(0,2))]),
        "life_events": random.choice(LIFE_EVENTS),
        "upload_sources": "|".join(random.sample(UPLOAD_SOURCES, random.randint(1,2))),
        "lists": "|".join(random.sample(LISTS, random.randint(1,3))),
        "score": random.randint(50,100)
    }

    # Add middle name for some records
    if random.random() < 0.05:
        middle = fake.first_name()
        record.update({
            "full_name": f"{first_name} {middle[0]}. {last_name}",
            "first_name": f"{first_name} {middle[0]}."
        })

    # Inject edge cases
    if is_edge_case:
        return inject_edge_cases(record)
    return record, False

# Generate dataset
records = []
generated_hashes = set()
edge_case_count = int(RECORD_COUNT * EDGE_CASE_RATE)
forced_duplicates = 0

while len(records) < RECORD_COUNT:
    is_edge = len(records) < edge_case_count
    record, is_forced_dup = generate_record(is_edge)
    
    # Create hash of dedup fields
    dedup_hash = hash(frozenset({
        k: v for k, v in record.items() 
        if k in ["apn", "full_name", "mailing_street", "mailing_city", "mailing_state", "mailing_zip"]
    }.items()))
    
    if is_forced_dup:
        records.append(record)
        forced_duplicates += 1
    else:
        if dedup_hash not in generated_hashes:
            generated_hashes.add(dedup_hash)
            records.append(record)

# Final shuffle and trim
random.shuffle(records)
records = records[:RECORD_COUNT]

# Write to CSV
with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=records[0].keys())
    writer.writeheader()
    writer.writerows(records)

print(f"""Generated {len(records)} owner records:
- Normal records: {RECORD_COUNT - edge_case_count}
- Edge cases: {edge_case_count}
  - Forced duplicates: {forced_duplicates}
  - Invalid addresses: {edge_case_count//6}
  - Missing fields: {edge_case_count//6}
  - Special chars: {edge_case_count//6}
  - Complex formats: {edge_case_count//6}""")