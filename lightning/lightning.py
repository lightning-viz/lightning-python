import requests
import os
import time
import json
from session import Session




class Lightning(object):
    _instance = None
    
    host = "http://lightning.mathisonian.com"

    data_dict_inputs = {
        'points': ['x', 'y']
    }

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Lightning, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance

    def create_session(self, name=None):
        self.session = Session.create(self.host, name=name)
        return self.session

    def use_session(self, session_id):
        self.session = Session(host=self.host, id=session_id)
        return self.session



    def _ensure_dict_or_list(self, x):
        if isinstance(x, dict):
            return x

        if isinstance(x, list):
            return x

        try:
            # Convert Numpy arrays to lists
            return x.toList()
        except Exception:
            pass


        # add other data type conversions here

        raise Exception("Could not convert to correct data type")


    def _check_unkeyed_arrays(self, key, val):

        if not key in self.data_dict_inputs:
            return val


        if not isinstance(val, list):
            raise Exception("Must provide a list")


        if len(val) == 0:
            return val

        
        if isinstance(val[0], dict) and isinstance(val[-1], dict):
            return val

        
        if isinstance(val[0], list) and isinstance(val[-1], list):
            # if both the first and last elements are lists
            out = []
            mapping = self.data_dict_inputs[key]
            for l in val:
                out.append(dict(zip(mapping, l)))

            return out



    def plot(self, type=None, **kwargs):
        if not type:
            raise Exception("Must provide a plot type")

        if 'data' in kwargs:
            data = kwargs['data']
            return self.session.create_visualization(data=self._ensure_dict_or_list(data), type=type)

        else:
            data = {}
            for key in kwargs:
                d = self._ensure_dict_or_list(kwargs[key])
                data[key] = self._check_unkeyed_arrays(key, d)

            return self.session.create_visualization(data=data, type=type)

