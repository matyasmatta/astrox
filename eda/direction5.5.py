from exif import Image
from datetime import datetime
import cv2
import math
import numpy as np

#def get_time(image):
#    with open(image, 'rb') as image_file:
#        img = Image(image_file)
 #       time_str = img.get("datetime_original")
 #       time = datetime.strptime(time_str, '%Y:%m:%d %H:%M:%S')
 #   return time
#def get_time_difference(image_1, image_2):
 #   time_1 = get_time(image_1)
 #   time_2 = get_time(image_2)
 #  time_difference = time_2 - time_1
  #  print("time_difference", time_difference)
  #  return time_difference.seconds

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
    match_img = cv2.drawMatches(image_1_cv, keypoints_1, image_2_cv, keypoints_2, matches[:1000], None)
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
    x_1all= 0
    x_2all= 0
    y_1all= 0
    y_2all=0
    counter=0
    for match in matches:
        image_1_idx = match.queryIdx
        image_2_idx = match.trainIdx
        (x1,y1) = keypoints_1[image_1_idx].pt
        (x2,y2) = keypoints_2[image_2_idx].pt
        coordinates_1.append((x1,y1))
        coordinates_2.append((x2,y2))
        counter+=1    
        x_11all.append(x1)
        x_22all.append(x2)
        y_11all.append(y1)
        y_22all.append(y2)
        x_1all=x_1all+x1
        x_2all=x_2all+x2
        y_1all=y_1all+y1
        y_2all=y_2all+y2
    x_1all_div=x_1all/counter
    x_2all_div=x_2all/counter
    y_1all_div=y_1all/counter
    y_2all_div=y_2all/counter
    print("P1:",x_1all_div, y_1all_div," P2:", x_2all_div, y_2all_div)
    x_11all_div=0
    x_11all_div=statistics.median(x_11all)
    x_22all_div=0
    x_22all_div=statistics.median(x_22all)
    y_11all_div=0
    y_11all_div=statistics.median(y_11all)
    y_22all_div=0
    y_22all_div=statistics.median(y_22all)
    print("P1:",x_11all_div, y_11all_div," P2:", x_22all_div, y_22all_div)
    global direction_x
    global direction_y
    delta_x = x_1all_div-x_2all_div
    if delta_x > 0:
        direction_x = "left"
    elif delta_x < 0:
        direction_x = "right"
    else: 
        direction_x = "null"
    delta_y = y_1all_div-y_2all_div
    if delta_y > 0:
        direction_y = "up"
    elif delta_y < 0:
        direction_y = "down"
    else:
        direction_y = "null"
    
    delta_x = abs(delta_x)
    delta_y = abs(delta_y)
    global tangens_angle_for_general_direction_degrees
    tangens_angle_for_general_direction_radians = np.arctan((delta_y)/(delta_x))
    tangens_angle_for_general_direction_degrees = tangens_angle_for_general_direction_radians * (360/(2*np.pi))
    print("Tan angle for direction:", tangens_angle_for_general_direction_degrees, "therefore IMAGE shifted", direction_x, direction_y)

    global new_direction_x
    global new_direction_y
    new_delta_x = x_11all_div-x_22all_div
    if new_delta_x > 0:
        new_direction_x = "left"
    elif new_delta_x < 0:
        new_direction_x = "right"
    else: 
        new_direction_x = "null"
    new_delta_y = y_11all_div-y_22all_div
    if new_delta_y > 0:
        new_direction_y = "up"
    elif new_delta_y < 0:
        new_direction_y = "down"
    else:
        new_direction_y = "null"

    new_delta_x = abs(new_delta_x)
    new_delta_y = abs(new_delta_y)
    global new_tangens_angle_for_general_direction_degrees
    new_tangens_angle_for_general_direction_radians = np.arctan((new_delta_y)/(new_delta_x))
    new_tangens_angle_for_general_direction_degrees = new_tangens_angle_for_general_direction_radians * (360/(2*np.pi))
    print("Tan angle for direction:", new_tangens_angle_for_general_direction_degrees, "therefore IMAGE shifted", new_direction_x, new_direction_y)

    return coordinates_1, coordinates_2

