from flask import Flask, request, jsonify, make_response, render_template, session, send_from_directory, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from pathlib import Path
import sys
from typing import Optional
from datetime import timedelta
import json
import os
import base64
import re
import sqlite3
from datetime import datetime
from werkzeug.utils import secure_filename

# Load environment variables from .env if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

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
app.config['SESSION_COOKIE_NAME'] = 'Invasisee_session'
app.config['UPLOAD_FOLDER'] = str(Path(__file__).resolve().parent / 'uploads')
Path(app.config['UPLOAD_FOLDER']).mkdir(parents=True, exist_ok=True)

# XP system configuration
XP_THRESHOLDS = [0, 50, 150, 300, 500]  # Levels 1..5
MAX_LEVEL = 5
XP_PER_INVASIVE = 50  # Award per correct (invasive) report

# Cosmetics catalog (id, label, cost)
COSMETICS_STORE = [
    {"id": "pot_terracotta", "label": "Terracotta Pot", "cost": 50},
    {"id": "pot_white", "label": "White Pot", "cost": 100},
    {"id": "leaves_spring", "label": "Spring Leaves", "cost": 75},
    {"id": "leaves_autumn", "label": "Autumn Leaves", "cost": 125},
]

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
    # Ensure reports table exists
    conn = sqlite3.connect(auth_module._db_path())
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            username TEXT,
            species TEXT,
            invasive INTEGER,
            summary TEXT,
            lat REAL,
            lng REAL,
            image_filename TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    # Ensure user XP columns exist
    try:
        cur.execute("PRAGMA table_info(users)")
        cols = {row[1] for row in cur.fetchall()}
        add_cols = []
        if 'xp_total' not in cols:
            add_cols.append("ALTER TABLE users ADD COLUMN xp_total INTEGER DEFAULT 0")
        if 'xp_balance' not in cols:
            add_cols.append("ALTER TABLE users ADD COLUMN xp_balance INTEGER DEFAULT 0")
        if 'level' not in cols:
            add_cols.append("ALTER TABLE users ADD COLUMN level INTEGER DEFAULT 1")
        if 'unlocked_cosmetics' not in cols:
            add_cols.append("ALTER TABLE users ADD COLUMN unlocked_cosmetics TEXT DEFAULT '[]'")
        if 'active_cosmetic' not in cols:
            add_cols.append("ALTER TABLE users ADD COLUMN active_cosmetic TEXT")
        for stmt in add_cols:
            try:
                cur.execute(stmt)
            except Exception:
                pass
        conn.commit()
    finally:
        conn.close()


def compute_level(xp_total: int) -> int:
    lvl = 1
    for i, thr in enumerate(XP_THRESHOLDS, start=1):
        if xp_total >= thr:
            lvl = i
    return min(lvl, MAX_LEVEL)


