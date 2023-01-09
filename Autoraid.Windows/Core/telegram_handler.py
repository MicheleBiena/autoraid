import telebot
from Core import config_loader as conf_load
from time import sleep

# TELEGRAM SETUP
bot = telebot.TeleBot(conf_load.config.get("telegram_bot_token", ""))
PASSWORD_CAPTION = "Tera Raid hosting\nPokémon: "
SNITCH_MODE_CAPTION = "Connected users: "

# sends a telegram message with a screenshot of the password screen
def send_password(raid_pokemon, extra_info, log, preferentials):
    caption = PASSWORD_CAPTION + raid_pokemon
    # We add an extra line if we have extra info to display
    if len(extra_info) > 0:
        caption += "\nExtra Info: " + extra_info
    message_list = send_telegram_image(caption, log, preferentials)
    return message_list


# sends a telegram message with a screenshot of the raid party screen
def send_snitch(messageList, log):
    with open("Autoraid.Windows\\Core\\image.jpg", "rb") as f:
        media = telebot.types.InputMediaPhoto(f, caption=SNITCH_MODE_CAPTION)
        log.insert_text("Sending snitches to telegram chats...\n")
        for chat_id, message_id in messageList.items():
            bot.edit_message_media(
                chat_id=int(chat_id), message_id=message_id, media=media
            )


# loops through all the telegram ids to send the message
def send_telegram_image(details, log, preferentials):
    # preferential chats get the password 15 seconds before all others
    if len(conf_load.config["telegram_preferential_ids"]) > 0 and preferentials is True:
        log.insert_text("Sending password to preferential contacts...\n")
        for pref in conf_load.config["telegram_preferential_ids"]:
            with open("Autoraid.Windows\\Core\\image.jpg", "rb") as f:
                bot.send_photo(pref, f, caption=details)
        sleep(15)
    messageList = {}
    with open("Autoraid.Windows\\Core\\image.jpg", "rb") as f:
        log.insert_text("Sending password to telegram chats...\n")
        for id in conf_load.config["telegram_chat_ids"]:
            message = bot.send_photo(id, f, caption=details)
            messageList[str(id)] = message.message_id
    return messageList


# sends a message to notify that the host has stopped the bot
def send_telegram_finished(raid_pokemon, message, preferentials):
    caption = (
        "Finished Auto-Hosting for: "
        + raid_pokemon
        + "\nNumber of raids completed: "
        + message
    )
    send_telegram_text(caption, preferentials)


# loops through all chat ids to send the ending notification
def send_telegram_text(caption, preferentials):
    if len(conf_load.config["telegram_preferential_ids"]) > 0 and preferentials is True:
        for pref in conf_load.config["telegram_preferential_ids"]:
            bot.send_message(pref, caption)

    for id in conf_load.config["telegram_chat_ids"]:
        bot.send_message(id, caption)
