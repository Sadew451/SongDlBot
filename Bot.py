from distutils.command.clean import clean
import os
import yt_dlp
import asyncio
import wget
from yt_dlp import YoutubeDL
from youtubesearchpython import SearchVideos
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters

STICKER = "CAACAgUAAxkBAAECBpth5B5USPwi_7g5CMqnE20ypGqBqwAC4gIAAs6tMFSzLJrz52ymECME"

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

SDBotz = Client("Sample Bot", bot_token = BOT_TOKEN, api_id = API_ID, api_hash = API_HASH)

START_MSG = """
Hi {name}, i am a sample bot this bot is making on 

**Server** : [Heroku](Heroku.com)
**Library** : [Pyrogram](https://github.com/pyrogram/pyrogram) 

__Bot By @SDBotsz.__"""

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

@SDBotz.on_message(filters.text & filters.private & ~filters.command("start"))
async def get_songs(_, message):
    query = message.text
    m = await message.reply_text("Searching", quote=True)
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
    
    await m.edit("Downloading...")
    try:
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(lenk, download=True)
    except Exception as e:
        return await m.edit(f"**Download Failed** \n\n```{e}```")
      
    cap = f"**🎧 Title:** {title} \n**🎥 Channel:** {channel} \n**⏳ Duration:** {dur} \n\n**📮 By @SDBotsz**"
    aud = f"{ytdl_data['id']}.mp3"
    await m.edit("Uploading")
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
#async def AWBotz(client, message):
#    await message.copy(message.chat.id)
    
print("""SDBot is Started...""")    
SDBotz.run()
