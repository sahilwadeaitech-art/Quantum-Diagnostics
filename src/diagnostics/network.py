"""
Network Diagnostics
Provides network connectivity checks, IP info, and ping tests.
"""

import socket
import subprocess
import platform


def check_internet_connection():
    """Check if the system has an active internet connection."""
    test_hosts = [
        ("8.8.8.8", 53),        # Google DNS
        ("1.1.1.1", 53),        # Cloudflare DNS
        ("208.67.222.222", 53),  # OpenDNS
    ]

    for host, port in test_hosts:
        try:
            sock = socket.create_connection((host, port), timeout=3)
            sock.close()
            return {"connected": True, "message": "Internet connection is active."}
        except (socket.timeout, OSError):
            continue

    return {"connected": False, "message": "No internet connection detected."}


def get_local_ip():
    """Get the local IP address of the machine."""
    try:
        # Create a dummy connection to find the local IP
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        local_ip = sock.getsockname()[0]
        sock.close()
        return local_ip
    except (socket.error, OSError):
        return "Unable to determine"


def get_hostname():
    """Get the system hostname."""
    return socket.gethostname()


def ping_host(host="8.8.8.8", count=4):
    """
    Ping a host and return results.

    Args:
        host: IP address or hostname to ping
        count: Number of ping packets to send
    """
    system = platform.system()

    # Build ping command based on OS
    if system == "Windows":
        cmd = ["ping", "-n", str(count), host]
    else:
        cmd = ["ping", "-c", str(count), host]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=15,
        )

        if result.returncode == 0:
            return {
                "success": True,
                "host": host,
                "output": result.stdout,
                "message": f"Successfully pinged {host}",
            }
        else:
            return {
                "success": False,
                "host": host,
                "output": result.stderr or result.stdout,
                "message": f"Ping to {host} failed",
            }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "host": host,
            "output": "",
            "message": "Ping timed out",
        }
    except FileNotFoundError:
        return {
            "success": False,
            "host": host,
            "output": "",
            "message": "Ping command not found",
        }


def get_network_summary():
    """Get a complete network diagnostic summary."""
    connection = check_internet_connection()
    return {
        "connected": connection["connected"],
        "status_message": connection["message"],
        "local_ip": get_local_ip(),
        "hostname": get_hostname(),
    }


def run_speed_test():
    """
    Run an internet speed test using speedtest-cli.
    Returns download/upload speeds and ping.
    """
    try:
        import speedtest
        st = speedtest.Speedtest()
        st.get_best_server()

        download = st.download() / 1_000_000  # Convert to Mbps
        upload = st.upload() / 1_000_000
        ping = st.results.ping

        return {
            "success": True,
            "download_mbps": round(download, 2),
            "upload_mbps": round(upload, 2),
            "ping_ms": round(ping, 1),
            "server": st.results.server.get("name", "Unknown"),
        }
    except ImportError:
        return {
            "success": False,
            "message": "speedtest-cli not installed. Install with: pip install speedtest-cli",
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Speed test failed: {str(e)}",
        }
