import platform
import psutil


def get_system_info():
    info = {}

    info["Operating System"] = platform.system() + " " + platform.release()
    info["Processor"] = platform.processor()

    info["CPU Usage"] = f"{psutil.cpu_percent(interval=1)} %"

    memory = psutil.virtual_memory()

    info["RAM Used"] = f"{memory.percent} %"

    disk = psutil.disk_usage("/")

    info["Disk Used"] = f"{disk.percent} %"

    battery = psutil.sensors_battery()

    if battery:
        info["Battery"] = f"{battery.percent}%"
    else:
        info["Battery"] = "Not Available"

    return info