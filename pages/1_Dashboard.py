"""
pages/1_Dashboard.py
-----------------------
Main analytics dashboard: KPIs, risk gauge, login trend, global map,
brute-force detection, user activity, and calendar heatmap.
"""

import random
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from datetime import datetime

from theme import (
    get_theme, inject_global_css, render_sidebar_brand, render_theme_toggle,
    load_dataset, footer, init_session_state,
)
from log_analysis import (
    count_successful_logins, count_failed_logins, total_events,
    detect_suspicious_users, login_counts_per_user, failed_counts_per_user,
)
from threat_detection import detect_brute_force, detect_abnormal_activity, get_suspicious_ips

try:
    from streamlit_autorefresh import st_autorefresh
    AUTOREFRESH_AVAILABLE = True
except ImportError:
    AUTOREFRESH_AVAILABLE = False

st.set_page_config(page_title="SOC Dashboard | Dashboard", page_icon="📊", layout="wide",
                    initial_sidebar_state="expanded")

init_session_state()
T = get_theme()
inject_global_css()

with st.sidebar:
    render_sidebar_brand()
    render_theme_toggle()
    st.markdown("---")
    st.session_state.live_mode = st.toggle("🔴 Live Monitoring Mode", value=st.session_state.live_mode)
    if st.session_state.live_mode and AUTOREFRESH_AVAILABLE:
        st_autorefresh(interval=4000, key="live_refresh_dash")
        st.caption("Auto-refreshing every 4s")
    st.markdown("---")
    uploaded_file = st.file_uploader("📁 Upload security log CSV", type=["csv"])
    st.caption("If no file is uploaded, the bundled sample dataset is used.")
    st.markdown("---")
    st.caption(f"Filters set on the Settings page apply here.")
    st.caption(f"Suspicious threshold: **{st.session_state.failed_threshold}** failed logins")
    st.caption(f"Brute-force threshold: **{st.session_state.brute_force_threshold}** failed logins")

df = load_dataset(uploaded_file)

if st.session_state.live_mode:
    sim_users = ["admin", "root", "test_user", "rakesh.kumar", "sneha.reddy"]
    sim_event = random.choice(["Login Failed", "Login Failed", "Login Success"])
    sim_user = random.choice(sim_users)
    ts_now = datetime.now().strftime("%H:%M:%S")
    msg = f"{sim_user} → {sim_event}"
    st.session_state.alert_feed.insert(0, {"ts": ts_now, "msg": msg, "level": "high" if sim_event == "Login Failed" else "low"})
    st.session_state.alert_feed = st.session_state.alert_feed[:6]

live_badge = """<span class="live-badge"><span class="live-dot"></span> LIVE</span>""" if st.session_state.live_mode else ""
st.markdown(f"""
<div class="dash-header">
    <div>
        <p class="dash-title">📊 Monitoring Dashboard</p>
        <p class="dash-subtitle">Real-time visibility into login activity, threats, and risk across the network</p>
    </div>
    <div>{live_badge}</div>
</div>
""", unsafe_allow_html=True)

success_count = count_successful_logins(df)
failed_count = count_failed_logins(df)
events_total = total_events(df)
suspicious_users = detect_suspicious_users(df, failed_threshold=st.session_state.failed_threshold)
brute_force_df = detect_brute_force(df, failed_threshold=st.session_state.brute_force_threshold)
risk_score = min(100, int((failed_count / max(events_total, 1)) * 140 + len(brute_force_df) * 4))

