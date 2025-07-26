from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, ChatJoinRequest
from pyrogram.errors import ChatAdminRequired, FloodWait, PeerIdInvalid
from pymongo import MongoClient
from pyrogram.types import CallbackQuery
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
    parse_mode=enums.ParseMode.HTML  
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
        [InlineKeyboardButton("⚜️ ᴀᴅᴅ ᴍᴇ ʙᴀʙʏ ⚜️", url=f"https://t.me/{approved_bot.username}?startgroup=botstart")],
        [InlineKeyboardButton("🔸 ᴏᴡɴᴇʀ 🔸", user_id=7473021518),
         InlineKeyboardButton("🔅 ᴜᴘᴅᴀᴛᴇs 🔅", url="https://t.me/PURVI_UPDATES")],
        [InlineKeyboardButton("🔺 ʜᴇʟᴘ & ᴄᴏᴍᴍᴀɴᴅs 🔺", callback_data="help")]
    ]
    
    photo_url = "https://files.catbox.moe/yy0ukm.jpg"
    
    await client.send_photo(
        chat_id=message.chat.id,
        photo=photo_url,
        caption=(
            f"<b>✦ » ʜᴇʏ {message.from_user.mention}!</b>\n\n"
            f"<b>✦ » ɪ ᴀᴍ ᴛᴇʟᴇɢʀᴀᴍ ʀᴇǫᴜᴇsᴛ ᴀᴘᴘʀᴏᴠᴇʀ ʙᴏᴛ ғᴏʀ ɢʀᴏᴜᴘ ᴄʜᴀɴɴᴇʟ.</b>\n\n"
            f"<b>✦ » ɪ ᴄᴀɴ ᴀᴄᴄᴇᴘᴛ ɴᴇᴡ ʀᴇǫᴜᴇsᴛs ᴀɴᴅ ᴘᴇɴᴅɪɴɢ ʀᴇǫᴜᴇsᴛs. ᴛᴀᴘ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴛᴏ sᴇᴇ ᴄᴏᴍᴍᴀɴᴅs & ʜᴇʟᴘ.</b>\n\n"
            f"<b>✦ » 𝐏ᴏᴡᴇʀᴇᴅ 𝐁ʏ » <a href='https://t.me/TheSigmaCoder'>⎯᪵፝֟፝֟⎯꯭𓆩꯭ 𝐀 ꯭ʟ ꯭ᴘ ꯭ʜ꯭ ᴧ꯭⎯꯭꯭‌꯭🥂꯭༎꯭ 𓆪</a></b>"
        ),
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@app.on_message(filters.private & filters.command("newsession"))
async def newsession(client: Client, message: Message):
    if len(message.command) < 2:
        await safe_reply(message, "<b>⚠️ sᴇɴᴅ ʏᴏᴜʀ ᴘʏʀᴏɢʀᴀᴍ sᴇssɪᴏɴ ʟɪᴋᴇ</b> <code>/newsession &lt;your_session&gt;</code>")
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
    try:
        user_id = message.from_user.id
        result = session_col.delete_one({"user_id": user_id})

        if result.deleted_count:
            await safe_reply(message, "<b>🗑️ sᴇssɪᴏɴ ʀᴇᴍᴏᴠᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ.</b>")
        else:
            await safe_reply(message, "<b>🚫 ʏᴏᴜ ᴅɪᴅɴ'ᴛ ᴀᴅᴅ ᴀɴʏ sᴇssɪᴏɴ, ᴘʟᴇᴀsᴇ ᴀᴅᴅ ғɪʀsᴛ.</b>")

    except Exception as e:
        await safe_reply(
            message,
            f"<b>❌ ᴇʀʀᴏʀ ᴡʜɪʟᴇ ʀᴇᴍᴏᴠɪɴɢ sᴇssɪᴏɴ:\n<code>{e}</code></b>"
        )

@app.on_message(filters.private & filters.command("allapprove"))
async def allapprove(client: Client, message: Message):
    if len(message.command) < 2:
        await safe_reply(message, "<b>❗ ᴜsᴀɢᴇ :</b> <code>/allapprove &lt;channel/group id&gt;</code>")
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


@app.on_callback_query(filters.regex("help"))
async def help_callback(_, query):
    await query.message.edit_caption(
        caption=(
            "<b><u>⊚ ʜᴇʀᴇ ᴍʏ ʜᴇʟᴘ ꜰᴜɴᴄᴛɪᴏɴs.</u></b>\n\n"
            "<b><u>✦ ᴀᴜᴛᴏ ʀᴇǫᴜᴇsᴛ ᴀᴘᴘʀᴏᴠᴇ :-</u> ᴀᴅᴅ ᴍᴇ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ/ᴄʜᴀɴɴᴇʟ ᴀɴᴅ ᴍᴀᴋᴇ ᴍᴇ ᴀᴅᴍɪɴ, ɪ ᴡɪʟʟ ʜᴀɴᴅʟᴇ ᴛʜᴇ ʀᴇsᴛ.</b>\n\n"
            "<b><u>⦿ ᴘᴇɴᴅɪɴɢ ʀᴇǫᴜᴇsᴛ ᴀᴘᴘʀᴏᴠᴇ :-</u></b>\n\n"
            "➻ /start - <b>sᴛᴀʀᴛ ʙᴏᴛ.</b>\n"
            "➻ /newsession - <b>ᴀᴅᴅ ɴᴇᴡ sᴇssɪᴏɴ.</b>\n"
            "➻ /removesession - <b>ʀᴇᴍᴏᴠᴇ sᴇssɪᴏɴ.</b>\n"
            "➻ /allapprove - <b>ᴀᴘᴘʀᴏᴠᴇ ᴘᴇɴᴅɪɴɢ ʀᴇǫᴜᴇsᴛs.</b>\n\n"
            "<b><u>✦ ʜᴏᴡ ᴛᴏ ɢᴇᴛ ᴄʜᴀɴɴᴇʟ, ɢʀᴏᴜᴘ ɪᴅ ᴀɴᴅ sᴇssɪᴏɴ ??</u></b>\n\n"
            "<b>:⧽ ᴄʜᴀɴɴᴇʟ ɪᴅ :- ғᴏʀᴡᴀʀᴅ @Purvi_Help_Bot ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟ ᴍᴇssᴀɢᴇ ᴀɴᴅ ɢᴇᴛ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟ ɪᴅ.</b>\n\n"
            "<b>:⧽ ɢʀᴏᴜᴘ ɪᴅ :- ᴀᴅᴅ @MissRose_bot ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴀɴᴅ ᴛʏᴘᴇ</b> <code>/id</code> <b>ᴛʜᴇɴ ɢᴇᴛ ɪᴅ.</b>\n\n"
            "<b>:⧽ sᴛʀɪɴɢ sᴇssɪᴏɴ :- ɢᴏ ᴛᴏ @StringFatherRobot ᴀɴᴅ ɢᴇɴᴇʀᴀᴛᴇ ʏᴏᴜʀ ᴘʏʀᴏɢʀᴀᴍ sᴇssɪᴏɴ.</b>"
        ),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔸 ʙᴀᴄᴋ 🔸", callback_data="start_back"),
            InlineKeyboardButton("🔸 ᴄʟᴏsᴇ 🔸", callback_data="close")]
        ]),
        parse_mode=enums.ParseMode.HTML
    )

