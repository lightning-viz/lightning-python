from lightning.types.base import Base
from lightning.types.decorators import viztype
from lightning.types.utils import array_to_lines, vecs_to_points, add_property


@viztype
class LineStreaming(Base):

    _name = 'line-streaming'
    _func = 'linestreaming'
    _local = False
    _options = dict(Base._options, **{
        'max_width': {'default': 50, 'name': 'maxWidth'},
        'zoom': {'default': False}
        }
    )

    @staticmethod
    def clean(series, index=None, color=None, group=None, size=None, xaxis=None, yaxis=None):
        """
        Plot streaming one-dimensional series data as updating lines.

        Plotting once returns a visualization on which 'append' can be called
        to add new data in a streaming fashion. New lines will appear on the right.

        .. image:: line-streaming.png

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

        size : array-like, optional, singleton or (n,)
            Single size or array to set line thickness

        xaxis : str, optional, default = None
            Label for x-axis

        yaxis : str, optional, default = None
            Label for y-axis

        max_width : int, optional, default = 50
            The maximum number of time points to show before plot shifts.
        """

        series = array_to_lines(series)
        outdict = {'series': series}

        outdict = add_property(outdict, color, 'color')
        outdict = add_property(outdict, size, 'size')
        outdict = add_property(outdict, group, 'group')
        outdict = add_property(outdict, index, 'index')
        outdict = add_property(outdict, xaxis, 'xaxis')
        outdict = add_property(outdict, yaxis, 'yaxis')

        return outdict


@viztype
class ScatterStreaming(Base):

    _name = 'scatter-streaming'
    _func = 'scatterstreaming'
    _local = False
    _options = dict(Base._options, **{
        'brush': {'default': False},
        'zoom': {'default': True},
        'tooltips': {'default': False},
        }
    )

    @staticmethod
    def clean(x, y, values=None, labels=None, group=None, color=None, colormap=None, size=None, xaxis=None, yaxis=None):
        """
        Create a streaming scatter plot of x and y.

        Plotting once returns a visualization on which 'append' can be called to add new data
        in a streaming fashion. The opacity of old and new data is automatically set
        to highlight the most recent data and fade old data away.

        .. image:: scatter-streaming.png

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

        xaxis : str, optional, default = None
            Label for x-axis

        yaxis : str, optional, default = None
            Label for y-axis
        """

        points = vecs_to_points(x, y)
        outdict = {'points': points}

        outdict = add_property(outdict, color, 'color')
        outdict = add_property(outdict, group, 'group')
        outdict = add_property(outdict, values, 'values')
        outdict = add_property(outdict, labels, 'labels')
        outdict = add_property(outdict, colormap, 'colormap')
        outdict = add_property(outdict, size, 'size')
        outdict = add_property(outdict, xaxis, 'xaxis')
        outdict = add_property(outdict, yaxis, 'yaxis')

        return outdict
