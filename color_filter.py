from split_image import split_image
import numpy as np
import cv2

frame = cv2.imread(r"C:\Users\kiv\Documents\GitHub\astrox\dataset\crop\zchop.meta.x000.y485.n009.jpg")
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
sensitivity = 90
lower_white = np.array([0,0,255-sensitivity])
upper_white = np.array([255,sensitivity,255])

mask = cv2.inRange(hsv, lower_white, upper_white)
res = cv2.bitwise_and(frame,frame, mask= mask)

cv2.imshow('frame',frame)
cv2.imshow('mask',mask)
cv2.imshow('res',res)

k = cv2.waitKey(5) & 0xFF
cv2.waitKey()
cv2.destroyAllWindows()
