from datetime import datetime

from assistant.listener import Listener
from assistant.speaker import Speaker


class RockyAI:

    def __init__(self):
        self.listener = Listener()
        self.speaker = Speaker()

    def run(self):

        self.speaker.speak(
            "Rocky artificial intelligence is now online."
        )

        while True:

            command = self.listener.listen()

            if not command:
                continue

            print("Command:", command)

            # Greeting
            if "hello" in command or "hi" in command:

                self.speaker.speak(
                    "Hello Ayush. How can I help you today?"
                )

            # Name
            elif "your name" in command:

                self.speaker.speak(
                    "My name is Rocky."
                )

            # Time
            elif "time" in command:

                now = datetime.now().strftime("%I:%M %p")

                self.speaker.speak(
                    f"The current time is {now}"
                )

            # Exit
            elif "exit" in command or "goodbye" in command:

                self.speaker.speak(
                    "Goodbye Ayush."
                )

                break

            else:

                self.speaker.speak(
                    "Sorry, I don't know that command yet."
                )


if __name__ == "__main__":
    RockyAI().run()