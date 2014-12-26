from lightning.types.base import Base
from lightning.types.decorators import viztype
from lightning.types.utils import array_to_lines, vecs_to_points, check_color, check_1d, \
    mat_to_links, array_to_im


@viztype
class Generic(Base):

    @staticmethod
    def clean(data):
        return {'data': data}


@viztype
class Scatter(Base):

    _name = 'scatter'

    @staticmethod
    def clean(x, y, color=None, label=None, size=None, alpha=None):
        """
        Create a scatter plot of x and y.

        Parameters
        ----------
        x, y : array-like
            Input data

        color : array-like, optional
            Single rgb value or array to set colors

        label : array-like, optional
            Single integer or array to set colors via groups

        size : array-like, optional
            Single size or array to set point sizes

        alpha : array-like, optional
            Single alpha value or array to set fill and stroke opacity
        """

        points = vecs_to_points(x, y)
        outdict = {'points': points}

        if color is not None:
            c = check_color(color)
            outdict['color'] = c
        if label is not None:
            l = check_1d(label, "label")
            outdict['label'] = l
        if size is not None:
            s = check_1d(size, "size")
            outdict['size'] = s
        if alpha is not None:
            a = check_1d(alpha, "alpha")
            if any(map(lambda d: d <= 0, a)):
                raise Exception('Alpha cannot be 0 or negative')
            outdict['alpha'] = a

        return outdict


@viztype
class ScatterStreaming(Base):

    _name = 'scatter-streaming'
    _func = 'scatterstreaming'

    @staticmethod
    def clean(x, y, color=None, label=None, size=None):
        """
        Create a streaming scatter plot of x and y.

        Plotting once returns a visualization on which 'append' can be called to add new data
        in a streaming fashion. The opacity of old and new data is automatically set
        to highlight the most recent data and fade old data away.

        Parameters
        ----------
        x, y : array-like
            Input data

        color : array-like, optional
            Single rgb value or array to set colors

        label : array-like, optional
            Single integer or array to set colors via groups

        size : array-like, optional
            Single size or array to set point sizes
        """
        
        points = vecs_to_points(x, y)
        outdict = {'points': points}

        if color is not None:
            c = check_color(color)
            outdict['color'] = c
        if label is not None:
            l = check_1d(label, "label")
            outdict['label'] = l
        if size is not None:
            s = check_1d(size, "size")
            outdict['size'] = s

        return outdict

@viztype
class ROI(Base):

    _name = 'roi'

    @staticmethod
    def clean(x, y, timeseries, clrs=None):

        points = vecs_to_points(x, y)
        timeseries = array_to_lines(timeseries)
        if clrs is not None:
            clrs = check_color(clrs)
            return {'points': points, 'timeseries': timeseries, 'colors': clrs}
        else:
            return {'points': points, 'timeseries': timeseries}


@viztype
class Matrix(Base):

    _name = 'matrix'

    @staticmethod
    def clean(mat, labels=None):

        links, nodes = mat_to_links(mat, labels)
        return {'links': links, 'nodes': nodes}


@viztype
class Line(Base):

    _name = 'line'

    @staticmethod
    def clean(data):
        
        data = array_to_lines(data)
        return {'data': data}
        
@viztype
class LineStreaming(Base):

    _name = 'line-streaming'
    _func = 'linestreaming'

    @staticmethod
    def clean(data):

        data = array_to_lines(data)
        return {'data': data}

@viztype
class LineStacked(Base):

    _name = 'line-stacked'
    _func = 'linestacked'

    @staticmethod
    def clean(data):

        data = array_to_lines(data)
        return {'data': data}


@viztype
class Force(Base):

    _name = 'force'
    _func = 'force'

    @staticmethod
    def clean(mat, labels=None):

        links, nodes = mat_to_links(mat, labels)
        return {'links': links, 'nodes': nodes}

@viztype
class Graph(Base):

    _name = 'graph'
    _func = 'graph'

    @staticmethod
    def clean(mat, x, y, imagedata=None, clrs=None):

        points = vecs_to_points(x, y)
        links, nodes = mat_to_links(mat)

        outdict = {'links': links, 'points': points}

        if clrs is not None:
            clrs = check_color(clrs)
            if clrs.shape[1] == 1:
                outdict['labels'] = clrs
            else:
                outdict['colors'] = clrs

        if imagedata is not None:
            images = array_to_im(imagedata)
            outdict['images'] = images

        return outdict


@viztype
class GraphBundled(Base):

    _name = 'graph-bundled'
    _func = 'graphbundled'

    @staticmethod
    def clean(mat, x, y, imagedata=None, clrs=None):

        points = vecs_to_points(x, y)
        links, nodes = mat_to_links(mat)

        outdict = {'links': links, 'points': points}

        if clrs is not None:
            clrs = check_color(clrs)
            if clrs.shape[1] == 1:
                outdict['labels'] = clrs
            else:
                outdict['colors'] = clrs

        if imagedata is not None:
            images = array_to_im(imagedata)
            outdict['images'] = images

        return outdict