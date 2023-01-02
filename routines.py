from time import sleep
import binascii
from PIL import Image
from io import BytesIO
import json
from discord_webhook import DiscordEmbed, DiscordWebhook
import telebot

# IMPORTANT: CHANGE THIS!
base_address = "C:\\autoraid\\autoraid\\"

# EXTRACT JSON DATA
with open(base_address + 'connection_info.json') as file:
    config = json.load(file)

with open(base_address + 'ram_pointers.json') as file:
    pointers = json.load(file)

# DISCORD WEBHOOK SETUP
webhook = DiscordWebhook(config['discord_webhook_url'])
embed = DiscordEmbed(title='DollyAutoRaid', description='Tera Raid in corso', color=config['discord_embed_color'])

# TELEGRAM SETUP
bot = telebot.TeleBot(config['telegram_bot_token'])

def sendCommand(s, content):
    content += '\r\n' # important for the parser on the switch side
    # print("Comando: " + content)
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
    image.save((base_address + 'image.jpg'), 'JPEG')

def send_discord(raid_pokemon, extra_info):
    with open(base_address + 'image.jpg', "rb") as f:
        webhook.add_file(file=f.read(), filename="image.jpg")

    embed.set_title(raid_pokemon)
    embed.set_image(url="attachment://image.jpg")
    if len(extra_info) > 0: 
        embed.add_embed_field(name='Informazioni aggiuntive', value=extra_info)
    webhook.add_embed(embed)
    response = webhook.execute()
    webhook.remove_embeds()

def send_image(file_path, details):
    with open(file_path, 'rb') as f:
        for id in config['telegram_chat_ids']:
            bot.send_photo(id, f, caption=details)
    

def send_telegram(raid_pokemon, extra_info):
    caption = "Tera Raid in corso\nPokémon: " + raid_pokemon
    if len(extra_info) > 0:
        caption += "\nInfo Aggiuntive: " + extra_info
    send_image(base_address + 'image.jpg', caption)

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
    # print(onOverworld.decode())
    return onOverworld[:-1].decode() == "11"

def isConnected(s):
    checkPointer(s, pointers['isConnectedPointer'], 1)
    onOverworld = s.recv(3)
    # print(onOverworld.decode())
    return onOverworld[:-1].decode() == "01"

def click(s, button):
    sendCommand(s, 'click ' + button)

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
        readyForRaid = isConnected(s) and isOnOverworld(s)
    click(s, "A") # entro nel raid
    sleep(2)
    click(s, "A") # affronta in gruppo
    sleep(2)
    click(s, "A") # solo chi conosce la password
    sleep(6) # per uno screenshot adatto
    screenshot(s)
    send_alerts(alert_data)
    sleep(120)
    print("Starting Raid")
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
        inRaid = not isOnOverworld(s)
        sleep(5)
    print("Raid Finished!") 
    sleep(5) 