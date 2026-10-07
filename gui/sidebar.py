import customtkinter as ctk
import theme

from gui.widgets.nav_button import NavButton


class Sidebar(ctk.CTkFrame):

    def __init__(self, master, app):
        super().__init__(
            master,
            width=theme.SIDEBAR_WIDTH,
            fg_color=theme.SIDEBAR_COLOR,
            corner_radius=20
        )

        self.pack_propagate(False)

        self.app = app

        # ==========================
        # Logo
        # ==========================

        logo = ctk.CTkLabel(
            self,
            text="R.O.C.K.Y",
            font=theme.TITLE_FONT,
            text_color=theme.PRIMARY
        )

        logo.pack(
            pady=(30, 5)
        )

        subtitle = ctk.CTkLabel(
            self,
            text="AI Desktop Assistant",
            font=theme.SMALL_FONT,
            text_color=theme.TEXT_SECONDARY
        )

        subtitle.pack(
            pady=(0, 25)
        )

        # ==========================
        # Navigation
        # ==========================

        self.add_button("🏠 Dashboard", lambda: None)

        self.add_button("📶 Wi-Fi Scanner", self.app.show_wifi)

        self.add_button("💻 System Information", self.app.show_system)

        self.add_button("🖥 System Monitor", self.app.show_monitor)

        self.add_button("🌐 Speed Test", self.app.show_speed)

        self.add_button("📡 Network Monitor", self.app.show_network)

        self.add_button("🌤 Weather", self.app.show_weather)

        self.add_button("📁 File Explorer", self.app.show_files)

        # Push status to bottom
        spacer = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        spacer.pack(
            expand=True,
            fill="both"
        )

        # ==========================
        # Status
        # ==========================

        status = ctk.CTkLabel(
            self,
            text="● SYSTEM ONLINE",
            text_color=theme.SUCCESS,
            font=("Consolas", 13, "bold")
        )

        status.pack(
            pady=20
        )

    def add_button(self, text, command):

        button = NavButton(
            self,
            text=text,
            command=command
        )

        button.pack(
            fill="x",
            padx=18,
            pady=6
        )