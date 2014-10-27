import requests
import os
import time
import json
from numpy import ndarray, asarray, vstack, transpose, nonzero, \
    concatenate, atleast_2d, ones, int, zeros, hstack, newaxis
from session import Session
from visualization import Visualization
from matplotlib.pyplot import imsave
from matplotlib.pyplot import cm
import io


class Lightning(object):

    data_dict_inputs = {
        'points': ['x', 'y', 'i'],
        'colors': ['r', 'g', 'b'],
        'labels': ['k'],
        'links': ['source', 'target', 'value'],
        'nodes': ['group']
    }

    def __init__(self, host="http://localhost:3000", ipython=False):
        self.host = host
        
        if ipython:
            self.enable_ipython()

    def enable_ipython(self, **kwargs):
        '''
        ipython code inspired by code powering similar functionality in mpld3:
        https://github.com/jakevdp/mpld3/blob/master/mpld3/_display.py#L357
        '''

        from IPython.core.getipython import get_ipython
        ip = get_ipython()
        formatter = ip.display_formatter.formatters['text/html']
        formatter.for_type(Visualization,
                           lambda viz, kwds=kwargs: viz.get_html())

    def disable_ipython(self):
        from IPython.core.getipython import get_ipython
        ip = get_ipython()
        formatter = ip.display_formatter.formatters['text/html']
        formatter.type_printers.pop(Visualization, None)

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

    def _check_colors(self, clrs):
    
        clrs = asarray(clrs)
        if clrs.ndim == 2 and clrs.shape[1] == 1:
            clrs = clrs.flatten()
        if clrs.ndim == 2 and clrs.shape[0] == 1:
            clrs = clrs.flatten()
        if clrs.ndim == 1:
            clrs = clrs[:,newaxis]
        elif clrs.shape[1] != 3:
            raise Exception("Color array must have three values per point")
        return clrs

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

    def _vecs_to_points(self, x, y):
        
        x = asarray(x)
        y = asarray(y)
        points = vstack([x, y, range(0,len(x))]).T

        return points

    def _mat_to_links(self, mat, labels=None):

        # get nonzero entries as list with the source, target, and value as columns
        inds = nonzero(mat)
        links = concatenate((transpose(nonzero(mat)), atleast_2d(mat[inds]).T), axis=1)

        # pick group assignments (default is all 1s)
        n = mat.shape[0]
        if labels is None:
            nodes = zeros((1, n)).T
        else:
            if labels.size != n:
                raise Exception("Must provide label for each row")
            nodes = labels.astype(int).reshape(labels.size, 1)

        return links, nodes

    def image(self, imagedata, type="image"):

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

    def forcenetwork(self, mat, labels=None):

        links, nodes = self._mat_to_links(mat, labels)

        return self.plot(links=links, nodes=nodes, type='force-directed-network')

    def spatialnetwork(self, mat, x, y, imagedata=None, bundling=False):

        points = self._vecs_to_points(x, y)

        links, nodes = self._mat_to_links(mat)

        if bundling:
            plottype = 'force-bundle'
        else:
            plottype = 'node-link'

        viz = self.plot(links=links, points=points, type=plottype)

        if imagedata is not None:
            viz.append_image(self._array_to_im(imagedata))
        
        return viz

    def roi(self, x, y, data):

        points = self._vecs_to_points(x, y)

        timeseries = self._ensure_dict_or_list(data)

        return self.plot(points=points, timeseries=timeseries, type='roi')

    def matrix(self, mat, labels=None):

        links, nodes = self._mat_to_links(mat, labels)

        return self.plot(links=links, nodes=nodes, type="matrix")

    def scatter(self, x, y, clrs=None):

        points = self._vecs_to_points(x, y)

        if clrs is not None:
            clrs = self._check_colors(clrs)
            if clrs.shape[1] == 1:
                return self.plot(points=points, labels=clrs, type='scatter')
            else:
                return self.plot(points=points, colors=clrs, type='scatter')
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


        

