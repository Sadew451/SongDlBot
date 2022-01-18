from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
#re code useing pytube
import os, pytube, requests
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import filters
from youtube_search import YoutubeSearch
from pyrogram.errors import UserAlreadyParticipant
from pyrogram.errors import UserNotParticipant, ChatAdminRequired, UsernameNotOccupied
import os

from config import Config
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Client, filters


STICKER = "CAACAgIAAxkBAAECCfBh5W6RRkFp1uVwc37cKDtHXwJX6gAC7wAD5KDOB6-HpQABpszgdCME"


BOT_USERNAME = os.environ.get("BOT_USERNAME")
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

#if you like import direct


SDBotz = Client("Music Bot", bot_token = BOT_TOKEN, api_id = API_ID, api_hash = API_HASH)


START_MSG = """
👋 Hi i am a **Music Downloader bot Send Music Name & Search Fast**. Please Join Updates Channel Click the button.

**Server**  : [Heroku](Heroku.com)
**Library** : [Pyrogram](https://github.com/pyrogram/pyrogram) 
**Dev**     : [@Sadew451](https://github.com/Sadew451)

Bot By @SDBotsz."""

REPLY_MARKUP = InlineKeyboardMarkup(
    [[
    InlineKeyboardButton('📣 Channel', url = 'https://t.me/SDBots_Inifinity'),
    InlineKeyboardButton('👥 Support', url = 'https://t.me/SDBotz')
    ]]
)
JOIN_ASAP = f"❌** Access Denied ❌**\n\n🙋‍♂️ Hey There , You Must Join @SDBots_Inifinity Telegram Channel To Use This BOT. So, Please Join it & Try Again🤗. Thank You 🤝"

FSUBB = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton(text="👨🏻‍💻 Bot Updates", url=f"https://t.me/SDBots_Inifinity") 
        ]]
)
DB_CHANNEL = "-1001511610738"
@SDBotz.on_message(filters.command('start') & filters.private)
async def start(client, message):
    try:
        await message._client.get_chat_member(int("-1001475839216"), message.from_user.id)
    except UserNotParticipant:
        await message.reply_text(
        text=JOIN_ASAP, disable_web_page_preview=True, reply_markup=FSUBB
    )
        return 
    #chat id = message.from_group.id 
    chat_id = message.from_user.id
    await message.reply_sticker(STICKER)    
    await message.reply_text(START_MSG,
                             reply_markup=REPLY_MARKUP,
                             disable_web_page_preview=True)

#pytube song download 
CAPTION_TEXT = """
**{}**
Requester : {}
Downloaded Via : {}
"""

# code for szmedia bot
@SDBotz.on_message(filters.command("song"))
async def songdown(_, message):
   try: 
    if len(message.command) < 2:
            return await message.reply_text("Give a song name ")
    m = await message.reply_text("🔎 Searching ...")
    name = message.text.split(None, 1)[1]
    id = (YoutubeSearch(name, max_results=1).to_dict())[0]["id"]
    await song(m, message, id)
   except Exception as e:
       await m.edit(f"try again {e}")
#dowload
async def song(m, message, id):
   try: 
    m = await m.edit(text = "📥 Downloading...",
    reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("📥 Downloading...", callback_data="progress")]]))
    link =  pytube.YouTube(f"https://youtu.be/{id}")
    thumbloc = link.title + "thumb"
    thumb = requests.get(link.thumbnail_url, allow_redirects=True)
    open(thumbloc , 'wb').write(thumb.content)
    songlink = link.streams.filter(only_audio=True).first()
    down = songlink.download()
    first, last = os.path.splitext(down)
    song = first + '.mp3'
    os.rename(down, song)
    m = await m.edit(text = "📤 Uploading...",
    reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("📤 Uploading...", callback_data="progress")]]))
    await message.reply_audio(song,
    caption = CAPTION_TEXT.format(link.title, message.from_user.mention if message.from_user else "Anonymous Admin", "Youtube"),
    thumb = thumbloc,
    reply_markup = REPLY_MARKUP)
    await m.delete()
    if os.path.exists(song):
        os.remove(song)
    if os.path.exists(thumbloc):
        os.remove(thumbloc)
   except Exception as e:
       await m.edit(f"Try again!\n\n{str(e)}")
    
print("""

Bot : Powerfull telegram song Bot 

""")    
SDBotz.run()
