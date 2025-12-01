# auth/routes.py — AB TOKEN COOKIE MEIN BHI SAVE HOGA → LOGIN SKIP HO JAYEGA!
from flask import Blueprint, request, redirect, render_template, make_response, jsonify
import requests
from config import Config
from utils.mail import send_otp_email
from utils.jwt import create_tokens
from models import create_user, find_by_email, verify_otp, verify_password

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    if find_by_email(data.get('email')):
        return {"msg": "Email already exists"}, 400
    create_user(data.get('name'), data.get('email'), data.get('password'))
    user = find_by_email(data.get('email'))
    send_otp_email(data.get('email'), user['otp'])
    return {"msg": "OTP sent to your email"}, 200

@auth_bp.route('/verify-otp', methods=['POST'])
def verify_otp_route():
    data = request.json
    if verify_otp(data.get('email'), data.get('otp')):
        return {"msg": "Email verified successfully"}, 200
    return {"msg": "Invalid OTP"}, 400

# YE WALA LOGIN — AB COOKIE MEIN BHI TOKEN DAALEGA!
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = find_by_email(data.get('email'))
    if not user or not user.get('password'):
        return {"msg": "Invalid credentials"}, 401
    if not user['is_verified']:
        return {"msg": "Please verify email first"}, 401
    if verify_password(user['password'], data.get('password')):
        access, refresh = create_tokens(str(user['_id']), data.get('email'))

        # YE 2 LINE ADD KI HAIN → COOKIE MEIN TOKEN SAVE!
        resp = make_response(jsonify({
            "msg": "Login successful",
            "access_token": access,
            "refresh_token": refresh,
            "name": user['name']
        }), 200)
        resp.set_cookie('access_token', access, httponly=False, samesite='Lax', max_age=60*60*24*7)  # 7 din
        return resp

    return {"msg": "Wrong password"}, 401

# Google Login bhi cookie mein token daal de
@auth_bp.route('/google')
def google_login():
    google_auth_url = f"https://accounts.google.com/o/oauth2/auth?client_id={Config.GOOGLE_CLIENT_ID}&redirect_uri={Config.GOOGLE_REDIRECT_URI}&response_type=code&scope=openid%20email%20profile"
    return redirect(google_auth_url)

@auth_bp.route('/google/callback')
def google_callback():
    code = request.args.get('code')
    if not code:
        return "No code received", 400

    # Google se token le
    token_res = requests.post("https://oauth2.googleapis.com/token", data={
        'code': code,
        'client_id': Config.GOOGLE_CLIENT_ID,
        'client_secret': Config.GOOGLE_CLIENT_SECRET,
        'redirect_uri': Config.GOOGLE_REDIRECT_URI,
        'grant_type': 'authorization_code'
    }).json()

    access_token = token_res.get('access_token')
    if not access_token:
        return "Google auth failed", 400

    user_info = requests.get("https://www.googleapis.com/oauth2/v1/userinfo",
                            headers={"Authorization": f"Bearer {access_token}"}).json()

    email = user_info.get('email')
    name = user_info.get('name', 'User')
    google_id = user_info.get('id')

    if not email:
        return "Email not received from Google", 400

    # YE LINE ADD KI HAI — MONGODB INIT KAR DO!
    from app import app  # app.py se app object le
    from models.user import init_db
    init_db(app)  # ← YE ZAROORI HAI!

    from models.user import User  # ab import safe hai

    user = User.find_by_email(email)
    if not user:
        User.create_user(name, email, google_id=google_id)

    from utils.jwt import create_tokens
    access, refresh = create_tokens(google_id or email, email)

    # Cookie set karo
    resp = make_response(redirect('/dashboard'))
    resp.set_cookie(
        'access_token', access,
        max_age=60*60*24*7,
        path='/',
        secure=False,
        httponly=False,
        samesite='Lax'
    )
    return resp