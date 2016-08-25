--Even odd matches ordered by distance
select
((cc1.xMatch - cc2.x) * (cc1.xMatch - cc2.x)) + ((cc1.yMatch - cc2.y) * (cc1.yMatch - cc2.y)),
 cc1.imageID,cc2.imageID, cc1.x, cc1.y, cc2.x, cc2.y,cc1.xMatch,cc1.yMatch
from coinCenters cc1
join coinCenters cc2
on  cc2.imageID = cc1.imageID + 1
and cc1.imageID % 2 = 0
and cc2.imageID % 2 = 1
and ((cc1.xMatch - cc2.x) * (cc1.xMatch - cc2.x)) + ((cc1.yMatch - cc2.y) * (cc1.yMatch - cc2.y)) < 5000
order by 1
