from lightning.types.base import Base
from lightning.types.decorators import viztype
from lightning.types.utils import vecs_to_points_three, add_property

@viztype
class Scatter3(Base):

    _name = 'scatter3'

    @staticmethod
    def clean(x, y, z, color=None, label=None, alpha=None, size=None):
        """
        Plot three-dimensional data as points.

        .. image:: particles.png

        Parameters
        ----------
        x, y, z : array-like, each (n,)
            Input data

        color : array-like, optional, singleton or (n,3)
            Single rgb value or array to set colors

        label : array-like, optional, singleton or (n,)
            Single integer or array to set colors via groups

        size : array-like, optional, singleton or (n,)
            Single size or array to set point sizes

        alpha : array-like, optional, singleton or (n,)
            Single alpha value or array to set fill and stroke opacity

        """

        points = vecs_to_points_three(x, y, z)
        outdict = {'points': points}

        outdict = add_property(outdict, color, 'color')
        outdict = add_property(outdict, label, 'label')
        outdict = add_property(outdict, size, 'size')
        outdict = add_property(outdict, alpha, 'alpha')

        return outdict


@viztype
class Volume(Base):

    _name = 'volume'

    @staticmethod
    def clean(imagedata):
        """
        Display a collection of arrays as browsable images with thumbnails.

        .. image:: volume.png

        Parameters
        ----------
        imagedata : array-like, or list of array-like
            Image or list of images as two dimensional (grayscale) or three dimensional (RGB) arrays.
        """

        if isinstance(imagedata, ndarray):
            imagedata = [imagedata]

        outdict = [array_to_im(im) for im in imagedata]

        return {'images': outdict}
