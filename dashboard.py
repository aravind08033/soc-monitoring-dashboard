"""
Module 4 - Dashboard
-----------------------
Generates visualizations for the SOC dashboard:
  - Login statistics (success vs failed) pie/bar chart
  - Failed login graph per user
  - User activity chart (total logins per user)
Saves each chart as a PNG image in the output/ folder.
"""

import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # safe for headless / server environments
import matplotlib.pyplot as plt

OUTPUT_DIR = "output"


def _ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def plot_login_statistics(success_count: int, failed_count: int):
    """Module 4: Login statistics - Success vs Failed (bar chart)."""
    _ensure_output_dir()
    fig, ax = plt.subplots(figsize=(6, 4.5))
    labels = ["Successful Logins", "Failed Logins"]
    values = [success_count, failed_count]
    colors = ["#2E8B57", "#C0392B"]

    bars = ax.bar(labels, values, color=colors)
    ax.set_title("Login Statistics", fontsize=14, fontweight="bold")
    ax.set_ylabel("Number of Events")
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, val + 0.5, str(val),
                 ha="center", fontweight="bold")

    fig.tight_layout()
    path = os.path.join(OUTPUT_DIR, "login_statistics.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def plot_failed_logins_per_user(failed_counts: pd.Series, top_n: int = 10):
    """Module 4: Failed login graph - failed attempts per user."""
    _ensure_output_dir()
    data = failed_counts.head(top_n)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.barh(data.index[::-1], data.values[::-1], color="#C0392B")
    ax.set_title("Failed Login Attempts per User", fontsize=14, fontweight="bold")
    ax.set_xlabel("Failed Attempts")
    fig.tight_layout()
    path = os.path.join(OUTPUT_DIR, "failed_logins_per_user.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def plot_user_activity(login_counts: pd.Series, top_n: int = 10):
    """Module 4: User activity chart - total login attempts per user."""
    _ensure_output_dir()
    data = login_counts.head(top_n)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.barh(data.index[::-1], data.values[::-1], color="#2E75B6")
    ax.set_title("User Activity (Total Login Attempts)", fontsize=14, fontweight="bold")
    ax.set_xlabel("Total Attempts")
    fig.tight_layout()
    path = os.path.join(OUTPUT_DIR, "user_activity.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def plot_daily_login_trend(df: pd.DataFrame):
    """Module 4: Login trend over time (daily event count)."""
    _ensure_output_dir()
    daily = df.copy()
    daily["date"] = daily["timestamp"].dt.date
    trend = daily.groupby(["date", "event_type"]).size().unstack(fill_value=0)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    trend.plot(ax=ax, marker="o")
    ax.set_title("Daily Login Trend", fontsize=14, fontweight="bold")
    ax.set_ylabel("Number of Events")
    ax.set_xlabel("Date")
    fig.tight_layout()
    path = os.path.join(OUTPUT_DIR, "daily_login_trend.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path
