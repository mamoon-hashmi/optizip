# app.py — FINAL VERSION: LANDING PAGE FIRST + SMART REDIRECTS
from flask import Flask, render_template, request, redirect, url_for, session
from config import Config
from models import init_db
from auth.routes import auth_bp
from optimization.routes import opti_bp
from admin.routes import admin_bp
import os
import jwt
from flask_cors import CORS   # ← Is line ko add kar


app = Flask(__name__)
app.config['MONGO_URI'] = Config.MONGODB_URI
app.config['SECRET_KEY'] = Config.JWT_SECRET_KEY

CORS(app, supports_credentials=True)   # Cookie-based login bhi chalega, sab frontend se hit hoga


# MongoDB Connect
init_db(app)
print("MongoDB Connected Successfully!")

# Create required folders
os.makedirs('static/optimized', exist_ok=True)

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(opti_bp, url_prefix='/api')
app.register_blueprint(admin_bp)

# Helper: Token valid hai ya nahi?
def is_logged_in():
    token = request.cookies.get('access_token')
    if not token:
        return False
    try:
        jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
        return True
    except:
        return False

# ========================================
# ROUTES — SAB KUCH PERFECT AB!
# ========================================

# 1. ROOT → LANDING PAGE (Free Compression Wala)
@app.route('/')
def landing():
    return render_template('index.html')  # ← YE WOH VIRAL LANDING PAGE HAI!

# 2. LOGIN PAGE → Agar logged in hai to direct dashboard
@app.route('/login')
def login_page():
    if is_logged_in():
        return redirect('/dashboard')
    return render_template('login.html')

# 3. REGISTER PAGE (optional)
@app.route('/register')
def register_page():
    if is_logged_in():
        return redirect('/dashboard')
    return render_template('register.html')

# 4. OTP VERIFY PAGE
@app.route('/verify-otp')
def verify_otp_page():
    return render_template('verify_otp.html')

# 5. DASHBOARD → Sirf logged in users
@app.route('/dashboard')
def dashboard():
    if is_logged_in():
        return render_template('dashboard.html')
    else:
        return redirect('/login')

# 6. LOGOUT (optional — tu ne nahi banaya to bana dete hain)
@app.route('/logout')
def logout():
    response = redirect('/')
    response.set_cookie('access_token', '', expires=0)
    return response

# ========================================
# RUN APP
# ========================================
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5500)