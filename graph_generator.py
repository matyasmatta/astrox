import pandas as pd
import matplotlib.pyplot as plt
import csv
import numpy

x, y1, y2, y3 = list(), list(), list(), list()
with open("new_data_source.csv", "r") as f:
    reader = csv.reader(f, delimiter=",")
    for row in reader:
        x_val = row[2] if row[2] != ("Error was raised properly" or '') else numpy.nan
        x.append(x_val)

        y1_val = row[3] if row[3] != ("Error was raised properly" or '') else numpy.nan
        y1.append(y1_val)

        y2_val = row[4] if row[4] != ("Error was raised properly" or '') else numpy.nan
        y2.append(y2_val)

        y3_val = row[5] if row[5] != ("Error was raised properly" or '') else numpy.nan
        y3.append(y3_val)

print(x, y1)


def list_add(x):
    x_values = []
    for item in x:
        if item != '':
            x_values.append(float(item))
        else:
            x_values.append(None)
    return tuple(x_values)

# Create coordinate pairs
x_values = list_add(x)
y1_values = list_add(y1)
y2_values = list_add(y2)
y3_values = list_add(y3)


# Separate x and y coordinates into separate lists
print(x_values, y1_values)
plt.grid(True, which='both', axis='both', linestyle=':', linewidth=0.5)
plt.xticks(range(0, 2501, 250))
plt.yticks(range(0, 2501, 250))

# Plot the data as scatter plots
plt.scatter(x_values, y1_values, marker='x', label='Y1')
plt.scatter(x_values, y2_values, marker='x', label='Y2')
plt.scatter(x_values, y3_values, marker='x', label='Y3')

plt.xlim(0, 2500)
plt.ylim(0, 2500)

plt.xlabel('Cloud height calculated algorithmically in meters', labelpad=5)
plt.ylabel('Cloud height calculated manually in meters', labelpad=5)
plt.title("Fig. 2: Comparasion between manual and algorithmic data", pad=15)

# Set the aspect ratio to 'equal' and figure size to make it square
plt.gca().set_aspect('equal')
plt.gcf().set_size_inches(6,6)

# Get the number of points in the figure
num_points = len(plt.gca().collections[0].get_offsets())

print("Number of points:", num_points, len(x), len(y1))

plt.show()