import pytest
from numpy import random
from lightning import Lightning, Visualization, VisualizationLocal


class TestLightningAPIClient(object):

    @pytest.fixture(scope="module")
    def lgn(self, host):
        lgn = Lightning(host)
        lgn.create_session("test-session")
        return lgn

    def test_create(self, lgn):

        series = random.randn(5, 100)
        viz = lgn.plot(data={"series": series}, type='line')

        assert isinstance(viz, Visualization)
        assert hasattr(viz, 'id')

    def test_local(self, lgn):

        lgn.enable_local()
        x = random.randn(100)
        viz = lgn.line(x)

        assert isinstance(viz, VisualizationLocal)

