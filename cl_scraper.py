import pandas as pd
import requests
import argparse
from datetime import datetime
from time import sleep
from bs4 import BeautifulSoup

sortFilters = {
    "LowPrice":         {"data": "Prices", "asc": True},
    "Alpha":            {"data": "Titles", "asc": True},
    "LocationAlpha":    {"data": "Locations", "asc": True},
    "Newest":           {"data": "Dates", "asc": False}
}

defaultSort = "LowPrice"

def cl_search(keywords, filterTypes=None, filterLocationData=None, filterPriceData=None, sort=defaultSort, filterFree=False, DEBUG=False):
    ### RETRIEVE RSS FILE FROM CRAIGSLIST SEARCH
    #url_base = 'http://vancouver.craigslist.org/search/sss?format=rss&query='
    url_base = "https://vancouver.craigslist.org/search/msa?query="
    url_search_base = "https://vancouver.craigslist.org"
    if keywords:
        searchTerms = keywords
    else:
        searchTerms = "synthesizer"

    titles = []
    locations = []
    dates = []
    prices = []
    descriptions = []
    urls = []
    urls.append(url_base + searchTerms)

    ### RECURSIVELY SCRAPE ALL PAGES
    while len(urls) > 0:
        #wait 1 second in between each new url request
        sleep(1)
        url = urls.pop(0)
        rsp = requests.get(url)
        soup = BeautifulSoup(rsp.text,"lxml")
        next_url = soup.find('a', class_= "button next")

        if next_url:
            if next_url['href']:
                urls.append(url_search_base + next_url['href'])

        #return all listings
        listings = soup.find_all('li', attrs={'class': 'result-row'})

        for listing in listings:
            titles.append(listing.find('a', {'class': ["result-title"]}).text.lstrip().rstrip())

            date = datetime.strptime(listing.find('time', {'class': ["result-date"]}).text.lstrip().rstrip(), '%b %d')
            dates.append(date)

            try:
                prices.append(int(listing.find('span', {'class': "result-price"}).text.lstrip().rstrip().strip("$")))
            except:
                prices.append(-1)

            try:
                locations.append(listing.find('span', {'class': "result-hood"}).text.lstrip().rstrip().strip("(").strip(")").upper())
            except:
                locations.append('zzz_missing')

    #write findings to a dataframa
    listings_df = pd.DataFrame({"Dates": dates, "Locations": locations, "Titles": titles, "Prices": prices})

    #filter results if necessary
    if filterFree:
        listings_df = listings_df[listings_df['Prices'] != 0]

    if filterTypes:
        if "Locations" in filterTypes:
            if filterLocationData:
                filter = listings_df["Locations"]==filterLocationData.upper()
                listings_df = listings_df[filter]

        if "Prices" in filterTypes:
            if filterPriceData:
                min = int(filterPriceData.split("-")[0])
                max = int(filterPriceData.split("-")[1])
                listings_df = listings_df[(listings_df["Prices"] >= min) & (listings_df["Prices"] <= max)]


    #sort listings
    sortFilter = sortFilters[sort]
    listings_df.sort_values(by=[sortFilter['data']], inplace=True, ascending=sortFilter['asc'])
    #listings_df.sort(sortFilter)

    ### DEBUG
    if DEBUG:
        print ("===========================================")
        print ("Keywords:           " + searchTerms.replace("+", ", "))
        print ("URL:                " + rsp.url)
        print ("Listings:           " + str(len(listings)))
        print ("FilterTypes:        " + filterTypes)
        if filterLocationData:
            print ("Filter Location:    " + filterLocationData)
        if filterPriceData:
            print ("Filter Price:       " + filterPriceData)
        print ("Sort By:            " + sort)
        print ("===========================================")
        #print (html.prettify())
        #print (listings[0].prettify())
        #print (listings_df)
        print (listings_df)
        print ("===========================================")

    return listings_df

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-k','--keys', '--keywords', nargs='+', help='Add keywords to a search', dest='keys', required=True)
    parser.add_argument('-s','--sort', help='Name of the sort filter', dest='sort', required=False)
    parser.add_argument('-v', '-d','--verbose', '--debug', action='store_true', dest='debug', required=False)
    parser.add_argument('-l', '--location', help='Filter for a particular location', dest='filterLocationData', required=False)
    parser.add_argument('-p', '--price', help='Filter for a particular price', dest='filterPriceData', required=False)
    parser.add_argument('-f', '--free', '--not-free', help='Filter out free things', action='store_true', dest='filterFree', required=False)
    args = parser.parse_args()
    allKeys = ""
    filterTypes = ""
    filterLocationData = None
    filterPriceData = None

    for key in args.keys:
        allKeys += key + "+"

    if args.debug:
        debug = args.debug
    else:
        debug = False

    if args.sort:
        try :
            if sortFilters[args.sort]:
                sort = args.sort
        except:
            sort = defaultSort
    else:
        sort = defaultSort

    if args.filterLocationData:
        filterTypes += "Locations , "
        filterLocationData = args.filterLocationData

    if args.filterPriceData:
        filterTypes += "Prices , "
        filterPriceData = args.filterPriceData

    filterFree = args.filterFree

    #print(allKeys)
    cl_search(allKeys,filterTypes=filterTypes, filterLocationData=filterLocationData, filterPriceData=filterPriceData, sort=sort, filterFree=filterFree, DEBUG=debug)
