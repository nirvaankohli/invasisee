# InvaSee 🌿

**Spot. Verify. Protect.**

InvaSee is a community-driven platform for identifying, reporting, and tracking invasive species to help protect local ecosystems.

## 🎯 Project Overview

InvaSee combines mobile-first web technologies with community engagement to create a powerful tool for conservation efforts. Users can:

- **Spot**: Discover and identify invasive species using our identification guide
- **Verify**: Upload photos and locations to confirm sightings with the community
- **Protect**: Contribute to conservation efforts and track your environmental impact

## 🏗️ Architecture

The project consists of a unified Flask application serving both backend API and frontend HTML:

### Application Stack
A Flask-based web application with server-side rendering and secure authentication:
- **HTML/CSS/JS** for the frontend with vanilla JavaScript
- **Flask** backend with secure session management
- **Flask-Login** for user authentication
- **SQLite** database for user management

**Tech Stack**: Python, Flask, Flask-Login, HTML5, CSS3, Vanilla JavaScript

### Features
- Server-side rendering with Jinja2 templates
- Secure session-based authentication with HTTPOnly cookies
- RESTful API endpoints for user management
- Responsive mobile-first design
- Nature-inspired UI with smooth animations

See [backend/README.md](./backend/README.md) for detailed backend documentation.

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation and Running

1. **Install dependencies**:
```bash
cd backend
pip install -r requirements.txt
```

2. **Set up environment variables** (create a `.env` file in the `backend` directory):
```bash
SECRET_KEY=your-secret-key-here
```

3. **Run the Flask application**:
```bash
python main.py
```

4. **Access the application**:
Visit `http://localhost:5000` to view the application.

The database will be automatically created on first run at `backend/db/auth.db`.

### Development Mode

For development with auto-reload:
```bash
cd backend
export FLASK_ENV=development
python main.py
```

## 📸 Screenshots

### Desktop
![Desktop View](https://github.com/user-attachments/assets/b4c2d9c7-dc93-46c5-b5bc-f06497450c29)

### Mobile
![Mobile View](https://github.com/user-attachments/assets/ade65d30-5db9-44cd-ab77-bc449e15ef98)

## 🎨 Design Philosophy

- **Nature-Inspired**: Organic shapes, green gradients, and leaf motifs
- **Clean & Minimal**: Generous whitespace and refined typography
- **Accessible**: WCAG 2.1 Level AA compliant with 4.5:1 contrast ratios
- **Mobile-First**: Optimized for all screen sizes from phones to desktop

## 🤝 Contributing

We welcome contributions! Please feel free to submit issues and pull requests.

## 📄 License

[License information to be added]

## 👥 Team

Built with ❤️ by the InvaSee team
