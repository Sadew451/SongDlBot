from distutils.command.clean import clean

import os
import yt_dlp
import asyncio
import wget

from yt_dlp import YoutubeDL
from youtubesearchpython import SearchVideos
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters

STICKER = "CAACAgIAAxkBAAECCfBh5W6RRkFp1uVwc37cKDtHXwJX6gAC7wAD5KDOB6-HpQABpszgdCME"

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

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


@SDBotz.on_message(filters.command('start') & filters.private)
async def start(client, message):
    await message.reply_sticker(STICKER)    
    await message.reply_text(START_MSG,
                             reply_markup=REPLY_MARKUP,
                             disable_web_page_preview=True)

@SDBotz.on_message(filters.text & filters.private & ~filters.command("start"))
async def get_songs(_, message):
    query = message.text
    m = await message.reply_text("**Searching...**", quote=True)
    search = SearchVideos(f"{query}", offset=1, mode="dict", max_results=1)
    mi = search.result()
    mio = mi["search_result"]
    lenk = mio[0]["link"]
    title = mio[0]["title"]
    ytid = mio[0]["id"]
    channel = mio[0]["channel"]
    #views = mio[0]["views"]
    dur = mio[0]["duration"]
    tblink = f"https://img.youtube.com/vi/{ytid}/hqdefault.jpg"
    await asyncio.sleep(0.6)
    tb = wget.download(tblink)
    
    opts = {
        "format": "bestaudio",
        "addmetadata": True,
        "key": "FFmpegMetadata",
        "writethumbnail": True,
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "720",
            }
        ],
        "outtmpl": "%(id)s.mp3",
        "quiet": True,
        "logtostderr": False,
    }
    
    await m.edit("**Downloading...**")
    try:
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(lenk, download=True)
    except Exception as e:
        return await m.edit(f"**Download Failed** \n\n```{e}```")
      
    cap = f"**🎧 Title:** `{title}` \n**🎥 Channel:** `{channel}` \n**⏳ Duration:** `{dur}` \n\n**Upload By @SDBotsz**"
    aud = f"{ytdl_data['id']}.mp3"
    await m.edit("**Uploading...**")
    await message.reply_audio(audio=open(aud, "rb"), 
                              duration=int(ytdl_data["duration"]), 
                              title=str(ytdl_data["title"]), 
                              performer=str(ytdl_data["uploader"]),
                              thumb=tb,
                              caption=cap,
                              quote=True)

    await m.delete()
    for files in (tb, aud):
        if files and os.path.exists(files):
            os.remove(files)

#@SDBotz.on_message(filters.private & filters.text | filters.media)
#async def SDBotz(client, message):
#    await message.copy(message.chat.id)
    
print("""SDBot is Started...""")    
SDBotz.run()
