# importing the module
import cv2
import math   
import PySimpleGUI as sg
import numpy as np
import csv
from tkinter import messagebox
import tkinter as tk


list_of_cisilko = []
ultra_destroy = 0
size_of_everything = 1 # 1 je cca 505 px

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

def write_valid(tuple1, tuple2):
    global cisilkoout
    global list_of_clouds
    list_of_clouds.append(image_name)
    list_of_clouds.append(' ')
    list_of_clouds.append(str(cisilko))
    list_of_clouds.append('True')
    x1,y1 = tuple1
    x2,y2= tuple2
    list_of_clouds.append(str(x1))
    list_of_clouds.append(str(y1))
    list_of_clouds.append(str(x2))
    list_of_clouds.append(str(y2))
    distance_px = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    list_of_clouds.append(str(distance_px))
    distance_m=distance_px*126.8
    list_of_clouds.append(str(distance_m))
    with open('eda/output.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        # Zápis dat ze seznamu
        writer.writerow(list_of_clouds)

    list_of_clouds = list()

    print('NAPSAL JSEM USPESNY MRAK')
    fill()
    cv2.putText(img, "Set cloud", (300*size_of_everything, 520*size_of_everything), cv2.FONT_HERSHEY_SIMPLEX ,0.5*size_of_everything, (255, 0, 0), 2)
    cv2.imshow('image', img)

def write_invalid():
    list_to_write = []
    list_to_write.append(image_name)
    list_to_write.append(' ')
    list_to_write.append(str(cisilko))
    list_to_write.append('False')
    with open('eda/output.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        # Zápis dat ze seznamu
        writer.writerow(list_to_write)
    print('NAPSAL JSEM NEUSPESNY MRAK')
    fill()
    cv2.putText(img, "Set cloud", (300*size_of_everything, 520*size_of_everything), cv2.FONT_HERSHEY_SIMPLEX ,0.5*size_of_everything, (255, 0, 0), 2)
    cv2.imshow('image', img)


def click_event(event, x, y, parms, args):
    global first_point, second_point, cisilko
    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
        # displaying the coordinates
        # on the Shell

        # displaying the coordinates
        # on the image window
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, str(x) + ',' +str(y), (x, y), font,0.25*size_of_everything, (255, 0, 0), 1*size_of_everything)
        cv2.imshow('image', img)
        
        if first_point == (0, 0):
            first_point = (x, y)
            fill()
            cv2.putText(img, "Set shadow pixel", (300*size_of_everything, 520*size_of_everything), cv2.FONT_HERSHEY_SIMPLEX ,0.5*size_of_everything, (255, 0, 0), 2)
            cv2.imshow('image', img)
        else:
            second_point = (x, y)
            cv2.line(img, first_point, second_point, (256, 0, 0), 1*size_of_everything)
            print('Line coordinates are:', first_point, second_point)
            cv2.imshow('image', img)
            write_valid(first_point, second_point)
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
    for p in range (367):
        global ultra_destroy
        if ultra_destroy == 1:
            break
        for i in range(1,5):
            list_of_cisilko = []
            if ultra_destroy == 1:
                with open('eda/output.csv', mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['shiiiiit - ultra destroy'])
                break
            # reading the image
            global cisilko, image_name, list_of_clouds
            image_name = 'img_'+str(p)+'_'+str(i)
            #image_path = r'C:\Users\kiv\Downloads\AstroX\meta_yolo_5/meta_corrected_'+image_name+'.jpg.bmp'
            image_path = 'eda/meta_corrected_img_23_2.jpg.bmp'
            global img
            img = cv2.imread(image_path, 1)
            img = resize_image(img)
            img = cv2.copyMakeBorder(img, 0, int(25*size_of_everything), 0, 0, cv2.BORDER_CONSTANT, value=(255,255,255))
            img = cv2.putText(img, image_name, (10*size_of_everything, 520*size_of_everything), cv2.FONT_HERSHEY_SIMPLEX ,0.5*size_of_everything, (255, 0, 0), 2)
            # displaying the image
            cv2.imshow('image', img)
        
            # setting mouse handler for the image
            # and calling the click_event() function
            prev_key = None
            fill()
            cv2.putText(img, "Set cloud", (300*size_of_everything, 520*size_of_everything), cv2.FONT_HERSHEY_SIMPLEX ,0.5*size_of_everything, (255, 0, 0), 2)
            cv2.imshow('image', img)
            while True:

                # wait for a key to be pressed to exit
                key = cv2.waitKeyEx(0)
                validation = False

                #start skipnutí chopu
                if key == 45:  # Stisknuta klávesa '-'
                    print("Žádné mraky")
                    with open('eda/output.csv', mode='a', newline='') as file:
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
                    break
                #konec skipnutí chopu
                #nastavení čísílka
                if key == 2490368:  # Šipka nahoru
                    cisilko += 1
                    validation = True
                elif key == 2621440:  # Šipka dolů
                    cisilko -= 1
                    validation = True
                elif key == 2424832:  # Šipka doleva
                    cisilko -= 10
                    validation = True
                elif key == 2555904:  # Šipka doprava
                    cisilko += 10
                    validation = True
                elif key >= 48 and key <= 57:  # Kontrola, zda je stisknuto číslo 0 až 9
                    if prev_key is not None:
                        cisilko = int(chr(prev_key) + chr(key))
                        prev_key = None

                        validation = True
                    else:
                        prev_key = key
                        validation = False                                
                elif key == 27: #ESC
                    result = messagebox.askquestion("Potvrzení", "Opravdu chcete zrušit celý program?")
                    if result == "yes":
                        ultra_destroy = 1
                        break
                elif key == 98:
                    result = messagebox.askquestion("Potvrzení", "Opravdu chcete zrušit měření mraku?")
                    if result == "yes":
                        global first_point
                        first_point = (0, 0)
                        try:
                            list_of_cisilko.remove(cisilko)
                        except:
                            pass
                        validation = False
                        geting_pixels = False
                elif key == 105:
                    messagebox.showinfo('Udělané mraky', sorted(list_of_cisilko))
                elif key == 112:
                    result = messagebox.askquestion("Potvrzení", "Pokračovat na další mrak")
                    if result == "yes":
                        break
                #konec nastavení čísílka
                
                geting_pixels = False
                #start validace
                if validation == True:
                    list_of_cisilko.append(cisilko)
                    print('LIST OF CISILKO:',list_of_cisilko)
                    print("Currently working with:" + str(cisilko))
                    fill()
                    cv2.putText(img, "Validate", (300*size_of_everything, 520*size_of_everything), cv2.FONT_HERSHEY_SIMPLEX ,0.5*size_of_everything, (255, 0, 0), 2)
                    cv2.imshow('image', img)
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
                        geting_pixels = False
                        write_invalid()
                    elif key == 49 + annotation_mode:
                        print(cisilko, 'is valid, continue with distance')
                        geting_pixels = True
                    else:
                        messagebox.showinfo('Zpráva','Jiná klávesa než 0 nebo 1 - znovu napiš číslo mraku')
                        geting_pixels = False
                        validation = False
                #konec validace

                #start získání pixelů
                if geting_pixels == True:
                    fill()
                    cv2.putText(img, "Set cloud pixel", (300*size_of_everything, 520*size_of_everything), cv2.FONT_HERSHEY_SIMPLEX ,0.5*size_of_everything, (255, 0, 0), 2)
                    cv2.imshow('image', img)

                    cv2.setMouseCallback('image', click_event)
                #konec získání pixelů

    # close the window
    cv2.destroyAllWindows()

def destroy():
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        # Ukončení programu při stisknutí klávesy "q"
        cv2.destroyAllWindows()
        

def main():
    global first_point, second_point, list_of_clouds
    list_of_clouds = list()
    first_point = (0,0)
    second_point = (0,0)
    manual()


if __name__=="__main__":
    # 0 for Maty, 1 for Eda
    annotation_mode = 0
    with open('eda/output.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        # Zápis dat ze seznamu
        writer.writerow(('chop', 'error?','cloud number', 'valid', 'x mrak', 'y mrak', 'x stin', 'y stin', 'vzdalenost v px', 'vzdalenost v m', 'vyska slunce', 'vyska mraku'))
    list_of_clouds = []
    main()
