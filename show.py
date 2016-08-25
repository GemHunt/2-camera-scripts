# HoughCircles works pretty good at first glance...
import cv2
import numpy as np
import sqlite3
conn = sqlite3.connect('C:/Users/pkrush/Documents/GemHunt/2-camera-scripts/coins.db')

num = 30833

image_name = 'F:/2Camera/raw/' + str(num) + '.png'
img = cv2.imread(image_name, 0)
img = cv2.medianBlur(img, 5)
cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)


if (num%2) == 0:
    # works on even:
    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 300, param1=50, param2=30, minRadius=350, maxRadius=357)
else:
    # works on odd:
    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 300, param1=50, param2=30, minRadius=320, maxRadius=330)
    #This seems to work better:
    #circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 300, param1=80, param2=20, minRadius=327, maxRadius=335)
    circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,300,param1=80,param2=20,minRadius=327,maxRadius=330)

circles = np.uint16(np.around(circles))

for i in circles[0, :]:
    #c = conn.cursor()
    #c.execute('INSERT INTO CoinCenters VALUES (' + str(num) + ',1,' + str(i[0]) + ',' + str(i[1])  + ',' + str(i[2])  + ')')
    #conn.commit()
    # draw the outer circle
    cv2.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0), 1)
    # draw the center of the circle
    cv2.circle(cimg, (i[0], i[1]), 2, (0, 0, 255), 1)

print circles, num
cv2.imshow('detected circles', cimg)
cv2.waitKey(0)
cv2.destroyAllWindows()
