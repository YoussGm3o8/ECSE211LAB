import numpy as np
import matplotlib.pyplot as plt

# Define the triangular wave function
def triangular_wave(x, w=1, h=1):
    """
    Returns the value of a triangular wave at point x.
    The triangle wave has width w and height h.
    
    :param x: The point at which to evaluate the wave.
    :param w: The width of the triangular wave (default 1).
    :param h: The height of the triangular wave (default 1).
    :return: The value of the triangular wave at point x.
    """
    # Scale x to the range [0, 1] based on the width w
    x = x % w  # To handle wrapping of the wave
    if 0 <= x < 0.25 * w:
        return h * (2 * x / w)
    elif 0.25 * w <= x < 0.75 * w:
        return h * (1 - 2 * (x / w - 0.25))
    elif 0.75 * w <= x < w:
        return h * (2 * (x / w - 0.75))
    else:
        return 0

# Define the convolution function
def convolve_with_triangular_kernel(signal, w=1, h=1, kernel_size=5):
    """
    Perform convolution of the signal with a triangular wave kernel.
    
    :param signal: The input signal (numpy array).
    :param w: The width of the triangular wave (default 1).
    :param h: The height of the triangular wave (default 1).
    :param kernel_size: The size of the triangular kernel (default 5).
    :return: The convolution result (numpy array).
    """
    # Create a kernel using the triangular wave function
    kernel = [triangular_wave(i / kernel_size, w, h) for i in range(kernel_size)]
    
    # Perform convolution (sliding the kernel over the signal)
    convolution_result = []
    half_kernel = kernel_size // 2

    # Padding the signal at both ends with zeros to handle edge cases
    padded_signal = np.pad(signal, (half_kernel, half_kernel), 'constant', constant_values=(0, 0))

    for i in range(len(signal)):
        conv_value = np.sum(padded_signal[i:i+kernel_size] * kernel)
        convolution_result.append(conv_value)

    return np.array(convolution_result)

# Example usage
# Load your data (replace with correct path if needed)
import os
path = os.path.dirname(__file__)
path = os.path.join(path, "csv", "us_data3.csv")
data = np.genfromtxt(path, delimiter=",", skip_header=1)

signal = data[:, 1]  # Assuming your data's second column contains the signal
signal = np.diff(signal)

# Convolve the signal with a triangular wave kernel
kernel_size = 5  # Adjust this based on your needs
conv_result = convolve_with_triangular_kernel(signal, w=1, h=1, kernel_size=kernel_size)
#perform the convolution twice
conv_result2 = convolve_with_triangular_kernel(conv_result, w=1, h=1, kernel_size=kernel_size)

# Plotting
plt.figure(figsize=(12, 6))

# Plot the original signal
plt.subplot(2, 1, 1)
plt.plot(data[1:, 0], signal, label="Original Signal")
plt.plot(data[:, 0], data[:, 1])
plt.title("Original Signal")
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.legend()

# Plot the convolution result
plt.subplot(2, 1, 2)
plt.plot(data[1:, 0], conv_result, label="Convolution with Triangular Kernel", color='orange')
plt.plot(data[1:, 0], conv_result2, label="Convolution with Triangular Kernel", color='red')
plt.axhline(y=0, color='r', linestyle='--', label="Threshold")
plt.title("Convolution Result")
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.legend()

plt.tight_layout()
plt.show()

