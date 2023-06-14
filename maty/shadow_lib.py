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
    x_final = x_centre - constant_for_starting_point_correction*x_increase_final
    y_final = y_centre - constant_for_starting_point_correction*y_increase_final
    x_final = round(x_final, 0)
    x_final = int(x_final)
    y_final = round(y_final, 0)
    y_final = int(y_final)
    return x_final, y_final

def calculate_shadow(file_path, x, y, angle, cloud_id="not specified", image_id="not specified", run_path = "./", file_name = "not_specified"):
    im = Image.open(file_path)
    pix = im.load() 
    total_x, total_y = im.size
    total_x -= 1
    total_y -= 1

    meta_name =  run_path +"/meta_shadow/meta" + file_name + ".bmp"

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
    limit_cloud_height = 7500 #not meters
    limit_shadow_cloud_distance = limit_cloud_height/np.tan(sun_altitude_for_limit_radians)
    limit_shadow_cloud_distance_pixels = limit_shadow_cloud_distance/142
    limit = limit_shadow_cloud_distance_pixels

    # clear the whole txt file
    with open('stiny.txt', 'w') as f:
        f.write("\n")
    with open('stiny_red.txt', 'w') as f:
        f.write("\n")

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
    print(x_increase_abs, y_increase_abs, x_dir, y_dir)

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
        if x > total_x or y > total_y or x == 1 or y == 1 or count >= limit:
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
    # set absolute final values
    x_increase_final_abs = abs(x_increase_final)
    y_increase_final_abs = abs(x_increase_final)

    def calculate_using_min_max(list_of_values):
        def main():
            # find items in list correspoding to the lowest and highest point
            shadow_low = min(list_of_values)
            cloud_high = max(list_of_values)

            # find of said items in the list (their order)
            shadow_location = list_of_values.index(shadow_low)
            cloud_location = list_of_values.index(cloud_high)

            # find the difference
            shadow_lenght = shadow_location - cloud_location
            return shadow_lenght, cloud_high, shadow_low, cloud_location, shadow_location
        shadow_lenght, cloud_high, shadow_low, cloud_location, shadow_location = main()
        while True:
            if shadow_lenght <= 0:
                list_of_values.remove(cloud_high)
                shadow_lenght, cloud_high, shadow_low, cloud_location, shadow_location = main()
            else:
                break
        return shadow_lenght

    def calculate_using_maximum_change(list_of_values):
        def main():
            n = 0
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

            # find difference between the two pixel lenghts
            shadow_lenght = shadow_location - cloud_location
            # print("max difference", shadow_lenght)
            # im2.show()
            return shadow_lenght, cloud_high, cloud_location
        shadow_lenght, cloud_high, cloud_location = main()
        while True:
            n = 0
            if shadow_lenght <= 0:
                item_to_be_deleted = list_of_values[cloud_location]
                list_of_values.remove(item_to_be_deleted)
                shadow_lenght, cloud_high, cloud_location = main()
                # print("When calculating via maximum change, the shadow resulted being negative, recalculation in progress.")
            else:
                break

        return shadow_lenght

    # define a simple function to calculate distance based on a given FOV and distance in pixels
    def distance(fieldOfView, distanceinpixels):
        fieldOfViewRadians = fieldOfView*(np.pi/180)
        distanceinmeters = int(distanceinpixels)*142
        return distanceinmeters
    
    shadow_lenght_min_max = calculate_using_min_max(list_of_values)
    shadow_lenght_max_difference = calculate_using_maximum_change(list_of_values)
    shadow_lenght_max_difference_red = calculate_using_maximum_change(list_of_red)
    shadow_lenght_final = (shadow_lenght_max_difference+shadow_lenght_min_max+shadow_lenght_max_difference_red)/3

    difference_of_methods = abs(shadow_lenght_max_difference-shadow_lenght_min_max)
    difference_of_methods = np.round(difference_of_methods,2)

    # calculate distance using said function
    lenght = distance(60, shadow_lenght_final)

    # because original lenghts is not Archimedes-compatible we will have to convert
    angle_final_radians = angle_final*(np.pi/180)
    if angle_final <= 45:
        lenght = lenght/np.cos(angle_final_radians)
    if angle_final > 45:
        lenght = lenght/np.sin(angle_final_radians)

    altitude_radians = altitude*(np.pi/180)
    cloudheight = np.tan(altitude_radians)*lenght
    cloudheight = np.round(cloudheight,2)

    return cloudheight

if __name__ == '__main__':
    cloudheight = calculate_shadow('zchop.meta.x000.y000.n011.jpg', 294,199,270)
    print(cloudheight)