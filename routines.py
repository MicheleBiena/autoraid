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
embed = DiscordEmbed(title='DollyAutoRaid', description='Tera raid hosting', color=config['discord_embed_color'])

# TELEGRAM SETUP
bot = telebot.TeleBot(config['telegram_bot_token'])

def sendCommand(s, content):
    content += '\r\n' # important for the parser on the switch side
    # print("Comando: " + content)
    s.sendall(content.encode())

def sleepfor(seconds):
    # print("Aspetto " + str(seconds) + " secondi.")
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
    print("Sending password to discord webhook...")
    with open(base_address + 'image.jpg', "rb") as f:
        webhook.add_file(file=f.read(), filename="image.jpg")

    embed.set_title(raid_pokemon)
    embed.set_image(url="attachment://image.jpg")
    webhook.add_embed(embed)
    if len(extra_info) > 0: 
        add_field_to_embed(webhook, 'Extra info', extra_info)
    response = webhook.execute()
    webhook.remove_embeds()

def send_image(file_path, details):
    if len(config['telegram_preferential_ids']) > 0:
        print("Sending password to preferential contacts...")
        for pref in config['telegram_preferential_ids']:
            with open(file_path, 'rb') as f:
                bot.send_photo(pref, f, caption=details)
        sleep(15)
    with open(file_path, 'rb') as f:
        print("Sending password to telegram chats...")
        for id in config['telegram_chat_ids']:
            bot.send_photo(id, f, caption=details)
    
def send_telegram(raid_pokemon, extra_info):
    caption = "Tera Raid hosting\nPokémon: " + raid_pokemon
    if len(extra_info) > 0:
        caption += "\nExtra Info: " + extra_info
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

def send_telegram_finished(raid_pokemon, message):
    caption = "Finished Auto-Hosting for: " + raid_pokemon + "\nNumber of raids completed: " + message
    send_text(caption)

def send_discord_finished(raid_pokemon, message):
    embed.set_title("Stopped")
    embed.set_description("Finished Auto-Hosting for: " + raid_pokemon)
    remove_field_from_webhook(webhook, 'Extra Info')
    embed.add_embed_field(name='Number of raids completed: ', value=message)
    webhook.add_embed(embed)
    response = webhook.execute()
    webhook.remove_embeds()

def send_text(caption):
    if len(config['telegram_preferential_ids']) > 0:
        for pref in config['telegram_preferential_ids']:
            bot.send_message(pref, caption)
    for id in config['telegram_chat_ids']:
        bot.send_message(id, caption)

def send_finished(message, alert_data):
    channels = {
        "t": send_telegram_finished,
        "d": send_discord_finished
    }
    channel, raid_pokemon, extra_info = [value for key, value in alert_data.items()]

    if channel in channels:
        channels[channel](raid_pokemon, message)
    else:
        send_telegram_finished(raid_pokemon, message)
        send_discord_finished(raid_pokemon, message)

def add_field_to_embed(webhook, field_name, field_value):
    field_exists = False
    for field in webhook.embeds[0].fields:
        if field.name == field_name:
            field_exists = True
            break
    if not field_exists:
        webhook.add_field(name=field_name, value=field_value)

def remove_field_from_webhook(webhook, field_name):
    # Loop through the fields in the webhook
    for field in webhook.embeds[0].fields:
        # If the field name matches the field we want to remove, remove it
        if field.name == field_name:
            webhook.remove_field(field)
            break

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
    send_alerts(alert_data)
    sleep(60)
    print("Starting Raid")
    send_text("Starting Raid!")
    screenshot(s)
    send_alerts(alert_data)
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
    send_text("Raid finished, restarting the game...")
    sleep(5) 