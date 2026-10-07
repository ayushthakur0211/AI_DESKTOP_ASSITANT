import customtkinter as ctk
import tkinter as tk
import math
import psutil
import theme


class AICore(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(
            master,
            fg_color=theme.PANEL,
            corner_radius=20
        )

        self.canvas = tk.Canvas(
            self,
            bg=theme.PANEL,
            highlightthickness=0,
            bd=0
        )

        self.canvas.pack(fill="both", expand=True)

        self.angle = 0
        self.scan_angle = 0

        self.particles = []

        for i in range(40):
            self.particles.append({
                "angle": i * 9,
                "radius": 100 + (i % 5) * 15,
                "speed": 0.5 + (i % 4) * 0.25
            })

        self.canvas.bind("<Configure>", self.redraw)

        self.animate()

    # =========================================================

    def animate(self):

        self.angle += 2
        self.scan_angle += 3

        for p in self.particles:
            p["angle"] += p["speed"]

        self.redraw()

        self.after(30, self.animate)

    # =========================================================

    def redraw(self, event=None):

        self.canvas.delete("all")

        w = max(self.canvas.winfo_width(), 10)
        h = max(self.canvas.winfo_height(), 10)

        cx = w / 2
        cy = h / 2

        radius = min(w, h) * 0.22

        # =====================================================
        # Background Glow
        # =====================================================

        self.canvas.create_oval(
            cx - radius * 1.8,
            cy - radius * 1.8,
            cx + radius * 1.8,
            cy + radius * 1.8,
            fill="#10253C",
            outline=""
        )

        # =====================================================
        # Radar Rings
        # =====================================================

        for i in range(1, 5):

            r = radius * (0.5 + i * 0.35)

            self.canvas.create_oval(
                cx - r,
                cy - r,
                cx + r,
                cy + r,
                outline="#1B4566",
                width=1
            )

        # =====================================================
        # Radar Sweep
        # =====================================================

        sweep = math.radians(self.scan_angle)

        x = cx + math.cos(sweep) * radius * 1.55
        y = cy + math.sin(sweep) * radius * 1.55

        self.canvas.create_line(
            cx,
            cy,
            x,
            y,
            fill="#46E7FF",
            width=2
        )

        # =====================================================
        # Floating Particles
        # =====================================================

        for p in self.particles:

            a = math.radians(p["angle"])

            px = cx + math.cos(a) * p["radius"]
            py = cy + math.sin(a) * p["radius"]

            self.canvas.create_oval(
                px - 2,
                py - 2,
                px + 2,
                py + 2,
                fill="#48F0FF",
                outline=""
            )

        # =====================================================
        # Orbiting Satellites
        # =====================================================

        for i in range(4):

            a = math.radians(self.angle + i * 90)

            sx = cx + math.cos(a) * radius * 1.65
            sy = cy + math.sin(a) * radius * 1.65

            self.canvas.create_oval(
                sx - 5,
                sy - 5,
                sx + 5,
                sy + 5,
                fill="#6CF8FF",
                outline=""
            )

        # =====================================================
        # Rotating Rings
        # =====================================================

        self.draw_ring(
            cx,
            cy,
            radius * 1.35,
            self.angle,
            theme.PRIMARY
        )

        self.draw_ring(
            cx,
            cy,
            radius,
            -self.angle * 1.5,
            theme.SECONDARY
        )

        # =====================================================
        # Core Glow
        # =====================================================

        self.canvas.create_oval(
            cx - radius * 0.72,
            cy - radius * 0.72,
            cx + radius * 0.72,
            cy + radius * 0.72,
            fill="#0C3248",
            outline=""
        )

        self.canvas.create_oval(
            cx - radius * 0.45,
            cy - radius * 0.45,
            cx + radius * 0.45,
            cy + radius * 0.45,
            fill="#28DFFF",
            outline=""
        )

        self.canvas.create_oval(
            cx - radius * 0.20,
            cy - radius * 0.20,
            cx + radius * 0.20,
            cy + radius * 0.20,
            fill="#D8FFFF",
            outline=""
        )

        # =====================================================
        # Text
        # =====================================================

        self.canvas.create_text(
            cx,
            cy - 18,
            text="R.O.C.K.Y",
            fill="white",
            font=("Segoe UI", 18, "bold")
        )

        self.canvas.create_text(
            cx,
            cy + 12,
            text="AI CORE",
            fill="#003B58",
            font=("Consolas", 11, "bold")
        )

        # =====================================================
        # Live System Info
        # =====================================================

        cpu = psutil.cpu_percent(interval=None)
        ram = psutil.virtual_memory().percent

        self.canvas.create_text(
            cx,
            cy + radius + 55,
            text=f"CPU {cpu:.0f}%   |   RAM {ram:.0f}%",
            fill="#39FFB8",
            font=("Consolas", 12, "bold")
        )

    # =========================================================

    def draw_ring(self, cx, cy, radius, angle, color):

        segments = 42

        for i in range(segments):

            if i % 2 == 0:
                continue

            start = math.radians(angle + i * (360 / segments))
            end = math.radians(angle + i * (360 / segments) + 6)

            x1 = cx + radius * math.cos(start)
            y1 = cy + radius * math.sin(start)

            x2 = cx + radius * math.cos(end)
            y2 = cy + radius * math.sin(end)

            self.canvas.create_line(
                x1,
                y1,
                x2,
                y2,
                fill=color,
                width=3
            )