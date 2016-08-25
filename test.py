import numpy as np
from sklearn import datasets, linear_model
from numpy import genfromtxt
import sqlite3
conn = sqlite3.connect('C:/Users/pkrush/Documents/GemHunt/2-camera-scripts/coins.db')

y = genfromtxt('y.csv', delimiter=',')
x = genfromtxt('x.csv', delimiter=',')

ols = linear_model.LinearRegression()
#y is the even and you x is odd.
ols.fit(y, x)

#print y #even
#print x #odd
#print ols.predict(x) #even prediction from odd

#np.savetxt("fit.csv", ols.predict(x) , delimiter=",")

c = conn.cursor()
c.execute('''select imageID,x, y from coinCenters where imageID % 2 = 0''')
all_rows = c.fetchall()
for row in all_rows:
    print('{0} : {1}, {2}'.format(row[0], row[1], row[2]))
    x = [row[1], row[2]]
    y = ols.predict(x) #even prediction from odd
    c.execute('Update CoinCenters Set xMatch = ' + str(y[0,0]) +  ', yMatch = ' + str(y[0,1]) +  ' Where imageID = ' + str(row[0]) + ' And x =' + str(x[0]))
    conn.commit()


