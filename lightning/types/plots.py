from lightning.types.base import Base
from lightning.types.decorators import viztype
from lightning.types.utils import array_to_lines, vecs_to_points, \
    parse_links, add_property, mat_to_array, list_to_regions, parse_nodes, ndarray


@viztype
class Plot(Base):

    _name = 'plot'
    _options = dict(Base._options, **{
        'type': {'default': None},
        }
    )

    @staticmethod
    def clean(data=None):
        """
        Generic plotting function.

        Provide arbitrary data and options objects as dictionaries,
        and a plot type as a string. The data and options dictionary will be passed
        directly to the plot, without any parsing or formatting,
        so make sure it is of the appropriate for your visualization
        (e.g. {"series": [1,2,3]} for a "line" visualization).

        Most useful when providing data to custom visualizations, as opposed
        to the included plot types (e.g. lightning.scatter, lightning.line, etc.)
        which do automatic parsing and formatting.

        Parameters
        ----------
        data : dict
            Dictionary with data to plot

        type : str
            Name of plot (e.g. 'line' or 'scatter')
        """
        return data


@viztype
class Scatter(Base):

    _name = 'scatter'
    _options = dict(Base._options, **{
        'tooltips': {'default': True},
        'zoom': {'default': True},
        'brush': {'default': True}
        }
    )

    @staticmethod
    def clean(x, y, labels=None, values=None, color=None, group=None, colormap=None,
              size=None, alpha=None, xaxis=None, yaxis=None):
        """
        Plot two-dimensional data as points.

        .. image:: scatter.png

        Parameters
        ----------
        x, y : array-like, each (n,)
            Input data

        values : array-like, optional, singleton or (n,)
            Values to set node colors via a linear scale

        labels : array-like, optional, (n,)
            Array of text labels to set tooltips

        color : array-like, optional, singleton or (n,3)
            Single rgb value or array to set colors

        group : array-like, optional, singleton or (n,)
            Single integer or array to set colors via groups

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

        tooltips : boolean, optional, default=True
            Whether to show tooltips

        zoom : boolean, optional, default=True
            Whether to allow zooming

        brush : boolean, optional, default=True
            Whether to support brushing
        """

        points = vecs_to_points(x, y)
        outdict = {'points': points}

        outdict = add_property(outdict, color, 'color')
        outdict = add_property(outdict, group, 'group')
        outdict = add_property(outdict, labels, 'labels')
        outdict = add_property(outdict, values, 'values')
        outdict = add_property(outdict, colormap, 'colormap')
        outdict = add_property(outdict, size, 'size')
        outdict = add_property(outdict, alpha, 'alpha')
        outdict = add_property(outdict, xaxis, 'xaxis')
        outdict = add_property(outdict, yaxis, 'yaxis')

        return outdict

    def selected(self):
        """
        Selected points from scatter plot as indices
        """
        user_data = self._get_user_data()['settings']
        if 'selected' in user_data.keys():
            return user_data['selected']
        else:
            return []

    def points(self):
        """
        Selected points from scatter plot as x,y coordinates
        """
        user_data = self._get_user_data()['settings']
        if 'x' in user_data.keys() and 'y' in user_data.keys():
            return user_data['x'], user_data['y']
        else:
            return []

@viztype
class Matrix(Base):

    _name = 'matrix'
    _options = dict(Base._options, **{
        'numbers': {'default': False}
        }
    )

    @staticmethod
    def clean(matrix, colormap=None, row_labels=None, column_labels=None):
        """
        Visualize a dense matrix or table as a heat map.

        .. image:: matrix.png

        Parameters
        ----------
        matrix : array-like (n,m)
            Two-dimensional array of matrix data

        row_labels : array-like (n,)
            Array of rows to label columns

        column_labels : array-like (m,)
            Array of strings to label columns

        colormap : string
            Specification of color map, only colorbrewer types supported

        numbers : boolean, optional, default=True
            Whether to show numbers on cells
        """

        matrix = mat_to_array(matrix)
        outdict = {'matrix': matrix}

        outdict = add_property(outdict, colormap, 'colormap')
        outdict = add_property(outdict, row_labels, 'rowLabels')
        outdict = add_property(outdict, column_labels, 'columnLabels')

        return outdict

