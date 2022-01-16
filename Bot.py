import os
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters

STICKER = "CAACAgUAAxkBAAECBClh4tnTjQQFEhITJUGrfZIvNGdodwACuAQAAlltyVQh83W7N5dW5yME"

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

SDBotz = Client("Sample Bot", bot_token = BOT_TOKEN, api_id = API_ID, api_hash = API_HASH)

START_MSG = """
Hi i am a sample bot this bot is making on 

**Server** : [Heroku](Heroku.com)
**Library** : [Pyrogram](https://github.com/pyrogram/pyrogram) 

Bot By @SDBotsz."""

REPLY_MARKUP = InlineKeyboardMarkup(
    [[
    InlineKeyboardButton('Channel', url = 'https://t.me/AWBotz'),
    InlineKeyboardButton('Support', url = 'https://t.me/AWBotz_Chat')
    ]]
)


@SDBotz.on_message(filters.command('start') & filters.private)
async def start(client, message):
    await message.reply_sticker(STICKER)    
    await message.reply_text(START_MSG,
                             reply_markup=REPLY_MARKUP,
                             disable_web_page_preview=True)

#@SDBotz.on_message(filters.private & filters.text | filters.media)
#async def AWBotz(client, message):
#    await message.copy(message.chat.id)
    
SDBotz.run()
