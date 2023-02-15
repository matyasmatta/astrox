from PIL import Image
import numpy as np
from numpy import average 

# open specific cloud
im = Image.open(r'C:\Users\kiv\Documents\GitHub\astrox\AO_2022.png') # Can be many different formats.
pix = im.load()
# get the width and hight of the image for iterating over
print(im.size)  

# set coordinates from AI model
x = 1
y = 1
angle = 0 # set the angle (formatted as reduced edoov coefficient) for search, i.e. clockwise

# calculate meta angle
angle_radians =np.radians(angle)
x_increase_meta = np.sin(angle_radians)
y_increase_meta = np.cos(angle_radians)
y_increase_meta = -y_increase_meta
x_increase_meta = np.round(x_increase_meta,5)
y_increase_meta = np.round(y_increase_meta,5)
print(x_increase_meta, y_increase_meta)
x_increase_meta_abs = abs(x_increase_meta)
y_increase_meta_abs = abs(y_increase_meta)

# divide into quadrant and basic angle information
if 0 <= angle <= 90:
    q = 1
    angle_final = angle 
if 90 < angle <= 180:
    q = 2
    angle_final = angle - 90
if 180 < angle <= 270:
    q = 3
    angle_final = angle - 180
if 270 < angle <= 360:
    q = 4
    angle_final = angle - 270

# make at least one variable 1 and the other smaller than 1
if x_increase_meta_abs > y_increase_meta_abs:
    x_increase_final = 1
    y_increase_final = y_increase_meta_abs/x_increase_meta_abs
if x_increase_meta_abs == y_increase_meta_abs:
    x_increase_final = 1
    y_increase_final = 1
if x_increase_meta_abs < y_increase_meta_abs:
    x_increase_final = x_increase_meta_abs/y_increase_meta_abs
    y_increase_final = 1
if angle_final == 0:
    x_increase_final = 0
    y_increase_final = 1

# set absolute final values
x_increase_final_abs = abs(x_increase_final)
y_increase_final_abs = abs(y_increase_final)

y_sum = 0
x_sum = 0
count = 0

# put quarter information back for pixel reading
if q == 1:
    x_increase_final = x_increase_final
    y_increase_final = -y_increase_final
    while True:
        count += 1
        if x_increase_final_abs > y_increase_final_abs:
            # check if y_sum is bigger than 1
            y_sum = abs(y_sum)
            if y_sum >= 1:
                y_sum -= 1
                y -= 1
            # read pixel value
            data = (pix[x,y])
            print(data)
            value = round(average(data))
            print(value)
            # add to y_sum and move pixel x for 1
            x += 1
            y_sum += y_increase_final_abs
        if x_increase_final_abs == y_increase_final_abs:
            data = (pix[x,y])
            print(data)
            value = round(average(data))
            print(value)
            x += 1
            y -= 1
        if x_increase_final_abs < y_increase_final_abs:
            x_sum = abs(x_sum)
            if x_sum >= 1:
                x_sum -= 1
                x += 1
            # read pixel value
            data = (pix[x,y])
            print(data)
            value = round(average(data))
            print(value)
            # add to y_sum and move pixel x for 1
            y -= 1
            x_sum += x_increase_final_abs
        if count > 20:
            break
if q == 2:
    x_increase_final = x_increase_final
    y_increase_final = y_increase_final   
    while True:
        count += 1
        if x_increase_final_abs > y_increase_final_abs:
            # check if y_sum is bigger than 1
            y_sum = abs(y_sum)
            if y_sum >= 1:
                y_sum -= 1
                y += 1
            # read pixel value
            data = (pix[x,y])
            print(data)
            value = round(average(data))
            print(value)
            # add to y_sum and move pixel x for 1
            x += 1
            y_sum += y_increase_final_abs
        if x_increase_final_abs == y_increase_final_abs:
            data = (pix[x,y])
            print(data)
            value = round(average(data))
            print(value)
            x += 1
            y += 1
        if x_increase_final_abs < y_increase_final_abs:
            x_sum = abs(x_sum)
            if x_sum >= 1:
                x_sum -= 1
                x += 1
            # read pixel value
            data = (pix[x,y])
            print(data)
            value = round(average(data))
            print(value)
            # add to y_sum and move pixel x for 1
            y += 1
            x_sum += x_increase_final_abs
        if count > 20:
            break
if q == 3:
    x_increase_final = -x_increase_final
    y_increase_final = y_increase_final 
    while True:
        count += 1
        if x_increase_final_abs > y_increase_final_abs:
            # check if y_sum is bigger than 1
            y_sum = abs(y_sum)
            if y_sum >= 1:
                y_sum -= 1
                y += 1
            # read pixel value
            data = (pix[x,y])
            print(data)
            value = round(average(data))
            print(value)
            # add to y_sum and move pixel x for 1
            x -= 1
            y_sum += y_increase_final_abs
        if x_increase_final_abs == y_increase_final_abs:
            data = (pix[x,y])
            print(data)
            value = round(average(data))
            print(value)
            x -= 1
            y += 1
        if x_increase_final_abs < y_increase_final_abs:
            x_sum = abs(x_sum)
            if x_sum >= 1:
                x_sum -= 1
                x -= 1
            # read pixel value
            data = (pix[x,y])
            print(data)
            value = round(average(data))
            print(value)
            # add to y_sum and move pixel x for 1
            y += 1
            x_sum += x_increase_final_abs
        if count > 20:
            break
if q == 4:
    x_increase_final = -x_increase_final
    y_increase_final = -y_increase_final 
    while True:
        count += 1
        if x_increase_final_abs > y_increase_final_abs:
            # check if y_sum is bigger than 1
            y_sum = abs(y_sum)
            if y_sum >= 1:
                y_sum -= 1
                y -= 1
            # read pixel value
            data = (pix[x,y])
            print(data)
            value = round(average(data))
            print(value)
            # add to y_sum and move pixel x for 1
            x -= 1
            y_sum += y_increase_final_abs
        if x_increase_final_abs == y_increase_final_abs:
            data = (pix[x,y])
            print(data)
            value = round(average(data))
            print(value)
            x -= 1
            y -= 1
        if x_increase_final_abs < y_increase_final_abs:
            x_sum = abs(x_sum)
            if x_sum >= 1:
                x_sum -= 1
                x -= 1
            # read pixel value
            data = (pix[x,y])
            print(data)
            value = round(average(data))
            print(value)
            # add to y_sum and move pixel x for 1
            y -= 1
            x_sum += x_increase_final_abs
        if count > 20:
            break

# print for debugging
print(x_increase_final, y_increase_final)

# set absolute final values
x_increase_final_abs = abs(x_increase_final)
y_increase_final_abs = abs(x_increase_final)