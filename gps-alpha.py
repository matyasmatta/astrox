import math

#input hodnot
meridionalCircumference = 40008
earthCircumference = 40075
k = 0.142                                                                           #konstanta pro převod pixelů na km
relativeLatitude = input("z. š. středu fothky ve formátu DD MM SS.SS N/S: ")       #input z. š. středu fotky
relativelongtitude = input("z. d. středu fotky ve formátu DDD MM SS.SS E/W: ")      #input z. d. středu fotky

#změna vzdálenosti na osách x,y
centerCoordinatesX, centerCoordinatesY = input("center coordinates (xxxx, yyyy): ").split(", ")     #input souřadnic (v pixelech) středu fotky
cloudCoordinatesX, cloudCoordinatesY = input("cloud coordinates (xxxx, yyyy): ").split(", ")        #input souřadnic (v pixelech) mraku
distanceX = (float(cloudCoordinatesX) - float(centerCoordinatesX)) * k                              #pozice mraku - pozice středu (osa x)
distanceY = (float(cloudCoordinatesY) - float(centerCoordinatesY)) * k                              #pozice mraku - pozice středu (osa y)

#převede souřadnice z. š. na desetinné číslo
degrees, minutes, seconds, cardinalDirection = relativeLatitude.split(" ")
decimalLatitude = (float(degrees) + float(minutes)/60 + float(seconds)/(60*60)) * (-1 if cardinalDirection in ["S"] else 1)

#převede souřadnice z. d. na desetinné číslo
degrees, minutes, seconds, cardinalDirection = relativelongtitude.split(" ")
decimalLongitude = (float(degrees) + float(minutes)/60 + float(seconds)/(60*60)) * (-1 if cardinalDirection in ["W"] else 1)

#zjištění zeměpisné šířky
cloudLatitude = float(decimalLatitude) + (distanceY*360)/meridionalCircumference
print("z. š.:", cloudLatitude)

#zjištění zeměpisné délky
cloudLongitude = float(decimalLongitude) + (distanceX*360)/(earthCircumference*math.cos(cloudLatitude * (math.pi/180)))
print("z. d.:", cloudLongitude)

