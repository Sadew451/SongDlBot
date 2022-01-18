from distutils.command.clean import clean

import time
import string
import random
import datetime
import aiofiles
import asyncio
import traceback
import aiofiles.os
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
#re code useing pytube
import os, pytube, requests
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import filters
from youtube_search import YoutubeSearch
from pyrogram.errors import UserAlreadyParticipant
from pyrogram.errors import UserNotParticipant, ChatAdminRequired, UsernameNotOccupied
import os
import asyncio
from config import Config
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters
from database import Database

STICKER = "CAACAgIAAxkBAAECCfBh5W6RRkFp1uVwc37cKDtHXwJX6gAC7wAD5KDOB6-HpQABpszgdCME"



#add user id to db
async def AddUserToDatabase(bot: Client, cmd: Message):
    if not await db.is_user_exist(cmd.from_user.id):
        await db.add_user(cmd.from_user.id)
        if LOG_CHANNEL is not None:
            await bot.send_message(
                int(LOG_CHANNEL),
                f"#NEW_USER: \n\nNew User [{cmd.from_user.first_name}](tg://user?id={cmd.from_user.id}) started @{Config.BOT_USERNAME} !!"
            )

#broadcast handller
broadcast_ids = {}

async def send_msg(user_id, message):
    try:
        if Config.BROADCAST_AS_COPY is False:
            await message.forward(chat_id=user_id)
        elif Config.BROADCAST_AS_COPY is True:
            await message.copy(chat_id=user_id)
        return 200, None
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return send_msg(user_id, message)
    except InputUserDeactivated:
        return 400, f"{user_id} : deactivated\n"
    except UserIsBlocked:
        return 400, f"{user_id} : blocked the bot\n"
    except PeerIdInvalid:
        return 400, f"{user_id} : user id invalid\n"
    except Exception as e:
        return 500, f"{user_id} : {traceback.format_exc()}\n"


async def main_broadcast_handler(m, db):
    all_users = await db.get_all_users()
    broadcast_msg = m.reply_to_message
    while True:
        broadcast_id = ''.join([random.choice(string.ascii_letters) for i in range(3)])
        if not broadcast_ids.get(broadcast_id):
            break
    out = await m.reply_text(
        text=f"Broadcast Started! You will be notified with log file when all the users are notified."
    )
    start_time = time.time()
    total_users = await db.total_users_count()
    done = 0
    failed = 0
    success = 0
    broadcast_ids[broadcast_id] = dict(
        total=total_users,
        current=done,
        failed=failed,
        success=success
    )
    async with aiofiles.open('broadcast.txt', 'w') as broadcast_log_file:
        async for user in all_users:
            sts, msg = await send_msg(
                user_id=int(user['id']),
                message=broadcast_msg
            )
            if msg is not None:
                await broadcast_log_file.write(msg)
            if sts == 200:
                success += 1
            else:
                failed += 1
            if sts == 400:
                await db.delete_user(user['id'])
            done += 1
            if broadcast_ids.get(broadcast_id) is None:
                break
            else:
                broadcast_ids[broadcast_id].update(
                    dict(
                        current=done,
                        failed=failed,
                        success=success
                    )
                )
    if broadcast_ids.get(broadcast_id):
        broadcast_ids.pop(broadcast_id)
    completed_in = datetime.timedelta(seconds=int(time.time() - start_time))
    await asyncio.sleep(3)
    await out.delete()
    if failed == 0:
        await m.reply_text(
            text=f"broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed.",
            quote=True
        )
    else:
        await m.reply_document(
            document='broadcast.txt',
            caption=f"broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed.",
            quote=True
        )
    await aiofiles.os.remove('broadcast.txt')

#ban check
async def handle_user_status(bot, cmd):
    chat_id = cmd.from_user.id
    if not await db.is_user_exist(chat_id):
        await db.add_user(chat_id)
        await bot.send_message(
            Config.LOG_CHANNEL,
            f"#NEW_USER: \n\nNew User [{cmd.from_user.first_name}](tg://user?id={cmd.from_user.id}) started @{Config.BOT_USERNAME} !!"
        )

    ban_status = await db.get_ban_status(chat_id)
    if ban_status["is_banned"]:
        if (
                datetime.date.today() - datetime.date.fromisoformat(ban_status["banned_on"])
        ).days > ban_status["ban_duration"]:
            await db.remove_ban(chat_id)
        else:
            await cmd.reply_text("You are Banned to Use This Bot 🥺", quote=True)
            return
    await cmd.continue_propagation()


BOT_USERNAME = os.environ.get("BOT_USERNAME")
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

#if you like import direct
db = Database(Config.DATABASE_URL,BOT_USERNAME)

SDBotz = Client("Music Bot", bot_token = BOT_TOKEN, api_id = API_ID, api_hash = API_HASH)
LOG_CHANNEL = "-1001511610738"

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
JOIN_ASAP = f"⛔️** Access Denied **⛔️\n\n🙋‍♂️ Hey There , You Must Join @szteambots Telegram Channel To Use This BOT. So, Please Join it & Try Again🤗. Thank You 🤝"

FSUBB = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton(text="Sz Team Bots <sz/>", url=f"https://t.me/szteambots") 
        ]]
    )

