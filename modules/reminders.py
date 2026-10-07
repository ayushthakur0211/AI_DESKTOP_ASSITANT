import re
import threading
from datetime import datetime, timedelta


class ReminderManager:
    """
    Simple in-memory reminders using threading.Timer.

    Important limitation: reminders only exist while R.O.C.K.Y
    is running. Closing the app cancels any pending reminders --
    they are not saved to disk or restored on the next launch.
    """

    _TIME_PATTERN = re.compile(
        r"(.+?)\s+in\s+(\d+)\s*(second|sec|minute|min|hour|hr)s?\b",
        re.IGNORECASE
    )

    def __init__(self, app):
        self.app = app
        self.reminders = []  # list of {"text": str, "trigger_time": datetime}

    def parse_and_set(self, phrase):
        """
        Parses phrases like "call John in 10 minutes" and
        schedules a reminder. Returns a confirmation string, or
        None if the phrase couldn't be understood.
        """

        if not phrase or not phrase.strip():
            return None

        match = self._TIME_PATTERN.search(phrase.strip())

        if not match:
            return None

        task = match.group(1).strip()
        amount = int(match.group(2))
        unit = match.group(3).lower()

        if not task:
            return None

        if unit in ("second", "sec"):
            seconds = amount
            unit_label = "second" if amount == 1 else "seconds"
        elif unit in ("minute", "min"):
            seconds = amount * 60
            unit_label = "minute" if amount == 1 else "minutes"
        else:
            seconds = amount * 3600
            unit_label = "hour" if amount == 1 else "hours"

        trigger_time = datetime.now() + timedelta(seconds=seconds)

        timer = threading.Timer(seconds, self._fire, args=(task,))
        timer.daemon = True
        timer.start()

        self.reminders.append({
            "text": task,
            "trigger_time": trigger_time
        })

        return f"Okay, I'll remind you to {task} in {amount} {unit_label}."

    def _fire(self, task):

        def notify():
            message = f"\u23f0 Reminder: {task}"
            self.app.dashboard.write(message)

            try:
                self.app.speaker.speak(f"Reminder: {task}")
            except Exception:
                pass

        # Timer callbacks run on their own thread -- dispatch
        # back to the main GUI thread before touching the GUI.
        self.app.after(0, notify)

        self.reminders = [
            r for r in self.reminders if r["text"] != task
        ]

    def list_reminders(self):

        if not self.reminders:
            return "You have no active reminders."

        lines = []

        for r in self.reminders:
            remaining = r["trigger_time"] - datetime.now()
            minutes = max(int(remaining.total_seconds() // 60), 0)
            lines.append(f"- {r['text']} (in about {minutes} min)")

        return "Your active reminders:\n" + "\n".join(lines)