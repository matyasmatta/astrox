import pandas as pd
import matplotlib.pyplot as plt
import csv
import numpy

font = {'size'   : 8}

plt.rc('font', **font)

x, red, rgb = list(), list(), list()
with open(r"C:\Users\kiv\Documents\GitHub\astrox\graph_generators\pixel_data.csv", "r") as f:
    reader = csv.reader(f, delimiter=",")
    for row in reader:
        x.append(row[0])
        rgb.append(row[1])
        red.append(row[2])

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
red_values = list_add(red)
rgb_values = list_add(rgb)

# Separate x and y coordinates into separate lists
plt.grid(True, which='both', axis='both', linestyle=':', linewidth=0.5)
plt.xticks(range(0, 41, 10))
plt.yticks(range(0, 251, 50))

# Plot the data as scatter plots
plt.plot(x_values, red_values, label='Red value')
plt.plot(x_values, rgb_values, label='Avg RGB value')

plt.legend(loc="upper center", numpoints=1, ncol=4)


plt.xlim(0, 40)
plt.ylim(0, 250)

plt.xlabel('Pixel no.', labelpad=5)
plt.ylabel('Pixel value', labelpad=5)

# Set the aspect ratio to 'equal' and figure size to make it square
plt.gcf().set_size_inches(3.1,2)
plt.savefig('fig5.png', dpi=1000)

plt.show()