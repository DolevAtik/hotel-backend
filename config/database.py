import os

from pymongo import MongoClient

# Module-level handles so the database can be reused across requests.
_client = None
_db = None


def init_db(app=None):
    """Create the MongoDB client and store a reference to the database."""
    global _client, _db

    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    db_name = os.getenv("MONGO_DB_NAME", "hotel")

    _client = MongoClient(mongo_uri)
    _db = _client[db_name]

    if app is not None:
        app.config["MONGO_DB"] = _db

    return _db


def get_db():
    """Return the active database, initializing it on first use."""
    global _db
    if _db is None:
        init_db()
    return _db


def get_collection(name):
    """Convenience accessor for a single collection."""
    return get_db()[name]
