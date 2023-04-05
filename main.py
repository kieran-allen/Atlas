from dotenv import load_dotenv
from guilds import allow_list

import openai
import discord
import os

load_dotenv()

OPEN_API_KEY = os.getenv("OPEN_API_KEY")
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

openai.api_key = OPEN_API_KEY
bot = discord.Bot(intents=intents)

threads = set()


@bot.event
async def on_ready():
    print(f'{bot.user} is ready and online!')


@bot.slash_command(name="chat", description="Chat with chatGPT", guild_ids=allow_list)
async def hello(ctx: discord.ApplicationContext, query: str):
    channel_id = ctx.channel_id

    if channel_id in threads:
        # we are in a thread.
        await ctx.respond("Thread already exists")
    else:
        await ctx.respond("Starting a new thread!")
        message = await ctx.send(query)
        thread = await message.create_thread(name="thread name", auto_archive_duration=60)
        # since we only care about the key we are setting to None.
        threads.add(thread.id)

bot.run(DISCORD_BOT_TOKEN)
