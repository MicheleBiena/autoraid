from Core import config_loader as conf_load
from discord_webhook import DiscordEmbed, DiscordWebhook
from pathlib import Path

# DISCORD WEBHOOK SETUP
webhook = DiscordWebhook(conf_load.config.get("discord_webhook_url", ""))
EMBED_TITLE_RUNNING = "DollyAutoRaid"
EMBED_TITLE_STOP = "Stopped"
EMBED_DESC_RUNNING = "Tera Raid hosting"
EMBED_DESC_STOPPED = "Finished auto hosting for: "
EMBED_COLOR = conf_load.config.get("discord_embed_color", 0)

embed = DiscordEmbed(
    title=EMBED_TITLE_RUNNING, description=EMBED_DESC_RUNNING, color=EMBED_COLOR
)


def send_password(raid_pokemon, extra_info, log):
    log.insert_text("Sending password to discord webhook...\n")
    # preparing the screenshot file
    with open(Path("Autoraid.Windows/Core/image.jpg"), "rb") as f:
        webhook.add_file(file=f.read(), filename="image.jpg")
    # compiling embed fields
    embed.set_title(raid_pokemon)
    embed.set_image(url="attachment://image.jpg")
    # only adding one extra field if there are extra info
    if len(extra_info) > 0:
        if len(embed.fields) == 0:
            embed.add_embed_field(name="Extra info", value=extra_info)
    # adding the embed to the webhook, executing and clearing it after
    webhook.add_embed(embed)
    webhook.execute()
    webhook.remove_embeds()


def send_discord_finished(raid_pokemon, message):
    # create a different embed (easier than clearing the old one)
    embed = DiscordEmbed(
        title=EMBED_TITLE_STOP,
        description=(EMBED_DESC_STOPPED + raid_pokemon),
        color=EMBED_COLOR,
    )
    embed.add_embed_field(name="Number of raids completed: ", value=message)
    webhook.add_embed(embed)
    webhook.execute()
    webhook.remove_embeds()
