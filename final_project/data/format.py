#reformat the file csv/latest_scan.csv
#right now it is only a row of values
#make each value its own row

import csv
import os

path = os.path.dirname(__file__)
path = os.path.join(path, "csv", "latest_scan.csv")

with open(path, 'r') as file:
    reader = csv.reader(file)
    data = list(reader)

#we have a list of a list of strings
#we need a list of tuples : [(x, y), (x, y), ...]
#to do so we need to convert each string to a tuple ex: '(1,2)' -> (1, 2)

data = data[0]

for i in range(len(data)):
    data[i] = data[i].replace('(', '').replace(')', '')
    data[i] = tuple(map(float, data[i].split(',')))
#write data to a csv file called 'csv/last_scan.csv'

path = os.path.join(os.path.dirname(__file__), "csv", "last_scan.csv")
with open(path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["x", "y"])
    writer.writerows(data)
