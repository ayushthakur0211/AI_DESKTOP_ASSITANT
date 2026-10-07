import ctypes
import os
import webbrowser
from datetime import datetime

from PIL import ImageGrab


# =====================================
# SCREENSHOT
# =====================================

def take_screenshot():
    """
    Captures the screen and saves it to
    ~/Pictures/ROCKY Screenshots/. Returns the saved file path.
    """

    folder = os.path.join(
        os.path.expanduser("~"), "Pictures", "ROCKY Screenshots"
    )

    os.makedirs(folder, exist_ok=True)

    filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    path = os.path.join(folder, filename)

    image = ImageGrab.grab()
    image.save(path)

    return path


# =====================================
# LOCK COMPUTER
# =====================================

def lock_computer():
    """
    Locks the Windows session immediately. Safe, non-destructive
    -- no confirmation needed.
    """

    ctypes.windll.user32.LockWorkStation()


# =====================================
# VOLUME CONTROL
# =====================================
# Uses the same virtual media keys a physical keyboard sends,
# so this works regardless of which audio device is active and
# needs no extra libraries beyond ctypes (already in Python).

_VK_VOLUME_MUTE = 0xAD
_VK_VOLUME_DOWN = 0xAE
_VK_VOLUME_UP = 0xAF
_KEYEVENTF_EXTENDEDKEY = 0x1
_KEYEVENTF_KEYUP = 0x2


def _press_media_key(vk_code, presses=1):

    for _ in range(presses):
        ctypes.windll.user32.keybd_event(vk_code, 0, _KEYEVENTF_EXTENDEDKEY, 0)
        ctypes.windll.user32.keybd_event(
            vk_code, 0, _KEYEVENTF_EXTENDEDKEY | _KEYEVENTF_KEYUP, 0
        )


def volume_up(steps=4):
    _press_media_key(_VK_VOLUME_UP, steps)


def volume_down(steps=4):
    _press_media_key(_VK_VOLUME_DOWN, steps)


def toggle_mute():
    """
    Windows only exposes a single MUTE TOGGLE key -- there's no
    separate "unmute" key. Pressing this again un-mutes.
    """
    _press_media_key(_VK_VOLUME_MUTE, 1)


# =====================================
# SHUTDOWN / RESTART
# =====================================
# These run a delayed Windows shutdown/restart rather than an
# instant one, specifically so a mis-heard command can still be
# cancelled with "cancel shutdown" before anything happens.

_SHUTDOWN_DELAY_SECONDS = 30


def shutdown_computer():
    os.system(f"shutdown /s /t {_SHUTDOWN_DELAY_SECONDS}")
    return _SHUTDOWN_DELAY_SECONDS


def restart_computer():
    os.system(f"shutdown /r /t {_SHUTDOWN_DELAY_SECONDS}")
    return _SHUTDOWN_DELAY_SECONDS


def cancel_shutdown():
    os.system("shutdown /a")


# =====================================
# OPEN WEBSITE
# =====================================

_SITE_SHORTCUTS = {
    "instagram": "https://instagram.com",
    "facebook": "https://facebook.com",
    "twitter": "https://twitter.com",
    "x": "https://x.com",
    "linkedin": "https://linkedin.com",
    "github": "https://github.com",
    "gmail": "https://mail.google.com",
    "whatsapp": "https://web.whatsapp.com",
    "netflix": "https://netflix.com",
    "amazon": "https://amazon.com",
    "reddit": "https://reddit.com",
    "chatgpt": "https://chat.openai.com",
}


def open_website(name_or_url):
    """
    Opens a website by shortcut name (e.g. "instagram"), a bare
    domain ("example.com"), or a full URL. Returns True if
    something was opened, False if given nothing usable.
    """

    if not name_or_url:
        return False

    query = name_or_url.strip().lower()

    if not query:
        return False

    if query in _SITE_SHORTCUTS:
        webbrowser.open(_SITE_SHORTCUTS[query])
        return True

    if query.startswith("http://") or query.startswith("https://"):
        webbrowser.open(query)
        return True

    if "." in query:
        webbrowser.open(f"https://{query}")
        return True

    # Bare name with no dot and no known shortcut -- best guess.
    webbrowser.open(f"https://{query}.com")
    return True