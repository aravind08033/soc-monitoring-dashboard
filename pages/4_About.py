"""
pages/4_About.py
--------------------
Project documentation: description, modules, tech stack, and learning outcomes.
"""

import streamlit as st

from theme import get_theme, inject_global_css, render_sidebar_brand, render_theme_toggle, footer, init_session_state

st.set_page_config(page_title="SOC Dashboard | About", page_icon="ℹ️", layout="wide",
                    initial_sidebar_state="expanded")

init_session_state()
T = get_theme()
inject_global_css()

with st.sidebar:
    render_sidebar_brand()
    render_theme_toggle()

st.markdown(f"""
<div class="dash-header">
    <div>
        <p class="dash-title">ℹ️ About This Project</p>
        <p class="dash-subtitle">Security Operations Center (SOC) Monitoring Dashboard — Major Project</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="info-card">
<p style="color:{T['text_primary']};line-height:1.7;">
A Security Operations Center (SOC) Monitoring Dashboard is a centralized system used by
cybersecurity teams to continuously monitor, analyze, and respond to security events occurring
across an organization's network and systems. This project implements a simplified SOC dashboard
that collects security logs, analyzes them, detects suspicious activity, and presents the results
through interactive visualizations and reports.
</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-label">Project Modules</div>', unsafe_allow_html=True)
modules = [
    ("1️⃣", "Log Collection", "Reads log data from CSV files into Pandas DataFrames for processing."),
    ("2️⃣", "Log Analysis", "Counts successful/failed logins and flags suspicious users by activity pattern."),
    ("3️⃣", "Threat Detection", "Identifies brute-force attempts, suspicious IPs, and abnormal login behavior."),
    ("4️⃣", "Dashboard", "Visualizes login statistics, trends, geography, and user activity interactively."),
    ("5️⃣", "Reporting", "Generates incident summaries with actionable security recommendations."),
]
cols = st.columns(5)
for col, (icon, title, desc) in zip(cols, modules):
    col.markdown(f"""
    <div class="info-card" style="height:190px;">
        <div style="font-size:1.6rem;">{icon}</div>
        <div style="font-weight:700;color:{T['text_primary']};margin-top:6px;">{title}</div>
        <div style="color:{T['text_secondary']};font-size:0.8rem;margin-top:4px;line-height:1.4;">{desc}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="section-label">Technology Stack</div>', unsafe_allow_html=True)
tech_cols = st.columns(6)
techs = ["Python", "Pandas", "NumPy", "Plotly", "Streamlit", "Matplotlib"]
for col, tech in zip(tech_cols, techs):
    col.markdown(f"""
    <div class="info-card" style="text-align:center;padding:1rem 0.5rem;">
        <div style="font-weight:700;color:{T['accent']};">{tech}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="section-label">Learning Outcomes</div>', unsafe_allow_html=True)
st.markdown(f"""
<div class="info-card">
<ul style="color:{T['text_primary']};line-height:1.8;">
    <li>Security log monitoring and analysis at scale</li>
    <li>Pattern-based threat detection (brute-force, anomaly detection)</li>
    <li>Interactive data visualization and dashboard design</li>
    <li>Security incident reporting and recommendation generation</li>
    <li>Building production-style multi-page web applications with Streamlit</li>
</ul>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-label">Project Info</div>', unsafe_allow_html=True)
st.markdown(f"""
<div class="info-card">
    <p style="color:{T['text_secondary']};margin:0;">
        <b style="color:{T['text_primary']};">Student:</b> Aravind Damera &nbsp;·&nbsp;
        <b style="color:{T['text_primary']};">Branch:</b> B.Tech CSE (Data Science) &nbsp;·&nbsp;
        <b style="color:{T['text_primary']};">College:</b> QIS College of Engineering & Technology, Ongole &nbsp;·&nbsp;
        <b style="color:{T['text_primary']};">University:</b> JNTUK
    </p>
</div>
""", unsafe_allow_html=True)

footer()
