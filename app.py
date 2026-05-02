import os
import re
import sqlite3
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from werkzeug.security import generate_password_hash, check_password_hash
import pyotp
import qrcode
import jwt
import datetime
import io
import base64
from database import get_db_connection
from middleware import token_required, role_required, SECRET_KEY

app = Flask(__name__)

# ==========================================
# 1. مسارات صفحات الويب (Frontend HTML Pages)
# ==========================================
@app.route('/')
def home(): return render_template('auth.html')

@app.route('/verify-page')
def verify_page(): return render_template('2fa.html')

@app.route('/dashboard-page')
def dashboard_page(): return render_template('dashboard.html')

@app.route('/profile-page')
def profile_page(): return render_template('profile.html')

@app.route('/admin-page')
def admin_page(): return render_template('admin.html')

@app.route('/manager-page')
def manager_page(): return render_template('manager.html')

@app.route('/user-page')
def user_page(): return render_template('user.html')

# ==========================================
# 2. مسارات المصادقة (Auth APIs)
# ==========================================
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    # Input Validation
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify({'message': 'Invalid email format!'}), 400
    if len(password) < 8:
        return jsonify({'message': 'Password must be at least 8 characters!'}), 400
    if role not in ['Admin', 'Manager', 'User']:
        return jsonify({'message': 'Invalid role!'}), 400

    hashed_password = generate_password_hash(password)
    two_factor_secret = pyotp.random_base32()

    try:
        conn = get_db_connection()
        conn.execute('INSERT INTO users (name, email, password, role, two_factor_secret) VALUES (?, ?, ?, ?, ?)',
                     (name, email, hashed_password, role, two_factor_secret))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'message': 'Email already exists!'}), 400
    except Exception:
        conn.close()
        return jsonify({'message': 'Internal Server Error'}), 500
    finally:
        conn.close()

    totp = pyotp.TOTP(two_factor_secret)
    provisioning_uri = totp.provisioning_uri(name=email, issuer_name="SecureAuthApp")
    
    img = qrcode.make(provisioning_uri)
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    qr_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return jsonify({
        'qr_code_base64': qr_base64,
        'secret_key': two_factor_secret
    }), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    conn.close()

    if not user or not check_password_hash(user['password'], password):
        return jsonify({'message': 'Invalid credentials!'}), 401

    return jsonify({'email': email}), 200

@app.route('/api/verify-2fa', methods=['POST'])
def verify_2fa():
    data = request.get_json()
    email = data.get('email')
    totp_code = data.get('code')

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    conn.close()

    if not user:
        return jsonify({'message': 'User not found!'}), 404

    totp = pyotp.TOTP(user['two_factor_secret'])
    if not totp.verify(totp_code):
        return jsonify({'message': 'Invalid 2FA code!'}), 401

    token = jwt.encode({
        'user_id': user['id'],
        'role': user['role'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, SECRET_KEY, algorithm="HS256")

    return jsonify({'token': token}), 200

# ==========================================
# 3. المسارات المحمية (Protected APIs)
# ==========================================
@app.route('/api/profile', methods=['GET'])
@token_required
def profile_api(current_user):
    conn = get_db_connection()
    user = conn.execute('SELECT id, name, email, role FROM users WHERE id = ?', (current_user['user_id'],)).fetchone()
    conn.close()
    if not user: return jsonify({'message': 'User not found'}), 404
    return jsonify(dict(user))

@app.route('/api/admin', methods=['GET'])
@token_required
@role_required('Admin')
def admin_data(current_user): return jsonify({'data': 'This is top secret Admin data!'})

@app.route('/api/manager', methods=['GET'])
@token_required
@role_required('Manager')
def manager_data(current_user): return jsonify({'data': 'This is confidential Manager reports.'})

@app.route('/api/user', methods=['GET'])
@token_required
@role_required('User')
def user_data(current_user): return jsonify({'data': 'This is your personal User section.'})

if __name__ == '__main__':
    app.run(debug=True)