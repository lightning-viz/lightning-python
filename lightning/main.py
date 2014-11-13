import requests
import os
import time
import json
from numpy import ndarray, asarray, vstack, transpose, nonzero, \
    concatenate, atleast_2d, ones, int, zeros, hstack, newaxis
from session import Session
from visualization import Visualization
from matplotlib.pyplot import imsave
from matplotlib.pyplot import cm
import io

class Lightning(object):

    def __init__(self, host="http://localhost:3000", ipython=False):
        self.host = host

        if ipython:
            self.enable_ipython()

    def enable_ipython(self, **kwargs):
        '''
        ipython code inspired by code powering similar functionality in mpld3:
        https://github.com/jakevdp/mpld3/blob/master/mpld3/_display.py#L357
        '''

        from IPython.core.getipython import get_ipython
        ip = get_ipython()
        formatter = ip.display_formatter.formatters['text/html']
        formatter.for_type(Visualization,
                           lambda viz, kwds=kwargs: viz.get_html())

    def disable_ipython(self):
        from IPython.core.getipython import get_ipython
        ip = get_ipython()
        formatter = ip.display_formatter.formatters['text/html']
        formatter.type_printers.pop(Visualization, None)

    def create_session(self, name=None):
        self.session = Session.create(self.host, name=name)
        return self.session

    def use_session(self, session_id):
        self.session = Session(host=self.host, id=session_id)
        return self.session

    def plot(self, type=None, **kwargs):

        from lightning.types.base import Base
        
        viz = Base.baseplot(self.session, type=type, **kwargs)
        self.session.visualizations.append(viz)
        return viz




        

