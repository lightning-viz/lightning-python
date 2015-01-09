from lightning.types.base import Base
from lightning.types.decorators import viztype
from lightning.types.utils import array_to_lines, vecs_to_points, \
    mat_to_links, array_to_im, add_property, mat_to_array, list_to_regions


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
class ScatterLine(Base):

    _name = 'scatter-line'
    _func = 'scatterline'

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
        series = array_to_lines(series)
        outdict = {'points': points, 'series': series}

        outdict = add_property(outdict, color, 'color')
        outdict = add_property(outdict, label, 'label')
        outdict = add_property(outdict, size, 'size')
        outdict = add_property(outdict, alpha, 'alpha')

        return outdict

@viztype
class Matrix(Base):

    _name = 'matrix'

    @staticmethod
    def clean(matrix, colormap=None):
        """
        Visualize a matrix or table as a heat map.

        Parameters
        ----------
        matrix : array-like
            Two-dimensional array of matrix data

        colormap : string
            Specification of color map, only colorbrewer types supported
        """

        matrix = mat_to_array(matrix)
        outdict = {'matrix': matrix}

        outdict = add_property(outdict, colormap, 'colormap')

        return outdict

@viztype
class Adjacency(Base):

    _name = 'adjacency'

    @staticmethod
    def clean(matrix, label=None):

        """
        Visualize an adjacency matrix.



        Parameters
        ----------
        matrix : array-like
            Two-dimensional array of matrix data

        colormap : string
            Specification of color map, only colorbrewer types supported
        """

        links = mat_to_links(matrix)
        nodes = range(0, matrix.shape[0])
        outdict = {'links': links, 'nodes': nodes}

        outdict = add_property(outdict, label, 'label')

        return outdict


@viztype
class Line(Base):

    _name = 'line'

    @staticmethod
    def clean(series, index=None, color=None, label=None, size=None):
        """
        Create a line plot.

        Can plot a single series as a line, or multiple series as multiple lines.

        Parameters
        ----------
        series : array-like, (n,m)
            Input data for line plot, typically n series each of length m.
            Can also pass a list where each individual series is of a different length.

        index : array-like, (m,)
            Specify index for the x-axis of the line plot.

        color : array-like, optional, singleton or (n,3)
            Single rgb value or array to set line colors

        label : array-like, optional, singleton or (n,)
            Single integer or array to set line colors via group labels

        size : array-like, optional, singleton or (n,)
            Single size or array to set line thickness
        """
        
        series = array_to_lines(series)
        outdict = {'series': series}

        outdict = add_property(outdict, color, 'color')
        outdict = add_property(outdict, size, 'size')
        outdict = add_property(outdict, label, 'label')
        outdict = add_property(outdict, index, 'index')

        return outdict


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
        """
        Create a node-link graph with bundled edges
        from a set of points and a connectivity matrix.

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

        points = vecs_to_points(x, y)
        links = mat_to_links(matrix)

        outdict = {'links': links, 'nodes': points}

        outdict = add_property(outdict, color, 'color')
        outdict = add_property(outdict, label, 'label')
        outdict = add_property(outdict, size, 'size')

        if imagedata is not None:
            images = array_to_im(imagedata)
            outdict['images'] = images

        return outdict

@viztype
class Map(Base):

    _name = 'map'

    @staticmethod
    def clean(regions, values):
        """
        Create a chloropleth map of the world or United States.

        Inputs are weights for each region, which will be used to color regions.
        Regions are either strings of length two (for a US map) or three (for world map).

        Parameters
        ----------
        regions : string or list
            String identifiers for map regions, either length two strings (for states
            in a US map) or length three strings (for countries in a world map)

        weights : scalar or list
            Values to use to color each region
        """

        regions = list_to_regions(regions)
        outdict = {'regions': regions}

        outdict = add_property(outdict, values, 'values')

        print(outdict)

        return outdict