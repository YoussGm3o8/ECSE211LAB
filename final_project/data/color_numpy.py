import numpy as np
import matplotlib.pyplot as plt

#open green.csv to numpy

green = np.genfromtxt('green.csv', delimiter=',', skip_header=1)
blue = np.genfromtxt('blue.csv', delimiter=',', skip_header=1)
red = np.genfromtxt('red.csv', delimiter=',', skip_header=1)
yellow = np.genfromtxt('yellow.csv', delimiter=',', skip_header=1)
orange = np.genfromtxt('orange.csv', delimiter=',', skip_header=1)
purple = np.genfromtxt('purple.csv', delimiter=',', skip_header=1)
print(purple.shape)
#scatter plot 3d
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(green[:,0], green[:,1], green[:,2], c='g', marker='o', label='green')
ax.scatter(blue[:,0], blue[:,1], blue[:,2], c='b', marker='o', label='blue')
ax.scatter(red[:,0], red[:,1], red[:,2], c='r', marker='o', label='red')
ax.scatter(yellow[:,0], yellow[:,1], yellow[:,2], c='y', marker='o', label='yellow')
ax.scatter(orange[:,0], orange[:,1], orange[:,2], c='orange', marker='o', label='orange')
ax.scatter(purple[:,0], purple[:,1], purple[:,2], c='purple', marker='o', label='purple')
plt.show()
