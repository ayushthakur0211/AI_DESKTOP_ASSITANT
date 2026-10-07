import psutil
import socket


def get_network_info():
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
    except:
        ip_address = "Not Connected"

    net = psutil.net_io_counters()

    return {
        "Status": "Connected" if ip_address != "Not Connected" else "Disconnected",
        "IP Address": ip_address,
        "Data Sent": f"{net.bytes_sent / (1024**2):.2f} MB",
        "Data Received": f"{net.bytes_recv / (1024**2):.2f} MB"
    }