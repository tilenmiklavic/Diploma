import matplotlib.pyplot as plt
import json
import numpy as np
import datetime
from os import listdir
from os.path import isfile, join 

PATH_TWEETS = "example_btc_tweets"
PATH_PRICE = "example_btc_price" 


# function for returning the list of data in directory
def listFiles(dir): 
    files = [f for f in listdir(dir) if isfile(join(dir, f))]

    jsons = [f for f in files if f[-4:] == "json"]
    print(len(jsons), " JSON files found.")
    print("JSON files in directory ", dir, " : ", jsons)

    return jsons



# function for plotting a graph from JSON data
def plotGraph(file1, file2): 
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    """
        plotting tweets data
    """
    dates = []
    tweets = []
    

    with open(PATH_TWEETS + "/" + file1) as json_file:
        data = json.load(json_file)
        for p in data["tweets"]:
            try:
                a = int(p["tweet"])
                tweets.append(a)
                dates.append(np.datetime64(p["date"]))
            except ValueError:
                print("Not int")


    """
        plotting prices data
    """
    price_dates = []
    prices = []

    with open(PATH_PRICE + "/" + file2) as json_file:
        data = json.load(json_file)
        for p in data["prices"]:
            try:
                a = float(p["close"])
                prices.append(a)
                price_dates.append(np.datetime64(datetime.datetime.strptime(p["date"], '%d-%m-%Y')))
            except ValueError:
                print("Erorr with prices")


    print("dates: {0} tweets: {1}".format(len(dates), len(tweets)))
    print("dates: {0} prices: {1}".format(len(price_dates), len(prices)))


    ax1.plot(dates, tweets, label="Tweets over time", color='green')
    ax1.tick_params(axis='y', labelcolor='green')
    ax2.plot(price_dates, prices, label="Price over time", color='blue')
    ax2.tick_params(axis='y', labelcolor='blue')

    ax1.set_xlabel('Time')
    ax1.set_ylabel('Tweets', color='green')
    ax2.set_ylabel('Price', color='blue')

    fig.tight_layout()
    plt.show()
    print("Plotting complete")

if __name__ == '__main__':
    tweetsFiles = listFiles(PATH_TWEETS)
    priceFiles = listFiles(PATH_PRICE)
    
    for file1, file2 in zip(tweetsFiles, priceFiles):
        plotGraph(file1, file2)