from sklearn import svm
import numpy as np

#change the root directory so that other script can import this
import os
#you will need to revert at the end
os_main = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
#open green.csv to numpy
green = np.genfromtxt('green.csv', delimiter=',', skip_header=1)
blue = np.genfromtxt('blue.csv', delimiter=',', skip_header=1)
red = np.genfromtxt('red.csv', delimiter=',', skip_header=1)
yellow = np.genfromtxt('yellow.csv', delimiter=',', skip_header=1)
orange = np.genfromtxt('orange.csv', delimiter=',', skip_header=1)
purple = np.genfromtxt('purple.csv', delimiter=',', skip_header=1)

colors = {'green': 0, 'blue': 1, 'red': 2, 'yellow': 3, 'orange': 4, 'purple': 5}

y = np.full((green.shape[0],), colors['green'], dtype=int)
y = np.concatenate((y, np.full((blue.shape[0],), colors['blue'], dtype=int)), axis=0)
y = np.concatenate((y, np.full((red.shape[0],), colors['red'], dtype=int)), axis=0)
y = np.concatenate((y, np.full((yellow.shape[0],), colors['yellow'], dtype=int)), axis=0)
y = np.concatenate((y, np.full((orange.shape[0],), colors['orange'], dtype=int)), axis=0)
y = np.concatenate((y, np.full((purple.shape[0],), colors['purple'], dtype=int)), axis=0)

x = np.concatenate((green, blue, red, yellow, orange, purple), axis=0)

print(x)
print(y)

clf = svm.SVC(decision_function_shape='ovo')
clf.fit(x, y)

#reset the root directory to the original
os.chdir(os_main)
