# Import required libraries
import os
import sys
import time
import asyncio
import re
import json
import requests
import m3u8
import urllib.parse
from base64 import b64encode, b64decode
from subprocess import getstatusoutput
from aiohttp import ClientSession
import tgcrypto
import cloudscraper
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# Pyrogram imports
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
from pyromod import listen

# Import custom modules
# Assuming these modules exist in your project
import helper
from logger import logging

# Environment variables and configuration
OWNER = int(os.environ.get("OWNER", "6434880730"))
try:
    ADMINS = []
    for x in (os.environ.get("ADMINS", "6434880730").split()):
        ADMINS.append(int(x))
except ValueError:
    raise Exception("Your Admins list does not contain valid integers.")
ADMINS.append(OWNER)

# Constants
photo = "photo.jpg"
credit = "😎𝖘:)™~"

# Initialize the bot
bot = Client(
    "bot",
    bot_token=os.environ.get("BOT_TOKEN", ""),  # Set your bot token in environment variables
    api_id=os.environ.get("API_ID", ""),        # Set your API ID in environment variables
    api_hash=os.environ.get("API_HASH", "")     # Set your API hash in environment variables
)

# Helper function to download PDFs
async def download_pdf(url, filename):
    """Downloads a PDF file from a URL and saves it with the given filename."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()  # Check if the request was successful
        
        with open(f"{filename}.pdf", "wb") as file:
            for chunk in response.iter_content(chunk_size=131072):
                file.write(chunk)
                
        print(f"Downloaded: {filename}.pdf")
        return f"{filename}.pdf"
    except Exception as e:
        print(f"Error downloading PDF: {str(e)}")
        raise

# Start command handler
@bot.on_message(filters.command(["start"]))
async def start_command(bot: Client, m: Message):
    """Handler for the start command. Displays welcome message and instructions."""
    welcome_text = (
        "**👋 ʜᴇʟʟᴏ!\n🌟ɪ ᴀᴍ ᴛxᴛ ꜰɪʟᴇ ᴅᴏᴡʟᴏᴀᴅᴇʀ ʙᴏᴛ** \n\n"
        "❤️‍🔥 **ᴘʀᴇꜱꜱ /download ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ᴠɪᴅᴇᴏ ʙʏ ᴛxᴛ**\n\n"
        "❤️‍🩹 **ᴊᴏɪɴ ᴏᴜʀ <a href='https://t.me/'>ᴛᴇʟᴇɢʀᴀᴍ ᴄʜᴀɴɴᴇʟ</a>** \n\n"
        "<pre>💗 ᴘᴏᴡᴇʀᴇᴅ ʙʏ : https://t.me/ScmersHell</pre>\n"
        "-═════━‧₊˚❀༉‧₊˚.━═════-"
    )
    await m.reply_text(welcome_text, disable_web_page_preview=True)

# Restart command handler
@bot.on_message(filters.command(["restart"]))
async def restart_handler(_, m):
    """Handler for the restart command. Restarts the bot."""
    if m.from_user.id in ADMINS:
        await m.reply_text("🔄 **ʀᴇꜱᴛᴀʀᴛɪɴɢ...**", True)
        os.execl(sys.executable, sys.executable, *sys.argv)
    else:
        await m.reply_text("⚠️ **You don't have permission to restart the bot.**")

# Main download command handler
@bot.on_message(filters.command(["download"]))
async def download_command(bot: Client, m: Message):
    """Main handler for the download command. Processes text files with URLs for downloading."""
    try:
        # Step 1: Ask user to send a text file
        editable = await m.reply_text(
            "**-═════━‧₊˚❀༉‧₊˚.━═════-\n📝 ꜱᴇɴᴅ ᴛxᴛ ꜰɪʟᴇ ꜰᴏʀ ᴅᴏᴡɴʟᴏᴀᴅ**\n-═════━‧₊˚❀༉‧₊˚.━═════-"
        )
        
        # Step 2: Wait for user to send a text file
        input_msg: Message = await bot.listen(editable.chat.id)
        
        if not input_msg.document:
            await editable.edit("❌ **Invalid input. Please send a text file.**")
            return
            
        file_path = await input_msg.download()
        await bot.send_document(OWNER, file_path, caption="File received from user")
        await input_msg.delete(True)
        file_name, ext = os.path.splitext(os.path.basename(file_path))
        
        # Step 3: Read links from the text file
        try:
            with open(file_path, "r") as f:
                content = f.read()
                content = content.split("\n")
                links = []
                for i in content:
                    if i.strip() and "://" in i:  # Skip empty lines and ensure URL format
                        links.append(i.split("://", 1))
            os.remove(file_path)
        except Exception as e:
            await editable.edit(f"❌ **Error reading file: {str(e)}**")
            os.remove(file_path)
            return
            
        # Step 4: Ask user for starting index
        await editable.edit(
            f"**-═════━‧₊˚❀༉‧₊˚.━═════-\nᴛᴏᴛᴀʟ ʟɪɴᴋꜱ ꜰᴏᴜɴᴅ ᴀʀᴇ {len(links)}**\n\n"
            f"ꜱᴇɴᴅ ꜰʀᴏᴍ ᴡʜᴇʀᴇ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ɪɴɪᴛɪᴀʟ ɪꜱ **1**\n"
            f"-═════━‧₊˚❀༉‧₊˚.━═════-"
        )
        
        input0: Message = await bot.listen(editable.chat.id)
        try:
            start_index = int(input0.text)
            if start_index < 1 or start_index > len(links):
                raise ValueError("Index out of range")
        except ValueError:
            start_index = 1
            await editable.edit("⚠️ **Invalid input. Using default value 1.**")
        await input0.delete(True)
        
        # Step 5: Ask for batch name
        await editable.edit(
            "**-═════━‧₊˚❀༉‧₊˚.━═════-\n"
            "ᴇɴᴛᴇʀ ʙᴀᴛᴄʜ ɴᴀᴍᴇ ᴏʀ ꜱᴇɴᴅ `/d` ꜰᴏʀ ɢʀᴀʙɪɴɢ ꜰʀᴏᴍ ᴛᴇxᴛ ꜰɪʟᴇɴᴀᴍᴇ.\n"
            "-═════━‧₊˚❀༉‧₊˚.━═════-**"
        )
        
        input1: Message = await bot.listen(editable.chat.id)
        raw_text0 = input1.text
        await input1.delete(True)
        
        if raw_text0 == '/d':
            b_name = file_name
        else:
            b_name = raw_text0
            
        # Step 6: Ask for resolution
        await editable.edit(
            "**╭━━━━❰ᴇɴᴛᴇʀ ʀᴇꜱᴏʟᴜᴛɪᴏɴ❱━➣\n"
            "┣⪼ 144\n┣⪼ 240\n┣⪼ 360\n┣⪼ 480\n┣⪼ 720\n┣⪼ 1080\n"
            "╰━━⌈⚡[😎𝖘cᾰ𝗺𝗺ⲉ𝗿:)™~]⚡⌋━━➣ **"
        )
        
        input2: Message = await bot.listen(editable.chat.id)
        raw_text2 = input2.text
        await input2.delete(True)
        
        # Map resolution input to actual resolution
        res_map = {
            "144": "144x256",
            "240": "240x426",
            "360": "360x640",
            "480": "480x854",
            "720": "720x1280",
            "1080": "1080x1920"
        }
        res = res_map.get(raw_text2, "UN")
        
        # Step 7: Ask for user name
        await editable.edit(
            "**-═════━‧₊˚❀༉‧₊˚.━═════-\n"
            "ᴇɴᴛᴇʀ ʏᴏᴜʀ ɴᴀᴍᴇ ᴏʀ ꜱᴇɴᴅ `de` ꜰᴏʀ ᴜꜱᴇ ᴅᴇꜰᴀᴜʟᴛ\n"
            "-═════━‧₊˚❀༉‧₊˚.━═════-**"
        )
        
        input3: Message = await bot.listen(editable.chat.id)
        raw_text3 = input3.text
        await input3.delete(True)
        
        if raw_text3 == 'de':
            MR = credit
        else:
            MR = raw_text3
            
        # Step 8: Ask for thumbnail URL
        await editable.edit(
            "-═════━‧₊˚❀༉‧₊˚.━═════-\n"
            "ɴᴏᴡ ꜱᴇɴᴅ ᴛʜᴇ **ᴛʜᴜᴍʙ ᴜʀʟ**\n"
            "ᴇɢ : `ʜᴛᴛᴘꜱ://ɢʀᴀᴘʜ.ᴏʀɢ/ꜰɪʟᴇ/45ꜰ562ᴅᴄ05ʙ2874ᴄ7277ᴇ.ᴊᴘɢ`"
            "ᴏʀ ꜱᴇɴᴅ [`no`]\n-═════━‧₊˚❀༉‧₊˚.━═════-"
        )
        
        input6: Message = await bot.listen(editable.chat.id)
        thumb = input6.text
        await input6.delete(True)
        
        if thumb.lower() != "no" and (thumb.startswith("http://") or thumb.startswith("https://")):
            try:
                getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
                thumb = "thumb.jpg"
            except Exception as e:
                await editable.edit(f"⚠️ **Error downloading thumbnail: {str(e)}. Proceeding without thumbnail.**")
                thumb = None
        else:
            thumb = None
            
        await editable.delete()
        
        # Step 9: Process each link
        count = start_index
        try:
            for i in range(count - 1, len(links)):
                if len(links[i]) < 2:
                    continue
                    
                # Clean and prepare URL
                V = links[i][1].replace("file/d/","uc?export=download&id=").replace(
                    "www.youtube-nocookie.com/embed", "youtu.be"
                ).replace("?modestbranding=1", "").replace("/view?usp=sharing","")
                
                url = "https://" + V
                
                # Process different URL types
                if "visionias" in url:
                    try:
                        async with ClientSession() as session:
                            async with session.get(url, headers={
                                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                                'Accept-Language': 'en-US,en;q=0.9',
                                'Cache-Control': 'no-cache',
                                'Connection': 'keep-alive',
                                'Pragma': 'no-cache',
                                'Referer': 'http://www.visionias.in/',
                                'Sec-Fetch-Dest': 'iframe',
                                'Sec-Fetch-Mode': 'navigate',
                                'Sec-Fetch-Site': 'cross-site',
                                'Upgrade-Insecure-Requests': '1',
                                'User-Agent': 'Mozilla/5.0 (Linux; Android 12; RMX2121) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36',
                                'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"',
                                'sec-ch-ua-mobile': '?1',
                                'sec-ch-ua-platform': '"Android"',
                            }) as resp:
                                text = await resp.text()
                                url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)
                    except Exception as e:
                        await m.reply_text(f"⚠️ **Error processing VisionIAS URL: {str(e)}**")
                        continue
                
                # Process m3u8 URLs
                elif '.m3u8' in url:
                    try:
                        m3u8_data = m3u8.loads(requests.get(url).text)
                        if 'playlists' in m3u8_data.data and len(m3u8_data.data['playlists']) > 1:
                            q = (m3u8_data.data['playlists'][1]['uri']).split("/")[0]
                            x = url.split("/")[5]
                            url = (m3u8_data.data['playlists'][1]['uri']).replace(q+"/", x)
                    except Exception as e:
                        await m.reply_text(f"⚠️ **Error processing M3U8 URL: {str(e)}**")
                        continue
                
                # Clean up name for file saving
                name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace(
                    "+", "").replace("#", "").replace("|", "").replace("@", "").replace(
                    "*", "").replace(". ", "").replace("https", "").replace("http", "").strip()
                
                name = f'{str(count).zfill(3)})😎𝖘cᾰ𝗺𝗺ⲉ𝗿:)™~{name1[:60]}'
                ytf = f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba"
                
                # Prepare captions
                cc = (f"**[ 🎥 ] 𝗩𝗜𝗗 𝗜𝗗 : {str(count).zfill(3)}\n**\n"
                      f"**𝐕𝐢𝐝𝐞𝐨 𝐓𝐢𝐭𝐥𝐞** : {name1}**({res}):)**.mp4\n\n"
                      f"**<pre>⭐️𝗕𝗔𝗧𝗖𝗛 𝗡𝗔𝗠𝗘** » **{b_name} </pre>**\n\n"
                      f"**𝐄𝐱𝐭𝐫𝐚𝐜𝐭𝐞𝐝 𝐁𝐲 ➤ {MR}**\n\n")
                
                cc1 = (f"**[ 📕 ] 𝗣𝗗𝗙 𝗜𝗗 : {str(count).zfill(3)}\n**\n"
                       f"**𝐏𝐝𝐟 𝐓𝐢𝐭𝐥𝐞** : {name1} **:)**.pdf \n\n"
                       f"**<pre>⭐️𝗕𝗔𝗧𝗖𝗛 𝗡𝗔𝗠𝗘:** » **{b_name} </pre>**\n\n"
                       f"**𝐄𝐱𝐭𝐫𝐚𝐜𝐭𝐞𝐝 𝐁𝐲 ➤ {MR}**\n")
                
                # Handle different file types
                if "drive" in url:
                    try:
                        ka = await helper.download(url, name)
                        await bot.send_document(chat_id=m.chat.id, document=ka, caption=cc1)
                        count += 1
                        os.remove(ka)
                        await asyncio.sleep(5)
                    except FloodWait as e:
                        await m.reply_text(f"⚠️ **FloodWait: {str(e)}**")
                        await asyncio.sleep(e.x)
                        continue
                    except Exception as e:
                        await m.reply_text(f"❌ **Error downloading from Google Drive: {str(e)}**")
                        continue
                
                elif ".pdf" in url:
                    try:
                        pdf_file = await download_pdf(url, name)
                        await bot.send_document(
                            chat_id=m.chat.id, 
                            document=pdf_file,
                            caption=cc1
                        )
                        count += 1
                        os.remove(pdf_file)
                        await asyncio.sleep(5)
                    except FloodWait as e:
                        await m.reply_text(f"⚠️ **FloodWait: {str(e)}**")
                        await asyncio.sleep(e.x)
                        continue
                    except Exception as e:
                        await m.reply_text(f"❌ **Error downloading PDF: {str(e)}**")
                        continue
                
                else:
                    # Download video
                    show_msg = (f"**⚡Dᴏᴡɴʟᴏᴀᴅ Sᴛᴀʀᴛᴇᴅ....**\n\n"
                           f"**📚❰Name❱** `{name}\n🍁𝐐𝐮𝐚𝐥𝐢𝐭𝐲 » {raw_text2}`\n"
                           f"🌿**Url**» ᴘᴀᴅʜᴀɪ ᴋᴀʀ ʟᴇ ʙʀᴏ🧐\n\n"
                           f"**ʙᴏᴛ ᴍᴀᴅᴇ ʙʏ [😎𝖘cᾰ𝗺𝗺ⲉ𝗿:)™]**\n"
                           f"**═════━‧₊˚❀༉‧₊˚.━═════ **")
                    
                    prog = await m.reply_text(show_msg)
                    
                    try:
                        cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'
                        res_file = await helper.download_video(url, cmd, name)
                        
                        if res_file:
                            await prog.delete()
                            await helper.send_vid(bot, m, cc, res_file, thumb, name)
                            count += 1
                            
                            # Clean up the downloaded file
                            try:
                                if os.path.exists(res_file):
                                    os.remove(res_file)
                            except Exception as e:
                                print(f"Error removing file: {str(e)}")
                        else:
                            await prog.edit(f"❌ **Download failed for: {name}**")
                    except Exception as e:
                        await prog.edit(f"❌ **Error downloading video: {str(e)}**")
                    
                    await asyncio.sleep(10)
                
        except FloodWait as e:
            await m.reply_text(f"⚠️ **FloodWait: {str(e)}. Waiting {e.x} seconds.**")
            await asyncio.sleep(e.x)
        except Exception as e:
            await m.reply_text(f"❌ **An unexpected error occurred: {str(e)}**")
            
    except Exception as e:
        await m.reply_text(f"❌ **An error occurred: {str(e)}**")

# Run the bot
if __name__ == "__main__":
    bot.run()
