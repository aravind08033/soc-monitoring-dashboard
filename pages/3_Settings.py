"""
pages/3_Settings.py
----------------------
Detection thresholds, theme preferences, and report export.
"""

import streamlit as st

from theme import get_theme, inject_global_css, render_sidebar_brand, render_theme_toggle, load_dataset, footer, init_session_state
from log_analysis import count_successful_logins, count_failed_logins, total_events, detect_suspicious_users
from threat_detection import detect_brute_force
from report_generator import build_recommendations, generate_report_text

st.set_page_config(page_title="SOC Dashboard | Settings", page_icon="⚙️", layout="wide",
                    initial_sidebar_state="expanded")

init_session_state()
T = get_theme()
inject_global_css()

with st.sidebar:
    render_sidebar_brand()
    render_theme_toggle()
    st.markdown("---")
    uploaded_file = st.file_uploader("📁 Upload security log CSV", type=["csv"], key="settings_uploader")

df = load_dataset(uploaded_file)

st.markdown(f"""
<div class="dash-header">
    <div>
        <p class="dash-title">⚙️ Settings & Preferences</p>
        <p class="dash-subtitle">Tune detection sensitivity and export incident reports</p>
    </div>
</div>
""", unsafe_allow_html=True)

c1, c2 = st.columns(2)

with c1:
    st.markdown('<div class="section-label">Detection Thresholds</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.session_state.failed_threshold = st.slider(
        "Suspicious user threshold (failed logins)", 2, 15, st.session_state.failed_threshold,
        help="A user is flagged as suspicious once their failed-login count reaches this number."
    )
    st.session_state.brute_force_threshold = st.slider(
        "Brute-force alert threshold (failed logins)", 3, 20, st.session_state.brute_force_threshold,
        help="A login source is flagged as a brute-force campaign once failed attempts reach this number."
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-label">Appearance</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.write("Theme is controlled from the sidebar on every page (Dark Cyber / Light Corporate).")
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="section-label">Data Source</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.write(f"**Rows loaded:** {len(df):,}")
    st.write(f"**Date range:** {df['timestamp'].min().strftime('%d %b %Y')} → {df['timestamp'].max().strftime('%d %b %Y')}")
    st.write(f"**Unique users:** {df['username'].nunique()}")
    st.write(f"**Unique IPs:** {df['ip_address'].nunique()}")
    st.write(f"**Unique locations:** {df['location'].nunique()}")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section-label">Export Incident Report</div>', unsafe_allow_html=True)
success_count = count_successful_logins(df)
failed_count = count_failed_logins(df)
events_total = total_events(df)
suspicious_users = detect_suspicious_users(df, failed_threshold=st.session_state.failed_threshold)
brute_force_df = detect_brute_force(df, failed_threshold=st.session_state.brute_force_threshold)
recommendations = build_recommendations(suspicious_users, brute_force_df)
report_text = generate_report_text(
    total_events=events_total, success_count=success_count, failed_count=failed_count,
    suspicious_users=suspicious_users, recommendations=recommendations,
)

st.code(report_text, language=None)
dl1, dl2 = st.columns(2)
with dl1:
    st.download_button("⬇️ Download Report (.txt)", data=report_text,
                        file_name="soc_security_report.txt", mime="text/plain", use_container_width=True)
with dl2:
    st.download_button("⬇️ Download Raw Logs (.csv)", data=df.to_csv(index=False),
                        file_name="security_logs.csv", mime="text/csv", use_container_width=True)

footer()
