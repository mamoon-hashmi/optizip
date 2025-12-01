# models/users.py  ← TERA PURANA + NAYA ADMIN FUNCTIONS SAB SAATH MEIN!

from flask_pymongo import PyMongo
from datetime import datetime
import bcrypt
import random
from bson import ObjectId   # ← YE ADD KIYA HAI (admin ke liye zaroori)

mongo = None

def init_db(app):
    global mongo
    mongo = PyMongo(app)

class User:
    @staticmethod
    def get_collection():
        if mongo is None:
            raise Exception("MongoDB not initialized!")
        return mongo.db.users

    # ==================== PURANA CODE — BILKUL WAHI JAISA KI TU NE DIYA ====================
    @staticmethod
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
        return User.get_collection().insert_one(user_data).inserted_id

    @staticmethod
    def find_by_email(email):
        return User.get_collection().find_one({"email": email.lower()})

    @staticmethod
    def verify_otp(email, otp):
        user = User.find_by_email(email)
        if user and str(user.get("otp")) == str(otp):
            User.get_collection().update_one(
                {"email": email.lower()},
                {"$set": {"is_verified": True, "otp": None}}
            )
            return True
        return False

    @staticmethod
    def verify_password(stored_hash, password):
        if not stored_hash:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))

    # ==================== NAYA ADMIN FUNCTIONS — ADD KIYA HAI (Tera purana code bilkul safe) ====================

    @staticmethod
    def get_all_users():
        """Saare users laao (password hide kar do)"""
        return list(User.get_collection().find({}, {'password': 0}))

    @staticmethod
    def get_user_by_id(user_id):
        """ID se user dhoondo"""
        return User.get_collection().find_one({'_id': ObjectId(user_id)})

    @staticmethod
    def update_credits(user_id, new_credits):
        """Credits update kar do (admin ke liye)"""
        User.get_collection().update_one(
            {'_id': ObjectId(user_id)},
            {'$set': {'credits': int(new_credits)}}
        )

    @staticmethod
    def delete_user(user_id):
        """User ko hamesha ke liye delete kar do"""
        User.get_collection().delete_one({'_id': ObjectId(user_id)})

    @staticmethod
    def add_credits_by_email(email, credits_to_add):
        """Email se credits add kar do (payment ke baad use hoga)"""
        User.get_collection().update_one(
            {'email': email.lower()},
            {'$inc': {'credits': int(credits_to_add)}}
        )