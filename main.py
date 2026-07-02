"""
main.py
---------
SOC (Security Operations Center) Monitoring Dashboard
Major Project - Console / Script Version

Run this script to:
  1. Load security logs (Module 1)
  2. Analyze logins (Module 2)
  3. Detect threats / brute-force attempts (Module 3)
  4. Generate dashboard charts (Module 4)
  5. Print and save the SOC Security Report (Module 5)

Usage:
    python3 main.py
"""

from log_analysis import (
    load_logs,
    count_successful_logins,
    count_failed_logins,
    total_events,
    detect_suspicious_users,
    login_counts_per_user,
    failed_counts_per_user,
)
from threat_detection import detect_brute_force, detect_abnormal_activity, get_suspicious_ips
from dashboard import (
    plot_login_statistics,
    plot_failed_logins_per_user,
    plot_user_activity,
    plot_daily_login_trend,
)
from report_generator import build_recommendations, generate_report_text, save_report

LOG_FILE = "data/security_logs.csv"


def main():
    print("=" * 50)
    print(" SOC MONITORING DASHBOARD - Processing Logs...")
    print("=" * 50)

    # ---- Module 1: Log Collection ----
    df = load_logs(LOG_FILE)
    print(f"\n[Module 1] Loaded {len(df)} log records from {LOG_FILE}")

    # ---- Module 2: Log Analysis ----
    success_count = count_successful_logins(df)
    failed_count = count_failed_logins(df)
    events_total = total_events(df)
    suspicious_users = detect_suspicious_users(df, failed_threshold=3)
    print(f"[Module 2] Successful Logins: {success_count} | Failed Logins: {failed_count}")

    # ---- Module 3: Threat Detection ----
    brute_force_df = detect_brute_force(df, failed_threshold=5)
    abnormal_df = detect_abnormal_activity(df)
    suspicious_ips = get_suspicious_ips(df, failed_threshold=5)
    print(f"[Module 3] Brute-force suspects: {len(brute_force_df)} | Abnormal events: {len(abnormal_df)}")

    # ---- Module 4: Dashboard (charts) ----
    chart1 = plot_login_statistics(success_count, failed_count)
    chart2 = plot_failed_logins_per_user(failed_counts_per_user(df))
    chart3 = plot_user_activity(login_counts_per_user(df))
    chart4 = plot_daily_login_trend(df)
    print(f"[Module 4] Charts saved: {chart1}, {chart2}, {chart3}, {chart4}")

    # ---- Module 5: Reporting ----
    recommendations = build_recommendations(suspicious_users, brute_force_df)
    report_text = generate_report_text(
        total_events=events_total,
        success_count=success_count,
        failed_count=failed_count,
        suspicious_users=suspicious_users,
        recommendations=recommendations,
    )
    report_path = save_report(report_text)

    print("\n" + "=" * 50)
    print(report_text)
    print("=" * 50)
    print(f"\n[Module 5] Full report saved to: {report_path}")

    # Extra detail for project viva / explanation
    if len(brute_force_df) > 0:
        print("\n--- Brute-force Detection Detail ---")
        print(brute_force_df.to_string(index=False))

    if len(suspicious_ips) > 0:
        print("\n--- Suspicious IP Addresses ---")
        print(suspicious_ips.to_string(index=False))


if __name__ == "__main__":
    main()
