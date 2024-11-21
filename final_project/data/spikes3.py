
import numpy as np
import statistics as stat
import os
import matplotlib.pyplot as plt
from collections import deque

# Load your data (replace with correct path if needed)
path = os.path.dirname(__file__)
path = os.path.join(path, "csv", "us_data3.csv")
data = np.genfromtxt(path, delimiter=",", skip_header=1)

# Filter class
class Filter:
    def __init__(self, func, buffer_length):
        self.buffer = deque(maxlen=buffer_length)
        self.func = func

    def update(self, value):
        """
        Update the buffer with the new value and returns the [func] of the buffer if full.
        NOTE: if the buffer is not full, the [func] is calculated based on the available values.
        """
        self.buffer.append(value)
        return self.func(self.buffer)

    def extend(self, values):
        self.buffer.extend(values)
        return self.func(self.buffer)

    def isReady(self):
        return len(self.buffer) == self.buffer.maxlen

    def __len__(self):
        return len(self.buffer)


class Median_Filter(Filter):
    def __init__(self, buffer_length):
        super().__init__(lambda x: stat.median(x), buffer_length)


# Apply median filter to the data (assuming data[:, 1] is the signal)
median_filter = Median_Filter(buffer_length=5)  # You can change the buffer size
filtered_data = [median_filter.update(y) for y in data[:, 1]]

# Calculate the difference between the original and filtered data (this highlights the outliers)
outlier_data = data[:, 1] - np.array(filtered_data)

# Optionally, you can amplify the outliers by multiplying the differences
amplified_outliers = outlier_data * 5  # Adjust the multiplier as needed to emphasize the outliers

# Plotting the data
plt.figure(figsize=(12, 8))

# Plot the original signal
plt.subplot(3, 1, 1)
plt.plot(data[:, 0], data[:, 1], label="Original Signal")
plt.title("Original Signal")
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.legend()

# Plot the filtered signal
plt.subplot(3, 1, 2)
plt.plot(data[:, 0], filtered_data, label="Median Filtered Signal", color='orange')
plt.title("Median Filtered Signal")
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.legend()

# Plot the amplified outliers (difference between original and filtered)
plt.subplot(3, 1, 3)
plt.plot(data[:, 0], amplified_outliers, label="Amplified Outliers", color='red')
plt.title("Amplified Outliers (Difference)")
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.legend()

# Show all plots
plt.tight_layout()
plt.show()
