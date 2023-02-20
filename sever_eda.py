from exif import Image
from datetime import datetime
import cv2
import math
import numpy as np
import statistics
from time import sleep
import statistics

# This is code for better calculation of position of north on photo
# We did analyze on example data which were on raspberry and found that compass can be easy affected by other magnetic fields. The difference between the correct position of north and the data from compass were sometimes different by 30 degrees
# So we invented equation that describe position of north towards positition of ISS (the ISS is looking in the direction of its flight).
# Then we are calculating relative rotation of a camera towards the ISS with opencv . We are tracking the movement of picture on compering it to the movement of the ISS on then calculating the relative rotation of camera on ISS

#for acessing program via other .py file
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

        x_11all_div=statistics.median(x_11all)
        x_22all_div=statistics.median(x_22all)
        y_11all_div=statistics.median(y_11all)
        y_22all_div=statistics.median(y_22all)
        
        #není nutné to dělit do 4 kvadrantů protože mega op funkce arctan2 to udělá za nás

        #we calculate the angle of movemment of "things" on photo
        delta_x = x_11all_div - x_22all_div
        #y jde v opačném směru (dolů) než je obvyklé pro práci s tangens, proto bude lepší odečítat y1 od y2
        delta_y = y_22all_div - y_11all_div
        
        edoov_coefficient = np.arctan2(delta_y,delta_x) * 57.29577951
        return coordinates_1, coordinates_2, edoov_coefficient
    
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
        cv2.waitKey(0)
        cv2.destroyAllWindows()



    #using defined functions
    latitude_image_1, latitude_image_2 = get_latitudes(image_1, image_2)
    time_difference = get_time_difference(image_1, image_2) 
    image_1_cv, image_2_cv = convert_to_cv(image_1, image_2) 
    keypoints_1, keypoints_2, descriptors_1, descriptors_2 = calculate_features(image_1_cv, image_2_cv, 1000) 
    matches = calculate_matches(descriptors_1, descriptors_2)
    #display_matches(image_1_cv, keypoints_1, image_2_cv, keypoints_2, matches)
    coordinates_1, coordinates_2, edoov_coefficient = find_matching_coordinates(keypoints_1,keypoints_2,matches)
    #calculating the relative rotation of camera on ISS
    store_edoov_coefficient = []
    store_edoov_coefficient.append(edoov_coefficient) 
    median_edoov_coefficient=statistics.median(store_edoov_coefficient)
    #averaging latitudes for more accurate calculation 
    latitude_avg = (latitude_image_1+latitude_image_2)/2

    #calculating the relative position of north for ISS (looks forward)
    alpha_k=np.arcsin(np.cos(51.8/57.29577951)/np.cos(latitude_avg/57.29577951))
    alpha_k = alpha_k * 57.29577951
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
    poloha_severu = - 90 - median_edoov_coefficient - corrected_alpha_k
    #print("Poloha severu: ",poloha_severu)
#    print(latitude_image_1, latitude_image_2)
    #print(list.get_median())
    #show_north(poloha_severu)
    #print(list.get_list())
    #return poloha_severu
    return poloha_severu
north = find_north("52652396850_976568dfb4_o.jpg","52652437058_efecd1212a_o.jpg")
print(north)
