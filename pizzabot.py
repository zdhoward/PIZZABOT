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
    return ("```css\n" + str(msg) + "```")

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
async def search(ctx, *, args:str = None):
    '''
    Search CraigsList
    '''
    if args:
        # PARSE ARGUMENTS
        #arguments = "synth dx7 -f -s Alpha -l VANCOUVER -p 200-300"
        arg = args.split(" ")
        sortType = "LowPrice"
        filterLocation = ""
        filterPrice = ""
        filterFree = False
        while (("-s" in arg) or ("-l" in arg) or ("-f" in arg) or ("-p" in arg)):
            for x in range(len(arg)):
                checked = False
                ## SORT
                try:
                    if (('-s' in arg[x]) and (not checked)):
                        sortType = arg.pop(x+1)
                        arg.pop(x)
                        checked = True
                except:
                    pass

                ## FILTER LOCATION
                try:
                    if (('-l' in arg[x]) and (not checked)):
                        filterLocation = arg.pop(x+1)
                        arg.pop(x)
                        checked = True
                except:
                    pass

                ## FILTER PRICE
                try:
                    if (('-p' in arg[x]) and (not checked)):
                        filterPrice = arg.pop(x+1)
                        arg.pop(x)
                        checked = True
                except:
                    pass

                ## FILTER FREE
                try:
                    if (('-f' in arg[x]) and (not checked)):
                        filterFree = True
                        arg.pop(x)
                        checked = True
                except:
                    pass


        ## Log the search
        logging = "-------------------------------------\n"
        logging += str(arg) + '\n'
        logging += "-------------------------------------\n"
        logging += "Sort: " + sortType + '\n'
        logging += "FilterLocation: " + filterLocation + '\n'
        logging += "FilterPrice: " + filterPrice + '\n'
        logging += "FilterFree: " + str(filterFree) + '\n'
        logging += "Keywords: " + str(arg) + '\n'
        Log(logging)

        header='**CraigsList Search**\nKeywords: {0}\nFilters: {1}\nSort: {2}'.format(str(arg), sortType, "NoFree")
        msg = cl_search(str(arg).replace(" ", "+"), sort=sortType, filterFree=True, filterLocationData=filterLocation, filterPriceData=filterPrice)
        await ctx.send(botMsg(msg[:10]))
    else:
        help = "====================\nCraigsList Search Help\n====================\n"
        help += "  SORT TYPE\n"
        help += "    -s LowPrice | Newest | Alpha\n"
        help += "  LOCATION FILTER\n"
        help += "    -l vancouver | langley | kitsilano\n"
        help += "  PRICE FILTER\n"
        help += "    -p min-max | 0-200 | 100-800\n"
        help += "  FILTER OUT FREE LISTINGS\n"
        help += "    -f\n"
        help += "===================="
        await ctx.send(botMsg(help))

@bot.event
async def on_command_error(error, ctx):
    # you can compare error here
    print("Error: " + str(error))

bot.run(token)
