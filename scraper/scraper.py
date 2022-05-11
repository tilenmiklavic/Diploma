from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from os import listdir
from os.path import isfile, join
from datetime import datetime
import json

PATH_COINS = 'coins.json'
OUTPUT_PATH = 'results.json'
APPEND_PATH = '../tweets_data/json_files/'

# function for returning a list of all coins
def listFiles(file1):
    coins = []
    
    # open json file containing list of all crypto coins
    with open(file1) as json_file:
        data = json.load(json_file)
        for p in data["coins"]:
            try:
                coins.append(p)
            except ValueError:
                print("Error", p["name"])

    return coins


def writeResults(data, file1):
    with open(OUTPUT_PATH + file1, 'w') as outfile:
        json.dump(data, outfile)


def appendScrapedData(data, file):
    f = open(APPEND_PATH + file)
    old_json = json.load(f)

    first_scrape_of_day = True
    for element in old_json["tweets"]:
        if element["date"] == data["date"]:
            first_scrape_of_day = False

    if first_scrape_of_day:
        old_json["tweets"].append(data)

    with open(APPEND_PATH + file, 'w') as outfile:
        json.dump(old_json, outfile)



# function for web scraping
def scrape(coins):
    date = datetime.today().strftime('%Y/%m/%d')
    tweets_current = { 'tweets': [], 'date': date}
    results = []
    browser = webdriver.Chrome()

    for coin in coins:
        name = coin['name']
        symbol = coin['symbol']

        print(name)

        url = 'https://bitinfocharts.com/' + name + '/'
        browser.get(url)

        element = browser.find_element_by_xpath('//tr[td[a[contains(text(), "Tweets per day")]]]/td[2]/a')
        tweets = element.text
        print(tweets)
        results.append({"date": date, "name": name, "symbol": symbol, "tweet": tweets })


        appendScrapedData({"date": date, "tweet": tweets}, "tweets-"+symbol+".json")

    browser.close()
    tweets_current['tweets'] = results
    return tweets_current

if __name__ == '__main__':
    coins = listFiles(PATH_COINS)
    tweets = scrape(coins)
    writeResults(tweets, "")