import customtkinter as ctk
import datetime


class Log(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        ctk.CTkFrame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # log page widgets
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.textbox = ctk.CTkTextbox(self)
        self.textbox.grid(row=0, column=0, sticky="nswe")

        self.textbox.insert("1.0", "Log: \n")
        self.text = self.textbox.get("1.0", "end")

        self.textbox.configure(state="disabled")

    def insert_text(self, text):
        now = datetime.datetime.now()
        toInsert = (now.strftime("[%H:%M] - ")) + text
        self.textbox.configure(state="normal")
        self.textbox.insert("end", toInsert)
        self.textbox.see("end")
        self.textbox.configure(state="disabled")
