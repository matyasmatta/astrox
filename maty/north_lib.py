import numpy as np
from exif import Image as exify


# this calculates calculating edoov_coefficient (=relative rotation of camera on ISS)
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
        
        # combining movemment of "things" to get edoov_coefficient (=relative rotation of camera on ISS) (between 0 and 360)
        edoov_coefficient = np.arctan2(delta_x,delta_y) * 57.29577951 + 180
        if edoov_coefficient >= 360:
            edoov_coefficient=edoov_coefficient-360
        return edoov_coefficient

    # using defined functions
    image_1_cv, image_2_cv = convert_to_cv(image_1, image_2) 
    keypoints_1, keypoints_2, descriptors_1, descriptors_2 = calculate_features(image_1_cv, image_2_cv, 1000) 
    matches = calculate_matches(descriptors_1, descriptors_2)
    edoov_coefficient = find_matching_coordinates(keypoints_1,keypoints_2,matches)

    # storing edoov_coefficient (=relative rotation of camera on ISS) for future usages              
    list.add_edoov_coefficient(edoov_coefficient)
    list_medianu = list.get_median()
    return list_medianu

# for fast calculation of north on picture
def find_north_fast(image_1, image_2):
    # getting coordinates of photo via exif
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
        # it is counterwise angle that tells us where is north pole towards the movement of ISS
        # if ISS is on 51° N the coefficient is 90°, when ISS moves to equator the coefficient is 135°
        # then when ISS approach 51° S is coefficient 90°, and when ISS moves to equator again, the coefficient is 45°
            # notice the equator situation, two coefficients for same place 
    alpha_k=np.arcsin(np.cos(51.8/57.29577951)/np.cos(latitude_avg/57.29577951)) * 57.29577951
    corrected_alpha_k=0
    # correcting "the equator situation" with looking if ISS moves up or down
    if latitude_image_1>latitude_image_2:
        corrected_alpha_k=180-alpha_k
    else:
        corrected_alpha_k=alpha_k
    
    # combinating both informations to get real position of north on photo
    north_position = 0 - corrected_alpha_k # zero previously edoov_coefficient
    if north_position < 0:
        north_position = north_position + 360
    return north_position