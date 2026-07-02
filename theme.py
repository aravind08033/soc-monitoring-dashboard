"""
theme.py
----------
Shared theme definitions, global CSS, and common data-loading helpers
used across every page of the SOC Monitoring Dashboard multi-page app.
"""

import streamlit as st
import pandas as pd
import numpy as np

THEMES = {
    "dark": {
        "bg": "#0a0e14",
        "bg_secondary": "#10151f",
        "card_bg": "#131927",
        "card_border": "#1f2937",
        "text_primary": "#e6edf3",
        "text_secondary": "#8b949e",
        "accent": "#00ff9d",
        "accent_glow": "rgba(0, 255, 157, 0.35)",
        "danger": "#ff3b5c",
        "danger_glow": "rgba(255, 59, 92, 0.35)",
        "warning": "#ffb020",
        "success": "#00ff9d",
        "grid": "#1f2937",
        "font": "'JetBrains Mono', 'Courier New', monospace",
        "plot_template": "plotly_dark",
    },
    "light": {
        "bg": "#f4f6fb",
        "bg_secondary": "#ffffff",
        "card_bg": "#ffffff",
        "card_border": "#e3e8f0",
        "text_primary": "#1a1f36",
        "text_secondary": "#6b7280",
        "accent": "#2563eb",
        "accent_glow": "rgba(37, 99, 235, 0.18)",
        "danger": "#dc2626",
        "danger_glow": "rgba(220, 38, 38, 0.18)",
        "warning": "#d97706",
        "success": "#059669",
        "grid": "#e5e9f2",
        "font": "'Inter', 'Segoe UI', sans-serif",
        "plot_template": "plotly_white",
    },
}


def init_session_state():
    if "theme" not in st.session_state:
        st.session_state.theme = "dark"
    if "live_mode" not in st.session_state:
        st.session_state.live_mode = False
    if "alert_feed" not in st.session_state:
        st.session_state.alert_feed = []
    if "failed_threshold" not in st.session_state:
        st.session_state.failed_threshold = 3
    if "brute_force_threshold" not in st.session_state:
        st.session_state.brute_force_threshold = 5
    if "date_range_days" not in st.session_state:
        st.session_state.date_range_days = 182


def get_theme():
    init_session_state()
    return THEMES[st.session_state.theme]


