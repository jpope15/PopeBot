import discord
import random
import os
import re
from yahoo_fin import stock_info as si

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
        data = si.get_quote_table(ticker, dict_result=True)
        curr_price = si.get_live_price(ticker)
        percent_change = 100 * (abs(curr_price - data['Previous Close']) / curr_price)
        if curr_price < data['Previous Close']:
            percent_change = percent_change * -1
        await message.channel.send(
            '**Ticker:** ' + ticker + 
            '\n**Last Price:** $' +str(round(curr_price, 2)) + 
            '\n**Open:** $' + str(round(data['Open'], 2)) + 
            '\n**Prev Close:** $' + str(round(data['Previous Close'], 2)) + 
            '\n**' + '%' + 'Change:** ' + str(round(percent_change, 2)) + '%' +
            '\n')

    #unknown command
    elif message.content.startswith('p!'):
        await message.add_reaction('❓')

client.run(TOKEN)
