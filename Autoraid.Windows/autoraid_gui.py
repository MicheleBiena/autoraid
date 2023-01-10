from Gui import bot, settings, log, boxes
from Core import autoraid
import customtkinter as ctk
import os
import json
import datetime
from pathlib import Path

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class MainWindow(ctk.CTk):

    # Initialize ctk using superconstructor
    def __init__(self):
        super().__init__()

        # change icon and title
        self.wm_title("Autoraid")
        self.center_window(1200, 640)
        self.iconbitmap(Path("Autoraid.Windows/orthworm.ico"))
        self.protocol("WM_DELETE_WINDOW", self.save_and_exit)

        # create a 1x2 grid system
        self.grid_columnconfigure(0, weight=5)
        self.grid_columnconfigure(1, weight=3)

        # create the two columns
        # column 1
        self.boxes = boxes.Boxes(self)
        self.boxes.grid(row=0, column=0, rowspan=1, sticky="nswe", padx=20, pady=20)

        self.bot = bot.Bot(self, callback=self.start_stop_bot)
        self.bot.grid(row=1, column=0, sticky="nswe", padx=20, pady=20)

        self.log = log.Log(self)
        self.log.grid(row=2, column=0, sticky="nswe", padx=20, pady=20)

        # column 2

        self.settings = settings.Settings(self)
        self.settings.grid(row=0, column=1, rowspan=3, sticky="nswe", padx=20, pady=20)

    def center_window(root, width, height):
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        root.geometry(f"{width}x{height}+{x}+{y}")

    def start_stop_bot(self):
        config = {}
        config_file = Path("Autoraid.Windows/config.json")
        if os.path.exists(config_file):
            with open(config_file, "r") as f:
                config = json.load(f)
            raider = autoraid.Autoraider(configs=config)
            if self.bot.bot_stopped:
                self.log.insert_text("Bot stopped\n")
                raider.stop_thread()
                self.log.insert_text("Hosted Raids: " + str(raider.hosted_raids) + "\n")
            else:
                alert_settings = [
                    self.boxes.discord_var.get(),
                    self.boxes.telegram_var.get(),
                    self.boxes.preferentials_var.get(),
                    self.boxes.snitch_var.get(),
                ]
                self.log.insert_text("Bot started\n")

                raider.start_thread(
                    self.log,
                    self.bot.fields.raid_boss_entry.get(),
                    self.bot.fields.extra_info_entry.get(),
                    alert_settings,
                    config,
                )

        else:
            self.log.insert_text("No configs loaded!\n")

    def save_and_exit(self):
        content = self.log.textbox.get("1.0", "end")

        now = datetime.datetime.now()
        file_name = now.strftime("%d_%m_%H_%M.txt")
        if not os.path.exists("Logs"):
            os.makedirs("Logs")
        with open(Path("Logs", file_name), "w") as f:
            f.write(content)

        self.destroy()


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
