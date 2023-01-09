from time import sleep
import binascii
from PIL import Image
from io import BytesIO
import json
from Core import telegram_handler as tel
from Core import discord_handler as disc

with open("Autoraid.Windows\\Core\\ram_pointers.json") as file:
    pointers = json.load(file)

# RAM CHECK
def checkPointer(s, pointer, length):
    request = "pointerPeek " + str(length)
    for jump in pointer:
        request += " " + jump
    sendCommand(s, request)


def screenshot(s):
    totalData = bytearray()
    sendCommand(s, "pixelPeek")
    while True:
        data = s.recv(1024)
        if (idx := data.find(b"\n")) != -1:
            totalData.extend(data[:idx])
            break
        totalData.extend(data)

    screen = binascii.unhexlify(totalData)

    image = Image.open(BytesIO(screen))
    image.save(("Autoraid.Windows\\Core\\image.jpg"), "JPEG")


# IMAGE PROCESSING


def cropScreenshot():
    image = Image.open("Autoraid.Windows\\Core\\image.jpg")
    cropped = image.crop((180, 360, 650, 630))
    cropped.save("Autoraid.Windows\\Core\\image.jpg")


# ALERTS HANDLING

# Combinator of all the different function to send a password to the users
def send_alerts(raid_pokemon, extra_info, log, alert_data):
    messageList = {}
    # If the user chose specific channels, the right functions are called
    if alert_data["telegram_alert"]:
        messageList = tel.send_password(
            raid_pokemon, extra_info, log, alert_data["preferentials"]
        )
    if alert_data["discord_alert"]:
        disc.send_password(raid_pokemon, extra_info, log)
    return messageList


def send_info_telegram(message, alert_data):
    if alert_data["telegram_alert"]:
        tel.send_telegram_text(message, alert_data["preferentials"])


# SYSBOT-BASE COMMAND HELPER
def sendCommand(s, content):
    content += "\r\n"  # important for the parser on the switch side
    # print("Comando: " + content)
    s.sendall(content.encode())


def isOnOverworld(s):
    checkPointer(s, pointers["overworldPointer"], 1)
    onOverworld = s.recv(3)
    # print(onOverworld.decode())
    return onOverworld[:-1].decode() == "11"


def isConnected(s):
    checkPointer(s, pointers["isConnectedPointer"], 1)
    onOverworld = s.recv(3)
    # print(onOverworld.decode())
    return onOverworld[:-1].decode() == "01"


def click(s, button):
    sendCommand(s, "click " + button)


# ROUTINES


def quitGame(s, log):
    log.insert_text("Quitting the game\n")
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


def enterGame(s, log):
    log.insert_text("Restarting the game\n")
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


def connect(s, alert_data, log):
    send_info_telegram("Connecting online\n", alert_data)
    log.insert_text("Connecting...\n")
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


def setup_raid(s, raid_pokemon, extra_info, alert_data, log):
    log.insert_text("Entering Raid\n")
    readyForRaid = False
    while readyForRaid is not True:
        sleep(0.5)
        click(s, "B")
        readyForRaid = isConnected(s) and isOnOverworld(s)
    sleep(2)
    click(s, "A")  # entro nel raid
    sleep(3)
    click(s, "A")  # affronta in gruppo
    sleep(2)
    click(s, "A")  # solo chi conosce la password
    sleep(10)  # per uno screenshot adatto
    screenshot(s)
    messageList = {}
    messageList = send_alerts(raid_pokemon, extra_info, log, alert_data)
    sleep(60)
    log.insert_text("Starting Raid\n")
    send_info_telegram("Starting Raid!", alert_data)
    if alert_data["snitch_mode"] and alert_data["telegram_alert"]:
        screenshot(s)
        cropScreenshot()
        tel.send_snitch(messageList, log)
    click(s, "A")
    sleep(3)
    click(s, "A")


def raid_execution(s, alert_data, log):
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
        sleep(1.3)  # Mashing A-button
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
        click(
            s, "B"
        )  # Mashing B-button (in case the raid is lost it goes back to overworld)
        sleep(1.3)
        inRaid = not isOnOverworld(s)
        sleep(5)
    log.insert_text("Raid Finished!\n")
    send_info_telegram("Raid finished, restarting the game...", alert_data)
    sleep(5)
