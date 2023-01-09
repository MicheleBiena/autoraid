import socket
from Core import routines as r, telegram_handler as tel
from time import sleep
from threading import Thread

IP = "switch-ip"
WEB_URL = "discord_webhook_url"
COLOR = "discord_embed_color"
TOKEN = "telegram_bot_token"
PREF = "telegram_preferential_ids"
IDS = "telegram_chat_ids"


class Autoraider:
    def __init__(self, configs):
        self.hosted_raids = 0
        self.log = ""
        self.raid_pokemon = ""
        self.extra_info = ""
        self.alerts = {}
        self.configs = configs

        # connection
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(5)

    def start_thread(self, log, raid_pokemon, extra_info, alert_settings, configs):
        global stop
        stop = 0

        t = Thread(
            target=self.startBot,
            args=(log, raid_pokemon, extra_info, alert_settings, configs),
        )
        t.start()

    def stop_thread(self):
        """
        if ("telegram_alert" in self.alerts) and self.alerts["telegram_alert"] is True:
            tel.send_telegram_finished(
                self.raid_pokemon, str(self.hosted_raids), self.alerts["preferentials"]
            )
        """
        global stop
        stop = 1

    def alert_dict(self, alert_list):
        alerts = {
            "discord_alert": False,
            "telegram_alert": False,
            "preferentials": False,
            "snitch_mode": False,
        }

        # tuple from alerts and alert_list
        values = list(zip(alerts.keys(), alert_list))

        for key, value in values:
            bool_value = False
            if value == "on":
                bool_value = True
            alerts[key] = bool_value

        return alerts

    def startBot(self, log, raid_pokemon, extra_info, alert_settings, configs):

        # MAIN LOOP
        try:
            self.socket.connect((self.configs[IP], 6000))
            # RAID INFO
            self.log = log
            self.raid_pokemon = raid_pokemon
            self.extra_info = extra_info
            self.alerts = self.alert_dict(alert_settings)
            self.config = configs
            while stop == 0:
                sleep(1.5)

                r.connect(self.socket, self.alerts, self.log)
                if stop == 1:
                    break
                r.setup_raid(
                    self.socket,
                    self.raid_pokemon,
                    self.extra_info,
                    self.alerts,
                    self.log,
                )
                if stop == 1:
                    break
                self.hosted_raids = self.hosted_raids + 1
                self.log.insert_text("Hosted Raids: " + str(self.hosted_raids) + "\n")
                r.raid_execution(self.socket, self.alerts, self.log)
                if stop == 1:
                    break
                r.quitGame(self.socket, self.log)
                if stop == 1:
                    break
                r.enterGame(self.socket, self.log)

        except socket.timeout:
            log.insert_text("No response from your switch, check if it's connected\n")
            self.stop_thread()
        except ConnectionRefusedError:
            log.insert_text("No response, check your IP\n")
            self.stop_thread
