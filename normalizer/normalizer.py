import matplotlib.pyplot as plt
import json
import numpy as np
import datetime
from os import listdir
from os.path import isfile, join

PATH = "example_btc_price"
OUTPUT_PATH = "normalized_prices"

# function for returning the list of data in directory
def listFiles(dir):
    files = [f for f in listdir(dir) if isfile(join(dir, f))]

    jsons = [f for f in files if f[-4:] == "json"]
    print(len(jsons), " JSON files found.")
    print("JSON files in directory ", dir, " : ", jsons)

    return jsons


# function for plotting a graph from JSON data
def normalize(file1):
    with open(PATH + "/" + file1) as json_file:
        data = json.load(json_file)
        new_data = []
        key = ''
        sub_key = ''
        max_value = float('-inf')
        min_value = float('inf')
        previous = None
        normalized_list = []
        normalized_data = {}

        # determine array key
        for title in data.keys():
            key = title
            normalized_data[key] = []

        # loop through the array
        for p in data[key]:
            try:

                # we have to get the key over which we normalize in the first loop iteration
                if not sub_key:
                    print('Normalize which column: ')
                    for kljuc in p.keys():
                        print(kljuc)
                    sub_key = input('Answear: ')

                # if we encounter a missing value we fill it with the last known one
                if p[sub_key] == 'null':
                    curr = previous
                else:
                    curr = float(p[sub_key])

                # determine max value and min value
                min_value = min(curr, min_value)
                max_value = max(curr, max_value)
                min_value = curr if curr < min_value else min_value
                max_value = curr if curr > max_value else max_value

                previous = curr

            except ValueError:
                print("Not int")

        print("Max value: ", max_value)
        print("Min value: ", min_value)

        # actual normalization
        for p in data[key]:
            try:
                # if we encounter a missing value we fill it with the last known one
                if p[sub_key] == 'null':
                    curr = previous
                else:
                    curr = float(p[sub_key])

                normalized_value = ((curr - min_value) / (max_value - min_value))
                normalized_list.append(normalized_value)

            except ValueError:
                print("Not int")

        for p, value in zip(data[key], normalized_list):
            try:
                normalized_data[key].append({
                    'date': p['date'],
                    key: value
                })

            except ValueError:
                print("Not int")

        with open(OUTPUT_PATH + "/" + file1 + "_normalized.json", 'w') as outfile:
            json.dump(normalized_data, outfile)


if __name__ == '__main__':
    tweetsFiles = listFiles(PATH)

    normalize(tweetsFiles[0])