@app.on_callback_query(filters.regex("close"))
async def close_callback(client, callback_query):
    try:
        await callback_query.message.delete()
    except:
        pass
    await callback_query.answer()

@app.on_callback_query(filters.regex("start_back"))
async def start_back_callback(_, query: CallbackQuery):
    bot_username = (await app.get_me()).username
    await query.message.edit_text(
        f"<b>✦ » ʜᴇʏ {query.from_user.mention}!</b>\n\n"
        f"<b>✦ » ɪ ᴀᴍ ᴛᴇʟᴇɢʀᴀᴍ ʀᴇǫᴜᴇsᴛ ᴀᴘᴘʀᴏᴠᴇʀ ʙᴏᴛ ғᴏʀ ɢʀᴏᴜᴘ ᴄʜᴀɴɴᴇʟ.</b>\n\n"
        f"<b>✦ » ɪ ᴄᴀɴ ᴀᴄᴄᴇᴘᴛ ɴᴇᴡ ʀᴇǫᴜᴇsᴛ ᴀɴᴅ ᴘᴇɴᴅɪɴɢ ʀᴇǫᴜᴇsᴛs. ᴛᴀᴘ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴛᴏ sᴇᴇ ᴄᴏᴍᴍᴀɴᴅs & ʜᴇʟᴘ.</b>\n\n"
        f"<b>✦ » 𝐏ᴏᴡᴇʀᴇᴅ 𝐁ʏ » <a href='https://t.me/TheSigmaCoder'>⎯᪵፝֟፝֟⎯꯭𓆩꯭ 𝐀 ꯭ʟ ꯭ᴘ ꯭ʜ꯭ ᴧ꯭⎯꯭꯭‌꯭🥂꯭༎꯭ 𓆪</a></b>",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("⚜️ ᴀᴅᴅ ᴍᴇ ʙᴀʙʏ ⚜️", url=f"https://t.me/{bot_username}?startgroup=botstart")],
                [InlineKeyboardButton("🔸 ᴏᴡɴᴇʀ 🔸", user_id=7473021518),
                 InlineKeyboardButton("🔅 ᴜᴘᴅᴀᴛᴇs 🔅", url="https://t.me/PURVI_UPDATES")],
                [InlineKeyboardButton("🔺 ʜᴇʟᴘ & ᴄᴏᴍᴍᴀɴᴅs 🔺", callback_data="help")]
            ]
        )
    )

if __name__ == "__main__":
    print("Auto Approved Bot started...")
    app.run()
