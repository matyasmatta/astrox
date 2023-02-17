#import stiny_maty
import sever_eda
import statistics

#data = stiny_maty.sun_data.altitude("34.28614 S", "147.9849 E", 2022, 1, 15, 5, 16, 50)
#print(data)

#data = stiny_maty.calculate_shadow('.\\zchop.meta.x000.y000.n011.jpg', 294,199,310)
#print(data)
counter=234
for i in range(130):
    i_1=str(counter)
    if int(i_1) < 10:
        before_1 = "eda\direction12\photo_18"
    else:
        if int(i_1) <100:
            before_1 = "eda\direction12\photo_18"
        if int(i_1) >= 100:
            before_1 = "eda\direction12\photo_18"
    image_1=str(before_1 + i_1 +".jpg")
    i_2=str(counter+1)
    #print(image_1)
    if int(i_2) < 10:
        before_2 = "eda\direction12\photo_18"
    else:
        if int(i_2) <100:
            before_2 = "eda\direction12\photo_18"
        if int(i_1) >= 100:
            before_2 = "eda\direction12\photo_18"

    image_2=str(before_2 + i_2 +".jpg")
    #print(image_2)

    data = sever_eda.find_north(image_1, image_2)
    #print(data)
    counter+=1

    
