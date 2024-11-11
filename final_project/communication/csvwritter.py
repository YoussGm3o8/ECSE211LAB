import csv
import sys

#verify that an argument was passed
if len(sys.argv) < 2:
    print('Usage: csvwritter.py <filename>')
    sys.exit(1)

arg1 = sys.argv[1]


def to_csv(data):
    with open(arg1, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)
    print(f"Data written to {arg1}")
