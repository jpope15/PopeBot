import discord
import random
import os
import re
from yahoo_fin import stock_info as si

client = discord.Client()
<<<<<<< HEAD
TOKEN = 'ODE0NTQyMjY2MDk3MDc0MjI2.YDfXmQ.Xj31fyhmkZz-7hD1Qisn8JNbVfo' #move this to a .env file somehow
=======
>>>>>>> 42c69fa9a65f5c4de034cbac5b342ac17fba015b

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
        if data['error'] is not None:
            await message.channel.send('Error, symbol not found.\nUse `p!stock <symbol>` to get' + 
            'real time quote data.')
        else: 
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

    #unknown command
    elif message.content.startswith('p!'):
        await message.add_reaction('❓')

client.run(TOKEN)
