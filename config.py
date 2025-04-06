import os

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN")
admin_id = int(os.getenv("ADMIN_ID"))
main_channel = os.getenv("MAIN_CHANNEL")
watched_channels = os.getenv("WATCHED_CHANNELS").split(",")
