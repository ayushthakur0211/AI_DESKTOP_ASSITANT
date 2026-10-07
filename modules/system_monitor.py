import psutil
import time


def format_uptime(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    return f"{hours}h {minutes}m"


def get_system_monitor():

    cpu = psutil.cpu_percent(interval=None)
    ram = psutil.virtual_memory()

    disk = psutil.disk_usage("/")

    battery = psutil.sensors_battery()

    boot = psutil.boot_time()

    uptime = time.time() - boot

    return {

        "CPU Usage": f"{cpu} %",

        "RAM Usage": f"{ram.percent} %",

        "RAM Available": f"{ram.available // (1024**3)} GB",

        "Disk Usage": f"{disk.percent} %",

        "Disk Free": f"{disk.free // (1024**3)} GB",

        "Battery": (
            f"{battery.percent}%"
            if battery
            else "No Battery"
        ),

        "System Uptime": format_uptime(uptime)
    }