import threading

import customtkinter as ctk
from assistant.ai_brain import AIBrain
from assistant.commands import CommandProcessor
from tkinter import filedialog, simpledialog

from assistant.listener import Listener
from assistant.speaker import Speaker

from gui.topbar import TopBar
from gui.sidebar import Sidebar
from gui.dashboard import Dashboard
from gui.explorer import Explorer

from modules.wifi import scan_wifi
from modules.system import get_system_info
from modules.speedtest import run_speed_test
from modules.network import get_network_info
from modules.weather import get_weather
from modules.system_monitor import get_system_monitor
from modules.phone import get_phone_info


class RockyApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        # -----------------------------
        # App Settings
        # -----------------------------
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("🤖 R.O.C.K.Y")
        self.geometry("1400x850")
        self.minsize(1200, 700)

        self.configure(fg_color="#060B16")

        # -----------------------------
        # Top Bar
        # -----------------------------
        self.topbar = TopBar(self)
        self.topbar.pack(fill="x")

        # -----------------------------
        # Main Container
        # -----------------------------
        self.container = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.container.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        # -----------------------------
        # Sidebar
        # -----------------------------
        self.sidebar = Sidebar(
            self.container,
            self
        )

        self.sidebar.pack(
            side="left",
            fill="y",
            padx=(0, 15)
        )

        # -----------------------------
        # Dashboard
        # -----------------------------
        self.dashboard = Dashboard(self.container)

        self.dashboard.pack(
            side="right",
            fill="both",
            expand=True
        )

        # -----------------------------
        # Voice Assistant
        # -----------------------------
        self.listener = Listener()
        self.speaker = Speaker()

        # Ollama AI
        self.ai = AIBrain()

        # Command Processor
        self.command_processor = CommandProcessor(self)

        # True while continuous listening is active. The mic
        # button toggles this; the loop checks it each cycle.
        self.listening_active = False

        self.dashboard.set_listener(
            self.toggle_voice_assistant
        )

        self.dashboard.set_stop_callback(
            self.speaker.stop
        )

        self.dashboard.set_text_command_callback(
            self.handle_text_command
        )

        # -----------------------------
        # Start Live Dashboard
        # -----------------------------
        self.update_dashboard()
    # =====================================
    # LIVE DASHBOARD UPDATE
    # =====================================

    def update_dashboard(self):


        try:

            info = get_system_monitor()

            cpu = float(info["CPU Usage"].replace("%", "").strip())
            ram = float(info["RAM Usage"].replace("%", "").strip())
            disk = float(info["Disk Usage"].replace("%", "").strip())

            battery_text = info["Battery"]

            if battery_text == "No Battery":
                battery = 0
            else:
                battery = float(
                    battery_text.replace("%", "").strip()
                )

            self.dashboard.cpu.set_value(cpu)
            self.dashboard.ram.set_value(ram)
            self.dashboard.disk.set_value(disk)
            self.dashboard.battery.set_value(battery)

            self.dashboard.status.update_status(
                cpu=cpu,
                ram=ram,
                disk=disk,
                battery=battery,
                network="Connected",
                weather="25°C"
            )

        except Exception as e:
            print("Dashboard Update Error:", e)

        self.after(1000, self.update_dashboard)

        # =====================================
    # Voice Assistant
    # =====================================

    def toggle_voice_assistant(self, starting):
        """
        Called by the dashboard's mic button. starting=True means
        the user just turned listening ON; False means they just
        turned it OFF.
        """

        if starting:
            self.listening_active = True

            threading.Thread(
                target=self.continuous_voice_loop,
                daemon=True
            ).start()

        else:
            # Just flip the flag. The loop thread notices on its
            # NEXT iteration (it may already be mid-listen(), up
            # to ~8 seconds, before it actually stops).
            self.listening_active = False

    def continuous_voice_loop(self):
        """
        Keeps listening and processing commands back-to-back
        until listening_active is turned off. One bad command
        (misheard, a module error, etc.) does NOT stop the loop
        -- only clicking Stop does.
        """

        while self.listening_active:

            command = self.listener.listen()

            if command and self.listening_active:
                self.process_command(command)

        # Loop has fully exited -- now it's safe to reset the
        # button, since no more commands will be processed.
        self.after(
            0,
            lambda: self.dashboard.set_mic_state(False)
        )

    def handle_text_command(self, text):
        """
        Called by the dashboard when a command is typed instead
        of spoken. Runs on its own thread so the GUI doesn't
        freeze while Ollama/other calls are in progress.
        """

        threading.Thread(
            target=self.process_command,
            args=(text,),
            daemon=True
        ).start()

    def process_command(self, command):
        """
        The single shared pipeline for BOTH voice and typed
        commands: write it to the dashboard, run it through the
        command processor (with AI fallback), display and speak
        the response. Keeping this in one place means voice and
        text can never drift out of sync with each other.

        Errors are caught here (not by the caller) so a crash on
        ONE command never kills continuous listening and never
        silently fails a typed command either.
        """

        try:
            self.after(
                0,
                lambda: self.dashboard.write(f"👤 You: {command}")
            )

            response = self.command_processor.execute(command)

            if response == "Sorry. I don't know that command yet.":
                response = self.ai.ask(command)

            self.after(
                0,
                lambda: self.dashboard.write(f"🤖 Rocky: {response}")
            )

            self.speaker.speak(response)

        except Exception as e:

            print("Command processing error:", e)

            error_message = (
                "Sorry, something went wrong while "
                "processing that."
            )

            self.after(
                0,
                lambda: self.dashboard.write(f"⚠️ {error_message}")
            )

            try:
                self.speaker.speak(error_message)
            except Exception:
                pass

    
            # =====================================
    # Wi-Fi Scanner
    # =====================================

    def show_wifi(self):

        self.dashboard.write("📶 Scanning nearby Wi-Fi networks...")

        networks = scan_wifi()

        text = "📶 NEARBY WI-FI NETWORKS\n\n"

        if networks:
            for wifi in networks:
                text += f"• {wifi}\n"
        else:
            text += "No Wi-Fi networks found."

        self.dashboard.write(text)

    # =====================================
    # System Information
    # =====================================

    def show_system(self):

        info = get_system_info()

        text = "💻 SYSTEM INFORMATION\n\n"

        for key, value in info.items():
            text += f"{key}: {value}\n"

        self.dashboard.write(text)

    # =====================================
    # Live System Monitor
    # =====================================

    def show_monitor(self):

        info = get_system_monitor()

        text = "🖥 LIVE SYSTEM MONITOR\n\n"

        for key, value in info.items():
            text += f"{key}: {value}\n"

        self.dashboard.write(text)

    # =====================================
    # Internet Speed Test
    # =====================================

    def show_speed(self):

        self.dashboard.write(
            "🌐 Running Internet Speed Test...\nPlease wait..."
        )

        self.update()

        result = run_speed_test()

        text = "🌐 INTERNET SPEED TEST\n\n"

        for key, value in result.items():
            text += f"{key}: {value}\n"

        self.dashboard.write(text)

    # =====================================
    # Network Information
    # =====================================

    def show_network(self):

        info = get_network_info()

        text = "📡 NETWORK INFORMATION\n\n"

        for key, value in info.items():
            text += f"{key}: {value}\n"

        self.dashboard.write(text)

    # =====================================
    # Weather
    # =====================================

    def show_weather(self):

        city = simpledialog.askstring(
            "Weather",
            "Enter City Name:"
        )

        if not city:
            self.dashboard.write("Weather request cancelled.")
            return

        result = get_weather(city)

        text = "🌦 WEATHER REPORT\n\n"

        for key, value in result.items():
            text += f"{key}: {value}\n"

        self.dashboard.write(text)

    # =====================================
    # File Explorer
    # =====================================

    def show_files(self):

        folder = filedialog.askdirectory(
            title="Select Folder"
        )

        if folder:

            Explorer(
                self,
                folder
            )

            self.dashboard.write(
                f"📂 Opened Folder:\n{folder}"
            )

        else:

            self.dashboard.write(
                "File explorer cancelled."
            )

    # =====================================
    # Phone Information
    # =====================================

    def show_phone(self):

        self.dashboard.write("📱 Checking connected phone...")

        info = get_phone_info()

        text = "📱 PHONE INFORMATION\n\n"

        for key, value in info.items():
            text += f"{key}: {value}\n"

        self.dashboard.write(text)