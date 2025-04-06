import re
import sqlite3
from datetime import datetime
from config import admin_id, main_channel, watched_channels

class AirdropWatcher:
    def __init__(self, app):
        self.app = app
        self.conn = sqlite3.connect("airdrops.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS airdrops (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)"
        )
        self.conn.commit()

    async def run(self):
        async with self.app:
            for channel in watched_channels:
                await self.app.join_chat(channel)
            self.app.add_handler("message", self.check_airdrop)
            print("🔍 Airdrop Watcher запущено...")
            await self.app.idle()

    async def check_airdrop(self, client, message):
        if not message.text:
            return

        text = message.text.lower()
        if "airdrop" in text or "фаєрдроп" in text or "дроп" in text:
            is_paid = any(word in text for word in ["buy", "sale", "$", "usd", "eth", "bnb", "платн", "купити"])
            duplicate = self.cursor.execute("SELECT * FROM airdrops WHERE text = ?", (message.text,)).fetchone()
            if not duplicate:
                self.cursor.execute("INSERT INTO airdrops (text) VALUES (?)", (message.text,))
                self.conn.commit()

            msg = f"🔔 <b>Знайдено дроп</b>

{message.text}"
            if is_paid:
                msg = f"🟨 {msg}"

            if duplicate:
                msg += "

♻️ Цей дроп вже зʼявлявся в іншому каналі."

            try:
                if main_channel:
                    await client.send_message(main_channel, msg)
                else:
                    await client.send_message(admin_id, msg)
            except Exception as e:
                print(f"❌ Не вдалося надіслати повідомлення: {e}")
