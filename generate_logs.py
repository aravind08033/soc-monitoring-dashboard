"""
generate_logs.py
-----------------
Generates a realistic, large-scale synthetic security log dataset for the
SOC (Security Operations Center) Monitoring Dashboard project.

Produces: data/security_logs.csv  (~3000 records, 6 months of history)

Columns:
    timestamp     - date & time of the login event
    username      - account that attempted login
    ip_address    - source IP of the request
    event_type    - "Login Success" or "Login Failed"
    location      - approximate geo location of the IP
    device        - device/browser used
    lat, lon      - coordinates for the location (for map visualization)
    severity      - Low / Medium / High (assigned to failed events)
"""

import csv
import random
from datetime import datetime, timedelta

random.seed(7)

OUTPUT_FILE = "data/security_logs.csv"

NORMAL_USERS = [
    "rakesh.kumar", "sneha.reddy", "arjun.rao", "priya.singh",
    "kiran.varma", "anjali.devi", "suresh.babu", "lakshmi.naidu",
    "vijay.kumar", "divya.sharma", "manoj.verma", "swathi.iyer",
    "naveen.chowdary", "deepika.rao", "harish.bhat", "pooja.menon",
    "ravi.teja", "sunitha.k", "abhishek.nair", "meena.pillai",
]

SUSPICIOUS_USERS = ["admin", "user5", "test_user", "root", "guest", "administrator"]

NORMAL_IPS = [
    "192.168.1.10", "192.168.1.14", "192.168.1.22", "192.168.1.35",
    "192.168.1.41", "10.0.0.5", "10.0.0.12", "10.0.0.18", "10.0.0.27",
    "10.0.0.33", "172.16.0.4", "172.16.0.9",
]

SUSPICIOUS_IPS = [
    "45.227.13.4", "103.211.9.88", "185.220.101.7", "194.5.6.12",
    "91.243.85.20", "198.51.100.23",
]

LOCATIONS_NORMAL = ["Hyderabad, IN", "Ongole, IN", "Vijayawada, IN", "Chennai, IN", "Bangalore, IN", "Pune, IN"]
LOCATIONS_SUSPICIOUS = ["Unknown", "Moscow, RU", "Lagos, NG", "Bucharest, RO", "Hanoi, VN"]

LOCATION_COORDS = {
    "Hyderabad, IN": (17.3850, 78.4867),
    "Ongole, IN": (15.5057, 80.0499),
    "Vijayawada, IN": (16.5062, 80.6480),
    "Chennai, IN": (13.0827, 80.2707),
    "Bangalore, IN": (12.9716, 77.5946),
    "Pune, IN": (18.5204, 73.8567),
    "Moscow, RU": (55.7558, 37.6173),
    "Lagos, NG": (6.5244, 3.3792),
    "Bucharest, RO": (44.4268, 26.1025),
    "Hanoi, VN": (21.0285, 105.8542),
    "Unknown": (0.0, 0.0),
}

DEVICES = ["Windows-Chrome", "MacOS-Safari", "Linux-Firefox", "Android-App", "iOS-App", "Windows-Edge"]


def random_timestamp(start, end):
    delta = end - start
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return start + timedelta(seconds=random_seconds)


def biased_hour_timestamp(day):
    """Most normal logins happen during business hours (9am-7pm), with a small tail."""
    if random.random() < 0.85:
        hour = random.randint(9, 19)
    else:
        hour = random.choice(list(range(0, 9)) + list(range(20, 24)))
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return day.replace(hour=hour, minute=minute, second=second)


def severity_for_failed(streak_position, total_in_burst):
    if total_in_burst >= 8:
        return "High"
    elif total_in_burst >= 4:
        return "Medium"
    return "Low"


