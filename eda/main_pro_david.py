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
        distance_m=distance_px*126.48
        list_to_write.append(str(distance_m))
        list_to_write.append(str(optional_arg1))
        altitude_rad = optional_arg1/180*np.pi
        cloud_high = math.tan(altitude_rad)*distance_m
        list_to_write.append(cloud_high)
        sorted_list_to_write.append([image_name, '', cisilko, variable_getting_pixels, x1, y1, x2, y2, distance_px, distance_m, optional_arg1, cloud_high, p, i])
    else:
        sorted_list_to_write.append([image_name, '', cisilko, variable_getting_pixels, '', '', '', '', '', '', '', '', p, i])
    with open('eda/david/output2.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        # Zápis dat ze seznamu
        writer.writerow(list_to_write)
    fill()
    cv2.putText(img, "Set cloud", (int(300*size_of_everything), int(520*size_of_everything)), cv2.FONT_HERSHEY_SIMPLEX, 0.5*size_of_everything, (255, 0, 0), 2)
    cv2.imshow('image', img)
    points = np.array([[int(100*size_of_everything), int(505*size_of_everything)],
                   [int(100*size_of_everything), int(525*size_of_everything)],
                   [int(300*size_of_everything), int(525*size_of_everything)],
                   [int(300*size_of_everything), int(505*size_of_everything)]], np.int32)
    cv2.fillPoly(img, [points], (255, 255, 255))
    cv2.imshow('image', img)  
    global getting_cisilko
    getting_cisilko = True

class new_csv():
    def write_missing(rows):
        # Vytvoření seznamu čísel ve třetím sloupci
        numbers = []
        for row in rows:
            number = int(row[2])
            numbers.append(number)
        image_name = row[0]
        p=row[-2]
        i=row[-1]
        for y in range(max(numbers)):
            if y not in numbers:
                rows.append([image_name, '', y, 'False', '', '', '', '', '', '', '', '', p, i])
        print(rows)    
        return rows

    def write_sorted(rows):  
        # Vytvoření seznamu čísel ve třetím sloupci
        numbers = []
        for row in rows:
            number = row[2]
            numbers.append(number)
        for i in range(len(numbers)-1):
            numbers = []
            for row in rows:
                number = row[2]
                numbers.append(number)
            for j in range(i+1, len(numbers)):
                if numbers[i] == numbers[j]:
                    row_i = rows[i]
                    row_j = rows[j]
                    if row_i[3] ==True and row_j[3] ==True:
                        rows.remove(row_j)
                        break
                    elif row_i[3] ==True:
                        rows.remove(row_j)
                        break
                    elif row_j[3] ==True: 
                        rows.remove(row_i)
                        break
                    else:
                        rows.remove(row_i)
                        break
        sorted_rows = sorted(rows, key=lambda x: (x[-2], x[-1], x[2]))

        print(sorted_rows)
        return sorted_rows

    def write_sorted_csv(rows):
        with open('eda\david/output_pro', 'w', newline='') as output_file:
            writer = csv.writer(output_file)
            writer.writerows(rows)

def click_event(event, x, y, parms, args):

    if event == cv2.EVENT_LBUTTONDOWN:
        #psaní textu
        cv2.putText(img, str(x) + ',' +str(y), (x, y), cv2.FONT_HERSHEY_SIMPLEX,0.25*size_of_everything, (255, 0, 0), int(int(1*size_of_everything)))
        cv2.imshow('image', img)

        global first_point, second_point
        if first_point == (0, 0):
            first_point = (x, y)
            fill()
            cv2.putText(img, "Set shadow pixel", (int(300*size_of_everything), int(520*size_of_everything)), cv2.FONT_HERSHEY_SIMPLEX ,0.5*size_of_everything, (255, 0, 0), 2)
            cv2.imshow('image', img)
        else:
            second_point = (x, y)
            cv2.line(img, first_point, second_point, (256, 0, 0), int(1*size_of_everything))
            cv2.imshow('image', img)
            write_to_csv(altitude, first_point, second_point)
            first_point = (0,0)
            second_point = (0,0)
            cv2.setMouseCallback('image', do_nothing)

def fill():
    points = np.array([[int(300*size_of_everything), int(505*size_of_everything)],
                   [int(300*size_of_everything), int(525*size_of_everything)],
                   [int(505*size_of_everything), int(525*size_of_everything)],
                   [int(505*size_of_everything), int(505*size_of_everything)]], np.int32)
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
    for p in range (12,36):
        if ultra_destroy == 1:
            break     
        for i in range(1,5):
            list_of_cisilko = []
            sorted_list_to_write = []
            prev_key = None
            if ultra_destroy == 1:
                with open('eda/david/output_pro.csv', mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([image_name, 'shiiiiit - ultra destroy'])
                break
            # reading the image
            image_name = 'img_'+str(p)+'_'+str(i)
            #image_path = r'C:\Users\kiv\Downloads\AstroX\meta_yolo_5/meta_corrected_'+image_name+'.jpg.bmp'
            image_path = r'C:\Users\kiv\Downloads\cops/meta'+image_name+'.jpg.bmp'
            image_path_for_sun = r'C:\Users\kiv\Downloads\gh/img_'+str(p)+'.jpg'
            global altitude
            altitude = get_sun(image_path_for_sun)   
            img = cv2.imread(image_path, 1)
            img = resize_image(img)
            #přidat spodek
            img = cv2.copyMakeBorder(img, 0, int(25*size_of_everything), 0, 0, cv2.BORDER_CONSTANT, value=(255,255,255)) 
            #napsat jméno obrázku
            img = cv2.putText(img, image_name, (int(10*size_of_everything), int(520*size_of_everything)), cv2.FONT_HERSHEY_SIMPLEX, 0.5*size_of_everything, (255, 0, 0), 2)
            cv2.imshow('image', img)
        
            #psaní
            fill()  
            cv2.putText(img, "Set cloud", (int(300*size_of_everything), int(520*size_of_everything)), cv2.FONT_HERSHEY_SIMPLEX, 0.5*size_of_everything, (255, 0, 0), 2)            
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
                    with open('eda/david/output2.csv', mode='a', newline='') as file:
                        writer = csv.writer(file)
                        # Zápis dat ze seznamu
                        writer.writerow((image_name, 'no clouds'))
                    with open('eda/david/output_pro.csv', mode='a', newline='') as file:
                        writer = csv.writer(file)
                        # Zápis dat ze seznamu
                        writer.writerow((image_name, 'no clouds'))
                    break
                elif key == 43:  # Stisknuta klávesa '+'
                    chop_skipped = True
                    with open('eda/david/output2.csv', mode='a', newline='') as file:
                        writer = csv.writer(file)
                        # Zápis dat ze seznamu
                        writer.writerow((image_name, 'too bright'))  
                    with open('eda/david/output_pro.csv', mode='a', newline='') as file:
                        writer = csv.writer(file)
                        # Zápis dat ze seznamu
                        writer.writerow((image_name, 'too bright'))  
                    break
                elif key == 27: #ESC
                    chop_skipped = True
                    result = messagebox.askquestion("Potvrzení", "Opravdu chcete zrušit celý program?")
                    if result == "yes":
                        ultra_destroy = 1
                        break
                elif key == 105:
                    messagebox.showinfo('Udělané mraky', sorted(list_of_cisilko))
                elif key == 112 or key == 110: #klávesa p nebo n
                    result = messagebox.askquestion("Potvrzení", "Pokračovat na další obrázek?")
                    if result == "yes":
                        break
                    if result == 'no':
                        messagebox.showinfo('Zpráva', 'Špatná odpoveď, nejde to vrátit')
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
                    cv2.putText(img, "Validate", (int(300*size_of_everything), int(520*size_of_everything)), cv2.FONT_HERSHEY_SIMPLEX, int(0.5*size_of_everything), (255, 0, 0), 2)                    
                    cv2.imshow('image', img)
                    
                    #napsání Cloud No. XY
                    points = np.array([[int(100*size_of_everything), int(505*size_of_everything)],
                                        [int(100*size_of_everything), int(525*size_of_everything)],
                                        [int(300*size_of_everything), int(525*size_of_everything)],
                                        [int(300*size_of_everything), int(505*size_of_everything)]], np.int32)
                    cv2.fillPoly(img, [points], (255, 255, 255))
                    cv2.imshow('image', img)  
                    cv2.putText(img, "Cloud No.:" + str(cisilko), (int(100*size_of_everything), int(520*size_of_everything)), cv2.FONT_HERSHEY_SIMPLEX ,0.5*size_of_everything, (255, 0, 0), 2)
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
                    cv2.putText(img, "Set cloud pixel", (int(300*size_of_everything), int(520*size_of_everything)), cv2.FONT_HERSHEY_SIMPLEX ,0.5*size_of_everything, (255, 0, 0), 2)
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
                print(sorted_list_to_write)
                try:
                    rows=new_csv.write_missing(sorted_list_to_write)
                    rows=new_csv.write_sorted(rows)
                    new_csv.write_sorted_csv(rows)
                except:
                    with open('eda/david/output_pro.csv', mode='a', newline='') as file:
                        writer = csv.writer(file)
                        # Zápis dat ze seznamu
                        writer.writerow((image_name, 'Sum Ting Wong'))  
      
                        
    # close the window
    cv2.destroyAllWindows()

if __name__=="__main__":
    # 0 for Maty, 1 for Eda
    annotation_mode = 0
    size_of_everything = 2.15 # 1 je cca 505 px
    size_int = int(size_of_everything)
    print(size_int)
    with open('eda/david/output2.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        # Zápis dat ze seznamu
        writer.writerow(('chop', 'error?','cloud number', 'valid', 'x mrak', 'y mrak', 'x stin', 'y stin', 'vzdalenost v px', 'vzdalenost v m', 'vyska slunce', 'vyska mraku'))
    with open('eda/david/output_pro.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        # Zápis dat ze seznamu
        writer.writerow(('chop', 'error?','cloud number', 'valid', 'x mrak', 'y mrak', 'x stin', 'y stin', 'vzdalenost v px', 'vzdalenost v m', 'vyska slunce', 'vyska mraku', 'cislo img', 'cislo chopu', 'size of everything je:'+str(size_of_everything)))
    main()
