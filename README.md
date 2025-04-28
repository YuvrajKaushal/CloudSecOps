# 🛡️ CloudSecOps - SOC Dashboard

CloudSecOps is a Security Operations Center (SOC) dashboard built using Python Flask, PostgreSQL, Socket.IO, and Chart.js.  
It provides real-time monitoring, incident response, reporting, and AI threat analysis 🧠 for cybersecurity teams.

---

## 📸 Features

- **🔐 Secure Login System** — Role-based access (Admin, Analyst, Incident Manager).
- **📈 Live Dashboard** — Real-time threat tracking with live updating graphs.
- **⚡ Real-time Alerts** — Threats pushed to frontend instantly via WebSocket (Socket.IO).
- **🧠 AI Insights** — Integrated ML-based AI hints and threat commentary.
- **📋 Incident Response Panel** — Review, triage, and resolve incidents.
- **📊 Reports Module** — Generate reports between custom date ranges.
- **🧩 Widget Editing Mode** — Add, remove, and rearrange dashboard widgets visually.
- **💾 PostgreSQL Backend** — Reliable storage of threat logs and incidents.
- **🛡️ Secure Session Management** — Role-based sessions and logout system.
- **🌑 Full Dark Mode UI** — Modern, sleek, cybersecurity-themed dashboard.

---

## 🛠️ Technologies Used

- **Python 3.11 
- **Flask 
- **Flask-SQLAlchemy
- **Socket.IO (Flask-SocketIO) 
- **PostgreSQL
- **Chart.js 
- **HTML5 / CSS3 / JavaScript 
- **Docker** *(Recommended for deployment)*

---

## 🚀 Quickstart (Dev)

1. Clone the repo
   ```bash
   git clone https://github.com/yourusername/cloudsecops-soc-dashboard.git
   cd cloudsecops-soc-dashboard
2. pip install -r requirements.txt
3.python app.py
      OR
  docker-compose up --build


