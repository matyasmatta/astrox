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
angle = 135 # set the angle (formatted as reduced edoov coefficient) for search, i.e. clockwise

# calculate meta angle
angle_radians =np.radians(angle)
x_increase_meta = np.sin(angle_radians)
y_increase_meta = np.cos(angle_radians)
y_increase_meta = -y_increase_meta
x_increase_meta = np.round(x_increase_meta,5)
y_increase_meta = np.round(y_increase_meta,5)
print(x_increase_meta, y_increase_meta)

# keep the sign of the meta angle
if x_increase_meta < 0:
    x_increase_meta_sign = -1
if x_increase_meta >= 0:
    x_increase_meta_sign = 1
if y_increase_meta < 0:
    y_increase_meta_sign = -1
if y_increase_meta >= 0:
    y_increase_meta_sign = 1

# create absolute value for comparasion
x_increase_meta_abs = abs(x_increase_meta)
y_increase_meta_abs = abs(y_increase_meta)

# convert to the final angle
if x_increase_meta_abs > y_increase_meta_abs:
    x_increase_final_abs = 1
    y_increase_final_abs = (y_increase_meta_abs/x_increase_meta_abs)
if x_increase_meta_abs == y_increase_meta_abs: #pro 45 stupňů
    x_increase_final_abs = 1
    y_increase_final_abs = 1
if x_increase_meta_abs < y_increase_meta_abs:
    y_increase_final_abs = 1
    x_increase_final_abs = (x_increase_meta_abs/y_increase_meta_abs)

# put original signage back
x_increase_final = x_increase_meta_sign*x_increase_final_abs
y_increase_final = y_increase_meta_sign*y_increase_final_abs

     
# print for debugging
print(x_increase_final, y_increase_final)

y_sum = 0
x_sum = 0
count = 0
try:
    while True:
        count += 1
        if x_increase_final_abs == 1:
            if y_sum >= 1:
                y += 1
                y_sum -= 1
            if y_sum <= -1:
                y += -1
                y_sum += 1
            y_sum += y_increase_final
            data = (pix[x,y])
            print(data)
            value = round(average(data))
            print(value)
            x += 1
        if x_increase_final == -1:
            if y_sum >= 1:
                y += 1
                y_sum -= 1
            if y_sum <= -1:
                y += -1
                y_sum += 1
            y_sum += y_increase_final
            data = (pix[x,y])
            print(data)
            value = round(average(data))
            print(value)
            x -= 1
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
        if y_increase_final == -1:
            if x_sum >= 1:
                x += 1
                x_sum -= 1
            x_sum += x_increase_final
            data = (pix[x,y])
            print(data)
            value = round(average(data))
            print(value)
            y += -1
        if count > 20:
            break
except:
    print("Program ran successfully")
