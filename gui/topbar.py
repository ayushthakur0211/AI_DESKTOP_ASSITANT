import customtkinter as ctk
from datetime import datetime


class TopBar(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.configure(
            height=70,
            fg_color="#08111F",
            corner_radius=0
        )

        self.pack_propagate(False)

        # Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # ==========================
        # Left - Logo
        # ==========================

        self.logo = ctk.CTkLabel(
            self,
            text="🤖 R.O.C.K.Y",
            font=("Segoe UI", 28, "bold"),
            text_color="#00E5FF"
        )

        self.logo.grid(
            row=0,
            column=0,
            padx=20,
            pady=15,
            sticky="w"
        )

        # ==========================
        # Center - User Information
        # ==========================

        self.user = ctk.CTkLabel(
            self,
            text="👤 Ayush Thakur",
            font=("Segoe UI", 18, "bold"),
            text_color="#FFFFFF"
        )

        self.user.grid(
            row=0,
            column=1,
            pady=(8, 0)
        )

        self.status = ctk.CTkLabel(
            self,
            text="🟢 AI SYSTEM ONLINE",
            font=("Consolas", 14),
            text_color="#00FF99"
        )

        self.status.grid(
            row=1,
            column=1,
            pady=(0, 8)
        )

        # ==========================
        # Right - Clock
        # ==========================

        self.clock = ctk.CTkLabel(
            self,
            text="00:00:00",
            font=("Consolas", 24, "bold"),
            text_color="#00E5FF"
        )

        self.clock.grid(
            row=0,
            column=2,
            padx=20,
            pady=(8, 0),
            sticky="e"
        )

        self.date = ctk.CTkLabel(
            self,
            text="Loading...",
            font=("Segoe UI", 13),
            text_color="#B8C7D9"
        )

        self.date.grid(
            row=1,
            column=2,
            padx=20,
            pady=(0, 8),
            sticky="e"
        )

        self.update_clock()

    def update_clock(self):

        now = datetime.now()

        self.clock.configure(
            text=now.strftime("%H:%M:%S")
        )

        self.date.configure(
            text=now.strftime("%A, %d %B %Y")
        )

        self.after(1000, self.update_clock)