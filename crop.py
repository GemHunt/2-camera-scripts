import numpy as np
import sqlite3
import sys
import cv2
import cv2.cv as cv

conn = sqlite3.connect('coins.db')
# Make sure that caffe is on the python path:
# sys.path.append('~/caffe/python') using the ~ does not work, for some reason???
sys.path.append('/home/pkrush/caffe/python')


def crop(num, x, y, radius):
    # type: (object, object, object, object) -> object
    image_name = 'raw/' + str(num) + '.png'
    crop_name = 'crops/' + str(num) + '.png'

    img = cv2.imread(image_name)
    # The coin sometimes is off the top of the image. In this case this math will cause the coin to crop off center.
    x = x + 2
    top_y = y - radius
    if top_y < 0:
        top_y = 0
    bottom_y = top_y + radius + radius
    dst = img[top_y:bottom_y, x - radius:x + radius]
    cv2.imwrite(crop_name, dst)
    #cv2.imshow('crop', dst)
    #cv2.waitKey(0)
    return


c = conn.cursor()
c.execute("""Select
cc1.imageID,
cc1.x,
cc1.y,
cc1.xMatch,
cc1.yMatch
from coinCenters cc1
join coinCenters cc2
on  cc2.imageID = cc1.imageID + 1
and cc1.imageID % 2 = 0
and cc2.imageID % 2 = 1
and ((cc1.xMatch - cc2.x) * (cc1.xMatch - cc2.x)) + ((cc1.yMatch - cc2.y) * (cc1.yMatch - cc2.y)) < 200
and cc1.x > 390
and cc1.x <  840
--and cc1.imageID > 30999
--and cc1.imageID < 32000
and cc1.imageID not in (select imageID from badImages)
order by 1""")
all_rows = c.fetchall()
for row in all_rows:
    print('{0} : {1}, {2}'.format(row[0], row[1], row[2]))
    crop(row[0], row[1], row[2], 351)
    crop(row[0] + 1, row[3], row[4], 327)

cv2.destroyAllWindows()
