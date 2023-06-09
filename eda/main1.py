# importing the module
import cv2
import math   
import PySimpleGUI as sg
import numpy as np

# function that does nothing
def do_nothing(*args):
    pass

def resize_image(img, scale_percent) :
    # Calculate new size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    # Resize image
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    return resized

def distance(tuple1, tuple2):
    x1,y1=tuple1
    x2,y2=tuple2
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    print('Distance in pixels:', distance)
    list_of_clouds.append((image_name, cisilko, 'True', distance))
    fill()
    cv2.putText(img, "Set cloud", (600, 1040), cv2.FONT_HERSHEY_SIMPLEX ,1, (255, 0, 0), 2)
    cv2.imshow('image', img)
    return 
def click_event(event, x, y, parms, args):
    global first_point, second_point, cisilko
    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
        # displaying the coordinates
        # on the Shell

        # displaying the coordinates
        # on the image window
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, str(x) + ',' +str(y), (x, y), font,0.5, (255, 0, 0), 2)
        cv2.imshow('image', img)
        
        if first_point == (0, 0):
            first_point = (x, y)
            fill()
            cv2.putText(img, "Set shadow pixel", (600, 1040), cv2.FONT_HERSHEY_SIMPLEX ,1, (255, 0, 0), 2)
            cv2.imshow('image', img)
        else:
            second_point = (x, y)
            cv2.line(img, first_point, second_point, (256, 0, 0), 3)
            print('Line coordinates are:', first_point, second_point)
            cv2.imshow('image', img)
            distance(first_point, second_point)
            first_point = (0,0)
            second_point = (0,0)
            cv2.setMouseCallback('image', do_nothing)
def fill():
    points = np.array([[600, 1010], [600, 1050], [1010, 1050], [1010, 1010]], np.int32)
    cv2.fillPoly(img, [points], (255, 255, 255))
    cv2.imshow('image', img)    
def manual():
    for p in range (367):
        for i in range(1,5):
            # reading the image
            global cisilko, image_name, list_of_clouds
            image_name = 'img_'+str(p)+'_'+str(i)
            image_path = r'C:\Users\kiv\Downloads\AstroX\meta_yolo_5/meta_corrected_'+image_name+'.jpg.bmp'
            global img
            img = cv2.imread(image_path, 1)
            img = resize_image(img, 200)
            img = cv2.copyMakeBorder(img, 0, 50, 0, 0, cv2.BORDER_CONSTANT, value=(255,255,255))
            img = cv2.putText(img, image_name, (20, 1040), cv2.FONT_HERSHEY_SIMPLEX ,1, (255, 0, 0), 2)
            # displaying the image
            cv2.imshow('image', img)
        
            # setting mouse handler for the image
            # and calling the click_event() function
            prev_key = None

            while True:
                cv2.putText(img, "Set cloud", (600, 1040), cv2.FONT_HERSHEY_SIMPLEX ,1, (255, 0, 0), 2)
                cv2.imshow('image', img)
                
                # wait for a key to be pressed to exit
                key = cv2.waitKey(0)
                if key >= 48 and key <= 57:  # Kontrola, zda je stisknuto číslo 0 až 9
                    if prev_key is not None:
                        fill()
                        cv2.putText(img, "Validate", (600, 1040), cv2.FONT_HERSHEY_SIMPLEX ,1, (255, 0, 0), 2)
                        cv2.imshow('image', img)
                        cisilko = int(chr(prev_key) + chr(key))
                        print("Currently working with:" + str(cisilko))
                        prev_key = None
                        points = np.array([[200, 1010], [200, 1050], [600, 1050], [600, 1010]], np.int32)
                        cv2.fillPoly(img, [points], (255, 255, 255))
                        cv2.imshow('image', img)  
                        cv2.putText(img, "Cloud No.:" + str(cisilko), (200, 1040), cv2.FONT_HERSHEY_SIMPLEX ,1, (255, 0, 0), 2)
                        cv2.imshow('image', img)
                        key = cv2.waitKey(0)
                        if key == 48 + annotation_mode:
                            print(cisilko, 'is not valid')
                        elif key == 49 + annotation_mode:
                            print(cisilko, 'is valid, continue with distance')
                            fill()
                            cv2.putText(img, "Set cloud pixel", (600, 1040), cv2.FONT_HERSHEY_SIMPLEX ,1, (255, 0, 0), 2)
                            cv2.imshow('image', img)
                            cv2.setMouseCallback('image', click_event)
                        elif key == 50 + annotation_mode:
                            print("Image", image_name, "was skipped.")
                            break
                        else:
                            print('Invalid key was pressed')
                    else:
                        prev_key = key
                elif key == 27: #ESC
                    print("Image", image_name, "was skipped.")
                    break
            print('\n----\n\nFINÁLNÍ LIST\n', (list_of_clouds))
            with open('output.txt', 'a') as file:
                # Zápis seznamu do souboru
                file.write(image_path)
                file.write('\n')
                for item in list_of_clouds:
                    file.write(str(item) + '\n')
                file.write('\n')
            list_of_clouds = list()
    # close the window
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
    main()