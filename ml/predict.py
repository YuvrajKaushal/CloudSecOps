import random

def predict_threat(log):
    # Dummy logic: replace with real ML model
    return {
        "alert": "Malicious" if random.random() > 0.5 else "Benign",
        "severity": random.choice(["Low", "Medium", "High"]),
        "source_ip": log.get("ip", "0.0.0.0")
    }