from pyrogram import Client, Filters, StopPropagation, InlineKeyboardButton, InlineKeyboardMarkup


@Client.on_message(Filters.command(["start"]), group=-2)
async def start(client, message):
    # return
    joinButton = InlineKeyboardMarkup([
        [InlineKeyboardButton("Support Channel 📢", url="https://t.me/FilmClubChannel")],
        [InlineKeyboardButton(
            "Bugs & Reports Bot 🤖", url="https://t.me/FilmClubGroup")]
    ])
    welcomed = f"Hello <b>{message.from_user.first_name},\n\nWelcome To 𝗙C YOU𝗧𝗨𝗕𝗘 𝗕𝗢𝗧 🥳.\n\nI'm A Powered Youtube Download Bot Which Supports Video, Documents & Audio Of All Qualities 😇</b>\n\n<b>Click</b> /help <b>For More Info On How To Use Me</b>"
    await message.reply_text(welcomed, reply_markup=joinButton)
    raise StopPropagation