def calculate_mean_distance(coordinates_1, coordinates_2):
    all_distances = 0
    merged_coordinates = list(zip(coordinates_1, coordinates_2))
    for coordinate in merged_coordinates:
        x_difference = coordinate[0][0] - coordinate[1][0]
        y_difference = coordinate[0][1] - coordinate[1][1]
        distance = math.hypot(x_difference, y_difference)
        all_distances = all_distances + distance
    return all_distances / len(merged_coordinates)
import statistics

def calculate_median_tgangle(coordinates_1, coordinates_2):
    all_tgangles = []
    merged_coordinates = list(zip(coordinates_1, coordinates_2))
    for coordinate in merged_coordinates:
        x_difference = coordinate[0][0] - coordinate[1][0]
        y_difference = coordinate[0][1] - coordinate[1][1]
        if x_difference != 0:
            tgangle = y_difference / (x_difference)
            all_tgangles.append(tgangle)
    return statistics.median(all_tgangles)

def calculate_mean_tgangle(coordinates_1, coordinates_2):
    all_tgangles = 0
    merged_coordinates = list(zip(coordinates_1, coordinates_2))
    for coordinate in merged_coordinates:
        x_difference = coordinate[0][0] - coordinate[1][0]
        y_difference = coordinate[0][1] - coordinate[1][1]
        if x_difference !=0:
            tgangle = y_difference / (x_difference)
            all_tgangles = all_tgangles + tgangle
    return all_tgangles / len(merged_coordinates)


#def calculate_speed_in_kmps(feature_distance, GSD, time_difference):
#    distance = feature_distance * GSD / 100000
#    speed = distance / time_difference
#    return speed


image_1 = r'C:\Users\kiv\Downloads\eda\eda\sw1.jpg'
image_2 = r'C:\Users\kiv\Downloads\eda\eda\sw2.jpg'

#latitude_image_1 = -43.88975 #latitude před procesem
#latitude_image_2 = -44.18364 #latitude po procesu
#latitude_image_1 = 1 #latitude před procesem
#latitude_image_2 = -1 #latitude po procesu
#latitude_image_1 = -13.12361 #latitude před procesem madagaskar
#latitude_image_2 = -12.67333 #latitude po procesu madagaskar
#latitude_image_1 = -25.49306 #latitude před procesem namibie
#latitude_image_2 = -25.07194 #latitude po procesu namibie
latitude_image_1 = 51.61778 #latitude switzerland
latitude_image_2 = 51.55894 #latitude switzerland


#latitude_image_1 = -21.26222 #latitude namibie 1
#latitude_image_1 = -20.82889 #latitude namibie 2
#latitude_image_2 = -20.39417 #latitude namibie 3

#time_difference = get_time_difference(image_1, image_2) 
image_1_cv, image_2_cv = convert_to_cv(image_1, image_2) 
keypoints_1, keypoints_2, descriptors_1, descriptors_2 = calculate_features(image_1_cv, image_2_cv, 1000) 
matches = calculate_matches(descriptors_1, descriptors_2)
display_matches(image_1_cv, keypoints_1, image_2_cv, keypoints_2, matches)
coordinates_1, coordinates_2 = find_matching_coordinates(keypoints_1, keypoints_2, matches)
average_feature_distance = calculate_mean_distance(coordinates_1, coordinates_2)
#speed = calculate_speed_in_kmps(average_feature_distance, 12648, time_difference)
#print(speed)
#print(average_feature_distance)
average_tangens_angle = calculate_mean_tgangle(coordinates_1, coordinates_2)
#print("average_tangens_angle_radians", average_tangens_angle)
median_tangens_angle = calculate_median_tgangle(coordinates_1, coordinates_2)
#print("median_tangens_angle_radians", median_tangens_angle)

degrees_med = np.arctan(median_tangens_angle)*(360/(2*np.pi))
degrees_avg = np.arctan(average_tangens_angle)*(360/(2*np.pi))

print("mean_tangens_angle_degrees", degrees_med)
print("average_tangens_angle_degrees", degrees_avg)

#print("average_tangens_angle_radians", average_tangens_angle,"; median_tangens_angle_radians", median_tangens_angle,"; mean_tangens_angle_degrees", degrees_med, "; average_tangens_angle_degrees", degrees_avg)

tangens_angle_for_general_direction_degrees = abs(tangens_angle_for_general_direction_degrees)
new_tangens_angle_for_general_direction_degrees = abs(new_tangens_angle_for_general_direction_degrees)

