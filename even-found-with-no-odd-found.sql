--Even found with no odd found
select * 
from coinCenters
where imageID % 2 = 0
and x > 390
and x < 880
and ID not in
(
select
cc1.ID 
from coinCenters cc1
join coinCenters cc2
on  cc2.imageID = cc1.imageID + 1
and cc1.imageID % 2 = 0
and cc2.imageID % 2 = 1
and ((cc1.xMatch - cc2.x) * (cc1.xMatch - cc2.x)) + ((cc1.yMatch - cc2.y) * (cc1.yMatch - cc2.y)) < 300
)
and imageID not in (select imageID from badImages)
order by 1
