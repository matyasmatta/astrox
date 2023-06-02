# Lint as: python3
# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
r"""Example using PyCoral to detect objects in a given image.
To run this code, you must attach an Edge TPU attached to the host and
install the Edge TPU runtime (`libedgetpu.so`) and `tflite_runtime`. For
device setup instructions, see coral.ai/docs/setup.
Example usage:
```
bash examples/install_requirements.sh detect_image.py
python3 examples/detect_image.py \
  --model test_data/ssd_mobilenet_v2_coco_quant_postprocess_edgetpu.tflite \
  --labels test_data/coco_labels.txt \
  --input test_data/grace_hopper.bmp \
  --output ${HOME}/grace_hopper_processed.bmp
```
"""

import argparse
import time

from PIL import Image
from PIL import ImageDraw

from pycoral.adapters import common
from pycoral.adapters import detect
from pycoral.utils.dataset import read_label_file
from pycoral.utils.edgetpu import make_interpreter
import json
import os

import threading
import time
from time import sleep
import cv2
import numpy as np
from numpy import average 
import statistics
from PIL import Image, ImageStat
from pycoral.adapters import common, detect
from pycoral.utils.edgetpu import make_interpreter
from skyfield import api
from skyfield.api import load
import csv
from csv import writer
from datetime import timedelta, datetime
from pathlib import Path
from exif import Image as exify
import os

class ai:
    def draw_objects(draw, objs, labels):
        count = 0
        for obj in objs:
            bbox = obj.bbox
            draw.rectangle([(bbox.xmin, bbox.ymin), (bbox.xmax, bbox.ymax)],
                        outline='red')
            print(count)
            draw.text((bbox.xmin + 10, bbox.ymin + 10),
                    '%s\n%.2f' % (count, obj.score),
                    fill='red')
            count += 1
    def ai_model(image_path):
        open(r"model\labelmap.txt")
        labels = r'model\labelmap.txt'
        interpreter = make_interpreter(r'model\edgetpu.tflite')
        interpreter.allocate_tensors()

        image = Image.open(image_path)
        _, scale = common.set_resized_input(
            interpreter, image.size, lambda size: image.resize(size, Image.ANTIALIAS))
        print(scale)

        # print('----INFERENCE TIME----')
        # print('Note: The first inference is slow because it includes', 'loading the model into Edge TPU memory.')
        for _ in range(2):
            start = time.perf_counter()
            interpreter.invoke()
            inference_time = time.perf_counter() - start
            objs = detect.get_objects(interpreter, 0, scale)
            print('%.2f ms' % (inference_time * 1000))

        # print('-------RESULTS--------')
        if not objs:
            print('No objects detected')
        counter_for_ai_output = 0
        ai_output = {}
        for obj in objs:
            #print(labels.get(obj.id, obj.id))
            print('  id:    ', obj.id)
            print('  score: ', obj.score)
            print('  bbox:  ', obj.bbox)

            # obj.bbox needs to be converted into a dictionary
            bbox = obj.bbox
            score = obj.score
            ai_output[counter_for_ai_output] = {}
            ai_output[counter_for_ai_output]['xmin'] = bbox.xmin
            ai_output[counter_for_ai_output]['ymin'] = bbox.ymin
            ai_output[counter_for_ai_output]['xmax'] = bbox.xmax
            ai_output[counter_for_ai_output]['ymax'] = bbox.ymax
            ai_output[counter_for_ai_output]['accuracy'] = score

            counter_for_ai_output += 1
        image = image.convert('RGB')
        ai.draw_objects(ImageDraw.Draw(image), objs, labels)
        image.save('grace_hopper_processed.bmp')
        
            
        # image.show()
        if os.path.exists('meta.bmp') == True:
            os.remove('meta.bmp')
        image.save('meta.bmp')

        with open('ai_output.json', 'w', encoding='utf-8') as f:
            json.dump(ai_output, f, ensure_ascii=False, indent=4)
        return ai_output