def inject_global_css():
    """Injects the global look-and-feel CSS. Call once per page, near the top."""
    T = get_theme()
    css_html = f"""
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700;800&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
    @keyframes blink {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.35; }}
    }}
    @keyframes slideIn {{
        from {{ opacity: 0; transform: translateX(-12px); }}
        to {{ opacity: 1; transform: translateX(0); }}
    }}
    @keyframes countUp {{
        from {{ opacity: 0; transform: translateY(6px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    @keyframes fadeIn {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
    }}

    html, body, [class*="css"] {{
        font-family: {T['font']};
    }}
    .stApp {{
        background: {T['bg']};
    }}
    section[data-testid="stSidebar"] {{
        background: {T['bg_secondary']};
        border-right: 1px solid {T['card_border']};
    }}
    #MainMenu, footer, header {{visibility: hidden;}}

    .dash-header {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.5rem 0 1rem 0;
        animation: fadeIn 0.4s ease-out;
    }}
    .dash-title {{
        font-size: 2rem;
        font-weight: 800;
        color: {T['text_primary']};
        margin: 0;
        letter-spacing: -0.02em;
    }}
    .dash-subtitle {{
        font-size: 0.95rem;
        color: {T['text_secondary']};
        margin-top: 2px;
    }}
    .live-badge {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: {T['danger_glow']};
        color: {T['danger']};
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        border: 1px solid {T['danger']};
    }}
    .live-dot {{
        width: 8px; height: 8px;
        border-radius: 50%;
        background: {T['danger']};
        animation: blink 1.4s infinite;
    }}

    .kpi-card {{
        background: {T['card_bg']};
        border: 1px solid {T['card_border']};
        border-radius: 14px;
        padding: 1.1rem 1.3rem;
        animation: countUp 0.5s ease-out;
        position: relative;
        overflow: hidden;
        transition: transform 0.15s ease;
    }}
    .kpi-card:hover {{
        transform: translateY(-2px);
    }}
    .kpi-card::before {{
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: var(--accent-color, {T['accent']});
    }}
    .kpi-label {{
        color: {T['text_secondary']};
        font-size: 0.78rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 6px;
    }}
    .kpi-value {{
        color: {T['text_primary']};
        font-size: 2.1rem;
        font-weight: 800;
        line-height: 1;
    }}
    .kpi-delta {{
        font-size: 0.8rem;
        font-weight: 600;
        margin-top: 6px;
    }}

    .alert-ticker {{
        background: {T['card_bg']};
        border: 1px solid {T['card_border']};
        border-left: 4px solid {T['danger']};
        border-radius: 10px;
        padding: 10px 16px;
        margin-bottom: 6px;
        animation: slideIn 0.4s ease-out;
        font-size: 0.85rem;
        color: {T['text_primary']};
    }}
    .alert-ticker .ts {{
        color: {T['text_secondary']};
        font-size: 0.75rem;
        margin-right: 8px;
    }}
    .alert-ticker.high {{ border-left-color: {T['danger']}; }}
    .alert-ticker.medium {{ border-left-color: {T['warning']}; }}
    .alert-ticker.low {{ border-left-color: {T['success']}; }}

    .section-label {{
        color: {T['text_secondary']};
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin: 1.4rem 0 0.6rem 0;
    }}

    .info-card {{
        background: {T['card_bg']};
        border: 1px solid {T['card_border']};
        border-radius: 14px;
        padding: 1.4rem;
        animation: fadeIn 0.5s ease-out;
    }}

    div[data-testid="stMetric"] {{
        background: {T['card_bg']};
        border: 1px solid {T['card_border']};
        border-radius: 12px;
        padding: 12px 16px;
    }}

    .stTabs [data-baseweb="tab-list"] {{
        gap: 4px;
    }}
    .stTabs [data-baseweb="tab"] {{
        background: {T['card_bg']};
        border-radius: 8px 8px 0 0;
        color: {T['text_secondary']};
        font-weight: 600;
    }}
    .stTabs [aria-selected="true"] {{
        color: {T['accent']} !important;
        border-bottom: 2px solid {T['accent']};
    }}

    div.stButton > button {{
        border-radius: 8px;
        font-weight: 600;
    }}

    .footer-bar {{
        text-align: center;
        color: {T['text_secondary']};
        font-size: 0.8rem;
        padding: 1.2rem 0 0.4rem 0;
        border-top: 1px solid {T['card_border']};
        margin-top: 1.5rem;
    }}

    .badge {{
        display: inline-block;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.03em;
    }}
    .badge-high {{ background: {T['danger_glow']}; color: {T['danger']}; }}
    .badge-medium {{ background: rgba(255,176,32,0.18); color: {T['warning']}; }}
    .badge-low {{ background: rgba(0,255,157,0.18); color: {T['success']}; }}

    .timeline-item {{
        border-left: 2px solid {T['card_border']};
        padding-left: 16px;
        padding-bottom: 16px;
        position: relative;
    }}
    .timeline-item::before {{
        content: '';
        position: absolute;
        left: -5px; top: 2px;
        width: 8px; height: 8px;
        border-radius: 50%;
        background: {T['accent']};
    }}
    </style>
    """
    try:
        st.html(css_html)
    except AttributeError:
        st.markdown(css_html, unsafe_allow_html=True)


def render_sidebar_brand():
    T = get_theme()
    st.markdown(f"""
    <div style="display:flex;align-items:flex-start;gap:10px;margin-bottom:4px;">
        <span style="font-size:1.8rem;line-height:1;">🛡️</span>
        <div>
            <div style="font-weight:800;font-size:1rem;color:{T['text_primary']};line-height:1.25;">Security Operations Center (SOC) Monitoring Dashboard</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")


def render_theme_toggle():
    theme_choice = st.radio("🎨 Theme", ["Dark (Cyber)", "Light (Corporate)"],
                             index=0 if st.session_state.theme == "dark" else 1, horizontal=True,
                             key="theme_radio")
    new_theme = "dark" if theme_choice.startswith("Dark") else "light"
    if new_theme != st.session_state.theme:
        st.session_state.theme = new_theme
        st.rerun()


@st.cache_data(show_spinner=False)
def _load_csv(path):
    df = pd.read_csv(path, parse_dates=["timestamp"])
    return df


def load_dataset(uploaded_file=None):
    """Loads the dataset either from an uploaded file or the bundled sample CSV."""
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, parse_dates=["timestamp"])
        if "lat" not in df.columns:
            df["lat"] = np.nan
            df["lon"] = np.nan
        if "severity" not in df.columns:
            df["severity"] = ""
    else:
        df = _load_csv("data/security_logs.csv")
    return df


def footer():
    st.markdown("""
    <div class="footer-bar">
        SOC Monitoring Dashboard · Major Project · Built with Python, Pandas, Plotly & Streamlit
    </div>
    """, unsafe_allow_html=True)
