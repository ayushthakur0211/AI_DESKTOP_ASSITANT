import os
import customtkinter as ctk
from tkinter import ttk
from modules.file_manager import open_file


class Explorer(ctk.CTkToplevel):

    def __init__(self, master, start_folder):
        super().__init__(master)

        self.title("📁 R.O.C.K.Y File Explorer")
        self.geometry("950x600")

        self.current_folder = start_folder
        self.history = []

        # ==========================
        # Top Toolbar
        # ==========================

        toolbar = ctk.CTkFrame(self)
        toolbar.pack(fill="x", padx=10, pady=10)

        self.back_btn = ctk.CTkButton(
            toolbar,
            text="⬅ Back",
            width=90,
            command=self.go_back
        )
        self.back_btn.pack(side="left", padx=5)

        self.refresh_btn = ctk.CTkButton(
            toolbar,
            text="🔄 Refresh",
            width=90,
            command=lambda: self.load_folder(self.current_folder)
        )
        self.refresh_btn.pack(side="left", padx=5)

        self.path = ctk.CTkEntry(toolbar)

        self.path.pack(
            side="left",
            fill="x",
            expand=True,
            padx=10
        )

        # ==========================
        # File List
        # ==========================

        columns = ("Name", "Type", "Size")

        self.tree = ttk.Treeview(
            self,
            columns=columns,
            show="headings"
        )

        self.tree.heading("Name", text="Name")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Size", text="Size")

        self.tree.column("Name", width=500)
        self.tree.column("Type", width=120)
        self.tree.column("Size", width=120)

        self.tree.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.tree.bind("<Double-1>", self.open_selected)

        self.load_folder(start_folder)

    # -----------------------------------
    def load_folder(self, folder):

        self.current_folder = folder

        self.path.delete(0, "end")
        self.path.insert(0, folder)

        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            for name in sorted(os.listdir(folder)):

                full_path = os.path.join(folder, name)

                if os.path.isdir(full_path):
                    file_type = "Folder"
                    size = ""
                else:
                    file_type = "File"
                    size = f"{os.path.getsize(full_path)} B"

                self.tree.insert(
                    "",
                    "end",
                    values=(name, file_type, size)
                )

        except Exception as e:
            print("Error:", e)

    def open_selected(self, event):

        selected = self.tree.selection()

        if not selected:
            return

        values = self.tree.item(selected[0], "values")

        name = values[0]
        item_type = values[1]

        full_path = os.path.join(self.current_folder, name)

        if item_type == "Folder":
            self.history.append(self.current_folder)
            self.load_folder(full_path)
        else:
            open_file(full_path)

    def go_back(self):

        if self.history:
            previous = self.history.pop()
            self.load_folder(previous)