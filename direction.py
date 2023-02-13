from exif import Image
from datetime import datetime
import cv2
import math


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
    print(time_difference)
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

image_2 = 'dataset\original_all\photo_07473_51845707716_o.jpg'
image_1 = 'dataset\original_all\photo_07472_51844776372_o.jpg'

def display_matches(image_1_cv, keypoints_1, image_2_cv, keypoints_2, matches):
    match_img = cv2.drawMatches(image_1_cv, keypoints_1, image_2_cv, keypoints_2, matches[:100], None)
    resize = cv2.resize(match_img, (1600,600), interpolation = cv2.INTER_AREA)
    cv2.imshow('matches', resize)
    cv2.waitKey(0)
    cv2.destroyWindow('matches')

def find_matching_coordinates(keypoints_1, keypoints_2, matches):
    coordinates_1 = []
    coordinates_2 = []
    for match in matches:
        image_1_idx = match.queryIdx
        image_2_idx = match.trainIdx
        (x1,y1) = keypoints_1[image_1_idx].pt
        (x2,y2) = keypoints_2[image_2_idx].pt
        coordinates_1.append((x1,y1))
        coordinates_2.append((x2,y2))
    return coordinates_1, coordinates_2

#def calculate_mean_distance(coordinates_1, coordinates_2):
#    all_distances = 0
#    merged_coordinates = list(zip(coordinates_1, coordinates_2))
#    for coordinate in merged_coordinates:
#        x_difference = coordinate[0][0] - coordinate[1][0]
#        y_difference = coordinate[0][1] - coordinate[1][1]
#        distance = math.hypot(x_difference, y_difference)
#        all_distances = all_distances + distance
#    return all_distances / len(merged_coordinates)
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

time_difference = get_time_difference(image_1, image_2) 
image_1_cv, image_2_cv = convert_to_cv(image_1, image_2) 
keypoints_1, keypoints_2, descriptors_1, descriptors_2 = calculate_features(image_1_cv, image_2_cv, 1000) 
matches = calculate_matches(descriptors_1, descriptors_2)
display_matches(image_1_cv, keypoints_1, image_2_cv, keypoints_2, matches)
coordinates_1, coordinates_2 = find_matching_coordinates(keypoints_1, keypoints_2, matches)
#average_feature_distance = calculate_mean_distance(coordinates_1, coordinates_2)
#speed = calculate_speed_in_kmps(average_feature_distance, 12648, time_difference)
#print(speed)
#print(average_feature_distance)
average_tangens_angle = calculate_mean_tgangle(coordinates_1, coordinates_2)
print(average_tangens_angle)
median_tangens_angle = calculate_median_tgangle(coordinates_1, coordinates_2)
print(median_tangens_angle)