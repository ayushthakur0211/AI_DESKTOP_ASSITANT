import customtkinter as ctk
import tkinter as tk
import math


class CircleGauge(ctk.CTkFrame):

    def __init__(self, master, title):
        super().__init__(
            master,
            fg_color="transparent"
        )

        self.title = title
        self.value = 0
        self.target_value = 0

        self.canvas = tk.Canvas(
            self,
            width=170,
            height=170,
            bg="#0F1722",
            highlightthickness=0,
            bd=0
        )

        self.canvas.pack()

        self.animate()

    # =====================================================

    def set_value(self, value):
        """Update gauge value (0-100)."""
        self.target_value = max(0, min(100, value))

    # =====================================================

    def animate(self):

        if self.value < self.target_value:
            self.value += 1
        elif self.value > self.target_value:
            self.value -= 1

        self.draw()

        self.after(20, self.animate)

    # =====================================================

    def get_color(self):

        if self.value < 50:
            return "#39FFB8"

        elif self.value < 80:
            return "#FFD84A"

        return "#FF4D6D"

    # =====================================================

    def draw(self):

        self.canvas.delete("all")

        cx = 85
        cy = 85
        r = 58

        # Background Ring

        self.canvas.create_oval(
            cx-r,
            cy-r,
            cx+r,
            cy+r,
            outline="#1D344A",
            width=10
        )

        color = self.get_color()

        # Progress Arc

        extent = (self.value / 100) * 360

        self.canvas.create_arc(
            cx-r,
            cy-r,
            cx+r,
            cy+r,
            start=90,
            extent=-extent,
            style="arc",
            outline=color,
            width=10
        )

        # Glow Arc

        self.canvas.create_arc(
            cx-r,
            cy-r,
            cx+r,
            cy+r,
            start=90,
            extent=-extent,
            style="arc",
            outline="#66F7FF",
            width=2
        )

        # Percentage

        self.canvas.create_text(
            cx,
            cy-8,
            text=f"{int(self.value)}%",
            fill="white",
            font=("Segoe UI", 18, "bold")
        )

        # Label

        self.canvas.create_text(
            cx,
            cy+24,
            text=self.title,
            fill="#47D7FF",
            font=("Consolas", 11, "bold")
        )