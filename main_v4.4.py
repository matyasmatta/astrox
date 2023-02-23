# first version to include two threads
# for further file history see main_old (version 1.0 to 4.4)
import threading
import time
import cv2
import math
import numpy as np
import statistics
from time import sleep
import statistics
import argparse
import time
from PIL import Image
from PIL import ImageDraw
from PIL import ImageStat
from pycoral.adapters import common
from pycoral.adapters import detect
from pycoral.utils.dataset import read_label_file
from pycoral.utils.edgetpu import make_interpreter
import json
import os
from numpy import average 
from skyfield import api
from skyfield import almanac
import csv
from sense_hat import SenseHat
from datetime import timedelta, datetime
from orbit import ISS, ephemeris
from skyfield.api import load
from csv import writer
from pathlib import Path
from picamera import PiCamera
from orbit import ISS
from exif import Image as exify
import os
from os import listdir
import threading

# classes for functions
class gps:
    def cloud_position(chop_image_path): #centerCoordinates and cloudCoordinates in xxx.xx, xxx.xx format
        #input of values
        meridionalCircumference = 40008
        earthCircumference = 40075
        k = 0.12648                                                                           #constant for converting pixels to km

        # finds pixel distance delta
        txt = chop_image_path
        x = txt.split("_")
        chopCoordinatesX = x[2]
        chopCoordinatesY = x[3]      
        distanceX = (float(chopCoordinatesX) - float(970)) * k                                  #location of cloud - center location (x axis)
        distanceY = (float(chopCoordinatesY) - float(970)) * k                                  #location of cloud - center location (y axis)

        #finds latitude of the cloud
        splitLatitude, cardinalDirection = latitude.split()
        if cardinalDirection == "N":
            dec_latitude = float(splitLatitude)
        else:
            dec_latitude = - float(splitLatitude)
        
        splitLongitude, cardinalDirection = longitude.split()
        if cardinalDirection == "E":
            dec_longitude = float(splitLongitude)
        else:
            dec_longitude = - float(splitLongitude)

        chopLatitude = float(dec_latitude) + (distanceY*360)/meridionalCircumference
        print("z. š.:", chopLatitude)

        # find longitude of the cloud
        chopLongitude = float(dec_longitude) + (distanceX*360)/(earthCircumference*np.cos(chopLatitude * (np.pi/180)))
        print("z. d.:", chopLongitude)
        return(chopLatitude, chopLongitude)
    def convert_decimal_coordinates_to_legacy(latitude, longitude):
        # conversion of degrees specifically for an gps class friendly format
        def conversion(coordinates):
            coordinates = float(coordinates)
            coordinates = abs(coordinates)
            degrees = coordinates//1
            minutes = ((coordinates - coordinates//1)*60)//1
            seconds = round(((((coordinates - coordinates//1)*60) - minutes//1)*60),5)

            list = [degrees, minutes, seconds]
            data = tuple(list)

            return data

        latitude_data = conversion(latitude)
        longitude_data = conversion(longitude)

        if float(latitude) >= 0:
            latitude_ref = "N"
        else:
            latitude_ref = "S"

        if float(longitude) >= 0:
            longitude_ref = "E"
        else:
            longitude_ref = "W"

        return latitude_data, latitude_ref, longitude_data, longitude_ref        
class list:
    # used for calculating north, sets some simple statistics functions
    global store_edoov_coefficient
    store_edoov_coefficient = []
    def get_median():
        return statistics.median(store_edoov_coefficient)
    def add_edoov_coefficient(item):
        store_edoov_coefficient.append(item)
    def get_list():
        return store_edoov_coefficient
class north:
    def find_edoov_coefficient(image_1, image_2):

        # converting images to cv friendly readable format 
        def convert_to_cv(image_1, image_2):
            image_1_cv = cv2.imread(image_1, 0)
            image_2_cv = cv2.imread(image_2, 0)
            return image_1_cv, image_2_cv

        # finding same "things" on both images
        def calculate_features(image_1, image_2, feature_number):
            orb = cv2.ORB_create(nfeatures = feature_number)
            keypoints_1, descriptors_1 = orb.detectAndCompute(image_1_cv, None)
            keypoints_2, descriptors_2 = orb.detectAndCompute(image_2_cv, None)
            return keypoints_1, keypoints_2, descriptors_1, descriptors_2

        # connecting same "things" on photo
        def calculate_matches(descriptors_1, descriptors_2):
            try:
                brute_force = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
                matches = brute_force.match(descriptors_1, descriptors_2)
                matches = sorted(matches, key=lambda x: x.distance)
                return matches
            except:
                return 0

        # finding coordination of same "things" on both fotos
        def find_matching_coordinates(keypoints_1, keypoints_2, matches):
            global x_1all_div
            global x_2all_div
            global y_1all_div
            global y_2all_div
            x_11all= []
            x_22all= []
            y_11all= []
            y_22all= []
            for match in matches:
                image_1_idx = match.queryIdx
                image_2_idx = match.trainIdx
                (x1,y1) = keypoints_1[image_1_idx].pt
                (x2,y2) = keypoints_2[image_2_idx].pt
                # we store all matched coordinates to list for further calculation
                x_11all.append(x1)
                x_22all.append(x2)
                y_11all.append(y1)
                y_22all.append(y2)
            # this calculates us the median of all coordinations on output [x1, y1] and [x2,y2]

            try:
                x_11all_div=statistics.median(x_11all)
                x_22all_div=statistics.median(x_22all)
                y_11all_div=statistics.median(y_11all)
                y_22all_div=statistics.median(y_22all)
            except:
                x_11all_div=0
                x_22all_div=0
                y_11all_div=0
                y_22all_div=0

            # we calculate the angle of movemment of "things" on photo
            delta_x = x_22all_div - x_11all_div
            delta_y = y_11all_div - y_22all_div
            
            edoov_coefficient = np.arctan2(delta_x,delta_y) * 57.29577951 + 180
            if edoov_coefficient >= 360:
                edoov_coefficient=edoov_coefficient-360
            return edoov_coefficient

        # using defined functions
        image_1_cv, image_2_cv = convert_to_cv(image_1, image_2) 
        keypoints_1, keypoints_2, descriptors_1, descriptors_2 = calculate_features(image_1_cv, image_2_cv, 1000) 
        matches = calculate_matches(descriptors_1, descriptors_2)
        edoov_coefficient = find_matching_coordinates(keypoints_1,keypoints_2,matches)
        # calculating the relative rotation of camera on ISS
              
        list.add_edoov_coefficient(edoov_coefficient)
        list_medianu = list.get_median()
        return list_medianu
        
    def find_north_fast(image_1, image_2):
        def get_latitude(image):
            with open(image, 'rb') as image_file:
                img = exify(image_file)
                if img.has_exif:
                    try:
                        latitude = img.get("gps_latitude")
                        latitude_ref = img.get("gps_latitude_ref")
                        if latitude == None:
                            latitude, latitude_ref = (0.0, 0.0, 0.0), "A"
                    except AttributeError:
                        latitude, latitude_ref = (0.0, 0.0, 0.0), "A"
                else:
                    latitude, latitude_ref = (0.0, 0.0, 0.0), "A"
            return latitude, latitude_ref
        
        # converting latitude to decimal
        def get_decimal_latitude(latitude, latitude_ref):
            decimal_degrees = latitude[0] + latitude[1] / 60 + latitude[2] / 3600
            if latitude_ref == "S":
                decimal_degrees = -decimal_degrees
            return decimal_degrees

        # getting latitude for using
        def get_latitudes(image_1, image_2):    
            latitude_image_1_x, latitude_image_1_ref = get_latitude(image_1)
            latitude_image_1 = get_decimal_latitude(latitude_image_1_x, latitude_image_1_ref)
            latitude_image_2_x, latitude_image_2_ref = get_latitude(image_2)
            latitude_image_2 = get_decimal_latitude(latitude_image_2_x, latitude_image_2_ref)
            return latitude_image_1, latitude_image_2

        # using defined functions
        latitude_image_1, latitude_image_2 = get_latitudes(image_1, image_2)
        # averaging latitudes for more accurate calculation 
        latitude_avg = (latitude_image_1+latitude_image_2)/2

        # calculating the relative position of north for ISS (looks forward)
        alpha_k=np.arcsin(np.cos(51.8/57.29577951)/np.cos(latitude_avg/57.29577951)) * 57.29577951
        corrected_alpha_k=0
        if latitude_image_1>latitude_image_2:
            corrected_alpha_k=180-alpha_k
        else:
            corrected_alpha_k=alpha_k
        
        # combinating both informations to get real position of north on photo
        poloha_severu = all_edoov_coefficient - corrected_alpha_k
        print("all edoov koeficient:", all_edoov_coefficient)
        if poloha_severu < 0:
            poloha_severu = poloha_severu + 360
        return poloha_severu
class ai:
    # this is the class that works with the model itself
    def ai_model(image_path):
        open("./model/labelmap.txt")
        labels = './model/labelmap.txt'
        interpreter = make_interpreter('./model/edgetpu.tflite')
        interpreter.allocate_tensors()

        image = Image.open(image_path)
        _, scale = common.set_resized_input(
            interpreter, image.size, lambda size: image.resize(size, Image.ANTIALIAS))

        # inferencing
        for _ in range(2):
            start = time.perf_counter()
            interpreter.invoke()
            inference_time = time.perf_counter() - start
            objs = detect.get_objects(interpreter, 0, scale)

        # appending onto a list
        counter_for_ai_output = 0
        ai_output = {}
        for obj in objs:
            if obj.score > 0.25:
                #print(labels.get(obj.id, obj.id))
                print('  id:    ', counter_for_ai_output)
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
            else:
                pass
            counter_for_ai_output += 1
        image = image.convert('RGB')
        
        # saving into an image
        if os.path.exists('meta.jpg') == True:
            os.remove('meta.jpg')
        image.save('meta.jpg')
        return ai_output
class shadow:
    # this is a big class containing all things necessary to calculate the lenght of a shadow from data generated by the ai model

    # this function is used as for printing data (first used withing shadow so for legacy kept here)
    def print_log(data):
        with open('log.txt', 'a') as f:
            f.write(data)
            f.write("\n")

    # this class gets coordinates from EXIF and converts them into a more friendly decimal format (not to be confused with photo.convert())
    class coordinates:
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

    # here simply centres and lenghts of clouds are calculated, lenghts are further on used to remove too long objects and centres are used for shadow detection
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

    # here we define a subclass containing all we need to calculate sun data, i.e. altitude and azimuth, both can be triggered separately
    class sun_data:
        def altitude(coordinates_latitude, coordinates_longtitude, year, month, day, hour, minute, second):
            # use the NASA API to be able to calculate sun's position
            ts = api.load.timescale()
            ephem = api.load("ftp://ssd.jpl.nasa.gov/pub/eph/planets/bsp/de421.bsp")

            # define sky objects
            sun = ephem["Sun"]
            earth = ephem["Earth"]

            # given coordinates calculate the altitude (how many degrees sun is above the horizon), additional data is redundant
            location = api.Topos(coordinates_latitude, coordinates_longtitude, elevation_m=500)
            sun_pos = (earth + location).at(ts.tt(year,month,day,hour,minute,second)).observe(sun).apparent()
            altitude, azimuth, distance = sun_pos.altaz()
            altitude= float(altitude.degrees)
            return(altitude)
        def azimuth(coordinates_latitude, coordinates_longtitude, year, month, day, hour, minute, second):
            # use the NASA API to be able to calculate sun's position
            ts = api.load.timescale()
            ephem = api.load("ftp://ssd.jpl.nasa.gov/pub/eph/planets/bsp/de421.bsp")

            # define sky objects
            sun = ephem["Sun"]
            earth = ephem["Earth"]

            # given coordinates calculate the altitude (how many degrees sun is above the horizon), additional data is redundant
            location = api.Topos(coordinates_latitude, coordinates_longtitude, elevation_m=500)
            sun_pos = (earth + location).at(ts.tt(year,month,day,hour,minute,second)).observe(sun).apparent()
            altitude, azimuth, distance = sun_pos.altaz()
            azimuth= float(azimuth.degrees)
            return(azimuth)

    # because the brightest point needn't be the centre we ofset the starting pixel by a number defined partially by a constant 
    def starting_point_corrector(x_centre, y_centre, x_increase_final, y_increase_final):
        constant_for_starting_point_correction = 10
        x_final = x_centre - constant_for_starting_point_correction*x_increase_final
        y_final = y_centre - constant_for_starting_point_correction*y_increase_final
        x_final = round(x_final, 0)
        x_final = int(x_final)
        y_final = round(y_final, 0)
        y_final = int(y_final)
        return x_final, y_final
    
    # here we calculate the angle used to seatch for shadows (it is mostly just formatting now as of v4.4)
    def calculate_angle_for_shadow(latitude, longitude, year, month, day, hour=0, minute=0, second=0):
        azimuth = shadow.sun_data.azimuth(latitude, longitude, year, month, day, hour, minute, second)
        total_angle = azimuth + 180
        while total_angle >= 360:
            total_angle -= 360
        return total_angle

    # this is the most important function of the whole class, it calculates cloud height knowing only coordinates
    # we use robust error handling to make sure the function does not cause a fatal error, it is a very complicated function
    def calculate_shadow(x, y, angle, cloud_id="not specified", image_id="not specified", file_path="not specified", image_direct="not specified"):
        try:
            # open specific cloud
            if file_path != "not specified":
                im = Image.open(file_path) # Can be many different formats.
                if image_direct != "not specified":
                    im = image_direct
                pix = im.load()
            else:
                raise Exception("There was an error during initial loading for shadow calculation")


            # get the width and height of the image for iterating over
            total_x, total_y = im.size

            # the next lines of code are very complex, but the method is as follows
            # 1) we need to find "how does x increase in regards to y and vice versa?"
            # 2) we need that either x or y are set as a constant 1 whereas the other is used as addition to a sum
            # 3) when the sum overflows we move a pixel in the less significant direction
            # because of comparasions we need to work with absolute values, basic angles and sectors
            # we are aware that there might be a simpler solution but this is the only one we found consistent and fairly fast

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

            # set absolute final values
            x_increase_final_abs = abs(x_increase_final)
            y_increase_final_abs = abs(y_increase_final)

            # set values for future reference
            y_sum = 0
            x_sum = 0
            count = -1
            list_of_values = []
            list_of_red = []

            # automatic limit calculation
            # here we set basically how far we should search for shadows
            sun_altitude_for_limit = shadow.sun_data.altitude(latitude, longitude, year, month, day, hour, minute, second)
            sun_altitude_for_limit_radians = sun_altitude_for_limit*(np.pi/180)
            limit_cloud_height = 15000 #meters
            limit_shadow_cloud_distance = limit_cloud_height/np.tan(sun_altitude_for_limit_radians)
            limit_shadow_cloud_distance_pixels = limit_shadow_cloud_distance/126.48
            limit = limit_shadow_cloud_distance_pixels

            # we create meta.jpg for testing
            if os.path.exists('meta.jpg') == False:
                im2 = im.copy()
                im.save('meta.jpg')

            # put quarter information back for pixel reading
            ## first two lines are used for limit setting
            ## please note that explanation for all quarters are very similar to quarter 1, hence please excuse that we did not write the documentation for every sector
            if q == 1:

                # set increase with correct signage
                x_increase_final = x_increase_final
                y_increase_final = -y_increase_final

                # correct the starting point
                x,y = shadow.starting_point_corrector(x,y, x_increase_final, y_increase_final)
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

                        # save the value, also search in only red spectrum
                        value = round(average(data))
                        value_red = data[0]

                        # append onto a list
                        list_of_red.append(value_red)
                        list_of_values.append(value)

                        # edit the meta image for checking
                        im2 = Image.open('meta.jpg')
                        im2.putpixel((x,y),(0,0,0,0))
                        im2.save('meta.jpg')

                        # add to y_sum and move pixel x for 1
                        x += 1
                        y_sum += y_increase_final_abs
                        if x > total_x or y > total_y:
                            break
                    if x_increase_final_abs == y_increase_final_abs:               
                        data = (pix[x,y])
                        value = round(average(data))
                        value_red = data[0]
                        list_of_red.append(value_red)
                        list_of_values.append(value)
                        im2 = Image.open('meta.jpg')
                        im2.putpixel((x,y),(0,0,0,0))
                        im2.save('meta.jpg')
                        x += 1
                        y -= 1
                        if x > total_x or y > total_y:
                            break
                    if x_increase_final_abs < y_increase_final_abs:               
                        x_sum = abs(x_sum)
                        if x_sum >= 1:
                            x_sum -= 1
                            x += 1
                        data = (pix[x,y])
                        value = round(average(data))
                        value_red = data[0]
                        list_of_red.append(value_red)
                        list_of_values.append(value)
                        im2 = Image.open('meta.jpg')
                        im2.putpixel((x,y),(0,0,0,0))
                        im2.save('meta.jpg')
                        y -= 1
                        x_sum += x_increase_final_abs
                        if x > total_x or y > total_y:
                            break
                    if count > limit:
                        break
            if q == 2:
                x_increase_final = x_increase_final
                y_increase_final = y_increase_final  
                x,y = shadow.starting_point_corrector(x,y, x_increase_final, y_increase_final) 
                while True:
                    count += 1
                    if x_increase_final_abs > y_increase_final_abs:        
                        y_sum = abs(y_sum)
                        if y_sum >= 1:
                            y_sum -= 1
                            y += 1
                        data = (pix[x,y])
                        value = round(average(data))
                        value_red = data[0]
                        list_of_red.append(value_red)
                        list_of_values.append(value)
                        im2 = Image.open('meta.jpg')
                        im2.putpixel((x,y),(0,0,0,0))
                        im2.save('meta.jpg')
                        x += 1
                        y_sum += y_increase_final_abs
                        if x > total_x or y > total_y:
                            break
                    if x_increase_final_abs == y_increase_final_abs:          
                        data = (pix[x,y])
                        value = round(average(data))
                        value_red = data[0]
                        list_of_red.append(value_red)
                        list_of_values.append(value)
                        im2 = Image.open('meta.jpg')
                        im2.putpixel((x,y),(0,0,0,0))
                        im2.save('meta.jpg')
                        x += 1
                        y += 1
                        if x > total_x or y > total_y:
                            break
                    if x_increase_final_abs < y_increase_final_abs:   
                        x_sum = abs(x_sum)
                        if x_sum >= 1:
                            x_sum -= 1
                            x += 1
                        data = (pix[x,y])
                        value = round(average(data))
                        value_red = data[0]
                        list_of_red.append(value_red)
                        list_of_values.append(value)
                        im2 = Image.open('meta.jpg')
                        im2.putpixel((x,y),(0,0,0,0))
                        im2.save('meta.jpg')
                        y += 1
                        x_sum += x_increase_final_abs
                        if x > total_x or y > total_y:
                            break
                    if count > limit:
                        break
            if q == 3:
                x_increase_final = -x_increase_final
                y_increase_final = y_increase_final 
                x,y = shadow.starting_point_corrector(x,y, x_increase_final, y_increase_final)
                while True:
                    count += 1
                    if x_increase_final_abs > y_increase_final_abs:
                        y_sum = abs(y_sum)
                        if y_sum >= 1:
                            y_sum -= 1
                            y += 1
                        data = (pix[x,y])
                        value = round(average(data))
                        value_red = data[0]
                        list_of_red.append(value_red)
                        list_of_values.append(value)
                        im2 = Image.open('meta.jpg')
                        im2.putpixel((x,y),(0,0,0,0))
                        im2.save('meta.jpg')
                        x -= 1
                        y_sum += y_increase_final_abs
                        if x > total_x or y > total_y:
                            break
                    if x_increase_final_abs == y_increase_final_abs:
                        data = (pix[x,y])
                        value = round(average(data))
                        value_red = data[0]
                        list_of_red.append(value_red)
                        list_of_values.append(value)
                        im2 = Image.open('meta.jpg')
                        im2.putpixel((x,y),(0,0,0,0))
                        im2.save('meta.jpg')
                        x -= 1
                        y += 1
                        if x > total_x or y > total_y:
                            break
                    if x_increase_final_abs < y_increase_final_abs:
                        x_sum = abs(x_sum)
                        if x_sum >= 1:
                            x_sum -= 1
                            x -= 1
                        data = (pix[x,y])
                        value = round(average(data))
                        value_red = data[0]
                        list_of_red.append(value_red)
                        list_of_values.append(value)
                        im2 = Image.open('meta.jpg')
                        im2.putpixel((x,y),(0,0,0,0))
                        im2.save('meta.jpg')
                        y += 1
                        x_sum += x_increase_final_abs
                        if x > total_x or y > total_y:
                            break
                    if count > limit:
                        break
            if q == 4:
                x_increase_final = -x_increase_final
                y_increase_final = -y_increase_final 
                x,y = shadow.starting_point_corrector(x,y, x_increase_final, y_increase_final)
                while True:
                    count += 1
                    if x_increase_final_abs > y_increase_final_abs:
                        y_sum = abs(y_sum)
                        if y_sum >= 1:
                            y_sum -= 1
                            y -= 1
                        data = (pix[x,y])
                        value = round(average(data))
                        value_red = data[0]
                        list_of_red.append(value_red)
                        list_of_values.append(value)
                        im2 = Image.open('meta.jpg')
                        im2.putpixel((x,y),(0,0,0,0))
                        im2.save('meta.jpg')
                        x -= 1
                        y_sum += y_increase_final_abs
                        if x > total_x or y > total_y:
                            break
                    if x_increase_final_abs == y_increase_final_abs:
                        data = (pix[x,y])
                        value = round(average(data))
                        value_red = data[0]
                        list_of_red.append(value_red)
                        list_of_values.append(value)
                        im2 = Image.open('meta.jpg')
                        im2.putpixel((x,y),(0,0,0,0))
                        im2.save('meta.jpg')
                        x -= 1
                        y -= 1
                        if x > total_x or y > total_y:
                            break
                    if x_increase_final_abs < y_increase_final_abs:
                        x_sum = abs(x_sum)
                        if x_sum >= 1:
                            x_sum -= 1
                            x -= 1
                        data = (pix[x,y])
                        value = round(average(data))
                        value_red = data[0]
                        list_of_red.append(value_red)
                        list_of_values.append(value)
                        im2 = Image.open('meta.jpg')
                        im2.putpixel((x,y),(0,0,0,0))
                        im2.save('meta.jpg')
                        y -= 1
                        x_sum += x_increase_final_abs
                        if x > total_x or y > total_y:
                            break
                    if count > limit:
                        break
            # set absolute final values
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
                    else:
                        break
                return shadow_lenght

            # define a calculation method for cloud-shadow difference (the following one takes the changes in values and their respective min max values)
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
                    return shadow_lenght, cloud_high, cloud_location
                shadow_lenght, cloud_high, cloud_location = main()
                while True:
                    n = 0
                    if shadow_lenght <= 0:
                        item_to_be_deleted = list_of_values[cloud_location]
                        list_of_values.remove(item_to_be_deleted)
                        shadow_lenght, cloud_high, cloud_location = main()
                    else:
                        break

                return shadow_lenght

            # here we calculate the shadow-cloud distance by each respective method
            shadow_lenght_min_max = calculate_using_min_max(list_of_values)
            shadow_lenght_max_difference = calculate_using_maximum_change(list_of_values)
            shadow_lenght_max_difference_red = calculate_using_maximum_change(list_of_red)

            # we put the methods together
            shadow_lenght_final = (shadow_lenght_max_difference+shadow_lenght_min_max+shadow_lenght_max_difference_red)/3

            # calculate distance based on a distance in pixels
            lenght = int(shadow_lenght_final) * 126.48

            # because original lenghts are adjacent lenghts and not hypotenuse we will have to convert
            angle_final_radians = angle_final*(np.pi/180)
            if angle_final <= 45:
                lenght = lenght/np.cos(angle_final_radians)
            if angle_final > 45:
                lenght = lenght/np.sin(angle_final_radians)

            # now we calculate the sun altitude using a function
            altitude = shadow.sun_data.altitude(latitude, longitude, year, month, day, hour, minute, second)

            # calculate final values
            altitude_radians = altitude*(np.pi/180)
            cloudheight = np.tan(altitude_radians)*lenght
            cloudheight = np.round(cloudheight,2)
        except:
            # sometimes the AI models returns negative integers, these break the code and are difficult to protect against
            # so in case of an error we pass it to the outer function as well and make sure that the whole shadow process does not crash
            cloudheight = "error"
        return cloudheight    
class photo:
    # this is a small class containing a legacy method needed to convert angle into a special format used later
    def convert(angle):
        sign, degrees, minutes, seconds = angle.signed_dms()
        exif_angle = f'{degrees:.0f}/1,{minutes:.0f}/1,{seconds*10:.0f}/10'
        return sign < 0, exif_angle
class split:
    # this is a small class containing a method for cropping, chopping and rotating the original image into images that can be fed directly to the AI model
    def file_split(image_id, image_path, north_main):
        # check if the image ends with png or jpg or jpeg
        if (image_path.endswith(".png") or image_path.endswith(".jpg") or image_path.endswith(".jpeg")):
            # open
            im = Image.open(image_path)

            # rotate
            im = im.rotate(north_main)

            # crop
            left = 1075
            top = 520
            right = 3015
            bottom = 2460
            im1 = im.crop((left, top, right, bottom))
            
            # save as metadatum
            im1.save('meta.jpg')
            
            # chop definition
            infile = 'meta.jpg'
            chopsize = 485
            img = Image.open(infile)
            width, height = img.size

            # exif metadata
            image = Image.open(image_path)
            exif = image.info['exif']

            # save Chops of original image
            within_loop_counter = 0
            for x0 in range(0, width, chopsize):
                for y0 in range(0, height, chopsize):
                    box = (x0, y0,
                            x0+chopsize if x0+chopsize <  width else  width - 1,
                            y0+chopsize if y0+chopsize < height else height - 1)
                    file_name = "./chop/astrochop_" + str(within_loop_counter) + "_" + str(x0) + "_" + str(y0) + "_" + ".jpg"
                    print(file_name)
                    img.crop(box).save(file_name,exif=exif)

                    # we calculate the centre coordinates of the chop based on its name and original exif data
                    chop_latitude, chop_longitude = gps.cloud_position(file_name)
                    latitude, latitude_ref, longitude, longitude_ref = gps.convert_decimal_coordinates_to_legacy(chop_latitude, chop_longitude)

                    # modify metadate to include more accurate coordinates (i.e. for the center of the chop - not the centre of the whole imaeg)
                    image = exify(file_name)
                    del image.gps_latitude
                    del image.gps_longitude
                    image.gps_latitude = latitude
                    image.gps_latitude_ref = latitude_ref
                    image.gps_longitude = longitude
                    image.gps_longitude_ref = longitude_ref

                    print(latitude, longitude, chop_latitude, chop_longitude)

                    with open(file_name, 'wb') as new_image_file:
                        new_image_file.write(image.get_file())
                    within_loop_counter += 1
            del exif
class properties:
    # this is a small class containing methods for raw checking the quality of imagery
    def calculate_brightness(img_path):
        im = Image.open(img_path).convert('L')
        stat = ImageStat.Stat(im)
        return stat.rms[0]
    def calculate_contrast(img_path):
        img=cv2.imread(img_path)
        img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        contrast = img_grey.std()
        return contrast
class exifmeta:
    # this is a small class containing a method for date extraction that is not via the EXIF library but the PIL library
    def find_time_from_image(image_path):
        img = Image.open(image_path)
        img_exif_dict = img.getexif()
        date = str(img_exif_dict[306])
        global year
        global month
        global day
        global hour
        global minute
        global second
        year = int(date[0:4])
        month = int(date[5:7])
        day = int(date[8:10])
        hour = int(date[11:13])
        minute = int(date[14:16])
        second = int(date[17:19])

        return year, month, day, hour, minute, second
# classes for threads
class photo_thread(threading.Thread):
    # this thread, called "photo" or "auxiliary", is used as a simple data collecting thread, it takes photos and collects sense-hat data

    # we must make sure that initialization of each thread is done well
    def __init__(self, threadId, name, count):
        threading.Thread.__init__(self)

        # we set threadID
        self.threadId = threadId
        
        # we set thread-name
        self.name = name
        
    # this is the main process that will take photos in a loop
    def run(self):
        
        # we print into log.txt when we start a thread
        to_print = "Starting: " + self.name
        shadow.print_log(to_print)

        # first we initialize the process
        base_folder = Path(__file__).parent.resolve()
        data_file = base_folder / "data.csv"
        sense = SenseHat()
        sense.color.gain = 60
        sense.color.integration_cycles = 64
        start_time = datetime.now()
        count_for_images_day = 0
        count_for_images_night = 0
        
        with open('data.csv', 'w', buffering=1, newline='') as f:
            data_writer = writer(f)
            data_writer.writerow(['temp', 'pres', 'hum',
                                'red', 'green', 'blue', 'clear', #only for Sense HAT version 2
                                'yaw', 'pitch', 'roll',
                                'mag_x', 'mag_y', 'mag_z',
                                'acc_x', 'acc_y', 'acc_z',
                                'gyro_x', 'gyro_y', 'gyro_z',
                                'datetime'])

        while (datetime.now() < start_time + timedelta(minutes = 15)):
            timescale = load.timescale()
            t = timescale.now()
            if ISS.at(t).is_sunlit(ephemeris):
                imageName = str("./main/img_" + str(count_for_images_day) + ".jpg")
                count_for_images_day += 1
                photo_sleep_interval = 14

            else:
                imageName = str("./main/night_img_" + str(count_for_images_night) + ".jpg")
                count_for_images_night += 1
                photo_sleep_interval = 59
            location = ISS.coordinates()
            # Convert the latitude and longitude to EXIF-appropriate representations
            south, exif_latitude = photo.convert(location.latitude)
            west, exif_longitude = photo.convert(location.longitude)
            # Set the EXIF tags specifying the current location
            camera.exif_tags['GPS.GPSLatitude'] = exif_latitude
            camera.exif_tags['GPS.GPSLatitudeRef'] = "S" if south else "N"
            camera.exif_tags['GPS.GPSLongitude'] = exif_longitude
            camera.exif_tags['GPS.GPSLongitudeRef'] = "W" if west else "E"
            camera.capture(imageName)     
            sleep(photo_sleep_interval)
            del imageName   
            
            # we will also collect sense data just to collect as much as possible
            sense_data = []
            # Get environmental data
            sense_data.append(sense.get_temperature())
            sense_data.append(sense.get_pressure())
            sense_data.append(sense.get_humidity())
            # Get colour sensor data (version 2 Sense HAT only)
            red, green, blue, clear = sense.colour.colour
            sense_data.append(red)
            sense_data.append(green)
            sense_data.append(blue)
            sense_data.append(clear)
            # Get orientation data
            orientation = sense.get_orientation()
            sense_data.append(orientation["yaw"])
            sense_data.append(orientation["pitch"])
            sense_data.append(orientation["roll"])
            # Get compass data
            mag = sense.get_compass_raw()
            sense_data.append(mag["x"])
            sense_data.append(mag["y"])
            sense_data.append(mag["z"])
            # Get accelerometer data
            acc = sense.get_accelerometer_raw()
            sense_data.append(acc["x"])
            sense_data.append(acc["y"])
            sense_data.append(acc["z"])
            #Get gyroscope data
            gyro = sense.get_gyroscope_raw()
            sense_data.append(gyro["x"])
            sense_data.append(gyro["y"])
            sense_data.append(gyro["z"])
            sense_data.append(datetime.now())
            
            # all the data is written into a csv file
            with open("data.csv", "a", newline="") as f:
                data_writer = writer(f)
                data_writer.writerow(sense_data)  
        
        # when exiting a branch we make sure to write it into the log
        to_print = "Exiting: " + str(self.name)
        shadow.print_log(to_print)
class processing_thread(threading.Thread):
    # this thread is the main processing one, it calculated all things necessary to calculate the cloud height, id est calculates north, runs AI models and does the math
    # we must make sure that initialization of each thread is done well
    def __init__(self, threadId, name, count):
        threading.Thread.__init__(self)
        self.threadId = threadId
        self.name = name
        self.count = count
        
    def run(self):
        def main_processing():
            try:
                # first define all functions neccessary for operation and calibrate the camera
                # pre-initialization
                try:
                    start_time =  datetime.now()
                    global initialization_count
                    initialization_count = 1  
                except:
                    to_print = str("There was an error during pre-initialization")
                    shadow.print_log(to_print)
                # initialise and calibrate the north data via north class
                # initialization
                try:
                    while (datetime.now() < start_time + timedelta(seconds=100)):
                        i_1=str(initialization_count)
                        before = "./datasetlow/image ("
                        image_1=str(before + i_1 +").jpg")
                        i_2=str(initialization_count+1)
                        image_2=str(before + i_2 +").jpg")
                        list_medianu = north.find_edoov_coefficient(image_1, image_2)
                        initialization_count += 1
                        print("Edoov koeficient was defined at", list_medianu, "counted clockwise.")
                        global all_edoov_coefficient
                        all_edoov_coefficient = list_medianu
                except:
                    to_print = str("There was an error during the initialzitation")
                    shadow.print_log(to_print)

                # run the actual main code
                # main runtime
                try:
                    # first we reset the count
                    initialization_count = 1
                    image_1_path = str("./datasetlow/image (" + str(initialization_count) + ").jpg")
                    initialization_count +=1

                    # this id is what we will see in the final csv file
                    full_image_id = 0

                    # the following is the main loop which will run for the majority of time on the ISS, the condition is so that it does not run for too long
                    while (datetime.now() < start_time + timedelta(minutes=15)):
                        
                        # we need to set the name up first
                        imageName = str("./datasetlow/image (" + str(initialization_count) + ").jpg")
                        image_2_path = imageName
                        print(image_2_path)

                        # then we define the coordinates, see class shadow subclass coordinates for details but it's mostly export from EXIF data
                        global latitude
                        global longitude
                        latitude = shadow.coordinates.get_latitude(image_2_path)
                        longitude = shadow.coordinates.get_longitude(image_2_path)

                        # we extract the time information from the image, see class exifmeta for more information
                        year, month, day, hour, minute, second  = exifmeta.find_time_from_image(image_path=image_2_path)

                        # then we check where the sun is, as if it is below a set amount it will produce odd results, we need it to be above the horizon
                        if shadow.sun_data.altitude(coordinates_latitude=latitude, coordinates_longtitude=longitude, year=year, month=month, day=day, hour=hour, minute=minute, second=second) > 5:
                            
                            # calculate the north, see the north class, find_north function for more details, basically compares two images and uses also previous camera position data
                            north_main = north.find_north_fast(image_1=image_1_path, image_2=image_2_path)

                            # split image into many
                            split.file_split(north_main= north_main, image_id = full_image_id, image_path=image_2_path) # creates a ./chop/... folder and puts the chops into it with  "astrochop_n" syntax
                            
                            # this id is also to be seen in the final csv, it will be useful for backtracking back on Earth
                            sector_id = 0

                            # when we start a loop for all images in the chop, those were created with the split above, it will always be just 16 images
                            for images in os.listdir("./chop/"):
                                
                                # we must search for images as their names contain not only sector-id's but also coordinates, ergo that is best done via search 
                                search_image_path = "astrochop_" + str(sector_id)
                                def find(name, path):
                                    files = []
                                    for i in os.listdir(path):
                                        if os.path.isfile(os.path.join(path,i)) and name in i:
                                            files.append(i)
                                    files = files[0]
                                    return files
                                chop_image_path = find(search_image_path, "./chop")
                                print(chop_image_path)
                                chop_image_path = "./chop/" + chop_image_path
                                print(chop_image_path)

                                # then we check if the image is not all-clouds or all-sea with a brightness function, see the respective class for more information
                                if 50 < properties.calculate_brightness(chop_image_path) < 190 and properties.calculate_contrast(chop_image_path) > 10:
                                    try:
                                        # the image is fed to the ai model, which returns a dictionary of cloud boundaries and accuracies, see the ai class for more details
                                        global data
                                        data = ai.ai_model(chop_image_path)

                                        # we will use this counter to label the dictionary correctly
                                        counter_for_shadows = 0

                                        # the angle where shadows shall lay is calculated using the north data and sun azimuth angle, see the shadow class for more details
                                        angle = shadow.calculate_angle_for_shadow(latitude, longitude, year, month, day, hour, minute, second)

                                        # this loop runs through all the clouds detected in an image and writes the data into the final csv file
                                        while counter_for_shadows <= 9:
                                            try:
                                                # this code will figure us out the cloud bbox data, respectively its centre
                                                x_centre_of_cloud, y_centre_of_cloud, x_cloud_lenght, y_cloud_lenght = shadow.calculate_cloud_data(counter_for_shadows)
                                                
                                                # we check that the cloud is not too long as too long clouds would be useless and slow the program down
                                                if x_cloud_lenght < 100 and y_cloud_lenght < 100:
                                                    
                                                    # we add a simple error handling to make sure we can handle unexpected expections
                                                    try:
                                                        # this piece of code will return either data or "error" string, that will happen in rare cases
                                                        # so that the loop does not crash completely and skip the cloud we use the "error" string
                                                        result_shadow = shadow.calculate_shadow(file_path=image_2_path, x=x_centre_of_cloud, y=y_centre_of_cloud, angle=angle, image_id=sector_id, cloud_id=counter_for_shadows)
                                                        
                                                        # here we simply pass if an unexpected though handlable error happens
                                                        if result_shadow == "error":
                                                            pass

                                                        # else we write the results into a csv table which we will try to get back on Earth for analysis
                                                        else:
                                                            # here we add the datum to a python dictionary
                                                            data[counter_for_shadows]['shadow'] = shadow.calculate_shadow(file_path=image_2_path, x=x_centre_of_cloud, y=y_centre_of_cloud, angle=angle, image_id=sector_id, cloud_id=counter_for_shadows)
                                                            
                                                            # here we run a simple csv writer to write into the file
                                                            with open('shadows.csv', 'a') as f:
                                                                writer = csv.writer(f)
                                                                data_csv = [full_image_id, sector_id, counter_for_shadows, data[counter_for_shadows]['shadow']]
                                                                writer.writerow(data_csv)
                                                    except:
                                                        # we add simple error handling
                                                        pass

                                                    # we print the data into some log file
                                                    try:
                                                        to_print = str("Cloud number " + str(counter_for_shadows) + " has a height of " + str(data[counter_for_shadows]['shadow']))
                                                        shadow.print_log(to_print)
                                                    except:
                                                        to_print = str("Cloud number " + str(counter_for_shadows) + " raised error")
                                                        shadow.print_log(to_print)
                                                        pass
                                                else:
                                                    # add data to log file
                                                    to_print = str("Cloud number "+ str(counter_for_shadows) + " did not meet maximal lenght criteria")
                                                    shadow.print_log(to_print)
                                                counter_for_shadows += 1                             
                                            except:
                                                break
                                    except:
                                        to_print = "There was an error running the ai module" 
                                        shadow.print_log(to_print)
                                else:
                                    # add data to log file
                                    to_print = str("Skipped chop due to the brightness being" + str(properties.calculate_brightness(chop_image_path)))
                                    shadow.print_log(to_print)
                                sector_id += 1
                        else:
                            # add data to log file
                            to_print = str("Skipped image due to the sun being under 5 degrees, i.e. " + str(shadow.sun_data.altitude(coordinates_latitude=latitude, coordinates_longtitude=longitude, year=year, month=month, day=day, hour=hour, minute=minute, second=second)))
                            shadow.print_log(to_print)
                    
                        # for the north function we simply change the image_2_path to be image_1_path and we can count on
                        image_1_path = image_2_path

                        # we also up the counts
                        full_image_id += 1
                        initialization_count += 1
                except:
                    # add data to log file
                    to_print = str("There was an error during the main runtime")
                    shadow.print_log(to_print)
            except:
                # add data to log file
                to_print = str("There was an error running the code" )
                shadow.print_log(to_print)
        
        # add data to log file
        to_print = str("Starting: " + str(self.name))
        shadow.print_log(to_print)

        # run the main function as seen above
        main_processing()

        # add data to log file
        to_print = str("Exiting: " + str(self.name))
        shadow.print_log(to_print)
if __name__ == '__main__':
    # there are many advantages to multithreaded operation compare to monothread
    # suppose we ignore photos taken in the complete darkness, i.e. half the time,
    # but because the processing is so much slower than the photographing we will have many unprocessed images that could take advatage of being run in the dark.
    # also because the processing is about 2 minutes/full image (as of v2.4),
    # we would have to force-quit operation often just in order to take photos in which the north class can detect similiar objects (when too far apart openCV would fail)
    
    # first we define the threads, see details on each in their respective code
    auxiliary_thread = photo_thread(1, "Thread1")
    main_thread = processing_thread(2, "Thread2")

    # we need to turn on the camera for both threads
    camera = PiCamera()
    camera.resolution = (4056, 3040)
    sleep(3) # to ensure quality of pictures
    
    # set the default interval for taking photos, this will be changed depending on day-night cycle
    photo_sleep_interval = 20

    # then we start the threads
    auxiliary_thread.start()
    sleep(10) # we set them slightly apart to make sure that we have a picture before calculating north
    main_thread.start()

    # and then we wait until they are finished 
    auxiliary_thread.join()
    main_thread.join()

    # we print a happy message to let us know that everything went well
    to_print = str("Done main thread")
    shadow.print_log(to_print)