def generate_normal_traffic(rows, start, end, count=2400):
    """Legitimate daily user logins, business-hour biased, mostly successful."""
    num_days = (end - start).days
    for _ in range(count):
        day_offset = random.randint(0, num_days)
        day = start + timedelta(days=day_offset)
        ts = biased_hour_timestamp(day)
        user = random.choice(NORMAL_USERS)
        ip = random.choice(NORMAL_IPS)
        event = "Login Success" if random.random() > 0.07 else "Login Failed"
        location = random.choice(LOCATIONS_NORMAL)
        lat, lon = LOCATION_COORDS[location]
        rows.append({
            "timestamp": ts.strftime("%Y-%m-%d %H:%M:%S"),
            "username": user,
            "ip_address": ip,
            "event_type": event,
            "location": location,
            "device": random.choice(DEVICES),
            "lat": lat,
            "lon": lon,
            "severity": "Low" if event == "Login Failed" else "",
        })


def generate_brute_force_traffic(rows, start, end, num_campaigns=40):
    """Multiple brute-force campaigns scattered across the 6-month window."""
    num_days = (end - start).days
    for _ in range(num_campaigns):
        user = random.choice(SUSPICIOUS_USERS)
        ip = random.choice(SUSPICIOUS_IPS)
        day_offset = random.randint(0, num_days)
        burst_start = start + timedelta(days=day_offset, hours=random.randint(0, 23), minutes=random.randint(0, 59))
        num_attempts = random.randint(5, 14)
        location = random.choice(LOCATIONS_SUSPICIOUS)
        lat, lon = LOCATION_COORDS[location]
        for i in range(num_attempts):
            ts = burst_start + timedelta(seconds=i * random.randint(5, 45))
            is_last = (i == num_attempts - 1)
            event = "Login Success" if (is_last and random.random() > 0.55) else "Login Failed"
            sev = severity_for_failed(i, num_attempts) if event == "Login Failed" else ""
            rows.append({
                "timestamp": ts.strftime("%Y-%m-%d %H:%M:%S"),
                "username": user,
                "ip_address": ip,
                "event_type": event,
                "location": location,
                "device": random.choice(DEVICES),
                "lat": lat,
                "lon": lon,
                "severity": sev,
            })


def generate_weekend_spike(rows, start, end, count=150):
    """Occasional odd-hour weekend anomalies for variety in the abnormal-activity detector."""
    num_days = (end - start).days
    for _ in range(count):
        day_offset = random.randint(0, num_days)
        day = start + timedelta(days=day_offset)
        if day.weekday() < 5:  # force to weekend-ish odd hour event regardless of literal weekday
            pass
        hour = random.choice([0, 1, 2, 3, 4, 23])
        ts = day.replace(hour=hour, minute=random.randint(0, 59), second=random.randint(0, 59))
        user = random.choice(NORMAL_USERS + SUSPICIOUS_USERS)
        ip = random.choice(NORMAL_IPS + SUSPICIOUS_IPS)
        event = random.choice(["Login Failed", "Login Failed", "Login Success"])
        location = random.choice(LOCATIONS_NORMAL + LOCATIONS_SUSPICIOUS)
        lat, lon = LOCATION_COORDS[location]
        rows.append({
            "timestamp": ts.strftime("%Y-%m-%d %H:%M:%S"),
            "username": user,
            "ip_address": ip,
            "event_type": event,
            "location": location,
            "device": random.choice(DEVICES),
            "lat": lat,
            "lon": lon,
            "severity": "Medium" if event == "Login Failed" else "",
        })


def main():
    end = datetime(2026, 6, 25, 23, 59, 59)
    start = end - timedelta(days=182)  # ~6 months

    rows = []
    generate_normal_traffic(rows, start, end, count=2400)
    generate_brute_force_traffic(rows, start, end, num_campaigns=40)
    generate_weekend_spike(rows, start, end, count=150)

    rows.sort(key=lambda r: r["timestamp"])

    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "timestamp", "username", "ip_address", "event_type",
            "location", "device", "lat", "lon", "severity"
        ])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated {len(rows)} log records spanning {start.date()} to {end.date()} -> {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
