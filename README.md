# Security Operations Center (SOC) Monitoring Dashboard

**Major Project — 2nd Year B.Tech CSE (Data Science)**
QIS College of Engineering & Technology, Ongole | JNTUK

## 🚀 Quick Start (Easiest Way)

1. Extract this zip file (right-click → Extract All).
2. Open the extracted folder and double-click **`Run_Dashboard.bat`**.
3. A window will open and automatically install required packages, then your
   browser will open with the dashboard.

(Requires Python to already be installed on your system — most college lab
computers already have it. If not, install it free from python.org first.)

## Project Description

A Security Operations Center (SOC) Monitoring Dashboard is a centralized
system used by cybersecurity teams to continuously monitor, analyze, and
respond to security events occurring in an organization's network and
systems. This project builds a production-style, multi-page SOC dashboard
that collects ~3,000 security log events spanning 6 months, analyzes them,
detects suspicious activity in real time, and presents the results through
a polished, interactive web application.

## Problem Statement

Organizations generate thousands of security logs every day. Manually
checking these logs is difficult and time-consuming. This project
automatically analyzes security logs to help identify:
- Failed login attempts
- Brute-force attacks
- Unauthorized access attempts
- Unusual user behavior

## Project Structure

```
soc_project/
├── data/
│   └── security_logs.csv       # ~3,000 log events across 6 months
├── output/                     # Generated charts & reports (script version)
├── pages/
│   ├── 1_Dashboard.py          # Main analytics: KPIs, gauge, trend, map, heatmap
│   ├── 2_Alerts.py             # Threat detection: brute-force, suspicious IPs
│   ├── 3_Settings.py           # Thresholds, data source info, report export
│   └── 4_About.py              # Project documentation
├── theme.py                    # Shared theme, CSS, and data-loading helpers
├── generate_logs.py            # Generates the synthetic 6-month dataset
├── log_analysis.py             # Module 1 & 2: Log Collection + Log Analysis
├── threat_detection.py         # Module 3: Threat Detection
├── dashboard.py                # Module 4: Static Matplotlib charts (script version)
├── report_generator.py         # Module 5: Reporting
├── main.py                     # Console/script version - exact expected output format
├── app.py                      # Streamlit multi-page app - HOME page / entry point
└── requirements.txt            # Python dependencies
```

## Modules (as per Project Description)

| Module | Description |
|---|---|
| 1. Log Collection | Reads log data from CSV files into Pandas DataFrames |
| 2. Log Analysis | Counts successful/failed logins, detects suspicious users |
| 3. Threat Detection | Identifies brute-force attempts, abnormal login activity |
| 4. Dashboard | Login statistics, failed login graphs, user activity charts |
| 5. Reporting | Generates incident summaries and security recommendations |

## Application Pages

- **🏠 Home** — Landing page with quick stats and navigation cards
- **📊 Dashboard** — Risk gauge, login trend, global attack map, weekly heatmap, user activity, live monitoring mode
- **🚨 Alerts** — Brute-force campaign detection, suspicious IPs, abnormal activity log, incident timeline
- **⚙️ Settings** — Adjustable detection thresholds, data source summary, report export
- **ℹ️ About** — Project modules, tech stack, learning outcomes

## Key Features

- 🎨 **Dual theme** — Dark Cyber (neon-on-black) and Light Corporate, switchable from the sidebar on every page
- 🔴 **Live Monitoring Mode** — auto-refreshing view with an animated live alert feed
- 📈 **~3,000 log records** spanning 6 months, 26 users, 11 global locations
- 🌍 **Interactive world map** of login/attack sources
- 🎯 **Risk Score gauge**, weekly activity heatmap, and incident timeline
- 📄 **One-click report and CSV export**

## Technologies Used

- Python, Pandas, NumPy
- Plotly (interactive charts) / Matplotlib (script version)
- Streamlit (multi-page web application)
- CSV Files

## How to Run

### 1. Script Version (matches the exact expected output format)

```bash
pip install pandas matplotlib
python3 main.py
```

Prints the SOC Security Report to the console in the exact format from the
project description, and saves chart images + a report text file to `output/`.

### 2. Multi-Page Streamlit Web App

```bash
pip install -r requirements.txt
streamlit run app.py
```

Opens the full interactive web application in your browser, starting at the
Home page. Use the sidebar page links (or the navigation cards on Home) to
move between Dashboard, Alerts, Settings, and About.

You can upload your own CSV log file from the sidebar on the Dashboard,
Alerts, or Settings pages (columns: `timestamp, username, ip_address,
event_type, location, device, lat, lon, severity`).

### Deploying to Streamlit Community Cloud

1. Push this folder to a GitHub repository.
2. Go to share.streamlit.io and connect your GitHub repo.
3. Set the main file path to `app.py`.
4. Deploy — Streamlit Cloud installs everything from `requirements.txt`.

## Learning Outcomes

- Security Monitoring & Log Analysis at scale
- Threat Detection (brute-force, anomaly detection)
- Interactive Data Visualization & Dashboard Design
- Security Incident Reporting
- Building production-style multi-page web applications
