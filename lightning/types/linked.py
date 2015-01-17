from lightning.types.base import Base
from lightning.types.decorators import viztype
from lightning.types.utils import array_to_lines, vecs_to_points, add_property

@viztype
class ScatterLine(Base):

    _name = 'scatter-line'
    _func = 'scatterline'

    @staticmethod
    def clean(x, y, series, color=None, label=None, size=None, alpha=None):
        """
        Create a joint scatter / line plot.

        .. image:: scatterline.png

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
