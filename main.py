from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, ChatJoinRequest
from pyrogram.errors import ChatAdminRequired, FloodWait, PeerIdInvalid
from pymongo import MongoClient
import asyncio
from os import getenv

# ====== Bot Config =====
API_ID = int(getenv("API_ID", "24168862"))
API_HASH = getenv("API_HASH", "916a9424dd1e58ab7955001ccc0172b3")
BOT_TOKEN = getenv("BOT_TOKEN", "7635729732:AAG6QShFz20CmQgzcoRSDURw-RV9kDCWdEQ")
MONGO_DB_URI = getenv("MONGO_DB_URI", "mongodb+srv://CHATBOT:Purvichat@cluster0.i3u97sj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# ====== Init Clients ======
app = Client(
    "AutoApprovedBot",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH,
    parse_mode=enums.ParseMode.HTML  # Default parse mode
)
mongo = MongoClient(MONGO_DB_URI)
db = mongo.autoapprove
session_col = db.sessions

# ====== Utility Functions ======
async def safe_reply(message, text, **kwargs):
    try:
        await message.reply(text, parse_mode=enums.ParseMode.HTML, **kwargs)
    except Exception as e:
        print(f"Error sending message: {e}")
        await message.reply(text, parse_mode=None, **kwargs)

# ====== Commands ======
@app.on_message(filters.private & filters.command("start"))
async def start(client: Client, message: Message):
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
        caption=f"<b>✦ » ʜᴇʏ {message.from_user.mention}!</b>\n<b>✦ » ɪ ᴀᴍ ᴀᴜᴛᴏ ᴀᴘᴘʀᴏᴠᴇ ʙᴏᴛ.</b>\n\nUse <code>/newsession &lt;session_string&gt;</code> to set your session.",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@app.on_message(filters.private & filters.command("newsession"))
async def newsession(client: Client, message: Message):
    if len(message.command) < 2:
        await safe_reply(message, "⚠️ Send your Pyrogram session like: <code>/newsession &lt;your_string_session&gt;</code>")
        return
    
    string = message.text.split(" ", 1)[1]
    try:
        async with Client(":memory:", session_string=string, api_id=API_ID, api_hash=API_HASH) as user_client:
            user = await user_client.get_me()
            session_col.replace_one(
                {"_id": "session"}, 
                {"_id": "session", "string": string, "user_id": user.id}, 
                upsert=True
            )
            await safe_reply(message, f"✅ Session set successfully for user: <code>{user.first_name}</code>")
    except Exception as e:
        await safe_reply(message, f"❌ Invalid session: {str(e)}")

@app.on_message(filters.private & filters.command("removesession"))
async def removesession(client: Client, message: Message):
    result = session_col.delete_one({"_id": "session"})
    if result.deleted_count:
        await safe_reply(message, "🗑️ Session removed successfully.")
    else:
        await safe_reply(message, "⚠️ No session found.")

@app.on_message(filters.private & filters.command("allapprove"))
async def allapprove(client: Client, message: Message):
    if len(message.command) < 2:
        await safe_reply(message, "❗ Usage: <code>/allapprove &lt;chat_id&gt;</code>")
        return

    session_data = session_col.find_one({"_id": "session"})
    if not session_data:
        await safe_reply(message, "❌ No session found. Use <code>/newsession &lt;session_string&gt;</code> to add one.")
        return

    chat_id = message.command[1]
    try:
        async with Client(
            ":memory:",
            session_string=session_data['string'],
            api_id=API_ID,
            api_hash=API_HASH
        ) as user_client:
            approved = 0
            async for req in user_client.get_chat_join_requests(int(chat_id)):
                try:
                    await user_client.approve_chat_join_request(int(chat_id), req.user.id)
                    approved += 1
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                except Exception as err:
                    print(f"Failed to approve {req.user.id}: {err}")

            await safe_reply(message, f"✅ Approved {approved} join requests in <code>{chat_id}</code>")
    except ChatAdminRequired:
        await safe_reply(message, "❌ Error: The user session is not admin in the chat.")
    except PeerIdInvalid:
        await safe_reply(message, "❌ Error: Invalid Chat ID.")
    except Exception as e:
        await safe_reply(message, f"❌ Error occurred: {str(e)}")

@app.on_chat_join_request(filters.group | filters.channel)
async def autoapprove(client: Client, message: ChatJoinRequest):
    chat = message.chat
    user = message.user  
    print(f"{user.first_name} requested to join {chat.title} ✅")
    try:
        await client.approve_chat_join_request(chat_id=chat.id, user_id=user.id)
        if not user.is_bot:
            await client.send_message(
                user.id,
                f"<b>✦ » ʜᴇʟʟᴏ {user.mention}, ʏᴏᴜʀ ʀᴇQᴜᴇsᴛ ɪɴ {chat.title} ɪs ᴀᴜᴛᴏ-ᴀᴘᴘʀᴏᴠᴇᴅ.</b>",
                parse_mode=enums.ParseMode.HTML
            )
    except Exception as e:
        print(f"Error approving request: {e}")

if __name__ == "__main__":
    print("Auto Approved Bot started...")
    app.run()
