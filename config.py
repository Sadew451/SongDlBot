import os
class Config(object):
	BOT_USERNAME = os.environ.get("BOT_USERNAME")
	DATABASE_URL = os.environ.get("DATABASE_URL")
	BOT_OWNER = os.environ.get("BOT_OWNER")
