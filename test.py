from lightning import Lightning
import random

lgn = Lightning()
lgn.host = "http://localhost:3000"
session = lgn.use_session(9)


data = []

numPlots = 5

for i in xrange(numPlots):
    random_points = []
    while len(random_points) < 1000:
        tempX = random.random()
        random_points.append(tempX)

    data.append(random_points)

lgn.plot(data=data, type='stacked-line')

