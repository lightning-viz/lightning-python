from lightning.types.base import Base
from lightning.types.decorators import viztype
from lightning.types.utils import array_to_lines, vecs_to_points, \
    mat_to_links, array_to_im, add_property


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
        x, y : array-like, each (n,)
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

        points = vecs_to_points(x, y)
        outdict = {'points': points}

        outdict = add_property(outdict, color, 'color')
        outdict = add_property(outdict, label, 'label')
        outdict = add_property(outdict, size, 'size')
        outdict = add_property(outdict, alpha, 'alpha')

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
        x, y : array-like, each (n,)
            Input data

        color : array-like, optional, singleton or (n,3)
            Single rgb value or array to set colors

        label : array-like, optional, singleton or (n,)
            Single integer or array to set colors via groups

        size : array-like, optional, singleton or (n,)
            Single size or array to set point sizes
        """
        
        points = vecs_to_points(x, y)
        outdict = {'points': points}

        outdict = add_property(outdict, color, 'color')
        outdict = add_property(outdict, label, 'label')
        outdict = add_property(outdict, size, 'size')

        return outdict

@viztype
class ROI(Base):

    _name = 'roi'

    @staticmethod
    def clean(x, y, series, color=None, label=None, size=None, alpha=None):
        """
        Create a linked scatter / line plot.

        In this visualization, each point in the scatter plot is linked to a line.
        Hovering over points in the scatter plot will show the corresponding line.

        Parameters
        ----------
        x, y : array-like, each (n,)
            Input data for scatter plot as x,y coordinates

        t : array-like
            Input data for line plot

        color : array-like, optional, singleton or (n,3)
            Single rgb value or array to set point colors

        label : array-like, optional, singleton or (n,)
            Single integer or array to set point colors via group labels

        size : array-like, optional, singleton or (n,)
            Single size or array to set point sizes
        """

        points = vecs_to_points(x, y)
        timeseries = array_to_lines(series)
        outdict = {'points': points, 'timeseries': timeseries}

        outdict = add_property(outdict, color, 'color')
        outdict = add_property(outdict, label, 'label')
        outdict = add_property(outdict, size, 'size')
        outdict = add_property(outdict, alpha, 'alpha')

        return outdict

@viztype
class Matrix(Base):

    _name = 'matrix'

    @staticmethod
    def clean(matrix, label=None):

        links, nodes = mat_to_links(matrix)
        return {'links': links, 'nodes': nodes}


@viztype
class Line(Base):

    _name = 'line'

    @staticmethod
    def clean(series):
        
        data = array_to_lines(series)
        return {'data': data}
        
@viztype
class LineStreaming(Base):

    _name = 'line-streaming'
    _func = 'linestreaming'

    @staticmethod
    def clean(series):

        data = array_to_lines(series)
        return {'data': data}

@viztype
class LineStacked(Base):

    _name = 'line-stacked'
    _func = 'linestacked'

    @staticmethod
    def clean(series):

        data = array_to_lines(series)
        return {'data': data}


@viztype
class Force(Base):

    _name = 'force'
    _func = 'force'

    @staticmethod
    def clean(matrix, color=None, label=None, size=None):
        """
        Create a force-directed network from a connectivity matrix.

        Parameters
        ----------
        matrix : array-like, (n,n)
            Input data with connectivity matrix. Can be binary or continuous-valued
            for weighted edges.

        color : array-like, optional, singleton or (n,3)
            Single rgb value or array to set node colors

        label : array-like, optional, singleton or (n,)
            Single integer or array to set node colors via group labels

        size : array-like, optional, singleton or (n,)
            Single size or array to set node sizes
        """

        links = mat_to_links(matrix)
        nodes = range(0, matrix.shape[0])

        outdict = {'links': links, 'nodes': nodes}

        outdict = add_property(outdict, color, 'color')
        outdict = add_property(outdict, label, 'label')
        outdict = add_property(outdict, size, 'size')

        return outdict

@viztype
class Graph(Base):

    _name = 'graph'
    _func = 'graph'

    @staticmethod
    def clean(x, y, matrix, color=None, label=None, size=None, imagedata=None):
        """
        Create a node-link graph from a set of points and a connectivity matrix.

        Parameters
        ----------
        x,y : array-like, each (n,)
            Input data for nodes (x,y coordinates)

        matrix : array, (n,n)
            Input data with connectivity matrix. Can be binary or continuous-valued
            (for weighted edges).

        color : array-like, optional, singleton or (n,) or (n,3)
            Single rgb value or array to set node colors

        label : array-like, optional, singleton or (n,)
            Single integer or array to set node colors via group labels

        size : array-like, optional, singleton or (n,)
            Single size or array to set node sizes
        """

        links = mat_to_links(matrix)
        nodes = vecs_to_points(x, y)

        outdict = {'links': links, 'nodes': nodes}

        outdict = add_property(outdict, color, 'color')
        outdict = add_property(outdict, label, 'label')
        outdict = add_property(outdict, size, 'size')

        if imagedata is not None:
            images = array_to_im(imagedata)
            outdict['images'] = images

        return outdict


@viztype
class GraphBundled(Base):

    _name = 'graph-bundled'
    _func = 'graphbundled'

    @staticmethod
    def clean(x, y, matrix, color=None, label=None, size=None, imagedata=None):

        points = vecs_to_points(x, y)
        links = mat_to_links(matrix)

        outdict = {'links': links, 'points': points}

        outdict = add_property(outdict, color, 'color')
        outdict = add_property(outdict, label, 'label')
        outdict = add_property(outdict, size, 'size')

        if imagedata is not None:
            images = array_to_im(imagedata)
            outdict['images'] = images

        return outdict