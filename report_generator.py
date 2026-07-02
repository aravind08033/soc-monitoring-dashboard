"""
Module 5 - Reporting
------------------------
Generates the incident summary report in the exact format
specified in the project description, plus a saved text file
report for submission purposes.
"""

import os
from datetime import datetime

OUTPUT_DIR = "output"


def build_recommendations(suspicious_users: list, brute_force_df) -> list:
    """Generate recommendation lines based on detected threats."""
    recommendations = []
    if suspicious_users or len(brute_force_df) > 0:
        recommendations.append("Enable MFA")
        recommendations.append("Review user accounts")
    if len(brute_force_df) > 0:
        recommendations.append("Block suspicious IP addresses")
        recommendations.append("Lock accounts after repeated failed attempts")
    if not recommendations:
        recommendations.append("No immediate action required - continue routine monitoring")
    return recommendations


def generate_report_text(total_events: int, success_count: int, failed_count: int,
                          suspicious_users: list, recommendations: list) -> str:
    """
    Builds the report text in the exact format shown in the
    project description's 'Expected Output' section.
    """
    lines = []
    lines.append("SOC SECURITY REPORT")
    lines.append("")
    lines.append(f"Total Events: {total_events}")
    lines.append("")
    lines.append(f"Successful Logins: {success_count}")
    lines.append("")
    lines.append(f"Failed Logins: {failed_count}")
    lines.append("")
    lines.append("Suspicious Users:")
    if suspicious_users:
        for user in suspicious_users:
            lines.append(user)
    else:
        lines.append("None detected")
    lines.append("")
    lines.append("Recommendation:")
    for rec in recommendations:
        lines.append(rec)
    return "\n".join(lines)


def save_report(report_text: str, filename: str = "soc_security_report.txt") -> str:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w") as f:
        f.write(report_text)
        f.write(f"\n\nGenerated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    return path
