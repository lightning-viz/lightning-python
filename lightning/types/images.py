from numpy import ndarray, asarray

from lightning.types.base import Base
from lightning.types.decorators import viztype
from lightning.types.utils import array_to_im


@viztype
class Image(Base):
    _name = 'image'
    
    @staticmethod
    def clean(imagedata):
        """
        Display an array as an image.

        Parameters
        ----------
        imagedata : array-like
            Image as a two dimensional (grayscale) or three dimensional (RGB) array.
        """
        if asarray(imagedata).ndim not in set((2, 3)):
            raise Exception("Input must be two or three dimensional")

        outdict = [array_to_im(imagedata)]

        return {'images': outdict}

    def coords(self):
        user_data = self.get_user_data()['settings']
        if 'coords' in user_data.keys():
            return user_data['coords']
        else:
            return []


@viztype
class Gallery(Base):

    _name = 'gallery'

    @staticmethod
    def clean(imagedata):
        """
        Display a collection of arrays as browsable images with thumbnails.

        Parameters
        ----------
        imagedata : array-like, or list of array-like
            Image or list of images as two dimensional (grayscale) or three dimensional (RGB) arrays.
        """

        if isinstance(imagedata, ndarray):
            imagedata = [imagedata]

        outdict = [array_to_im(im) for im in imagedata]

        return {'images': outdict}
