from pymongo import MongoClient
import certifi

uri = "mongodb+srv://elisha_admin:1234qwerty@ac-3ay9hks.x7vtlhf.mongodb.net/PivotalRealEstate?retryWrites=true&w=majority"

try:
    client = MongoClient(uri, tlsCAFile=certifi.where())
    print("Connected to MongoDB version:", client.server_info()["version"])
    # Create or access your database
    db = client["PivotalRealEstate"]

    # Create or access your collections
    owners_collection = db["owners"]
    properties_collection = db["properties"]
    # Sample data for testing
    sample_owner = {
        "owner_id": "owner_001",
        "full_name": "John Doe",
        "mailing_address": "123 Main St, Seattle, WA",
        "phone_numbers": [
            {"number": "555-1234", "source": "Versium", "valid": True}
        ],
        "life_events": [
            {"type": "divorce", "date": "2023-10-01"}
        ],
        "properties": ["property_001"]
    }

    sample_property = {
        "property_id": "property_001",
        "apn": "APN123456",
        "address": "456 Market St, Seattle, WA",
        "owner_id": "owner_001",
        "sale_info": {
            "instrument": "warranty deed",
            "sale_price": 95000,
            "sale_reason": "gift",
            "date": "2022-06-15"
        },
        "architectural_grade": "C",
        "nuisance_flags": ["power lines"]
    }

    # Insert sample documents
    owners_collection.insert_one(sample_owner)
    properties_collection.insert_one(sample_property)

    print("Data inserted successfully!")
except Exception as e:
    print(f"Connection failed: {str(e)}")



