import numpy as np
from color_numpy import green, blue, red, yellow, orange, purple
from button1_svm import predict
import matplotlib.pyplot as plt

# Concatenate the dataset and initialize target values
dataset = np.concatenate((green, blue, red, yellow, orange, purple), axis=0)

# Initialize target with direct array creation to avoid redundant operations
target = np.concatenate([
    np.full((len(green),), 'g'),
    np.full((len(blue),), 'b'),
    np.full((len(red),), 'r'),
    np.full((len(yellow),), 'y'),
    np.full((len(orange),), 'o'),
    np.full((len(purple),), 'p')
])

# Vectorized function to compute Type 1 error
def compute_type1(predictions, target):
    pred = np.array(predictions)
    target = np.array(target)
    
    # Compute type 1 error: false positives (vectorized)
    type1_error = np.sum((pred != target) & (pred != 'unknown')) / len(pred)
    
    # Compute percentage of unknowns (vectorized)
    unknowns = np.sum(pred == 'unknown') / len(pred)
    
    # Return combined score: Type 1 error and penalty for unknowns
    return type1_error + 0.5 * unknowns

# Vectorized check for unknown decision based on entropy
def is_unknown(pixel, threshold):
    s = np.sum(pixel, axis=1)
    s = np.maximum(s, 0.0001)  # Avoid division by zero
    pixel = pixel / s[:, None]  # Normalize each row
    entropy = -np.sum(pixel * np.log(pixel), axis=1)
    return entropy > threshold

# Function for parallelized prediction using vectorized operations
def bulk_predict(dataset, threshold):
    is_unknown_pixels = is_unknown(dataset, threshold)
    predictions = np.array([predict(d) if not unknown else 'unknown' for d, unknown in zip(dataset, is_unknown_pixels)])
    return predictions

# Initialize best score tracking
best_score = float('inf')
best_threshold = 0

# Perform a random search for optimal threshold with bulk prediction
for iteration in range(100):
    threshold = iteration / 50
    
    # Bulk prediction of the entire dataset
    predictions = bulk_predict(dataset, threshold)
    
    # Compute the Type 1 error for this configuration
    score = compute_type1(predictions, target)
    
    # Track the best score and threshold
    if score < best_score:
        best_score = score
        best_threshold = threshold
        print(f"New best score: {best_score:.4f}")
        print(f"New best threshold: {best_threshold:.4f}")

# Final result
print(f"Final best configuration - Threshold: {best_threshold}")
print(f"Final best score: {best_score:.4f}")

# Visualize the results with scatter plot
# Vectorized classification of the dataset using the best threshold
new_target = bulk_predict(dataset, best_threshold)

# Plotting
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Create a mapping of colors for the target classes
color_data = {"g": [], "b": [], "r": [], "y": [], "o": [], "p": [], "unknown": []}
colors = {'g': "green", 'b': "blue", 'r': "red", 'y': "yellow", 'o': "orange", 'p': "purple", 'unknown': "black"}

for d, t in zip(dataset, new_target):
    color_data[t].append(d)

for color, data in color_data.items():
    data = np.array(data).reshape(-1, 3)
    ax.scatter(data[:, 0], data[:, 1], data[:, 2], c=colors[color], marker='o', label=color)

plt.show()
