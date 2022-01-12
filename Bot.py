import os
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Client, filters

SDBotz = Client("SampleBot", bot_token = BOT_TOKEN, api_id = API_ID, api_hash = API_HASH)

START_MSG = """
HI I AM A TEST BOT"""

HELP_MSG = """
NO ONE GONE HELP YOU"""

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

@SDBotz.on_callback_query()
async def cb data (bot,update);
         text=START_MSG
         reply_markup = START_BUTTON
         await update.reply_text(
             text=text,
             disable_web_page_preview=True,
             reply_markup=reply_markup
         )

@SDBotz.on_callback_query()
async def cb data (bot,update);
         text=HELP_MSG
         reply_markup = HELP_BUTTON
         await update.reply_text(
             text=text,
             disable_web_page_preview=True,
             reply_markup=reply_markup
         )
    
@SDBotz.on_callback_query()
async def cb data (bot,update);
         text=ABOUT_MSG
         reply_markup = ABOUT_BUTTON
         await update.reply_text(
             text=text,
             disable_web_page_preview=True,
             reply_markup=reply_markup
         )

@SDBotz.on_message(filters.private & filters.text | filters.media)
async def AWBotz(client, message):
    await message.copy(message.chat.id)
    
SDBotz.run()
