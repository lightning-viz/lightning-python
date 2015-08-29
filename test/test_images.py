import pytest
from numpy import random, ceil
from lightning import Lightning, Visualization


class TestLightningImages(object):

    @pytest.fixture(scope="module")
    def lgn(self, host):
        lgn = Lightning(host)
        lgn.create_session("test-images")
        return lgn

    def test_create_images(self, lgn):

        img1 = random.rand(10, 10, 3)
        viz = lgn.image(img1)

        assert isinstance(viz, Visualization)
        assert hasattr(viz, 'id')

    def test_create_gallery(self, lgn):

        img1 = random.rand(10, 10, 3)
        img2 = random.rand(10, 10, 3)
        viz = lgn.gallery([img1, img2])

        assert isinstance(viz, Visualization)
        assert hasattr(viz, 'id')
