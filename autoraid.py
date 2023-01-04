import socket
import routines as r
from time import sleep
from config_loader import CONFIG
import telegram_handler as th 

# CONNECTION
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((CONFIG["switch-ip"], 6000))

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

snitch_mode = False
if channel in ["t", ""] and len(CONFIG['telegram_preferential_ids']) == 0:
    while True:
        choice = input('Do you want to activate snitch mode for telegram? (y/n) ')
        if choice == 'y':
            snitch_mode = True
            break
        elif choice == 'n':
            break
        else: 
            print("Invalid option. Try again")
    

alert_data = {
    "channel" : channel,
    "raid_pokemon" : raid_pokemon,
    "extra_info" : extra_info,
    "snitch_mode" : snitch_mode    
}

hosted_raids = 0

# MAIN LOOP
sleep(1.5)
try:
    while True:
        r.connect(s)
        r.setup_raid(s, alert_data)
        hosted_raids = hosted_raids + 1
        r.raid_execution(s)
        r.quitGame(s)
        r.enterGame(s)
except KeyboardInterrupt:
    r.send_finished(str(hosted_raids), alert_data)
