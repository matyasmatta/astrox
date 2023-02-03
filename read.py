from PIL import Image
import numpy as np
from numpy import average 

im = Image.open(r'C:\Users\kiv\Documents\GitHub\astrox\dataset\crop\zchop.meta.x000.y485.n009.jpg') # Can be many different formats.
pix = im.load()
print(im.size)  # Get the width and hight of the image for iterating over
    
x = 302
y = 112
while True:
    x -= 1
    data = (pix[x,y])
    value = round(average(data))
    print(value)