# admin/routes.py — YE PURA CODE DAAL DE (100% WORKING)

from flask import Blueprint, render_template, request, redirect, flash
from models.user import User
from utils.jwt import verify_token  # ← AB YE FUNCTION HAI!
from config import Config

admin_bp = Blueprint('admin', __name__, url_prefix='/admin-mamoon-only')

# ← APNA EMAIL YAHAN DAAL DE
ADMIN_EMAIL = "mamoon.aiwork@gmail.com"  # ← YAHAN APNA EMAIL DAAL DE BHAI!

def admin_required(f):
    def wrapper(*args, **kwargs):
        # Cookie se token le
        token = request.cookies.get('access_token')
        
        # DEBUG LINE — Terminal mein dikhega kya aa raha hai
        print(f"ADMIN CHECK → Token mila? {'YES' if token else 'NO'}")
        if token:
            print(f"ADMIN CHECK → Token shuru ke 50 char: {token[:50]}...")
        else:
            print("ADMIN CHECK → Token bilkul nahi mila!")

        # Agar token nahi hai → login pe bhej do
        if not token:
            return redirect('/login')

        # Token verify karo
        from utils.jwt import verify_token
        payload = verify_token(token)

        if not payload:
            print("ADMIN CHECK → Token invalid ya expired!")
            return redirect('/login')

        # Email check karo
        user_email = payload.get('email')
        print(f"ADMIN CHECK → User email: {user_email}")
        print(f"ADMIN CHECK → Required admin email: {ADMIN_EMAIL}")

        if not user_email or user_email.lower() != ADMIN_EMAIL.lower():
            return '''
            <div style="font-family: system-ui, sans-serif; text-align:center; padding:100px; background:#0f0f0f; color:white; min-height:100vh;">
                <h1 style="font-size:70px; color:#ff4444; margin:0;">ACCESS DENIED!</h1>
                <h2 style="font-size:40px; color:#ff6666;">Sirf Mamoon Bhai Allowed Hai</h2>
                <p style="font-size:24px; margin:30px 0;">Tu kaun hai bhai?</p>
                <a href="/dashboard" style="color:#00ff00; font-size:20px; text-decoration:underline;">← Dashboard Pe Wapas Ja</a>
            </div>
            ''', 403

        # SAB KUCH SAHI → ADMIN KO ANDAR JAANE DO!
        print("ADMIN CHECK → SAB KUCH SAHI! Mamoon bhai aa gaye!")
        return f(*args, **kwargs)

    wrapper.__name__ = f.__name__
    return wrapper

@admin_bp.route('/')
@admin_required
def admin_dashboard():
    users = User.get_all_users()
    return render_template('admin_dashboard.html', users=users)

@admin_bp.route('/update-credits/<user_id>', methods=['POST'])
@admin_required
def update_credits(user_id):
    try:
        new_credits = int(request.form['credits'])
        if new_credits < 0:
            new_credits = 0
        User.update_credits(user_id, new_credits)
    except:
        pass
    return redirect('/admin-mamoon-only')

@admin_bp.route('/delete/<user_id>')
@admin_required
def delete_user(user_id):
    user = User.get_user_by_id(user_id)
    if user:
        User.delete_user(user_id)
    return redirect('/admin-mamoon-only')