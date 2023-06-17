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
from tkinter.simpledialog import askstring

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

def write_to_csv(optional_arg1=(), optional_arg2=(), optional_arg3=()):
    global image_name, variable_getting_pixels, sorted_list_to_write, p, i
    list_to_write = []
    list_to_write.append(image_name)
    list_to_write.append(' ')
    list_to_write.append(str(cisilko))
    list_to_write.append(str(variable_getting_pixels))
    if variable_getting_pixels == True:
        x1,y1 = optional_arg2
        x2,y2= optional_arg3
        list_to_write.append(str(x1))
        list_to_write.append(str(y1))
        list_to_write.append(str(x2))
        list_to_write.append(str(y2))
        distance_px = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        list_to_write.append(str(distance_px))
        distance_m=distance_px*126.8
        list_to_write.append(str(distance_m))
        list_to_write.append(str(optional_arg1))
        altitude_rad = optional_arg1/180*np.pi
        cloud_high = math.tan(altitude_rad)*distance_m
        list_to_write.append(cloud_high)
        sorted_list_to_write.append((image_name, '', cisilko, variable_getting_pixels, x1, y1, x2, y2, distance_px, distance_m, optional_arg1, cloud_high, p, i))
    else:
        sorted_list_to_write.append((image_name, '', cisilko, variable_getting_pixels, '', '', '', '', '', '', '', '', p, i))
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

