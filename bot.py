import discord
import os
import bot_server
import asyncpraw
import random
from dotenv import load_dotenv
from yahoo_fin import stock_info as si
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('TOKEN')
REDDIT_ID = os.getenv('REDDIT_ID')
REDDIT_SECRET = os.getenv('REDDIT_SECRET')

reddit = asyncpraw.Reddit(
        client_id=REDDIT_ID,
        client_secret=REDDIT_SECRET,
        user_agent='popebot',
    )


bot = commands.Bot(command_prefix='p!')

subreddits = ['dankmeme', 'nukedmemes', 'meirl', 'okaybuddyretard']
dark_subreddits = ['offensivememesoof']
cursed_subreddits = ['cursedimages']

@bot.command()
async def ping(ctx):
    await ctx.send('Pong')

@bot.command()
async def hello(ctx):
    await ctx.send('Hello, {}!'.format(ctx.author.name))

@bot.command()
async def h(ctx):
    embedVar = discord.Embed(title="PopeBot Commands", color=0x7289da)
    embedVar.add_field(name="p!ping", value="\tSends \'pong\' in response", inline=False)
    embedVar.add_field(name="p!hello", value="\tGreets the sender", inline=False)
    embedVar.add_field(name="p!stock <ticker>", value="\tReturns real time quote data for the ticker inputted", inline=False)
    await ctx.send(embed=embedVar)

@bot.command()
async def stock(ctx, arg):
    ticker = arg
    data = si.get_quote_data(ticker)
    volume = "{:,}".format(round(data['regularMarketVolume'], 2))
    embedVar = discord.Embed(title= data['symbol']+" Data", color=0x7289da)
    embedVar.add_field(name="Symbol", value=data['symbol'], inline=False)
    embedVar.add_field(name="Company Name", value=data['shortName'], inline=False)
    embedVar.add_field(name="Market Price", value="$"+str(round(data['regularMarketPrice'], 2)), inline=False)
    embedVar.add_field(name="Price Change", value="$"+str(round(data['regularMarketChange'], 2)), inline=False)
    embedVar.add_field(name="Percent Change", value=str(round(data['regularMarketChangePercent'], 2))+"%", inline=False)
    embedVar.add_field(name="Volume", value=volume, inline=False)
    embedVar.add_field(name="Open", value="$"+str(round(data['regularMarketOpen'], 2)), inline=False)
    embedVar.add_field(name="Day's Range", value=data['regularMarketDayRange'], inline=False)

    await ctx.send(embed=embedVar)

@bot.command()
async def meme(ctx, dark: str=""):
    if dark.lower() == 'offensive':
        sub = random.choice(dark_subreddits)
    elif dark.lower() == 'cursed':
        sub = random.choice(cursed_subreddits)
    else:
        sub = random.choice(subreddits)


    submissions = (await reddit.subreddit(sub)).new(limit=50)

    submission = random.choice([submission async for submission in submissions])        
    await ctx.send(submission.url)

#at bryans request
@bot.command()
async def rule34(ctx):
    submissions = (await reddit.subreddit('rule34')).new(limit=50)

    submission = random.choice([submission async for submission in submissions])        
    await ctx.send(submission.url)

#starting the server
bot_server.keep_running()

bot.run(TOKEN)