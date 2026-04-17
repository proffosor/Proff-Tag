from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, ChatJoinRequest
import os

API_ID = int(os.getenv("API_ID", "10079905"))
API_HASH = os.getenv("API_HASH", "e4a5fa251e2e055f26e5c2add8401530")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client(
    "Auto Approved Bot",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH
)

@app.on_message(filters.private & filters.command(["start"]))
async def start(client: app, message: Message):
    approved_bot = await client.get_me()
    buttons = [
        [InlineKeyboardButton("⚜️ ᴀᴅᴅ ᴍᴇ ʙᴀʙʏ ⚜️", url=f"http://t.me/{approved_bot.username}?startgroup=botstart")],
        [InlineKeyboardButton("🔸 sᴜᴘᴘᴏʀᴛ 🔸", url="https://t.me/PURVI_SUPPORT"),
         InlineKeyboardButton("▫️ ᴜᴘᴅᴀᴛᴇs ▫️", url="https://t.me/PURVI_UPDATES")]
    ]
    photo_url = "https://files.catbox.moe/yy0ukm.jpg"
    await client.send_photo(
        chat_id=message.chat.id,
        photo=photo_url,
        caption=f"**✦ » ʜᴇʏ {message.from_user.mention}!**\n**✦ » ɪ ᴀᴍ ᴀᴜᴛᴏ ᴀᴘᴘʀᴏᴠᴇ ʀᴇǫᴜᴇsᴛ ʙᴏᴛ ғᴏʀ ᴄʜᴀɴɴᴇʟ ᴏʀ ɢʀᴏᴜᴘ.**\n\n**✦ » ᴀᴅᴅ ᴍᴇ ʏᴏᴜʀ ɢʀᴏᴜᴘ / ᴄʜᴀɴɴᴇʟ ᴄʜᴇᴀᴋ ᴍʏ ғᴇᴀᴛᴜʀᴇs.**\n\n**✦ »𝐏ᴏᴡᴇʀᴇᴅ 𝖡ʏ » [⎯᪵፝֟፝֟⎯꯭𓆩꯭ 𝐀 ꯭ʟ ꯭ᴘ ꯭ʜ꯭ ᴧ꯭⎯꯭꯭‌꯭🥂꯭༎꯭ 𓆪](t.me/ll_ALPHA_BABY_lll)**",
        reply_markup=InlineKeyboardMarkup(buttons)
    )




if __name__ == "__main__":
    print("Auto Approved Bot started...")
    app.run()
