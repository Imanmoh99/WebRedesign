import pandas as pd
from pymongo import MongoClient, UpdateOne, IndexModel
from pymongo.errors import BulkWriteError
import uuid
import argparse
from datetime import datetime, timezone
import numpy as np
import re
import traceback
from typing import Dict, Any

# === CONFIGURATION ===
MONGO_URI = "mongodb+srv://elisha_admin:1234qwerty@ac-3ay9hks.x7vtlhf.mongodb.net/PivotalRealEstate?retryWrites=true&w=majority"
DB_NAME = "PivotalRealEstate"

# === COLLECTION SCHEMAS ===
COLLECTION_CONFIG = {
    "owners": {
        "dedup_keys": ["apn", "full_name", "mailing_street", "mailing_city", "mailing_state", "mailing_zip"],
        "record_type": "owner",
        "indexes": [
            IndexModel([("apn", 1), ("full_name", 1)], unique=True),
            IndexModel([("mailing_zip", 1)])
        ]
    },
    "properties": {
        "dedup_keys": ["apn"],
        "record_type": "property",
        "indexes": [
            IndexModel([("apn", 1)], unique=True),
            IndexModel([("address.state", 1), ("address.zip", 1)])
        ]
    },
    "phones": {
        "dedup_keys": ["number"],
        "record_type": "phone",
        "indexes": [
            IndexModel([("number", 1)], unique=True),
            IndexModel([("owner_apn", 1)])
        ]
    },
    "life_events": {
        "dedup_keys": ["apn", "event_type"],
        "record_type": "life_event",
        "indexes": [
            IndexModel([("apn", 1), ("event_date", -1)])
        ]
    },
    "upload_sessions": {
        "indexes": [
            IndexModel([("upload_id", 1)], unique=True),
            IndexModel([("timestamp", -1)])
        ]
    }
}

# === GLOBAL HELPERS ===
def clean_apn(apn: str) -> str:
    """Normalize APN to 10 digits with leading zeros"""
    return ''.join(filter(str.isdigit, str(apn))).zfill(10)[-10:]

def parse_array(value: Any) -> list:
    """Convert pipe-separated strings to lists"""
    if pd.isna(value) or value == "":
        return []
    return [v.strip() for v in str(value).split("|") if v.strip()]

def clean_phone(number: str) -> str:
    digits = re.sub(r"\D", "", str(number))
    if len(digits) == 10:
        return f"+1{digits}"
    elif len(digits) == 11 and digits.startswith("1"):
        return f"+{digits}"
    return ""

def validate_email(email: str) -> str:
    """Basic email validation"""
    if pd.isna(email) or "@" not in email:
        return ""
    return email.strip().lower()

def clean_field(value: Any, field_type: type) -> Any:
    """Type-safe field cleaning"""
    try:
        if pd.isna(value) or value in ["", "nan", "NaN"]:
            return field_type()
        
        if field_type == bool:
            return str(value).lower() in ["true", "1", "yes"]
        
        return field_type(value)
    except (ValueError, TypeError):
        return field_type()

def build_query(row: Dict[str, Any], keys: list) -> Dict[str, Any]:
    """Construct MongoDB query from dedup keys"""
    query = {}
    for key in keys:
        value = str(row.get(key, "")).strip()
        if not value:
            return None
        query[key] = value
    return query

# === COLLECTION-SPECIFIC PROCESSORS ===
def process_properties(row: Dict[str, Any]) -> Dict[str, Any]:
    """Updated property processor with WA state filter"""
    # Extract and clean state
    address_state = str(row.get("address.state", "")).strip().upper()[:2]
    if address_state != 'WA':
        return None  # Skip non-WA properties

    return {
        "apn": clean_apn(row.get("apn", "")),
        "address": {
            "street": str(row.get("address.street", "")).strip(),
            "city": str(row.get("address.city", "")).strip(),
            "state": address_state,
            "zip": str(row.get("address.zip", "")).strip()[:10]
        },
        "sale_info": {
            "price": float(clean_field(row.get("sale_info.price", 0), float)),
            "instrument": str(row.get("sale_info.instrument", "unknown")).strip(),
            "last_sold_date": pd.to_datetime(
                row.get("sale_info.last_sold_date", ""), 
                errors="coerce"
            ).to_pydatetime() if pd.notna(row.get("sale_info.last_sold_date")) else None
        },
        "upload_sources": parse_array(row.get("upload_sources", "")),
        "last_updated": datetime.now(timezone.utc)
    }

def process_owners(row: Dict[str, Any]) -> Dict[str, Any]:
    """Owner data processor with fallbacks"""
    return {
        "apn": clean_apn(row.get("apn", "")),
        "full_name": str(row.get("full_name", "")).strip(),
        "mailing_street": str(row.get("mailing_street", "")).strip(),
        "mailing_city": str(row.get("mailing_city", "")).strip(),
        "mailing_state": str(row.get("mailing_state", "")).strip().upper()[:2],
        "mailing_zip": str(row.get("mailing_zip", "")).strip()[:10],
        "phones": parse_array(row.get("phones", [])),  # Empty array allowed
        "upload_sources": parse_array(row.get("upload_sources", ["legacy"])),  # Default
        "last_updated": datetime.now(timezone.utc)
    }

