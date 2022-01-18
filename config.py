import os
class Config(object):
	BOT_USERNAME = os.environ.get("BOT_USERNAME")
	DATABASE_URL = os.environ.get("DATABASE_URL")
DB_CHANNEL = int(os.environ.get("DB_CHANNEL"))
