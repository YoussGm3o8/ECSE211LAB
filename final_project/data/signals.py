import numpy as np
import matplotlib.pyplot as plt

# Function to compute the shortest distance from (x0, y0) to the boundary of a square
def distance_to_border(x0, y0, theta, L=122):
    # Distance to the left side (x = 0)
    if np.cos(theta) < 0:
        r_left = -x0 / np.cos(theta)
        y_left = y0 + r_left * np.sin(theta)
        if 0 <= y_left <= L:
            r_left_valid = np.abs(r_left)
        else:
            r_left_valid = np.inf
    else:
        r_left_valid = np.inf

    # Distance to the right side (x = L)
    if np.cos(theta) > 0:
        r_right = (L - x0) / np.cos(theta)
        y_right = y0 + r_right * np.sin(theta)
        if 0 <= y_right <= L:
            r_right_valid = np.abs(r_right)
        else:
            r_right_valid = np.inf
    else:
        r_right_valid = np.inf

    # Distance to the bottom side (y = 0)
    if np.sin(theta) < 0:
        r_bottom = -y0 / np.sin(theta)
        x_bottom = x0 + r_bottom * np.cos(theta)
        if 0 <= x_bottom <= L:
            r_bottom_valid = np.abs(r_bottom)
        else:
            r_bottom_valid = np.inf
    else:
        r_bottom_valid = np.inf

    # Distance to the top side (y = L)
    if np.sin(theta) > 0:
        r_top = (L - y0) / np.sin(theta)
        x_top = x0 + r_top * np.cos(theta)
        if 0 <= x_top <= L:
            r_top_valid = np.abs(r_top)
        else:
            r_top_valid = np.inf
    else:
        r_top_valid = np.inf

    # Return the minimum valid distance
    return min(r_left_valid, r_right_valid, r_bottom_valid, r_top_valid)


# Squared distance function (no changes from previous)
def squared_distance(x0, y0, observed_points, L=122):
    """
    Compute the squared distance between the observed data points and the model output for different x0, y0.
    :param x0: x-coordinate of the model point.
    :param y0: y-coordinate of the model point.
    :param observed_points: List or array of observed (theta, y) points.
    :param L: Domain length (default 122).
    :return: Squared distance value for the given (x0, y0).
    """
    squared_dist = 0
    for theta_i, y_i in observed_points:
        # Calculate model output (distance to border for the current (x0, y0) and theta_i)
        model_value = distance_to_border(x0, y0, theta_i, L)
        
        # Calculate squared difference
        squared_dist += (model_value - y_i)**2
    
    return squared_dist

# Function to compute squared distances for all pairs of x0, y0 within the lower triangle
def compute_lower_triangle_squared_distances(observed_points, L=122):
    """
    Compute squared distances for all pairs of x0, y0 within the lower triangle of the range [0, 61].
    :param observed_points: List of observed points (theta, y).
    :param L: Domain length (default 122).
    :return: A 2D array with squared distances for each (x0, y0) pair in the lower triangle.
    """
    x_range = np.linspace(0, 61, 62)  # 62 values from 0 to 61 inclusive
    y_range = np.linspace(0, 61, 62)  # 62 values from 0 to 61 inclusive
    
    # Initialize a list to store squared distances
    squared_distances = []
    coordinates = []
    
    # Iterate over all combinations of x0 and y0 within the lower triangle (x0 <= y0)
    for i, x0 in enumerate(x_range):
        for j, y0 in enumerate(y_range):
            if x0 <= y0:  # Only consider the lower triangle
                # Compute the squared distance for this pair (x0, y0)
                squared_dist = squared_distance(x0, y0, observed_points, L)
                squared_distances.append(squared_dist)
                coordinates.append((x0, y0))
    
    return np.array(squared_distances), np.array(coordinates)

# Example of how to use this function:
if __name__ == "__main__":
    # Example observed points (theta, y) you want to compare with the model
    #generate points from distance to border function using x0=60, y0=55
    x = np.linspace(0, 61, 200)
    y = [distance_to_border(22, 55, i, 122) for i in x]
    plt.plot(x,y)
    plt.show()
    observed_points = np.genfromtxt("csv/us_data.csv", delimiter=",", skip_header=1)
    observed_points = observed_points[21000:34000, :]
    #remove half of the points
    observed_points = observed_points[::32, :]
    #normalize x values so that it fits within [0, 25]
    observed_points[:, 0] -= 21000 
    observed_points[:, 0] /= 13000
    observed_points[:, 0] *= 25
    print(observed_points.shape)
    plt.plot(observed_points[:, 0], observed_points[:, 1])
    plt.show()

    # Compute the squared distances for all pairs of x0, y0 in the lower triangle
    squared_distances, coordinates = compute_lower_triangle_squared_distances(observed_points)
    min_index = np.argmin(squared_distances)
    print(f"Minimum squared distance: {coordinates[min_index]}")

    # Extract the x0 and y0 values from the coordinates
    x0_values = coordinates[:, 0]
    y0_values = coordinates[:, 1]

    # Plot the results
    plt.figure(figsize=(8, 6))
    plt.scatter(x0_values, y0_values, c=squared_distances, cmap='viridis', s=10)
    plt.colorbar(label='Squared Distance')
    plt.xlabel('x0')
    plt.ylabel('y0')
    plt.title('Squared Distance of Observed Data to Model (Lower Triangle)')
    plt.show()
