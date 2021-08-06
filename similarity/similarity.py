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
def similarity(file1, file2):

    tweets = []
    prices = []
    similarity = 0
    iterations = 0

    # get both datasets into variables
    with open(PATH_TWEETS + file1) as json_file:
        data = json.load(json_file)
        for p in data["tweets"]:
            try:
                tweets.append(p)
            except ValueError:
                print("Not int", p["tweet"])

    with open(PATH_PRICE + file2) as json_file:
        data = json.load(json_file)
        for p in data["prices"]:
            try:
                prices.append(p)
            except ValueError:
                print("Not int", p["price"])

    tweets_iterator = 0
    price_iterator = 0

    # go into a loop until we reach the end of dataset
    while True:

        # exit the loop when the end of array is reached
        if tweets_iterator > len(tweets) or price_iterator > len(prices):
            break

        tweets_date = np.datetime64(tweets[tweets_iterator]['date'])
        prices_date = np.datetime64(prices[price_iterator]['date'])

        if tweets_date == prices_date:
            similarity += abs(tweets[tweets_iterator]['tweet'] + prices[price_iterator]['price'])
            iterations += 1
            break

        # if dates are not aligned we iterate over dataset until we align them
        tweets_iterator += 1 if tweets_date < prices_date else 0
        price_iterator += 1 if prices_date < tweets_date else 0

    print(file1)
    print('Similarity:', similarity)
    print('Iterations:', iterations)
    print('Relative difference:', similarity / iterations)
    print('\n')


if __name__ == '__main__':
    tweetsFiles = sorted(listFiles(PATH_TWEETS))
    priceFiles = sorted(listFiles(PATH_PRICE))

    print(tweetsFiles)
    print(priceFiles)

    for file1, file2 in zip(tweetsFiles, priceFiles):
        similarity(file1, file2)