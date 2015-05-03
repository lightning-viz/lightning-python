from lightning import Lightning, Session, Visualization
from random import randrange, uniform
from numpy import random, ceil, array, clip


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
        l = ceil(random.rand(100) * 5)
        s = random.rand(100) * 10 + 10
        a = clip(random.rand(100) + 0.1, 0, 1)

        viz = lightning.scatter(x, y, label=l, size=s, alpha=a)

        assert isinstance(viz, Visualization)
        assert hasattr(viz, 'id')


    def test_create_generic(self):

        series = random.randn(5,100)

        viz = lightning.plot(data={"series": series}, type='line')
        viz = lightning.plot({"series": series}, 'line')

        assert isinstance(viz, Visualization)
        assert hasattr(viz, 'id')


    def test_create_line(self):

        series = random.randn(5,100)
        s = random.rand(5) * 5 + 5

        viz = lightning.line(series, size=4)

        assert isinstance(viz, Visualization)
        assert hasattr(viz, 'id')


    def test_create_images(self):

        img1 = random.rand(128, 256, 3)

        viz = lightning.image(img1)

        assert isinstance(viz, Visualization)
        assert hasattr(viz, 'id')

    def test_create_gallery(self):

        img1 = random.rand(128, 256, 3)
        img2 = random.rand(128, 256, 3)

        viz = lightning.gallery([img1, img2])

        assert isinstance(viz, Visualization)
        assert hasattr(viz, 'id')


    def test_create_scatter_line(self):        

        x = random.randn(50)
        y = random.randn(50)
        series = random.randn(50,1000)
        l = ceil(random.rand(50) * 5)

        viz = lightning.scatterline(x, y, series, label=l)

        assert isinstance(viz, Visualization)
        assert hasattr(viz, 'id')


    # def test_create_line_stacked(self):

    #     series = random.randn(6, 100)

    #     viz = lightning.linestacked(series)

    #     assert isinstance(viz, Visualization)
    #     assert hasattr(viz, 'id')


    def test_ipython_support(self):

        lightning.ipython = True
        x = random.randn(100)

        viz = lightning.line(x)

        assert isinstance(viz, Visualization)
        assert hasattr(viz, 'id')


    def test_create_us_map(self):

        states = ["NA", "AK", "AL", "AR", "AZ", "CA", "CO","CT","DC","DE","FL","GA","HI","IA","ID","IL","IN","KS","KY","LA","MA","MD","ME","MI","MN","MO","MS","MT","NC","ND","NE","NH","NJ","NM","NV","NY","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VA","VI","VT","WA","WI","WV","WY"]
        values = random.randn(len(states))

        viz = lightning.map(states,values, colormap="Blues")

        assert isinstance(viz, Visualization)
        assert hasattr(viz, 'id')

    def test_create_world_map(self):

        countries = ["USA", "MEX", "CAN", "GER", "AUS", "BRA", "ARG", "PER", "SPA", "POR", "FRA", "ITA", "RUS", "CHN", "IND"]
        values = random.randn(len(countries))

        viz = lightning.map(countries, values, colormap="Purples")

        assert isinstance(viz, Visualization)
        assert hasattr(viz, 'id')

    def test_create_adjacency(self):

        mat = random.randn(10,10)
        mat[mat<0.8] = 0
        l = ceil(random.rand(10)*4)

        viz = lightning.adjacency(mat, label=l)

        assert isinstance(viz, Visualization)
        assert hasattr(viz, 'id')

    def test_create_matrix(self):

        mat = random.randn(10,10)
        viz = lightning.matrix(mat)

        assert isinstance(viz, Visualization)
        assert hasattr(viz, 'id')

    def test_create_force(self):

        mat = array([[random.uniform(0, 25) if random.random() > 0.95 else 0 for _ in range(25)] for _ in range(25)])
        viz = lightning.force(mat)

        assert isinstance(viz, Visualization)
        assert hasattr(viz, 'id')

    def test_create_graph(self):

        mat = array([[random.uniform(0, 25) if random.random() > 0.9 else 0 for _ in range(25)] for _ in range(25)])
        x = random.randn(25)
        y = random.randn(25)
        
        viz = lightning.graph(x, y, mat)

        assert isinstance(viz, Visualization)
        assert hasattr(viz, 'id')

