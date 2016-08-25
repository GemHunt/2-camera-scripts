--Manual Center Vs HoughCircles
select coins.x - coinCenters.x, coins.y - coinCenters.y, *
from coins 
join coinCenters
on coins.imageID = coinCenters.imageID
and coinCenters.x > 390
and coinCenters.x < 880
order by 4
