#Program na zjištění souřadnic mraku
import numpy as np
from PIL import Image

image = Image.open(r"C:\Users\trajc\Downloads\51844772672_92599fb67a_o.jpg")
rotated_image = image.rotate(225)
rotated_image.show()
rotated_image = rotated_image.save("otocena_fotka.jpg")

def cloudPosition(relativeLatitude, relativeLongtitude, centerCoordinates, cloudCoordinates): #centerCoordinates and cloudCoordinates in xxx.xx, xxx.xx format
    #input hodnot
    meridionalCircumference = 40008
    earthCircumference = 40075
    k = 0.12648                                                                           #constant for converting pixels to km

    #finds pixel distance delta
    centerCoordinatesX, centerCoordinatesY = centerCoordinates.split(", ")         
    cloudCoordinatesX, cloudCoordinatesY = cloudCoordinates.split(", ")           
    distanceX = (float(cloudCoordinatesX) - float(centerCoordinatesX)) * k                                  #location of cloud - center location (x axis)
    distanceY = (float(cloudCoordinatesY) - float(centerCoordinatesY)) * k                                  #location of cloud - center location (y axis)

    #converts relativeLatitude in DMS format to decimal degrees
    degrees, minutes, seconds, cardinalDirection = relativeLatitude.split(" ")
    decimalLatitude = (float(degrees) + float(minutes)/60 + float(seconds)/(60*60)) * (-1 if cardinalDirection == "S" else 1)

    #converts relativeLongtitude in DMS format to decimal degrees
    degrees, minutes, seconds, cardinalDirection = relativeLongtitude.split(" ")
    decimalLongitude = (float(degrees) + float(minutes)/60 + float(seconds)/(60*60)) * (-1 if cardinalDirection == "W" else 1)

    #finds latitude of the cloud
    cloudLatitude = float(decimalLatitude) + (distanceY*360)/meridionalCircumference
    print("z. š.:", cloudLatitude)

    #find longtitude of the cloud
    cloudLongitude = float(decimalLongitude) + (distanceX*360)/(earthCircumference*np.cos(cloudLatitude * (np.pi/180)))
    print("z. d.:", cloudLongitude)
    return(cloudLatitude, cloudLongitude)

cloudPosition("33 28 14.6 S", "125 24 03.9 E", "2366, 2251", "903, 1780")