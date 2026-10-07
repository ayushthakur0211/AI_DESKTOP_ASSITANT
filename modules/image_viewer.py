from PIL import Image
import customtkinter as ctk


class ImageViewer(ctk.CTkToplevel):

    def __init__(self, master, image_path):
        super().__init__(master)

        self.title("🖼 Image Viewer")
        self.geometry("900x700")

        image = Image.open(image_path)

        # Resize if image is too large
        image.thumbnail((850, 650))

        self.photo = ctk.CTkImage(
            light_image=image,
            dark_image=image,
            size=image.size
        )

        label = ctk.CTkLabel(
            self,
            text="",
            image=self.photo
        )

        label.pack(expand=True, padx=20, pady=20)