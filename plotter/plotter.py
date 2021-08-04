import matplotlib.pyplot as plt
import json
import numpy as np
import datetime
from os import listdir
from os.path import isfile, join 

PATH_TWEETS = "normalized_tweets/"
PATH_PRICE = "normalized_prices/"


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
    

    with open(PATH_TWEETS + file1) as json_file:
        data = json.load(json_file)
        for p in data["tweets"]:
            try:
                a = float(p["tweet"])
                tweets.append(a)
                dates.append(np.datetime64(p["date"]))
            except ValueError:
                print("Not int", p["tweet"])


    """
        plotting prices data
    """
    price_dates = []
    prices = []

    with open(PATH_PRICE + file2) as json_file:
        data = json.load(json_file)
        for p in data["prices"]:
            try:
                a = float(p["price"])
                prices.append(a)
                price_dates.append(np.datetime64(p["date"]))
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

    leg = plt.legend()
    for line in leg.get_lines():
        line.set_linewidth(1)

    # fig.tight_layout()
    # plt.show()
    plt.savefig(file1 + '_' + file2 + '.png', dpi=600)
    print("Plotting complete")

if __name__ == '__main__':
    tweetsFiles = sorted(listFiles(PATH_TWEETS))
    priceFiles = sorted(listFiles(PATH_PRICE))

    print(tweetsFiles)
    print(priceFiles)
    
    for file1, file2 in zip(tweetsFiles, priceFiles):
        plotGraph(file1, file2)