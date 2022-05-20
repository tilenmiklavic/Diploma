from datetime import datetime, timedelta
from genericpath import isfile
import json
from ntpath import join
from os import listdir
import matplotlib.pyplot as plt
from numpy import sort
from scipy import stats

TWEETS_DATASET = "../tweets_data/json_files/"
PRICES_DATASET = "../price_data/json_files/"
OUTPUT_PATH = "predicted_prices/"


# write data to output file
def writeToFile(data, file):
    with open(OUTPUT_PATH + file, 'w') as outfile:
        json.dump(data, outfile)
        

def isDayYesterday(dayBefore, today):
    date1 = datetime.strptime(dayBefore, '%Y/%m/%d')
    date2 = datetime.strptime(today, '%Y/%m/%d')
    date3 = date2 - timedelta(days=1)
    
    return date3 == date1


def isDayBefore(date1, date2):
    date1 = datetime.strptime(date1, '%Y/%m/%d')
    date2 = datetime.strptime(date2, '%Y/%m/%d')
    
    return date1 < date2


# function for returning the list of data in directory
def listFiles(dir):
    files = [f for f in listdir(dir) if isfile(join(dir, f))]

    jsons = [f for f in files if f[-4:] == "json"]
    print(len(jsons), " JSON files found.")
    print("JSON files in directory ", dir, " : ", jsons)

    return jsons


# clean daatset and convert it to array for processing
def prepareDataset(dataset1, dataset2):
    with open(TWEETS_DATASET + dataset1) as json_file_tweets:
        with open(PRICES_DATASET + dataset2) as json_file_prices:
            
            tweets_cleaned_dataset = []
            prices_cleaned_dataset = []
            tweet_index = 0
            price_index = 0
            
            prices = json.load(json_file_prices)["prices"]
            tweets = json.load(json_file_tweets)["tweets"]
                        
            while price_index < len(prices) and tweet_index < len(tweets):
                try:
                    float(tweets[tweet_index]["tweet"])
                except:
                    tweet_index += 1
                    continue
                    
                try:
                    float(prices[price_index]["price"])
                except:
                    price_index += 1
                    continue
                    
                if isDayYesterday(tweets[tweet_index]["date"], prices[price_index]["date"]):
                    tweets_cleaned_dataset.append(float(tweets[tweet_index]["tweet"]))
                    prices_cleaned_dataset.append(float(prices[price_index]["price"]))
                    
                    tweet_index += 1
                    price_index += 1
                
                elif isDayBefore(tweets[tweet_index]["date"], prices[price_index]["date"]):
                    tweet_index += 1
                    
                else:
                    price_index += 1
                    
            return makePrediction(tweets_cleaned_dataset, prices_cleaned_dataset, tweets)
            

# make prediction based on today's tweets
def makePrediction(x, y, tweet_dataset):
    slope, intercept, r, p, std_err = stats.linregress(x, y)

    return slope * int(tweet_dataset.pop()["tweet"].replace('.','').replace(',','')) + intercept


if __name__ == '__main__':    
    tweet_files = sort(listFiles(TWEETS_DATASET))
    price_files = sort(listFiles(PRICES_DATASET))
    
    output_data = {
        "predictions": [],
        "date": datetime.today().strftime('%Y/%m/%d')
    }
    
    for file1, file2 in zip(tweet_files, price_files):
        prediction = prepareDataset(file1, file2)    
        
        output_data["predictions"].append({
            "symbol": file1.split('.')[0].split('-')[1],
            "date": datetime.today().strftime('%Y/%m/%d'),
            "prediction": prediction
        })
        
    writeToFile(output_data, "predictions.json")