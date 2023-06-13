# importing the module
import cv2
import math   
import PySimpleGUI as sg
import numpy as np
import csv
from tkinter import messagebox
import tkinter as tk
from PIL import Image
from skyfield import api
from skyfield.api import load
from exif import Image as exify


# function that does nothing
def do_nothing(*args):
    pass

def resize_image(img) :
    # Calculate new size
    width = int(img.shape[1] * size_of_everything)
    height = int(img.shape[0] * size_of_everything)
    dim = (width, height)
    # Resize image
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    return resized

def write_to_csv(optional_arg1=(), optional_arg2=()):
    global image_name, variable_getting_pixels
    list_to_write = []
    list_to_write.append(image_name)
    list_to_write.append(' ')
    list_to_write.append(str(cisilko))
    list_to_write.append(str(variable_getting_pixels))
    if variable_getting_pixels == True:
        x1,y1 = optional_arg1
        x2,y2= optional_arg2
        list_to_write.append(str(x1))
        list_to_write.append(str(y1))
        list_to_write.append(str(x2))
        list_to_write.append(str(y2))
        distance_px = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        list_to_write.append(str(distance_px))
        distance_m=distance_px*126.8
        list_to_write.append(str(distance_m))
        list_to_write.append(str(altitude))
        cloud_high = math.tan(altitude)*distance_m
        list_to_write.append(cloud_high)
    with open('eda/output2.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        # Zápis dat ze seznamu
        writer.writerow(list_to_write)
    fill()
    cv2.putText(img, "Set cloud", (300*size_of_everything, 520*size_of_everything), cv2.FONT_HERSHEY_SIMPLEX ,0.5*size_of_everything, (255, 0, 0), 2)
    cv2.imshow('image', img)
    points = np.array([[100*size_of_everything, 505*size_of_everything],
                   [100*size_of_everything, 525*size_of_everything],
                   [300*size_of_everything, 525*size_of_everything],
                   [300*size_of_everything, 505*size_of_everything]], np.int32)
    cv2.fillPoly(img, [points], (255, 255, 255))
    cv2.imshow('image', img)  
    global getting_cisilko
    getting_cisilko = True

def click_event(event, x, y, parms, args):
    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
        # displaying the coordinates
        # on the Shell
        # displaying the coordinates
        # on the image window
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, str(x) + ',' +str(y), (x, y), font,0.25*size_of_everything, (255, 0, 0), 1*size_of_everything)
        cv2.imshow('image', img)
        global first_point, second_point
        if first_point == (0, 0):
            first_point = (x, y)
            fill()
            cv2.putText(img, "Set shadow pixel", (300*size_of_everything, 520*size_of_everything), cv2.FONT_HERSHEY_SIMPLEX ,0.5*size_of_everything, (255, 0, 0), 2)
            cv2.imshow('image', img)
        else:
            second_point = (x, y)
            cv2.line(img, first_point, second_point, (256, 0, 0), 1*size_of_everything)
            cv2.imshow('image', img)
            write_to_csv(first_point, second_point)
            first_point = (0,0)
            second_point = (0,0)
            cv2.setMouseCallback('image', do_nothing)

def fill():
    points = np.array([[300*size_of_everything, 505*size_of_everything],
                   [300*size_of_everything, 525*size_of_everything],
                   [505*size_of_everything, 525*size_of_everything],
                   [505*size_of_everything, 505*size_of_everything]], np.int32)
    cv2.fillPoly(img, [points], (255, 255, 255))
    cv2.imshow('image', img)    

