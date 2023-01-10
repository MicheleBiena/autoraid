import customtkinter as ctk
import json
import os
from pathlib import Path

padding = 20


class Settings(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        ctk.CTkFrame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=4)
        self.rowconfigure(5, weight=4)
        self.rowconfigure(6, weight=4)

        self.config = {
            "switch-ip": "192.168.1.1",
            "discord_webhook_url": "webhook/url/discord",
            "discord_embed_color": "112233",
            "telegram_bot_token": "token:xxxx",
            "telegram_preferential_ids": [11111, 22222],
            "telegram_chat_ids": [33333, 44444],
        }

        self.config_file = Path("Autoraid.Windows/config.json")
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                self.config = json.load(f)
        with open(self.config_file, "w") as f:
            json.dump(self.config, f)

        self.ip_label = ctk.CTkLabel(self, text="Switch IP address", justify="right")
        self.ip_entry = ctk.CTkEntry(self)
        self.ip_entry.insert(0, self.config["switch-ip"])

        self.webhook_label = ctk.CTkLabel(
            self, text="Discord webhook url", justify="right"
        )
        self.webhook_entry = ctk.CTkEntry(self)
        self.webhook_entry.insert(0, self.config["discord_webhook_url"])

        self.embedColor_label = ctk.CTkLabel(
            self, text="Discord embed color", justify="right"
        )
        self.embedColor_entry = ctk.CTkEntry(self)
        self.embedColor_entry.insert(0, self.config["discord_embed_color"])

        self.token_label = ctk.CTkLabel(
            self, text="Telegram bot token", justify="right"
        )
        self.token_entry = ctk.CTkEntry(self)
        self.token_entry.insert(0, self.config["telegram_bot_token"])

        # list items
        self.pref_ids_label = ctk.CTkLabel(
            self, text="Preferential telegram chat ids\n(comma separated)"
        )
        self.pref_ids_text = ctk.CTkTextbox(self, height=15, width=15)
        pref_str = ",".join(str(i) for i in self.config["telegram_preferential_ids"])
        self.pref_ids_text.insert("end", pref_str)

        self.ids_label = ctk.CTkLabel(self, text="Telegram chat ids\n(comma separated)")
        self.ids_text = ctk.CTkTextbox(self, height=15, width=15)
        id_str = ",".join(str(i) for i in self.config["telegram_chat_ids"])
        self.ids_text.insert("end", id_str)

        # save button
        self.save_label = ctk.CTkLabel(self, text="")
        self.save_button = ctk.CTkButton(self, text="Save", command=self.save_settings)

        # pack the widgets

        self.ip_label.grid(row=0, column=0, sticky="nswe", padx=padding, pady=padding)
        self.ip_entry.grid(
            row=0, column=1, columnspan=2, sticky="nswe", padx=padding, pady=padding
        )
        self.webhook_label.grid(
            row=1, column=0, sticky="nswe", padx=padding, pady=padding
        )
        self.webhook_entry.grid(
            row=1, column=1, columnspan=2, sticky="nswe", padx=padding, pady=padding
        )
        self.embedColor_label.grid(
            row=2, column=0, sticky="nswe", padx=padding, pady=padding
        )
        self.embedColor_entry.grid(
            row=2, column=1, columnspan=2, sticky="nswe", padx=padding, pady=padding
        )
        self.token_label.grid(
            row=3, column=0, sticky="nswe", padx=padding, pady=padding
        )
        self.token_entry.grid(
            row=3, column=1, columnspan=2, sticky="nswe", padx=padding, pady=padding
        )
        self.pref_ids_label.grid(
            row=4, column=0, sticky="nswe", padx=padding, pady=padding
        )
        self.pref_ids_text.grid(
            row=4,
            column=1,
            sticky="nswe",
            padx=padding,
            pady=padding,
        )
        self.ids_label.grid(row=5, column=0, sticky="nswe", padx=padding, pady=padding)
        self.ids_text.grid(
            row=5,
            column=1,
            sticky="nswe",
            padx=padding,
            pady=padding,
        )
        self.save_label.grid(row=6, column=0, sticky="nswe", padx=padding, pady=padding)
        self.save_button.grid(
            row=6, column=1, sticky="nswe", padx=padding, pady=padding
        )

    def save_settings(self):
        # update the config file with the new values
        self.config["switch-ip"] = self.ip_entry.get()
        self.config["discord_webhook_url"] = self.webhook_entry.get()
        self.config["discord_embed_color"] = self.embedColor_entry.get()
        self.config["telegram_bot_token"] = self.token_entry.get()
        pref_ids_string = self.pref_ids_text.get("1.0", "end").rstrip()
        if len(pref_ids_string) > 0:
            self.config["telegram_preferential_ids"] = [
                int(x) for x in pref_ids_string.split(",")
            ]
        else:
            self.config["telegram_preferential_ids"] = []
        ids_string = self.ids_text.get("1.0", "end").rstrip()
        if len(ids_string) > 0:
            self.config["telegram_chat_ids"] = [int(x) for x in ids_string.split(",")]
        else:
            self.config["telegram_chat_ids"] = []

        # save the config file
        with open(self.config_file, "w") as configfile:
            self.save_label.configure(text="Configs saved! Restart the program!")
            json.dump(self.config, configfile)
