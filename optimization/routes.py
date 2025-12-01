# optimization/routes.py — COMPLETE & FINAL
from flask import Blueprint, request, jsonify, send_file, current_app
from models import find_by_email, get_collection
from optimization.compressor import optimize_image
import jwt
from config import Config
import os
import base64

opti_bp = Blueprint('opti', __name__)

# Yeh folder path global bana dete hain — import time safe hai
OPTIMIZED_DIR = os.path.join(os.path.dirname(__file__), '..', 'static', 'optimized')
os.makedirs(OPTIMIZED_DIR, exist_ok=True)

@opti_bp.route('/upload', methods=['POST'])
def upload_images():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not token:
        return jsonify({"msg": "Login required"}), 401

    try:
        payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
        user = find_by_email(payload['email'])
        if not user or user.get('credits', 0) <= 0:
            return jsonify({"msg": "No credits left!"}), 402

        files = request.files.getlist('images')
        if not files or len(files) > 10:
            return jsonify({"msg": "Select 1-10 images"}), 400

        results = []
        for file in files:
            if file.filename == '':
                continue

            result = optimize_image(file)
            if result:
                # Save file
                filename = result['filename']
                filepath = os.path.join(OPTIMIZED_DIR, filename)
                with open(filepath, 'wb') as f:
                    f.write(result['image_data'])

                # Add preview (base64)
                result['preview'] = f"data:image/webp;base64,{base64.b64encode(result['image_data']).decode()}"

                results.append(result)

        # Deduct credits
        if results:
            get_collection().update_one(
                {"email": payload['email']},
                {"$inc": {"credits": -len(results)}}
            )

        return jsonify({
            "msg": f"{len(results)} images optimized!",
            "results": results,
            "credits_used": len(results)
        }), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"msg": "Session expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"msg": "Invalid token"}), 401
    except Exception as e:
        print("Error:", e)
        return jsonify({"msg": "Server error"}), 500


@opti_bp.route('/user')
def get_user_credits():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    try:
        payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
        user = find_by_email(payload['email'])
        return jsonify({"credits": user.get('credits', 0)}), 200
    except:
        return jsonify({"msg": "Invalid token"}), 401
    
    




@opti_bp.route('/download/<filename>')
def download_single(filename):
    filepath = os.path.join(OPTIMIZED_DIR, filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True, download_name=filename)
    return "File not found", 404


# ADD YE ROUTE — WORDPRESS PLUGIN KE LIYE FREE UPLOAD (NO LOGIN, NO CREDIT DEDUCT)
@opti_bp.route('/upload-free', methods=['POST'])
def upload_free():
    print("\nAPI HIT FROM WORDPRESS PLUGIN! (FREE ROUTE)")
    
    if 'images' not in request.files:
        return jsonify({"msg": "No images found"}), 400

    files = request.files.getlist('images')
    if not files or len(files) == 0:
        return jsonify({"msg": "No valid images"}), 400
    if len(files) > 10:
        return jsonify({"msg": "Max 10 images allowed"}), 400

    results = []
    for file in files:
        if file.filename == '':
            continue

        print(f"Processing: {file.filename} ({file.content_length} bytes)")

        try:
            # Same compressor use karo
            result = optimize_image(file)
            if result:
                # Base64 preview (landing page ke liye)
                result['preview'] = f"data:image/webp;base64,{base64.b64encode(result['image_data']).decode()}"
                results.append(result)
        except Exception as e:
            print("Error compressing:", file.filename, e)
            continue

    print(f"Compressed {len(results)} images successfully!\n")
    return jsonify({
        "msg": "Compressed successfully!",
        "results": results
    }), 200

# ADD YE ROUTE — WORDPRESS PLUGIN KE LIYE FREE UPLOAD (NO LOGIN, NO CREDIT DEDUCT)
@opti_bp.route('/wordpress_plugin', methods=['POST'])
def wordpress_plugin():
    print("\nAPI HIT FROM WORDPRESS PLUGIN! (FREE ROUTE)")
    print("Files received:", list(request.files.keys()))        # ← YE LINE ADD KAR DO
    print("Form data:", request.form.to_dict())

    if 'images' not in request.files:
        print("No 'images' field found!")
        return jsonify({"msg": "No images field"}), 400

    files = request.files.getlist('images')
    print(f"Total files received: {len(files)}")

    results = []
    for file in files:
        if not file or file.filename == '':
            continue
            
        file.seek(0)
        file_size = len(file.read())
        file.seek(0)  # Reset again
        print(f"Processing: {file.filename} → {file_size} bytes")   # ← YE DIKHEGA AB!

        result = optimize_image(file)
        if result:
            results.append(result)

    print(f"Total compressed: {len(results)}\n")
    return jsonify({"results": results, "msg": "Done"}), 200