from pyrogram import Client, Filters, StopPropagation, InlineKeyboardButton, InlineKeyboardMarkup


@Client.on_message(Filters.command(["start"]), group=-2)
async def start(client, message):
    # return
    joinButton = InlineKeyboardMarkup([
        [InlineKeyboardButton("Support Channel ð¢", url="https://t.me/FilmClubChannel")],
        [InlineKeyboardButton(
            "Bugs & Reports Bot ð¤", url="https://t.me/FilmClubGroup")]
    ])
    welcomed = f"Hello <b>{message.from_user.first_name},\n\nWelcome To ðC YOUð§ð¨ðð ðð¢ð§ ð¥³.\n\nI'm A Powered Youtube Download Bot Which Supports Video, Documents & Audio Of All Qualities ð</b>\n\n<b>Click</b> /help <b>For More Info On How To Use Me</b>"
    await message.reply_text(welcomed, reply_markup=joinButton)
    raise StopPropagation
