"""
Module 1 - Log Collection
Module 2 - Log Analysis
--------------------------
Reads security logs from a CSV file into a Pandas DataFrame,
and provides analysis functions: counting successful/failed logins
and detecting suspicious users based on failed-login frequency.
"""

import pandas as pd


def load_logs(csv_path: str) -> pd.DataFrame:
    """
    Module 1 - Log Collection
    Reads log data from a CSV file and stores it in a Pandas DataFrame.
    """
    df = pd.read_csv(csv_path, parse_dates=["timestamp"])
    return df


def count_successful_logins(df: pd.DataFrame) -> int:
    """Module 2 - Log Analysis: Count successful logins."""
    return int((df["event_type"] == "Login Success").sum())


def count_failed_logins(df: pd.DataFrame) -> int:
    """Module 2 - Log Analysis: Count failed logins."""
    return int((df["event_type"] == "Login Failed").sum())


def total_events(df: pd.DataFrame) -> int:
    """Module 2 - Log Analysis: Total number of log events."""
    return len(df)


def detect_suspicious_users(df: pd.DataFrame, failed_threshold: int = 5, window_hours: int = 24) -> list:
    """
    Module 2 - Log Analysis: Detect suspicious users.

    A user is flagged suspicious if they accumulate `failed_threshold` or more
    failed login attempts within any rolling `window_hours` window. This is a
    burst-based check (similar to real SOC tooling) rather than a raw lifetime
    count, so it scales correctly across datasets spanning many months and
    doesn't falsely flag normal users whose occasional mistyped passwords are
    simply spread out over a long history.
    """
    failed_df = df[df["event_type"] == "Login Failed"].copy()
    if failed_df.empty:
        return []

    failed_df["timestamp"] = pd.to_datetime(failed_df["timestamp"])
    suspicious = []
    burst_counts = {}

    for user, group in failed_df.groupby("username"):
        times = group["timestamp"].sort_values().to_numpy()
        max_in_window = 1
        start = 0
        for end in range(len(times)):
            while times[end] - times[start] > pd.Timedelta(hours=window_hours):
                start += 1
            max_in_window = max(max_in_window, end - start + 1)
        burst_counts[user] = max_in_window
        if max_in_window >= failed_threshold:
            suspicious.append(user)

    suspicious.sort(key=lambda u: burst_counts[u], reverse=True)
    return suspicious


def login_counts_per_user(df: pd.DataFrame) -> pd.Series:
    """Helper: total login attempts (success + failed) per user."""
    return df.groupby("username").size().sort_values(ascending=False)


def failed_counts_per_user(df: pd.DataFrame) -> pd.Series:
    """Helper: failed login attempts per user."""
    failed_df = df[df["event_type"] == "Login Failed"]
    return failed_df.groupby("username").size().sort_values(ascending=False)