# For phones
def process_phones(row: Dict[str, Any]) -> Dict[str, Any]:
    """Phone number processor with defaults and validation"""
    # Validate status
    status = str(row.get("status", "unverified")).lower()
    valid_statuses = {"valid", "invalid", "pending", "unverified"}
    if status not in valid_statuses:
        status = "unverified"

    # Validate boolean
    verified = row.get("verified", False)
    if not isinstance(verified, bool):
        verified = str(verified).lower() in ["true", "1", "yes"]

    return {
        "number": clean_phone(row.get("number", "")),
        "owner_apn": clean_apn(row.get("owner_apn", "")),
        "source": str(row.get("source", "manual")).strip(),
        "status": status,
        "verified": verified,
        "tags": parse_array(row.get("tags", [])),
        "last_updated": datetime.now(timezone.utc)
    }

def process_life_events(row: Dict[str, Any]) -> Dict[str, Any]:
    """Life event processor with null handling and validation"""
    event_date = row.get("event_date")
    try:
        # Handle all possible input types (str, float, None)
        event_date = pd.to_datetime(event_date, errors="coerce").to_pydatetime()
        if pd.isna(event_date):
            event_date = None
    except:
        event_date = None

    event_type = str(row.get("event_type", "")).strip().lower()
    if not event_type:
        raise ValueError("event_type cannot be empty")

    return {
        "apn": clean_apn(row.get("apn", "")),
        "event_type": event_type,
        "event_date": event_date,
        "description": str(row.get("description", "")).strip(),
        "documents": parse_array(row.get("documents", [])),
        "last_updated": datetime.now(timezone.utc)
    }

# === MAIN IMPORT FUNCTION ===
def import_data(collection_name: str, csv_file: str, uploaded_by: str, source: str):
    """Main data import handler"""
    if collection_name not in COLLECTION_CONFIG:
        raise ValueError(f"Unsupported collection: {collection_name}")

    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[collection_name]
    
    try:
        # Read and clean data
        df = pd.read_csv(csv_file, dtype=str, keep_default_na=False)
        processor = globals().get(f"process_{collection_name}")
        
        if not processor:
            raise ValueError(f"No processor for {collection_name}")

        # Process records
        valid_records = []
        for _, row in df.iterrows():
            try:
                processed = processor(row.to_dict())
                if processed:
                    valid_records.append(processed)
            except Exception as e:
                print(f"Error processing row: {e}")
                continue

        # Prepare bulk operations
        bulk_ops = []
        config = COLLECTION_CONFIG[collection_name]
        for record in valid_records:
            query = build_query(record, config["dedup_keys"])
            if not query:
                continue
                
            bulk_ops.append(UpdateOne(
                query,
                {"$set": record},
                upsert=True
            ))

        # Execute bulk write
        result = collection.bulk_write(bulk_ops, ordered=False)
        inserted = result.inserted_count
        updated = result.modified_count

        # Log upload session with corrected fields
        start_time = datetime.now(timezone.utc)
        session_doc = {
            "upload_id": f"US_{start_time.strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:6]}",
            "collection": collection_name,
            "source": source,
            "record_type": config.get("record_type", ""),
            "record_count": len(valid_records),
            "inserted": inserted,
            "updated": updated,
            "uploaded_by": uploaded_by,
            "status": "processed",
            "timestamp": datetime.now(timezone.utc),
            "start_time": start_time,
            "duration_sec": (datetime.now(timezone.utc) - start_time).total_seconds(),
            "file_name": csv_file.split("/")[-1]
        }
        db.upload_sessions.insert_one(session_doc)

        print(f"✅ {collection_name} import completed: {inserted} new, {updated} updated")

    except Exception as e:
        error_doc = {
            "error": str(e),
            "collection": collection_name,
            "timestamp": datetime.now(timezone.utc),
            "stack_trace": traceback.format_exc()
        }
        db.import_errors.insert_one(error_doc)
        print(f"❌ Critical error: {e}")
    finally:
        client.close()

# === CLI INTERFACE ===
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Real Estate Data Importer")
    parser.add_argument("--collection", required=True, 
                      choices=["owners", "properties", "phones", "life_events"],
                      help="Target collection")
    parser.add_argument("--file", required=True, help="CSV file path")
    parser.add_argument("--uploaded_by", required=True, help="User ID/email")
    parser.add_argument("--source", default="manual", 
                      help="Data source system")

    args = parser.parse_args()
    
    try:
        import_data(
            args.collection,
            args.file,
            args.uploaded_by,
            args.source
        )
    except Exception as e:
        print(f"🚨 Fatal error: {str(e)}")
        exit(1)