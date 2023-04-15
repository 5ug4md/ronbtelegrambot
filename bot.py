import asyncio
import instaloader
from instaloader import Post
from aiogram import Bot, types
from aiogram.utils import exceptions
from aiogram.types import ParseMode
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_polling
import os

#setting up Instaloader
L = instaloader.Instaloader()

# insta profilename
PROFILE_NAME = "routineofnepalbanda"

# create a bot object
BOT_TOKEN = "ENTER YOUT BOT TOKEN HERE"
bot_telegram = Bot(token=BOT_TOKEN)

#creating a dispatcher
dp = Dispatcher(bot_telegram)

#initializing the last sent_post_id to None
sent_post_id = None

async def sendPost():
    #checking if bot passed till here without errors
    print("Bot is UP")
    global sent_post_id
    profile = instaloader.Profile.from_username(L.context, PROFILE_NAME)
    posts = profile.get_posts()
    post = next(posts)
    if post.shortcode != sent_post_id:
        #sendig post to telegram using aiogram module
        try:
            chat_id = 'ENTER YOUR CHAT ID HERE'
            await bot_telegram.send_photo(chat_id=chat_id, photo=post.url, caption=post.caption)
        except exceptions.TelegramAPIError as e:
            if e.error_code == 400:
                return False
            else:
                raise e
        #updating last sent_post_id with the id of the recently sent post
        sent_post_id = post.shortcode

async def main():
    while True:
        await sendPost()
        #i've set the delay to 1 hours but you can change it as per your needs
        await asyncio.sleep(3600)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Program stopped by user')
 
