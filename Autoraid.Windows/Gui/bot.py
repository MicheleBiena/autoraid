import customtkinter as ctk
import os
from pathlib import Path

class Bot(ctk.CTkFrame):
    def __init__(self, parent, callback, *args, **kwargs):
        ctk.CTkFrame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.callback = callback

        self.bot_stopped = True

        self.columnconfigure(0, weight=1)
        # main page widgets
        self.button = ctk.CTkButton(self, text="Run Bot", command=self.button_callback)
        self.button.grid(row=0, column=0, padx=50, pady=50)

        self.fields = RaidInfo(self)
        self.fields.grid(row=1, column=0, padx=10, pady=10)

    def button_callback(self):
        configs = Path("Autoraid.Windows/config.json")
        if os.path.exists(configs):
            if self.bot_stopped:
                self.bot_stopped = False
                self.button.configure(
                    text="Stop Bot",
                    fg_color=("#DB3E39", "#821D1A"),
                    hover_color=("#A33329", "#441612"),
                )
            else:
                self.bot_stopped = True
                self.button.configure(
                    text="Run Bot",
                    fg_color=("#3a7ebf", "#1f538d"),
                    hover_color=("#325882", "#14375e"),
                )

        self.callback()


class RaidInfo(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        ctk.CTkFrame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # two fields to input the raid info
        self.raid_boss_label = ctk.CTkLabel(self, text="Raid Boss")
        self.raid_boss_entry = ctk.CTkEntry(self)

        self.extra_info_label = ctk.CTkLabel(self, text="Extra Info")
        self.extra_info_entry = ctk.CTkEntry(self)

        # grid
        self.raid_boss_label.grid(row=0, column=0, sticky="nswe", padx=20, pady=10)
        self.raid_boss_entry.grid(row=1, column=0, sticky="nswe", padx=20, pady=10)

        self.extra_info_label.grid(row=0, column=1, sticky="nswe", padx=20, pady=10)
        self.extra_info_entry.grid(row=1, column=1, sticky="nswe", padx=20, pady=10)
