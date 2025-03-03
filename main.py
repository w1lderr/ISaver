import os
import sys
import uuid
import asyncio
import logging
import tempfile
import validators
from config import TOKEN
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile
from identify_platform import identify_platform
from download_video import download_video
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.types import (
    Message, 
    InlineKeyboardButton, 
    InlineKeyboardMarkup,
    CallbackQuery,
    FSInputFile
)

dp = Dispatcher()
message_queue = asyncio.Queue()

def get_start_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📥 Download video",
                    callback_data="download_video"
                )
            ],
            [
                InlineKeyboardButton(
                    text="ℹ️ Help",
                    callback_data="help"
                )
            ]
        ]
    )
    return keyboard

@dp.message(F.text == "/start")
async def welcome_handler(message: Message) -> None:
    welcome_text = (
        f"👋 Hello {message.from_user.full_name}!\n\n"
        "I'm a Video saver bot. I can help you download "
        "videos from YouTube Shorts, TikTok and Instagram Reels.\n\n"
        "Click the button below to start downloading or get help!"
    )
    await message.answer(text=welcome_text, reply_markup=get_start_keyboard())

@dp.callback_query(F.data == "download_video")
async def download_instruction(callback: CallbackQuery) -> None:
    instruction_text = (
        "🔗 Send me the video link."
    )
    await callback.message.answer(instruction_text)
    await callback.answer()

@dp.callback_query(F.data == "help")
async def help_handler(callback: CallbackQuery) -> None:
    help_text = (
        "💡 How to use this bot:\n\n"
        "1️⃣ Click the button\n"
        "2️⃣ Send the video link\n"
        "3️⃣ Wait for the video to download\n\n"
        "❓ Having issues? Make sure the video is public and accessible"
    )
    await callback.message.answer(help_text, reply_markup=get_start_keyboard())
    await callback.answer()

@dp.message()
async def process_media_url(message: Message) -> None:
    await message_queue.put(message)
    
    if message_queue.qsize() == 1:
        asyncio.create_task(process_queue())

async def process_queue() -> None:
    while not message_queue.empty():
        message = await message_queue.get()
        
        if validators.url(message.text):
            platform = identify_platform(message.text)
            if platform:
                download_msg = await message.answer(f"Downloading {platform} video...")
                try:
                    temp_uuid = str(uuid.uuid4())
                    with tempfile.TemporaryDirectory() as temp_dir:
                        temp_file_path = os.path.join(temp_dir, f"{temp_uuid}")
                        
                        video_path = download_video(message.text, temp_file_path, platform)
                        
                        if video_path and os.path.exists(video_path):
                            video = FSInputFile(video_path)
                            await message.reply_video(video=video)
                        else:
                            pass
                        if video_path and os.path.exists(video_path):
                            os.remove(video_path)
                
                except Exception as e:
                    logging.error(f"Error processing video: {e}")
                    await message.reply(f"Error processing video: {str(e)}")
                
                finally:
                    await download_msg.delete()
            else:
                pass
        else:
            pass
        message_queue.task_done()

async def main() -> None:
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        stream=sys.stdout
    )
    asyncio.run(main())