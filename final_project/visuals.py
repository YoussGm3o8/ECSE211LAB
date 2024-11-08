import matplotlib.pyplot as plt
from array import array
import pandas as pd

x_buffer= array('i', [0]*10)
y_buffer= array('i', [0]*10)

x = list(range(100))
y = x
z = y 
print(len(x), len(y), len(z))
df = pd.DataFrame({'x': x, 'y': y, 'z': z})
# for i in range(100):
#     #draw the plot one element at a time
#     x_buffer[i % 10] = x[i]
#     y_buffer[i % 10] = y[i]
#     plt.xlim(0, 100)
#     plt.ylim(0, 100)
#     plt.scatter(x_buffer, y_buffer)
#     plt.pause(0.01)
#     plt.draw()
#     plt.clf()

fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(projection='3d')

ax.scatter(df['x'], df['y'], df['z'])
plt.show()