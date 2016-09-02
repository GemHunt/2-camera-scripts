import cv2
import sqlite3
import sys
import time
import numpy as np

def open_windows():
    if len(imageIDs) == open_windows.count:
        sys.exit

    for x in range(0, 4):
        for y in range(0, 4):
            if len(imageIDs) == open_windows.count:
                continue

            imageID = imageIDs[open_windows.count]
            open_windows.count = open_windows.count + 1
            #angle = int(imageID[1])
            imageID = str(imageID[0])
            filename = '/home/pkrush/2-camera-scripts/crops/' + imageID + '.png'
            crop = cv2.imread(filename)
            if crop is None:
                continue
            crop = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
            crop = cv2.resize(crop, (thumb_nail_size,thumb_nail_size), interpolation=cv2.INTER_AREA)

            #crop = rotate(crop, 360 - angle)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(crop, imageID, (20, 20), font, 0.4, (0, 0, 0), 2)
            window_name = 'window ' + str((x*4 + y)+1)
            cv2.moveWindow(window_name, 80 + (y * 170), 80 + (x * 190))
            cv2.imshow(window_name, crop)
            cv2.setMouseCallback(window_name, call_back, param=[imageID,window_name ])
            cv2.waitKey(5)
    cv2.waitKey(5)

def rotate(img, angle):
    rows, cols = img.shape
    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)
    cv2.warpAffine(img, M, (cols, rows),img, cv2.INTER_CUBIC)
    return img

# mouse callback function
def call_back(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.imshow(param[1], blank_image)
        if flags == cv2.EVENT_FLAG_SHIFTKEY:
            c.execute('update images set bad_image = 1 where imageID = ' + param[0])
            conn.commit()
        else:
            c.execute('update images set heads = 0 where imageID = ' + param[0])
            conn.commit()

    if event == cv2.EVENT_RBUTTONDOWN:
        print flags
        open_windows()

conn = sqlite3.connect('/home/pkrush/2-camera-scripts/coins.db')
c = conn.cursor()
sql = '''
--these are double headed or double tails:
Select i2.imageID
from images i1
join images i2
on i1.imageID % 2 = 0
and i2.imageID % 2 = 1
and i1.imageID = i2.ImageID - 1
and not (i1.bad_image = 1 or i2.bad_image = 1)
and i1.heads = i2.heads
Order by 1
'''

sql = '''
--check tails angle
Select i2.imageID, i2.angle
from images i1
join images i2
on i1.imageID % 2 = 0
and i2.imageID % 2 = 1
and i1.imageID = i2.ImageID - 1
and not (i1.bad_image = 1 or i2.bad_image = 1)
and i2.heads = 1
and i2.angle is not null
Order by 1'''


sql = '''
--check tails
Select imageID
from images
where heads = 1
and bad_image = 0
Order by 1
'''

c.execute(sql)
imageIDs = c.fetchall()

thumb_nail_size = 145
blank_image = np.zeros((thumb_nail_size,thumb_nail_size,3), np.uint8)
for num in range(1,16):
    window_name = 'window ' + str(num)
    cv2.imshow(window_name,blank_image)

open_windows.count = 0
open_windows()


while 1==1:
    pressed_key = cv2.waitKey(0)
    if pressed_key & 0xFF == ord('q'):
        break

# When everything done, release the capture
cv2.destroyAllWindows()