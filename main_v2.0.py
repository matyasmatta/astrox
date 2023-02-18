# for further file history see main_old/main_v1.4.py

from datetime import datetime
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
from pycoral.adapters import common
from pycoral.adapters import detect
from pycoral.utils.dataset import read_label_file
from pycoral.utils.edgetpu import make_interpreter
import json
import os
from PIL import Image
import numpy as np
from numpy import average 
from skyfield import api
from skyfield import almanac
import os
import json
import csv
from sense_hat import SenseHat
from datetime import datetime, timedelta
from time import sleep
from csv import writer
from pathlib import Path
from picamera import PiCamera
from orbit import ISS
from exif import Image as exify

class list:
    global store_clockwise_edoov_coefficient
    store_clockwise_edoov_coefficient = []
    def get_median():
        return statistics.median(store_clockwise_edoov_coefficient)
    def add_clockwise_edoov_coefficient(item):
        store_clockwise_edoov_coefficient.append(item)
    def get_list():
        return store_clockwise_edoov_coefficient
class north:
    def find_north(image_1, image_2):

        #geting EXIF time of capture
        def get_time(image):
            with open(image, 'rb') as image_file:
                img = Image(image_file)
                try:
                    time_str = img.get("datetime_original")
                    time = datetime.strptime(time_str, '%Y:%m:%d %H:%M:%S')
                except TypeError:
                    time = 0
            return time
        
        #getting time difference between the two input images
        def get_time_difference(image_1, image_2):
            time_1 = get_time(image_1)
            time_2 = get_time(image_2)
            if time_2 != 0:
                time_difference = time_2 - time_1
    #            print("time_difference", time_difference)
            else:
                return 0
            return time_difference.seconds

        #converting images to cv friendly readable format 
        def convert_to_cv(image_1, image_2):
            image_1_cv = cv2.imread(image_1, 0)
            image_2_cv = cv2.imread(image_2, 0)
            return image_1_cv, image_2_cv

        #finding same "things" on both images
        def calculate_features(image_1, image_2, feature_number):
            orb = cv2.ORB_create(nfeatures = feature_number)
            keypoints_1, descriptors_1 = orb.detectAndCompute(image_1_cv, None)
            keypoints_2, descriptors_2 = orb.detectAndCompute(image_2_cv, None)
            return keypoints_1, keypoints_2, descriptors_1, descriptors_2

        #connecting same "things" on photo
        def calculate_matches(descriptors_1, descriptors_2):
            brute_force = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
            matches = brute_force.match(descriptors_1, descriptors_2)
            matches = sorted(matches, key=lambda x: x.distance)
            return matches
        
        #displaying the matches (only works on PC)
        #def display_matches(image_1_cv, keypoints_1, image_2_cv, keypoints_2, matches):
            match_img = cv2.drawMatches(image_1_cv, keypoints_1, image_2_cv, keypoints_2, matches[:1000], None)
            resize = cv2.resize(match_img, (1600,600), interpolation = cv2.INTER_AREA)
            cv2.imshow('matches', resize)
            cv2.waitKey(10)
            cv2.destroyWindow('matches')

        def hack_ISS():
            h=[]
            all_informations = 1000101
            h.append(all_informations)

        #finding coordination of same "things" on both fotos
        def find_matching_coordinates(keypoints_1, keypoints_2, matches):
            coordinates_1 = []
            coordinates_2 = []
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
                coordinates_1.append((x1,y1))
                coordinates_2.append((x2,y2))
                #we store all matched coordinates to list for further calculation
                x_11all.append(x1)
                x_22all.append(x2)
                y_11all.append(y1)
                y_22all.append(y2)
            #this calculates us the median of all coordinations on output [x1, y1] and [x2,y2]
            x_11all_div=0
            x_11all_div=statistics.median(x_11all)
            x_22all_div=0
            x_22all_div=statistics.median(x_22all)
            y_11all_div=0
            y_11all_div=statistics.median(y_11all)
            y_22all_div=0
            y_22all_div=statistics.median(y_22all)
            
            #we find the vector of median coordinates and place them into one of four quadrants 
            global direction_x
            global direction_y
            delta_x = x_11all_div-x_22all_div
            if delta_x > 0:
                direction_x = "left"
            elif delta_x < 0:
                direction_x = "right"
            else: 
                direction_x = "null"
            delta_y = y_11all_div-y_22all_div
            if delta_y > 0:
                direction_y = "up"
            elif delta_y < 0:
                direction_y = "down"
            else:
                direction_y = "null"

            #we calculate the angle of movemment of "things" on photo
            delta_x = abs(delta_x)
            delta_y = abs(delta_y)
            tangens_angle_for_general_direction_radians = np.arctan((delta_y)/(delta_x))
            tangens_angle_for_general_direction_degrees = tangens_angle_for_general_direction_radians * (360/(2*np.pi))

            return coordinates_1, coordinates_2, tangens_angle_for_general_direction_degrees
        
        #getting latitude of both images from EXIF data
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
            return latitude, latitude_ref
        

        #converting latitude to decimal
        def get_decimal_latitude(latitude, latitude_ref):
            decimal_degrees = latitude[0] + latitude[1] / 60 + latitude[2] / 3600
            if latitude_ref == "S" or latitude_ref == "W":
                decimal_degrees = -decimal_degrees
            return decimal_degrees

        #getting latitude for using
        def get_latitudes(image_1, image_2):    
            latitude_image_1_x, latitude_image_1_ref = get_latitude(image_1)
            latitude_image_1 = get_decimal_latitude(latitude_image_1_x, latitude_image_1_ref)
            latitude_image_2_x, latitude_image_2_ref = get_latitude(image_2)
            latitude_image_2 = get_decimal_latitude(latitude_image_2_x, latitude_image_2_ref)
            return latitude_image_1, latitude_image_2

        #def show_north(angle):
            angle=angle/180*np.pi
            r=560/2
            x_0=183+r
            y_0=37+r
            dy=-np.cos(angle)*r
            dx=np.sin(angle)*r
            print_x=int(x_0+dx)
            print_y=int(y_0+dy)
            print_cordinations=(print_x, print_y)
            #print(angle)
            #print(x_0, y_0)
            #print("lool", dx, dy)
            #print(print_cordinations)
            image=cv2.imread(image_1)
            resized = cv2.resize(image, (800,600), interpolation = cv2.INTER_AREA)
            cv2.putText(resized, "N", print_cordinations, cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5, cv2.LINE_AA)
            cv2.imshow('north', resized)
            cv2.waitKey(10)
            cv2.destroyAllWindows()

        #latitude_image_1 = -43.88975 #latitude před procesem
        #latitude_image_2 = -44.18364 #latitude po procesu
        #latitude_image_1 = 1 #latitude před procesem
        #latitude_image_2 = -1 #latitude po procesu
        #latitude_image_1 = -13.12361 #latitude před procesem madagaskar
        #latitude_image_2 = -12.67333 #latitude po procesu madagaskar
        #latitude_image_1 = -25.49306 #latitude před procesem nqamibie
        #latitude_image_2 = -25.07194 #latitude po procesu namibie
        #latitude_image_1 = 51.61778 #latitude switzerland
        #latitude_image_2 = 51.55894 #latitude switzerland


        #latitude_image_1 = -21.26222 #latitude namibie 1
        #latitude_image_1 = -20.82889 #latitude namibie 2
        #latitude_image_2 = -20.39417 #latitude namibie 3

        #using defined functions
        latitude_image_1, latitude_image_2 = get_latitudes(image_1, image_2)
        #time_difference = get_time_difference(image_1, image_2) 
        image_1_cv, image_2_cv = convert_to_cv(image_1, image_2) 
        keypoints_1, keypoints_2, descriptors_1, descriptors_2 = calculate_features(image_1_cv, image_2_cv, 10) 
        matches = calculate_matches(descriptors_1, descriptors_2)
        #display_matches(image_1_cv, keypoints_1, image_2_cv, keypoints_2, matches)
        coordinates_1, coordinates_2, tangens_angle_for_general_direction_degrees = find_matching_coordinates(keypoints_1, keypoints_2, matches)

        tangens_angle_for_general_direction_degrees = abs(tangens_angle_for_general_direction_degrees)

        #calculating the relative rotation of camera on ISS
        edoov_coefficient = ""
        if direction_x == "left":
            if direction_y == "up":
                edoov_coefficient = (tangens_angle_for_general_direction_degrees, -1, -1, "↖")
                clockwise_edoov_coefficient = 270-tangens_angle_for_general_direction_degrees
            if direction_y == "down":
                edoov_coefficient = (tangens_angle_for_general_direction_degrees, -1, 1,"↙")
                clockwise_edoov_coefficient = 270+tangens_angle_for_general_direction_degrees
        if direction_x == "right":
            if direction_y == "up":
                edoov_coefficient = (tangens_angle_for_general_direction_degrees, 1, -1, "↗")
                clockwise_edoov_coefficient = 90+tangens_angle_for_general_direction_degrees
            if direction_y == "down":
                edoov_coefficient = (tangens_angle_for_general_direction_degrees, 1, 1, "↘")
                clockwise_edoov_coefficient = 90-tangens_angle_for_general_direction_degrees
        list.add_clockwise_edoov_coefficient(clockwise_edoov_coefficient)
        median_clockwise_edoov_coefficient=list.get_median()
        #averaging latitudes for more accurate calculation 
        latitude_avg = (latitude_image_1+latitude_image_2)/2

        #calculating the relative position of north for ISS (looks forward)
        alpha_k=np.arcsin((np.cos(51.8*(np.pi/180)))/(np.cos(latitude_avg*(np.pi/180))))
        alpha_k = alpha_k*(180/np.pi)
    #    print("Alpha:", alpha_k)
        corrected_alpha_k=0
        if latitude_image_1>latitude_image_2:
            corrected_alpha_k=180-alpha_k
        else:
            corrected_alpha_k=alpha_k
        clockwise_alpha_k=360-corrected_alpha_k

    #    print("Clockwise alpha_k: ",clockwise_alpha_k)
    #    print("Edoov koeficient: ", edoov_coefficient)
    #    print("Clockwise edoov koeficient: ", clockwise_edoov_coefficient)

        #combinating both informations to get real position of north on photo
        poloha_severu=clockwise_alpha_k-median_clockwise_edoov_coefficient
        #print("Poloha severu: ",poloha_severu)
    #    print(latitude_image_1, latitude_image_2)

        #print(list.get_median())
        #show_north(poloha_severu)
        #print(list.get_list())
        return poloha_severu    # updated by @Alfons8128 via sever_eda_2tecka0.py
    def find_north(image_1, image_2):
        #geting EXIF time of capture
        def get_time(image):
            with open(image, 'rb') as image_file:
                img = Image(image_file)
                try:
                    time_str = img.get("datetime_original")
                    time = datetime.strptime(time_str, '%Y:%m:%d %H:%M:%S')
                except TypeError:
                    time = 0
            return time
        
        #getting time difference between the two input images
        def get_time_difference(image_1, image_2):
            time_1 = get_time(image_1)
            time_2 = get_time(image_2)
            if time_2 != 0:
                time_difference = time_2 - time_1
    #            print("time_difference", time_difference)
            else:
                return 0
            return time_difference.seconds

        #converting images to cv friendly readable format 
        def convert_to_cv(image_1, image_2):
            image_1_cv = cv2.imread(image_1, 0)
            image_2_cv = cv2.imread(image_2, 0)
            return image_1_cv, image_2_cv

        #finding same "things" on both images
        def calculate_features(image_1, image_2, feature_number):
            orb = cv2.ORB_create(nfeatures = feature_number)
            keypoints_1, descriptors_1 = orb.detectAndCompute(image_1_cv, None)
            keypoints_2, descriptors_2 = orb.detectAndCompute(image_2_cv, None)
            return keypoints_1, keypoints_2, descriptors_1, descriptors_2

        #connecting same "things" on photo
        def calculate_matches(descriptors_1, descriptors_2):
            brute_force = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
            matches = brute_force.match(descriptors_1, descriptors_2)
            matches = sorted(matches, key=lambda x: x.distance)
            return matches
        
        #displaying the matches (only works on PC)
        #def display_matches(image_1_cv, keypoints_1, image_2_cv, keypoints_2, matches):
            match_img = cv2.drawMatches(image_1_cv, keypoints_1, image_2_cv, keypoints_2, matches[:1000], None)
            resize = cv2.resize(match_img, (1600,600), interpolation = cv2.INTER_AREA)
            cv2.imshow('matches', resize)
            cv2.waitKey(10)
            cv2.destroyWindow('matches')
            
        #nic čeho se obávat
        def hack_ISS():
            h=[]
            all_informations = 1000101
            h.append(all_informations)

        #finding coordination of same "things" on both fotos
        def find_matching_coordinates(keypoints_1, keypoints_2, matches):
            coordinates_1 = []
            coordinates_2 = []
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
                coordinates_1.append((x1,y1))
                coordinates_2.append((x2,y2))
                #we store all matched coordinates to list for further calculation
                x_11all.append(x1)
                x_22all.append(x2)
                y_11all.append(y1)
                y_22all.append(y2)
            #this calculates us the median of all coordinations on output [x1, y1] and [x2,y2]
            x_11all_div=0
            x_11all_div=statistics.median(x_11all)
            x_22all_div=0
            x_22all_div=statistics.median(x_22all)
            y_11all_div=0
            y_11all_div=statistics.median(y_11all)
            y_22all_div=0
            y_22all_div=statistics.median(y_22all)
            
            #není nutné to dělit do 4 kvadrantů protože mega op funkce arctan2 to udělá za nás

            #we calculate the angle of movemment of "things" on photo
            delta_x = x_11all_div - x_22all_div
            #y jde v opačném směru (dolů) než je obvyklé pro práci s tangens, proto bude lepší odečítat y1 od y2
            delta_y = y_22all_div - y_11all_div
            
            tangens_angle_for_general_direction_radians = np.arctan2(delta_y,delta_x)
            tangens_angle_for_general_direction_degrees = tangens_angle_for_general_direction_radians * (360/(2*np.pi))

            return coordinates_1, coordinates_2, tangens_angle_for_general_direction_degrees
        
        #getting latitude of both images from EXIF data
        def get_latitude(image):
            with open(image, 'rb') as image_file:
                img = Image(image_file)
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
        
        #converting latitude to decimal
        def get_decimal_latitude(latitude, latitude_ref):
            decimal_degrees = latitude[0] + latitude[1] / 60 + latitude[2] / 3600
            if latitude_ref == "S" or latitude_ref == "W":
                decimal_degrees = -decimal_degrees
            return decimal_degrees

        #getting latitude for using
        def get_latitudes(image_1, image_2):    
            latitude_image_1_x, latitude_image_1_ref = get_latitude(image_1)
            latitude_image_1 = get_decimal_latitude(latitude_image_1_x, latitude_image_1_ref)
            latitude_image_2_x, latitude_image_2_ref = get_latitude(image_2)
            latitude_image_2 = get_decimal_latitude(latitude_image_2_x, latitude_image_2_ref)
            return latitude_image_1, latitude_image_2

        #def show_north(angle):
            angle=angle/180*np.pi
            r=560/2
            x_0=183+r
            y_0=37+r
            dy=-np.cos(angle)*r
            dx=np.sin(angle)*r
            print_x=int(x_0+dx)
            print_y=int(y_0+dy)
            print_cordinations=(print_x, print_y)
            #print(angle)
            #print(x_0, y_0)
            #print("lool", dx, dy)
            #print(print_cordinations)
            image=cv2.imread(image_1)
            resized = cv2.resize(image, (800,600), interpolation = cv2.INTER_AREA)
            cv2.putText(resized, "N", print_cordinations, cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5, cv2.LINE_AA)
            cv2.imshow('north', resized)
            cv2.waitKey(10)
            cv2.destroyAllWindows()

        #latitude_image_1 = -43.88975 #latitude před procesem
        #latitude_image_2 = -44.18364 #latitude po procesu
        #latitude_image_1 = 1 #latitude před procesem
        #latitude_image_2 = -1 #latitude po procesu
        #latitude_image_1 = -13.12361 #latitude před procesem madagaskar
        #latitude_image_2 = -12.67333 #latitude po procesu madagaskar
        #latitude_image_1 = -25.49306 #latitude před procesem nqamibie
        #latitude_image_2 = -25.07194 #latitude po procesu namibie
        #latitude_image_1 = 51.61778 #latitude switzerland
        #latitude_image_2 = 51.55894 #latitude switzerland


        #latitude_image_1 = -21.26222 #latitude namibie 1
        #latitude_image_1 = -20.82889 #latitude namibie 2
        #latitude_image_2 = -20.39417 #latitude namibie 3

        #using defined functions
        latitude_image_1, latitude_image_2 = get_latitudes(image_1, image_2)
        time_difference = get_time_difference(image_1, image_2) 
        image_1_cv, image_2_cv = convert_to_cv(image_1, image_2) 
        keypoints_1, keypoints_2, descriptors_1, descriptors_2 = calculate_features(image_1_cv, image_2_cv, 1000) 
        matches = calculate_matches(descriptors_1, descriptors_2)
        #display_matches(image_1_cv, keypoints_1, image_2_cv, keypoints_2, matches)
        coordinates_1, coordinates_2, tangens_angle_for_general_direction_degrees = find_matching_coordinates(keypoints_1, keypoints_2, matches)

        #calculating the relative rotation of camera on ISS
        edoov_coefficient = tangens_angle_for_general_direction_degrees #orientovaný úhel od spodku fotky ke směru pohybu - tedy to samé, co vyhodí arctan2
        
        list.add_clockwise_edoov_coefficient(edoov_coefficient) 
        #nechal jsem list.add_clockwise i když to není clockwise protože tu funkci tak Eda má pojmenovanou v list.py a mně se to nechce měnit
        median_edoov_coefficient=list.get_median()
        #averaging latitudes for more accurate calculation 
        latitude_avg = (latitude_image_1+latitude_image_2)/2

        #calculating the relative position of north for ISS (looks forward)
        alpha_k=np.arcsin((np.cos(51.8*(np.pi/180)))/(np.cos(latitude_avg*(np.pi/180))))
        alpha_k = alpha_k*(180/np.pi)
    #    print("Alpha:", alpha_k)
        corrected_alpha_k=0
        if latitude_image_1>latitude_image_2:
            corrected_alpha_k=180-alpha_k
        else:
            corrected_alpha_k=alpha_k

    #    print("Clockwise alpha_k: ",clockwise_alpha_k)
    #    print("Edoov koeficient: ", edoov_coefficient)
    #    print("Clockwise edoov koeficient: ", clockwise_edoov_coefficient)

        #combinating both informations to get real position of north on photo
        poloha_severu=corrected_alpha_k+median_edoov_coefficient
        #print("Poloha severu: ",poloha_severu)
    #    print(latitude_image_1, latitude_image_2)

        #print(list.get_median())
        #show_north(poloha_severu)
        #print(list.get_list())
        return poloha_severu
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
        shadow.draw_objects(ImageDraw.Draw(image), objs, labels)
        image.save('grace_hopper_processed.bmp')
        
            
        # image.show()
        if os.path.exists('meta.jpg') == True:
            os.remove('meta.jpg')
        image.save('meta.jpg')

        with open('ai_output.json', 'w', encoding='utf-8') as f:
            json.dump(ai_output, f, ensure_ascii=False, indent=4)
        return ai_output
