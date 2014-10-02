from lightning import Lightning, Session, Visualization
from random import randrange, uniform
from numpy import random


lightning = Lightning()


class TestLightningAPIClient:

    def test_create_session(self, host):

        lightning.host = host

        session = lightning.create_session()
        
        assert isinstance(session, Session)


    def test_create_named_session(self):
        
        session_name = 'test-session'
        session = lightning.create_session(session_name)
        
        assert isinstance(session, Session)
        assert hasattr(session, 'name')
        assert session.name == session_name


    def test_create_scatter(self):

        x = [randrange(100) for x in xrange(50)]
        y = [randrange(100) for y in xrange(50)]

        viz = lightning.scatter(x, y)

        assert isinstance(viz, Visualization)
        assert hasattr(viz, 'id')


    def test_create_line(self):

        x = [randrange(100) for x in xrange(50)]

        viz = lightning.plot('line', data=x)

        assert isinstance(viz, Visualization)
        assert hasattr(viz, 'id')



    def test_create_image(self):

        img1 = random.rand(256, 256)
        img2 = random.rand(256, 256)

        viz = lightning.image([img1, img2], type='gallery')

        assert isinstance(viz, Visualization)
        assert hasattr(viz, 'id')



    def test_create_roi(self):        


        points = [{ 'x': randrange(100), 'y': randrange(100), 'i': i} for i in xrange(50)]
        timeseries = [[uniform(-1, 1) for _ in xrange(1000)] for _ in xrange(50)]

        data = {
            'points': points,
            'timeseries': timeseries
        }

        viz = lightning.plot(data=data, type='roi')

        assert isinstance(viz, Visualization)
        assert hasattr(viz, 'id')



    def test_create_line(self):

        timeseries = [[randrange(100) for x in xrange(50)] for _ in xrange(6)]

        viz = lightning.plot('stacked-line', data=timeseries)

        assert isinstance(viz, Visualization)
        assert hasattr(viz, 'id')



    def test_ipython_support(self):

        lightning.ipython = True
        x = [randrange(100) for x in xrange(50)]

        viz = lightning.plot('line', data=x)

        assert isinstance(viz, Visualization)
        assert hasattr(viz, 'id')



    def test_create_us_map(self):

        states = ["NA", "AK", "AL", "AR", "AZ", "CA", "CO","CT","DC","DE","FL","GA","HI","IA","ID","IL","IN","KS","KY","LA","MA","MD","ME","MI","MN","MO","MS","MT","NC","ND","NE","NH","NJ","NM","NV","NY","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VA","VI","VT","WA","WI","WV","WY"]
        mapDict = dict((state, random.random()) for state in states)

        viz = lightning.plot('map', data=mapDict)

        assert isinstance(viz, Visualization)
        assert hasattr(viz, 'id')

    def test_create_world_map(self):

        countries = ["USA", "MEX", "CAN", "GER", "AUS", "BRA", "ARG", "PER", "SPA", "POR", "FRA", "ITA", "RUS", "CHN", "IND"]
        mapDict = dict((country, random.random()) for country in countries)

        viz = lightning.plot('map', data=mapDict)

        assert isinstance(viz, Visualization)
        assert hasattr(viz, 'id')


    def test_create_matrix(self):

        import numpy as np

        mat = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]])
        viz = lightning.matrix(mat)

        assert isinstance(viz, Visualization)
        assert hasattr(viz, 'id')


    def test_create_network(self):

        import numpy as np

        mat = np.array([[random.uniform(0, 15) if random.random() > 0.8 else 0 for _ in xrange(15)] for _ in xrange(15)])
        viz = lightning.network(mat)

        assert isinstance(viz, Visualization)
        assert hasattr(viz, 'id')

