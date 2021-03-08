import discord
import os
import bot_server
from dotenv import load_dotenv
from yahoo_fin import stock_info as si

load_dotenv()
TOKEN = os.getenv('TOKEN')
client = discord.Client()


#TODO
#add a help feature
#   -p!help
#   -lists commands and a description


#add a meme feature
#   -p!meme
#   -scrapes reddit for new memes
#   -always refreshed

#DONE
#stock market feature
#   -p!stock <ticker>
#   -live prices
#   -ticker : price : %increase 
#   -maybe paper trades in the future

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

    #ignore messages made by bot
    if message.author == client.user:
        return

    #pretty self explanatory
    elif message.content.startswith('p!hello'):
        await message.channel.send('Dont talk to me ever again {}'.format(message.author.name))

    #killing the bot
    elif message.content.startswith('p!kill'):
        await message.channel.send('*dies*')
        await client.close()
    #ping test
    elif message.content.startswith('p!ping'):
        await message.channel.send('pong')
    
    #STONKS
    elif message.content.startswith('p!stock'):
        string = message.content.split()
        if len(string) == 1:
            await message.channel.send('Command is `p!stock <ticker>`, please try again')
            pass
        ticker = string[1]
        data = si.get_quote_data(ticker)
        await message.channel.send(
        '**Symbol:** ' + data['symbol'] + 
        '\n**Company Name:** ' + data['shortName'] + 
        '\n**Last Price:** $' +str(round(data['regularMarketPrice'], 2)) + 
        '\n**Price Change:** $' + str(round(data['regularMarketChange'], 2)) + 
        '\n**Percent Change:** ' + str(round(data['regularMarketChangePercent'], 2)) + '%' + 
        '\n**Volume:** ' + '{:,}'.format(data['regularMarketVolume']) + 
        '\n**Open:** $' + str(round(data['regularMarketOpen'], 2)) + 
        '\n**Days Range:** ' + data['regularMarketDayRange'] + 
        '\n')

    #help command
    elif message.content.startswith('p!help'):
        await message.channel.send('**Here is a list of my Commands:**\n\n' +
        '**p!ping**\n' + '\tSends \'pong\' in response.\n' + 
        '**p!hello**\n' + '\tSays hello to the sender.\n' + 
        '**p!kill**\n' + '\tKills the bot in case of an error.\n' + 
        '**p!stock** *<symbol>*\n' + '\tReturns real time quote data for the symbol inputted.\n')

    #unknown command
    elif message.content.startswith('p!'):
        await message.add_reaction('❓')

#starting the server
bot_server.keep_running()

client.run(TOKEN)