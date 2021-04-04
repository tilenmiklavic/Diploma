import matplotlib.pyplot as plt
import json
import numpy as np
from os import listdir
from os.path import isfile, join 

PATH = "." 


# function for returning the list of data in directory
def listFiles(dir): 
    files = [f for f in listdir(dir) if isfile(join(dir, f))]

    jsons = [f for f in files if f[-4:] == "json"]
    print(len(jsons), " JSON files found.")
    print("JSON files in directory ", PATH, " : ", jsons)

    return jsons


# function for plotting a graph from JSON data
def plotGraph(file): 

    dates = []
    tweets = []

    with open(file) as json_file:
        data = json.load(json_file)
        for p in data["tweets"]:
            try:
                a = int(p["tweet"])
                tweets.append(a)
                dates.append(np.datetime64(p["date"]))
            except ValueError:
                print("Not int")



    plt.plot(dates, tweets)
    plt.show()
    print("Plotting complete")

if __name__ == '__main__':
    jsonFiles = listFiles(PATH)
    
    for file in jsonFiles:
        plotGraph(file)