def write_sorted_1():
    # Otevření vstupního souboru CSV
    with open('eda\output_for_deleting.csv', 'r') as input_file:
        reader = csv.reader(input_file)
        rows = list(reader)

    # Vytvoření seznamu čísel ve třetím sloupci
    numbers = []
    for row in rows:
        number = row[2]
        numbers.append(number)

    #musí být seřazený za sebou
    # Kontrola, zda se v seznamu čísel vyskytují duplicity
    has_duplicates = False
    line_deleted = False
    updated_rows = []
    for i in range(len(numbers)):
        if line_deleted == False:
            row_i = rows[i]
            if i == len(numbers)-1:
                updated_rows.append(row_i)
                break
            j = i+1
            row_j = rows[j]
            if numbers[i] == numbers[j]:
                line_deleted = True
                if row_i[3] == 'True' and row_j[3] == 'True':
                    updated_rows.append(row_i)
                elif row_i[3] == 'True':
                    updated_rows.append(row_i)
                elif row_j[3] == 'True': 
                    updated_rows.append(row_j)
                else:
                    updated_rows.append(row_i)
            else:
                updated_rows.append(row_i)
        else:
            line_deleted = False


    # Otevření výstupního souboru CSV
    with open('eda\output_after_1.csv', 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        writer.writerows(updated_rows)

    with open('eda\output_for_deleting.csv', 'w') as file:
        file.truncate(0)

def write_sorted_2():
    # Otevření vstupního souboru CSV
    with open('eda\output_after_1.csv', 'r') as input_file:
        reader = csv.reader(input_file)
        rows = list(reader)

    # Vytvoření seznamu čísel ve třetím sloupci
    numbers = []
    for row in rows:
        number = row[2]
        numbers.append(number)

    #musí být seřazený za sebou
    # Kontrola, zda se v seznamu čísel vyskytují duplicity
    has_duplicates = False
    line_deleted = False
    updated_rows = []
    for i in range(len(numbers)):
        if line_deleted == False:
            row_i = rows[i]
            if i == len(numbers)-1:
                updated_rows.append(row_i)
                break
            j = i+1
            row_j = rows[j]
            if numbers[i] == numbers[j]:
                line_deleted = True
                if row_i[3] == 'True' and row_j[3] == 'True':
                    updated_rows.append(row_i)
                elif row_i[3] == 'True':
                    updated_rows.append(row_i)
                elif row_j[3] == 'True': 
                    updated_rows.append(row_j)
                else:
                    updated_rows.append(row_i)
            else:
                updated_rows.append(row_i)
        else:
            line_deleted = False



    # Otevření výstupního souboru CSV
    with open('eda\output_after_2.csv', 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        writer.writerows(updated_rows)
    with open('eda\output_after_1.csv', 'w') as file:
        file.truncate(0)

def click_event(event, x, y, parms, args):

    if event == cv2.EVENT_LBUTTONDOWN:
        #psaní textu
        cv2.putText(img, str(x) + ',' +str(y), (x, y), cv2.FONT_HERSHEY_SIMPLEX,0.25*size_of_everything, (255, 0, 0), 1*size_of_everything)
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
            write_to_csv(altitude, first_point, second_point)
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
    altitude2 = altitude(latitude, longitude, year, month, day, hour, minute, second)
    return altitude2


def main():
    global img, ultra_destroy, cisilko, list_of_cisilko, sorted_list_to_write, p, i
    ultra_destroy = 0
    global first_point, second_point
    first_point = (0,0)
    second_point = (0,0)
    global image_name
    for p in range (23,25):
        if ultra_destroy == 1:
            break     
        for i in range(1,5):
            list_of_cisilko = []
            sorted_list_to_write = []
            prev_key = None
            if ultra_destroy == 1:
                with open('eda/output2.csv', mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([image_name, 'shiiiiit - ultra destroy'])
                break
            # reading the image
            image_name = 'img_'+str(p)+'_'+str(i)
            #image_path = r'C:\Users\kiv\Downloads\AstroX\meta_yolo_5/meta_corrected_'+image_name+'.jpg.bmp'
            image_path = 'eda/14/meta_ai/metacorrected_'+image_name+'.jpg.bmp'
            image_path_for_sun = 'eda/img_'+str(p)+'.jpg'
            global altitude
            altitude = get_sun(image_path_for_sun)   
            img = cv2.imread(image_path, 1)
            img = resize_image(img)
            #přidat spodek
            img = cv2.copyMakeBorder(img, 0, int(25*size_of_everything), 0, 0, cv2.BORDER_CONSTANT, value=(255,255,255)) 
            #napsat jméno obrázku
            img = cv2.putText(img, image_name, (10*size_of_everything, 520*size_of_everything), cv2.FONT_HERSHEY_SIMPLEX ,0.5*size_of_everything, (255, 0, 0), 2)
            cv2.imshow('image', img)
        
            #psaní
            fill()
            cv2.putText(img, "Set cloud", (300*size_of_everything, 520*size_of_everything), cv2.FONT_HERSHEY_SIMPLEX ,0.5*size_of_everything, (255, 0, 0), 2)
            cv2.imshow('image', img)

            global getting_cisilko, variable_validation, variable_getting_pixels, max_cisilko
            getting_cisilko = True
            variable_validation = False
            variable_getting_pixels = False
            max_cisilko = 0
            old_cisilko = 0
            chop_skipped = False
            while True:
                # wait for a key to be pressed to exit
                key = cv2.waitKeyEx(0)
                print('klíč je:', key)             

                if key == 45:  # Stisknuta klávesa '-'
                    chop_skipped = True
                    print("Žádné mraky")
                    with open('eda/output2.csv', mode='a', newline='') as file:
                        writer = csv.writer(file)
                        # Zápis dat ze seznamu
                        writer.writerow((image_name, 'no clouds'))
                    with open('eda/output_after_2.csv', mode='a', newline='') as file:
                        writer = csv.writer(file)
                        # Zápis dat ze seznamu
                        writer.writerow((image_name, 'no clouds'))
                    break
                elif key == 43:  # Stisknuta klávesa '+'
                    chop_skipped = True
                    with open('eda/output2.csv', mode='a', newline='') as file:
                        writer = csv.writer(file)
                        # Zápis dat ze seznamu
                        writer.writerow((image_name, 'too bright'))  
                    with open('eda/output_After_2.csv', mode='a', newline='') as file:
                        writer = csv.writer(file)
                        # Zápis dat ze seznamu
                        writer.writerow((image_name, 'too bright'))  
                    break
                elif key == 110: #klávesa n - všechny mraky jsou nevalidní
                    chop_skipped = True
                    result = messagebox.askquestion("Potvrzení", "Jsou všechny mraky nevalidní?")
                    if result == "yes":
                        sorted_list_to_write_110 = []
                        variable_getting_pixels = False
                        max_cloud = int(askstring('Nejvyšší mrak', 'Jaké je nejvyšší číslo mraku na obrázku?'))
                        for cisilko in range(0,max_cloud+1):
                            write_to_csv()
                        for c in range(max_cloud+1):
                            sorted_list_to_write_110.append((image_name, '', c, 'False', '', '', '', '', '', '', '', '', p, i))
                        with open('eda/output_after_2.csv', mode='a', newline='') as file:
                            writer = csv.writer(file)
                            for tuple0 in sorted_list_to_write_110:
                                writer.writerow(tuple0)

                        break

                elif key == 27: #ESC
                    chop_skipped = True
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

                if variable_validation == True:
                    if cisilko > old_cisilko:
                        max_cisilko = cisilko
                    old_cisilko = cisilko
                
              #start validace
                if variable_validation == True:
                    getting_cisilko = False
                    list_of_cisilko.append(cisilko)

                    #napsání validate
                    fill()
                    cv2.putText(img, "Validate", (300*size_of_everything, 520*size_of_everything), cv2.FONT_HERSHEY_SIMPLEX ,0.5*size_of_everything, (255, 0, 0), 2)
                    cv2.imshow('image', img)
                    
                    #napsání Cloud No. XY
                    points = np.array([[100*size_of_everything, 505*size_of_everything],
                   [100*size_of_everything, 525*size_of_everything],
                   [300*size_of_everything, 525*size_of_everything],
                   [300*size_of_everything, 505*size_of_everything]], np.int32)
                    cv2.fillPoly(img, [points], (255, 255, 255))
                    cv2.imshow('image', img)  
                    cv2.putText(img, "Cloud No.:" + str(cisilko), (100*size_of_everything, 520*size_of_everything), cv2.FONT_HERSHEY_SIMPLEX ,0.5*size_of_everything, (255, 0, 0), 2)
                    cv2.imshow('image', img)

                    #samotná validace
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
                        variable_validation = False
                    else:
                        messagebox.showinfo('Zpráva','Jiná klávesa než 0 nebo 1 - znovu napiš číslo mraku')
                        getting_cisilko = True
                        variable_getting_pixels = False
                        variable_validation = False
                #konec validace

                #start získání pixelů
                if variable_getting_pixels == True:
                    variable_validation = False

                    #naspsání Set cloud pixel
                    fill()
                    cv2.putText(img, "Set cloud pixel", (300*size_of_everything, 520*size_of_everything), cv2.FONT_HERSHEY_SIMPLEX ,0.5*size_of_everything, (255, 0, 0), 2)
                    cv2.imshow('image', img)

                    #nevim moc co ale čeká (vlastně ne nebo nevím) to na kliknutí
                    cv2.setMouseCallback('image', click_event)

                    #zrušení měření jednoho mraku
                    if key == 98: #klávesa b
                        result = messagebox.askquestion("Potvrzení", "Opravdu chcete zrušit měření mraku?")
                        if result == "yes":
                            first_point = (0, 0)
                            try:
                                list_of_cisilko.remove(cisilko)
                            except:
                                pass
                            variable_validation = False
                            variable_getting_pixels = False
                            getting_cisilko = True
                #konec získání pixelů
            
            if chop_skipped == False:
                #napsání všech čísel
                for c in range(max(list_of_cisilko)+1):
                    if c not in list_of_cisilko:
                        sorted_list_to_write.append((image_name, '', c, 'False', '', '', '', '', '', '', '', '', p, i))
                with open('eda/output_for_deleting.csv', mode='a', newline='') as file:
                    writer = csv.writer(file)
                    new_sorted_list_to_write = sorted(sorted_list_to_write, key=lambda x: (x[-2], x[-1], x[2]))
                    for tuple0 in new_sorted_list_to_write:
                        writer.writerow(tuple0)
                write_sorted_1()
                write_sorted_2()

    # close the window
    cv2.destroyAllWindows()

if __name__=="__main__":
    # 0 for Maty, 1 for Eda
    annotation_mode = 0
    size_of_everything = 1 # 1 je cca 505 px
    with open('eda\output_for_deleting.csv', 'w') as file:
        file.truncate(0)
    with open('eda\output_after_1', 'w') as file:
        file.truncate(0)

    with open('eda/output2.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        # Zápis dat ze seznamu
        writer.writerow(('chop', 'error?','cloud number', 'valid', 'x mrak', 'y mrak', 'x stin', 'y stin', 'vzdalenost v px', 'vzdalenost v m', 'vyska slunce', 'vyska mraku'))
    with open('eda/output_after_2.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        # Zápis dat ze seznamu
        writer.writerow(('chop', 'error?','cloud number', 'valid', 'x mrak', 'y mrak', 'x stin', 'y stin', 'vzdalenost v px', 'vzdalenost v m', 'vyska slunce', 'vyska mraku', 'cislo img', 'cislo chopu'))
    main()