kpi_cols = st.columns(4)
kpi_data = [
    ("TOTAL EVENTS", f"{events_total:,}", T["accent"], None),
    ("SUCCESSFUL LOGINS", f"{success_count:,}", T["success"], f"{success_count/events_total*100:.0f}% of total"),
    ("FAILED LOGINS", f"{failed_count:,}", T["danger"], f"{failed_count/events_total*100:.0f}% of total"),
    ("SUSPICIOUS USERS", len(suspicious_users), T["warning"], None),
]
for col, (label, value, color, delta) in zip(kpi_cols, kpi_data):
    delta_html = f'<div class="kpi-delta" style="color:{T["text_secondary"]};">{delta}</div>' if delta else ""
    col.markdown(f"""
    <div class="kpi-card" style="--accent-color:{color};">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

st.markdown("###")

if st.session_state.live_mode and st.session_state.alert_feed:
    st.markdown('<div class="section-label">⚡ Live Alert Feed</div>', unsafe_allow_html=True)
    for alert in st.session_state.alert_feed:
        st.markdown(f"""
        <div class="alert-ticker {alert['level']}">
            <span class="ts">{alert['ts']}</span>{alert['msg']}
        </div>
        """, unsafe_allow_html=True)
    st.markdown("###")

tab1, tab2, tab3 = st.tabs(["📈 Overview", "🌍 Threat Map", "👤 User Activity"])
plot_template = T["plot_template"]
plot_font = dict(family=T["font"], color=T["text_primary"])

with tab1:
    c1, c2 = st.columns([1, 1.4])
    with c1:
        st.markdown('<div class="section-label">Risk Score</div>', unsafe_allow_html=True)
        gauge_color = T["success"] if risk_score < 35 else (T["warning"] if risk_score < 65 else T["danger"])
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number", value=risk_score,
            number={"suffix": " / 100", "font": {"size": 36, "color": T["text_primary"]}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": T["text_secondary"]},
                "bar": {"color": gauge_color, "thickness": 0.3},
                "bgcolor": T["card_bg"], "borderwidth": 0,
                "steps": [
                    {"range": [0, 35], "color": "rgba(0,255,157,0.12)"},
                    {"range": [35, 65], "color": "rgba(255,176,32,0.12)"},
                    {"range": [65, 100], "color": "rgba(255,59,92,0.12)"},
                ],
            },
        ))
        fig_gauge.update_layout(height=240, margin=dict(t=10, b=10, l=20, r=20),
                                 paper_bgcolor="rgba(0,0,0,0)", font=plot_font)
        st.plotly_chart(fig_gauge, use_container_width=True)

        fig_pie = px.pie(
            names=["Successful", "Failed"], values=[success_count, failed_count],
            color=["Successful", "Failed"],
            color_discrete_map={"Successful": T["success"], "Failed": T["danger"]}, hole=0.55,
        )
        fig_pie.update_layout(template=plot_template, height=220, margin=dict(t=10, b=10, l=10, r=10),
                               paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=plot_font,
                               legend=dict(orientation="h", y=-0.1))
        st.plotly_chart(fig_pie, use_container_width=True)

    with c2:
        st.markdown('<div class="section-label">Login Trend Over Time</div>', unsafe_allow_html=True)
        daily = df.copy()
        daily["date"] = pd.to_datetime(daily["timestamp"]).dt.date
        trend = daily.groupby(["date", "event_type"]).size().reset_index(name="count")
        fig_trend = px.area(
            trend, x="date", y="count", color="event_type", markers=False,
            color_discrete_map={"Login Success": T["success"], "Login Failed": T["danger"]},
        )
        fig_trend.update_layout(template=plot_template, height=260, margin=dict(t=10, b=10, l=10, r=10),
                                 paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=plot_font,
                                 legend=dict(orientation="h", y=1.15), xaxis_title=None, yaxis_title="Events")
        fig_trend.update_xaxes(gridcolor=T["grid"])
        fig_trend.update_yaxes(gridcolor=T["grid"])
        st.plotly_chart(fig_trend, use_container_width=True)

        st.markdown('<div class="section-label">Weekly Pattern (Heatmap)</div>', unsafe_allow_html=True)
        wk = df.copy()
        wk["weekday"] = pd.to_datetime(wk["timestamp"]).dt.day_name()
        wk["hour"] = pd.to_datetime(wk["timestamp"]).dt.hour
        weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        heat = wk.groupby(["weekday", "hour"]).size().reset_index(name="count")
        heat_pivot = heat.pivot(index="weekday", columns="hour", values="count").reindex(weekday_order).fillna(0)
        fig_heat = px.imshow(
            heat_pivot, color_continuous_scale=[T["card_bg"], T["accent"]], aspect="auto",
            labels=dict(x="Hour of Day", y="", color="Events"),
        )
        fig_heat.update_layout(template=plot_template, height=220, margin=dict(t=10, b=10, l=10, r=10),
                                paper_bgcolor="rgba(0,0,0,0)", font=plot_font, coloraxis_showscale=False)
        st.plotly_chart(fig_heat, use_container_width=True)

with tab2:
    st.markdown('<div class="section-label">Global Login & Attack Map</div>', unsafe_allow_html=True)
    if "lat" in df.columns and df["lat"].notna().any():
        map_df = df.dropna(subset=["lat", "lon"]).copy()
        map_df = map_df[(map_df["lat"] != 0) | (map_df["lon"] != 0)]
        if len(map_df) > 0:
            map_agg = map_df.groupby(["location", "lat", "lon", "event_type"]).size().reset_index(name="count")
            fig_map = px.scatter_geo(
                map_agg, lat="lat", lon="lon", size="count", color="event_type",
                hover_name="location", projection="natural earth", size_max=35,
                color_discrete_map={"Login Success": T["success"], "Login Failed": T["danger"]},
            )
            fig_map.update_layout(template=plot_template, height=420, margin=dict(t=10, b=10, l=10, r=10),
                                   paper_bgcolor="rgba(0,0,0,0)", font=plot_font,
                                   geo=dict(bgcolor="rgba(0,0,0,0)", landcolor=T["card_border"],
                                            showcountries=True, countrycolor=T["grid"]),
                                   legend=dict(orientation="h", y=-0.05))
            st.plotly_chart(fig_map, use_container_width=True)

    st.markdown('<div class="section-label">Events by Location</div>', unsafe_allow_html=True)
    loc_counts = df["location"].value_counts().reset_index()
    loc_counts.columns = ["location", "count"]
    fig_loc = px.bar(loc_counts, x="location", y="count", color="count",
                      color_continuous_scale=[T["card_border"], T["danger"]])
    fig_loc.update_layout(template=plot_template, height=280, margin=dict(t=10, b=10, l=10, r=10),
                           paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=plot_font,
                           coloraxis_showscale=False, xaxis_title=None)
    fig_loc.update_xaxes(gridcolor=T["grid"])
    fig_loc.update_yaxes(gridcolor=T["grid"])
    st.plotly_chart(fig_loc, use_container_width=True)

with tab3:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="section-label">Top 10 Most Active Users</div>', unsafe_allow_html=True)
        login_counts = login_counts_per_user(df).reset_index()
        login_counts.columns = ["username", "total_logins"]
        fig_active = px.bar(login_counts.head(10), x="total_logins", y="username", orientation="h",
                             color="total_logins", color_continuous_scale=[T["card_border"], T["accent"]])
        fig_active.update_layout(template=plot_template, height=340, margin=dict(t=10, b=10, l=10, r=10),
                                  paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=plot_font,
                                  yaxis_title=None, xaxis_title=None, coloraxis_showscale=False)
        fig_active.update_yaxes(categoryorder="total ascending", gridcolor=T["grid"])
        fig_active.update_xaxes(gridcolor=T["grid"])
        st.plotly_chart(fig_active, use_container_width=True)

    with c2:
        st.markdown('<div class="section-label">Top 10 Users by Failed Logins</div>', unsafe_allow_html=True)
        fc = failed_counts_per_user(df).reset_index()
        fc.columns = ["username", "failed_logins"]
        fig_failed = px.bar(fc.head(10), x="failed_logins", y="username", orientation="h",
                             color="failed_logins", color_continuous_scale=[T["card_border"], T["danger"]])
        fig_failed.update_layout(template=plot_template, height=340, margin=dict(t=10, b=10, l=10, r=10),
                                  paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=plot_font,
                                  yaxis_title=None, xaxis_title=None, coloraxis_showscale=False)
        fig_failed.update_yaxes(categoryorder="total ascending", gridcolor=T["grid"])
        fig_failed.update_xaxes(gridcolor=T["grid"])
        st.plotly_chart(fig_failed, use_container_width=True)

    st.markdown('<div class="section-label">Raw Log Data</div>', unsafe_allow_html=True)
    display_cols = [c for c in df.columns if c not in ("lat", "lon")]
    st.dataframe(df[display_cols].sort_values("timestamp", ascending=False), use_container_width=True,
                 height=300, hide_index=True)

footer()
