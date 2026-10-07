import customtkinter as ctk
import tkinter as tk
import psutil


class PerformanceGraph(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(
            master,
            fg_color="#101A28",
            corner_radius=20
        )

        self.canvas = tk.Canvas(
            self,
            bg="#101A28",
            highlightthickness=0,
            bd=0
        )

        self.canvas.pack(fill="both", expand=True)

        # Get an initial CPU reading
        initial_cpu = psutil.cpu_percent(interval=0.1)

        self.values = [initial_cpu] * 80
        self.current_cpu = initial_cpu
        self.scan_x = 0

        self.canvas.bind("<Configure>", self.redraw)

        self.after(200, self.animate)

    # =====================================================

    def animate(self):

        self.current_cpu = psutil.cpu_percent(interval=None)

        self.values.append(self.current_cpu)

        if len(self.values) > 80:
            self.values.pop(0)

        self.scan_x += 6

        width = self.canvas.winfo_width()

        if width > 0 and self.scan_x > width:
            self.scan_x = 0

        self.redraw()

        self.after(200, self.animate)

    # =====================================================

    def redraw(self, event=None):

        self.canvas.delete("all")

        w = max(self.canvas.winfo_width(), 10)
        h = max(self.canvas.winfo_height(), 10)

        graph_top = 40
        graph_bottom = h - 20

        # ==========================
        # GRID
        # ==========================

        for i in range(11):

            x = i * w / 10

            self.canvas.create_line(
                x, 0,
                x, h,
                fill="#173148"
            )

        for i in range(7):

            y = i * h / 6

            self.canvas.create_line(
                0, y,
                w, y,
                fill="#173148"
            )

        # ==========================
        # HEADER
        # ==========================

        self.canvas.create_text(
            18,
            18,
            anchor="w",
            text="CPU PERFORMANCE",
            fill="#42E8FF",
            font=("Segoe UI", 12, "bold")
        )

        self.canvas.create_text(
            w - 18,
            18,
            anchor="e",
            text=f"{self.current_cpu:.0f}%",
            fill="#42E8FF",
            font=("Segoe UI", 13, "bold")
        )

        # ==========================
        # GRAPH POINTS
        # ==========================

        points = []

        for i, value in enumerate(self.values):

            x = i * (w / (len(self.values) - 1))

            y = graph_bottom - ((value / 100) * (graph_bottom - graph_top))

            points.append((x, y))

        # ==========================
        # AREA
        # ==========================

        area = [(0, graph_bottom)]

        area.extend(points)

        area.append((w, graph_bottom))

        flat_area = []

        for x, y in area:
            flat_area.extend([x, y])

        self.canvas.create_polygon(
            flat_area,
            fill="#0D3248",
            outline=""
        )

        # ==========================
        # GLOW
        # ==========================

        flat = []

        for x, y in points:
            flat.extend([x, y])

        self.canvas.create_line(
            flat,
            smooth=True,
            width=7,
            fill="#145A7C"
        )

        self.canvas.create_line(
            flat,
            smooth=True,
            width=3,
            fill="#45F2FF"
        )

        # ==========================
        # CURRENT POINT
        # ==========================

        px, py = points[-1]

        self.canvas.create_oval(
            px - 5,
            py - 5,
            px + 5,
            py + 5,
            fill="#7AFFFF",
            outline=""
        )

        # ==========================
        # SCANNER
        # ==========================

        self.canvas.create_line(
            self.scan_x,
            graph_top,
            self.scan_x,
            graph_bottom,
            fill="#1CE7FF",
            width=2
        )

        # ==========================
        # FOOTER
        # ==========================

        self.canvas.create_text(
            18,
            h - 10,
            anchor="w",
            text="LIVE",
            fill="#3DFFBF",
            font=("Consolas", 10, "bold")
        )

        self.canvas.create_text(
            w - 18,
            h - 10,
            anchor="e",
            text="REAL-TIME",
            fill="#3DFFBF",
            font=("Consolas", 10)
        )