# 2-camera-scripts
Python scripts to match up images of pennies from 2 cameras

DataSet is on www.GemHunt.com

Two cameras are pointed at each other. Each one images one side of the coin. 

**The coin centers need to be correlated to each other:**
* The X is mirrored
* They are twisted to each other at some point at some angle. 
* The cameras are at different zooms
* The centers are offset
* They might not be parallel to each other. 
* The cameras are not calibrated

Instead of trying to do the math for all that, I just use linear regression to match up the centers. It works good!

