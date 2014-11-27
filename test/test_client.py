from lightning import Lightning, Session, Visualization
from random import randrange, uniform
from numpy import random, ceil, array


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

        x = random.randn(100)
        y = random.randn(100)
        c = ceil(random.rand(100)*10)

        viz = lightning.scatter(x, y, clrs=c)

        print(viz)

        assert isinstance(viz, Visualization)
        assert hasattr(viz, 'id')


    def test_create_line(self):

        x = random.randn(100)

        viz = lightning.line(x)

        assert isinstance(viz, Visualization)
        assert hasattr(viz, 'id')


    def test_create_image(self):

        img1 = random.rand(256, 256, 3)
        img2 = random.rand(256, 256, 3)

        viz = lightning.gallery([img1, img2])

        assert isinstance(viz, Visualization)
        assert hasattr(viz, 'id')


    def test_create_roi(self):        

        x = random.randn(50)
        y = random.randn(50)
        timeseries = random.randn(50,1000)

        viz = lightning.roi(x, y, timeseries)

        assert isinstance(viz, Visualization)
        assert hasattr(viz, 'id')


    def test_create_stacked_line(self):

        timeseries = random.randn(6, 100)

        viz = lightning.stackedline(timeseries)

        assert isinstance(viz, Visualization)
        assert hasattr(viz, 'id')


    def test_ipython_support(self):

        lightning.ipython = True
        x = random.randn(100)

        viz = lightning.line(x)

        assert isinstance(viz, Visualization)
        assert hasattr(viz, 'id')


    def test_create_us_map(self):

        states = ["NA", "AK", "AL", "AR", "AZ", "CA", "CO","CT","DC","DE","FL","GA","HI","IA","ID","IL","IN","KS","KY","LA","MA","MD","ME","MI","MN","MO","MS","MT","NC","ND","NE","NH","NJ","NM","NV","NY","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VA","VI","VT","WA","WI","WV","WY"]
        mapDict = dict((state, random.random()) for state in states)

        viz = lightning.plot(type='map', data=mapDict)

        assert isinstance(viz, Visualization)
        assert hasattr(viz, 'id')

    def test_create_world_map(self):

        countries = ["USA", "MEX", "CAN", "GER", "AUS", "BRA", "ARG", "PER", "SPA", "POR", "FRA", "ITA", "RUS", "CHN", "IND"]
        mapDict = dict((country, random.random()) for country in countries)

        viz = lightning.plot(type='map', data=mapDict)

        assert isinstance(viz, Visualization)
        assert hasattr(viz, 'id')


    def test_create_matrix(self):

        mat = random.randn(10,10)
        viz = lightning.matrix(mat)

        assert isinstance(viz, Visualization)
        assert hasattr(viz, 'id')


    def test_create_network(self):

        mat = array([[random.uniform(0, 15) if random.random() > 0.8 else 0 for _ in xrange(15)] for _ in xrange(15)])
        viz = lightning.forcenetwork(mat)
    def test_create_graph(self):

        mat = array([[random.uniform(0, 15) if random.random() > 0.8 else 0 for _ in xrange(15)] for _ in xrange(15)])
        x = random.randn(15)
        y = random.randn(15)
        
        viz = lightning.graph(mat, x, y)

        assert isinstance(viz, Visualization)
        assert hasattr(viz, 'id')

