import os, time
from display_progress import progress_for_pyrogram
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyromod import listen
import config
from handlers.broadcast import broadcast
from handlers.check_user import handle_user_status
from handlers.database import Database

LOG_CHANNEL = config.LOG_CHANNEL
AUTH_USERS = config.AUTH_USERS
DB_URL = config.DB_URL
DB_NAME = config.DB_NAME

db = Database(DB_URL, DB_NAME)


BOT_TOKEN = "5618782891:AAHaNxV7WgvgqrPN6FdgVo1aFBSfkhj-xDs"
API_ID = "10098309"
API_HASH = "aaacac243dddc9f0433c89cab8efe323"

Bot = Client(
    "Thumb-Bot",
    bot_token = BOT_TOKEN,
    api_id = API_ID,
    api_hash = API_HASH
)

START_TXT = """
Hey there, {} 👋 

I am video thumbnail changer Bot. I will helps you to change your video thumbnail on telegram.

Send a video/file to get started.
"""

START_BTN = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Contact Owner 👨🏻‍💻', url='t.me/PavanMagar'),
        ]]
    )


@Bot.on_message(filters.command(["start"]))
async def start(client: Client, message: Message):
      # return
    chat_id = message.from_user.id
    if not await db.is_user_exist(chat_id):
        data = await client.get_me()
        BOT_USERNAME = data.username
        await db.add_user(chat_id)
        if LOG_CHANNEL:
            await client.send_message(
                LOG_CHANNEL,
                f"#NEWUSER: \n\nNew User [{message.from_user.first_name}](tg://user?id={message.from_user.id}) started @{BOT_USERNAME} !!",
            )
    text = START_TXT.format(update.from_user.mention)
    reply_markup = START_BTN
    await update.reply_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=reply_markup
    )


# global variable to store path of the recent sended thumbnail
thumb = ""

@Bot.on_message(filters.private & (filters.video | filters.document))
async def thumb_change(bot, m):
    global thumb
    msg = await m.reply("Downloading video...")
    c_time = time.time()
    file_dl_path = await bot.download_media(message=m, progress=progress_for_pyrogram, progress_args=("Downloading file..", msg, c_time))
    await msg.delete()
    answer = await bot.ask(m.chat.id,'Now send the new thumbnail.', filters=filters.photo | filters.text)
    if answer.photo:
        try:
            os.remove(thumb)
        except:
            pass
        thumb = await bot.download_media(message=answer.photo)
    msg = await m.reply("Setting new thumbnail..")
    c_time = time.time()
    if m.document:
        await bot.send_document(chat_id=m.chat.id, document=file_dl_path, thumb=thumb, caption=m.caption if m.caption else None, progress=progress_for_pyrogram, progress_args=("Uploading file..", msg, c_time))
    elif m.video:
        await bot.send_video(chat_id=m.chat.id, video=file_dl_path, thumb=thumb, caption=m.caption if m.caption else None, progress=progress_for_pyrogram, progress_args=("Uploading file..", msg, c_time))
    await msg.delete()
    os.remove(file_dl_path)



Bot.run()
