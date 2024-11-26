import numpy as np
from color_numpy import green, blue, red, yellow, orange, purple
from button1_svm import predict

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
def is_unknown(pixel, treshold):
    s = np.sum(pixel)
    s = np.max((s, 0.0001))
    pixel = pixel / s
    ent = -np.sum(pixel * np.log(pixel))
    # print(ent)
    return True if ent < treshold else False


# Evaluate random planes and minimize Type 1 error
best_score = float('inf')
best_treshold = 0

# Generate random search or optimization
for iteration in range(1000):  # Limit number of iterations for efficiency
    # Randomly initialize weights and bias
    treshold = iteration / 500

    # Classify the data based on the decision plane
    predictions = [predict(d) if not is_unknown(d, treshold) else 'unknown' for d in dataset]
    
    # Compute the Type 1 error for this configuration
    score = compute_type1(predictions, target)
    
    # Keep track of the best configuration
    if score < best_score:
        best_score = score
        best_treshold = treshold
        print(f"New best score: {best_score:.4f}")
        print(f"New best treshold: {best_treshold:.4f}")

print(f"Final best configuration - Treshold: {best_treshold}")
print(f"Final best score: {best_score:.4f}")

# plot a scatter graph of the data with unknown as its own color
import matplotlib.pyplot as plt

# Scatter plot 3D

#overwrite target with unknown
new_target = []
for d in dataset:
    if is_unknown(d, best_treshold):
        new_target.append('unknown')
    else:
        new_target.append(predict(d))

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
