import pytest
from numpy import random, ceil
from lightning import Lightning, Visualization


class TestLightningAPIClient(object):

    @pytest.fixture(scope="module")
    def lgn(self, host):
        lgn = Lightning(host)
        lgn.create_session("test-session")
        return lgn

    def test_create_generic(self, lgn):

        series = random.randn(5, 100)
        viz = lgn.plot(data={"series": series}, type='line')

        assert isinstance(viz, Visualization)
        assert hasattr(viz, 'id')


    def test_ipython_support(self, lgn):

        lgn.ipython = True
        x = random.randn(100)
        viz = lgn.line(x)

        assert isinstance(viz, Visualization)
        assert hasattr(viz, 'id')

