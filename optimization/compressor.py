from PIL import Image, ImageOps
from io import BytesIO
import uuid

# ← YE SIRF ADD KIYA HAI (human readable size ke liye)
def format_bytes(bytes_size):
    if bytes_size < 1024:
        return f"{bytes_size} B"
    elif bytes_size < 1024 * 1024:
        return f"{bytes_size / 1024:.2f} KB"
    elif bytes_size < 1024 * 1024 * 1024:
        return f"{bytes_size / (1024 * 1024):.2f} MB"
    else:
        return f"{bytes_size / (1024 * 1024 * 1024):.2f} GB"

def optimize_image(file_storage):
    try:
        # YE SABSE ZAROORI HAI — file pointer reset + read as bytes
        file_storage.seek(0)
        raw_bytes = file_storage.read()

        # Agar file khali hai ya bohot chhoti hai → skip
        if not raw_bytes or len(raw_bytes) < 100:
            print(f"Invalid or too small file: {len(raw_bytes)} bytes")
            return None

        original_size = len(raw_bytes)

        # YE LINE FIX KI — BytesIO(raw_bytes) direct pass karo
        img = Image.open(BytesIO(raw_bytes))
        original_format = img.format or "JPEG"

        # Fix orientation
        img = ImageOps.exif_transpose(img)

        # Resize if huge
        if max(img.width, img.height) > 5000:
            img.thumbnail((5000, 5000), Image.Resampling.LANCZOS)

        buf = BytesIO()

        save_kwargs = {
            'format': 'WEBP',
            'quality': 84,
            'method': 6,
            'lossless': False
        }

        # PNG with alpha → lossless WebP
        if original_format == 'PNG' and img.mode in ('RGBA', 'LA', 'P'):
            save_kwargs['lossless'] = True
            save_kwargs.pop('quality', None)
            save_kwargs.pop('method', None)
        else:
            img = img.convert('RGB')

        img.save(buf, **save_kwargs)
        webp_data = buf.getvalue()
        buf.close()

        final_data = webp_data
        final_size = len(webp_data)
        ext = 'webp'

        # Rare fallback
        if final_size >= original_size * 0.95:
            buf = BytesIO()
            img.convert('RGB').save(buf, format='JPEG', quality=90, optimize=True)
            final_data = buf.getvalue()
            buf.close()
            final_size = len(final_data)
            ext = 'jpg'

        reduction = max(0.1, round(((original_size - final_size) / original_size) * 100, 2))
        filename = f"{uuid.uuid4().hex[:12]}_optizip.{ext}"

        # ← SIRF YE LINE BADLI HAI (human readable size dikhaane ke liye)
        print(f"COMPRESSED: {file_storage.filename} → {format_bytes(original_size)} → {format_bytes(final_size)} ({reduction}% saved)")

        return {
            'original_size': original_size,
            'optimized_size': final_size,
            'reduction_percent': reduction,
            'format': ext.upper(),
            'image_data': final_data,
            'filename': filename
        }

    except Exception as e:
        print(f"CRITICAL COMPRESSION ERROR: {e}")
        import traceback
        traceback.print_exc()
        # Safe fallback — original return kar do
        file_storage.seek(0)
        raw = file_storage.read()
        return {
            'original_size': len(raw),
            'optimized_size': len(raw),
            'reduction_percent': 0,
            'format': 'ORIGINAL',
            'image_data': raw,
            'filename': f"error_{uuid.uuid4().hex[:8]}.jpg"
        }