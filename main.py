from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, ChatJoinRequest
from pyrogram.errors import ChatAdminRequired, FloodWait, PeerIdInvalid
from pyrogram.sessions import StringSession
from pymongo import MongoClient
import asyncio
from os import getenv

# ====== Bot Config =====
API_ID = int(getenv("API_ID", "24168862"))
API_HASH = getenv("API_HASH", "916a9424dd1e58ab7955001ccc0172b3")

BOT_TOKEN = getenv("BOT_TOKEN", "7635729732:AAG6QShFz20CmQgzcoRSDURw-RV9kDCWdEQ")
MONGO_DB_URI = getenv("MONGO_DB_URI", "mongodb+srv://CHATBOT:Purvichat@cluster0.i3u97sj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# ====== Init Clients ======
app = Client("Auto Approved Bot", bot_token=bot_token, api_id=api_id, api_hash=api_hash)
mongo = MongoClient(mongo_url)
db = mongo.autoapprove
session_col = db.sessions

# ====== Commands ======
@app.on_message(filters.private & filters.command("start"))
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
        caption=f"**✦ » ʜᴇʏ {message.from_user.mention}!**\n**✦ » ɪ ᴀᴍ ᴀᴜᴛᴏ ᴀᴘᴘʀᴏᴠᴇ ʙᴏᴛ.**\n\n**Use `/newsession <session_string>` to set your session.**",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@app.on_message(filters.private & filters.command("newsession"))
async def newsession(client, message: Message):
    if len(message.command) < 2:
        return await message.reply("⚠️ Send your Pyrogram session like: `/newsession <your_string_session>`")
    string = message.text.split(" ", 1)[1]
    try:
        user_client = Client(StringSession(string), api_id=api_id, api_hash=api_hash)
        await user_client.start()
        user = await user_client.get_me()
        session_col.replace_one({"_id": "session"}, {"_id": "session", "string": string, "user_id": user.id}, upsert=True)
        await user_client.stop()
        await message.reply(f"✅ Session set successfully for user: `{user.first_name}`")
    except Exception as e:
        await message.reply(f"❌ Invalid session: {e}")

@app.on_message(filters.private & filters.command("removesession"))
async def removesession(_, message):
    result = session_col.delete_one({"_id": "session"})
    if result.deleted_count:
        await message.reply("🗑️ Session removed successfully.")
    else:
        await message.reply("⚠️ No session found.")

@app.on_message(filters.private & filters.command("allapprove"))
async def allapprove(_, message):
    if len(message.command) < 2:
        return await message.reply("❗ Usage: `/allapprove <chat_id>`")
    session_data = session_col.find_one({"_id": "session"})
    if not session_data:
        return await message.reply("❌ No session found. Use `/newsession <session_string>` to add one.")
    chat_id = message.command[1]
    try:
        user_client = Client(StringSession(session_data['string']), api_id=api_id, api_hash=api_hash)
        await user_client.start()
        approved = 0
        async for req in user_client.get_chat_join_requests(int(chat_id)):
            try:
                await user_client.approve_chat_join_request(int(chat_id), req.from_user.id)
                approved += 1
            except FloodWait as e:
                await asyncio.sleep(e.value)
            except Exception as err:
                print(f"Failed to approve {req.from_user.id}: {err}")
        await user_client.stop()
        await message.reply(f"✅ Approved {approved} join requests in `{chat_id}`")
    except ChatAdminRequired:
        await message.reply("❌ Error: The user session is not admin in the chat.")
    except PeerIdInvalid:
        await message.reply("❌ Error: Invalid Chat ID.")
    except Exception as e:
        await message.reply(f"❌ Error occurred: {e}")

@app.on_chat_join_request(filters.group | filters.channel)
async def autoapprove(client: app, message: ChatJoinRequest):
    chat = message.chat
    user = message.from_user
    print(f"{user.first_name} requested to join {chat.title} ✅")
    await client.approve_chat_join_request(chat_id=chat.id, user_id=user.id)
    if not user.is_bot:
        await client.send_message(user.id, f"**✦ » ʜᴇʟʟᴏ {user.mention}, ʏᴏᴜʀ ʀᴇQᴜᴇsᴛ ɪɴ `{chat.title}` ɪs ᴀᴜᴛᴏ-ᴀᴘᴘʀᴏᴠᴇᴅ.**")

if __name__ == "__main__":
    print("Auto Approved Bot started...")
    app.run()
