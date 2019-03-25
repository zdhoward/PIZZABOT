from discord.ext import commands
import asyncio
from datetime import date

from credentials import secret_key, client_id, token
from cl_scraper import cl_search


### CONFIG ###
prefix = "!"
bot = commands.Bot(command_prefix='!')

def Log(msg):
    print(str(date.today()) + ": " + msg)

def botMsg(msg):
    return ("```" + str(msg) + "```")

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command(pass_context=True)
async def ping(ctx):
    '''
    Returns the bot's latency
    '''
    latency = bot.latency
    await ctx.send(botMsg(str(round(latency * 1000, 3)) + "ms"))

@bot.command(name='echo', pass_context=True)
async def echo(ctx, *, content:str):
    '''
    Reply with the user's parameters
    '''
    await ctx.send(botMsg(content))

@bot.command(name="search", pass_context=True)
async def search(ctx, *, args:str):
    '''
    Search CraigsList and Format Results
    '''

    arguments = "-s Alpha -l VANCOUVER -p 200-300 -k synth dx7"

    arg = arguments.split(" ")

    for x in range(len(arguments))

    #Decipher args for options
    args = "DX7"

    header='**CraigsList Search**\nKeywords: {0}\nFilters: {1}\nSort: {2}'.format(args, "LowPrice", "NoFree")
    msg = cl_search(args.replace(" ", "+"), sort="LowPrice", filterFree=True)
    await ctx.send(botMsg(msg[:10]))

bot.run(token)
