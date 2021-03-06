# This finds penny centers in batch
# The db details are broken...
# HoughCircles works pretty good at first glance...
# I have yet to try changing the blur to improved centering
# Centering is better on the bottom camera with a lower param2 and a higher minRadius...

import numpy as np
import sqlite3
import sys
import cv2
import cv2.cv as cv

conn = sqlite3.connect('coins.db')

# Make sure that caffe is on the python path:
# sys.path.append('~/caffe/python') using the ~ does not work, for some reason???
sys.path.append('/home/pkrush/caffe/python')

for num in range(30000, 30050):
    image_name = '' + str(num) + '.png'
    img = cv2.imread(image_name, 0)
    img = cv2.medianBlur(img, 5)
    cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    if (num%2) == 0:
        # works on even:
        circles = cv2.HoughCircles(img, cv.CV_HOUGH_GRADIENT, 1, 300, param1=50, param2=30, minRadius=350, maxRadius=357)
    else:
        # works on odd:
        #circles = cv2.HoughCircles(img, cv.CV_HOUGH_GRADIENT, 1, 300, param1=50, param2=30, minRadius=320, maxRadius=330)
        #This seems to work better:
        circles = cv2.HoughCircles(img,cv.CV_HOUGH_GRADIENT,1,300,param1=80,param2=20,minRadius=328,maxRadius=330)

    circles = np.uint16(np.around(circles))

    for i in circles[0, :]:
        c = conn.cursor()
        c.execute('INSERT INTO CoinCenters VALUES (' + str(num) + ',1,' + str(i[0]) + ',' + str(i[1])  + ',' + str(i[2])  + ')')
        conn.commit()
        # draw the outer circle
        #cv2.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0), 1)
        # draw the center of the circle
        #cv2.circle(cimg, (i[0], i[1]), 2, (0, 0, 255), 1)
        #print circles, num
        #cv2.imshow('detected circles', cimg)
        #cv2.waitKey(0)


cv2.destroyAllWindows()
