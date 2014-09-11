import requests
import os
import time
import json
from numpy import ndarray, asarray, vstack
from session import Session
from matplotlib.pyplot import imsave
from matplotlib.pyplot import cm
import io


class Lightning(object):
    _instance = None
    
    host = "http://lightning.mathisonian.com"

    data_dict_inputs = {
        'points': ['x', 'y'],
        'colors': ['r', 'g', 'b']
    }

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Lightning, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance

    def create_session(self, name=None):
        self.session = Session.create(self.host, name=name)
        return self.session

    def use_session(self, session_id):
        self.session = Session(host=self.host, id=session_id)
        return self.session

    def _check_unkeyed_arrays(self, key, val):

        if not key in self.data_dict_inputs:
            return val

        if not isinstance(val, list):
            raise Exception("Must provide a list")

        if len(val) == 0:
            return val

        if isinstance(val[0], dict) and isinstance(val[-1], dict):
            return val

        if isinstance(val[0], list) and isinstance(val[-1], list):
            # if both the first and last elements are lists
            out = []
            mapping = self.data_dict_inputs[key]
            for l in val:
                out.append(dict(zip(mapping, l)))

            return out

    def _ensure_dict_or_list(self, x):

        if isinstance(x, dict):
            return x

        if isinstance(x, list):
            return x

        try:
            # Convert Numpy arrays to lists
            return x.tolist()
        except Exception:
            pass

        # add other data type conversions here
        raise Exception("Could not convert to correct data type")

    def _array_to_im(self, im):

        imfile = io.BytesIO()
        if im.ndim == 3:
            # if 3D, show as RGB
            imsave(imfile, im, format="png")
        else:
            # if 2D, show as grayscale
            imsave(imfile, im, format="png", cmap=cm.gray)

        if im.ndim > 3:
            raise Exception("Images must be 2 or 3 dimensions")

        return imfile.getvalue()

    def _check_colors(self, clrs):
        clrs = asarray(clrs)
        if clrs.ndim != 2:
            raise Exception("Color array must be two dimensional")
        elif clrs.shape[1] != 3:
            raise Exception("Colors must be three-dimensional")
        else:
            return clrs

    def image(self, imagedata, type=None):

        if not type:
            raise Exception("Must provide a plot type")

        out = []
        # an array means a single image for image display
        if isinstance(imagedata, ndarray):
            out.append(self._array_to_im(imagedata))
            if type == "gallery" or type == "volume":
                raise Exception("must provide multiple images for gallery or volume")
        # a list means a set of images for gallery or volume display
        elif isinstance(imagedata, list):
            if type == "image":
                raise Exception("can only display one image")
            for im in imagedata:
                out.append(self._array_to_im(im))
        else:
            raise Exception("Could not parse image format, must be list or ndarray")

        return self.session.create_visualization(images=out, type=type)

    def scatter(self, x, y, clrs=None):

        x = asarray(x)
        y = asarray(y)
        points = vstack([x, y]).T

        if clrs is not None:
            return self.plot(points=points, colors=self._check_colors(clrs), type='scatter')
        else:
            return self.plot(points=points, type="scatter")

    def plot(self, type=None, **kwargs):

        if not type:
            raise Exception("Must provide a plot type")

        if 'data' in kwargs:
            data = kwargs['data']
            return self.session.create_visualization(data=self._ensure_dict_or_list(data), type=type)

        else:
            data = {}
            for key in kwargs:
                d = self._ensure_dict_or_list(kwargs[key])
                data[key] = self._check_unkeyed_arrays(key, d)

            return self.session.create_visualization(data=data, type=type)


        