def manual():
    global img, altitude, list_of_clouds, first_point, second_point, ultra_destroy, cisilko, list_of_cisilko
    global image_name, variable_getting_pixels
    for p in range (367):
        if ultra_destroy == 1:
            break     
        for i in range(1,5):
            list_of_cisilko = []
            prev_key = None
            if ultra_destroy == 1:
                with open('eda/output2.csv', mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([image_name, 'shiiiiit - ultra destroy'])
                break
            # reading the image
            image_name = 'img_'+str(p)+'_'+str(i)
            #image_path = r'C:\Users\kiv\Downloads\AstroX\meta_yolo_5/meta_corrected_'+image_name+'.jpg.bmp'
            image_path = 'eda\meta_corrected_img_23_2.jpg.bmp'
            image_path_for_sun = 'eda/img_23.jpg'
            altitude = get_sun(image_path_for_sun)   
            img = cv2.imread(image_path, 1)
            img = resize_image(img)
            img = cv2.copyMakeBorder(img, 0, int(25*size_of_everything), 0, 0, cv2.BORDER_CONSTANT, value=(255,255,255))
            img = cv2.putText(img, image_name, (10*size_of_everything, 520*size_of_everything), cv2.FONT_HERSHEY_SIMPLEX ,0.5*size_of_everything, (255, 0, 0), 2)
            # displaying the image
            cv2.imshow('image', img)
        
            # setting mouse handler for the image
            # and calling the click_event() function
            fill()
            cv2.putText(img, "Set cloud", (300*size_of_everything, 520*size_of_everything), cv2.FONT_HERSHEY_SIMPLEX ,0.5*size_of_everything, (255, 0, 0), 2)
            cv2.imshow('image', img)
            getting_cisilko = True
            variable_validation = False
            variable_getting_pixels = False
            while True:

                # wait for a key to be pressed to exit
                key = cv2.waitKeyEx(0)
                print('klíč je:', key)             

                if key == 45:  # Stisknuta klávesa '-'
                    print("Žádné mraky")
                    with open('eda/output.csv', mode='a', newline='') as file:
                        writer = csv.writer(file)
                        # Zápis dat ze seznamu
                        writer.writerow((image_name, 'no clouds'))
                    with open('eda/output2.csv', mode='a', newline='') as file:
                        writer = csv.writer(file)
                        # Zápis dat ze seznamu
                        writer.writerow((image_name, 'no clouds'))
                    break
                elif key == 43:  # Stisknuta klávesa '+'
                    print("Obrázek je moc světlý") 
                    with open('eda/output.csv', mode='a', newline='') as file:
                        writer = csv.writer(file)
                        # Zápis dat ze seznamu
                        writer.writerow((image_name, 'too bright'))  
                    with open('eda/output2.csv', mode='a', newline='') as file:
                        writer = csv.writer(file)
                        # Zápis dat ze seznamu
                        writer.writerow((image_name, 'too bright'))  
                    break
                elif key == 27: #ESC
                    result = messagebox.askquestion("Potvrzení", "Opravdu chcete zrušit celý program?")
                    if result == "yes":
                        ultra_destroy = 1
                        break
                elif key == 105:
                    messagebox.showinfo('Udělané mraky', sorted(list_of_cisilko))
                elif key == 112:
                    result = messagebox.askquestion("Potvrzení", "Pokračovat na další obrázek?")
                    if result == "yes":
                        break
                #konec skipnutí chopu

                #nastavení čísílka
                if getting_cisilko == True:
                    variable_validation = True
                    if key == 2490368:  # Šipka nahoru
                        cisilko += 1
                    elif key == 2621440:  # Šipka dolů
                        cisilko -= 1
                    elif key == 2424832:  # Šipka doleva
                        cisilko -= 10
                    elif key == 2555904:  # Šipka doprava
                        cisilko += 10
                    elif key >= 48 and key <= 57:  # Kontrola, zda je stisknuto číslo 0 až 9
                        if prev_key is not None:
                            cisilko = int(chr(prev_key) + chr(key))
                            prev_key = None
                        else:
                            prev_key = key
                            variable_validation = False                                
                    #konec nastavení čísílka
                    
              #start validace
                if variable_validation == True:
                    getting_cisilko = False
                    list_of_cisilko.append(cisilko)
                    fill()
                    cv2.putText(img, "Validate", (300*size_of_everything, 520*size_of_everything), cv2.FONT_HERSHEY_SIMPLEX ,0.5*size_of_everything, (255, 0, 0), 2)
                    cv2.imshow('image', img)
                    
                    #napsání CLoud No. XY
                    points = np.array([[100*size_of_everything, 505*size_of_everything],
                   [100*size_of_everything, 525*size_of_everything],
                   [300*size_of_everything, 525*size_of_everything],
                   [300*size_of_everything, 505*size_of_everything]], np.int32)
                    cv2.fillPoly(img, [points], (255, 255, 255))
                    cv2.imshow('image', img)  
                    cv2.putText(img, "Cloud No.:" + str(cisilko), (100*size_of_everything, 520*size_of_everything), cv2.FONT_HERSHEY_SIMPLEX ,0.5*size_of_everything, (255, 0, 0), 2)
                    cv2.imshow('image', img)
                                        
                    key = cv2.waitKey(0)
                    if key == 48 + annotation_mode:
                        print(cisilko, 'is not valid')
                        variable_getting_pixels = False
                        getting_cisilko = True
                        variable_validation = False
                        write_to_csv()
                    elif key == 49 + annotation_mode:
                        print(cisilko, 'is valid, continue with distance')
                        variable_getting_pixels = True
                    else:
                        messagebox.showinfo('Zpráva','Jiná klávesa než 0 nebo 1 - znovu napiš číslo mraku')
                        getting_cisilko = True
                        variable_getting_pixels = False
                        variable_validation = False
                #konec validace

                #start získání pixelů
                if variable_getting_pixels == True:
                    variable_validation = False
                    fill()
                    cv2.putText(img, "Set cloud pixel", (300*size_of_everything, 520*size_of_everything), cv2.FONT_HERSHEY_SIMPLEX ,0.5*size_of_everything, (255, 0, 0), 2)
                    cv2.imshow('image', img)
                    cv2.setMouseCallback('image', click_event)
                    if key == 98:
                        result = messagebox.askquestion("Potvrzení", "Opravdu chcete zrušit měření mraku?")
                        if result == "yes":
                            global first_point
                            first_point = (0, 0)
                            try:
                                list_of_cisilko.remove(cisilko)
                            except:
                                pass
                            variable_validation = False
                            variable_getting_pixels = False
                            getting_cisilko = True
                #konec získání pixelů

    # close the window
    cv2.destroyAllWindows()

def get_sun(image_path):
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
    # this is a small class containing a method for date extraction that is not via the EXIF library but the PIL library
    def find_time_from_image(image_path):
        img = Image.open(image_path)
        img_exif_dict = img.getexif()
        date = str(img_exif_dict[306])

        year = int(date[0:4])
        month = int(date[5:7])
        day = int(date[8:10])
        hour = int(date[11:13])
        minute = int(date[14:16])
        second = int(date[17:19])

        return year, month, day, hour, minute, second

    def altitude(coordinates_latitude, coordinates_longtitude, year, month, day, hour, minute, second):
        # use the NASA API to be able to calculate sun's position
        ts = api.load.timescale()
        ephem = api.load("de421.bsp")

        # define sky objects
        sun = ephem["Sun"]
        earth = ephem["Earth"]

        # given coordinates calculate the altitude (how many degrees sun is above the horizon), additional data is redundant
        location = api.Topos(coordinates_latitude, coordinates_longtitude, elevation_m=500)
        sun_pos = (earth + location).at(ts.tt(year,month,day,hour,minute,second)).observe(sun).apparent()
        altitude, azimuth, distance = sun_pos.altaz()
        altitude= float(altitude.degrees)
        return(altitude)
    year, month, day, hour, minute, second = find_time_from_image(image_path)
    latitude = get_latitude(image_path)
    longitude = get_longitude(image_path)

    # now we calculate the sun altitude using a function
    altitude = altitude(latitude, longitude, year, month, day, hour, minute, second)
    return altitude
'''
def validation():

def getting_pixels():'''

def main():
    global altitude, list_of_clouds, first_point, second_point, ultra_destroy
    altitude = 0
    list_of_clouds = list()
    first_point = (0,0)
    second_point = (0,0)
    ultra_destroy = 0
    manual()


if __name__=="__main__":
    # 0 for Maty, 1 for Eda
    annotation_mode = 0
    size_of_everything = 1 # 1 je cca 505 px
    with open('eda/output2.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        # Zápis dat ze seznamu
        writer.writerow(('chop', 'error?','cloud number', 'valid', 'x mrak', 'y mrak', 'x stin', 'y stin', 'vzdalenost v px', 'vzdalenost v m', 'vyska slunce', 'vyska mraku'))
    main()
