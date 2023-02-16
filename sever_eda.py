from exif import Image
from datetime import datetime
import cv2
import math
import numpy as np
import statistics

def find_north(image_1, image_2, latitude_image_1, latitude_image_2):
    latitude_image_1 = float(latitude_image_1)
    latitude_image_2 = float(latitude_image_2)

    def get_time(image):
        with open(image, 'rb') as image_file:
            img = Image(image_file)
            time_str = img.get("datetime_original")
            time = datetime.strptime(time_str, '%Y:%m:%d %H:%M:%S')
        return time
    def get_time_difference(image_1, image_2):
        time_1 = get_time(image_1)
        time_2 = get_time(image_2)
        time_difference = time_2 - time_1
        print("time_difference", time_difference)
        return time_difference.seconds

    def convert_to_cv(image_1, image_2):
        image_1_cv = cv2.imread(image_1, 0)
        image_2_cv = cv2.imread(image_2, 0)
        return image_1_cv, image_2_cv

    def calculate_features(image_1, image_2, feature_number):
        orb = cv2.ORB_create(nfeatures = feature_number)
        keypoints_1, descriptors_1 = orb.detectAndCompute(image_1_cv, None)
        keypoints_2, descriptors_2 = orb.detectAndCompute(image_2_cv, None)
        return keypoints_1, keypoints_2, descriptors_1, descriptors_2

    def calculate_matches(descriptors_1, descriptors_2):
        brute_force = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = brute_force.match(descriptors_1, descriptors_2)
        matches = sorted(matches, key=lambda x: x.distance)
        return matches
    def display_matches(image_1_cv, keypoints_1, image_2_cv, keypoints_2, matches):
        match_img = cv2.drawMatches(image_1_cv, keypoints_1, image_2_cv, keypoints_2, matches[:100000000], None)
        resize = cv2.resize(match_img, (1600,600), interpolation = cv2.INTER_AREA)
        cv2.imshow('matches', resize)
        cv2.waitKey(0)
        cv2.destroyWindow('matches')

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
            x_11all.append(x1)
            x_22all.append(x2)
            y_11all.append(y1)
            y_22all.append(y2)
        x_11all_div=0
        x_11all_div=statistics.median(x_11all)
        x_22all_div=0
        x_22all_div=statistics.median(x_22all)
        y_11all_div=0
        y_11all_div=statistics.median(y_11all)
        y_22all_div=0
        y_22all_div=statistics.median(y_22all)
        
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

        delta_x = abs(delta_x)
        delta_y = abs(delta_y)
        tangens_angle_for_general_direction_radians = np.arctan((delta_y)/(delta_x))
        tangens_angle_for_general_direction_degrees = tangens_angle_for_general_direction_radians * (360/(2*np.pi))

        return coordinates_1, coordinates_2, tangens_angle_for_general_direction_degrees

    #latitude_image_1 = -43.88975 #latitude před procesem
    #latitude_image_2 = -44.18364 #latitude po procesu
    #latitude_image_1 = 1 #latitude před procesem
    #latitude_image_2 = -1 #latitude po procesu
    #latitude_image_1 = -13.12361 #latitude před procesem madagaskar
    #latitude_image_2 = -12.67333 #latitude po procesu madagaskar
    #latitude_image_1 = -25.49306 #latitude před procesem namibie
    #latitude_image_2 = -25.07194 #latitude po procesu namibie
    #latitude_image_1 = 51.61778 #latitude switzerland
    #latitude_image_2 = 51.55894 #latitude switzerland


    #latitude_image_1 = -21.26222 #latitude namibie 1
    #latitude_image_1 = -20.82889 #latitude namibie 2
    #latitude_image_2 = -20.39417 #latitude namibie 3

    time_difference = get_time_difference(image_1, image_2) 
    image_1_cv, image_2_cv = convert_to_cv(image_1, image_2) 
    keypoints_1, keypoints_2, descriptors_1, descriptors_2 = calculate_features(image_1_cv, image_2_cv, 10000) 
    matches = calculate_matches(descriptors_1, descriptors_2)
    display_matches(image_1_cv, keypoints_1, image_2_cv, keypoints_2, matches)
    coordinates_1, coordinates_2, tangens_angle_for_general_direction_degrees = find_matching_coordinates(keypoints_1, keypoints_2, matches)

    tangens_angle_for_general_direction_degrees = abs(tangens_angle_for_general_direction_degrees)
    tangens_angle_for_general_direction_degrees = abs(tangens_angle_for_general_direction_degrees)

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


    latitude_avg = (latitude_image_1+latitude_image_2)/2

    alpha_k=np.arcsin((np.cos(51.8*(np.pi/180)))/(np.cos(latitude_avg*(np.pi/180))))
    alpha_k = alpha_k*(180/np.pi)
    print("Alpha:", alpha_k)
    corrected_alpha_k=0
    if latitude_image_1>latitude_image_2:
        corrected_alpha_k=180-alpha_k
    else:
        corrected_alpha_k=alpha_k
    clockwise_alpha_k=360-corrected_alpha_k

    print("Clockwise alpha_k: ",clockwise_alpha_k)
    print("Edoov koeficient: ", edoov_coefficient)
    print("Clockwise edoov koeficient: ", clockwise_edoov_coefficient)

    poloha_severu=clockwise_alpha_k-clockwise_edoov_coefficient
    print("Poloha severu: ",poloha_severu)
    return poloha_severu, clockwise_edoov_coefficient

if __name__ == '__main__':
    find_north(".\\namibie1.jpg", ".\\namibie2.jpg", "-25.07194", "-25.49306")