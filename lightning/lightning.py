import requests
import os
import time
import json
from session import Session


class Lightning(object):
    _instance = None
    
    host = "http://lightning.mathisonian.com"

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


    def plot(self, data=[], type=None, colors=None):
        return self.session.create_visualization(data=data, type=type)
