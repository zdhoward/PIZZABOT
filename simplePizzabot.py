import discord
import asyncio
import argparse
from datetime import date

from credentials import secret_key, client_id, token
from cl_scraper import cl_search

client = discord.Client()

parser = argparse.ArgumentParser()
parser.add_argument('-k','--keys', '--keywords', nargs='+', help='Add keywords to a search', dest='keys', required=True)
parser.add_argument('-s','--sort', help='Name of the sort filter', dest='sort', required=False)
parser.add_argument('-v', '-d','--verbose', '--debug', action='store_true', dest='debug', required=False)
parser.add_argument('-l', '--location', help='Filter for a particular location', dest='filterLocationData', required=False)
parser.add_argument('-p', '--price', help='Filter for a particular price', dest='filterPriceData', required=False)
parser.add_argument('-f', '--free', '--not-free', help='Filter out free things', action='store_true', dest='filterFree', required=False)

def Log(msg):
    print(str(date.today()) + ": " + msg)

@client.event
async def on_message(message):
    global parser
    #Do not reply to self
    if message.author == client.user:
        return

    ## HELLO COMMAND
    if message.content.startswith("!hello") and message.channel.name == "craigslist":
        Log("{0.author.mention}: !hello".format(message))
        await message.channel.send('Hello!')

    ## BASIC CRAIGSLIST SEARCH
    if message.content.startswith("!cl_search") and message.channel.name == "craigslist":

        arguments = message.content.lstrip('!cl_search').lstrip().rstrip()

        '''
        allKeys = ""
        filterFree = False
        filterTypes = ""
        filterLocationData = ""
        filterPriceData = ""
        sort = "LowPrice"

        try:
            args = parser.parse_args([arguments])
        except:
            print ("FAILED PARSING")
            args.keys = "synthesizer"
            args.filterFree = False

        for key in args.keys:
            allKeys += key + "+"

        if args.sort:
            sort = args.sort

        if args.filterLocationData:
            filterTypes += "Locations , "
            filterLocationData = args.filterLocationData

        if args.filterPriceData:
            filterTypes += "Prices , "
            filterPriceData = args.filterPriceData

        filterFree = args.filterFree
        '''

        Log("{0.author.mention}: !cl_search {1}".format(message, arguments))

        header='**CraigsList Search**\nKeywords: {0}\nFilters: {1}\nSort: {2}'.format(arguments, "LowPrice", "NoFree")

        msg = cl_search(arguments, sort="LowPrice", filterFree=True)

        #cl_search(allKeys, filterTypes=filterTypes, filterLocationData=filterLocationData, filterPriceData=filterPriceData, sort=sort, filterFree=filterFree)
        await message.channel.send(header + '```' + str(msg[:10]) + '```')

    ### SIMPLE SEARCH
    if message.content.startswith("!search") and message.channel.name == "craigslist":

        arguments = message.content.lstrip('!search').lstrip().rstrip()

        Log("{0.author.mention}: !cl_search {1}".format(message, arguments))

        header='**CraigsList Search**\nKeywords: {0}\nFilters: {1}\nSort: {2}'.format(arguments, "LowPrice", "NoFree")

        msg = cl_search(arguments.replace(" ", "+"), sort="LowPrice", filterFree=True)

        await message.channel.send(header + '```' + str(msg[:10]) + '```')

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(token)
