"""
Network diagnostics — connectivity check, local IP, ping, speed test.
"""

import socket
import subprocess
import platform


def check_internet_connection():
    """Try connecting to a few DNS servers to verify internet access."""
    targets = [
        ("8.8.8.8", 53),        # Google DNS
        ("1.1.1.1", 53),        # Cloudflare
        ("208.67.222.222", 53),  # OpenDNS
    ]
    for host, port in targets:
        try:
            s = socket.create_connection((host, port), timeout=3)
            s.close()
            return {"connected": True, "message": "Internet connection active."}
        except (socket.timeout, OSError):
            continue

    return {"connected": False, "message": "No internet connection detected."}


def get_local_ip():
    """Get local IP by connecting to external address (doesn't send data)."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except (socket.error, OSError):
        return "Unable to determine"


def get_hostname():
    return socket.gethostname()


def ping_host(host="8.8.8.8", count=4):
    """Run ping command and return output."""
    system = platform.system()
    flag = "-n" if system == "Windows" else "-c"
    cmd = ["ping", flag, str(count), host]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        if result.returncode == 0:
            return {
                "success": True,
                "host": host,
                "output": result.stdout,
                "message": f"Ping to {host} successful",
            }
        return {
            "success": False,
            "host": host,
            "output": result.stderr or result.stdout,
            "message": f"Ping to {host} failed",
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "host": host, "output": "", "message": "Ping timed out"}
    except FileNotFoundError:
        return {"success": False, "host": host, "output": "", "message": "Ping not available"}


def get_network_summary():
    """Quick summary for the dashboard / report."""
    conn = check_internet_connection()
    return {
        "connected": conn["connected"],
        "status_message": conn["message"],
        "local_ip": get_local_ip(),
        "hostname": get_hostname(),
    }


def run_speed_test():
    """
    Uses speedtest-cli if installed. This can take 20-30 seconds.
    Returns Mbps for download/upload.
    """
    try:
        import speedtest
        st = speedtest.Speedtest()
        st.get_best_server()

        dl = st.download() / 1_000_000
        ul = st.upload() / 1_000_000
        ping = st.results.ping

        return {
            "success": True,
            "download_mbps": round(dl, 2),
            "upload_mbps": round(ul, 2),
            "ping_ms": round(ping, 1),
            "server": st.results.server.get("name", "Unknown"),
        }
    except ImportError:
        return {"success": False, "message": "speedtest-cli not installed. Run: pip install speedtest-cli"}
    except Exception as e:
        return {"success": False, "message": f"Speed test failed: {e}"}
