from lightning.types.base import Base
from lightning.types.decorators import viztype
from lightning.types.utils import array_to_lines, vecs_to_points, check_colors, mat_to_links, array_to_im


@viztype
class Generic(Base):

    @staticmethod
    def clean(data):
        return {'data': data}


@viztype
class Scatter(Base):

    _name = 'scatter'

    @staticmethod
    def clean(x, y, clrs=None):
        """
        Create a scatter plot.

        Parameters
        ----------
        x : array
            x values to plot
        y : array
            y values to plot
        clrs : array
            Array of colors, can be rgb triplets or group labels
        """
        points = vecs_to_points(x, y)
        if clrs is not None:
            clrs = check_colors(clrs)
            if clrs.shape[1] == 1:
                return {'points': points, 'labels': clrs}
            else:
                return {'points': points, 'colors': clrs}
        else:
            return {'points': points}


@viztype
class ScatterStreaming(Base):

    _name = 'scatter-streaming'
    _func = 'scatterstreaming'

    @staticmethod
    def clean(x, y, clrs=None):
        
        points = vecs_to_points(x, y)
        if clrs is not None:
            clrs = check_colors(clrs)
            if clrs.shape[1] == 1:
                return {'points': points, 'labels': clrs}
            else:
                return {'points': points, 'colors': clrs}
        else:
            return {'points': points}


@viztype
class ROI(Base):

    _name = 'roi'

    @staticmethod
    def clean(x, y, timeseries, clrs=None):

        points = vecs_to_points(x, y)
        timeseries = array_to_lines(timeseries)
        if clrs is not None:
            clrs = check_colors(clrs)
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
            clrs = check_colors(clrs)
            if clrs.shape[1] == 1:
                outdict['labels'] = clrs
            else:
                outdict['colors'] = clrs

        if imagedata is not None:
            images = array_to_im(imagedata)
            outdict['images'] = images

        return outdict
