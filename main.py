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
        caption=f"""**✦ » ʜᴇʏ {message.from_user.mention}! 🌸**

**✦ » ɪ ᴀᴍ ᴀ ᴘᴏᴡᴇʀғᴜʟ ᴛᴀɢɢᴇʀ ʙᴏᴛ 🤖**
**✦ » ɪ ᴄᴀɴ ᴛᴀɢ ᴀʟʟ ᴍᴇᴍʙᴇʀs ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ⚡**
**✦ » ғᴀsᴛ ᴀɴᴅ sᴍᴏᴏᴛʜ ᴛᴀɢɢɪɴɢ sʏsᴛᴇᴍ 🚀**
**✦ » ᴊᴜsᴛ ᴀᴅᴅ ᴍᴇ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴀɴᴅ ᴍᴀᴋᴇ ᴍᴇ ᴀᴅᴍɪɴ 🥂**

**✦ » ᴄᴏᴍᴍᴀɴᴅs :**

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
    except Exception:
        pass

    replied = message.reply_to_message
    text = message.text.split(None, 1)[1] if len(message.command) > 1 else ""

    if not replied and not text:
        return await message.reply("**» ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ/ɢɪᴠᴇ ᴛᴇxᴛ ᴛᴏ ᴛᴀɢ ᴀʟʟ ʟɪᴋᴇ »** `/all Hi Friends`")

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
            usertxt += f"⊚ [{member.user.first_name}](tg://user?id={member.user.id})\n"

            if usernum == 5:
                try:
                    if replied:
                        await replied.reply_text(
                            f"{text}\n\n{usertxt}\n**🏆 ᴛᴏᴛᴀʟ** `{total_tagged}` **ᴜsᴇʀs ᴛᴀɢs ᴅᴏɴᴇ...**"
                        )
                    else:
                        await message.reply_text(
                            f"{text}\n\n{usertxt}\n**🏆 ᴛᴏᴛᴀʟ** `{total_tagged}` **ᴜsᴇʀs ᴛᴀɢs ᴅᴏɴᴇ...**"
                        )
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                except Exception:
                    pass

                await asyncio.sleep(3)
                usernum, usertxt = 0, ""

        if usertxt:
            try:
                if replied:
                    await replied.reply_text(
                        f"{text}\n\n{usertxt}\n**🏆 ᴛᴏᴛᴀʟ** `{total_tagged}` **ᴜsᴇʀs ᴛᴀɢs ᴅᴏɴᴇ...**"
                    )
                else:
                    await message.reply_text(
                        f"{text}\n\n{usertxt}\n**🏆 ᴛᴏᴛᴀʟ** `{total_tagged}` **ᴜsᴇʀs ᴛᴀɢs ᴅᴏɴᴇ...**"
                    )
            except Exception:
                pass

        await message.reply(f"✅ **ᴛᴀɢ ᴄᴏᴍᴘʟᴇᴛᴇᴅ. ᴛᴏᴛᴀʟ :-** `{total_tagged}` **ᴜsᴇʀs.**")

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
