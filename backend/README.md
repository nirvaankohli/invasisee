# InvaSee Backend

Flask-based backend application with secure session management and authentication.

## 🏗️ Architecture

- **Flask**: Web framework for Python
- **Flask-Login**: User session management
- **SQLite**: Database for user storage
- **Jinja2**: Server-side template rendering
- **Secure Sessions**: HTTPOnly cookies with session protection

## 📁 Project Structure

```
backend/
├── main.py              # Flask application and routes
├── auth.py              # Authentication utilities
├── requirements.txt     # Python dependencies
├── templates/          # HTML templates
│   └── index.html      # Main application template
├── static/             # Static assets
│   ├── css/
│   │   └── styles.css  # Application styles
│   └── js/
│       └── app.js      # Client-side JavaScript
└── db/                 # Database files (auto-created)
    └── auth.db         # SQLite database
```

## 🔐 Security Features

### Session Management
- **HTTPOnly Cookies**: Prevents XSS attacks by making cookies inaccessible to JavaScript
- **SameSite Protection**: Set to 'Lax' to prevent CSRF attacks
- **Secure Flag**: Can be enabled for HTTPS in production
- **Session Protection**: Flask-Login provides strong session protection

### Authentication
- **Password Hashing**: Uses passlib with PBKDF2-SHA256
- **User Session Management**: Flask-Login handles user sessions securely
- **Database**: SQLite with parameterized queries to prevent SQL injection

### Configuration
```python
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)
app.config['SESSION_COOKIE_NAME'] = 'invasee_session'
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip

### Installation

1. **Create and activate a virtual environment** (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**:
```bash
cp .env.example .env
# Edit .env and set a secure SECRET_KEY
```

4. **Generate a secure secret key**:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Running the Application

**Development mode**:
```bash
python main.py
```

The application will be available at `http://localhost:5000`

**Production deployment**:
For production, use a WSGI server like Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 main:app
```

## 📡 API Endpoints

### Authentication Endpoints

#### POST `/api/register`
Register a new user account.

**Request Body**:
```json
{
  "username": "string",
  "password": "string"
}
```

**Response** (200 OK):
```json
{
  "msg": "user created"
}
```

#### POST `/api/login`
Login and create a secure session.

**Request Body**:
```json
{
  "username": "string",
  "password": "string"
}
```

**Response** (200 OK):
```json
{
  "msg": "logged in successfully",
  "username": "string",
  "is_authenticated": true
}
```

**Sets secure HTTPOnly cookie**: `invasee_session`

#### GET `/api/me`
Get current user information (requires authentication).

**Response** (200 OK):
```json
{
  "username": "string",
  "created_at": "timestamp",
  "is_authenticated": true
}
```

#### POST `/api/logout`
Logout and clear session (requires authentication).

**Response** (200 OK):
```json
{
  "msg": "logged out successfully"
}
```

### Page Routes

#### GET `/`
Serves the main HTML application with server-side rendered authentication state.

## 🗄️ Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

## 🔧 Configuration

### Environment Variables
- `SECRET_KEY`: Flask secret key for session signing (required)
- `ALGORITHM`: Algorithm for JWT tokens (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Session timeout in minutes (default: 60)

### Flask Configuration
Edit `main.py` to modify:
- Session cookie settings
- Session lifetime
- Login manager configuration

## 🧪 Testing

Run tests with pytest:
```bash
pytest tests/
```

## 🚨 Security Best Practices

### For Production Deployment:

1. **Set SESSION_COOKIE_SECURE to True**:
```python
app.config['SESSION_COOKIE_SECURE'] = True  # Requires HTTPS
```

2. **Use a strong SECRET_KEY**:
Generate with: `python -c "import secrets; print(secrets.token_hex(32))"`

3. **Enable HTTPS**:
Use a reverse proxy like Nginx with SSL/TLS certificates

4. **Use a production WSGI server**:
Deploy with Gunicorn, uWSGI, or similar

5. **Database backup**:
Regularly backup the SQLite database file

6. **Environment variables**:
Never commit `.env` file to version control

## 📚 Dependencies

- **Flask**: Web framework
- **Flask-Login**: User session management
- **passlib**: Password hashing
- **python-jose**: JWT token handling (for API extensions)
- **python-dotenv**: Environment variable management

## 🛠️ Development

### Adding New Routes
Add routes in `main.py`:
```python
@app.route("/new-route")
def new_route():
    return render_template('new_template.html')
```

### Adding Protected Routes
Use the `@login_required` decorator:
```python
@app.route("/protected")
@login_required
def protected():
    return f"Hello {current_user.username}!"
```

## 📄 License

[License information to be added]
