"""
Module 3 - Threat Detection
-----------------------------
Identifies multiple failed login attempts (brute-force pattern)
and detects abnormal login activity (e.g. logins from unusual
locations, or odd-hour login attempts).
"""

import pandas as pd


def detect_brute_force(df: pd.DataFrame, failed_threshold: int = 5) -> pd.DataFrame:
    """
    Identify users with repeated failed login attempts that suggest
    a brute-force attack. Returns a DataFrame summary:
    username, failed_attempts, risk_level.
    """
    failed_df = df[df["event_type"] == "Login Failed"]
    counts = failed_df.groupby("username").size().reset_index(name="failed_attempts")
    flagged = counts[counts["failed_attempts"] >= failed_threshold].copy()

    def risk_level(n):
        if n >= 8:
            return "High"
        elif n >= 5:
            return "Medium"
        return "Low"

    flagged["risk_level"] = flagged["failed_attempts"].apply(risk_level)
    flagged = flagged.sort_values("failed_attempts", ascending=False).reset_index(drop=True)
    return flagged


def detect_abnormal_activity(df: pd.DataFrame, odd_hour_start: int = 0, odd_hour_end: int = 5) -> pd.DataFrame:
    """
    Detect abnormal login activity:
      - Logins occurring during odd hours (default: 12 AM - 5 AM)
      - Logins from known suspicious / unknown locations
    Returns the filtered DataFrame of abnormal events.
    """
    df = df.copy()
    df["hour"] = df["timestamp"].dt.hour

    odd_hour_mask = (df["hour"] >= odd_hour_start) & (df["hour"] <= odd_hour_end)
    unusual_location_mask = df["location"].isin(["Unknown", "Moscow, RU", "Lagos, NG", "Bucharest, RO"])

    abnormal = df[odd_hour_mask | unusual_location_mask]
    return abnormal.drop(columns=["hour"])


def get_suspicious_ips(df: pd.DataFrame, failed_threshold: int = 5) -> pd.DataFrame:
    """
    Identify IP addresses associated with a high number of failed
    login attempts - useful for blocking at the firewall level.
    """
    failed_df = df[df["event_type"] == "Login Failed"]
    ip_counts = failed_df.groupby("ip_address").size().reset_index(name="failed_attempts")
    suspicious_ips = ip_counts[ip_counts["failed_attempts"] >= failed_threshold]
    return suspicious_ips.sort_values("failed_attempts", ascending=False).reset_index(drop=True)
