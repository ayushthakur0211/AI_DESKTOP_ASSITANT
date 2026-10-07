import re
from datetime import datetime

from modules.apps import (
    open_chrome,
    open_edge,
    open_notepad,
    open_calculator,
    open_paint,
    open_explorer,
    open_vscode
)

from modules.browser import (
    google_search,
    youtube_search
)

from assistant.intent_router import IntentRouter
from modules.phone import call_contact
from modules.system_actions import (
    take_screenshot,
    lock_computer,
    volume_up,
    volume_down,
    toggle_mute,
    shutdown_computer,
    restart_computer,
    cancel_shutdown,
    open_website
)
from modules.notes import add_note, read_notes, clear_notes
from modules.brightness import set_brightness, get_brightness
from modules.reminders import ReminderManager


class CommandProcessor:

    def __init__(self, app):
        self.app = app
        self.router = IntentRouter()
        self.reminder_manager = ReminderManager(app)

        # When set to "shutdown" or "restart", the NEXT command
        # must be a yes/no confirmation before anything else is
        # processed. This is the only destructive-action gate in
        # the assistant right now.
        self.pending_confirmation = None

    def execute(self, command):

        command = command.lower().strip()

        print(f"Recognized command: '{command}'")

        # =====================================
        # Pending Confirmation Gate
        # (shutdown / restart safety check -- this MUST be
        # checked before anything else, including the wake-word
        # strip, so a stray "rocky" in the reply doesn't confuse
        # the yes/no check.)
        # =====================================

        if self.pending_confirmation:

            action = self.pending_confirmation

            if any(word in command for word in ["yes", "confirm", "do it", "go ahead", "sure"]):

                self.pending_confirmation = None

                if action == "shutdown":
                    delay = shutdown_computer()
                    return (
                        f"Confirmed. Shutting down in {delay} seconds. "
                        "Say 'cancel shutdown' to stop it."
                    )

                if action == "restart":
                    delay = restart_computer()
                    return (
                        f"Confirmed. Restarting in {delay} seconds. "
                        "Say 'cancel shutdown' to stop it."
                    )

            if any(word in command for word in ["no", "cancel", "don't", "stop", "never mind", "nevermind"]):

                self.pending_confirmation = None
                return "Okay, cancelled. Nothing was changed."

            # Anything else while a confirmation is pending --
            # don't guess, ask again.
            return (
                f"I still need a yes or no. Do you want me to "
                f"{action} the computer?"
            )

        # =====================================
        # Strip wake word ("rocky", "hey rocky")
        # so it doesn't get treated as part of
        # the actual question/command below.
        # =====================================

        for wake_word in ["hey rocky", "rocky"]:

            if command.startswith(wake_word):

                command = command[len(wake_word):].strip(" ,.")
                break

        # =====================================
        # Greetings
        # (EXACT match only -- NOT "in", so a
        # question that merely contains "hi" or
        # "rocky" somewhere in it, like
        # "this" or "history", does not
        # accidentally trigger a greeting)
        # =====================================

        if command in [
            "",
            "hello",
            "hi",
            "hey",
            "hi there",
            "hello there",
            "hey there",
            "good morning",
            "good afternoon",
            "good evening"
        ]:

            hour = datetime.now().hour

            if hour < 12:
                greet = "Good Morning"
            elif hour < 18:
                greet = "Good Afternoon"
            else:
                greet = "Good Evening"

            return f"{greet}, Ayush. How can I help you today?"

        # =====================================
        # New Conversation / Reset AI
        # =====================================

        elif any(phrase in command for phrase in [
            "new conversation",
            "start a new conversation",
            "reset conversation",
            "clear conversation",
            "clear chat",
            "forget our conversation",
            "forget this conversation",
            "start new topic",
            "new topic",
            "start something new"
        ]):

            self.app.ai.reset_conversation()

            return (
                "Sure. I have cleared the previous conversation. "
                "What would you like to talk about?"
            )

        # =====================================
        # Name
        # =====================================

        elif "your name" in command or "who are you" in command:

            return "My name is Rocky."

        # =====================================
        # Time
        # =====================================

        elif any(word in command for word in [
            "time",
            "what time is it",
            "current time"
        ]):

            now = datetime.now().strftime("%I:%M %p")

            return f"The current time is {now}"

        # =====================================
        # Wi-Fi
        # =====================================

        elif any(word in command for word in [
            "wifi",
            "wi fi",
            "wi-fi",
            "scan wifi",
            "scan wi-fi",
            "show wifi",
            "show wi-fi",
            "nearby wifi"
        ]):

            self.app.after(
                0,
                self.app.show_wifi
            )

            return "Scanning nearby Wi-Fi networks."

        # =====================================
        # Network
        # =====================================

        elif any(word in command for word in [
            "network",
            "network information",
            "show network"
        ]):

            self.app.after(
                0,
                self.app.show_network
            )

            return "Opening network information."

        # =====================================
        # Weather
        # =====================================

        elif any(word in command for word in [
            "weather",
            "temperature outside",
            "what is the weather"
        ]):

            self.app.after(
                0,
                self.app.show_weather
            )

            return "Opening weather."

        # =====================================
        # Speed Test
        # =====================================

        elif any(word in command for word in [
            "speed test",
            "internet speed",
            "check internet speed",
            "test my internet"
        ]):

            self.app.after(
                0,
                self.app.show_speed
            )

            return "Running internet speed test."

        # =====================================
        # System Information
        # =====================================

        elif any(word in command for word in [
            "system information",
            "system info",
            "computer information",
            "computer info",
            "show system"
        ]):

            self.app.after(
                0,
                self.app.show_system
            )

            return "Opening system information."

        # =====================================
        # File Explorer
        # =====================================

        elif any(word in command for word in [
            "open file explorer",
            "open explorer",
            "file explorer"
        ]):

            self.app.after(
                0,
                self.app.show_files
            )

            return "Opening file explorer."

        # =====================================
        # Chrome
        # =====================================

        elif any(phrase in command for phrase in [
            "open chrome",
            "launch chrome",
            "start chrome",
            "chrome"
        ]):

            open_chrome()

            return "Opening Google Chrome."

        # =====================================
        # Microsoft Edge
        # =====================================

        elif any(phrase in command for phrase in [
            "open edge",
            "launch edge",
            "start edge",
            "microsoft edge"
        ]):

            open_edge()

            return "Opening Microsoft Edge."

        # =====================================
        # VS Code
        # =====================================

        elif any(phrase in command for phrase in [
            "open code",
            "open vs code",
            "open visual studio code",
            "launch vs code",
            "start vs code"
        ]):

            open_vscode()

            return "Opening Visual Studio Code."

        # =====================================
        # Notepad
        # =====================================

        elif any(phrase in command for phrase in [
            "open notepad",
            "launch notepad",
            "start notepad"
        ]):

            open_notepad()

            return "Opening Notepad."

        # =====================================
        # Calculator
        # =====================================

        elif any(phrase in command for phrase in [
            "open calculator",
            "launch calculator",
            "start calculator"
        ]):

            open_calculator()

            return "Opening Calculator."

        # =====================================
        # Paint
        # =====================================

        elif any(phrase in command for phrase in [
            "open paint",
            "launch paint",
            "start paint"
        ]):

            open_paint()

            return "Opening Paint."

        # =====================================
        # Google Search
        # =====================================

        elif command.startswith("search google for"):

            query = command.replace(
                "search google for",
                "",
                1
            ).strip()

            if query:

                google_search(query)

                return f"Searching Google for {query}."

            return "What should I search on Google?"

        # =====================================
        # Google Search - Natural
        # =====================================

        elif command.startswith("google search for"):

            query = command.replace(
                "google search for",
                "",
                1
            ).strip()

            if query:

                google_search(query)

                return f"Searching Google for {query}."

            return "What should I search on Google?"

        # =====================================
        # YouTube Search
        # =====================================

        elif command.startswith("search youtube for"):

            query = command.replace(
                "search youtube for",
                "",
                1
            ).strip()

            if query:

                youtube_search(query)

                return f"Searching YouTube for {query}."

            return "What should I search on YouTube?"

        # =====================================
        # YouTube Search - Natural
        # =====================================

        elif command.startswith("youtube search for"):

            query = command.replace(
                "youtube search for",
                "",
                1
            ).strip()

            if query:

                youtube_search(query)

                return f"Searching YouTube for {query}."

            return "What should I search on YouTube?"

        # =====================================
        # Play on YouTube
        # =====================================

        elif command.startswith("play"):

            query = command.replace(
                "play",
                "",
                1
            ).strip()

            if query:

                youtube_search(query)

                return f"Playing {query} on YouTube."

            return "What would you like me to play?"

        # =====================================
        # Phone Information
        # =====================================

        elif any(word in command for word in [
            "phone info",
            "phone information",
            "check my phone",
            "phone status",
            "is my phone connected",
            "phone battery"
        ]):

            self.app.after(
                0,
                self.app.show_phone
            )

            return "Checking your phone."

        # =====================================
        # Call a Contact
        # =====================================

        elif command.startswith("call "):

            name_query = command.replace("call", "", 1).strip()

            result = call_contact(name_query)

            return result["message"]

        # =====================================
        # Screenshot
        # =====================================

        elif any(phrase in command for phrase in [
            "take a screenshot",
            "take screenshot",
            "screenshot",
            "capture screen",
            "capture the screen"
        ]):

            path = take_screenshot()

            return f"Screenshot saved to {path}"

        # =====================================
        # Lock Computer
        # (safe, non-destructive -- no confirmation needed)
        # =====================================

        elif any(phrase in command for phrase in [
            "lock my computer",
            "lock the computer",
            "lock my pc",
            "lock pc",
            "lock the screen",
            "lock my screen"
        ]):

            lock_computer()

            return "Locking your computer."

        # =====================================
        # Volume Control
        # =====================================

        elif any(phrase in command for phrase in [
            "volume up",
            "increase volume",
            "turn up the volume",
            "raise the volume"
        ]):

            volume_up()

            return "Turning the volume up."

        elif any(phrase in command for phrase in [
            "volume down",
            "decrease volume",
            "turn down the volume",
            "lower the volume"
        ]):

            volume_down()

            return "Turning the volume down."

        elif any(phrase in command for phrase in [
            "mute",
            "unmute",
            "mute the volume",
            "mute sound"
        ]):

            toggle_mute()

            return "Toggling mute."

        # =====================================
        # Cancel a pending Shutdown/Restart
        # (works even without an active confirmation prompt, in
        # case the countdown was already confirmed earlier)
        # =====================================

        elif any(phrase in command for phrase in [
            "cancel shutdown",
            "stop shutdown",
            "abort shutdown",
            "cancel restart"
        ]):

            cancel_shutdown()

            return "Shutdown cancelled."

        # =====================================
        # Shutdown Computer
        # (DESTRUCTIVE -- requires confirmation. This only sets
        # the flag and asks; the actual shutdown happens in the
        # confirmation gate at the top of this method.)
        # =====================================

        elif any(phrase in command for phrase in [
            "shutdown",
            "shut down the computer",
            "shut down my computer",
            "shut down pc",
            "turn off the computer",
            "turn off my computer"
        ]):

            self.pending_confirmation = "shutdown"

            return (
                "Are you sure you want to shut down the computer? "
                "Say yes to confirm."
            )

        # =====================================
        # Restart Computer
        # (DESTRUCTIVE -- requires confirmation, same pattern
        # as shutdown above.)
        # =====================================

        elif any(phrase in command for phrase in [
            "restart the computer",
            "restart my computer",
            "restart pc",
            "reboot the computer",
            "reboot my computer",
            "reboot pc"
        ]):

            self.pending_confirmation = "restart"

            return (
                "Are you sure you want to restart the computer? "
                "Say yes to confirm."
            )

        # =====================================
        # Open Website
        # =====================================

        elif command.startswith("open website"):

            site = command.replace("open website", "", 1).strip()

            if open_website(site):
                return f"Opening {site}."

            return "Which website would you like me to open?"

        # =====================================
        # Notes
        # =====================================

        elif command.startswith("take a note"):

            text = command.replace("take a note", "", 1).strip()

            if add_note(text):
                return "Got it. I've saved that note."

            return "What would you like me to note down?"

        elif command.startswith("add note"):

            text = command.replace("add note", "", 1).strip()

            if add_note(text):
                return "Got it. I've saved that note."

            return "What would you like me to note down?"

        elif command.startswith("note that"):

            text = command.replace("note that", "", 1).strip()

            if add_note(text):
                return "Got it. I've saved that note."

            return "What would you like me to note down?"

        elif any(phrase in command for phrase in [
            "clear my notes",
            "delete my notes",
            "clear notes",
            "clear my note",
            "delete my note",
            "clear note"
        ]):

            return clear_notes()

        elif "my note" in command or (
            "note" in command and any(w in command for w in ["read", "show"])
        ):
            # "my note" also matches "my notes" (it's a substring),
            # so this one check covers singular/plural together.
            # Deliberately does NOT trigger on a bare "note" paired
            # with "what" -- that would wrongly hijack real
            # questions like "what is a musical note".

            return read_notes()

        # =====================================
        # Reminders
        # =====================================

        elif command.startswith("remind me to"):

            phrase = command.replace("remind me to", "", 1).strip()

            result = self.reminder_manager.parse_and_set(phrase)

            if result:
                return result

            return (
                "I didn't catch the timing. Try something like "
                "'remind me to call John in 10 minutes'."
            )

        elif command.startswith("remind me"):

            phrase = command.replace("remind me", "", 1).strip()

            result = self.reminder_manager.parse_and_set(phrase)

            if result:
                return result

            return (
                "I didn't catch the timing. Try something like "
                "'remind me to call John in 10 minutes'."
            )

        elif any(phrase in command for phrase in [
            "list reminders",
            "show reminders",
            "my reminders",
            "show my reminders"
        ]):

            return self.reminder_manager.list_reminders()

        # =====================================
        # Brightness Control
        # =====================================

        elif any(phrase in command for phrase in [
            "brightness up",
            "increase brightness",
            "turn up the brightness"
        ]):

            current = get_brightness()
            target = min((current or 50) + 10, 100)

            if set_brightness(target):
                return f"Setting brightness to {target} percent."

            return "Sorry, I couldn't change the brightness on this display."

        elif any(phrase in command for phrase in [
            "brightness down",
            "decrease brightness",
            "turn down the brightness"
        ]):

            current = get_brightness()
            target = max((current or 50) - 10, 0)

            if set_brightness(target):
                return f"Setting brightness to {target} percent."

            return "Sorry, I couldn't change the brightness on this display."

        elif command.startswith("set brightness to"):

            number_match = re.search(r"\d+", command)

            if not number_match:
                return "What brightness percentage would you like?"

            target = int(number_match.group())

            if set_brightness(target):
                return f"Setting brightness to {target} percent."

            return "Sorry, I couldn't change the brightness on this display."

        # =====================================
        # Clipboard
        # (Tkinter's built-in clipboard access --
        # no extra library needed.)
        # =====================================

        elif command.startswith("copy to clipboard"):

            text = command.replace("copy to clipboard", "", 1).strip()

            if not text:
                return "What would you like me to copy?"

            try:
                self.app.clipboard_clear()
                self.app.clipboard_append(text)
                self.app.update()
            except Exception as e:
                return f"Sorry, I couldn't copy that: {e}"

            return "Copied to clipboard."

        elif any(phrase in command for phrase in [
            "read clipboard",
            "what's in my clipboard",
            "whats in my clipboard",
            "show clipboard"
        ]):

            try:
                content = self.app.clipboard_get()
            except Exception:
                content = ""

            if not content.strip():
                return "Your clipboard is empty."

            return f"Your clipboard contains: {content.strip()}"

        # =====================================
        # Exit
        # =====================================

        elif any(word in command for word in [
            "exit",
            "quit",
            "goodbye",
            "bye"
        ]):

            self.app.after(
                0,
                self.app.destroy
            )

            return "Goodbye Ayush. Have a great day."

        # =====================================
        # Unknown Command -> Try Intent Router
        # =====================================

        else:

            intent = self.router.detect(command)

            if intent:
                return self.run_intent(intent)

            return "Sorry. I don't know that command yet."

    # =====================================
    # INTENT DISPATCHER
    # (used only when the rules above find no exact match)
    # =====================================

    def run_intent(self, intent):

        if intent == "OPEN_CHROME":
            open_chrome()
            return "Opening Google Chrome."

        elif intent == "OPEN_EDGE":
            open_edge()
            return "Opening Microsoft Edge."

        elif intent == "OPEN_VSCODE":
            open_vscode()
            return "Opening Visual Studio Code."

        elif intent == "OPEN_NOTEPAD":
            open_notepad()
            return "Opening Notepad."

        elif intent == "OPEN_CALCULATOR":
            open_calculator()
            return "Opening Calculator."

        elif intent == "OPEN_PAINT":
            open_paint()
            return "Opening Paint."

        elif intent == "FILE_EXPLORER":
            self.app.after(0, self.app.show_files)
            return "Opening file explorer."

        elif intent == "SYSTEM_INFO":
            self.app.after(0, self.app.show_system)
            return "Opening system information."

        elif intent == "SYSTEM_MONITOR":
            self.app.after(0, self.app.show_monitor)
            return "Opening live system monitor."

        elif intent == "WIFI_SCAN":
            self.app.after(0, self.app.show_wifi)
            return "Scanning nearby Wi-Fi networks."

        elif intent == "NETWORK_INFO":
            self.app.after(0, self.app.show_network)
            return "Opening network information."

        elif intent == "SPEED_TEST":
            self.app.after(0, self.app.show_speed)
            return "Running internet speed test."

        elif intent == "WEATHER":
            self.app.after(0, self.app.show_weather)
            return "Opening weather."

        elif intent == "PHONE_INFO":
            self.app.after(0, self.app.show_phone)
            return "Checking your phone."

        elif intent == "NEW_CONVERSATION":
            self.app.ai.reset_conversation()
            return (
                "Sure. I have cleared the previous conversation. "
                "What would you like to talk about?"
            )

        elif intent == "EXIT":
            self.app.after(0, self.app.destroy)
            return "Goodbye Ayush. Have a great day."

        return "Sorry. I don't know that command yet."