import os
import discord
from dotenv import load_dotenv
from discord.ext import commands,tasks
from utils import sort_quiz_participants, get_free_game_list, send_free_game_list_to_chat, get_special_event
from chat import chat_with_hf_model
import datetime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)
client = discord.Client(intents=intents)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(f"<@{os.getenv("BOT_ID")}>"):
        question = message.content.replace(f'<@{os.getenv("BOT_ID")}>', '').strip()
        reply_from_bot = chat_with_hf_model(question)
        await message.channel.send(reply_from_bot)
    
    return
    
@tasks.loop(hours=24)
async def daily_schedule():
    await bot.wait_until_ready()
    await bot.change_presence(activity=discord.Activity(name=f'$lkb <BlaBlaBla>', type=discord.ActivityType.listening))
    # bsk3s_general_channel_id = os.getenv('BSK3S_GENERAL_CHANNEL_ID')
    bsk3s_general_channel_id = os.getenv('TEST_CHANNEL_ID') # test channel id in private server
    bsk3s_message_channel = bot.get_channel(int(bsk3s_general_channel_id))

    # if messages := get_birthday_message():
    #     for entry in messages:
    #         await bsk3s_message_channel.send('Happy Birthday '+ entry + '   \U0001F389  .Live long and prosper')
    
    if special_event := get_special_event():
        await bsk3s_message_channel.send(file=special_event)

    if free_games := get_free_game_list():
        send_free_game_list_to_chat(bot, free_games)
        
# @bot.command(name='lkb')
# async def lkb(ctx):
#     message = ctx.message
#     if message.author == client.user:
#         return

#     if message.content.startswith("$lkb sh"):
#         await sort_quiz_participants(message, ctx, bot)
    
# daily_schedule.start()

client.run(TOKEN, log_handler=None)