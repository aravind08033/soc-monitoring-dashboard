"""
pages/2_Alerts.py
--------------------
Threat detection center: brute-force campaigns, suspicious IPs,
abnormal-activity log, and an incident timeline view.
"""

import pandas as pd
import plotly.express as px
import streamlit as st

from theme import get_theme, inject_global_css, render_sidebar_brand, render_theme_toggle, load_dataset, footer, init_session_state
from threat_detection import detect_brute_force, detect_abnormal_activity, get_suspicious_ips

st.set_page_config(page_title="SOC Dashboard | Alerts", page_icon="🚨", layout="wide",
                    initial_sidebar_state="expanded")

init_session_state()
T = get_theme()
inject_global_css()

with st.sidebar:
    render_sidebar_brand()
    render_theme_toggle()
    st.markdown("---")
    uploaded_file = st.file_uploader("📁 Upload security log CSV", type=["csv"], key="alerts_uploader")
    st.caption("If no file is uploaded, the bundled sample dataset is used.")
    st.markdown("---")
    st.caption(f"Brute-force threshold: **{st.session_state.brute_force_threshold}** (change in Settings)")

df = load_dataset(uploaded_file)

st.markdown(f"""
<div class="dash-header">
    <div>
        <p class="dash-title">🚨 Threat Detection Center</p>
        <p class="dash-subtitle">Brute-force campaigns, suspicious sources, and abnormal access patterns</p>
    </div>
</div>
""", unsafe_allow_html=True)

brute_force_df = detect_brute_force(df, failed_threshold=st.session_state.brute_force_threshold)
suspicious_ips = get_suspicious_ips(df, failed_threshold=st.session_state.brute_force_threshold)
abnormal_df = detect_abnormal_activity(df)

alert_cols = st.columns(3)
alert_kpis = [
    ("ACTIVE CAMPAIGNS", len(brute_force_df), T["danger"]),
    ("FLAGGED IPs", len(suspicious_ips), T["warning"]),
    ("ABNORMAL EVENTS", len(abnormal_df), T["accent"]),
]
for col, (label, value, color) in zip(alert_cols, alert_kpis):
    col.markdown(f"""
    <div class="kpi-card" style="--accent-color:{color};">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("###")
plot_template = T["plot_template"]
plot_font = dict(family=T["font"], color=T["text_primary"])

tab1, tab2, tab3 = st.tabs(["🎯 Brute-Force Campaigns", "🌐 Suspicious IPs", "⏰ Abnormal Activity"])

with tab1:
    if len(brute_force_df) > 0:
        left, right = st.columns([1.4, 1])
        with left:
            fig_bf = px.bar(brute_force_df, x="username", y="failed_attempts", color="risk_level",
                             color_discrete_map={"High": T["danger"], "Medium": T["warning"], "Low": T["success"]},
                             text="failed_attempts")
            fig_bf.update_traces(textposition="outside")
            fig_bf.update_layout(template=plot_template, height=360, margin=dict(t=10, b=10, l=10, r=10),
                                  paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=plot_font,
                                  xaxis_title=None, yaxis_title="Failed Attempts")
            fig_bf.update_xaxes(gridcolor=T["grid"])
            fig_bf.update_yaxes(gridcolor=T["grid"])
            st.plotly_chart(fig_bf, use_container_width=True)

        with right:
            risk_dist = brute_force_df["risk_level"].value_counts().reset_index()
            risk_dist.columns = ["risk_level", "count"]
            fig_risk = px.pie(risk_dist, names="risk_level", values="count", hole=0.5,
                               color="risk_level",
                               color_discrete_map={"High": T["danger"], "Medium": T["warning"], "Low": T["success"]})
            fig_risk.update_layout(template=plot_template, height=360, margin=dict(t=10, b=10, l=10, r=10),
                                    paper_bgcolor="rgba(0,0,0,0)", font=plot_font,
                                    legend=dict(orientation="h", y=-0.1))
            st.plotly_chart(fig_risk, use_container_width=True)

        st.markdown('<div class="section-label">Incident Timeline</div>', unsafe_allow_html=True)
        for _, row in brute_force_df.iterrows():
            badge_class = {"High": "badge-high", "Medium": "badge-medium", "Low": "badge-low"}[row["risk_level"]]
            st.markdown(f"""
            <div class="timeline-item">
                <b style="color:{T['text_primary']};">{row['username']}</b>
                <span class="badge {badge_class}" style="margin-left:8px;">{row['risk_level']} RISK</span>
                <div style="color:{T['text_secondary']};font-size:0.85rem;margin-top:3px;">
                    {row['failed_attempts']} failed login attempts detected — recommend reviewing account activity and enforcing MFA.
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("✅ No brute-force campaigns detected at the current sensitivity threshold.")

with tab2:
    if len(suspicious_ips) > 0:
        fig_ip = px.bar(suspicious_ips, x="failed_attempts", y="ip_address", orientation="h",
                         color="failed_attempts", color_continuous_scale=[T["warning"], T["danger"]])
        fig_ip.update_layout(template=plot_template, height=320, margin=dict(t=10, b=10, l=10, r=10),
                              paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=plot_font,
                              yaxis_title=None, xaxis_title="Failed Attempts", coloraxis_showscale=False)
        fig_ip.update_yaxes(categoryorder="total ascending", gridcolor=T["grid"])
        fig_ip.update_xaxes(gridcolor=T["grid"])
        st.plotly_chart(fig_ip, use_container_width=True)
        st.dataframe(suspicious_ips, use_container_width=True, hide_index=True)
    else:
        st.info("No IP addresses exceeded the failed-login threshold.")

with tab3:
    display_abnormal = abnormal_df.drop(columns=[c for c in ["lat", "lon"] if c in abnormal_df.columns])
    st.dataframe(display_abnormal.sort_values("timestamp", ascending=False), use_container_width=True,
                 height=400, hide_index=True)
    st.caption("Abnormal activity = logins during odd hours (12 AM – 5 AM) or from unusual/unrecognized locations.")

footer()
