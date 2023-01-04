from time import sleep
import binascii
from PIL import Image
from io import BytesIO
import json
import telegram_handler as tel 
import discord_handler as disc

with open('ram_pointers.json') as file:
    pointers = json.load(file)

# RAM CHECK
def checkPointer(s, pointer, length):
    request = "pointerPeek " + str(length) 
    for jump in pointer:
        request += (" " + jump)
    sendCommand(s, request)

def screenshot(s):
    totalData = bytearray()
    sendCommand(s, "pixelPeek")
    while True:
        data = s.recv(1024)
        if (idx := data.find(b'\n')) != -1:
            totalData.extend(data[:idx])
            break
        totalData.extend(data)
    
    screen = binascii.unhexlify(totalData)

    image = Image.open(BytesIO(screen))
    image.save(('image.jpg'), 'JPEG')

# IMAGE PROCESSING

def cropScreenshot():
    image = Image.open('image.jpg')
    cropped = image.crop((180, 360, 650, 630))
    cropped.save('image.jpg')
    
# ALERTS HANDLING

# Combinator of all the different function to send a password to the users
def send_alerts(alert_data):
    messageList = {}
    # If the user chose specific channels, the right functions are called
    
    channel, raid_pokemon, extra_info, snitch_mode = [value for key, value in alert_data.items()]

    if channel == "t":
        messageList = tel.send_password(raid_pokemon, extra_info)
    elif channel == "d":
        disc.send_password(raid_pokemon, extra_info)
    else: # in this case we call every function
        messageList = tel.send_password(raid_pokemon, extra_info)
        disc.send_password(raid_pokemon, extra_info)
    return messageList

# Combinator of all the different function to notify that the raid is over
def send_finished(message, alert_data):
    channels = {
        "t": tel.send_telegram_finished,
        "d": disc.send_discord_finished
    }
    channel, raid_pokemon, extra_info, snitch_mode = [value for key, value in alert_data.items()]

    if channel in channels:
        channels[channel](raid_pokemon, message)
    else:
        tel.send_telegram_finished(raid_pokemon, message)
        disc.send_discord_finished(raid_pokemon, message)

# SYSBOT-BASE COMMAND HELPER
def sendCommand(s, content):
    content += '\r\n' # important for the parser on the switch side
    # print("Comando: " + content)
    s.sendall(content.encode())

def isOnOverworld(s):
    checkPointer(s, pointers['overworldPointer'], 1)
    onOverworld = s.recv(3)
    # print(onOverworld.decode())
    return onOverworld[:-1].decode() == "11"

def isConnected(s):
    checkPointer(s, pointers['isConnectedPointer'], 1)
    onOverworld = s.recv(3)
    # print(onOverworld.decode())
    return onOverworld[:-1].decode() == "01"

def click(s, button):
    sendCommand(s, 'click ' + button)

# ROUTINES 

def quitGame(s):
    print("Quitting the game")
    click(s, "B")
    sleep(0.2)
    click(s, "HOME")
    sleep(0.8)
    click(s, "X")
    sleep(0.2)
    click(s, "X")
    sleep(0.4)
    click(s, "A")
    sleep(0.2)
    click(s, "A")
    sleep(3)

def enterGame(s):
    print("Restarting the game")
    click(s, "A")
    sleep(0.2)
    click(s, "A")
    sleep(1.3)
    click(s, "A")
    sleep(0.2)
    click(s, "A")
    sleep(1.3)
    sleep(16)
    click(s, "A")
    sleep(1.3)
    click(s, "A")
    sleep(1.3)
    
def connect(s):
    tel.send_telegram_text("Connecting online")
    print("Connecting...")
    ready = False
    while ready is not True:
        sleep(1)
        ready = isOnOverworld(s)
    sleep(1)
    click(s, "X")
    sleep(1)
    click(s, "L")
    connected = False
    while connected is not True:
        sleep(2)
        connected = isConnected(s)
    sleep(5)
    click(s, "A")
    sleep(0.2)
    click(s, "A")
    sleep(1.3)
    click(s, "B")
    sleep(0.2)
    click(s, "B")
    sleep(1.3)

def setup_raid(s, alert_data):
    print("Entering Raid")
    readyForRaid = False
    while readyForRaid is not True:
        sleep(0.5)
        click(s, "B")
        readyForRaid = isConnected(s) and isOnOverworld(s)
    sleep(2)
    click(s, "A") # entro nel raid
    sleep(3)
    click(s, "A") # affronta in gruppo
    sleep(2)
    click(s, "A") # solo chi conosce la password
    sleep(10) # per uno screenshot adatto
    screenshot(s)
    messageList = {}
    messageList = send_alerts(alert_data)
    sleep(60)
    print("Starting Raid")
    tel.send_telegram_text("Starting Raid!")
    if alert_data["snitch_mode"]: 
        screenshot(s)
        cropScreenshot()
        tel.send_snitch(messageList)
    click(s, "A")
    sleep(3)
    click(s, "A")
    
def raid_execution(s):
    inRaid = True
    while inRaid:
        click(s, "A")
        sleep(0.2)
        click(s, "A")
        sleep(1.3)
        click(s, "A")
        sleep(0.2)
        click(s, "A")
        sleep(1.3) 
        click(s, "A")
        sleep(0.2)
        click(s, "A")
        sleep(1.3) # Mashing A-button
        click(s, "B")
        sleep(0.2)
        click(s, "B")
        sleep(1.3)
        click(s, "B")
        sleep(0.2)
        click(s, "B")
        sleep(1.3) 
        click(s, "B")
        sleep(0.2)
        click(s, "B") # Mashing B-button (in case the raid is lost it goes back to overworld)
        sleep(1.3)
        inRaid = not isOnOverworld(s)
        sleep(5)
    print("Raid Finished!") 
    tel.send_telegram_text("Raid finished, restarting the game...")
    sleep(5) 
