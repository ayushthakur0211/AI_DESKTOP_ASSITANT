import customtkinter as ctk
import theme


class NavButton(ctk.CTkButton):

    def __init__(self, master, text, command=None):

        super().__init__(
            master,

            text=text,

            command=command,

            height=48,

            corner_radius=12,

            anchor="w",

            font=theme.BODY_FONT,

            fg_color=theme.BUTTON,

            hover_color=theme.BUTTON_HOVER,

            text_color=theme.TEXT,

            border_width=1,

            border_color=theme.BORDER
        )