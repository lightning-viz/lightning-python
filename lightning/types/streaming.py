from lightning.types.base import Base
from lightning.types.decorators import viztype
from lightning.types.utils import array_to_lines, vecs_to_points, add_property


@viztype
class LineStreaming(Base):

    _name = 'line-streaming'
    _func = 'linestreaming'

    @staticmethod
    def clean(series, index=None, color=None, label=None, size=None, xaxis=None, yaxis=None):
        """
        Plot streaming one-dimensional series data as updating lines.

        Plotting once returns a visualization on which 'append' can be called
        to add new data in a streaming fashion. New lines will appear on the right.

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
class ScatterStreaming(Base):

    _name = 'scatter-streaming'
    _func = 'scatterstreaming'

    @staticmethod
    def clean(x, y, color=None, label=None, size=None, xaxis=None, yaxis=None):
        """
        Create a streaming scatter plot of x and y.

        Plotting once returns a visualization on which 'append' can be called to add new data
        in a streaming fashion. The opacity of old and new data is automatically set
        to highlight the most recent data and fade old data away.

        .. image:: scatter.png

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

        xaxis : str, optional, default = None
            Label for x-axis

        yaxis : str, optional, default = None
            Label for y-axis
        """

        points = vecs_to_points(x, y)
        outdict = {'points': points}

        outdict = add_property(outdict, color, 'color')
        outdict = add_property(outdict, label, 'label')
        outdict = add_property(outdict, size, 'size')
        outdict = add_property(outdict, xaxis, 'xaxis')
        outdict = add_property(outdict, yaxis, 'yaxis')

        return outdict
