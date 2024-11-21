import numpy as np
import os
import matplotlib.pyplot as plt

# Load your data (replace with correct path if needed)
path = os.path.dirname(__file__)
path = os.path.join(path, "csv", "us_data3.csv")
data = np.genfromtxt(path, delimiter=",", skip_header=1)


class diff:
    def __init__(self, treshold, width):
        self.treshold = treshold
        self.up = []
        self.down = []
        self.values = []
        self.width = width

    def update(self, x, y):
        if len(self.values) == 0:
            self.values.append(y)
            return False
        diff = y - self.values[-1]
        self.values.append(y)

        if diff > self.treshold:
            self.up.append((x,y))
            return self.is_signal()
        elif diff < -self.treshold:
            self.down.append((x,y))
        return False

    def is_signal(self):
        if len(self.up) > 0 and len(self.down) > 0:
            if abs(self.down[-1][0] - self.up[-1][0]) < self.width:
                return True
        return False



#test filter on data
d = diff(5, 50)
signals = [d.update(s[0], s[1]) for s in data]



#plot data

plt.plot(data[:,0], data[:,1])

for i, s in enumerate(signals):
    if s:
        plt.axvline(x=data[i][0], color='r', linestyle='--')
#plot ups and downs

ups = np.array(d.up)
downs = np.array(d.down)
plt.scatter(ups[:,0], ups[:,1], color='g')
plt.scatter(downs[:,0], downs[:,1], color='b')
plt.show()


