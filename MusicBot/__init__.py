""" Wrtten By Sadew Jayasekara
Project By @SDBots_Inifinity """

import os 
from pyrogram import Client

API_ID =int(os.environ.get('API_ID'))
API_HASH = (os.environ.get("API_HASH"))
BOT_TOKEN = (os.environ.get("BOT_TOKEN"))

LOGGER = logging.getLogger(__name__)

SDBotz = Client("Music Bot", bot_token = BOT_TOKEN, api_id = API_ID, api_hash = API_HASH)

SDBotz.run()
