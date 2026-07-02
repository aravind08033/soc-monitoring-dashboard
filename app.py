"""
app.py  (Home Page)
---------------------
SOC Monitoring Dashboard - Major Project
Multi-page Streamlit application entry point.

Run with:
    streamlit run app.py
"""

import streamlit as st
from datetime import datetime

from theme import (
    get_theme, inject_global_css, render_sidebar_brand, render_theme_toggle,
    load_dataset, footer, init_session_state,
)
from log_analysis import count_successful_logins, count_failed_logins, total_events, detect_suspicious_users
from threat_detection import detect_brute_force

st.set_page_config(page_title="SOC Dashboard | Home", page_icon="🛡️", layout="wide",
                    initial_sidebar_state="expanded")

init_session_state()
T = get_theme()
inject_global_css()

with st.sidebar:
    render_sidebar_brand()
    render_theme_toggle()
    st.markdown("---")
    st.caption("Built with Python · Pandas · Plotly · Streamlit")
    st.caption(f"Session time: {datetime.now().strftime('%d %b %Y, %I:%M %p')}")

df = load_dataset()
success_count = count_successful_logins(df)
failed_count = count_failed_logins(df)
events_total = total_events(df)
suspicious_users = detect_suspicious_users(df, failed_threshold=st.session_state.failed_threshold)
brute_force_df = detect_brute_force(df, failed_threshold=st.session_state.brute_force_threshold)

st.markdown(f"""
<div class="dash-header">
    <div>
        <p class="dash-title">🛡️ Security Operations Center (SOC) Monitoring Dashboard</p>
        <p class="dash-subtitle">Welcome back. Here's what's happening across your network right now.</p>
    </div>
</div>
""", unsafe_allow_html=True)

date_min = df["timestamp"].min().strftime("%d %b %Y")
date_max = df["timestamp"].max().strftime("%d %b %Y")
st.markdown(f"""
<div class="info-card" style="margin-bottom:1.2rem;">
    <span style="color:{T['text_secondary']};font-size:0.85rem;">
        📅 Monitoring window: <b style="color:{T['text_primary']};">{date_min} → {date_max}</b>
        &nbsp;·&nbsp; 📦 <b style="color:{T['text_primary']};">{events_total:,}</b> total log events analyzed
    </span>
</div>
""", unsafe_allow_html=True)

kpi_cols = st.columns(4)
kpi_data = [
    ("TOTAL EVENTS", f"{events_total:,}", T["accent"]),
    ("SUCCESSFUL LOGINS", f"{success_count:,}", T["success"]),
    ("FAILED LOGINS", f"{failed_count:,}", T["danger"]),
    ("ACTIVE THREATS", len(brute_force_df), T["warning"]),
]
for col, (label, value, color) in zip(kpi_cols, kpi_data):
    col.markdown(f"""
    <div class="kpi-card" style="--accent-color:{color};">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="section-label">Quick Navigation</div>', unsafe_allow_html=True)

nav_cols = st.columns(4)
nav_items = [
    ("📊", "Dashboard", "Live charts, risk score, global threat map & trends", "pages/1_Dashboard.py"),
    ("🚨", "Alerts", "Brute-force campaigns, suspicious IPs & abnormal activity", "pages/2_Alerts.py"),
    ("⚙️", "Settings", "Detection thresholds, data source & app preferences", "pages/3_Settings.py"),
    ("ℹ️", "About", "Project info, modules, tech stack & documentation", "pages/4_About.py"),
]
for col, (icon, title, desc, target) in zip(nav_cols, nav_items):
    with col:
        st.markdown(f"""
        <div class="info-card" style="height:170px;">
            <div style="font-size:1.8rem;">{icon}</div>
            <div style="font-weight:700;color:{T['text_primary']};margin-top:6px;font-size:1.05rem;">{title}</div>
            <div style="color:{T['text_secondary']};font-size:0.82rem;margin-top:4px;line-height:1.4;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)
        st.page_link(target, label=f"Open {title} →", use_container_width=True)

st.markdown('<div class="section-label">Top Suspicious Accounts Right Now</div>', unsafe_allow_html=True)
if len(brute_force_df) > 0:
    top3 = brute_force_df.head(3)
    cols = st.columns(len(top3)) if len(top3) > 0 else [st.container()]
    for col, (_, row) in zip(cols, top3.iterrows()):
        badge_class = {"High": "badge-high", "Medium": "badge-medium", "Low": "badge-low"}[row["risk_level"]]
        col.markdown(f"""
        <div class="info-card">
            <div style="font-weight:700;color:{T['text_primary']};font-size:1rem;">{row['username']}</div>
            <div style="color:{T['text_secondary']};font-size:0.8rem;margin:4px 0 8px 0;">{row['failed_attempts']} failed login attempts</div>
            <span class="badge {badge_class}">{row['risk_level']} RISK</span>
        </div>
        """, unsafe_allow_html=True)
else:
    st.success("✅ No active brute-force threats detected at the current sensitivity threshold.")

footer()
