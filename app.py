from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_session import Session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import bcrypt
import sqlite3
import os
import time
import json
from dotenv import load_dotenv
load_dotenv()



app = Flask(__name__, template_folder='templates')

# Secret key
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))

# Session configuration
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False
Session(app)

# Rate limiter
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

def get_db():
    conn = sqlite3.connect('hotel.db', timeout=10)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        try:
            user = db.execute(
                'SELECT * FROM users WHERE username = ?',
                (username,)
            ).fetchone()

            if not user:
                flash('Invalid username or password.', 'error')
                return render_template('login.html')

            if user['locked_until'] and time.time() < user['locked_until']:
                minutes_left = int((user['locked_until'] - time.time()) / 60) + 1
                flash(f'Account locked. Try again in {minutes_left} minute(s).', 'error')
                return render_template('login.html')

            if bcrypt.checkpw(password.encode('utf-8'), user['password']):
                db.execute(
                    'UPDATE users SET failed_attempts = 0, locked_until = NULL WHERE id = ?',
                    (user['id'],)
                )
                db.commit()
                session['user_id'] = user['id']
                session['username'] = user['username']
                return redirect(url_for('dashboard'))
            else:
                failed_attempts = user['failed_attempts'] + 1
                if failed_attempts >= 5:
                    locked_until = time.time() + (15 * 60)
                    db.execute(
                        'UPDATE users SET failed_attempts = ?, locked_until = ? WHERE id = ?',
                        (failed_attempts, locked_until, user['id'])
                    )
                    db.commit()
                    flash('Too many failed attempts. Account locked for 15 minutes.', 'error')
                else:
                    db.execute(
                        'UPDATE users SET failed_attempts = ? WHERE id = ?',
                        (failed_attempts, user['id'])
                    )
                    db.commit()
                    attempts_left = 5 - failed_attempts
                    flash(f'Invalid password. {attempts_left} attempt(s) remaining.', 'error')
        finally:
            db.close()
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        db = get_db()
        try:
            db.execute(
                'INSERT INTO users (username, password) VALUES (?, ?)',
                (username, hashed)
            )
            db.commit()
            flash('Registration successful — please log in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists.', 'error')
        finally:
            db.close()
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

# ⚠️ VULNERABLE endpoint — no authorization check
@app.route('/api/receipts/<int:receipt_id>')
def get_receipt_vulnerable(receipt_id):
    if 'user_id' not in session:
        return json.dumps({'error': 'Not authenticated'}), 401
    db = get_db()
    try:
        booking = db.execute(
            'SELECT * FROM bookings WHERE id = ?',
            (receipt_id,)
        ).fetchone()
        if not booking:
            return json.dumps({'error': 'Receipt not found'}), 404
        return json.dumps({
            'id': booking['id'],
            'user_id': booking['user_id'],
            'room': booking['room'],
            'check_in': booking['check_in'],
            'check_out': booking['check_out'],
            'total': booking['total']
        })
    finally:
        db.close()

# ✅ SECURE endpoint — checks ownership
@app.route('/api/receipts/<int:receipt_id>/secure')
def get_receipt_secure(receipt_id):
    if 'user_id' not in session:
        return json.dumps({'error': 'Not authenticated'}), 401
    db = get_db()
    try:
        booking = db.execute(
            'SELECT * FROM bookings WHERE id = ?',
            (receipt_id,)
        ).fetchone()
        if not booking:
            return json.dumps({'error': 'Receipt not found'}), 404
        if booking['user_id'] != session['user_id']:
            return json.dumps({'error': 'Unauthorized'}), 403
        return json.dumps({
            'id': booking['id'],
            'user_id': booking['user_id'],
            'room': booking['room'],
            'check_in': booking['check_in'],
            'check_out': booking['check_out'],
            'total': booking['total']
        })
    finally:
        db.close()

if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'False') == 'True'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)