class shadow:
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

            print(f"Azimuth: {azimuth.degrees:.4f}")
            print(f"Altitude: {altitude.degrees:.4f}")

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

        if angle > 360:
            angle -= 360

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
        sun_altitude_for_limit = shadow.sun_data.altitude("34.28614 S", "147.9849 E", 2022, 1, 15, 5, 16, 5)
        sun_altitude_for_limit_radians = sun_altitude_for_limit*(np.pi/180)
        limit_cloud_height = 7500 #not meters
        limit_shadow_cloud_distance = limit_cloud_height/np.tan(sun_altitude_for_limit_radians)
        limit_shadow_cloud_distance_pixels = limit_shadow_cloud_distance/142
        limit = limit_shadow_cloud_distance_pixels

        # clear the whole txt file
        with open('stiny.txt', 'w') as f:
            f.write("\n")
        with open('stiny_red.txt', 'w') as f:
            f.write("\n")

        if os.path.exists('meta.bmp') == False:
            im2 = im.copy()
            im.save('meta.bmp')

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
        counter_for_loop = 0
        global pixel
        pixel = {}
        while counter_for_loop < limit:
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
            im2 = Image.open('meta.bmp')
            im2.putpixel((x,y),(0,0,0,0))
            im2.save('meta.bmp')
            pixel[counter_for_loop] = {}
            pixel[counter_for_loop]['x'] = x
            pixel[counter_for_loop]['y'] = y
            counter_for_loop += 1


        x_increase_final_abs = abs(x_increase_final)
        y_increase_final_abs = abs(x_increase_final)

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
                # in case that shadow is found before a cloud in the line, we delete the value as its false and repeat
                if shadow_lenght <= 0:
                    list_of_values.remove(cloud_high)
                    shadow_lenght, cloud_high, shadow_low, cloud_location, shadow_location = main()

                    x = pixel[cloud_location]['x']
                    y = pixel[cloud_location]['y']

                    im = Image.open('meta.bmp')
                    im.putpixel((x,y),(255,0,0,0))
                    im.save('meta.bmp')


                    x = pixel[shadow_location]['x']
                    y = pixel[shadow_location]['y']

                    im = Image.open('meta.bmp')
                    im.putpixel((x,y),(0,255,0,0))
                    im.save('meta.bmp')

                    del x
                    del y
                else:
                    break
            return shadow_lenght

        # define a calculation method for cloud-shadow difference (the following one takes the changes in values and their respective min max values)
        def calculate_using_maximum_change(list_of_values):
            def main():
                n = 0
                list_of_changes = []

                # IMPORTANT: please note that this code will return EXCEPTIONS
                # it is NEVER a fatal error and IS HANDLED perfectly fine
                # it was the easiest method as to how to correct for clouds being after shadows (means we detected a different cloud)
                # the code one by one removes pixels that are detected as the brightest and simultaniously are after the shadow (returns negative lenght)
                # done as a loop that will return an error when there are no more objects in the list
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

                # self-explanatory
                shadow_low = max(list_of_changes)
                cloud_high = min(list_of_changes)

                shadow_location = list_of_changes.index(shadow_low)
                cloud_location = list_of_changes.index(cloud_high)

                # find difference between the two pixel lenghts
                shadow_lenght = shadow_location - cloud_location
                return shadow_lenght, cloud_high, cloud_location
            
            # first we calculate
            shadow_lenght, cloud_high, cloud_location = main()

            # then we check for clouds after shadows and if necessary re-run the local main function (see above)
            while True:
                n = 0
                if shadow_lenght <= 0:
                    item_to_be_deleted = list_of_values[cloud_location]
                    list_of_values.remove(item_to_be_deleted)
                    shadow_lenght, cloud_high, cloud_location = main()
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

        altitude = shadow.sun_data.altitude("34.28614 S", "147.9849 E", 2022, 1, 15, 5, 16, 5)
        # calculate final values
        altitude_radians = altitude*(np.pi/180)
        cloudheight = np.tan(altitude_radians)*lenght
        cloudheight = np.round(cloudheight,2)

        # print("Shadow is exactly", cloudheight, "meters from ground!")
        # print(list_of_values)
        return cloudheight
    
    def calculate_cloud_data(counter_for_shadows):
        x_max = data[counter_for_shadows]['xmax']
        y_max = data[counter_for_shadows]['ymax']
        x_min = data[counter_for_shadows]['xmin']
        y_min = data[counter_for_shadows]['ymin']
        x_centre_of_cloud = (x_min+x_max)/2
        y_centre_of_cloud = (y_min+y_max)/2
        x_centre_of_cloud = round(x_centre_of_cloud, 0)
        y_centre_of_cloud = round(y_centre_of_cloud, 0)
        x_centre_of_cloud = int(x_centre_of_cloud)
        y_centre_of_cloud = int(y_centre_of_cloud)
        x_cloud_lenght = abs(x_max - x_min)
        y_cloud_lenght = abs(y_max - y_min)

        return x_centre_of_cloud, y_centre_of_cloud, x_cloud_lenght, y_cloud_lenght

    def calculate_cloud_limit(metadata):
            sun_altitude_for_limit = shadow.sun_data.altitude(metadata['latitude'], metadata['longitude'], metadata['year'], metadata['month'], metadata['day'], metadata['hour'], metadata['minute'], metadata['second'])
            sun_altitude_for_limit_radians = sun_altitude_for_limit*(np.pi/180)
            limit_cloud_height = 12000 #meters
            limit_shadow_cloud_distance = limit_cloud_height/np.tan(sun_altitude_for_limit_radians)
            limit_shadow_cloud_distance_pixels = limit_shadow_cloud_distance/126.48
            limit = limit_shadow_cloud_distance_pixels

