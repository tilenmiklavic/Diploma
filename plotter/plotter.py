import matplotlib.pyplot as plt
import json
import numpy as np
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


    price_dates = []
    prices = []

    with open(PATH_PRICE + "/" + file2) as json_file:
        data = json.load(json_file)
        print(data)
        for p in data["prices"]:
            try:
                a = float(p["close"])
                prices.append(a)
                price_dates.append(np.datetime64(p["date"]))
            except ValueError:
                print("Erorr with prices")


    plt.plot(dates, tweets)
    plt.show()
    print("Plotting complete")

if __name__ == '__main__':
    tweetsFiles = listFiles(PATH_TWEETS)
    priceFiles = listFiles(PATH_PRICE)
    
    for file1, file2 in zip(tweetsFiles, priceFiles):
        plotGraph(file1, file2)