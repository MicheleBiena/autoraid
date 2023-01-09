import customtkinter as ctk
import tkinter as tk


class Boxes(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        ctk.CTkFrame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # checkboxes variables
        self.discord_var = tk.StringVar(value="off")
        self.telegram_var = tk.StringVar(value="off")
        self.preferentials_var = tk.StringVar(value="off")
        self.snitch_var = tk.StringVar(value="off")
        # checkboxes
        self.discord_alerts = ctk.CTkCheckBox(
            self,
            text="send discord alerts",
            command=self.discord_event,
            variable=self.discord_var,
            onvalue="on",
            offvalue="off",
        )

        self.telegram_alerts = ctk.CTkCheckBox(
            self,
            text="send telegram alerts",
            command=self.telegram_event,
            variable=self.telegram_var,
            onvalue="on",
            offvalue="off",
        )

        self.preferentials = ctk.CTkCheckBox(
            self,
            text="activate preferential chats",
            command=self.preferentials_event,
            variable=self.preferentials_var,
            onvalue="on",
            offvalue="off",
        )

        self.snitch_mode = ctk.CTkCheckBox(
            self,
            text="activate snitch mode",
            command=self.snitch_event,
            variable=self.snitch_var,
            onvalue="on",
            offvalue="off",
        )

        # setting up grid
        self.discord_alerts.grid(row=0, column=0, padx=20, pady=20, sticky="nswe")
        self.telegram_alerts.grid(row=0, column=1, padx=10, pady=20, sticky="nswe")
        self.preferentials.grid(row=0, column=2, padx=10, pady=20, sticky="nswe")
        self.snitch_mode.grid(row=0, column=3, padx=10, pady=20, sticky="nswe")

    def discord_event(self):
        pass

    def telegram_event(self):
        pass

    def preferentials_event(self):
        if self.preferentials_var.get() == "on":
            if self.snitch_var.get() == "on":
                self.snitch_mode.toggle()
            self.snitch_mode.configure(state="disabled")
        else:
            self.snitch_mode.configure(state="normal")

    def snitch_event(self):
        pass
