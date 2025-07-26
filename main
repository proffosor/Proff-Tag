from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, ChatJoinRequest

api_id = 10079905
api_hash = "e4a5fa251e2e055f26e5c2add8401530"
bot_token = "7549973847:AAEAhvUW8X0IEamKdFw0NtXwvFkJ57IJ7zA"

app = Client(
    "Auto Approved Bot",
    bot_token=bot_token,
    api_id=api_id,
    api_hash=api_hash
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
@app.on_chat_join_request(filters.group | filters.channel)
async def autoapprove(client: app, message: ChatJoinRequest):
    chat = message.chat
    user = message.from_user
    print(f"{user.first_name} Approved ðŸ‘")
    await client.approve_chat_join_request(chat_id=chat.id, user_id=user.id)
    user_chat = await app.get_users(user.id)
    if user_chat.is_bot:
        return
    await app.send_message(user.id, f"**✦ » ʜᴇʟʟᴏ {user.mention} ʏᴏᴜ ᴀʀᴇ ɴᴏᴡ ᴀᴜᴛᴏ ᴀᴘᴘʀᴏᴠᴇᴅ ᴀ ᴄʜᴀᴛ : {chat.title}**\n\n**ᴠɪsɪᴛ » @PURVI_SUPPORT**")

if __name__ == "__main__":
    print("Auto Approved Bot started...")
    app.run()