@SDBotz.on_message(filters.command('start') & filters.private)
async def start(client, message):
    try:
        await message._client.get_chat_member(int("-1001325914694"), message.from_user.id)
    except UserNotParticipant:
        await message.reply_text(
        text=JOIN_ASAP, disable_web_page_preview=True, reply_markup=FSUBB
    )
        return 
    #chat id = message.from_group.id 
    chat_id = message.from_user.id
    if not await db.is_user_exist(chat_id):
            await db.add_user(chat_id)
            await SDBotz.send_message(
                LOG_CHANNEL,
                f"✅ Bot Started Successfully!\n👽New User: [{message.from_user.first_name}](tg://user?id={message.from_user.id}) \nUser Id: {message.from_user.id}\nBot username 🤖 @SDSongDlBot "
            ) 
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

CAPTION_BTN = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Updates ", url="https://t.me/SDBOTs_inifinity")]])

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
    reply_markup = CAPTION_BTN)
    await m.delete()
    if os.path.exists(song):
        os.remove(song)
    if os.path.exists(thumbloc):
        os.remove(thumbloc)
   except Exception as e:
       await m.edit(f"Try again!\n\n{str(e)}")


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



#broadcast added
@SDBotz.on_message(filters.private & filters.command("broadcast") & filters.user(Config.BOT_OWNER) & filters.reply)
async def broadcast_handler_open(_, m: Message):
    await main_broadcast_handler(m, db)

#user stats
@SDBotz.on_message(filters.private & filters.command("stats") & filters.user(Config.BOT_OWNER))
async def sts(_, m: Message):
    total_users = await db.total_users_count()
    await m.reply_text(text=f"**Total Users in DB:** `{total_users}`", parse_mode="Markdown", quote=True)

#ban user
@SDBotz.on_message(filters.private & filters.command("ban") & filters.user(Config.BOT_OWNER))
async def ban(c: Client, m: Message):
    
    if len(m.command) == 1:
        await m.reply_text(
            f"Use this command to ban any user from the bot.\n\nUsage:\n\n`/ban user_id ban_duration ban_reason`\n\nEg: `/ban 1234567 28 You misused me.`\n This will ban user with id `1234567` for `28` days for the reason `You misused me`.",
            quote=True
        )
        return

    try:
        user_id = int(m.command[1])
        ban_duration = int(m.command[2])
        ban_reason = ' '.join(m.command[3:])
        ban_log_text = f"Banning user {user_id} for {ban_duration} days for the reason {ban_reason}."
        try:
            await c.send_message(
                user_id,
                f"You are banned to use this bot for **{ban_duration}** day(s) for the reason __{ban_reason}__ \n\n**Message from the admin**"
            )
            ban_log_text += '\n\nUser notified successfully!'
        except:
            traceback.print_exc()
            ban_log_text += f"\n\nUser notification failed! \n\n`{traceback.format_exc()}`"

        await db.ban_user(user_id, ban_duration, ban_reason)
        print(ban_log_text)
        await m.reply_text(
            ban_log_text,
            quote=True
        )
    except:
        traceback.print_exc()
        await m.reply_text(
            f"Error occoured! Traceback given below\n\n`{traceback.format_exc()}`",
            quote=True
        )

#unban
@SDBotz.on_message(filters.private & filters.command("unban") & filters.user(Config.BOT_OWNER))
async def unban(c: Client, m: Message):
    if len(m.command) == 1:
        await m.reply_text(
            f"Use this command to unban any user.\n\nUsage:\n\n`/unban user_id`\n\nEg: `/unban 1234567`\n This will unban user with id `1234567`.",
            quote=True
        )
        return
    try:
        user_id = int(m.command[1])
        unban_log_text = f"Unbanning user {user_id}"
        try:
            await c.send_message(
                user_id,
                f"Your ban was lifted!"
            )
            unban_log_text += '\n\nUser notified successfully!'
        except:
            traceback.print_exc()
            unban_log_text += f"\n\nUser notification failed! \n\n`{traceback.format_exc()}`"
        await db.remove_ban(user_id)
        print(unban_log_text)
        await m.reply_text(
            unban_log_text,
            quote=True
        )
    except:
        traceback.print_exc()
        await m.reply_text(
            f"Error occoured! Traceback given below\n\n`{traceback.format_exc()}`",
            quote=True
        )

#baned users
@SDBotz.on_message(filters.private & filters.command("banned") & filters.user(Config.BOT_OWNER))
async def _banned_usrs(_, m: Message):
    
    all_banned_users = await db.get_all_banned_users()
    banned_usr_count = 0
    text = ''

    async for banned_user in all_banned_users:
        user_id = banned_user['id']
        ban_duration = banned_user['ban_status']['ban_duration']
        banned_on = banned_user['ban_status']['banned_on']
        ban_reason = banned_user['ban_status']['ban_reason']
        banned_usr_count += 1
        text += f"> **user_id**: `{user_id}`, **Ban Duration**: `{ban_duration}`, **Banned on**: `{banned_on}`, **Reason**: `{ban_reason}`\n\n"
    reply_text = f"Total banned user(s): `{banned_usr_count}`\n\n{text}"
    if len(reply_text) > 4096:
        with open('banned-users.txt', 'w') as f:
            f.write(reply_text)
        await m.reply_document('banned-users.txt', True)
        os.remove('banned-users.txt')
        return
    await m.reply_text(reply_text, True)





#@SDBotz.on_message(filters.private & filters.text | filters.media)
#async def SDBotz(client, message):
#    await message.copy(message.chat.id)
    
print("""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Bot : Powerfull telegram song Bot             ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
└───────────────────────────────────────────────┘
""")    
SDBotz.run()

