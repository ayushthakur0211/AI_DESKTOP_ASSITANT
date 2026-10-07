import customtkinter as ctk
import theme


class InfoPanel(ctk.CTkFrame):

    def __init__(self, master, title, value="--"):

        super().__init__(
            master,
            fg_color=theme.PANEL,
            corner_radius=18,
            border_width=1,
            border_color=theme.BORDER
        )

        self.configure(height=90)

        self.pack_propagate(False)

        self.title = ctk.CTkLabel(
            self,
            text=title,
            font=theme.BODY_FONT,
            text_color=theme.TEXT_SECONDARY
        )

        self.title.pack(pady=(12, 0))

        self.value = ctk.CTkLabel(
            self,
            text=value,
            font=("Segoe UI", 22, "bold"),
            text_color=theme.PRIMARY
        )

        self.value.pack(pady=(5, 10))

    def set_value(self, value):
        self.value.configure(text=str(value))