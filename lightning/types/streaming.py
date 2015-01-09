from lightning.types.base import Base
from lightning.types.decorators import viztype
from lightning.types.utils import array_to_lines


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
