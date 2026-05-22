"""
Health score calculator.
Weighted average of CPU/RAM/Disk (inverted usage = score).
Simple but gives a decent quick read on system state.
"""

import psutil


# thresholds for rating labels
EXCELLENT = 85
GOOD = 70
MODERATE = 50


def calculate_health_score():
    """
    Returns dict with overall score (0-100), rating string,
    individual component scores, and any recommendations.
    """
    cpu = _score_cpu()
    ram = _score_ram()
    disk = _score_disk()

    # weighted: CPU 35%, RAM 35%, Disk 30%
    overall = round((cpu * 0.35) + (ram * 0.35) + (disk * 0.30), 1)

    return {
        "overall_score": overall,
        "rating": _rating_label(overall),
        "cpu_score": cpu,
        "ram_score": ram,
        "disk_score": disk,
        "details": _build_recommendations(cpu, ram, disk),
    }


def _score_cpu():
    """Lower CPU usage = higher score."""
    usage = psutil.cpu_percent(interval=1)
    return max(0, 100 - usage)


def _score_ram():
    """Lower RAM usage = higher score."""
    return max(0, 100 - psutil.virtual_memory().percent)


def _score_disk():
    """More free disk = higher score. Tries / then C:\\."""
    for path in ["/", "C:\\"]:
        try:
            usage = psutil.disk_usage(path)
            return max(0, 100 - usage.percent)
        except (FileNotFoundError, OSError):
            continue
    return 50  # can't determine, give neutral


def _rating_label(score):
    if score >= EXCELLENT:
        return "Excellent"
    elif score >= GOOD:
        return "Good"
    elif score >= MODERATE:
        return "Moderate"
    return "Poor"


def _build_recommendations(cpu, ram, disk):
    """Give some useful tips based on what's struggling."""
    tips = []
    if cpu < 50:
        tips.append("CPU is under heavy load — try closing unused programs.")
    if ram < 40:
        tips.append("RAM is running low. Close memory-heavy apps or consider upgrading.")
    if disk < 30:
        tips.append("Disk space is critically low! Free up storage soon.")
    elif disk < 50:
        tips.append("Disk space getting low — might want to run a cleanup.")

    if not tips:
        tips.append("Everything looks good. No issues detected.")
    return tips
