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
        caption=f"<b>✦ » ʜᴇʏ {message.from_user.mention}!</b>\n<b>✦ » ɪ ᴀᴍ ᴛᴇʟᴇɢʀᴀᴍ ʀᴇǫᴜᴇsᴛ ᴀᴘᴘʀᴏᴠᴇʀ ʙᴏᴛ ғᴏʀ ɢʀᴏᴜᴘ ᴄʜᴀɴɴᴇʟ.</b>\n\n<b>ɪ ᴄᴀɴ ᴀᴄᴄᴇᴘᴄᴛ ɴᴇᴡ ʀᴇǫᴜᴇsᴛ ᴀɴᴅ ᴘᴇɴᴅɪɴɢ ʀᴇǫᴜᴇsᴛ. ᴛᴀᴘ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴ ᴀɴᴅ sᴇᴇ ʜᴇʟᴘs ᴀɴᴅ ᴄᴏᴍᴍᴀɴᴅs.</b>",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@app.on_message(filters.private & filters.command("newsession"))
async def newsession(client: Client, message: Message):
    if len(message.command) < 2:
        await safe_reply(message, "<b>⚠️ sᴇɴᴅ ʏᴏᴜʀ ᴘʏʀᴏɢʀᴀᴍ sᴇssɪᴏɴ ʟɪᴋᴇ</b> <code>/newsession &lt;your_string_session&gt;</code>\n\n<b>ʏᴏᴜ ʜᴀᴠᴇ ɴᴏᴛ sᴇssɪᴏɴ ɢᴏ @StringFatherRobot ᴀɴᴅ ɢᴇɴ sᴇssɪᴏɴ.</b>")
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
            await safe_reply(message, f"<b>✅ sᴇssɪᴏɴ ᴀᴅᴅ sᴜᴄᴄᴇssғᴜʟʟʏ :</b> <code>{user.first_name}</code>")
    except Exception as e:
        await safe_reply(message, f"<b>❌ ɪɴᴠᴀʟɪᴅ sᴇssɪᴏɴ :</b> {str(e)}")

@app.on_message(filters.private & filters.command("removesession"))
async def removesession(client: Client, message: Message):
    result = session_col.delete_one({"_id": "session"})
    if result.deleted_count:
        await safe_reply(message, "<b>🗑️ sᴇssɪᴏɴ ʀᴇᴍᴏᴠᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ.</b>")
    else:
        await safe_reply(message, "<b>⚠️ ɴᴏ sᴇssɪᴏɴ ғᴏᴜɴᴅ.</b>")

@app.on_message(filters.private & filters.command("allapprove"))
async def allapprove(client: Client, message: Message):
    if len(message.command) < 2:
        await safe_reply(message, "<b>❗ ᴜsᴀɢᴇ :</b> <code>/allapprove &lt;channel/group id&gt;</code>\n\n<b>ғᴏʀᴡᴀʀᴅ @Purvi_Help_Bot ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟ ᴍᴇss ᴀɴᴅ ɢᴇᴛ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟ/ɢʀᴏᴜᴘ ɪᴅ ʜᴇʀᴇ.</b>")
        return

    session_data = session_col.find_one({"_id": "session"})
    if not session_data:
        await safe_reply(message, "<b>❌ ɴᴏ sᴇssɪᴏɴ ғᴏᴜɴᴅ. ᴜsᴇ</b> <code>/newsession &lt;session_string&gt;</code> <b>ᴛᴏ ᴀᴅᴅ ᴏɴᴇ.</b>")
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

            await safe_reply(message, f"<b>✅ ᴀᴘᴘʀᴏᴠᴇᴅ {approved} ᴘᴇɴᴅɪɴɢ ᴊᴏɪɴ ʀᴇǫᴜᴇsᴛs ɪɴ</b> <code>{chat_id}</code>")
    except ChatAdminRequired:
        await safe_reply(message, "<b>❌ ᴇʀʀᴏʀ : ᴛʜᴇ ᴜsᴇʀ ɴᴏᴛ ᴀᴅᴍɪɴ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ/ᴄʜᴀɴɴᴇʟ.</b>")
    except PeerIdInvalid:
        await safe_reply(message, "<b>❌ ᴇʀʀᴏʀ : ɪɴᴠᴀʟɪᴅ ᴄʜᴀɴɴᴇʟ/ɢʀᴏᴜᴘ ɪᴅ.</b>")
    except Exception as e:
        await safe_reply(message, f"<b>❌ ᴇʀʀᴏʀ ᴏᴄᴄᴏᴜʀᴅ :</b> {str(e)}")

@app.on_chat_join_request(filters.group | filters.channel)
async def autoapprove(client: Client, message: ChatJoinRequest):
    chat = message.chat
    user_id = message.from_user.id if message.from_user else message.user.id  
    user = await client.get_users(user_id)

    print(f"{user.first_name} ᴀᴘᴘʀᴏᴠᴇᴅ 👍")
    
    await client.approve_chat_join_request(chat_id=chat.id, user_id=user.id)

    if user.is_bot:
        return
    
    await client.send_message(
        user.id,
        f"<b>✦ » ʜᴇʟʟᴏ {user.mention} ʏᴏᴜ ᴀʀᴇ ɴᴏᴡ ᴀᴜᴛᴏ ᴀᴘᴘʀᴏᴠᴇᴅ ᴀ ᴄʜᴀᴛ : {chat.title}</b>\n\n<b>ᴠɪsɪᴛ » @PURVI_BOTS</b>"
    )

if __name__ == "__main__":
    print("Auto Approved Bot started...")
    app.run()
