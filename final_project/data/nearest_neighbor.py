#import linear regression from sklearn
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt
from color_numpy import green, blue, red, yellow, orange, purple


def create_ray(color, length=1):

    #perform linear regression on only 2 features
    X = color[:, 0].reshape(-1, 1)
    y = color[:, 1]
    z = color[:, 2]
    #fit the model
    model = LinearRegression().fit(X, y)
    model2 = LinearRegression().fit(X, z)
    #predict a range of values from 0 to 255
    X_new = np.linspace(0, length, 100)
    y_new = model.predict(X_new[:, np.newaxis])
    z_new = model2.predict(X_new[:, np.newaxis])
    #plot the data
    return X_new, y_new, z_new




fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
if True:
    #scatter with opacity 0.90
    ax.scatter(green[:,0], green[:,1], green[:,2], c='g', marker='o', label='green', alpha=0.9)
    ax.scatter(blue[:,0], blue[:,1], blue[:,2], c='b', marker='o', label='blue', alpha=0.9)
    ax.scatter(red[:,0], red[:,1], red[:,2], c='r', marker='o', label='red', alpha=0.9)
    ax.scatter(yellow[:,0], yellow[:,1], yellow[:,2], c='y', marker='o', label='yellow', alpha=0.9)
    ax.scatter(orange[:,0], orange[:,1], orange[:,2], c='orange', marker='o', label='orange', alpha=0.9)
    ax.scatter(purple[:,0], purple[:,1], purple[:,2], c='purple', marker='o', label='purple', alpha=0.9)

# g_x, g_y, g_z = create_ray(green)
# ax.plot(g_x, g_y, g_z, c='black')
# b_x, b_y, b_z = create_ray(blue)
# ax.plot(b_x, b_y, b_z, c='black')
# r_x, r_y, r_z = create_ray(red)
# ax.plot(r_x, r_y, r_z, c='black')
# y_x, y_y, y_z = create_ray(yellow)
# ax.plot(y_x, y_y, y_z, c='black')
# o_x, o_y, o_z = create_ray(orange)
# ax.plot(o_x, o_y, o_z, c='black')
# p_x, p_y, p_z = create_ray(purple)
# ax.plot(p_x, p_y, p_z, c='black')

#plot a ray using x_new, y_new, and z_new plt.show()
plt.show()
