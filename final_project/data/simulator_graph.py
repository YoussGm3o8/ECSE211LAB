import matplotlib.pyplot as plt
import numpy as np
import os
import sys

if len(sys.argv) < 2:
    print("Usage: python simulator_graph.py <input_file)>")
    sys.exit(1)
#open csv file in csv/simulated/sys.argv[1]
path = os.path.join(os.path.dirname(__file__), "csv", "simulated")
csv_path = os.path.join(path, sys.argv[1])
data = np.genfromtxt(csv_path, delimiter=',', skip_header=1)
plt.plot(data[:,0], data[:,1])
plt.show()

