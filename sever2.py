#import stiny_maty
from exif import Image
from datetime import datetime
import cv2
import numpy as np
import statistics
import list

# This is code for better calculation of position of north on photo
# We did analyze on example data which were on raspberry and found that compass can be easy affected by other magnetic fields. The difference between the correct position of north and the data from compass were sometimes different by 30 degrees
# So we invented equation that describe position of north towards positition of ISS (the ISS is looking in the direction of its flight).
# Then we are calculating relative rotation of a camera towards the ISS with opencv . We are tracking the movement of picture on compering it to the movement of the ISS on then calculating the relative rotation of camera on ISS

#for acessing program via other .py file
def find_north(image_1, image_2):

    #converting images to cv friendly readable format 
    def convert_to_cv(image_1, image_2):
        image_1_cv = cv2.imread(image_1, 0)
        image_2_cv = cv2.imread(image_2, 0)
        return image_1_cv, image_2_cv

    #finding same "things" on both images
    def calculate_features(image_1_cv, image_2_cv, feature_number):
        orb = cv2.ORB_create(nfeatures = feature_number)
        keypoints_1, descriptors_1 = orb.detectAndCompute(image_1_cv, None)
        keypoints_2, descriptors_2 = orb.detectAndCompute(image_2_cv, None)
        return keypoints_1, keypoints_2, descriptors_1, descriptors_2

    #connecting same "things" on photo
    def calculate_matches(descriptors_1, descriptors_2):
        try:
            brute_force = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
            matches = brute_force.match(descriptors_1, descriptors_2)
            matches = sorted(matches, key=lambda x: x.distance)
            return matches
        except:
            return 0
        
    #nic čeho se obávat
    def hack_ISS():
        h=[]
        all_informations = 1000101
        h.append(all_informations)

    #finding coordination of same "things" on both fotos
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
            #we store all matched coordinates to list for further calculation
            x_11all.append(x1)
            x_22all.append(x2)
            y_11all.append(y1)
            y_22all.append(y2)
        #this calculates us the median of all coordinations on output [x1, y1] and [x2,y2]

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

        #we calculate the angle of movemment of "things" on photo
        delta_x = x_22all_div - x_11all_div
        delta_y = y_11all_div - y_22all_div
        
        edoov_coefficient = np.arctan2(delta_x,delta_y) * 57.29577951 - 180
        return edoov_coefficient
    
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

    #using defined functions
    latitude_image_1, latitude_image_2 = get_latitudes(image_1, image_2)
    image_1_cv, image_2_cv = convert_to_cv(image_1, image_2) 
    keypoints_1, keypoints_2, descriptors_1, descriptors_2 = calculate_features(image_1_cv, image_2_cv, 1000) 
    matches = calculate_matches(descriptors_1, descriptors_2)
    edoov_coefficient = find_matching_coordinates(keypoints_1,keypoints_2,matches)
    #calculating the relative rotation of camera on ISS
    list.add_clockwise_edoov_coefficient(edoov_coefficient) 
    median_edoov_coefficient=list.get_median()
    #averaging latitudes for more accurate calculation 
    latitude_avg = (latitude_image_1+latitude_image_2)/2
    #print("coef:",median_edoov_coefficient)
    #calculating the relative position of north for ISS (looks forward)
    alpha_k=np.arcsin(np.cos(51.8/57.29577951)/np.cos(latitude_avg/57.29577951)) * 57.29577951
    corrected_alpha_k=0
    if latitude_image_1>latitude_image_2:
        corrected_alpha_k=180-alpha_k
    else:
        corrected_alpha_k=alpha_k
    #print("corralpha:", corrected_alpha_k)
    #combinating both informations to get real position of north on photo
    poloha_severu = median_edoov_coefficient - corrected_alpha_k
    if poloha_severu < 0:
        poloha_severu = poloha_severu + 360
    return poloha_severu

counter=234
timeted = datetime.now()
for i in range(130):
    i_1=str(counter)
    before = "eda\direction12\photo_18"
    image_1=str(before + i_1 +".jpg")
    i_2=str(counter+1)
    #print(image_1)
    image_2=str(before + i_2 +".jpg")
    #print(image_2)

    data = find_north(image_1, image_2)
    print(data)
    counter+=1
print(datetime.now()- timeted)