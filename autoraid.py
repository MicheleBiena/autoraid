import socket
import routines as r
import time
import json

with open ("connection_info.json") as f:
    config = json.load(f)

# CONNECTION
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((config["switch-ip"], 6000))

# RAID INFO
raid_pokemon = input('Pokémon da Hostare: ')
extra_info = input('Info aggiuntive (premi invio per non aggiungere): ')
options = ["t", "d", ""]
while True: 
    channel = input('Vuoi inviare notifiche su telegram o discord (t/d - premi invio per inviare a entrambi): ')
    if channel in options:
        break
    else:
        print("Opzione invalida.")

alert_data = {
    "channel" : channel,
    "raid_pokemon" : raid_pokemon,
    "extra_info" : extra_info
}


# MAIN LOOP
time.sleep(1.5)
while True:
    r.connect(s)
    r.setup_raid(s, alert_data)
    r.raid_execution(s)
    r.quitGame(s)
    r.enterGame(s)

