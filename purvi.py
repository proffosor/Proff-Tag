import asyncio
from pyrogram import Client, filters, enums
from pyrogram.errors import UserNotParticipant, FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
import os

spam_chats = set()

API_ID = int(os.getenv("API_ID", "10079905"))
API_HASH = os.getenv("API_HASH", "e4a5fa251e2e055f26e5c2add8401530")
BOT_TOKEN = os.getenv("BOT_TOKEN", None)

app = Client(
    "Tagger Bot",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH
)

@app.on_message(filters.private & filters.command(["start"]))
async def start(client: app, message: Message):
    approved_bot = await client.get_me()
    buttons = [
        [InlineKeyboardButton("⚜️ ᴀᴅᴅ ᴍᴇ ʙᴀʙʏ ⚜️", url=f"http://t.me/{approved_bot.username}?startgroup=botstart")],
        [InlineKeyboardButton("🔸 sᴜᴘᴘᴏʀᴛ 🔸", url="https://t.me/+UUms38xWttkzM2M1"),
         InlineKeyboardButton("▫️ ᴜᴘᴅᴀᴛᴇs ▫️", url="https://t.me/+6Cjm9Jh3qyQ0ODJl")]
    ]
    photo_url = "https://files.catbox.moe/yy0ukm.jpg"

    await client.send_photo(
        chat_id=message.chat.id,
        photo=photo_url,
        caption=f"""**✦ ʜᴇʏ {message.from_user.mention}! 🌸**

**▸ ɪ ᴀᴍ ᴘᴏᴡᴇʀғᴜʟ ᴛᴀɢɢᴇʀ ʙᴏᴛ 🤖**
**▸ ғᴀsᴛ & sᴍᴏᴏᴛʜ ᴛᴀɢɢɪɴɢ sʏsᴛᴇᴍ 🚀**
**▸ ɪ ᴄᴀɴ ᴛᴀɢ ᴀʟʟ ᴍᴇᴍʙᴇʀs ɪɴ ɢʀᴏᴜᴘ ⚡**
**▸ ᴊᴜsᴛ ᴀᴅᴅ ᴍᴇ ɪɴ ɢʀᴏᴜᴘ & ᴍᴀᴋᴇ ᴀᴅᴍɪɴ 🥂**

**❏ ᴄᴏᴍᴍᴀɴᴅs :**

• /tagall - sᴛᴀʀᴛ ᴛᴀɢ ᴀʟʟ 👥  
• /stop - sᴛᴏᴘ ᴛᴀɢ ❌  
━━━━━━━━━━━━━━━━━━

""",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@app.on_message(filters.command(["utag", "all", "mention", "tagall"], prefixes=["/", "@"]))
async def tag_all_users(client: Client, message: Message):

    if message.chat.type == enums.ChatType.PRIVATE:
        return await message.reply("⬤ **ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴏɴʟʏ ғᴏʀ ɢʀᴏᴜᴘs.**")

    member = await client.get_chat_member(message.chat.id, message.from_user.id)
    if member.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
        return await message.reply("⬤ **ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ʙᴀʙʏ.**")

    try:
        await message.delete()
    except:
        pass

    replied = message.reply_to_message
    text = message.text.split(None, 1)[1] if len(message.command) > 1 else ""

    if not replied and not text:
        return await message.reply("**» ʀᴇᴘʟʏ ᴏʀ ɢɪᴠᴇ ᴛᴇxᴛ »** `/all hi ғʀɪᴇɴᴅs`")

    spam_chats.add(message.chat.id)
    usernum, usertxt, total_tagged = 0, "", 0

    try:
        async for member in client.get_chat_members(message.chat.id):
            if message.chat.id not in spam_chats:
                break

            if not member.user or member.user.is_bot:
                continue

            usernum += 1
            total_tagged += 1

            usertxt += f"[{member.user.first_name}](tg://user?id={member.user.id}), "

            if usernum == 20:
                try:
                    final_text = f"""**{text}**

{usertxt.strip(', ')}

**🏆 ᴛᴏᴛᴀʟ ** `{total_tagged}` ᴜsᴇʀs ᴛᴀɢɢᴇᴅ**"""

                    if replied:
                        await replied.reply_text(final_text)
                    else:
                        await message.reply_text(final_text)

                except FloodWait as e:
                    await asyncio.sleep(e.value)
                except:
                    pass

                await asyncio.sleep(3)
                usernum, usertxt = 0, ""

        if usertxt:
            final_text = f"""**{text}**

{usertxt.strip(', ')}

**🏆 ᴛᴏᴛᴀʟ ** `{total_tagged}` **ᴜsᴇʀs ᴛᴀɢɢᴇᴅ.**"""

            if replied:
                await replied.reply_text(final_text)
            else:
                await message.reply_text(final_text)

        await message.reply(f"✅ **ᴛᴀɢ ᴄᴏᴍᴘʟᴇᴛᴇᴅ.**\n\n**» ᴛᴏᴛᴀʟ :** `{total_tagged}` **ᴜsᴇʀs.**")

    finally:
        spam_chats.discard(message.chat.id)


@app.on_message(filters.command(["cancel", "stop"], prefixes=["/", "@"]))
async def cancel_spam(client: Client, message: Message):
    # Private chat check
    if message.chat.type == enums.ChatType.PRIVATE:
        return await message.reply("⬤ **ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴏɴʟʏ ғᴏʀ ɢʀᴏᴜᴘs.**")

    chat_id = message.chat.id

    if chat_id not in spam_chats:
        return await message.reply("**» ɪ'ᴍ ɴᴏᴛ ᴛᴀɢɢɪɴɢ ᴀɴʏᴏɴᴇ ʀɪɢʜᴛ ɴᴏᴡ.**")

    try:
        member = await client.get_chat_member(chat_id, message.from_user.id)
        if member.status not in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):
            return await message.reply("⬤ **ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ʙᴀʙʏ.**")
    except UserNotParticipant:
        return await message.reply("**» ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀ ᴘᴀʀᴛɪᴄɪᴘᴀɴᴛ ᴏғ ᴛʜɪs ᴄʜᴀᴛ.**")
    except Exception:
        return await message.reply("**» ᴇʀʀᴏʀ ᴄʜᴇᴄᴋɪɴɢ ᴀᴅᴍɪɴ sᴛᴀᴛᴜs.**")

    spam_chats.discard(chat_id)
    return await message.reply("**🚫 ᴛᴀɢɢɪɴɢ ᴄᴀɴᴄᴇʟʟᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ.**")



if __name__ == "__main__":
    print("Tagger Bot started... 🚀")
    app.run()
