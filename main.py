import asyncio
from pyrogram import Client
from config import api_id, api_hash, bot_token
from watcher import AirdropWatcher

app = Client("airdrop_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app.on_message()
async def main_handler(client, message):
    pass  # можна додати обробку команд

async def main():
    watcher = AirdropWatcher(app)
    await watcher.run()

if __name__ == "__main__":
    asyncio.run(main())
