import telebot
from config_loader import CONFIG
from time import sleep

# TELEGRAM SETUP
bot = telebot.TeleBot(CONFIG['telegram_bot_token'])
PASSWORD_CAPTION = "Tera Raid hosting\nPokémon: "
SNITCH_MODE_CAPTION = "Utenti connessi"

# sends a telegram message with a screenshot of the password screen
def send_password(raid_pokemon, extra_info):
    caption = PASSWORD_CAPTION + raid_pokemon
    # We add an extra line if we have extra info to display
    if len(extra_info) > 0:
        caption += "\nExtra Info: " + extra_info
    message_list = send_telegram_image(caption)
    return message_list

# sends a telegram message with a screenshot of the raid party screen
def send_snitch(messageList):
    with open('image.jpg', 'rb') as f:
        media = telebot.types.InputMediaPhoto(f, caption=SNITCH_MODE_CAPTION)
        print("Sending snitches to telegram chats...")
        for chat_id, message_id in messageList.items():
            bot.edit_message_media(chat_id=int(chat_id), message_id=message_id, media=media)

# loops through all the telegram ids to send the message
def send_telegram_image(details):   
    # preferential chats get the password 15 seconds before all others
    if len(CONFIG['telegram_preferential_ids']) > 0:
        print("Sending password to preferential contacts...")
        for pref in CONFIG['telegram_preferential_ids']:
            with open('image.jpg', 'rb') as f:
                bot.send_photo(pref, f, caption=details)
        sleep(15) 
    messageList = {}
    with open('image.jpg', 'rb') as f:
        print("Sending password to telegram chats...")
        for id in CONFIG['telegram_chat_ids']:
            message = bot.send_photo(id, f, caption=details)
            messageList[str(id)] = message.message_id
    return messageList

# sends a message to notify that the host has stopped the bot
def send_telegram_finished(raid_pokemon, message):
    caption = "Finished Auto-Hosting for: " + raid_pokemon + "\nNumber of raids completed: " + message
    send_telegram_text(caption)

# loops through all chat ids to send the ending notification
def send_telegram_text(caption):
    for pref in CONFIG['telegram_preferential_ids']:
        bot.send_message(pref, caption)
        
    for id in CONFIG['telegram_chat_ids']:
        bot.send_message(id, caption)