def get_user_profile(user_id: str) -> dict:
    conn = sqlite3.connect(auth_module._db_path())
    cur = conn.cursor()
    cur.execute("SELECT username, xp_total, xp_balance, level, unlocked_cosmetics, active_cosmetic FROM users WHERE id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return {}
    username, xp_total, xp_balance, level, unlocked_json, active = row
    try:
        unlocked = json.loads(unlocked_json or '[]')
    except Exception:
        unlocked = []
    next_level_idx = min(level, len(XP_THRESHOLDS)-1)
    next_threshold = XP_THRESHOLDS[next_level_idx]
    prev_threshold = XP_THRESHOLDS[max(0, next_level_idx-1)] if level > 1 else 0
    return {
        "username": username,
        "xp_total": xp_total or 0,
        "xp_balance": xp_balance or 0,
        "level": level or 1,
        "unlocked_cosmetics": unlocked,
        "active_cosmetic": active,
        "next_threshold": next_threshold,
        "prev_threshold": prev_threshold,
        "max_level": MAX_LEVEL,
        "store": COSMETICS_STORE,
    }


def award_xp(user_id: str, amount: int) -> None:
    if not user_id:
        return
    conn = sqlite3.connect(auth_module._db_path())
    cur = conn.cursor()
    cur.execute("SELECT xp_total, xp_balance FROM users WHERE id = ?", (user_id,))
    row = cur.fetchone()
    xp_total = (row[0] if row else 0) + (amount or 0)
    xp_balance = (row[1] if row else 0) + (amount or 0)
    level = compute_level(xp_total)
    cur.execute("UPDATE users SET xp_total = ?, xp_balance = ?, level = ? WHERE id = ?", (xp_total, xp_balance, level, user_id))
    conn.commit()
    conn.close()


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


@app.route("/auth")
def auth():
    """Serve a dedicated authentication page; redirect if already logged in"""
    if current_user.is_authenticated:
        # Already logged in, send to app
        return render_template('app.html', user={
            'username': current_user.username,
            'is_authenticated': True
        })
    return render_template('auth.html', user=None)


@app.route("/app")
@login_required
def app_page():
    """Basic app landing after login"""
    return render_template('app.html', user={
        'username': current_user.username,
        'is_authenticated': True
    })


@app.route("/capture")
@login_required
def capture_page():
    """Camera capture page"""
    return render_template('capture.html')


@app.route("/api/report", methods=["POST"])
@login_required
def api_report():
    """Accept an image upload and forward to OpenAI for analysis (if configured)."""
    if 'image' not in request.files:
        return jsonify({"detail": "No image provided"}), 400
    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({"detail": "Empty filename"}), 400

    # Read file bytes
    content = image_file.read()
    if not content:
        return jsonify({"detail": "Empty file"}), 400

    # Optionally store temporarily (disabled by default)
    # upload_dir = Path('uploads'); upload_dir.mkdir(exist_ok=True)
    # temp_path = upload_dir / image_file.filename
    # temp_path.write_bytes(content)

    # Optional location
    lat = request.form.get('lat')
    lng = request.form.get('lng')
    try:
        lat_val = float(lat) if lat is not None else None
        lng_val = float(lng) if lng is not None else None
    except ValueError:
        lat_val, lng_val = None, None

    openai_api_key = os.getenv('OPENAI_API_KEY')
    if not openai_api_key:
        # Return stubbed response if OpenAI is not configured
        return jsonify({
            "msg": "received",
            "openai": "skipped (no OPENAI_API_KEY)",
            "bytes": len(content)
        }), 200

    # Attempt to send to OpenAI vision model
    b64 = base64.b64encode(content).decode('utf-8')
    data_url = f"data:image/jpeg;base64,{b64}"
    prompt_system = (
        "You identify species in images. Respond ONLY with strict JSON: "
        "{\"species\": string, \"invasive\": boolean, \"summary\": string}. "
        "If unsure, set species='Unknown' and invasive=false, and explain uncertainty in summary."
    )
    loc_text = f" The photo was taken near coordinates ({lat_val}, {lng_val})." if (lat_val is not None and lng_val is not None) else ""
    prompt_user = "Identify the species and whether it is invasive. Provide a summary under 500 chars including distinctive features, typical habitats, your reasonings for your description, and any potential risks." + loc_text

    def extract_json(text: str):
        if not text:
            return None
        try:
            return json.loads(text)
        except Exception:
            pass
        m = re.search(r"\{[\s\S]*\}", text)
        if m:
            try:
                return json.loads(m.group(0))
            except Exception:
                return None
        return None

    # Try new OpenAI SDK first (>=1.0)
    try:
        from openai import OpenAI  # type: ignore
        client = OpenAI(api_key=openai_api_key)
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": prompt_system},
                {"role": "user", "content": [
                    {"type": "text", "text": prompt_user},
                    {"type": "image_url", "image_url": {"url": data_url}}
                ]}
            ],
            temperature=0.2,
            max_tokens=600,
            response_format={"type": "json_object"}
        )
        content_text = resp.choices[0].message.content if resp and resp.choices else None
        parsed = extract_json(content_text)
        result = parsed or {"species": "Unknown", "invasive": False, "summary": content_text or "No analysis returned"}
        # Persist if invasive
        saved = None
        try:
            if isinstance(result, dict) and result.get('invasive'):
                ts = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
                base_name = secure_filename(image_file.filename) or 'upload.jpg'
                fname = f"{ts}_{base_name}"
                out_path = Path(app.config['UPLOAD_FOLDER']) / fname
                with open(out_path, 'wb') as f:
                    f.write(content)
                conn = sqlite3.connect(auth_module._db_path())
                cur = conn.cursor()
                cur.execute(
                    """
                    INSERT INTO reports (user_id, username, species, invasive, summary, lat, lng, image_filename, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        getattr(current_user, 'id', None),
                        getattr(current_user, 'username', None),
                        result.get('species') or 'Unknown',
                        1,
                        result.get('summary') or '',
                        lat_val,
                        lng_val,
                        fname,
                        datetime.utcnow().isoformat()
                    )
                )
                conn.commit()
                saved = cur.lastrowid
                conn.close()
                # Award XP for correct invasive report
                try:
                    award_xp(getattr(current_user, 'id', None), XP_PER_INVASIVE)
                except Exception:
                    pass
        except Exception:
            saved = None
        return jsonify({"msg": "received", "result": result, "saved_report_id": saved}), 200
    except Exception:
        # Fall back to legacy SDK if available
        try:
            import importlib
            openai = importlib.import_module('openai')
            openai.api_key = openai_api_key
            resp = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": prompt_system},
                    {"role": "user", "content": [
                        {"type": "text", "text": prompt_user},
                        {"type": "image_url", "image_url": {"url": data_url}}
                    ]}
                ],
                temperature=0.2,
                max_tokens=600
            )
            content_text = resp.choices[0].message.get('content') if resp and getattr(resp, 'choices', None) else None
            parsed = extract_json(content_text) if isinstance(content_text, str) else None
            result = parsed or {"species": "Unknown", "invasive": False, "summary": content_text or "No analysis returned"}
            saved = None
            try:
                if isinstance(result, dict) and result.get('invasive'):
                    ts = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
                    base_name = secure_filename(image_file.filename) or 'upload.jpg'
                    fname = f"{ts}_{base_name}"
                    out_path = Path(app.config['UPLOAD_FOLDER']) / fname
                    with open(out_path, 'wb') as f:
                        f.write(content)
                    conn = sqlite3.connect(auth_module._db_path())
                    cur = conn.cursor()
                    cur.execute(
                        """
                        INSERT INTO reports (user_id, username, species, invasive, summary, lat, lng, image_filename, created_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            getattr(current_user, 'id', None),
                            getattr(current_user, 'username', None),
                            result.get('species') or 'Unknown',
                            1,
                            result.get('summary') or '',
                            lat_val,
                            lng_val,
                            fname,
                            datetime.utcnow().isoformat()
                        )
                    )
                    conn.commit()
                    saved = cur.lastrowid
                    conn.close()
                    try:
                        award_xp(getattr(current_user, 'id', None), XP_PER_INVASIVE)
                    except Exception:
                        pass
            except Exception:
                saved = None
            return jsonify({"msg": "received", "result": result, "saved_report_id": saved}), 200
        except Exception as e:
            return jsonify({"msg": "received", "openai_error": str(e)}), 200

    # If we reached here, we already returned JSON above. The code below is just to satisfy type checkers.



