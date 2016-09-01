import cv2
import sqlite3

def rotate(img, angle):
    rows, cols = img.shape
    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)
    cv2.warpAffine(img, M, (cols, rows),img, cv2.INTER_CUBIC)
    return img

conn = sqlite3.connect('/home/pkrush/2-camera-scripts/coins.db')

c = conn.cursor()

c.execute('''Select imageID, angle
from images
where bad_image = 0
and angle is not null
Order by 1''')
imageIDs = c.fetchall()
count = 0
while 1==1:
    for x in range(0, 5):
        for y in range(0, 6):
            imageID = imageIDs[count]
            count = count + 1
            angle = imageID[1]
            imageID = str(imageID[0])
            filename = '/home/pkrush/2-camera-scripts/crops/' + imageID + '.png'
            crop = cv2.imread(filename)
            if crop is None:
                continue
            crop = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
            crop = cv2.resize(crop, (145,145), interpolation=cv2.INTER_AREA)
            rotated = rotate(crop, 360 - angle)
            cv2.imshow(str(imageID), rotated)
            cv2.moveWindow(str(imageID),60 + (y*170),30 + (x*190))

    while 1==1:
        pressed_key = cv2.waitKey(0)

        if pressed_key & 0xFF == ord('a'):
            sql = 'update images set heads = 1, angle = ' + str(angle) + ' where imageID = ' + imageID
            print sql
            c.execute(sql)
            conn.commit()
        if pressed_key & 0xFF == ord('b'):
            c.execute('update images set heads = 1 where imageID = ' + imageID)
            conn.commit()
        if pressed_key & 0xFF == ord('t'):
            c.execute('update images set heads = 0 where imageID = ' + imageID)
            conn.commit()
        if pressed_key & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

# When everything done, release the capture
cv2.destroyAllWindows()