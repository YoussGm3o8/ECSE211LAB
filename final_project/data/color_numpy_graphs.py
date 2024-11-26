import os
import numpy as np
import matplotlib.pyplot as plt

path = os.path.join(os.path.dirname(__file__), "csv", "color")
path = os.path.join(path, "sensor2")
print(path)
green = np.genfromtxt(os.path.join(path, "green.csv"), delimiter=',', skip_header=1)
blue = np.genfromtxt(os.path.join(path, "blue.csv"), delimiter=',', skip_header=1)
red = np.genfromtxt(os.path.join(path, "red.csv"), delimiter=',', skip_header=1)
yellow = np.genfromtxt(os.path.join(path, "yellow.csv"), delimiter=',', skip_header=1)
orange = np.genfromtxt(os.path.join(path, "orange.csv"), delimiter=',', skip_header=1)
purple = np.genfromtxt(os.path.join(path, "purple.csv"), delimiter=',', skip_header=1)

full_data = np.concatenate((green, blue, red, yellow, orange, purple))
#get the covariance matrix
cov = np.cov(full_data.T)
print(cov)


#plot 2d version of data

plt.scatter(green[:,0], green[:,2], c='g', marker='o', label='green')
plt.scatter(blue[:,0], blue[:,2], c='b', marker='o', label='blue')
plt.scatter(red[:,0], red[:,2], c='r', marker='o', label='red')
plt.scatter(yellow[:,0], yellow[:,2], c='y', marker='o', label='yellow')
plt.scatter(orange[:,0], orange[:,2], c='orange', marker='o', label='orange')
plt.scatter(purple[:,0], purple[:,2], c='purple', marker='o', label='purple')
plt.title("x vs z")
plt.show()

#plot 0 and 2 now
plt.scatter(green[:,1], green[:,2], c='g', marker='o', label='green')
plt.scatter(blue[:,1], blue[:,2], c='b', marker='o', label='blue')
plt.scatter(red[:,1], red[:,2], c='r', marker='o', label='red')
plt.scatter(yellow[:,1], yellow[:,2], c='y', marker='o', label='yellow')
plt.scatter(orange[:,1], orange[:,2], c='orange', marker='o', label='orange')
plt.scatter(purple[:,1], purple[:,2], c='purple', marker='o', label='purple')
plt.title("y vs z")
plt.show()

#plot 3d graph
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(green[:,0], green[:,1], green[:,2], c='g', marker='o', label='green')
ax.scatter(blue[:,0], blue[:,1], blue[:,2], c='b', marker='o', label='blue')
ax.scatter(red[:,0], red[:,1], red[:,2], c='r', marker='o', label='red')
ax.scatter(yellow[:,0], yellow[:,1], yellow[:,2], c='y', marker='o', label='yellow')
ax.scatter(orange[:,0], orange[:,1], orange[:,2], c='orange', marker='o', label='orange')
ax.scatter(purple[:,0], purple[:,1], purple[:,2], c='purple', marker='o', label='purple')

#plot the plane z = -0.2x -0.5y + 20

x = np.linspace(-100, 100, 100)
y = np.linspace(-100, 100, 100)
X, Y = np.meshgrid(x, y)
Z = -0.2*X - 0.5*Y + 20
ax.plot_surface(X, Y, Z, alpha=0.5)

#display the vectors of the cov matrix
origin = [0,0,0]
plt.plot([origin[0], cov[0,0]], [origin[1], cov[0,1]], [origin[2], cov[0,2]], color='r')
plt.plot([origin[0], cov[1,0]], [origin[1], cov[1,1]], [origin[2], cov[1,2]], color='g')
plt.plot([origin[0], cov[2,0]], [origin[1], cov[2,1]], [origin[2], cov[2,2]], color='b')

plt.show()

path = os.path.join(os.path.dirname(__file__), "csv", "color")
print(path)
green = np.genfromtxt(os.path.join(path, "green.csv"), delimiter=',', skip_header=1)
blue = np.genfromtxt(os.path.join(path, "blue.csv"), delimiter=',', skip_header=1)
red = np.genfromtxt(os.path.join(path, "red.csv"), delimiter=',', skip_header=1)
yellow = np.genfromtxt(os.path.join(path, "yellow.csv"), delimiter=',', skip_header=1)
orange = np.genfromtxt(os.path.join(path, "orange.csv"), delimiter=',', skip_header=1)
purple = np.genfromtxt(os.path.join(path, "purple.csv"), delimiter=',', skip_header=1)

#plot 2d version of data

plt.scatter(green[:,0], green[:,2], c='g', marker='o', label='green')
plt.scatter(blue[:,0], blue[:,2], c='b', marker='o', label='blue')
plt.scatter(red[:,0], red[:,2], c='r', marker='o', label='red')
plt.scatter(yellow[:,0], yellow[:,2], c='y', marker='o', label='yellow')
plt.scatter(orange[:,0], orange[:,2], c='orange', marker='o', label='orange')
plt.scatter(purple[:,0], purple[:,2], c='purple', marker='o', label='purple')
plt.title("x vs z")
plt.show()

#plot 0 and 2 now
plt.scatter(green[:,1], green[:,2], c='g', marker='o', label='green')
plt.scatter(blue[:,1], blue[:,2], c='b', marker='o', label='blue')
plt.scatter(red[:,1], red[:,2], c='r', marker='o', label='red')
plt.scatter(yellow[:,1], yellow[:,2], c='y', marker='o', label='yellow')
plt.scatter(orange[:,1], orange[:,2], c='orange', marker='o', label='orange')
plt.scatter(purple[:,1], purple[:,2], c='purple', marker='o', label='purple')
plt.title("y vs z")
plt.show()

#plot 3d graph
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(green[:,0], green[:,1], green[:,2], c='g', marker='o', label='green')
ax.scatter(blue[:,0], blue[:,1], blue[:,2], c='b', marker='o', label='blue')
ax.scatter(red[:,0], red[:,1], red[:,2], c='r', marker='o', label='red')
ax.scatter(yellow[:,0], yellow[:,1], yellow[:,2], c='y', marker='o', label='yellow')
ax.scatter(orange[:,0], orange[:,1], orange[:,2], c='orange', marker='o', label='orange')
ax.scatter(purple[:,0], purple[:,1], purple[:,2], c='purple', marker='o', label='purple')

#plot the plane z = -0.2x -0.4y + 20

x = np.linspace(-100, 100, 100)
y = np.linspace(-100, 100, 100)
X, Y = np.meshgrid(x, y)
Z = -0.2*X - 0.5*Y + 20
ax.plot_surface(X, Y, Z, alpha=0.5)
plt.show()
