#Simple example on how to connect to and send commands to the sys module.
#The example is for Pokemon Sword/Shield, it reads a .ek8 file from a certain file path, injects it into box1slot1
#and starts a surprise trade with the given pokemon. It waits a certain amount of time (hoping the trade has completed)
#before retrieving the new pokemon. Finally it extracts the pokemons .ek8 data from the game and saves it to the hard drive.
#The script assumes the game is set up in a way that the character is not currently in any menus and that the cursor of the
#pokebox is on box1slot1.

#The script isn't exactly robust, there are many ways to make it better (for example one could compare the box1slot1 data in
#RAM with that of the pokemon sent to see if a trade has been found and if not back out of the menu to search for another 10 
#seconds or so instead of waiting a fixed 45 seconds), but it is rather meant as a showcase of the functionalites of the 
#sysmodule anyway.

#Commands:
#make sure to append \r\n to the end of the command string or the switch args parser might not work
#responses end with a \n (only poke has a response atm)

#click A/B/X/Y/LSTICK/RSTICK/L/R/ZL/ZR/PLUS/MINUS/DLEFT/DUP/DDOWN/DRIGHT/HOME/CAPTURE
#press A/B/X/Y/LSTICK/RSTICK/L/R/ZL/ZR/PLUS/MINUS/DLEFT/DUP/DDOWN/DRIGHT/HOME/CAPTURE
#release A/B/X/Y/LSTICK/RSTICK/L/R/ZL/ZR/PLUS/MINUS/DLEFT/DUP/DDOWN/DRIGHT/HOME/CAPTURE

#peek <address in hex, prefaced by 0x> <amount of bytes, dec or hex with 0x>
#poke <address in hex, prefaced by 0x> <data, if in hex prefaced with 0x>

#setStick LEFT/RIGHT <xVal from -0x8000 to 0x7FFF> <yVal from -0x8000 to 0x7FFF


import socket
import routines as r
import time

# CONNECTION
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.1.3", 6000))

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
    r.quitGame(s)
    r.enterGame(s)
    r.connect(s)
    r.setup_raid(s, alert_data)
    r.raid_execution(s)


