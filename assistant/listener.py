import speech_recognition as sr


class Listener:

    def __init__(self):
        self.recognizer = sr.Recognizer()

    def listen(self):

        try:
            with sr.Microphone() as source:

                print("\n🎤 Listening...")

                # Calibrate against background noise for a full
                # second (more stable than 0.5s).
                self.recognizer.adjust_for_ambient_noise(
                    source,
                    duration=1
                )

                # The auto-calibration above can still end up too
                # high in a noisy room, forcing you to shout. Nudge
                # it down and lock it so it can't drift back up
                # mid-listen.
                self.recognizer.energy_threshold = max(
                    self.recognizer.energy_threshold - 50,
                    150
                )
                self.recognizer.dynamic_energy_threshold = False

                # Slightly longer pause_threshold avoids cutting
                # you off mid-sentence during natural pauses.
                self.recognizer.pause_threshold = 0.8

                print(
                    "🎚 Energy threshold set to: "
                    f"{self.recognizer.energy_threshold}"
                )

                audio = self.recognizer.listen(
                    source,
                    timeout=8,
                    phrase_time_limit=12
                )

        except OSError as e:
            # No microphone found / mic is in use by another app.
            print("Microphone Error:", e)
            return ""

        except sr.WaitTimeoutError:
            print("No speech detected in time.")
            return ""

        # Microphone is now released here

        try:
            text = self.recognizer.recognize_google(audio)

            print(f"\n👤 You: {text}")

            return text.lower()

        except sr.UnknownValueError:
            print("Couldn't understand.")
            return ""

        except sr.RequestError as e:
            # Google Speech API unreachable -- usually means no
            # internet connection.
            print("Speech Recognition Service Error:", e)
            return ""