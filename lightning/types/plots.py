from lightning.types.base import Base
from lightning.types.decorators import viztype
from lightning.types.utils import array_to_lines, vecs_to_points, \
    parse_links, array_to_im, add_property, mat_to_array, list_to_regions, \
    check_colormap, parse_nodes


@viztype
class Generic(Base):

    @staticmethod
    def clean(data):
        return data


@viztype
class Scatter(Base):

    _name = 'scatter'

    @staticmethod
    def clean(x, y, color=None, label=None, value=None, colormap=None, size=None, alpha=None, xaxis=None, yaxis=None):
        """
        Plot two-dimensional data as points.

        .. image:: scatter.png

        Parameters
        ----------
        x, y : array-like, each (n,)
            Input data

        color : array-like, optional, singleton or (n,3)
            Single rgb value or array to set colors

        label : array-like, optional, singleton or (n,)
            Single integer or array to set colors via groups

        value : array-like, optional, singleton or (n,)
            Values to set node colors via a linear scale

        colormap : string
            Specification of color map, only colorbrewer types supported

        size : array-like, optional, singleton or (n,)
            Single size or array to set point sizes

        alpha : array-like, optional, singleton or (n,)
            Single alpha value or array to set fill and stroke opacity

        xaxis : str, optional, default = None
            Label for x-axis

        yaxis : str, optional, default = None
            Label for y-axis
        """

        points = vecs_to_points(x, y)
        outdict = {'points': points}

        outdict = add_property(outdict, color, 'color')
        outdict = add_property(outdict, label, 'label')
        outdict = add_property(outdict, value, 'value')
        outdict = add_property(outdict, colormap, 'colormap')
        outdict = add_property(outdict, size, 'size')
        outdict = add_property(outdict, alpha, 'alpha')
        outdict = add_property(outdict, xaxis, 'xaxis')
        outdict = add_property(outdict, yaxis, 'yaxis')

        return outdict

@viztype
class Matrix(Base):

    _name = 'matrix'

    @staticmethod
    def clean(matrix, colormap=None):
        """
        Visualize a dense matrix or table as a heat map.

        .. image:: matrix.png

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
    def clean(conn, label=None):

        """
        Visualize a sparse adjacency matrix.

        .. image:: adjacency.png

        Parameters
        ----------
       conn : array-like, (n,n) or (n,3) or (n,2)
            Input connectivity data as either a matrix or a list of links.
            Matrix can be binary or continuous valued. Links should contain
            either 2 elements per link (source, target),
            or 3 elements (source, target, value).

        label : array-like, optional, singleton or (n,)
            Single integer or array to set colors via groups
        """
        links = parse_links(conn)
        nodes = parse_nodes(conn)

        outdict = {'links': links, 'nodes': nodes}

        outdict = add_property(outdict, label, 'label')

        return outdict


@viztype
class Line(Base):

    _name = 'line'
    _validOptions = {
        'log_scale_x': {
            'default_value': False,
            'lightning_name': 'logScaleX'
        },
        'log_scale_y': {
            'default_value': False,
            'lightning_name': 'logScaleY'
        }
    }

    @staticmethod
    def clean(series, index=None, color=None, label=None, size=None, xaxis=None, yaxis=None):
        """
        Plot one-dimensional series data as lines.

        .. image:: line.png

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

        xaxis : str, optional, default = None
            Label for x-axis

        yaxis : str, optional, default = None
            Label for y-axis
        """

        series = array_to_lines(series)
        outdict = {'series': series}

        outdict = add_property(outdict, color, 'color')
        outdict = add_property(outdict, size, 'size')
        outdict = add_property(outdict, label, 'label')
        outdict = add_property(outdict, index, 'index')
        outdict = add_property(outdict, xaxis, 'xaxis')
        outdict = add_property(outdict, yaxis, 'yaxis')

        return outdict


@viztype
class LineStacked(Base):

    _name = 'line-stacked'
    _func = 'linestacked'

    @staticmethod
    def clean(series, color=None, label=None, size=None):
        """
        Create a browsable array of line plots.

        .. image:: linestacked.png

        Parameters
        ----------
        series : array-like, (n,m)
            Input data for lines, typically n series each of length m.
            Can also pass a list where each individual series is of a different length.

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

        return outdict


