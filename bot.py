from discord.ext import commands
import discord
import os
import bot_server
from dotenv import load_dotenv
from yahoo_fin import stock_info as si

bot = commands.Bot(command_prefix='p!')
load_dotenv()
TOKEN = os.getenv('TOKEN')

@bot.command()
async def ping(ctx):
    await ctx.send('Pong')

@bot.command()
async def hello(ctx):
    await ctx.send('Hello, {}!'.format(ctx.author.name))

@bot.command()
async def help(ctx):
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


#starting the server
bot_server.keep_running()

bot.run(TOKEN)
