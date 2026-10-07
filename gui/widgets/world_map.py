import os
import customtkinter as ctk
from PIL import Image


class WorldMap(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.configure(
            fg_color="#0E1624",
            corner_radius=20,
            border_width=1,
            border_color="#1F4D7A"
        )

        title = ctk.CTkLabel(
            self,
            text="🌍 GLOBAL NETWORK",
            font=("Arial", 18, "bold"),
            text_color="#47D7FF"
        )
        title.pack(pady=(15, 10))

        project_root = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                ".."
            )
        )

        image_path = os.path.join(
            project_root,
            "assets",
            "world_map.png"
        )

        if not os.path.exists(image_path):
            ctk.CTkLabel(
                self,
                text="Image not found",
                text_color="red"
            ).pack(pady=20)
            return

        image = Image.open(image_path)

        self.world_image = ctk.CTkImage(
            light_image=image,
            dark_image=image,
            size=(760, 320)
        )

        self.map_label = ctk.CTkLabel(
            self,
            text="",
            image=self.world_image
        )

        self.map_label.pack(
            padx=20,
            pady=(0, 20)
        )