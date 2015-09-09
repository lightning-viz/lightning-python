import pytest
from numpy import random, ceil, array, clip
from lightning import Lightning, Visualization
from lightning.types.utils import mat_to_links


class TestLightningPlots(object):

    @pytest.fixture(scope="module")
    def lgn(self, host):
        lgn = Lightning(host)
        lgn.create_session("test-plots")
        return lgn

    def test_create_scatter(self, lgn):

        x = random.randn(100)
        y = random.randn(100)
        g = ceil(random.rand(100) * 5)
        s = random.rand(100) * 10 + 10
        a = clip(random.rand(100) + 0.1, 0, 1)

        viz = lgn.scatter(x, y, group=g, size=s, alpha=a)

        assert isinstance(viz, Visualization)
        assert hasattr(viz, 'id')

    def test_create_scatter_value(self, lgn):

        x = random.randn(100)
        y = random.randn(100)
        v = ceil(random.rand(100) * 5)
        s = random.rand(100) * 10 + 10
        a = clip(random.rand(100) + 0.1, 0, 1)

        viz = lgn.scatter(x, y, values=v, colormap="Purples", size=s, alpha=a)

        assert isinstance(viz, Visualization)
        assert hasattr(viz, 'id')

    def test_create_line(self, lgn):

        series = random.randn(5,100)
        s = random.rand(5) * 5 + 5
        viz = lgn.line(series, thickness=s)

        assert isinstance(viz, Visualization)
        assert hasattr(viz, 'id')

    def test_create_us_map(self, lgn):

        states = ["NA", "AK", "AL", "AR", "AZ", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
                  "HI", "IA", "ID", "IL", "IN", "KS", "KY", "LA", "MA", "MD", "ME", "MI",
                  "MN", "MO", "MS", "MT", "NC", "ND", "NE", "NH", "NJ", "NM", "NV", "NY",
                  "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VA", "VI",
                  "VT", "WA", "WI", "WV", "WY"]
        values = random.randn(len(states))
        viz = lgn.map(states, values, colormap="Blues")

        assert isinstance(viz, Visualization)
        assert hasattr(viz, 'id')

    def test_create_world_map(self, lgn):

        countries = ["USA", "MEX", "CAN", "GER", "AUS", "BRA", "ARG", "PER", "SPA",
                     "POR", "FRA", "ITA", "RUS", "CHN", "IND"]
        values = random.randn(len(countries))
        viz = lgn.map(countries, values, colormap="Purples")

        assert isinstance(viz, Visualization)
        assert hasattr(viz, 'id')

    def test_create_adjacency(self, lgn):

        mat = random.randn(10, 10)
        mat[mat < 0.8] = 0
        g = ceil(random.rand(10)*4)
        viz = lgn.adjacency(mat, group=g)

        assert isinstance(viz, Visualization)
        assert hasattr(viz, 'id')

    def test_create_matrix(self, lgn):

        mat = random.randn(10, 10)
        viz = lgn.matrix(mat)

        assert isinstance(viz, Visualization)
        assert hasattr(viz, 'id')

    def test_create_force(self, lgn):

        mat = array([[random.uniform(0, 25) if random.random() > 0.95 else 0 for _ in range(25)] for _ in range(25)])
        viz = lgn.force(mat)

        assert isinstance(viz, Visualization)
        assert hasattr(viz, 'id')

    def test_create_force_links(self, lgn):

        mat = array([[random.uniform(0, 25) if random.random() > 0.95 else 0 for _ in range(25)] for _ in range(25)])
        links = mat_to_links(mat)
        viz = lgn.force(links)

        assert isinstance(viz, Visualization)
        assert hasattr(viz, 'id')

    def test_create_graph(self, lgn):

        mat = array([[random.uniform(0, 25) if random.random() > 0.9 else 0 for _ in range(25)] for _ in range(25)])
        x = random.randn(25)
        y = random.randn(25)
        viz = lgn.graph(x, y, mat)

        assert isinstance(viz, Visualization)
        assert hasattr(viz, 'id')

    def test_create_graph_bundled(self, lgn):

        mat = array([[random.uniform(0, 25) if random.random() > 0.9 else 0 for _ in range(25)] for _ in range(25)])
        x = random.randn(25)
        y = random.randn(25)
        viz = lgn.graph(x, y, mat)

        assert isinstance(viz, Visualization)
        assert hasattr(viz, 'id')
