#!/bin/bash

# === CONFIG ===
API_URL="http://localhost:5000/add_threat"
CONTENT_TYPE="Content-Type: application/json"

# === THREAT PAYLOADS ===
declare -a threats=(
  '{"timestamp":"2025-04-17 16:45","source":"Web Application Firewall","event":"SQL Injection Attempt","details":"Suspicious payload detected in login POST request"}'
  '{"timestamp":"2025-04-17 17:00","source":"Endpoint Antivirus","event":"Ransomware Detected","details":"Encryption activity and ransom note identified in user documents"}'
  '{"timestamp":"2025-04-17 17:15","source":"DLP System","event":"Data Exfiltration Attempt","details":"Sensitive data attempted to be uploaded to external domain"}'
  '{"timestamp":"2025-04-17 17:30","source":"Authentication Server","event":"Brute Force Login Detected","details":"1000+ failed login attempts from 192.168.1.25"}'
  '{"timestamp":"2025-04-17 17:45","source":"Firewall","event":"Port Scan Detected","details":"Nmap-style scan from 10.0.0.12 on multiple ports"}'
)

# === SEND THREATS ===
echo "🚀 Injecting demo threats into SOC..."

for i in "${!threats[@]}"; do
  echo -e "\n🔐 Sending threat $((i+1))..."
  curl -s -X POST "$API_URL" \
    -H "$CONTENT_TYPE" \
    -d "${threats[$i]}"
done

echo -e "\n✅ All demo threats successfully sent to $API_URL!"
