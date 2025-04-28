import requests
import random
import time
from datetime import datetime, timedelta

# === CONFIG ===
API_URL = "http://soc_app:5000/add_threat"
API_URL = "http://localhost:5000/add_threat"
THREAT_COUNT = 10
DELAY_BETWEEN_THREATS = 2  # seconds

# === DYNAMIC THREAT DATA ===
sources = [
    "Web Application Firewall", "Endpoint Antivirus", "Firewall",
    "SIEM", "DLP System", "Email Gateway", "Authentication Server"
]

events = [
    "SQL Injection Attempt",
    "Ransomware Detected",
    "Brute Force Login Detected",
    "Port Scan Detected",
    "Data Exfiltration Attempt",
    "Phishing Email Delivered",
    "Unauthorized Access Attempt"
]

details_lookup = {
    "SQL Injection Attempt": "Suspicious input in query param triggered WAF rule.",
    "Ransomware Detected": "File encryption and ransom note pattern identified.",
    "Brute Force Login Detected": "Excessive login attempts from external IP.",
    "Port Scan Detected": "Nmap-like scanning behavior detected.",
    "Data Exfiltration Attempt": "Sensitive file transfer to foreign IP blocked.",
    "Phishing Email Delivered": "Malicious attachment in email from suspicious domain.",
    "Unauthorized Access Attempt": "User tried accessing restricted resource."
}

# === THREAT SENDER ===
def generate_threat():
    source = random.choice(sources)
    event = random.choice(events)
    timestamp = (datetime.now() - timedelta(minutes=random.randint(0, 30))).strftime("%Y-%m-%d %H:%M")
    details = details_lookup[event]

    payload = {
        "timestamp": timestamp,
        "source": source,
        "event": event,
        "details": details
    }

    return payload

def send_threat(threat_data):
    try:
        response = requests.post(API_URL, json=threat_data)
        if response.status_code == 201:
            print(f"✅ Injected: [{threat_data['timestamp']}] {threat_data['event']} from {threat_data['source']}")
        else:
            print(f"⚠️  Failed to send threat: {response.status_code} | {response.text}")
    except Exception as e:
        print(f"❌ Error sending threat: {e}")

# === EXECUTION LOOP ===
if __name__ == "__main__":
    print("🚨 Starting Threat Simulator Mode...")

    for _ in range(THREAT_COUNT):
        threat = generate_threat()
        send_threat(threat)
        time.sleep(DELAY_BETWEEN_THREATS)

    print("🎯 Threat simulation complete.")
