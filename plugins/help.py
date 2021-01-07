from pyrogram import Client, Filters, StopPropagation, InlineKeyboardButton, InlineKeyboardMarkup


@Client.on_message(Filters.command(["help"]))
async def start(client, message):
    # return
    joinButton = InlineKeyboardMarkup([
        [InlineKeyboardButton("Support Channel 📢", url="https://t.me/FlixBots")],
        [InlineKeyboardButton(
            "Bugs & Reports Bot 🤖", url="https://t.me/FlixHelpBot")]
    ])
    helptxt = f"Currently Only Supports Youtube Single  (No Playlist) Just Send Any Valid Youtube Url"
    await message.reply_text(helptxt, reply_markup=joinButton)
    raise StopPropagation
