from numpy import ndarray, asarray

from lightning.types.base import Base
from lightning.types.decorators import viztype
from lightning.types.utils import add_property, array_to_im, polygon_to_points, polygon_to_mask


@viztype
class Image(Base):
    _name = 'image'

    @staticmethod
    def clean(imagedata):
        """
        Display an array as an image.

        .. image:: image.png

        Parameters
        ----------
        imagedata : array-like
            Image as a two dimensional (grayscale) or three dimensional (RGB) array.
        """
        if asarray(imagedata).ndim not in set((2, 3)):
            raise Exception("Input must be two or three dimensional")

        outdict = [array_to_im(imagedata)]

        return {'images': outdict}

@viztype
class ImagePoly(Base):
    _name = 'image-poly'
    _func = 'imagepoly'
    
    @staticmethod
    def clean(imagedata, coordinates=None, xy=None):
        """
        Display an array as an image with polygonal regions and region drawing.

        .. image:: image.png

        Parameters
        ----------
        imagedata : array-like
            Image as a two dimensional (grayscale) or three dimensional (RGB) array.

        coordinates : array-like
            List of coordinates or list of list of coordinates. Assumes array indexing
            (i.e. row/column), in the form [[r,c],[r,c]] for one region or
            [[[r0,c0],[r0,c0]], [[r1,c1],[r1,c1]]] for multiple regions

        xy : boolean, optional, default = None
            Only if True treat coordinates as x/y positions instead of row/column indices
        """
        if asarray(imagedata).ndim not in set((2, 3)):
            raise Exception("Input must be two or three dimensional")

        imgs = [array_to_im(imagedata)]
        outdict = {'images': imgs}
        outdict = add_property(outdict, coordinates, 'coordinates', xy=xy)

        return outdict

    @property
    def _coords(self):
        """
        Coordinates of regions retrieved from visualization user data.
        """
        user_data = self.get_user_data()['settings']
        if 'coords' in user_data.keys():
            return user_data['coords']
        else:
            return []

    @property
    def polygons(self):
        """
        Coordinates of polygons as drawn on an image.

        These coordinates can be drawn directly to an image using lighting.imagepoly
        and should be in the exact same locatinos as they were drawn.
        """
        coords = self._coords
        # convert from x/y to row/column indexing
        polygons = map(lambda b: asarray(b)[:, ::-1].tolist(), coords)
        return polygons

    def points(self, z=None):
        """
        Points contained in regions drawn on an image

        Parameters
        ----------
        z : int, optiona, default=None
            Append a z-index to coordinates (yielding three dimensional coordinates)
        """
        coords = self._coords
        return [polygon_to_points(x, z) for x in coords]

    def masks(self, dims, z=None):
        """
        Binary masks with regions filled in as 1s or 0s.

        Parameters
        ----------
        dims : array-like
            Specify the dimensions of the image containing the polygons

        z : int, optional, default=None
            Use a z-index to insert regions into the appropriate slice if using
            three-dimensional volumes.
        """
        coords = self._coords
        return [polygon_to_mask(x, dims, z) for x in coords]


@viztype
class Gallery(Base):

    _name = 'gallery'

    @staticmethod
    def clean(imagedata):
        """
        Display a collection of arrays as browsable images with thumbnails.

        .. image:: gallery.png

        Parameters
        ----------
        imagedata : array-like, or list of array-like
            Image or list of images as two dimensional (grayscale) or three dimensional (RGB) arrays.
        """

        if isinstance(imagedata, ndarray):
            imagedata = [imagedata]

        outdict = [array_to_im(im) for im in imagedata]

        return {'images': outdict}
