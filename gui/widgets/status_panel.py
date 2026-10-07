import customtkinter as ctk
from gui.widgets.info_panel import InfoPanel


class StatusPanel(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(
            master,
            fg_color="transparent"
        )

        # ----------------------------
        # WEATHER
        # ----------------------------

        self.weather = InfoPanel(
            self,
            "🌤 Weather",
            "Loading..."
        )
        self.weather.pack(fill="x", pady=8)

        # ----------------------------
        # NETWORK
        # ----------------------------

        self.network = InfoPanel(
            self,
            "📡 Network",
            "Checking..."
        )
        self.network.pack(fill="x", pady=8)

        # ----------------------------
        # BATTERY
        # ----------------------------

        self.battery = InfoPanel(
            self,
            "🔋 Battery",
            "--"
        )
        self.battery.pack(fill="x", pady=8)

        # ----------------------------
        # CPU
        # ----------------------------

        self.cpu = InfoPanel(
            self,
            "🖥 CPU",
            "--"
        )
        self.cpu.pack(fill="x", pady=8)

        # ----------------------------
        # RAM
        # ----------------------------

        self.ram = InfoPanel(
            self,
            "💾 RAM",
            "--"
        )
        self.ram.pack(fill="x", pady=8)

        # ----------------------------
        # DISK
        # ----------------------------

        self.disk = InfoPanel(
            self,
            "💽 Disk",
            "--"
        )
        self.disk.pack(fill="x", pady=8)

        # ----------------------------
        # AI STATUS
        # ----------------------------

        self.status = InfoPanel(
            self,
            "🤖 AI Status",
            "ONLINE"
        )
        self.status.pack(fill="x", pady=8)

    # ===================================
    # UPDATE VALUES
    # ===================================

    def update_status(
        self,
        cpu,
        ram,
        disk,
        battery,
        network="Connected",
        weather="--"
    ):

        self.cpu.set_value(f"{cpu:.0f}%")
        self.ram.set_value(f"{ram:.0f}%")
        self.disk.set_value(f"{disk:.0f}%")
        self.battery.set_value(f"{battery:.0f}%")
        self.network.set_value(network)
        self.weather.set_value(weather)