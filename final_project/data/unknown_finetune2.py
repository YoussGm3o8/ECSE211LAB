import numpy as np
from color_numpy import green, blue, red, yellow, orange, purple
from button2_svm import predict

# Concatenate the dataset and initialize target values
dataset = np.concatenate((green, blue, red, yellow, orange, purple), axis=0)

target = np.concatenate([
    np.full((len(green),), 'g'),
    np.full((len(blue),), 'b'),
    np.full((len(red),), 'r'),
    np.full((len(yellow),), 'y'),
    np.full((len(orange),), 'o'),
    np.full((len(purple),), 'p')
])

# Function to compute Type 1 error
def compute_type1(predictions, target):
    pred = np.array(predictions)
    target = np.array(target)
    
    # Compute type 1 error: false positives
    type1_error = np.sum((pred != target) & (pred != 'unknown')) / len(pred)
    
    # Compute percentage of unknowns
    unknowns = np.sum(pred == 'unknown') / len(pred)
    
    # Return combined score: Type 1 error and penalty for unknowns
    print(f"Type 1 error: {type1_error:.4f}, Unknown ratio: {unknowns:.4f}")
    return type1_error + 0.05 * unknowns

# Function to compute the decision plane
def compute_plane(x, weights, bias):
    return np.dot(x, weights) + bias

# Evaluate random planes and minimize Type 1 error
best_score = float('inf')
best_weights = None
best_bias = None

# Generate random search or optimization
for iteration in range(1000):  # Limit number of iterations for efficiency
    # Randomly initialize weights and bias
    weights = np.random.random_integers(0, 1000, 3)
    weights  = (weights - 500) / 250  # Random weights between -2 and 2
    bias = np.random.random_integers(0, 1000) / 100 - 5  # Random bias between -5 and 5
    
    # Classify the data based on the decision plane
    predictions = [predict(d) if compute_plane(d, weights, bias) > 0 else 'unknown' for d in dataset]
    
    # Compute the Type 1 error for this configuration
    score = compute_type1(predictions, target)
    
    # Keep track of the best configuration
    if score < best_score:
        best_score = score
        best_weights = weights
        best_bias = bias
        print(f"New best score: {best_score:.4f}")
        print(f"Weights: {best_weights}, Bias: {best_bias}")

print(f"Final best configuration - Weights: {best_weights}, Bias: {best_bias}")
print(f"Final best score: {best_score:.4f}")


# plot a scatter graph of the data with unknown as its own color
import matplotlib.pyplot as plt

# Scatter plot 3D

#overwrite target with unknown
new_target = []
for d in dataset:
    if compute_plane(d, best_weights, best_bias) > 0:
        new_target.append(predict(d))
    else:
        new_target.append('unknown')

#plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
color_data = {"g": [], "b": [], "r": [], "y": [], "o": [], "p": [], "unknown": []}
colors = {'g':"green", 'b':"blue", 'r':"red", 'y':"yellow", 'o':"orange", 'p':"purple", 'unknown':"black"}
for d, t in zip(dataset, new_target):
    color_data[t].append(d)
for color, data in color_data.items():
    data = np.array(data)
    ax.scatter(data[:, 0], data[:, 1], data[:, 2], c=colors[color], marker='o', label=color)
plt.show()
