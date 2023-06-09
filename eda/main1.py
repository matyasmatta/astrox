# importing the module
import cv2
import math   


# function to display the coordinates of
# of the points clicked on the image 

# function that does nothing
def do_nothing(*args):
    pass

def distance(tuple1, tuple2):
    x1,y1=tuple1
    x2,y2=tuple2
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    print('vzdálenost v px je:', distance)
    list_of_clouds.append((cisilko, 'YES', distance))
    return 
def click_event(event, x, y, flags, params):
    global first_point, second_point

    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
        # displaying the coordinates
        # on the Shell

        # displaying the coordinates
        # on the image window
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, str(x) + ',' +
                    str(y), (x, y), font,
                    0.5, (255, 0, 0), 2)
        cv2.imshow('image', img)
        
        if first_point == (0, 0):
            first_point = (x, y)
            print('čekám na stín')
        else:
            second_point = (x, y)
            cv2.line(img, first_point, second_point, (256, 0, 0), 3)
            print('čára je:', first_point, second_point)
            cv2.imshow('image', img)
            distance(first_point, second_point)
            first_point = (0,0)
            second_point = (0,0)
            print('cekam na prvni cislo')
            cv2.setMouseCallback('image', do_nothing)
            

# driver function
list_of_clouds = list()
first_point = (0,0)
second_point = (0,0)
if __name__=="__main__":
    for p in range (367):

        for i in range(1,5):
            # reading the image
            image_path = 'chops/img_'+str(p)+'_'+str(i)+'.jpg'
            img = cv2.imread(image_path, 1)
        
            # displaying the image
            cv2.imshow('image', img)
        
            # setting mouse handler for the image
            # and calling the click_event() function
            prev_key = None

            while True:
                
                # wait for a key to be pressed to exit
                key = cv2.waitKey(0)

                if key >= 48 and key <= 57:  # Kontrola, zda je stisknuto číslo 0 až 9
                    if prev_key is not None:
                        cisilko = int(chr(prev_key) + chr(key))
                        print(cisilko)
                        prev_key = None
                        print('starting validation')
                        key = cv2.waitKey(0)
                        if key == 49:
                            print(cisilko, 'is NOT valid')
                            list_of_clouds.append((cisilko, 'NO', '----'))
                        elif key == 50:
                            print(cisilko, 'is valid, beginnig distance')
                            cv2.setMouseCallback('image', click_event)
                        else:
                            print('jiná klávesa')
                    else:
                        prev_key = key
                        print
                        print('čekám na druhé číslo')
                elif key == 27: #ESC
                    break
            print('\n----\n\nFINÁLNÍ LIST\n', list_of_clouds)
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