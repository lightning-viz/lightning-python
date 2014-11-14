from lightning.types.base import Base
from lightning.types.decorators import imgtype
from lightning.types.utils import array_to_im


@imgtype
class Image(Base):
    _name = 'image'
    @staticmethod
    def clean(imagedata):

        out = []
        out.append(array_to_im(imagedata))
        return {'images': out}


@imgtype
class Volume(Base):

    _name = 'volume'

    @staticmethod
    def clean(imagedata):

        out = []
        for im in imagedata:
            out.append(array_to_im(im))
        return {'images': out}


@imgtype
class Gallery(Base):

    _name = 'gallery'

    @staticmethod
    def clean(imagedata):

        out = []
        for im in imagedata:
            out.append(array_to_im(im))
        return {'images': out}
