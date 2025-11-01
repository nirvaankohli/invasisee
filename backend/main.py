from flask import Flask, request, jsonify, make_response, render_template, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from pathlib import Path
import sys
from typing import Optional
from datetime import timedelta

sys.path.append(str(Path(__file__).resolve().parents[1]))
import auth as auth_module

app = Flask(__name__, 
            static_folder='static',
            template_folder='templates')

# Security configuration
app.secret_key = auth_module.SECRET_KEY or 'dev-secret-key-change-in-production'
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)
app.config['SESSION_COOKIE_NAME'] = 'invasee_session'

# Flask-Login configuration
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = 'strong'


class User(UserMixin):
    """User class for Flask-Login"""
    def __init__(self, user_data):
        self.id = str(user_data['id'])
        self.username = user_data['username']
        self.created_at = user_data['created_at']


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login"""
    # Query user by ID from database
    import sqlite3
    conn = sqlite3.connect(auth_module._db_path())
    cur = conn.cursor()
    cur.execute("SELECT id, username, password, created_at FROM users WHERE id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    
    if not row:
        return None
    
    user_data = {
        "id": row[0],
        "username": row[1],
        "password": row[2],
        "created_at": row[3]
    }
    return User(user_data)


@app.before_request
def init_db_once():
    """Initialize database before first request"""
    auth_module.init_db()


@app.route("/")
def index():
    """Serve the main HTML page with authentication context"""
    user_data = None
    if current_user.is_authenticated:
        user_data = {
            'username': current_user.username,
            'is_authenticated': True
        }
    return render_template('index.html', user=user_data)


@app.route("/api/register", methods=["POST"])
def register():
    """Register a new user"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"detail": "Username and password required"}), 400
    
    try:
        auth_module.create_user(username, password)
    except ValueError:
        return jsonify({"detail": "user already exists"}), 400
    
    return jsonify({"msg": "user created"}), 200


@app.route("/api/login", methods=["POST"])
def api_login():
    """Login a user and create a secure session"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"detail": "Username and password required"}), 400
    
    user_data = auth_module.get_user(username)
    if not user_data or not auth_module.verify_password(password, user_data["password"]):
        return jsonify({"detail": "Incorrect username or password"}), 401
    
    # Create User object and login with Flask-Login
    user = User(user_data)
    login_user(user, remember=True)
    session.permanent = True
    
    # Store additional secure session data
    session['username'] = user.username
    session['user_id'] = user.id
    session['is_authenticated'] = True
    
    return jsonify({
        "msg": "logged in successfully",
        "username": user.username,
        "is_authenticated": True
    }), 200


@app.route("/api/me", methods=["GET"])
@login_required
def read_me():
    """Get current user information from secure session"""
    return jsonify({
        "username": current_user.username,
        "created_at": current_user.created_at,
        "is_authenticated": True
    }), 200


@app.route("/api/logout", methods=["POST"])
@login_required
def api_logout():
    """Logout user by clearing secure session"""
    logout_user()
    session.clear()
    
    response = make_response(jsonify({"msg": "logged out successfully"}))
    # Explicitly delete all session cookies
    response.set_cookie('invasee_session', '', expires=0)
    response.set_cookie('remember_token', '', expires=0)
    response.set_cookie('session', '', expires=0)
    
    return response, 200


@login_manager.unauthorized_handler
def unauthorized():
    """Handle unauthorized access"""
    return jsonify({"detail": "Authentication required"}), 401


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

