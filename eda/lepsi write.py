def write_valid(tuple1, tuple2):
    list_to_write.append('True')
    x1,y1 = tuple1
    x2,y2= tuple2
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
    with open('eda/output.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        # Zápis dat ze seznamu
        writer.writerow(list_to_write)
    global getting_cisilko
    getting_cisilko = True
    list_to_write = list()

    print('NAPSAL JSEM USPESNY MRAK')
    fill()
    cv2.putText(img, "Set cloud", (300*size_of_everything, 520*size_of_everything), cv2.FONT_HERSHEY_SIMPLEX ,0.5*size_of_everything, (255, 0, 0), 2)
    cv2.imshow('image', img)

def write_invalid():
    with open('eda/output.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        # Zápis dat ze seznamu
        writer.writerow(list_to_write)
    print('NAPSAL JSEM NEUSPESNY MRAK')

def write_to_csv(optional_arg=tuple1, optional_arg=tuple2)
    list_to_write = []
    list_to_write.append(image_name)
    list_to_write.append(' ')
    list_to_write.append(str(cisilko))
    list_to_write.append(str(validation))
    if validation == True:
        x1,y1 = tuple1
        x2,y2= tuple2
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
    with open('eda/output.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        # Zápis dat ze seznamu
        writer.writerow(list_to_write)
    fill()
    cv2.putText(img, "Set cloud", (300*size_of_everything, 520*size_of_everything), cv2.FONT_HERSHEY_SIMPLEX ,0.5*size_of_everything, (255, 0, 0), 2)
    cv2.imshow('image', img)
    global getting_cisilko
    getting_cisilko = True