class shadow:
    class coordinates:
        def get_latitude(image):
            with open(image, 'rb') as image_file:
                img = exify(image_file)
                try:
                    latitude = img.get("gps_latitude")
                except:
                    latitude = (0.0, 0.0, 0.0)
            return latitude
        def get_longitude(image):
            with open(image, 'rb') as image_file:
                img = exify(image_file)
                try:
                    longitude = img.get("gps_longitude")
                except:
                    longitude = (0.0, 0.0, 0.0)
            return longitude            

    def calculate_cloud_data(counter_for_shadows):
        x_max = data[counter_for_shadows]['xmax']
        y_max = data[counter_for_shadows]['ymax']
        x_min = data[counter_for_shadows]['xmin']
        y_min = data[counter_for_shadows]['ymin']
        print(x_min, y_min, x_max, y_max)
        x_centre_of_cloud = (x_min+x_max)/2
        y_centre_of_cloud = (y_min+y_max)/2
        x_centre_of_cloud = round(x_centre_of_cloud, 0)
        y_centre_of_cloud = round(y_centre_of_cloud, 0)
        x_centre_of_cloud = int(x_centre_of_cloud)
        y_centre_of_cloud = int(y_centre_of_cloud)
        x_cloud_lenght = abs(x_max - x_min)
        y_cloud_lenght = abs(y_max - y_min)

        return x_centre_of_cloud, y_centre_of_cloud, x_cloud_lenght, y_cloud_lenght

    # ignore the 'json' in the name, we replaced the file format with csv for simplicity, jsons are useful for export data - not metadata
    def write_pixel_into_icon(count, x, y, cloud_id="not specified", image_id="not specified"):
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
    
    def calculate_angle_for_shadow(north, latitude, longitude, year, month, day, hour=0, minute=0, second=0):
        azimuth = shadow.sun_data.azimuth(latitude, longitude, year, month, day, hour, minute, second)
        print(north, azimuth)
        total_angle = north + azimuth
        while True:
            if total_angle >= 360:
                total_angle -= 360
            else:
                break
        return total_angle


    def calculate_shadow(x, y, angle, cloud_id="not specified", image_id="not specified", file_path="not specified", image_direct="not specified"):
        # open specific cloud
        if file_path != "not specified":
            im = Image.open(file_path) # Can be many different formats.
            if image_direct != "not specified":
                im = image_direct
            pix = im.load()
        else:
            raise Exception("There was an error during initial loading for shadow calculation")


        # get the width and height of the image for iterating over
        # print(im.size) 
        total_x, total_y = im.size
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
        sun_altitude_for_limit = shadow.sun_data.altitude("34.28614 S", "147.9849 E", 2022, 1, 15, 5, 16, 5)
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

        # put quarter information back for pixel reading
        ## first two lines in each if condition are mostly legacy for backwards-compatibility, code should function without them though not tested yet
        if q == 1:
            x_increase_final = x_increase_final
            y_increase_final = -y_increase_final
            x,y = shadow.starting_point_corrector(x,y, x_increase_final, y_increase_final)
            while True:
                if x_increase_final_abs > y_increase_final_abs:
                    # check if y_sum is bigger than 1
                    y_sum = abs(y_sum)
                    if y_sum >= 1:
                        y_sum -= 1
                        y -= 1
                    # read pixel value
                    data = (pix[x,y])
                    # print(data)
                    value = round(average(data))
                    value_red = data[0]
                    # print(value)
                    # print("red", value_red)
                    list_of_red.append(value_red)
                    list_of_values.append(value)
                    im2 = Image.open('meta.jpg')
                    im2.putpixel((x,y),(0,0,0,0))
                    im2.save('meta.jpg')
                    # add to y_sum and move pixel x for 1
                    x += 1
                    y_sum += y_increase_final_abs
                    # print(count, limit)
                    shadow.write_pixel_into_icon(count=count, x=x, y=y, cloud_id=cloud_id, image_id=image_id)
                    if x > total_x or y > total_y:
                        break
                if x_increase_final_abs == y_increase_final_abs:               
                    data = (pix[x,y])
                    # print(data)
                    value = round(average(data))
                    value_red = data[0]
                    # print(value)
                    # print("red", value_red)
                    list_of_red.append(value_red)
                    list_of_values.append(value)
                    im2 = Image.open('meta.jpg')
                    im2.putpixel((x,y),(0,0,0,0))
                    im2.save('meta.jpg')
                    x += 1
                    y -= 1
                    # print(count, limit)
                    shadow.write_pixel_into_icon(count=count, x=x, y=y, cloud_id=cloud_id, image_id=image_id)
                    if x > total_x or y > total_y:
                        break
                if x_increase_final_abs < y_increase_final_abs:               
                    x_sum = abs(x_sum)
                    if x_sum >= 1:
                        x_sum -= 1
                        x += 1
                    # read pixel value
                    data = (pix[x,y])
                    # print(data)
                    value = round(average(data))
                    value_red = data[0]
                    # print(value)
                    # print("red", value_red)
                    list_of_red.append(value_red)
                    list_of_values.append(value)
                    im2 = Image.open('meta.jpg')
                    im2.putpixel((x,y),(0,0,0,0))
                    im2.save('meta.jpg')
                    # add to y_sum and move pixel x for 1
                    y -= 1
                    x_sum += x_increase_final_abs
                    # print(count, limit)
                    shadow.write_pixel_into_icon(count=count, x=x, y=y, cloud_id=cloud_id, image_id=image_id)
                    if x > total_x or y > total_y:
                        break
                #write into txt
                with open('stiny.txt', 'a') as f:
                    value = str(value)
                    f.write(value)
                    f.write("\n")
                with open('stiny_red.txt', 'a') as f:
                    value_red = str(value_red)
                    f.write(value_red)
                    f.write("\n")
                if count > limit:
                    break
        if q == 2:
            x_increase_final = x_increase_final
            y_increase_final = y_increase_final  
            x,y = shadow.shadow.starting_point_corrector(x,y, x_increase_final, y_increase_final) 
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
                    # print(data)
                    value = round(average(data))
                    value_red = data[0]
                    # print(value)
                    # print("red", value_red)
                    list_of_red.append(value_red)
                    list_of_values.append(value)
                    im2 = Image.open('meta.jpg')
                    im2.putpixel((x,y),(0,0,0,0))
                    im2.save('meta.jpg')
                    # add to y_sum and move pixel x for 1
                    x += 1
                    y_sum += y_increase_final_abs
                    # print(count, limit)
                    shadow.write_pixel_into_icon(count=count, x=x, y=y, cloud_id=cloud_id, image_id=image_id)
                    if x > total_x or y > total_y:
                        break
                if x_increase_final_abs == y_increase_final_abs:          
                    data = (pix[x,y])
                    # print(data)
                    value = round(average(data))
                    value_red = data[0]
                    # print(value)
                    # print("red", value_red)
                    list_of_red.append(value_red)
                    list_of_values.append(value)
                    im2 = Image.open('meta.jpg')
                    im2.putpixel((x,y),(0,0,0,0))
                    im2.save('meta.jpg')
                    x += 1
                    y += 1
                    # print(count, limit)
                    shadow.write_pixel_into_icon(count=count, x=x, y=y, cloud_id=cloud_id, image_id=image_id)
                    if x > total_x or y > total_y:
                        break
                if x_increase_final_abs < y_increase_final_abs:   
                    x_sum = abs(x_sum)
                    if x_sum >= 1:
                        x_sum -= 1
                        x += 1
                    # read pixel value
                    data = (pix[x,y])
                    # print(data)
                    value = round(average(data))
                    value_red = data[0]
                    # print(value)
                    # print("red", value_red)
                    list_of_red.append(value_red)
                    list_of_values.append(value)
                    im2 = Image.open('meta.jpg')
                    im2.putpixel((x,y),(0,0,0,0))
                    im2.save('meta.jpg')
                    # add to y_sum and move pixel x for 1
                    y += 1
                    x_sum += x_increase_final_abs
                    #write into txt
                    # print(count, limit)
                    shadow.write_pixel_into_icon(count=count, x=x, y=y, cloud_id=cloud_id, image_id=image_id)
                    if x > total_x or y > total_y:
                        break
                with open('stiny.txt', 'a') as f:
                    value = str(value)
                    f.write(value)
                    f.write("\n")
                with open('stiny_red.txt', 'a') as f:
                    value_red = str(value_red)
                    f.write(value_red)
                    f.write("\n")
                if count > limit:
                    break
        if q == 3:
            x_increase_final = -x_increase_final
            y_increase_final = y_increase_final 
            x,y = shadow.starting_point_corrector(x,y, x_increase_final, y_increase_final)
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
                    # print(data)
                    value = round(average(data))
                    value_red = data[0]
                    # print(value)
                    # print("red", value_red)
                    list_of_red.append(value_red)
                    list_of_values.append(value)
                    im2 = Image.open('meta.jpg')
                    im2.putpixel((x,y),(0,0,0,0))
                    im2.save('meta.jpg')
                    # add to y_sum and move pixel x for 1
                    x -= 1
                    y_sum += y_increase_final_abs
                    # print(count, limit)
                    shadow.write_pixel_into_icon(count=count, x=x, y=y, cloud_id=cloud_id, image_id=image_id)
                    if x > total_x or y > total_y:
                        break
                if x_increase_final_abs == y_increase_final_abs:
                    data = (pix[x,y])
                    # print(data)
                    value = round(average(data))
                    value_red = data[0]
                    # print(value)
                    # print("red", value_red)
                    list_of_red.append(value_red)
                    list_of_values.append(value)
                    im2 = Image.open('meta.jpg')
                    im2.putpixel((x,y),(0,0,0,0))
                    im2.save('meta.jpg')
                    x -= 1
                    y += 1
                    # print(count, limit)
                    shadow.write_pixel_into_icon(count=count, x=x, y=y, cloud_id=cloud_id, image_id=image_id)
                    if x > total_x or y > total_y:
                        break
                if x_increase_final_abs < y_increase_final_abs:
                    x_sum = abs(x_sum)
                    if x_sum >= 1:
                        x_sum -= 1
                        x -= 1
                    # read pixel value
                    data = (pix[x,y])
                    # print(data)
                    value = round(average(data))
                    value_red = data[0]
                    # print(value)
                    # print("red", value_red)
                    list_of_red.append(value_red)
                    list_of_values.append(value)
                    im2 = Image.open('meta.jpg')
                    im2.putpixel((x,y),(0,0,0,0))
                    im2.save('meta.jpg')
                    # add to y_sum and move pixel x for 1
                    y += 1
                    x_sum += x_increase_final_abs
                    # print(count, limit)
                    shadow.write_pixel_into_icon(count=count, x=x, y=y, cloud_id=cloud_id, image_id=image_id)
                    if x > total_x or y > total_y:
                        break
                #write into txt
                value = str(value)
                with open('stiny.txt', 'a') as f:
                    f.write(value)
                    f.write("\n")
                if count > limit:
                    break
        if q == 4:
            x_increase_final = -x_increase_final
            y_increase_final = -y_increase_final 
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
                    # print(data)
                    value = round(average(data))
                    value_red = data[0]
                    # print(value)
                    # print("red", value_red)
                    list_of_red.append(value_red)
                    list_of_values.append(value)
                    im2 = Image.open('meta.jpg')
                    im2.putpixel((x,y),(0,0,0,0))
                    im2.save('meta.jpg')
                    # add to y_sum and move pixel x for 1
                    x -= 1
                    y_sum += y_increase_final_abs
                    # print(count)
                    # print(count, limit)
                    shadow.write_pixel_into_icon(count=count, x=x, y=y, cloud_id=cloud_id, image_id=image_id)
                    if x > total_x or y > total_y:
                        break
                if x_increase_final_abs == y_increase_final_abs:
                    data = (pix[x,y])
                    # print(data)
                    value = round(average(data))
                    value_red = data[0]
                    # print(value)
                    # print("red", value_red)
                    list_of_red.append(value_red)
                    list_of_values.append(value)
                    im2 = Image.open('meta.jpg')
                    im2.putpixel((x,y),(0,0,0,0))
                    im2.save('meta.jpg')
                    x -= 1
                    y -= 1
                    # print(count, limit)
                    shadow.write_pixel_into_icon(count=count, x=x, y=y, cloud_id=cloud_id, image_id=image_id)
                    if x > total_x or y > total_y:
                        break
                if x_increase_final_abs < y_increase_final_abs:
                    x_sum = abs(x_sum)
                    if x_sum >= 1:
                        x_sum -= 1
                        x -= 1
                    # read pixel value
                    data = (pix[x,y])
                    # print(data)
                    value = round(average(data))
                    value_red = data[0]
                    # print(value)
                    # print("red", value_red)
                    list_of_red.append(value_red)
                    list_of_values.append(value)
                    im2 = Image.open('meta.jpg')
                    im2.putpixel((x,y),(0,0,0,0))
                    im2.save('meta.jpg')
                    # add to y_sum and move pixel x for 1
                    y -= 1
                    x_sum += x_increase_final_abs
                    # print(count, limit)
                    shadow.write_pixel_into_icon(count=count, x=x, y=y, cloud_id=cloud_id, image_id=image_id)
                    if x > total_x or y > total_y:
                        break
                #write into txt
                with open('stiny.txt', 'a') as f:
                    value = str(value)
                    f.write(value)
                    f.write("\n")
                with open('stiny_red.txt', 'a') as f:
                    value_red = str(value_red)
                    f.write(value_red)
                    f.write("\n")
                if count > limit:
                    break

        # # print for debugging
        # print(x_increase_final, y_increase_final)
        im2.save('meta.jpg')
        # set absolute final values
        x_increase_final_abs = abs(x_increase_final)
        y_increase_final_abs = abs(x_increase_final)

        # print(list_of_values)
        breakpoint
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

        altitude = shadow.sun_data.altitude("34.28614 S", "147.9849 E", 2022, 1, 15, 5, 16, 5)
        # calculate final values
        altitude_radians = altitude*(np.pi/180)
        cloudheight = np.tan(altitude_radians)*lenght
        cloudheight = np.round(cloudheight,2)

        # print("Shadow is exactly", cloudheight, "meters from ground!")
        # print(list_of_values)
        return cloudheight    
