import threading

import pyttsx3


class Speaker:

    def __init__(self):

        # One persistent engine, reused for every speak() call.
        # This is what lets stop() reach into an utterance that's
        # already in progress on another thread.
        self.engine = pyttsx3.init()

        self.engine.setProperty("rate", 170)
        self.engine.setProperty("volume", 1.0)

        self._lock = threading.Lock()
        self.is_speaking = False

    def speak(self, text):

        print(f"🤖 Rocky: {text}")

        with self._lock:
            self.is_speaking = True

        try:
            self.engine.say(text)
            self.engine.runAndWait()

        except RuntimeError:
            # This can happen if stop() was called from another
            # thread while runAndWait() was still running. That's
            # expected when the user interrupts Rocky -- ignore it.
            pass

        finally:
            with self._lock:
                self.is_speaking = False

    def stop(self):
        """
        Interrupts whatever Rocky is currently saying.
        Safe to call even if Rocky isn't speaking right now.
        """

        try:
            self.engine.stop()
        except Exception as e:
            print("Speaker stop error:", e)


if __name__ == "__main__":

    speaker = Speaker()
    speaker.speak("Hello. This is Rocky.")