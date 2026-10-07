import customtkinter as ctk
import theme
from datetime import datetime

from gui.widgets.circle_gauge import CircleGauge
from gui.widgets.ai_core import AICore
from gui.widgets.performance_graph import PerformanceGraph
from gui.widgets.status_panel import StatusPanel
from gui.widgets.world_map import WorldMap


class Dashboard(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        # ==========================================
        # MAIN GRID
        # ==========================================

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=4)
        self.grid_columnconfigure(2, weight=1)

        self.grid_rowconfigure(0, weight=7)
        self.grid_rowconfigure(1, weight=2)
        self.grid_rowconfigure(2, weight=0)

        # ==========================================
        # LEFT PANEL
        # ==========================================

        left = ctk.CTkFrame(
            self,
            fg_color=theme.PANEL,
            corner_radius=20
        )

        left.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 12),
            pady=(0, 10)
        )

        ctk.CTkLabel(
            left,
            text="SYSTEM",
            font=theme.SUBTITLE_FONT,
            text_color=theme.PRIMARY
        ).pack(pady=(20, 15))

        self.cpu = CircleGauge(left, "CPU")
        self.cpu.pack(pady=8)

        self.ram = CircleGauge(left, "RAM")
        self.ram.pack(pady=8)

        self.disk = CircleGauge(left, "DISK")
        self.disk.pack(pady=8)

        self.battery = CircleGauge(left, "BATTERY")
        self.battery.pack(pady=8)

        # ==========================================
        # CENTER PANEL
        # ==========================================

        center = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        center.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=10,
            pady=(0, 10)
        )

        center.grid_columnconfigure(0, weight=1)

        center.grid_rowconfigure(0, weight=9)
        center.grid_rowconfigure(1, weight=3)
        center.grid_rowconfigure(2, weight=2)

        # ==========================================
        # AI CORE
        # ==========================================

        self.ai_core = AICore(center)

        self.ai_core.grid(
            row=0,
            column=0,
            sticky="nsew",
            pady=(0, 10)
        )

        # ==========================================
        # WORLD MAP
        # ==========================================

        self.world_map = WorldMap(center)

        self.world_map.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(0, 10)
        )

        # ==========================================
        # PERFORMANCE GRAPH
        # ==========================================

        self.graph = PerformanceGraph(center)

        self.graph.grid(
            row=2,
            column=0,
            sticky="ew"
        )

        # ==========================================
        # RIGHT PANEL
        # ==========================================

        self.status = StatusPanel(self)

        self.status.grid(
            row=0,
            column=2,
            sticky="nsew",
            padx=(12, 0),
            pady=(0, 10)
        )

        # ==========================================
        # CONSOLE
        # ==========================================

        self.output = ctk.CTkTextbox(
            self,
            font=theme.CONSOLE_FONT,
            fg_color=theme.PANEL,
            corner_radius=20
        )

        self.output.grid(
            row=1,
            column=0,
            columnspan=3,
            sticky="nsew",
            padx=2,
            pady=(5, 5)
        )

        # ==========================================
        # TEXT INPUT (type a command instead of speaking)
        # ==========================================

        self.controls = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.controls.grid(
            row=2,
            column=1,
            pady=(5, 15),
            sticky="ew"
        )

        self.controls.grid_columnconfigure(0, weight=1)

        entry_row = ctk.CTkFrame(self.controls, fg_color="transparent")
        entry_row.pack(fill="x", pady=(0, 10))
        entry_row.grid_columnconfigure(0, weight=1)

        self.command_entry = ctk.CTkEntry(
            entry_row,
            placeholder_text="Type a command instead of speaking...",
            height=42,
            corner_radius=12,
            font=("Segoe UI", 14)
        )

        self.command_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.command_entry.bind("<Return>", self.send_typed_command)

        self.send_button = ctk.CTkButton(
            entry_row,
            text="Send",
            width=90,
            height=42,
            corner_radius=12,
            font=("Segoe UI", 14, "bold"),
            fg_color="#0D6EFD",
            hover_color="#0B5ED7",
            command=self.send_typed_command
        )

        self.send_button.grid(row=0, column=1)

        # ==========================================
        # MIC + STOP BUTTONS
        # ==========================================

        button_row = ctk.CTkFrame(self.controls, fg_color="transparent")
        button_row.pack()

        self.is_listening = False

        self.mic_button = ctk.CTkButton(
            button_row,
            text="🎤 Start Listening",
            width=220,
            height=45,
            corner_radius=12,
            font=("Segoe UI", 16, "bold"),
            fg_color="#0D6EFD",
            hover_color="#0B5ED7",
            command=self.toggle_listening
        )

        self.mic_button.pack(side="left", padx=(0, 10))

        self.stop_button = ctk.CTkButton(
            button_row,
            text="🛑 Stop",
            width=110,
            height=45,
            corner_radius=12,
            font=("Segoe UI", 16, "bold"),
            fg_color="#DC3545",
            hover_color="#BB2D3B",
            command=self.stop_speaking
        )

        self.stop_button.pack(side="left")

        # ==========================================
        # BOOT MESSAGES
        # ==========================================

        self.write("R.O.C.K.Y Boot Sequence Started...")
        self.write("Loading AI Core...")
        self.write("Loading Dashboard...")
        self.write("System Monitor Connected.")
        self.write("Performance Graph Ready.")
        self.write("Status Panel Online.")
        self.write("System Ready.")

    # ===================================================
    # CONSOLE
    # ===================================================

    def write(self, text, clear=False):

        if clear:
            self.output.delete("1.0", "end")

        timestamp = datetime.now().strftime("%H:%M:%S")

        self.output.insert(
            "end",
            f"[{timestamp}] {text}\n"
        )

        self.output.see("end")

    # ===================================================
    # VOICE LISTENER (continuous, toggle on/off)
    # ===================================================

    def set_listener(self, callback):
        # callback(starting: bool) -- True when the user just
        # turned listening ON, False when they just turned it OFF.
        self.listener_callback = callback

    def toggle_listening(self):

        self.is_listening = not self.is_listening

        if self.is_listening:

            self.mic_button.configure(
                text="⏹ Stop Listening",
                fg_color="#DC3545",
                hover_color="#BB2D3B"
            )
            self.write("🎤 Continuous listening started. I'll keep listening until you click Stop.")

        else:

            self.mic_button.configure(
                text="🎤 Start Listening",
                fg_color="#0D6EFD",
                hover_color="#0B5ED7"
            )
            self.write("⏹ Stopped listening.")

        if hasattr(self, "listener_callback"):
            self.listener_callback(self.is_listening)

    def set_mic_state(self, active):
        """
        Lets the app force the button back to the correct state
        from the background thread once the listening loop has
        actually exited (it may take a moment after Stop is
        clicked, since a listen() call already in progress has
        to finish first).
        """

        self.is_listening = active

        if active:
            self.mic_button.configure(
                text="⏹ Stop Listening",
                fg_color="#DC3545",
                hover_color="#BB2D3B"
            )
        else:
            self.mic_button.configure(
                text="🎤 Start Listening",
                fg_color="#0D6EFD",
                hover_color="#0B5ED7"
            )

    # ===================================================
    # TEXT COMMAND INPUT
    # ===================================================

    def set_text_command_callback(self, callback):
        self.text_command_callback = callback

    def send_typed_command(self, event=None):

        text = self.command_entry.get().strip()

        if not text:
            return

        self.command_entry.delete(0, "end")

        if hasattr(self, "text_command_callback"):
            self.text_command_callback(text)

    # ===================================================
    # STOP SPEAKING
    # ===================================================

    def set_stop_callback(self, callback):
        self.stop_callback = callback

    def stop_speaking(self):

        if hasattr(self, "stop_callback"):
            self.stop_callback()

        self.write("🛑 Stopped speaking.")