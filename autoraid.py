import socket
import routines as r
import time
import json

base_folder = r.base_address

with open (base_folder + "connection_info.json") as f:
    config = json.load(f)

# CONNECTION
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((config["switch-ip"], 6000))

# RAID INFO
raid_pokemon = input('Raid Pokémon: ')
extra_info = input('Extra Info (press Enter to skip): ')
options = ["t", "d", ""]
while True: 
    channel = input('Do you want to send Discord or Telegram alerts? (t/d - press Enter for both): ')
    if channel in options:
        break
    else:
        print("Invalid option. Try again")

alert_data = {
    "channel" : channel,
    "raid_pokemon" : raid_pokemon,
    "extra_info" : extra_info
}

hosted_raids = 0

# MAIN LOOP
time.sleep(1.5)
try:
    while True:
        r.connect(s)
        r.setup_raid(s, alert_data)
        r.raid_execution(s)
        r.quitGame(s)
        hosted_raids = hosted_raids + 1
        r.enterGame(s)
except KeyboardInterrupt:
    r.send_finished(str(hosted_raids), alert_data)


