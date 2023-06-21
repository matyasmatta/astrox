from PIL import Image
import numpy as np
from numpy import average 
from skyfield import api
from skyfield import almanac
import os
import json
import csv
import exifmeta

# ignore the 'json' in the name, we replaced the file format with csv for simplicity, jsons are useful for export data - not metadata
def write_pixel_into_json(count, x, y, cloud_id="not specified", image_id="not specified"):
    with open('pixels.csv', 'a') as f:
        writer = csv.writer(f)
        data = [image_id, cloud_id, count, x, y]
        writer.writerow(data)

def starting_point_corrector(x_centre, y_centre, x_increase_final, y_increase_final):
    constant_for_starting_point_correction = 10
    x_final = x_centre + constant_for_starting_point_correction*x_increase_final
    y_final = y_centre + constant_for_starting_point_correction*y_increase_final
    x_final = round(x_final)
    y_final = round(y_final)
    return x_final, y_final

def calculate_shadow(file_path, x, y, angle, cloud_id="not specified", image_id="not specified", run_path = "./", file_name = "not_specified"):
    im = Image.open(file_path)
    pix = im.load() 
    total_x, total_y = im.size
    total_x -= 1
    total_y -= 1

    meta_name =  run_path +"/meta_shadow/meta_" + file_name + ".bmp"
    pixels_txt_classic_name = run_path +"/pixel_txt/classic_" + file_name + str(cloud_id) + ".txt"
    pixels_txt_red_name = run_path +"/pixel_txt/red_" + file_name + str(cloud_id) + ".txt"

    # calculate meta angle
    angle_radians =np.radians(angle)
    x_increase_meta = np.sin(angle_radians)
    y_increase_meta = np.cos(angle_radians)
    y_increase_meta = -y_increase_meta
    x_increase_meta = np.round(x_increase_meta,5)
    y_increase_meta = np.round(y_increase_meta,5)
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

    y_sum = int()
    x_sum = int()
    count = int()
    list_of_values = list()
    list_of_red = list()

    year, month, day, hour, minute, second = exifmeta.find_time(file_path)
    altitude = exifmeta.sun_data.altitude(exifmeta.get_latitude(file_path), exifmeta.get_longitude(file_path), year, month, day, hour, minute, second)

    sun_altitude_for_limit_radians = altitude*(np.pi/180)
    limit_cloud_height = 3000 #not meters
    limit_shadow_cloud_distance = limit_cloud_height/np.tan(sun_altitude_for_limit_radians)
    limit_shadow_cloud_distance_pixels = limit_shadow_cloud_distance/126.48
    limit = limit_shadow_cloud_distance_pixels

    # clear the whole txt file

    if os.path.exists(meta_name) == False:
        im2 = im.copy()
        im.save(meta_name)

    x_increase_abs = abs(x_increase_final)
    y_increase_abs = abs(y_increase_final)
    if q == 1:
        x_dir = +1
        y_dir = -1
    if q == 2:
        x_dir = +1
        y_dir = +1
    if q == 3:
        x_dir = -1
        y_dir = +1
    if q == 4:
        x_dir = -1
        y_dir = -1

    x, y = starting_point_corrector(x, y, x_increase_final, y_increase_final)

    # Beautifully simplified method when compared to release ;)
    x_sum = 0
    y_sum = 0
    while True:
        if x_sum >= 1:
            x_sum -= 1
            x += x_dir
        if y_sum >= 1:
            y_sum -= 1
            y += y_dir
        x_sum += x_increase_abs
        y_sum += y_increase_abs
        if x > total_x or y > total_y or x == 1 or y == 1 or count >= (limit+10): # + constant_for_starting_point_correction, občas chyběl konec stínu
            break
        
        data = (pix[x,y])
        value = round(average(data))
        value_red = data[0]
        list_of_red.append(value_red)
        list_of_values.append(value)
        im2 = Image.open(meta_name)
        im2.putpixel((x,y),(0,0,0,0))
        im2.save(meta_name)
        count += 1
    im2.save(meta_name)

    # Get pixel data into txts; later for graphs
    with open(pixels_txt_classic_name, "a") as file:
        for i in range(len(list_of_values)):
            file.write(str(list_of_values[i]) + "\n") 
    with open(pixels_txt_red_name, "a") as file:
        for i in range(len(list_of_red)):
            file.write(str(list_of_red[i]) + "\n") 
    
    # This is the first method that is used to calculate the shadow lenght
    def calculate_using_min_max(list_of_values):
        # Define internal function
        def main():
            # Find items in list correspoding to the lowest and highest point
            shadow_low = min(list_of_values)
            cloud_high = max(list_of_values)

            # Find of said items in the list (their order)
            shadow_location = list_of_values.index(shadow_low)
            cloud_location = list_of_values.index(cloud_high)

            # Find the difference
            shadow_lenght = shadow_location - cloud_location
            return shadow_lenght, cloud_high, shadow_low, cloud_location, shadow_location
        
        # Initialise run
        shadow_lenght, cloud_high, shadow_low, cloud_location, shadow_location = main()

        # Validate if data is 1) positive and there is 2) no shadow in the complete beginning (returns wrong values)
        while shadow_lenght <= 0:
            if shadow_location < 10:
                list_of_values.remove(shadow_low)
            else:
                list_of_values.remove(cloud_high)

            # Rerun functions once validation is done (is rerun as many times as is necessary)
            shadow_lenght, cloud_high, shadow_low, cloud_location, shadow_location = main()
        
        # Returns two values as the cloud location proved useful in the other calculation method
        return shadow_lenght, cloud_location

    # Second calculation method
    def calculate_using_maximum_change(list_of_values):
        # Get the n variable which specified how far from initial point we should start calculating (keep in mind it's the centre minus 10 pixels)
        _, n = calculate_using_min_max(list_of_values)

        # Define the main internal function    
        def main(n):
            list_of_changes = []
            while n < len(list_of_values):
                try:
                    current_data = list_of_values[n]
                    previous_data = list_of_values[n-1]
                    change_in_data = current_data-previous_data
                    if n == 0:
                        pass
                    else:
                        list_of_changes.append(change_in_data)
                    n+=1
                except:
                    break
            shadow_low = max(list_of_changes)
            cloud_high = min(list_of_changes)

            shadow_location = list_of_changes.index(shadow_low)
            cloud_location = list_of_changes.index(cloud_high)

            # Find difference between the two pixel lenghts
            shadow_lenght = shadow_location - cloud_location
            return shadow_lenght, cloud_high, cloud_location
        shadow_lenght, cloud_high, cloud_location = main(n)
        while True:
            if shadow_lenght <= 0:
                item_to_be_deleted = list_of_values[cloud_location]
                list_of_values.remove(item_to_be_deleted)
                shadow_lenght, cloud_high, cloud_location = main(n)
            else:
                break

        return shadow_lenght
    
    # Get data from internal functions that take pixel values into shadow lenght
    shadow_lenght_min_max, _ = calculate_using_min_max(list_of_values)
    shadow_lenght_min_max_red, _ = calculate_using_min_max(list_of_red)
    shadow_lenght_max_difference = calculate_using_maximum_change(list_of_values)
    shadow_lenght_max_difference_red = calculate_using_maximum_change(list_of_red)
    
    # Calculate the maximum difference between methods
    if abs(shadow_lenght_min_max_red - shadow_lenght_min_max) > 10:
        shadow_lenght_final = (shadow_lenght_max_difference+shadow_lenght_min_max)/2
        message = "Difference between methods was too high"
    else:
        shadow_lenght_final = (shadow_lenght_max_difference+shadow_lenght_min_max+shadow_lenght_max_difference_red+shadow_lenght_min_max_red)/4
    
    # Data validation using the differences in data
    all_methods = list()
    all_methods.append(shadow_lenght_min_max)
    all_methods.append(shadow_lenght_min_max_red)
    all_methods.append(shadow_lenght_max_difference)
    all_methods.append(shadow_lenght_max_difference_red)
    difference_of_methods = max(all_methods) - min(all_methods)


    # calculate distance using said function
    lenght = shadow_lenght_final*126.48

    # because original lenghts is not Archimedes-compatible we will have to convert
    angle_final_radians = angle_final*(np.pi/180)
    if angle_final <= 45:
        lenght = lenght/np.cos(angle_final_radians)
    if angle_final > 45:
        lenght = lenght/np.sin(angle_final_radians)

    altitude_radians = altitude*(np.pi/180)
    cloudheight = np.tan(altitude_radians)*lenght
    cloudheight = np.round(cloudheight,2)

    return cloudheight, shadow_lenght_final, shadow_lenght_min_max, shadow_lenght_max_difference, difference_of_methods

if __name__ == '__main__':
    cloudheight = calculate_shadow('zchop.meta.x000.y000.n011.jpg', 294,199,270)
    print(cloudheight)