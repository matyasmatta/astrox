from PIL import Image
import numpy as np
from numpy import average 
from skyfield import api
from skyfield import almanac
import os
import json
import csv
import PIL 
from PIL import ImageEnhance
from PIL import Image
# import the modules
import os
from os import listdir
from PIL import Image

# ignore the 'json' in the name, we replaced the file format with csv for simplicity, jsons are useful for export data - not metadata
def write_pixel_into_json(count, x, y, cloud_id="not specified", image_id="not specified"):
    with open('pixels.csv', 'a') as f:
        writer = csv.writer(f)
        data = [image_id, cloud_id, count, x, y]
        writer.writerow(data)

# define classes
class sun_data:
    def altitude(coordinates_latitude, coordinates_longtitude, year, month, day, hour, minute, second):
        # use the NASA API to be able to calculate sun's position
        ts = api.load.timescale()
        ephem = api.load("ftp://ssd.jpl.nasa.gov/pub/eph/planets/bsp/de421.bsp")

        # define sky objects
        sun = ephem["Sun"]
        earth = ephem["Earth"]

        # define where photo was taken(usually via EXIF data)
        # given coordinates calculate the altitude (how many degrees sun is above the horizon), additional data is redundant
        location = api.Topos(coordinates_latitude, coordinates_longtitude, elevation_m=500)
        sun_pos = (earth + location).at(ts.tt(year,month,day,hour,minute,second)).observe(sun).apparent()
        altitude, azimuth, distance = sun_pos.altaz()

        # print(f"Azimuth: {azimuth.degrees:.4f}")
        # print(f"Altitude: {altitude.degrees:.4f}")

        altitude= float(altitude.degrees)
        return(altitude)
    def azimuth(coordinates_latitude, coordinates_longtitude, year, month, day, hour, minute, second):
        # use the NASA API to be able to calculate sun's position
        ts = api.load.timescale()
        ephem = api.load("ftp://ssd.jpl.nasa.gov/pub/eph/planets/bsp/de421.bsp")

        # define sky objects
        sun = ephem["Sun"]
        earth = ephem["Earth"]

        # define where photo was taken(usually via EXIF data)
        # given coordinates calculate the altitude (how many degrees sun is above the horizon), additional data is redundant
        location = api.Topos(coordinates_latitude, coordinates_longtitude, elevation_m=500)
        sun_pos = (earth + location).at(ts.tt(year,month,day,hour,minute,second)).observe(sun).apparent()
        altitude, azimuth, distance = sun_pos.altaz()

        # print(f"Azimuth: {azimuth.degrees:.4f}")
        # print(f"Altitude: {altitude.degrees:.4f}")

        azimuth= float(azimuth.degrees)
        return(azimuth)

def starting_point_corrector(x_centre, y_centre, x_increase_final, y_increase_final):
    constant_for_starting_point_correction = 10
    x_final = x_centre - constant_for_starting_point_correction*x_increase_final
    y_final = y_centre - constant_for_starting_point_correction*y_increase_final
    x_final = round(x_final, 0)
    x_final = int(x_final)
    y_final = round(y_final, 0)
    y_final = int(y_final)
    return x_final, y_final

