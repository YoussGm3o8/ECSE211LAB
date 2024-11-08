"""
This file must be run locally (not on the raspberry pi)
"""
import os
import time
import matplotlib.pyplot as plt

while True:
    os.system("./sync_log.sh")
    with open("session.log", "r") as f:
        log = f.read()
        values = []
        for line in log.split("\n"):
            if line == "":
                break
            try:
                print(line)
                values.append(float(line))
            except Exception as e:
                print(e)
                continue
        plt.bar(range(len(values)), values)
        plt.show()


