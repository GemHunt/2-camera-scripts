Select *
from images i1
join images i2
on i1.imageID % 2 = 0
and i2.imageID % 2 = 1
and i1.imageID = i2.ImageID - 1
and not (i1.bad_image = 1 or i2.bad_image = 1)
and i1.heads = i2.heads
Order by 1