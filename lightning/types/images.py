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
    
    def get_coords(self, return_type='bounds', dims=None, z=None):
        """
        Get data from polygons drawn on image.

        Parameters
        ----------
        return_type : string, optional, default='bounds'
            Specification of output data. Options are 'bounds','points', and 'mask'

        dims : array-like, optional, default=None
            Specify the size of the image containing the polygon.

        z : int, optional, default=None
            When returning points or masks, embed the given z-index in the coordinates (for points),
            or use them to create a volume (for masks). Use when working with a
            two-dimensional image from a three-dimensional volume.
        """

        user_data = self.get_user_data()['settings']
        if 'coords' in user_data.keys():
            coords = user_data['coords']

            if return_type == 'bounds':
                return coords

            elif return_type == 'points':
                return [polygon_to_points(x, z) for x in coords]

            elif return_type == 'mask':
                if not dims:
                    raise Exception('Must provide image dimensions to return mask')
                return [polygon_to_mask(x, dims, z) for x in coords]

            else:
                raise Exception('Option %s is not supported' % return_type)
        else:
            return []


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
