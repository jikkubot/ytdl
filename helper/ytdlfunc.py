from __future__ import unicode_literals
import os
import time
import asyncio

from pyrogram import InlineKeyboardButton
import youtube_dl
from PIL import Image
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
from utils.util import humanbytes


def buttonmap(item):
    quality = item['format']
    if "audio" in quality:
        return [
            InlineKeyboardButton(
                f"{quality} 🎵 {humanbytes(item['filesize'])}",
                callback_data=
                f"ytdata||audio||{item['format_id']}||{item['yturl']}")
        ]
    else:
        return [
            InlineKeyboardButton(
                f"{quality} 📹 {humanbytes(item['filesize'])}",
                callback_data=
                f"ytdata||video||{item['format_id']}||{item['yturl']}")
        ]


# Return a array of Buttons
def create_buttons(quailitylist):
    return map(buttonmap, quailitylist)


# extract Youtube info
def extractYt(yturl):
    ydl = youtube_dl.YoutubeDL()
    with ydl:
        qualityList = []
        r = ydl.extract_info(yturl, download=False)
        for format in r['formats']:
            # Filter dash video(without audio)
            if not "dash" in str(format['format']).lower():
                qualityList.append({
                    "format": format['format'],
                    "filesize": format['filesize'],
                    "format_id": format['format_id'],
                    "yturl": yturl
                })

        return r['title'], r['thumbnail'], qualityList


#  Need to work on progress

# def downloadyt(url, fmid, custom_progress):
#     ydl_opts = {
#         'format': f"{fmid}+bestaudio",
#         "outtmpl": "test+.%(ext)s",
#         'noplaylist': True,
#         'progress_hooks': [custom_progress],
#     }
#     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#         ydl.download([url])

# https://github.com/SpEcHiDe/AnyDLBot


async def downloadvideocli(command_to_exec):
    process = await asyncio.create_subprocess_exec(
        *command_to_exec,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    print(e_response)
    filename = t_response.split("Merging formats into")[-1].split('"')[1]
    return filename


async def downloadaudiocli(command_to_exec):
    process = await asyncio.create_subprocess_exec(
        *command_to_exec,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    print("Download error:", e_response)

    return t_response.split("Destination")[-1].split("Deleting")[0].split(":")[-1].strip()


async def get_thumb(file_path):
    file_path = os.path.normpath(file_path)
    thumb_file = os.path.join(f'thumb_{time.time()}.jpeg')
    ffmpeg_cmd = f'ffmpeg -ss 30 -i "{file_path}" -vframes 1 -vf "scale=320:-1" -y "{thumb_file}"'
    process = await asyncio.create_subprocess_exec(
        ffmpeg_cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    await process.communicate()
    if os.path.exists(thumb_file):
        resize_thumbnail(thumb_file)
        return thumb_file


def resize_thumbnail(thumb_path):
    """Return: thumb_path, height, width"""

    width = 0
    height = 0
    metadata = extractMetadata(createParser(thumb_path))

    if metadata.has("width"):
        width = metadata.get("width")

    if metadata.has("height"):
        height = metadata.get("height")

    # resize image
    img = Image.open(thumb_path)

    try:
        img.convert("RGB")
        # https://stackoverflow.com/a/37631799/4723940
        img.resize((320, height))
    finally:
        img.save(thumb_path, "JPEG")

    return thumb_path, height, width