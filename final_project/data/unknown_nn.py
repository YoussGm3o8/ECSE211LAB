"""
This script will not work without disabling unknowns in button1_svm.py
"""
import os
import numpy as np
from button1_svm import predict

path = os.path.join(os.path.dirname(__file__), "csv", "color")
green = np.genfromtxt(os.path.join(path, "green.csv"), delimiter=',', skip_header=1)
blue = np.genfromtxt(os.path.join(path, "blue.csv"), delimiter=',', skip_header=1)
red = np.genfromtxt(os.path.join(path, "red.csv"), delimiter=',', skip_header=1)
yellow = np.genfromtxt(os.path.join(path, "yellow.csv"), delimiter=',', skip_header=1)
orange = np.genfromtxt(os.path.join(path, "orange.csv"), delimiter=',', skip_header=1)
purple = np.genfromtxt(os.path.join(path, "purple.csv"), delimiter=',', skip_header=1)


# Concatenate the dataset and initialize target values
dataset = np.concatenate((green, blue, red, yellow, orange, purple), axis=0)
cov = np.cov(dataset.T)
cov_diag = np.diag(cov)
cov_diag = cov_diag / np.sqrt(np.sum(cov_diag**2))
print(cov_diag)

target = np.concatenate([
    np.full((len(green),), 'g'),
    np.full((len(blue),), 'b'),
    np.full((len(red),), 'r'),
    np.full((len(yellow),), 'y'),
    np.full((len(orange),), 'o'),
    np.full((len(purple),), 'p')
])

def compute_accuracy(predictions, target):
    pred = np.array(predictions)
    target = np.array(target)
    
    # Compute type 1 error: false positives
    # accuracy = np.sum(pred == target | pred == 'unknown', axis=0) / len(pred)
    accuracy = np.sum(pred == target)
    unknown_count = np.sum(pred == 'unknown')
    accuracy = (accuracy + unknown_count)/len(pred)

    print(f"Accuracy: {accuracy:.4f}")



# Function to compute Type 1 error
def compute_type1(predictions, target):
    pred = np.array(predictions)
    target = np.array(target)
    
    # Compute type 1 error: false positives
    type1_error = np.sum((pred != target) & (pred != 'unknown'))/ len(pred)
    unknowns = np.sum(pred == 'unknown') / len(pred)

    # Compute percentage of unknowns

    # Return combined score: Type 1 error and penalty for unknowns
    # print(f"Type 1 error: {type1_error:.4f}, Unknown ratio: {unknowns:.4f}")
    return type1_error + 0.1 * unknowns, type1_error

# Function to compute the decision plane
def not_unknown(x, treshold):
    x = np.dot(x, cov_diag ))
    dist = np.sum(x**2)
    return dist > treshold

compute_type1([predict(d) for d in dataset], target)

# Evaluate random planes and minimize Type 1 error
best_score = float('inf')
best_type1 = 0
best_treshold = None

# Generate random search or optimization
for iteration in reversed(range(50, 300)):  # Limit number of iterations for efficiency
    # Randomly initialize treshold
    treshold = iteration * 5
    # Classify the data based on the decision plane
    predictions = [predict(d) if not_unknown(d, treshold) else 'unknown' for d in dataset]

    # Compute the Type 1 error for this configuration
    score, type1 = compute_type1(predictions, target)

    # Keep track of the best configuration
    if score < best_score:
        best_score = score
        best_type1 = type1
        best_treshold = treshold
        print(f"New best score: {best_score:.4f}")
        print(f"New best treshold: {best_treshold:.4f}")

print(f"Final best treshold: {best_treshold:.4f}")
print(f"Final best score: {best_score:.4f}")
print(f"Final best type 1 error: {best_type1:.4f}")


predictions = [predict(d) if not_unknown(d, best_treshold) else 'unknown' for d in dataset]
compute_accuracy(predictions, target)

# plot a scatter graph of the data with unknown as its own color
import matplotlib.pyplot as plt

# Scatter plot 3D

#overwrite target with unknown
new_target = []
for d in dataset:
    if not_unknown(d, best_treshold):
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
#display axis names
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()
