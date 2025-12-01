# utils/jwt.py
import jwt
from datetime import datetime, timedelta, timezone
from config import Config

# utils/jwt.py — YE FUNCTION REPLACE KAR DE (email daal diya!)

# utils/jwt.py — YE FUNCTION REPLACE KAR DE (EMAIL DAALNA ZAROORI HAI!)

def create_tokens(user_id, email):
    access_token = jwt.encode(
        {
            'user_id': str(user_id),
            'email': email.lower(),                     # ← YE LINE ZAROORI HAI!
            'exp': datetime.now(timezone.utc) + timedelta(hours=24)  # 24 ghante tak chalega
        },
        Config.JWT_SECRET_KEY,
        algorithm='HS256'
    )
    refresh_token = jwt.encode(
        {
            'user_id': str(user_id),
            'exp': datetime.now(timezone.utc) + timedelta(days=30)
        },
        Config.JWT_REFRESH_SECRET_KEY,
        algorithm='HS256'
    )
    return access_token, refresh_token

def get_current_user(token):
    """Get user from JWT token"""
    try:
        payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
        return payload
    except:
        return None
    
    

# utils/jwt.py — YE FUNCTION ADD KAR DE (neeche wala)

def verify_token(token):
    """Sirf token valid hai ya nahi check karega — admin ke liye perfect!"""
    try:
        payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    except:
        return None