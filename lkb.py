import os
import discord
import random
import pandas
import datetime
from dotenv import load_dotenv
from discord.ext import commands,tasks
from requests import get
from bs4 import BeautifulSoup

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='$', intents=intents)
client = discord.Client()

def get_birthday_message():
    todays_date = datetime.datetime.now().strftime('%d-%m')
    bday_table = pandas.read_csv('bdays.csv')
    bday_candidates = bday_table.loc[bday_table['Date'] == todays_date]['Name'].tolist()
    return bday_candidates

def get_special_event():
    todays_date = datetime.datetime.now().strftime('%d-%m')
    try:
        image_path = './images/'+todays_date+'.jpg'
        with open(image_path):
            file = discord.File(image_path)
            return file
    except Exception:
        return False

def get_free_game_list():
    day_of_week = datetime.datetime.today().weekday()
    try:
        if day_of_week == 4 :
            url = 'https://store-site-backend-static-ipv4.ak.epicgames.com/freeGamesPromotions?locale=en-US&country=IN&allowCountries=IN'
            resp = get(url)
            data = resp.json()
            all_free_games = data.get('data',{}).get('Catalog',{}).get('searchStore',{}).get('elements',[])
            discounted_games = [game['title'] for game in all_free_games if (game['price']['totalPrice']['originalPrice']) > 0 and (game['price']['totalPrice']['discountPrice'] == 0)]
            return (", ").join(discounted_games)
    except Exception:
        return False

@tasks.loop(hours=24)
async def daily_schedule():
    await bot.wait_until_ready()
    await bot.change_presence(activity=discord.Activity(name=f'$lkb <BlaBlaBla>', type=discord.ActivityType.listening))
    bsk3s_general_channel_id = os.getenv('BSK3S_GENERAL_CHANNEL_ID')
    # bsk3s_general_channel_id = os.getenv('TEST_CHANNEL_ID') # test channel id in private server
    bsk3s_message_channel = bot.get_channel(int(bsk3s_general_channel_id))

    if messages := get_birthday_message():
        for entry in messages:
            await bsk3s_message_channel.send('Happy Birthday '+ entry + '   \U0001F389  .Live long and prosper')
    
    if special_event := get_special_event():
        await bsk3s_message_channel.send(file=special_event)

    if free_games := get_free_game_list():
        gb_lobby = bot.get_channel(int(os.getenv('GB_GAMES')))
        message_channels = [gb_lobby]
        for msg_channel in message_channels:
            await msg_channel.send('__Free games for this week on epic:__')
            await msg_channel.send(('**{free_games}**').format(free_games=free_games))
            await msg_channel.send('check them out at: https://www.epicgames.com/store/en-US/free-games')

@bot.command(name='lkb')
async def lkb(ctx):
    message = ctx.message
    if message.author == client.user:
            return

    curse_vocabulary = [
        'Lowde ke baal',
        'Nin tika naimari keya',
        'Tika tinnu',
        'Oorsoole',
        'Gaandu tulla',
        'Tunne unnu',
        'Nin tikakk benki haaka',
        'Shenda',
        'Tika muchkond iru',
        'Halka nan magne',
        'Nin shatak benki haka'
    ]

    praise_vocabulary = [
        'Big PP'
    ]

    if message.content.startswith("$lkb sh"):
        try:
            content = message.content.replace('$lkb sh', '').strip()
            if content.startswith('#'):
                channel = bot.get_channel(int(os.getenv('TLTO_CHANNEL_ID')))
                message_id = content.replace('#', '')
                message = await channel.fetch_message(message_id)
                users = set()
                
                for reaction in message.reactions:
                    async for user in reaction.users():
                        users.add(user)
                participants = [user.name for user in users]
            elif content:
                participants = content.split(",")
            else:
                participants = bot.get_guild(int(os.getenv('BSK3S_GUILD'))).members
                participants = [user.nick or user.name for user in participants if not user.bot]
            random.shuffle(participants)
            await ctx.send("\n".join(participants))
        except Exception as e:
            print("exception",e)
            pass
    
    if message.content.startswith("$lkb pl"):
        try:
           url = 'http://www.pickuplinegen.com/'
           resp = get(url)
           html_soup = BeautifulSoup(resp.text, 'html.parser')
           pickupline_content = html_soup.find_all(id="content")[0].text
           await ctx.send(pickupline_content)
        except Exception as e:
            print("exception",e)
            pass

    elif message.content.startswith("$lkb"):
        target = message.content.replace('$lkb', '').strip()
        
        if target.lower().find('ani') != -1 or target.lower().find('aniruddh') != -1 or target.lower().find('preet') != -1:
            file = discord.File('./audio/no_way.mp3')
            await ctx.send(file=file)
        else:
            response = target +', '+ random.choice(curse_vocabulary)
            if ctx.message.guild.id == int(os.getenv('BSK3S_GUILD')):
                await ctx.send(response)
            else:
                await ctx.send('This server is not NSFW enough :)')

daily_schedule.start()
bot.run(TOKEN)