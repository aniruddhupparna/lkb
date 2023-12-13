import os
import random
from bs4 import BeautifulSoup
import datetime
import pandas
from requests import get
import discord
# collection of unused utils

async def sort_quiz_participants(message, ctx, bot):
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

# site is not alive      
# async def pickupline_gen(message, ctx):
#     if message.content.startswith("$lkb pl"):
#         try:
#            url = 'http://www.pickuplinegen.com/'
#            resp = get(url)
#            html_soup = BeautifulSoup(resp.text, 'html.parser')
#            pickupline_content = html_soup.find_all(id="content")[0].text
#            await ctx.send(pickupline_content)
#         except Exception as e:
#             print("exception",e)
#             pass
        
def get_birthday_message():
    todays_date = datetime.datetime.now().strftime('%d-%m')
    bday_table = pandas.read_csv('bdays.csv')
    bday_candidates = bday_table.loc[bday_table['Date'] == todays_date]['Name'].tolist()
    return bday_candidates

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
    
async def send_free_game_list_to_chat(bot, free_games):
    gb_lobby = bot.get_channel(int(os.getenv('GB_GAMES')))
    message_channels = [gb_lobby]
    for msg_channel in message_channels:
        await msg_channel.send('__Free games for this week on epic:__')
        await msg_channel.send(('**{free_games}**').format(free_games=free_games))
        await msg_channel.send('check them out at: https://www.epicgames.com/store/en-US/free-games')


def get_special_event():
    todays_date = datetime.datetime.now().strftime('%d-%m')
    try:
        image_path = './images/'+todays_date+'.jpg'
        with open(image_path):
            file = discord.File(image_path)
            return file
    except Exception:
        return False