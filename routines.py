from time import sleep
import binascii
from PIL import Image
from io import BytesIO
import json
from discord_webhook import DiscordEmbed, DiscordWebhook
import telebot


# EXTRACT JSON DATA
with open('connection_info.json') as file:
    config = json.load(file)

with open('ram_pointers.json') as file:
    pointers = json.load(file)

# DISCORD WEBHOOK SETUP
webhook = DiscordWebhook(config['discord_webhook_url'])
embed = DiscordEmbed(title='DollyAutoRaid', description='Tera Raid in corso', color=config['discord_embed_color'])

# TELEGRAM SETUP
bot = telebot.TeleBot(config['telegram_bot_token'])

def sendCommand(s, content):
    content += '\r\n' #important for the parser on the switch side
    print("Comando: " + content)
    s.sendall(content.encode())

def sleepfor(seconds):
    print("Aspetto " + str(seconds) + " secondi.")
    sleep(seconds)

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

def send_discord(raid_pokemon, extra_info):
    with open('image.jpg', "rb") as f:
        webhook.add_file(file=f.read(), filename="image.jpg")

    embed.set_title(raid_pokemon)
    embed.set_image(url="attachment://image.jpg")
    if len(extra_info) > 0: 
        embed.add_embed_field(name='Informazioni aggiuntive', value=extra_info)
    webhook.add_embed(embed)
    response = webhook.execute()
    print(response)

def send_image(file_path, details):
    with open(file_path, 'rb') as f:
        for id in config['telegram_chat_ids']:
            bot.send_photo(id, f, caption=details)
    

def send_telegram(raid_pokemon, extra_info):
    caption = "Tera Raid in corso\nPokémon: " + raid_pokemon
    if len(extra_info) > 0:
        caption += "\nInfo Aggiuntive: " + extra_info
    send_image('image.jpg', caption)

def send_alerts(alert_data):
    channels = {
        "t": send_telegram,
        "d": send_discord
    }
    channel, raid_pokemon, extra_info = [value for key, value in alert_data.items()]

    if channel in channels:
        channels[channel](raid_pokemon, extra_info)
    else:
        send_telegram(raid_pokemon, extra_info)
        send_discord(raid_pokemon, extra_info)

# ALL COMMANDS
def isOnOverworld(s):
    checkPointer(s, pointers['overworldPointer'], 1)
    onOverworld = s.recv(3)
    print(onOverworld.decode())
    return onOverworld[:-1].decode() == "11"

def isConnected(s):
    checkPointer(s, pointers['isConnectedPointer'], 1)
    onOverworld = s.recv(3)
    print(onOverworld.decode())
    return onOverworld[:-1].decode() == "01"

def click(s, button):
    sendCommand(s, 'click ' + button)

def quitGame(s):
    print("Quitting the game")
    click(s, "B")
    sleepfor(0.2)
    click(s, "HOME")
    sleepfor(0.8)
    click(s, "X")
    sleepfor(0.2)
    click(s, "X")
    sleepfor(0.4)
    click(s, "A")
    sleepfor(0.2)
    click(s, "A")
    sleepfor(3)

def enterGame(s):
    print("Restarting the game")
    click(s, "A")
    sleepfor(0.2)
    click(s, "A")
    sleepfor(1.3)
    click(s, "A")
    sleepfor(0.2)
    click(s, "A")
    sleepfor(1.3)
    sleepfor(16)
    click(s, "A")
    sleepfor(1.3)
    click(s, "A")
    sleepfor(1.3)
    
def connect(s):
    ready = False
    while ready is not True:
        sleepfor(1)
        ready = isOnOverworld(s)
    sleepfor(1)
    click(s, "X")
    sleepfor(1)
    click(s, "L")
    connected = False
    while connected is not True:
        sleepfor(2)
        connected = isConnected(s)
    sleepfor(4)
    click(s, "A")
    sleepfor(0.2)
    click(s, "A")
    sleepfor(1.3)
    click(s, "B")
    sleepfor(0.2)
    click(s, "B")
    sleepfor(1.3)

def setup_raid(s, alert_data):
    readyForRaid = False
    while readyForRaid is not True:
        sleepfor(0.5)
        readyForRaid = isConnected(s) and isOnOverworld(s)
    click(s, "A") # entro nel raid
    sleepfor(2)
    click(s, "A") # affronta in gruppo
    sleepfor(2)
    sendCommand(s, "click A") # solo chi conosce la password
    sleepfor(6) # per uno screenshot adatto
    screenshot(s)
    send_alerts(alert_data)
    sleepfor(120)
    sendCommand(s, "click A")
    sleepfor(3)
    sendCommand(s, "click A")
    
def raid_execution(s):
    inRaid = True
    while inRaid:
        click(s, "A")
        sleepfor(0.2)
        click(s, "A")
        sleepfor(1.3)
        click(s, "A")
        sleepfor(0.2)
        click(s, "A")
        sleepfor(1.3) 
        click(s, "A")
        sleepfor(0.2)
        click(s, "A")
        sleepfor(1.3) # Mashing A-button
        inRaid = not isOnOverworld(s)
        sleepfor(5) 
    sleepfor(6) 