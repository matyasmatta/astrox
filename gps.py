#Program na zjištění souřadnic mraku
import numpy as np
from PIL import Image

image = Image.open(r"C:\Users\trajc\Downloads\51844772672_92599fb67a_o.jpg")
rotated_image = rotated_image.rotate(225)
rotated_image.show()
rotated_image = rotated_image.save("otocena_fotka.jpg")
def cloudPosition(relativeLatitude, relativeLongtitude, centerCoordinates, cloudCoordinates): #centerCoordinates and cloudCoordinates in xxx.xx, xxx.xx format
    #input hodnot
    meridionalCircumference = 40008
    earthCircumference = 40075
    k = 0.12648                                                                           #konstanta pro převod pixelů na km
#    relativeLatitude = input("z. š. středu fotky ve formátu DD MM SS.SS N/S: ")       #input z. š. středu fotky
#    relativeLongtitude = input("z. d. středu fotky ve formátu DDD MM SS.SS E/W: ")      #input z. d. středu fotky

    #změna vzdálenosti na osách x,y
    centerCoordinatesX, centerCoordinatesY = centerCoordinates.split(", ")         #input souřadnic (v pixelech) středu fotky
    cloudCoordinatesX, cloudCoordinatesY = cloudCoordinates.split(", ")            #input souřadnic (v pixelech) mraku
    distanceX = (float(cloudCoordinatesX) - float(centerCoordinatesX)) * k                                  #pozice mraku - pozice středu (osa x)
    distanceY = (float(cloudCoordinatesY) - float(centerCoordinatesY)) * k                                  #pozice mraku - pozice středu (osa y)

    #převede souřadnice z. š. na desetinné číslo
    degrees, minutes, seconds, cardinalDirection = relativeLatitude.split(" ")
    decimalLatitude = (float(degrees) + float(minutes)/60 + float(seconds)/(60*60)) * (-1 if cardinalDirection == "S" else 1)

    #převede souřadnice z. d. na desetinné číslo
    degrees, minutes, seconds, cardinalDirection = relativeLongtitude.split(" ")
    decimalLongitude = (float(degrees) + float(minutes)/60 + float(seconds)/(60*60)) * (-1 if cardinalDirection == "W" else 1)

    #zjištění zeměpisné šířky
    cloudLatitude = float(decimalLatitude) + (distanceY*360)/meridionalCircumference
    print("z. š.:", cloudLatitude)

    #zjištění zeměpisné délky
    cloudLongitude = float(decimalLongitude) + (distanceX*360)/(earthCircumference*np.cos(cloudLatitude * (np.pi/180)))
    print("z. d.:", cloudLongitude)

cloudPosition("33 28 14.6 S", "125 24 03.9 E", "2366, 2251", "903, 1780")