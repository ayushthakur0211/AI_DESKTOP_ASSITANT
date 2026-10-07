import subprocess

_NO_WINDOW_FLAG = getattr(subprocess, "CREATE_NO_WINDOW", 0)

# NOTE: This works for laptop built-in displays (which expose
# the WMI brightness interface). It generally does NOT work for
# external desktop monitors, which use a different (DDC/CI)
# protocol Windows doesn't expose this way.


def set_brightness(percent):

    percent = max(0, min(100, int(percent)))

    ps_command = (
        "(Get-WmiObject -Namespace root/WMI "
        "-Class WmiMonitorBrightnessMethods)"
        f".WmiSetBrightness(1,{percent})"
    )

    try:
        subprocess.run(
            ["powershell", "-Command", ps_command],
            capture_output=True,
            text=True,
            timeout=8,
            creationflags=_NO_WINDOW_FLAG
        )
        return True

    except Exception as e:
        print("Brightness set error:", e)
        return False


def get_brightness():

    ps_command = (
        "(Get-WmiObject -Namespace root/WMI "
        "-Class WmiMonitorBrightness).CurrentBrightness"
    )

    try:
        result = subprocess.run(
            ["powershell", "-Command", ps_command],
            capture_output=True,
            text=True,
            timeout=8,
            creationflags=_NO_WINDOW_FLAG
        )

        value = result.stdout.strip()

        return int(value) if value.isdigit() else None

    except Exception as e:
        print("Brightness read error:", e)
        return None