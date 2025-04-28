import eventlet
eventlet.monkey_patch()

import json
import joblib
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from time import sleep
from datetime import datetime

# 🛡️ App Setup
app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = 'your_secret_key'

DATABASE_HOST = 'db'
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://soc_admin:soc_password@{DATABASE_HOST}/soc_db'

socketio = SocketIO(app, async_mode='eventlet')
db = SQLAlchemy(app)

# 🧬 Threat Model
class Threat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(100), nullable=False)
    source = db.Column(db.String(100), nullable=False)
    event = db.Column(db.String(200), nullable=False)
    details = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(50), default='Pending')

# 🛠 Ensure DB is ready
MAX_RETRIES = 5
for attempt in range(MAX_RETRIES):
    try:
        with app.app_context():
            db.create_all()
        print("✅ Database connection successful!")
        break
    except Exception as e:
        print(f"⏳ Database not ready, retrying ({attempt + 1}/{MAX_RETRIES})...")
        sleep(5)
else:
    print("❌ Failed to connect to database after retries. Exiting...")
    exit(1)

# ==================== ROUTES ====================

# 🏠 Home / Dashboard
@app.route('/')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template("dashboard.html")

# 🔐 Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        role = request.form.get('role')
        password = request.form.get('password')

        # ⚡ Very basic password check
        if password == "admin123":  # temporary password
            session['user'] = role
            return redirect(url_for('home'))
        else:
            return "❌ Invalid credentials", 401

    return render_template("login.html")

# 🚪 Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ⚡ Dashboard APIs
@app.route('/dashboard_stats')
def dashboard_stats():
    stats = {
        "monitored_devices": 5,
        "monitored_endpoints": 298,
        "monitored_users": 9,
        "processed_logs": 9400000,
        "security_events": Threat.query.count(),
        "triaged_alerts": Threat.query.filter_by(status="Triaged").count(),
        "escalated_alerts": Threat.query.filter_by(status="Escalated").count()
    }
    return jsonify(stats)

@app.route('/get_threats')
def get_threats():
    threats = Threat.query.with_entities(Threat.event, db.func.count(Threat.event)).group_by(Threat.event).all()
    threat_types = [t[0] for t in threats]
    threat_counts = [t[1] for t in threats]
    return jsonify({"types": threat_types, "counts": threat_counts})

@app.route('/get_all_threats')
def get_all_threats():
    threats = Threat.query.all()
    return jsonify([
        {
            "id": t.id,
            "timestamp": t.timestamp,
            "source": t.source,
            "event": t.event,
            "status": t.status
        } for t in threats
    ])

@app.route('/add_threat', methods=['POST'])
def add_threat():
    data = request.json
    new_threat = Threat(
        timestamp=data['timestamp'],
        source=data['source'],
        event=data['event'],
        details=data['details'],
        status="Pending"
    )
    db.session.add(new_threat)
    db.session.commit()

    socketio.emit('new_threat', {"message": "New threat detected", "threat": data})
    return jsonify({"message": "Threat added successfully"}), 201

@app.route('/update_threat/<int:threat_id>', methods=['PUT'])
def update_threat(threat_id):
    threat = Threat.query.get(threat_id)
    if threat:
        data = request.json
        threat.status = data.get("status", threat.status)
        db.session.commit()
        return jsonify({"message": "Threat updated successfully"})
    return jsonify({"error": "Threat not found"}), 404

@app.route('/delete_threat/<int:threat_id>', methods=['DELETE'])
def delete_threat(threat_id):
    threat = Threat.query.get(threat_id)
    if threat:
        db.session.delete(threat)
        db.session.commit()
        return jsonify({"message": "Threat deleted successfully"})
    return jsonify({"error": "Threat not found"}), 404

# 📈 Other Pages
@app.route('/incident_response')
def incident_response():
    if 'user' not in session:
        return redirect(url_for('login'))
    incidents = Threat.query.filter(Threat.status.in_(['Pending', 'Escalated'])).all()
    threats = [
        {
            "id": i.id,
            "timestamp": i.timestamp,
            "source": i.source,
            "event": i.event,
            "status": i.status,
            "severity": classify_severity(i.event)
        } for i in incidents
    ]
    return render_template("incident_response.html", threats=threats)

@app.route('/resolve_threat/<int:threat_id>', methods=['POST'])
def resolve_threat(threat_id):
    threat = Threat.query.get(threat_id)
    if threat:
        threat.status = "Resolved"
        db.session.commit()
    return redirect(url_for('incident_response'))

@app.route('/alerts')
def alerts():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template("alerts.html")

@app.route('/reports')
def reports():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template("reports.html")

@app.route('/threat_timeline')
def threat_timeline():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template("threat_timeline.html")

@app.route('/get_reports')
def get_reports():
    start = request.args.get('start')
    end = request.args.get('end')

    try:
        start_date = datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.strptime(end, "%Y-%m-%d")
    except (TypeError, ValueError):
        return jsonify([])

    reports = Threat.query.filter(
        db.func.to_timestamp(Threat.timestamp, 'YYYY-MM-DD HH24:MI') >= start_date,
        db.func.to_timestamp(Threat.timestamp, 'YYYY-MM-DD HH24:MI') <= end_date
    ).all()

    return jsonify([
        {
            "id": r.id,
            "timestamp": r.timestamp,
            "event": r.event,
            "severity": classify_severity(r.event),
            "status": r.status
        } for r in reports
    ])

@app.route('/get_ai_insights')
def get_ai_insights():
    threats = Threat.query.all()

    def ai_comment(event):
        if "Brute Force" in event:
            return "🧠 Likely false positive (based on login frequency)"
        elif "SQL Injection" in event:
            return "🧠 Matches critical threat signature"
        elif "Ransomware" in event:
            return "🧠 Encryption behavior detected - isolate immediately"
        else:
            return "🧠 No significant match"

    return jsonify([
        {
            "event": t.event,
            "status": t.status,
            "ai": ai_comment(t.event)
        } for t in threats
    ])

# 📡 WebSocket Event
@socketio.on("request_threat_data")
def handle_threat_data():
    threats = Threat.query.all()
    socketio.emit("threat_data", [
        {
            "timestamp": t.timestamp,
            "source": t.source,
            "event": t.event,
            "status": t.status,
            "severity": classify_severity(t.event)
        } for t in threats
    ])

# 🧠 Classify severity simple helper
def classify_severity(event):
    high = ["Ransomware Detected", "SQL Injection Attempt", "Data Exfiltration Attempt"]
    medium = ["Brute Force Login Detected"]
    if event in high:
        return "High"
    elif event in medium:
        return "Medium"
    else:
        return "Low"

# 🚀 Main runner
if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