def calculate_shadow(file_path, x, y, angle, cloud_id="not specified", image_id="not specified"):
    # open specific cloud
    im = Image.open(file_path) # Can be many different formats.
    pix = im.load()

    # get the width and height of the image for iterating over
    # print(im.size) 
    total_x, total_y = im.size
    total_x -= 1
    total_y -= 1
    # print(total_x, total_y)

    # set coordinates from AI model
    x = x
    y = y
    angle = angle # set the angle (formatted as reduced edoov coefficient) for search, i.e. clockwise


    # calculate meta angle
    angle_radians =np.radians(angle)
    x_increase_meta = np.sin(angle_radians)
    y_increase_meta = np.cos(angle_radians)
    y_increase_meta = -y_increase_meta
    x_increase_meta = np.round(x_increase_meta,5)
    y_increase_meta = np.round(y_increase_meta,5)
    # print(x_increase_meta, y_increase_meta)
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

    # set values for future reference
    ## do not alter the sums or code will break
    y_sum = 0
    x_sum = 0
    count = -1
    ## set how many pixel you want to count via limit manually if you want (since v5 it is calculated automatically)
    # limit = 100
    ## do not alter list_of_values
    list_of_values = []
    list_of_red = []

    # automatic limit calculation (turn off if you want to use manual)
    sun_altitude_for_limit = sun_data.altitude("34.28614 S", "147.9849 E", 2022, 1, 15, 5, 16, 5)
    # print("altitude", sun_altitude_for_limit)
    sun_altitude_for_limit_radians = sun_altitude_for_limit*(np.pi/180)
    limit_cloud_height = 7500 #not meters
    limit_shadow_cloud_distance = limit_cloud_height/np.tan(sun_altitude_for_limit_radians)
    limit_shadow_cloud_distance_pixels = limit_shadow_cloud_distance/142
    limit = limit_shadow_cloud_distance_pixels
    # print("limit", limit)

    # clear the whole txt file
    with open('stiny.txt', 'w') as f:
        f.write("\n")
    with open('stiny_red.txt', 'w') as f:
        f.write("\n")

    if os.path.exists('meta.jpg') == False:
        im2 = im.copy()
        im.save('meta.jpg')

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
        if x > total_x or y > total_y or x == 1 or y == 1:
            break
        
        data = (pix[x,y])
        value = round(average(data))
        value_red = data[0]
        list_of_red.append(value_red)
        list_of_values.append(value)
        im2 = Image.open('meta.jpg')
        im2.putpixel((x,y),(0,0,0,0))
        im2.save('meta.jpg')

    # # print for debugging
    # print(x_increase_final, y_increase_final)
    im2.save('meta.jpg')
    # set absolute final values
    x_increase_final_abs = abs(x_increase_final)
    y_increase_final_abs = abs(x_increase_final)

    # print(list_of_values)
    # define a calculation method for cloud-shadow difference (the following one just takes the min and max values)
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
                # print("př", list_of_values)
                list_of_values.remove(cloud_high)
                shadow_lenght, cloud_high, shadow_low, cloud_location, shadow_location = main()
                # print("When calculating via min max, the shadow resulted being negative, recalculation in progress.")
                # print("po", list_of_values)
            else:
                break
        with open('pixels.csv', "r") as f:
            csv_file = csv.reader(f, delimiter=",")
            for row in csv_file:
                # print(row)
                if not ''.join(row).strip():
                    pass
                else:
                    try:
                        if int(row[1]) == cloud_id and int(row[0]) == image_id and int(row[2]) == shadow_location:
                            x = row[3]
                            y = row[4]
                            x = int(x)
                            y = int(y)
                            im3 = Image.open('meta.jpg')
                            im3.putpixel((x,y),(255,255,255,0))
                            print("found it!", x, y, shadow_location)
                            im3.show()
                            im3.save('meta.jpg')
                            break
                        else:
                            pass
                    except:
                        pass
        with open('pixels.csv', "r") as f:
            csv_file = csv.reader(f, delimiter=",")
            for row in csv_file:
                if not ''.join(row).strip():
                    pass
                else:
                    try:
                        if int(row[1]) == cloud_id and int(row[0]) == image_id and int(row[2]) == cloud_location:
                            x = row[3]
                            y = row[4]
                            x = int(x)
                            y = int(y)
                            im3 = Image.open('meta.jpg')
                            im3.putpixel((x,y),(255,0,0,0))
                            print("found it!", x, y, cloud_location)
                            im3.show()
                            im3.save('meta.jpg')
                            break
                        else:
                            pass
                    except:
                        pass
        # find difference between the two pixel lenghts
        # print("minmax", shadow_lenght)
        return shadow_lenght

    def calculate_using_maximum_change(list_of_values):
        def main():
            n = 0
            list_of_changes = []
            while True:
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

        # find difference between the two pixel lenghts
        # print("minmax", shadow_lenght)
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
    # print("Difference between the two methods of cloud-shadow calculation is", difference_of_methods)

    # calculate distance using said function
    lenght = distance(60, shadow_lenght_final)

    # because original lenghts is not Archimedes-compatible we will have to convert
    # print("angle", angle_final)
    angle_final_radians = angle_final*(np.pi/180)
    # print("lenght", lenght)
    if angle_final <= 45:
        lenght = lenght/np.cos(angle_final_radians)
    if angle_final > 45:
        lenght = lenght/np.sin(angle_final_radians)
    # print("lenght2", lenght)

    # print("Shadow is exactly", lenght, "meters from the cloud!")

    altitude = sun_data.altitude("34.28614 S", "147.9849 E", 2022, 1, 15, 5, 16, 5)
    # calculate final values
    altitude_radians = altitude*(np.pi/180)
    cloudheight = np.tan(altitude_radians)*lenght
    cloudheight = np.round(cloudheight,2)

    # print("Shadow is exactly", cloudheight, "meters from ground!")
    # print(list_of_values)
    return cloudheight

class app:
    photoID = 0
    def
    # get the path or directory
    folder_dir = r"C:\Users\kiv\Documents\GitHub\astrox\dataset\sample_original"
    for images in os.listdir(folder_dir):
        photoID += 1
        # check if the image ends with png or jpg or jpeg
        if (images.endswith(".png") or images.endswith(".jpg")\
            or images.endswith(".jpeg")):
            # display
            print(images)
            # Opens a image in RGB mode
            im = Image.open("./dataset/original/" + images)
            left = 1075
            top = 520
            right = 3015
            bottom = 2460
            # Cropped image of above dimension
            # (It will not change original image)
            im1 = im.crop((left, top, right, bottom))
            # Shows the image in image viewer
            im1.save('meta.bmp')
            # Slice
            infile = 'meta.jpg'
            chopsize = 485

            img = Image.open(infile)
            width, height = img.size

            # Metadata
            image = Image.open('./dataset/original/51844762822_3b10505c80_o.jpg')
            exif = image.info['exif']

            # Save Chops of original image
            for x0 in range(0, width, chopsize):
                for y0 in range(0, height, chopsize):
                    box = (x0, y0,
                            x0+chopsize if x0+chopsize <  width else  width - 1,
                            y0+chopsize if y0+chopsize < height else height - 1)
                    print('%s %s' % (infile, box))
                    img.crop(box).save('./dataset/crop/zchop.%s.x%03d.y%03d.n%03d.jpg' % (infile.replace('.jpg',''), x0, y0, int(photoID)),exif=exif)



if __name__ == '__main__':
    cloudheight = calculate_shadow('zchop.meta.x000.y000.n011.jpg', 294,199,360)
    print(cloudheight)