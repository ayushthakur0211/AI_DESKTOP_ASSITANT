import customtkinter as ctk


class InfoCard(ctk.CTkFrame):

    def __init__(self, master, title, value="--"):
        super().__init__(
            master,
            corner_radius=15
        )

        self.configure(
            width=220,
            height=130
        )

        self.grid_propagate(False)

        self.title = ctk.CTkLabel(
            self,
            text=title,
            font=("Arial", 16, "bold")
        )
        self.title.pack(pady=(15, 5))

        self.value = ctk.CTkLabel(
            self,
            text=value,
            font=("Arial", 32, "bold")
        )
        self.value.pack(expand=True)

    def update_value(self, value):
        self.value.configure(text=value)