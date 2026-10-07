import ollama


class AIBrain:

    def __init__(self, model="llama3.2:1b"):

        self.model = model

        # =====================================
        # System Prompt
        # =====================================

        self.system_prompt = (
            "You are R.O.C.K.Y "
            "(Responsive Optimized Cognitive Knowledge Yielder), "
            "a professional desktop AI assistant created by Ayush Thakur. "

            "You are friendly, intelligent, helpful, and concise. "

            "For simple factual or definitional questions "
            "(e.g. 'what is a variable', 'what is Python'), "
            "answer in 2-4 sentences. Do not add extra sections, "
            "examples, or headings unless asked for more detail. "

            "For coding questions, give the code directly in a "
            "code block with only a brief explanation -- skip "
            "long preambles before the code. "

            "For genuinely complex or multi-part questions, use "
            "headings, bullet points and examples where they "
            "make the explanation clearer. "

            "Do not unnecessarily repeat the user's question. "

            "If the user changes the topic, focus on the new topic."
        )

        # =====================================
        # Conversation History
        # =====================================

        self.messages = [
            {
                "role": "system",
                "content": self.system_prompt
            }
        ]

    # =====================================
    # ASK AI
    # =====================================

    def ask(self, prompt):

        # Ignore empty prompts
        if not prompt or not prompt.strip():

            return (
                "Please tell me what you would "
                "like to know."
            )

        prompt = prompt.strip()

        # =================================
        # Save User Message
        # =================================

        self.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        try:

            # =================================
            # Ask Ollama
            # =================================

            response = ollama.chat(
                model=self.model,
                messages=self.messages,

                # Keep the model loaded in memory for 30 minutes
                # of inactivity instead of Ollama's default ~5.
                # Avoids the "cold start" reload delay on the
                # first question after a gap.
                keep_alive="30m",

                options={
                    # Caps how long a single answer can run.
                    # Generation time scales with output length,
                    # so this is the single biggest speed lever
                    # short of switching to a smaller model.
                    "num_predict": 350
                }
            )

            # =================================
            # Get AI Response
            # =================================

            reply = response["message"]["content"].strip()

            # =================================
            # Save AI Response
            # =================================

            self.messages.append(
                {
                    "role": "assistant",
                    "content": reply
                }
            )

            # =================================
            # Limit Conversation History
            # =================================

            # Keep system prompt + latest 20 messages
            if len(self.messages) > 21:

                self.messages = (
                    [self.messages[0]]
                    + self.messages[-20:]
                )

            return reply

        except Exception as e:

            print("AI Brain Error:", e)

            # The user message we appended above has no matching
            # assistant reply now. If we leave it in place, the
            # NEXT successful call would send two "user" messages
            # back to back, which can confuse the model. Roll it
            # back so history stays clean.
            if self.messages and self.messages[-1]["role"] == "user":
                self.messages.pop()

            return self._friendly_error(e)

    # =====================================
    # FRIENDLY ERROR MESSAGES
    # =====================================

    def _friendly_error(self, error):

        text = str(error).lower()

        # ollama's client raises a connection error with wording
        # along these lines when the Ollama service isn't running.
        if any(word in text for word in [
            "connection",
            "connect",
            "refused",
            "timed out",
            "timeout"
        ]):

            return (
                "I can't reach my AI brain right now. "
                "Please make sure Ollama is running "
                "on your computer, then try again."
            )

        if "model" in text and (
            "not found" in text or "pull" in text
        ):

            return (
                f"The AI model '{self.model}' doesn't seem to be "
                "installed. Try running: ollama pull "
                f"{self.model}"
            )

        return (
            "Sorry, I am having trouble connecting "
            "to my AI brain right now."
        )

    # =====================================
    # RESET CONVERSATION
    # =====================================

    def reset_conversation(self):

        self.messages = [
            {
                "role": "system",
                "content": self.system_prompt
            }
        ]

        return "Conversation has been reset."

    # =====================================
    # GET CONVERSATION STATUS
    # =====================================

    def conversation_count(self):

        return len(self.messages) - 1


# ==========================================
# TEST AI BRAIN
# ==========================================

if __name__ == "__main__":

    ai = AIBrain()

    print("=" * 50)
    print("        R.O.C.K.Y AI Assistant")
    print("=" * 50)
    print("Model:", ai.model)
    print("Type 'exit' to quit.")
    print("Type 'reset' to clear conversation.")
    print("=" * 50)

    while True:

        prompt = input("You: ").strip()

        # ==================================
        # Exit
        # ==================================

        if prompt.lower() == "exit":

            print("Rocky: Goodbye!")
            break

        # ==================================
        # Reset Conversation
        # ==================================

        if prompt.lower() == "reset":

            print("Rocky:", ai.reset_conversation())
            continue

        # ==================================
        # Empty Input
        # ==================================

        if not prompt:

            continue

        # ==================================
        # Ask AI
        # ==================================

        print("\nRocky:")

        response = ai.ask(prompt)

        print(response)

        print()