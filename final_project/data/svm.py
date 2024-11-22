from sklearn import svm
import numpy as np
from color_numpy import green, blue, red, yellow, orange, purple, white

colors = {'green': 0, 'blue': 1, 'red': 2, 'yellow': 3, 'orange': 4, 'purple': 5, 'white': 6}

y = np.full((green.shape[0],), colors['green'], dtype=int)
y = np.concatenate((y, np.full((blue.shape[0],), colors['blue'], dtype=int)), axis=0)
y = np.concatenate((y, np.full((red.shape[0],), colors['red'], dtype=int)), axis=0)
y = np.concatenate((y, np.full((yellow.shape[0],), colors['yellow'], dtype=int)), axis=0)
y = np.concatenate((y, np.full((orange.shape[0],), colors['orange'], dtype=int)), axis=0)
y = np.concatenate((y, np.full((purple.shape[0],), colors['purple'], dtype=int)), axis=0)
y = np.concatenate((y, np.full((white.shape[0],), colors['white'], dtype=int)), axis=0)

x = np.concatenate((green, blue, red, yellow, orange, purple, white), axis=0)
x_norm = x / np.repeat(np.sum(x, axis=1).reshape(-1, 1), 3, axis=1)
#replace nan with 0
x_norm = np.nan_to_num(x_norm)
print(x_norm)
print(x)
print(y)

clf = svm.SVC(decision_function_shape='ovr')
clf2 = svm.SVC(decision_function_shape='ovr')
clf.fit(x, y)
clf2.fit(x_norm, y)

orange_x = np.array(orange)
orange_x_norm = orange_x / np.repeat(np.sum(orange_x, axis=1).reshape(-1, 1), 3, axis=1)
orange_x_norm = np.nan_to_num(orange_x_norm)

orange_y = np.full((orange.shape[0],), colors['orange'], dtype=int)

print(f"Accuracy clf: {clf.score(x, y)}")
print(f"Accuracy clf2: {clf2.score(x_norm, y)}")
print(f"Accuracy orange: {clf.score(orange_x, orange_y)}")
print(f"Accuracy orange: {clf2.score(orange_x_norm, orange_y)}")