@viztype
class Adjacency(Base):

    _name = 'adjacency'
    _options = dict(Base._options, **{
        'numbers': {'default': False},
        'symmetric': {'default': True},
        'sort': {'default': 'group'}
        }
    )

    @staticmethod
    def clean(conn, labels=None, group=None):
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

        labels : array-like, (n,)
            Text labels for each item (will label rows and columns)

        group : array-like, optional, singleton or (n,)
            Single integer or array to set colors via groups

        sort : str, optional, default='group'
            What to sort by, options are 'group' | 'degree'

        numbers : boolean, optional, default=False
            Whether to show numbers on cells

        symmetric : boolean, optional, default=True
            Whether to make links symmetrical
        """
        links = parse_links(conn)
        nodes = parse_nodes(conn)

        outdict = {'links': links, 'nodes': nodes}

        outdict = add_property(outdict, labels, 'labels')
        outdict = add_property(outdict, group, 'group')

        return outdict


@viztype
class Line(Base):

    _name = 'line'
    _options = dict(Base._options, **{
        'zoom': {'default': True}
        }
    )

    @staticmethod
    def clean(series, index=None, color=None, group=None, thickness=None, xaxis=None, yaxis=None):
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

        group : array-like, optional, singleton or (n,)
            Single integer or array to set line colors via group assignment

        thickness : array-like, optional, singleton or (n,)
            Single size or array to set line thickness

        xaxis : str, optional, default = None
            Label for x-axis

        yaxis : str, optional, default = None
            Label for y-axis

        zoom : boolean, optional, default=True
            Whether to allow zooming
        """

        series = array_to_lines(series)
        outdict = {'series': series}

        outdict = add_property(outdict, color, 'color')
        outdict = add_property(outdict, thickness, 'thickness')
        outdict = add_property(outdict, group, 'group')
        outdict = add_property(outdict, index, 'index')
        outdict = add_property(outdict, xaxis, 'xaxis')
        outdict = add_property(outdict, yaxis, 'yaxis')

        return outdict

@viztype
class Force(Base):

    _name = 'force'
    _options = dict(Base._options, **{
        'tooltips': {'default': True},
        'zoom': {'default': True},
        'brush': {'default': True}
        }
    )

    @staticmethod
    def clean(conn, values=None, labels=None, color=None, group=None, colormap=None, size=None):
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

        values : array-like, optional, singleton or (n,)
            Values to set node colors via a linear scale

        labels : array-like, optional, (n,)
            Array of text labels to set tooltips

        color : array-like, optional, singleton or (n,3)
            Single rgb value or array to set node colors

        group : array-like, optional, singleton or (n,)
            Single integer or array to set node colors via group assignment

        colormap : string
            Specification of color map, only colorbrewer types supported

        size : array-like, optional, singleton or (n,)
            Single size or array to set node sizes

        tooltips : boolean, optional, default=True
            Whether to show tooltips

        zoom : boolean, optional, default=True
            Whether to allow zooming

        brush : boolean, optional, default=True
            Whether to support brushing
        """

        links = parse_links(conn)
        nodes = parse_nodes(conn)

        outdict = {'links': links, 'nodes': nodes}

        outdict = add_property(outdict, color, 'color')
        outdict = add_property(outdict, group, 'group')
        outdict = add_property(outdict, values, 'values')
        outdict = add_property(outdict, labels, 'labels')
        outdict = add_property(outdict, colormap, 'colormap')
        outdict = add_property(outdict, size, 'size')

        return outdict

    def selected(self):
        """
        Selected points from force plot
        """
        user_data = self._get_user_data()['settings']
        if 'selected' in user_data.keys():
            return user_data['selected']
        else:
            return []

@viztype
class Circle(Base):

    _name = 'circle'

    @staticmethod
    def clean(conn, group=None, color=None, labels=None):
        """
        Create a circular graph from connectivity data.

        .. image:: circle.png

        Parameters
        ----------
        conn : array-like, (n,n) or (n,3) or (n,2)
            Input connectivity data as either a matrix or a list of links.
            Matrix can be binary or continuous valued. Links should contain
            either 2 elements per link (source, target),
            or 3 elements (source, target, value).

        group : array-like, optional, (m,n) or (n,)
            Hierarchical group assignments, where m is
            the number of groups

        color : array-like, optional, singleton or (k,3)
            Single rgb value or array to set colors of top-level group,
            where k is the number of unique elements in the top-level group

        labels : array-like, optional, (n,)
            Array of text labels to label nodes
        """
        links = parse_links(conn)
        nodes = parse_nodes(conn)

        outdict = {'links': links, 'nodes': nodes}

        outdict = add_property(outdict, labels, 'labels')
        outdict = add_property(outdict, color, 'color')

        if group is not None:
            if isinstance(group, ndarray):
                group = group.tolist()
            if isinstance(group, list):
                if not isinstance(group[0], list):
                    if isinstance(group[0], ndarray):
                        group = [g.tolist() for g in group]
                    else:
                        group = [group]
            else:
                raise ValueError('group must be list or nested list')

            outdict['group'] = group

        return outdict


@viztype
class Graph(Base):

    _name = 'graph'
    _options = dict(Base._options, **{
        'tooltips': {'default': True},
        'zoom': {'default': True},
        'brush': {'default': True}
        }
    )

    @staticmethod
    def clean(x, y, conn, values=None, labels=None,color=None, group=None, colormap=None, size=None):
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

        values : array-like, optional, singleton or (n,)
            Values to set node colors via a linear scale

        labels : array-like, optional, (n,)
            Array of text labels to set tooltips

        color : array-like, optional, singleton or (n,) or (n,3)
            Single rgb value or array to set node colors

        group : array-like, optional, singleton or (n,)
            Single integer or array to set node colors via group assignment

        colormap : string
            Specification of color map, only colorbrewer types supported

        size : array-like, optional, singleton or (n,)
            Single size or array to set node sizes

        tooltips : boolean, optional, default=True
            Whether to show tooltips

        zoom : boolean, optional, default=True
            Whether to allow zooming

        brush : boolean, optional, default=True
            Whether to support brushing
        """

        links = parse_links(conn)
        nodes = vecs_to_points(x, y)

        outdict = {'links': links, 'nodes': nodes}

        outdict = add_property(outdict, color, 'color')
        outdict = add_property(outdict, group, 'group')
        outdict = add_property(outdict, values, 'values')
        outdict = add_property(outdict, labels, 'labels')
        outdict = add_property(outdict, colormap, 'colormap')
        outdict = add_property(outdict, size, 'size')

        return outdict


