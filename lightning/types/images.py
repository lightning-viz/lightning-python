from lightning.types.base import Base
from lightning.types.decorators import viztype
from lightning.types.utils import array_to_im
import requests


@viztype
class Image(Base):
    _name = 'image'
    
    @staticmethod
    def clean(imagedata):

        out = []
        out.append(array_to_im(imagedata))
        return {'images': out}

    @property
    def coords(self):
        user_data = self.get_user_data()['settings']
        if 'coords' in user_data.keys():
            return user_data['coords']
        else:
            return []

@viztype
class Volume(Base):

    _name = 'volume'

    @staticmethod
    def clean(imagedata):

        out = []
        for im in imagedata:
            out.append(array_to_im(im))
        return {'images': out}


@viztype
class Gallery(Base):

    _name = 'gallery'

    @staticmethod
    def clean(imagedata):

        out = []
        for im in imagedata:
            out.append(array_to_im(im))
        return {'images': out}
