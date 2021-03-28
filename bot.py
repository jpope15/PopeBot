import discord
import os
import bot_server
import asyncpraw
import random
from dotenv import load_dotenv
from yahoo_fin import stock_info as si
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

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
programmer_subreddits = ['programmerhumor']
monke_subreddits = ['monke', 'ape']

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send('This command is on a %.2fs cooldown' % error.retry_after)
    raise error  

@bot.command(help='sends pong in response')
async def ping(ctx):
    await ctx.send('Pong')

@bot.command(help='Greets the sender')
async def hello(ctx):
    await ctx.send('Hello, {}!'.format(ctx.author.name))

@bot.command(help='returns real-time stock data on the symbol inputted')
async def stock(ctx, symbol):
    ticker = symbol
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

@bot.command(help='Returns a meme\n\nmeme_type:\n\t-offensive\n\t-programmer')
async def meme(ctx, meme_type: str=""):
    if meme_type.lower() == 'offensive':
      sub = random.choice(dark_subreddits)
    elif  meme_type.lower() == 'programmer':
      sub = random.choice(programmer_subreddits)
    else:
      sub = random.choice(subreddits)


    submissions = (await reddit.subreddit(sub)).new(limit=50)

    submission = random.choice([submission async for submission in submissions])        
    await ctx.send(submission.url)

#at bryans request
@bot.command(help='returns a NSFW picture')
@commands.cooldown(1, 15, commands.BucketType.guild)
async def rule34(ctx):
  if not ctx.channel.is_nsfw():
    await ctx.send('Cannot use that command here.')
  else:
    if ctx.author == 'Boran#3803':
      await ctx.send('You are banned from this command')
    else: 
      submissions = (await reddit.subreddit('rule34')).new(limit=50)

      submission = random.choice([submission async for submission in submissions])        
      await ctx.send(submission.url)

@bot.command(help='returns a picture of a monkey')
async def monke(ctx):
      submissions = (await reddit.subreddit(random.choice(monke_subreddits))).new(limit=50)
      submission = random.choice([submission async for submission in submissions])        
      await ctx.send(submission.url)

#starting the server
bot_server.keep_running()

bot.run(TOKEN)
