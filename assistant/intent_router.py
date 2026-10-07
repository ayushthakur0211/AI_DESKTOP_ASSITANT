"""
IntentRouter
=====================================
A lightweight, dependency-free "second pass" command matcher.

CommandProcessor.execute() tries its normal exact/keyword rules FIRST.
Only if none of those rules match does it fall back to this router.

This keeps commands.py from turning into a giant pile of elif
statements (see project roadmap, Phase 10 / architectural rule),
while still letting Rocky understand more natural phrasing like:

    "Can you launch my browser?"
    "Start the calculator."
    "How much RAM am I using?"
    "Open my code editor."

How it works:
    Each intent has one or more "trigger sets". A trigger set is a
    group of words that must ALL appear somewhere in the command
    (in any order) for that set to match. The intent with the
    trigger set that requires the MOST words is preferred, since
    more specific matches should win over vague ones.
"""


class IntentRouter:

    def __init__(self):

        # =====================================
        # Intent -> list of trigger word sets
        # =====================================
        self.intents = {

            "OPEN_CHROME": [
                {"chrome"},
                {"open", "browser"},
                {"launch", "browser"},
                {"start", "browser"},
                {"use", "chrome"},
            ],

            "OPEN_EDGE": [
                {"edge"},
                {"microsoft", "edge"},
            ],

            "OPEN_VSCODE": [
                {"vscode"},
                {"vs", "code"},
                {"code", "editor"},
                {"visual", "studio"},
            ],

            "OPEN_NOTEPAD": [
                {"notepad"},
                {"note", "pad"},
                {"text", "editor"},
            ],

            "OPEN_CALCULATOR": [
                {"calculator"},
                {"calc"},
                {"do", "math"},
            ],

            "OPEN_PAINT": [
                {"paint"},
                {"drawing", "app"},
            ],

            "FILE_EXPLORER": [
                {"file", "explorer"},
                {"my", "files"},
                {"browse", "files"},
                {"open", "folder"},
                {"show", "files"},
            ],

            "SYSTEM_INFO": [
                {"system", "information"},
                {"system", "info"},
                {"computer", "info"},
                {"about", "my", "computer"},
                {"specs"},
                {"specifications"},
            ],

            "SYSTEM_MONITOR": [
                {"ram"},
                {"cpu"},
                {"memory", "usage"},
                {"performance"},
                {"disk", "usage"},
                {"how", "much", "ram"},
                {"how", "much", "cpu"},
            ],

            "WIFI_SCAN": [
                {"wifi"},
                {"wi-fi"},
                {"wireless", "network"},
                {"wireless", "networks"},
            ],

            "NETWORK_INFO": [
                {"network"},
                {"ip", "address"},
                {"internet", "connection"},
            ],

            "SPEED_TEST": [
                {"speed", "test"},
                {"internet", "speed"},
                {"how", "fast", "internet"},
            ],

            "WEATHER": [
                {"weather"},
                {"temperature"},
                {"forecast"},
                {"raining"},
            ],

            "PHONE_INFO": [
                {"phone"},
                {"my", "mobile"},
                {"mobile", "battery"},
            ],

            "NEW_CONVERSATION": [
                {"new", "topic"},
                {"change", "subject"},
                {"change", "topic"},
                {"different", "topic"},
                {"start", "over"},
                {"forget", "that"},
                {"talk", "about", "something", "else"},
            ],

            "EXIT": [
                {"shut", "down", "rocky"},
                {"close", "the", "app"},
                {"close", "rocky"},
                {"see", "you", "later"},
                {"turn", "off", "rocky"},
            ],
        }

    # =====================================
    # DETECT INTENT
    # =====================================

    def detect(self, command):
        """
        Returns the best-matching intent name (a string) or None
        if nothing matches well enough.
        """

        command = command.lower().strip()

        if not command:
            return None

        best_intent = None
        best_score = 0

        for intent, trigger_sets in self.intents.items():

            for trigger in trigger_sets:

                # Every word in this trigger set must be present
                # somewhere in the command.
                if all(word in command for word in trigger):

                    score = len(trigger)

                    # Prefer the most specific (longest) match.
                    if score > best_score:
                        best_score = score
                        best_intent = intent

        return best_intent