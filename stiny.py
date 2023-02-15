from PIL import Image
import numpy as np
from numpy import average 


# open specific cloud
im = Image.open(r'C:\Users\kiv\Documents\GitHub\astrox\AO_2022.png') # Can be many different formats.
pix = im.load()
# get the width and hight of the image for iterating over
print(im.size)  

# set coordinates from AI model
x = 198
y = 118
angle = 90 # set the angle (formatted as reduced edoov coefficient) for search, i.e. clockwise

angle_radians =np.radians(angle)
x_increase_meta = np.sin(angle_radians)
y_increase_meta = np.cos(angle_radians)
print(x_increase_meta, y_increase_meta)

if x_increase_meta > y_increase_meta:
    x_increase_final = 1
    y_increase_final = (y_increase_meta/x_increase_meta)
if x_increase_meta == y_increase_meta:
    x_increase_final = 1
    y_increase_final = 1
if x_increase_meta < y_increase_meta:
    y_increase_final = 1
    x_increase_final = (x_increase_meta/y_increase_meta)
print(x_increase_final, y_increase_final)

# include quarter information
if 0<angle<90 or angle == 90:
    q = 1
    x = x
    y = -y
if 90<angle<180 or angle == 180:
    q = 2
    x = x
    y = y
if 180<angle<270 or angle == 270:
    q = 3
    x = -x
    y = y
if 270<angle<360 or angle == 270:
    q = 4
    x = -x
    y = -y

y_sum = 0
x_sum = 0
count = 0
try:
    while True:
        count += 1
        if x_increase_final == 1:
            if y_sum >= 1:
                y += 1
                y_sum -= 1
            y_sum += y_increase_final
            data = (pix[x,y])
            print(data)
            value = round(average(data))
            print(value)
            x += 1
        if y_increase_final == 1:
            if x_sum >= 1:
                x += 1
                x_sum -= 1
            x_sum += x_increase_final
            data = (pix[x,y])
            print(data)
            value = round(average(data))
            print(value)
            y += 1
        if count > 10:
            break
except:
    print("Program ran successfully")
