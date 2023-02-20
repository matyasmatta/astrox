#Program na zjištění souřadnic mraku
import numpy as np
def cloudPosition(relativeLatitude, relativeLongtitude, centerCoordinates, cloudCoordinates): #centerCoordinates and cloudCoordinates in xxx.xx, xxx.xx format
    #input hodnot
    meridionalCircumference = 40008
    earthCircumference = 40075
    k = 0.142                                                                           #konstanta pro převod pixelů na km
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

cloudPosition("55 55 55 N", "56 56 56 E", "55.5, 565", "35, 25")