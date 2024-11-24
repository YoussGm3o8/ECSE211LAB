import os
import numpy as np
import matplotlib.pyplot as plt


data_path = os.path.join(os.path.dirname(__file__), 'csv')
path = os.path.join(data_path, 'us_data3.csv')
data = np.genfromtxt(path, delimiter=',', skip_header=1)
dif = np.diff(data[:, 1])
print(data.shape)

#we will perform convolution using different kernels

def haar_kernel(buffer):
    w = buffer.shape[0] // 2
    kernel = np.ones((w,))
    kernel = np.concatenate((kernel, -kernel))
    return np.dot(buffer[:w*2], kernel)

def haar_kernel_v2(buffer):
    w = buffer.shape[0] // 3
    kernel = np.ones((w,))
    kernel /= w
    kernel = np.concatenate((-0.5*kernel, kernel, -0.5*kernel))
    return np.dot(buffer[:w*3], kernel)

class iter_mean:
    def __init__(self):
        self.mean = 0
        self.n = 0
    def update(self, x):
        self.n += 1
        self.mean = self.mean + (x - self.mean) / self.n
        return self.mean

class exp_mean:
    def __init__(self):
        self.mean = 0

    def reset(self, x):
        self.mean = x

    def update(self, x):
        self.mean = 0.95 * self.mean + 0.05 * x
        return self.mean

x = data[:, 0]
y = data[:, 1]
m = exp_mean()
m.reset(np.mean(y[-1]))
mean = [m.update(y[i]) for i in range(len(y))]
mean = np.array(mean)
def convolute(y, kernel, size):
    res = []
    for i in range(len(y)):
        res.append(kernel(y[i:i+size]))
    return np.array(res)
y_clip = np.where(y > mean, mean, y)
dif_clip = np.diff(y_clip)
w_size = 6
data_haar = convolute(y_clip, haar_kernel_v2, w_size)
data_haar_wide = convolute(y_clip, haar_kernel_v2, 24)
x_ajusted = np.roll(x, -w_size//3)
treshold =  np.mean(y) * -0.4 + 26
print(treshold)
if treshold < 0:
    treshold = 2
detected = np.where(data_haar < - 2.5, x_ajusted, 0)
for d in detected:
    if d == 0:
        continue
    plt.axvline(x=d, color='r', linestyle='--')
# plt.plot(x[1:], dif_clip, label='derivative')
plt.plot(x, y, label='Original')
plt.plot(x, data_haar, label='Haar')
plt.plot(x, data_haar_wide, label='Haar')
plt.plot(x, mean, label='Mean')
plt.show()


#8 points for 15 cm
#1-2 points for 50 cm


