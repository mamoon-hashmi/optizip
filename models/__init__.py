# models/__init__.py
from flask_pymongo import PyMongo
from datetime import datetime
import bcrypt
import random

mongo = None

def init_db(app):
    global mongo
    mongo = PyMongo(app)

def get_collection():
    if mongo is None:
        raise Exception("MongoDB not initialized!")
    return mongo.db.users

# All User functions yahan hi rakh rahe hain taaki import simple rahe
def create_user(name, email, password=None, google_id=None):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()) if password else None
    user_data = {
        "name": name,
        "email": email.lower(),
        "password": hashed.decode('utf-8') if hashed else None,
        "google_id": google_id,
        "is_verified": True if google_id else False,
        "otp": str(random.randint(100000, 999999)) if not google_id else None,
        "credits": 100,
        "created_at": datetime.utcnow()
    }
    return get_collection().insert_one(user_data).inserted_id

def find_by_email(email):
    return get_collection().find_one({"email": email.lower()})

def verify_otp(email, otp):
    user = find_by_email(email)
    if user and str(user.get("otp")) == str(otp):
        get_collection().update_one({"email": email.lower()}, {"$set": {"is_verified": True, "otp": None}})
        return True
    return False

def verify_password(stored_hash, password):
    if not stored_hash:
        return False
    return bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))