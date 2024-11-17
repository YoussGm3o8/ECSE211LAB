import os
import matplotlib.pyplot as plt
import numpy as np
import csv
import common.filters as filters


path = os.path.join("data", "csv", "us_data.csv")
data = None
with open(path, "r") as file:
    reader = csv.reader(file)
    data = list(reader)
    data = data[1:]

filter = filters.Median_Filter(1000)
it = iter(data)
result = 0
history = []
while not filter.isReady():
    result = filter.update(float(next(it)[1]))

for i, v in enumerate(it):
    result = filter.update(float(v[1]))
    history.append((i,result))

x, y = zip(*history)
plt.plot(x,y)
plt.show()
