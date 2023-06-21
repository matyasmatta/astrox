import matplotlib.pyplot as plt
import numpy as np
import os

def plot_graph(rgb, red, name):

    x = np.arange(len(rgb))  
    rgb = np.array(rgb)
    red = np.array(red)


    plt.plot(x, rgb, label='RGB', color= 'blue')
    plt.plot(x, red, label='RED', color = 'red')

    plt.savefig(name)
    plt.close()
    del x, name, rgb, red
