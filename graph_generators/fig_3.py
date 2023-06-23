import pandas as pd
import matplotlib.pyplot as plt
import csv
import numpy

font = {'size'   : 8}

plt.rc('font', **font)

x, y1, y2, i = list(), list(), list(), int()
with open(r"C:\Users\kiv\Documents\GitHub\astrox\graph_generators\data_david_fig3.csv", "r") as f:
    reader = csv.reader(f, delimiter=",")
    for row in reader:
        x.append(i)
        y1.append(row[0])
        y2.append(row[1])
        i+=1
print(x, y1, y2)


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

# Separate x and y coordinates into separate lists
print(x_values, y1_values)

# Plot the data as scatter plots
plt.fill_between(x_values, y1_values, facecolor='red', alpha=0.5, label="Real latitude")
plt.fill_between(x_values, y2_values, facecolor='blue', alpha=0.5, label="Magnetometer data")
plt.ylabel("North azimuth")
plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=False,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    labelbottom=False)
plt.xlabel("One Flight Epoch")
plt.legend(loc="upper center", numpoints=1, ncol=4)

plt.ylim(20, 170)
plt.xlim(250,2350)
# Set the aspect ratio to 'equal' and figure size to make it square
plt.gcf().set_size_inches(6,3)

# Get the number of points in the figure
num_points = len(plt.gca().collections[0].get_offsets())

print("Number of points:", num_points, len(x), len(y1))
plt.savefig('fig3.png', dpi=1000)
plt.show()