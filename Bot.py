import os
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Client, filters

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

SDBotz = Client("Sample Bot", bot_token = BOT_TOKEN, api_id = API_ID, api_hash = API_HASH)

START_MSG = """
HI I AM A TEST BOT"""

HELP_MSG = """
NO ONE GONE HELP YOU"""

ABOUT_MSG = """
Monai balamne"""

START_BUTTON = InlineKeyboardMarkup(
    [[
    InlineKeyboardButton('Channel', url = 'https://t.me/AWBotz'),
    InlineKeyboardButton('Support', url = 'https://t.me/AWBotz_Chat')
    ],[
    InlineKeyboardButton('Help', callback_data= 'help'),
    InlineKeyboardButton('About', callback_data= 'about'),
    InlineKeyboardButton('Close', callback_data= 'close'),
    ]]
    )

HELP_BUTTON = InlineKeyboardMarkup(
    [[
    InlineKeyboardButton ('Channel', url = 'https://t.me/AWBotz'),
    InlineKeyboardButton('Support', url = 'https://t.me/AWBotz_Chat')
    ],[
    InlineKeyboardButton('Home', callback_data= 'home'),
    InlineKeyboardButton('About', callback_data= 'about'),
    InlineKeyboardButton('Close', callback_data= 'close'),
    ]]
)

ABOUT_BUTTON = InlineKeyboardMarkup(
    [[
    InlineKeyboardButton ('Channel', url = 'https://t.me/AWBotz'),
    InlineKeyboardButton('Support', url = 'https://t.me/AWBotz_Chat')
    ],[
    InlineKeyboardButton('Home', callback_data= 'home'),
    InlineKeyboardButton('About', callback_data= 'about'),
    InlineKeyboardButton('Close', callback_data= 'close'),
    ]]
)

@SDBotz.on_message(filters.command('start') & filters.private)
async def start(client, message):    
    await message.reply_text(START_MSG)
    await message.reply_text(START_BUTTON,
                             reply_markup=START_BUTTON,
                             disable_web_page_preview=True)


@SDBotz.on_callback_query()
async def addorno(client, message):
    message = message.message.id
    await message.reply_text('start bot go to the option', quote=True,
    reply_markup=InlineKeyboardMarkup([InlineKeyboardButton(text="yes",
    callback_data=f"yes-{message}"),
    InlineKeyboardButton(text="No",
    callback_data=f"no-{message}")])
    )
    
@SDBotz.on_callback_query()
async def addorno(client, message):
         text=ABOUT_MSG
         reply_markup = ABOUT_BUTTON
         await message.reply_text(
             text=text,
             disable_web_page_preview=True,
             reply_markup=reply_markup
         )

@SDBotz.on_message(filters.private & filters.text | filters.media)
async def AWBotz(client, message):
    await message.copy(message.chat.id)
    
SDBotz.run()