@viztype
class GraphBundled(Base):

    _name = 'graph-bundled'
    _func = 'graphbundled'
    _options = dict(Base._options, **{
        'tooltips': {'default': True},
        'zoom': {'default': True},
        'brush': {'default': True}
        }
    )

    @staticmethod
    def clean(x, y, conn, labels=None, values=None, color=None, group=None, colormap=None, size=None):
        """
        Create a bundled node-link graph from spatial points and their connectivity.

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

        values : array-like, optional, singleton or (n,)
            Values to set node colors via a linear scale

        labels : array-like, optional, (n,)
            Array of text labels to set tooltips

        color : array-like, optional, singleton or (n,) or (n,3)
            Single rgb value or array to set node colors

        group : array-like, optional, singleton or (n,)
            Single integer or array to set node colors via group assignment

        colormap : string
            Specification of color map, only colorbrewer types supported

        size : array-like, optional, singleton or (n,)
            Single size or array to set node sizes

        tooltips : boolean, optional, default=True
            Whether to show tooltips

        zoom : boolean, optional, default=True
            Whether to allow zooming

        brush : boolean, optional, default=True
            Whether to support brushing
        """
        links = parse_links(conn)
        points = vecs_to_points(x, y)

        outdict = {'links': links, 'nodes': points}

        outdict = add_property(outdict, color, 'color')
        outdict = add_property(outdict, group, 'group')
        outdict = add_property(outdict, values, 'values')
        outdict = add_property(outdict, labels, 'labels')
        outdict = add_property(outdict, colormap, 'colormap')
        outdict = add_property(outdict, size, 'size')

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


@viztype
class Histogram(Base):

    _name = 'histogram'
    _options = dict(Base._options, **{
        'zoom': {'default': True}
        }
    )

    @staticmethod
    def clean(values, bins=None):
        """
        Create a histogram.

        .. image:: histogram.png

        Parameters
        ----------
        values : list
            Values to plot a histogram of

        bins : number, optional
            Number of bins to used in the histogram. If unspecified
            will default to sqrt(len(values))
        """

        outdict = {'values': values}
        outdict = add_property(outdict, bins, 'bins')

        return outdict


@viztype
class VegaLite(Base):

    _name = 'vega-lite'
    _func = 'vega_lite'

    @staticmethod
    def clean(spec):
        outdict = {}
        outdict = add_property(outdict, spec, 'spec')
        return outdict