@viztype
class Force(Base):

    _name = 'force'
    _func = 'force'

    @staticmethod
    def clean(conn, color=None, label=None, value=None, colormap=None, size=None):
        """
        Create a force-directed network from connectivity.

        .. image:: force.png

        Parameters
        ----------
        conn : array-like, (n,n) or (n,3) or (n,2)
            Input connectivity data as either a matrix or a list of links.
            Matrix can be binary or continuous valued. Links should contain
            either 2 elements per link (source, target),
            or 3 elements (source, target, value).

        color : array-like, optional, singleton or (n,3)
            Single rgb value or array to set node colors

        label : array-like, optional, singleton or (n,)
            Single integer or array to set node colors via group labels

        value : array-like, optional, singleton or (n,)
            Values to set node colors via a linear scale

        colormap : string
            Specification of color map, only colorbrewer types supported

        size : array-like, optional, singleton or (n,)
            Single size or array to set node sizes
        """

        links = parse_links(conn)
        nodes = parse_nodes(conn)

        outdict = {'links': links, 'nodes': nodes}

        outdict = add_property(outdict, color, 'color')
        outdict = add_property(outdict, label, 'label')
        outdict = add_property(outdict, value, 'value')
        outdict = add_property(outdict, colormap, 'colormap')
        outdict = add_property(outdict, size, 'size')

        return outdict

@viztype
class Graph(Base):

    _name = 'graph'
    _func = 'graph'

    @staticmethod
    def clean(x, y, conn, color=None, label=None, value=None, colormap=None, size=None, imagedata=None):
        """
        Create a node-link graph from spatial points and their connectivity.

        .. image:: graph.png

        Parameters
        ----------
        x,y : array-like, each (n,)
            Input data for nodes (x,y coordinates)

        conn : array-like, (n,n) or (n,3) or (n,2)
            Input connectivity data as either a matrix or a list of links.
            Matrix can be binary or continuous valued. Links should contain
            either 2 elements per link (source, target),
            or 3 elements (source, target, value).

        color : array-like, optional, singleton or (n,) or (n,3)
            Single rgb value or array to set node colors

        label : array-like, optional, singleton or (n,)
            Single integer or array to set node colors via group labels

        value : array-like, optional, singleton or (n,)
            Values to set node colors via a linear scale

        colormap : string
            Specification of color map, only colorbrewer types supported

        size : array-like, optional, singleton or (n,)
            Single size or array to set node sizes
        """

        links = parse_links(conn)
        nodes = vecs_to_points(x, y)

        outdict = {'links': links, 'nodes': nodes}

        outdict = add_property(outdict, color, 'color')
        outdict = add_property(outdict, label, 'label')
        outdict = add_property(outdict, value, 'value')
        outdict = add_property(outdict, colormap, 'colormap')
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
    def clean(x, y, conn, color=None, label=None, value=None, colormap=None, size=None, imagedata=None):
        """
        Create a node-link graph with bundled edges from spatial points and their connectivity.

        .. image:: graphbundled.png

        Parameters
        ----------
        x,y : array-like, each (n,)
            Input data for nodes (x,y coordinates)

        conn : array-like, (n,n) or (n,3) or (n,2)
            Input connectivity data as either a matrix or a list of links.
            Matrix can be binary or continuous valued. Links should contain
            either 2 elements per link (source, target),
            or 3 elements (source, target, value).

        color : array-like, optional, singleton or (n,) or (n,3)
            Single rgb value or array to set node colors

        label : array-like, optional, singleton or (n,)
            Single integer or array to set node colors via group labels

        value : array-like, optional, singleton or (n,)
            Values to set node colors via a linear scale

        colormap : string
            Specification of color map, only colorbrewer types supported

        size : array-like, optional, singleton or (n,)
            Single size or array to set node sizes
        """
        links, _ = parse_links(conn)
        points = vecs_to_points(x, y)

        outdict = {'links': links, 'nodes': points}

        outdict = add_property(outdict, color, 'color')
        outdict = add_property(outdict, label, 'label')
        outdict = add_property(outdict, value, 'value')
        outdict = add_property(outdict, colormap, 'colormap')
        outdict = add_property(outdict, size, 'size')

        if imagedata is not None:
            images = array_to_im(imagedata)
            outdict['images'] = images

        return outdict

@viztype
class Map(Base):

    _name = 'map'

    @staticmethod
    def clean(regions, values, colormap=None):
        """
        Create a chloropleth map of the world or united states.

        .. image:: map.png

        Parameters
        ----------
        regions : string or list
            String identifiers for map regions, either length two strings (for states
            in a US map) or length three strings (for countries in a world map)

        weights : scalar or list
            Values to use to color each region

        colormap : string
            Specification of color map, only colorbrewer types supported
        """

        regions = list_to_regions(regions)
        outdict = {'regions': regions}

        outdict = add_property(outdict, values, 'values')
        outdict = add_property(outdict, colormap, 'colormap')

        return outdict
