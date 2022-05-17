from os import listdir
from os.path import isfile, join
import json

NORMALIZED_PRICES_PATH = "../normalizer/normalized_prices/"
NORMALIZED_TWEETS_PATH = "../normalizer/normalized_tweets/"
OUTPUT_PATH = "correlation_data/"

correlation_data = { "similarity": []}


# function for returning the list of data in directory
def listFiles(dir):
    files = [f for f in listdir(dir) if isfile(join(dir, f))]

    jsons = [f for f in files if f[-4:] == "json"]
    print(len(jsons), " JSON files found.")
    print("JSON files in directory ", dir, " : ", jsons)

    return jsons


# write data to output file
def writeToFile(data, file):
    with open(OUTPUT_PATH + file, 'w') as outfile:
        json.dump(data, outfile)


# get coin symbol from file name
def getSymbol(file_name):
    return file_name.split('.')[0].split('-')[1]


# calculate similarity between two datasets
def similarity(file1, file2):
    
    difference = 0
    difference_count = 0
    
    with open(NORMALIZED_TWEETS_PATH + file1) as json_file_tweets:
        with open(NORMALIZED_PRICES_PATH + file2) as json_file_prices:
            prices = json.load(json_file_prices)["prices"]
            tweets = json.load(json_file_tweets)["tweets"]
            
            price_index = 0
            tweet_index = 0
            
            while price_index < len(prices) and tweet_index < len(tweets):
                if prices[price_index]["date"] == tweets[tweet_index]["date"]:
                    difference += abs(prices[price_index]["price"] - tweets[tweet_index]["tweet"])
                    difference_count += 1
                    price_index += 1
                    tweet_index += 1
                elif prices[price_index]["date"] < tweets[tweet_index]["date"]:
                    price_index += 1
                elif prices[price_index]["date"] > tweets[tweet_index]["date"]:
                    tweet_index += 1
            
            print(difference)
            print(difference_count)
            
            return difference / difference_count


if __name__ == '__main__':
    tweetsFiles = sorted(listFiles(NORMALIZED_TWEETS_PATH))
    priceFiles = sorted(listFiles(NORMALIZED_PRICES_PATH))
    
    for file1, file2 in zip(tweetsFiles, priceFiles):
        symbol = getSymbol(file1)
        correlation = similarity(file1, file2)
        
        correlation_data["similarity"].append({"symbol": symbol,
                                               "correlation": correlation})
        
    writeToFile(correlation_data, "correlation.json")
    