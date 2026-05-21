"""
PC Health Score Calculator
Computes an overall system health score based on key metrics.
"""

import psutil


# Score thresholds
EXCELLENT_THRESHOLD = 85
GOOD_THRESHOLD = 70
MODERATE_THRESHOLD = 50


def calculate_health_score():
    """
    Calculate overall PC health score (0-100).

    Scoring breakdown:
    - CPU load: 35% weight (lower is better)
    - RAM usage: 35% weight (lower is better)
    - Disk space remaining: 30% weight (more free space is better)
    """
    cpu_score = _get_cpu_score()
    ram_score = _get_ram_score()
    disk_score = _get_disk_score()

    # Weighted average
    overall = (cpu_score * 0.35) + (ram_score * 0.35) + (disk_score * 0.30)
    overall = round(overall, 1)

    return {
        "overall_score": overall,
        "rating": _get_rating(overall),
        "cpu_score": cpu_score,
        "ram_score": ram_score,
        "disk_score": disk_score,
        "details": _get_details(cpu_score, ram_score, disk_score),
    }


def _get_cpu_score():
    """Score based on CPU usage (lower usage = higher score)."""
    usage = psutil.cpu_percent(interval=1)
    # Invert: 0% usage = 100 score, 100% usage = 0 score
    return max(0, 100 - usage)


def _get_ram_score():
    """Score based on RAM usage (lower usage = higher score)."""
    ram = psutil.virtual_memory()
    return max(0, 100 - ram.percent)


def _get_disk_score():
    """Score based on primary disk free space."""
    try:
        for path in ["/", "C:\\"]:
            try:
                usage = psutil.disk_usage(path)
                # More free space = higher score
                return max(0, 100 - usage.percent)
            except (FileNotFoundError, OSError):
                continue
    except Exception:
        pass
    return 50  # Default middle score if unable to read


def _get_rating(score):
    """Convert numeric score to human-readable rating."""
    if score >= EXCELLENT_THRESHOLD:
        return "Excellent"
    elif score >= GOOD_THRESHOLD:
        return "Good"
    elif score >= MODERATE_THRESHOLD:
        return "Moderate"
    else:
        return "Poor"


def _get_details(cpu_score, ram_score, disk_score):
    """Generate helpful detail messages based on individual scores."""
    details = []

    if cpu_score < 50:
        details.append("High CPU usage detected. Consider closing unused applications.")
    if ram_score < 40:
        details.append("RAM is running low. Close memory-heavy programs.")
    if disk_score < 30:
        details.append("Disk space is critically low. Free up storage.")
    elif disk_score < 50:
        details.append("Disk space is getting low. Consider cleanup.")

    if not details:
        details.append("System is running smoothly. No issues detected.")

    return details