class photo:
    def convert(angle):
        sign, degrees, minutes, seconds = angle.signed_dms()
        exif_angle = f'{degrees:.0f}/1,{minutes:.0f}/1,{seconds*10:.0f}/10'
        return sign < 0, exif_angle

    def get_photo(camera):
        location = ISS.coordinates()

        # Convert the latitude and longitude to EXIF-appropriate representations
        south, exif_latitude = photo.convert(location.latitude)
        west, exif_longitude = photo.convert(location.longitude)

        # Set the EXIF tags specifying the current location
        camera.exif_tags['GPS.GPSLatitude'] = exif_latitude
        camera.exif_tags['GPS.GPSLatitudeRef'] = "S" if south else "N"
        camera.exif_tags['GPS.GPSLongitude'] = exif_longitude
        camera.exif_tags['GPS.GPSLongitudeRef'] = "W" if west else "E"

        # Capture the image
        imageName = ""
        imageName = str("/img_" + str(count_for_edovo_srac) + ".jpg")
        camera.capture("./Pictures" + imageName)
try:
    # first define all functions neccessary for operation and calibrate the camera
    # pre-initialization
    try:
        start_time =  datetime.now()
        camera = PiCamera()
        sleep(2)
        initialization_count = 240
        photo.get_photo(camera)
        initialization_count += 1
    except:
        print("There was an error during pre-initialization")

    # initialise and calibrate the north data via north class
    # initialization
    try:
        while (datetime.now() < start_time + timedelta(seconds=69)):
            photo.get_photo(camera)
            i_1=str(initialization_count-1)
            before = "./Pictures2/photo_18"
            image_1=str(before + i_1 +".jpg")
            i_2=str(initialization_count)
            #print(image_1)
            image_2=str(before + i_2 +".jpg")
            #print(image_2)

            data = north.find_north(image_1, image_2)
            print(list.get_median())
            initialization_count += 1
            sleep(0)
            print(datetime.now())
            print(image_1)
            north_initial = list.get_median()
        print("North was defined at", north_initial, "counted clockwise.")
    except:
        print("There was an error during the initialzitation")

    # run the actual main code
    # main runtime
    try:
        # first take a photo outside the loop for first reference
        image_1 = photo.get_photo(camera)

        # make sure there is a little bit of differnce for the north class
        sleep(1)

        # set the north calculated during initialization as baseline of a new list
        north_database = [north_initial]
        image_id = 0

        # the following is the main loop which will run for the majority of time on the ISS
        while (datetime.now() < start_time + timedelta(minutes=170)):
            # first we take a photo within the loop
            image_2 = photo.get_photo(camera)

            # then we define the coordinates, see class shadow subclass coordinates for details but it's mostly export from EXIF data
            latitude = shadow.coordinates.get_latitude(image_2)
            longitude = shadow.coordinates.get_longitude(image_2)

            # we extract the time information from datetime library 
            year = datetime.datetime.now().year
            month = datetime.datetime.now().month
            day = datetime.datetime.now().day
            hour = datetime.datetime.now().hour
            minute = datetime.datetime.now().minute
            second = datetime.datetime.now().second

            # calculate the north, see the north class, find_north function for more details, basically compares two images and uses also previous camera position data
            north_main = north.find_north(image_1=image_1, image_2=image_2)

            # the image is fed to the ai model, which returns a dictionary of cloud boundaries and accuracies, see the ai class for more details
            data_of_ai_model = ai.ai_model(image_2)

            # we will use this counter to label the dictionary correctly
            counter_for_shadows = 0

            # the angle where shadows shall lay is calculated using the north data and sun azimuth angle, see the shadow class for more details
            angle = shadow.calculate_angle_for_shadow(latitude, longitude, year, month, day, hour, minute, second)

            # this loop runs through all the clouds detected in an image and writes the data into the final csv file
            while True:
                try:
                    x_centre_of_cloud, y_centre_of_cloud, x_cloud_lenght, y_cloud_lenght = shadow.calculate_cloud_data(counter_for_shadows)
                    if x_cloud_lenght < 69 and y_cloud_lenght < 69:
                        try:
                            data[counter_for_shadows]['shadow'] = shadow.calculate_shadow(image_2, x_centre_of_cloud, y_centre_of_cloud, angle, cloud_id=counter_for_shadows, image_id=image_id)
                        except:
                            print("There was an error running the shadow module.")
                        print("Cloud number", counter_for_shadows, "has a lenght of", data[counter_for_shadows]['shadow'])
                    else:
                        print("Cloud number", counter_for_shadows, "did not meet maximal lenght criteria")
                    counter_for_shadows += 1                             
                except:
                    meta = Image.open('meta.jpg')
                    meta.show()
                    break

            image_1 = image_2
            image_id += 1
            del image_2
    except:
        print("There was an error during the main runtime")

    # after time has passed do automatic runtime checks
    # finalization
except:
    print("There was an error running the code")
    pass