class exif_metadata:
        def find_time(path):
            img = Image.open(path)
            img_exif_dict = img.getexif()
            date = str(img_exif_dict[306])
            year = int(date[0:4])
            month = int(date[5:7])
            day = int(date[8:10])
            hour = int(date[11:13])
            minute = int(date[14:16])
            second = int(date[17:19])
            metadata['year'] = year
            metadata['month'] = month
            metadata['day'] = day
            metadata['hour'] = hour
            metadata['minute'] = minute
            metadata['second'] = second
        def find_coordinates(path):
            def get_latitude(image):
                with open(image, 'rb') as image_file:
                    img = exify(image_file)
                    try:
                        latitude = img.get("gps_latitude")
                        latitude_ref = img.get("gps_latitude_ref")
                        if latitude == None:
                            latitude, latitude_ref = (0.0, 0.0, 0.0), "A"
                    except AttributeError:
                        latitude, latitude_ref = (0.0, 0.0, 0.0), "A"
                decimal_degrees = latitude[0] + latitude[1] / 60 + latitude[2] / 3600
                latitude_formatted = str(str(decimal_degrees)+" "+str(latitude_ref))
                return latitude_formatted

            def get_longitude(image):
                with open(image, 'rb') as image_file:
                    img = exify(image_file)
                    try:
                        longitude = img.get("gps_longitude")
                        longitude_ref = img.get("gps_longitude_ref")
                        if longitude == None:
                            longitude, longitude_ref = (0.0, 0.0, 0.0), "A"
                    except AttributeError:
                        longitude, longitude_ref = (0.0, 0.0, 0.0), "A"
                decimal_degrees = longitude[0] + longitude[1] / 60 + longitude[2] / 3600
                longitude_formatted = str(str(decimal_degrees)+" "+longitude_ref)
                return longitude_formatted

            metadata['latitude'] = get_latitude(path)
            metadata['longitude'] = get_longitude(path)

if __name__ == '__main__':
    path = 'data_chop\img_330_x1515_y1010.jpg'
    data = ai.ai_model(path)
    counter_for_shadows = 0
    global metadata
    metadata = {}
    exif_metadata.find_time(path)
    exif_metadata.find_coordinates(path)
    metadata['sun_altitude'] = shadow.sun_data.altitude(metadata['latitude'], metadata['longitude'], metadata['year'], metadata['month'], metadata['day'], metadata['hour'], metadata['minute'], metadata['second'])
    metadata['sun_azimuth'] = shadow.sun_data.azimuth(metadata['latitude'], metadata['longitude'], metadata['year'], metadata['month'], metadata['day'], metadata['hour'], metadata['minute'], metadata['second'])
    while counter_for_shadows < 9:
        try:
            x_centre_of_cloud, y_centre_of_cloud, x_cloud_lenght, y_cloud_lenght = shadow.calculate_cloud_data(counter_for_shadows)
            print(data)
            metadata['shadow_azimuth'] = metadata['sun_azimuth']+236+180
            metadata['shadow_lenght'] = shadow.calculate_shadow(file_path = path, x = x_centre_of_cloud, y = y_centre_of_cloud, angle = metadata['shadow_azimuth'])
            print(metadata['shadow_lenght'])
        except:
            pass
        counter_for_shadows += 1