@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route("/api/reports", methods=["GET"])
def get_reports():
    """Return invasive reports for map consumption (public feed)."""
    conn = sqlite3.connect(auth_module._db_path())
    cur = conn.cursor()
    cur.execute("SELECT id, species, invasive, summary, lat, lng, image_filename, created_at, username FROM reports WHERE invasive = 1 ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    items = []
    for r in rows:
        id_, species, invasive, summary, lat, lng, image_filename, created_at, username = r
        image_url = url_for('uploaded_file', filename=image_filename) if image_filename else None
        items.append({
            "id": id_,
            "species": species,
            "invasive": bool(invasive),
            "summary": summary,
            "lat": lat,
            "lng": lng,
            "image_url": image_url,
            "created_at": created_at,
            "username": username,
        })
    return jsonify({"reports": items}), 200


@app.route("/api/profile", methods=["GET"])
@login_required
def api_profile():
    prof = get_user_profile(current_user.id)
    return jsonify(prof), 200


@app.route("/api/cosmetics/purchase", methods=["POST"])
@login_required
def api_cosmetics_purchase():
    data = request.get_json(force=True, silent=True) or {}
    item_id = data.get('id')
    item = next((c for c in COSMETICS_STORE if c['id'] == item_id), None)
    if not item:
        return jsonify({"detail": "Unknown item"}), 400
    conn = sqlite3.connect(auth_module._db_path())
    cur = conn.cursor()
    cur.execute("SELECT xp_balance, unlocked_cosmetics FROM users WHERE id = ?", (current_user.id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return jsonify({"detail": "User not found"}), 404
    xp_balance, unlocked_json = row
    try:
        unlocked = json.loads(unlocked_json or '[]')
    except Exception:
        unlocked = []
    if item_id in unlocked:
        conn.close()
        return jsonify({"detail": "Already owned"}), 400
    if (xp_balance or 0) < item['cost']:
        conn.close()
        return jsonify({"detail": "Not enough XP"}), 400
    xp_balance -= item['cost']
    unlocked.append(item_id)
    cur.execute("UPDATE users SET xp_balance = ?, unlocked_cosmetics = ? WHERE id = ?", (xp_balance, json.dumps(unlocked), current_user.id))
    conn.commit()
    conn.close()
    return jsonify({"ok": True, "xp_balance": xp_balance, "unlocked_cosmetics": unlocked}), 200


@app.route("/api/cosmetics/equip", methods=["POST"])
@login_required
def api_cosmetics_equip():
    data = request.get_json(force=True, silent=True) or {}
    item_id = data.get('id')
    conn = sqlite3.connect(auth_module._db_path())
    cur = conn.cursor()
    cur.execute("SELECT unlocked_cosmetics FROM users WHERE id = ?", (current_user.id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return jsonify({"detail": "User not found"}), 404
    try:
        unlocked = json.loads(row[0] or '[]')
    except Exception:
        unlocked = []
    if item_id not in unlocked:
        conn.close()
        return jsonify({"detail": "Item not owned"}), 400
    cur.execute("UPDATE users SET active_cosmetic = ? WHERE id = ?", (item_id, current_user.id))
    conn.commit()
    conn.close()
    return jsonify({"ok": True, "active_cosmetic": item_id}), 200


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
    response.set_cookie('Invasisee_session', '', expires=0)
    response.set_cookie('remember_token', '', expires=0)
    response.set_cookie('session', '', expires=0)
    
    return response, 200


@login_manager.unauthorized_handler
def unauthorized():
    """Handle unauthorized access"""
    return jsonify({"detail": "Authentication required"}), 401


@app.route("/api/openai/health", methods=["GET"])
def openai_health():
    """Quick readiness check for OpenAI integration without making a billable request."""
    key = os.getenv('OPENAI_API_KEY')
    status = {
        "has_api_key": bool(key),
        "sdk": None,
        "import_ok": False,
    }
    try:
        from openai import OpenAI  # type: ignore
        _ = OpenAI(api_key=key or "")
        status["sdk"] = "new"
        status["import_ok"] = True
    except Exception:
        try:
            import importlib
            _ = importlib.import_module('openai')
            status["sdk"] = "legacy"
            status["import_ok"] = True
        except Exception:
            status["sdk"] = None
            status["import_ok"] = False
    code = 200 if status["has_api_key"] and status["import_ok"] else 500
    return jsonify(status), code


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

