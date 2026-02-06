from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram import *
from pyrogram.types import *
from config import OWNER_ID
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.raw.functions.phone import CreateGroupCall, DiscardGroupCall
from pyrogram.raw.types import InputGroupCall
import aiohttp
import re
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

# Try different import approaches
try:
    # Try importing from AnonXMusic first
    from AnonXMusic import app
    print("✓ Imported app from AnonXMusic")
except ImportError:
    try:
        # Try importing from the root directory
        import AnonXMusic
        app = AnonXMusic.app
        print("✓ Imported app via AnonXMusic module")
    except ImportError:
        try:
            # Try importing directly
            import __main__
            app = __main__.app
            print("✓ Imported app from __main__")
        except AttributeError:
            # Last resort: create Client instance if needed
            print("⚠ Could not import app, you may need to pass it as parameter")
            app = None

# If app is still None, you'll need to handle this in your deployment
if app is None:
    # This is a fallback - you should configure your app properly
    from pyrogram import Client
    app = Client(
        "my_bot",
        api_id=123456,  # Replace with your actual values
        api_hash="your_api_hash",  # Replace with your actual values
        bot_token="your_bot_token"  # Replace with your actual values
    )

# vc on
@app.on_message(filters.video_chat_started)
async def brah(_, msg):
    await msg.reply("**😍ᴠɪᴅᴇᴏ ᴄʜᴀᴛ sᴛᴀʀᴛᴇᴅ🥳**")


# vc off
@app.on_message(filters.video_chat_ended)
async def brah2(_, msg):
    await msg.reply("**😕ᴠɪᴅᴇᴏ ᴄʜᴀᴛ ᴇɴᴅᴇᴅ💔**")


# invite members on vc - FIXED VERSION
@app.on_message(filters.video_chat_members_invited)
async def brah3(app: app, message: Message):
    inviter = message.from_user.mention if message.from_user else "Someone"
    
    invited_users = []
    for user in message.video_chat_members_invited.users:
        try:
            # Sirf FIRST NAME use karo (last name nahi)
            if user.first_name:
                name = user.first_name
            elif user.username:
                name = f"@{user.username}"
            else:
                name = f"User {user.id}"
            
            # Clickable mention banayein sirf first name se
            mention = f"[{name}](tg://user?id={user.id})"
            invited_users.append(mention)
        except Exception as e:
            print(f"Error processing user: {e}")
            continue

    if invited_users:
        # Sabhi users ko ek line mein space ke saath
        users_text = " ".join(invited_users)
        text = f"➻ {inviter}\n\n**๏ ɪɴᴠɪᴛɪɴɢ ɪɴ ᴠᴄ ᴛᴏ :**\n\n{users_text}"
    else:
        text = f"➻ {inviter}\n\n**๏ ɪɴᴠɪᴛɪᴏɴ ᴘᴀᴛᴀ ɴᴀʜɪ ᴄʜᴀʟᴀ :(**"

    try:
        await message.reply(
            text,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(text="๏ ᴊᴏɪɴ ᴠᴄ ๏", url=f"https://t.me/{app.username}?startgroup=true")],
                ]
            ),
            disable_web_page_preview=True  # Link preview disable karega
        )
    except Exception as e:
        print(f"Error sending message: {e}")


####


@app.on_message(filters.command("math", prefixes="/"))
def calculate_math(client, message):
    expression = message.text.split("/math ", 1)[1]
    try:
        result = eval(expression)
        response = f"ᴛʜᴇ ʀᴇsᴜʟᴛ ɪs : {result}"
    except:
        response = "ɪɴᴠᴀʟɪᴅ ᴇxᴘʀᴇssɪᴏɴ"
    message.reply(response)


@app.on_message(filters.command(["spg"], ["/", "!", "."]))
async def search(event):
    msg = await event.respond("Searching...")
    async with aiohttp.ClientSession() as session:
        start = 1
        async with session.get(
            f"https://content-customsearch.googleapis.com/customsearch/v1?cx=ec8db9e1f9e41e65e&q={event.text.split()[1]}&key=AIzaSyAa8yy0GdcGPHdtD083HiGGx_S0vMPScDM&start={start}",
            headers={"x-referer": "https://explorer.apis.google.com"},
        ) as r:
            response = await r.json()
            result = ""

            if not response.get("items"):
                return await msg.edit("No results found!")
            for item in response["items"]:
                title = item["title"]
                link = item["link"]
                if "/s" in item["link"]:
                    link = item["link"].replace("/s", "")
                elif re.search(r"\/\d", item["link"]):
                    link = re.sub(r"\/\d", "", item["link"])
                if "?" in link:
                    link = link.split("?")[0]
                if link in result:
                    # remove duplicates
                    continue
                result += f"{title}\n{link}\n\n"
            
            await msg.edit(result, reply_markup=None)
            await session.close()