edoov_coefficient = ""
if direction_x == "left":
    if direction_y == "up":
        edoov_coefficient = (tangens_angle_for_general_direction_degrees, -1, -1)
        reduced_edoov_coefficient = 270-tangens_angle_for_general_direction_degrees
    if direction_y == "down":
        edoov_coefficient = (tangens_angle_for_general_direction_degrees, -1, 1)
        reduced_edoov_coefficient = 270+tangens_angle_for_general_direction_degrees
if direction_x == "right":
    if direction_y == "up":
        edoov_coefficient = (tangens_angle_for_general_direction_degrees, 1, -1)
        reduced_edoov_coefficient = 90+tangens_angle_for_general_direction_degrees
    if direction_y == "down":
        edoov_coefficient = (tangens_angle_for_general_direction_degrees, 1, 1)
        reduced_edoov_coefficient = 90-tangens_angle_for_general_direction_degrees

new_edoov_coefficient = ""
if new_direction_x == "left":
    if new_direction_y == "up":
        new_edoov_coefficient = (new_tangens_angle_for_general_direction_degrees, -1, -1)
        new_reduced_edoov_coefficient = 270-new_tangens_angle_for_general_direction_degrees
    if new_direction_y == "down":
        new_edoov_coefficient = (new_tangens_angle_for_general_direction_degrees, -1, 1)
        new_reduced_edoov_coefficient = 270+new_tangens_angle_for_general_direction_degrees
if new_direction_x == "right":
    if new_direction_y == "up":
        new_edoov_coefficient = (new_tangens_angle_for_general_direction_degrees, 1, -1)
        new_reduced_edoov_coefficient = 90+new_tangens_angle_for_general_direction_degrees
    if new_direction_y == "down":
        new_edoov_coefficient = (new_tangens_angle_for_general_direction_degrees, 1, 1)
        new_reduced_edoov_coefficient = 90-new_tangens_angle_for_general_direction_degrees

negated_reduced_edoov_coefficient = reduced_edoov_coefficient+180
if negated_reduced_edoov_coefficient > 360:
    negated_reduced_edoov_coefficient-=360
print("obraz Matyas", reduced_edoov_coefficient)
print("let Matyas", negated_reduced_edoov_coefficient)

print("obraz Eda", new_reduced_edoov_coefficient)


latitude_avg = (latitude_image_1+latitude_image_2)/2

alpha_k=np.arcsin((np.cos(51.8*(np.pi/180)))/(np.cos(latitude_avg*(np.pi/180))))
alpha_k = alpha_k*(180/np.pi)
print("alpha:", alpha_k)
corrected_alpha_k=0
if latitude_image_1>latitude_image_2:
    corrected_alpha_k=180-alpha_k
else:
    corrected_alpha_k=alpha_k
print("corrected alpha", corrected_alpha_k)
clockwise_alpha_k=360-corrected_alpha_k
print("Clockwise ak: ",clockwise_alpha_k)


print("corrected alpha k:", corrected_alpha_k)
print("edoov koeficient: ", edoov_coefficient)
print("reduced edoov koeficient: ", reduced_edoov_coefficient)
print("new reduced edoov koeficient: ", new_reduced_edoov_coefficient)

poloha_severu=corrected_alpha_k-reduced_edoov_coefficient
print("Poloha severu: ",poloha_severu)

new_corrected_alpha_k=corrected_alpha_k
new_poloha_severu=0
if latitude_image_1>latitude_image_2:
    new_poloha_severu=new_corrected_alpha_k-new_reduced_edoov_coefficient+180
else:
    new_poloha_severu=new_corrected_alpha_k-new_reduced_edoov_coefficient

print("New Poloha severu: ",new_poloha_severu)

#print(time_difference)
print("patch size: 85")


# function to find best detected features using brute force
# matcher and match them according to there humming distance
def BF_FeatureMatcher(des1,des2):
    brute_force = cv2.BFMatcher(cv2.NORM_HAMMING,crossCheck=True)
    no_of_matches = brute_force.match(des1,des2)
  
    # finding the humming distance of the matches and sorting them
    no_of_matches = sorted(no_of_matches,key=lambda x:x.distance)
    return no_of_matches

# sorting the number of best matches obtained from brute force matcher
number_of_matches = BF_FeatureMatcher(descriptors_1,descriptors_2)
tot_feature_matches = len(number_of_matches)

# printing total number of feature matches found
print(f'Total Number of Features matches found are {tot_feature_matches}')
