import re
import subprocess

# CREATE_NO_WINDOW only exists on Windows (prevents a black
# console window from flashing open every time we call adb).
_NO_WINDOW_FLAG = getattr(subprocess, "CREATE_NO_WINDOW", 0)

# =====================================
# ADB PATH
# =====================================
# Update this path if you ever move the platform-tools folder.
ADB_PATH = (
    r"C:\Users\AYUSH THAKUR\Downloads\platform-tools-latest-windows"
    r"\platform-tools\adb.exe"
)


def _run_adb(args, timeout=8):
    """
    Runs an adb command and returns its stdout as a stripped
    string. Returns None if adb isn't found, the command times
    out, or something else goes wrong.
    """

    try:
        result = subprocess.run(
            [ADB_PATH] + args,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            creationflags=_NO_WINDOW_FLAG
        )

        return result.stdout.strip()

    except FileNotFoundError:
        print("ADB not found at:", ADB_PATH)
        return None

    except subprocess.TimeoutExpired:
        print("ADB command timed out.")
        return None

    except Exception as e:
        print("ADB error:", e)
        return None


def is_connected():
    """
    Returns True if a phone is connected AND authorized via adb.
    (A device listed as "unauthorized" or "offline" does not
    count as connected.)
    """

    output = _run_adb(["devices"])

    if not output:
        return False

    for line in output.splitlines()[1:]:

        line = line.strip()

        if line.endswith("device"):
            return True

    return False


def get_phone_info():
    """
    Returns a dict of basic phone info. If no phone is
    connected/authorized, returns a dict with an "Error" key
    instead (same pattern as modules/weather.py).
    """

    if not is_connected():
        return {
            "Error": (
                "No phone connected. Make sure USB debugging is "
                "on and the cable is plugged in."
            )
        }

    model = _run_adb(
        ["shell", "getprop", "ro.product.model"]
    ) or "Unknown"

    manufacturer = _run_adb(
        ["shell", "getprop", "ro.product.manufacturer"]
    ) or "Unknown"

    android_version = _run_adb(
        ["shell", "getprop", "ro.build.version.release"]
    ) or "Unknown"

    battery_raw = _run_adb(
        ["shell", "dumpsys", "battery"]
    ) or ""

    battery_level = "Unknown"
    charging = "No"

    for line in battery_raw.splitlines():

        line = line.strip()

        if line.startswith("level:"):
            battery_level = line.split(":")[1].strip() + "%"

        if line.startswith("AC powered:") or line.startswith("USB powered:"):
            if "true" in line.lower():
                charging = "Yes"

    return {
        "Manufacturer": manufacturer,
        "Model": model,
        "Android Version": android_version,
        "Battery": battery_level,
        "Charging": charging
    }


if __name__ == "__main__":

    print("Connected:", is_connected())
    print(get_phone_info())


# =====================================
# CONTACTS + CALLING
# =====================================
# Nothing here is ever saved to a file. Every lookup reads
# straight from the phone, live, and the result is discarded
# as soon as the function returns.

def _get_contacts():
    """
    Reads (name, number) pairs live from the phone's Contacts
    Provider via adb. Returns [] if nothing found or no phone
    is connected. Nothing is written to disk.
    """

    print("📇 Reading contacts from phone...")

    output = _run_adb(
        [
            "shell", "content", "query",
            "--uri", "content://com.android.contacts/data/phones",
            "--projection", "display_name:data1"
        ],
        timeout=25
    )

    if not output:
        print("📇 No contact data received (empty result or timeout).")
        return []

    contacts = []

    for line in output.splitlines():

        line = line.strip()

        if not line.startswith("Row:"):
            continue

        # Example line:
        # Row: 0 display_name=John Doe, data1=9876543210
        try:
            after_row = line.split(" ", 2)[2]
            parts = after_row.split(", ")

            entry = {}

            for part in parts:
                if "=" in part:
                    key, value = part.split("=", 1)
                    entry[key.strip()] = value.strip()

            name = entry.get("display_name")
            number = entry.get("data1")

            if name and number:
                contacts.append({"name": name, "number": number})

        except Exception:
            continue

    print(f"📇 Loaded {len(contacts)} contact entries.")

    return contacts


def find_contact(name_query):
    """
    Searches the live contact list for a match. Returns
    (contact_dict, None) on a clean single match, or
    (None, [list of names]) if more than one DIFFERENT person
    matched (ambiguous), or (None, []) if nobody matched.

    Matching works two ways, since real speech often has extra
    words around the actual name (e.g. "call tu Nishant jija
    ji" instead of just "Nishant"):

      1. The whole spoken phrase appears inside the contact's
         name (handles saying a full/partial name cleanly).
      2. A real word FROM the contact's name appears somewhere
         inside what was said (handles filler words wrapped
         around the name).
    """

    contacts = _get_contacts()

    if not contacts:
        return None, []

    query = name_query.strip().lower()

    if not query:
        return None, []

    # Pass 1: strict match -- what was said is fully contained
    # in the contact's name. This is the stronger signal, so if
    # ANY contact matches this way, we trust it and stop there.
    matches = [
        c for c in contacts
        if query in c["name"].lower()
    ]

    # Pass 2: only if pass 1 found NOTHING -- fall back to
    # checking whether a real word from the contact's name shows
    # up somewhere in what was said, even with extra words
    # wrapped around it (handles noisy/filler speech).
    if not matches:

        for c in contacts:

            name_words = c["name"].lower().split()

            for word in name_words:

                if len(word) > 2 and word in query:
                    matches.append(c)
                    break

    if not matches:
        return None, []

    # A contact can have multiple numbers (home/work/mobile) --
    # collapse those down to one entry per unique name.
    unique_names = {}

    for m in matches:
        unique_names.setdefault(m["name"], m["number"])

    if len(unique_names) == 1:
        name, number = next(iter(unique_names.items()))
        return {"name": name, "number": number}, None

    # More than one different person matched -- don't guess.
    return None, list(unique_names.keys())


def call_number(number):
    """
    Triggers a real phone call to the given number via adb.
    Returns True if the command was sent successfully.
    """

    clean_number = re.sub(r"[^\d+]", "", number)

    if not clean_number:
        return False

    _run_adb([
        "shell", "am", "start",
        "-a", "android.intent.action.CALL",
        "-d", f"tel:{clean_number}"
    ])

    return True


def call_contact(name_query):
    """
    Looks up a contact by (partial) name and places a call.
    Returns a dict describing what happened -- never raises.
    """

    if not name_query or not name_query.strip():
        return {
            "status": "error",
            "message": "Who would you like me to call?"
        }

    if not is_connected():
        return {
            "status": "error",
            "message": (
                "No phone connected. Make sure USB debugging is "
                "on and the cable is plugged in."
            )
        }

    contact, ambiguous_names = find_contact(name_query)

    if contact is None and ambiguous_names:

        options = ", ".join(ambiguous_names[:5])

        return {
            "status": "ambiguous",
            "message": (
                f"I found multiple contacts matching "
                f"'{name_query}': {options}. "
                "Please be more specific."
            )
        }

    if contact is None:
        return {
            "status": "not_found",
            "message": (
                f"I couldn't find a contact named "
                f"'{name_query}' on your phone."
            )
        }

    success = call_number(contact["number"])

    if success:
        return {
            "status": "calling",
            "message": f"Calling {contact['name']}.",
            "name": contact["name"],
            "number": contact["number"]
        }

    return {
        "status": "error",
        "message": (
            f"Found {contact['name']}'s number but couldn't "
            "start the call."
        )
    }