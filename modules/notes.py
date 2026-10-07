import os
from datetime import datetime

NOTES_FOLDER = os.path.join(os.path.expanduser("~"), "Documents", "ROCKY")
NOTES_FILE = os.path.join(NOTES_FOLDER, "notes.txt")


def add_note(text):
    """
    Appends a timestamped note to a plain text file --
    a simple running log, not a database.
    """

    if not text or not text.strip():
        return False

    os.makedirs(NOTES_FOLDER, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %I:%M %p")

    with open(NOTES_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {text.strip()}\n")

    return True


def read_notes(limit=10):
    """
    Returns the most recent notes as a single string. Caps how
    many are read back so a long history doesn't turn into a
    huge wall of speech.
    """

    if not os.path.exists(NOTES_FILE):
        return "You don't have any notes yet."

    with open(NOTES_FILE, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    if not lines:
        return "You don't have any notes yet."

    recent = lines[-limit:]

    return "Here are your recent notes:\n" + "\n".join(recent)


def clear_notes():

    if os.path.exists(NOTES_FILE):
        os.remove(NOTES_FILE)

    return "All notes have been cleared."