import customtkinter as ctk
from datetime import datetime


class LiveClock(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.configure(fg_color="transparent")

        self.time_label = ctk.CTkLabel(
            self,
            text="00:00:00",
            font=("Arial", 24, "bold")
        )
        self.time_label.pack()

        self.date_label = ctk.CTkLabel(
            self,
            text="Loading...",
            font=("Arial", 14)
        )
        self.date_label.pack()

        self.update_clock()

    def update_clock(self):

        now = datetime.now()

        self.time_label.configure(
            text=now.strftime("%I:%M:%S %p")
        )

        self.date_label.configure(
            text=now.strftime("%A, %d %B %Y")
        )

        self.after(1000, self.update_clock)