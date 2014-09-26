import requests
import os
import time
import json
from visualization import Visualization

class Session(object):
    name = None
    visualizations = []

    def __init__(self, host=None, id=None, json=None):
        self.host = host
        self.id = id
        if json:
            self.id = json.get('id')
            self.name = json.get('name')

    def __str__(self):
        if self.name:
            return self.name
        return str(self.id)


    def create_visualization(self, data=None, images=None, type=None, ipython=False):
        viz = Visualization.create(session=self, data=data, images=images, type=type, ipython=ipython)
        self.visualizations.append(viz)
        return viz

    @classmethod
    def create(cls, host, name=None):
        url = host + '/sessions/'

        payload = {}
        if name:
            payload = {'name': name}

        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

        r = requests.post(url, data=json.dumps(payload), headers=headers)
        return cls(host=host, json=r.json())
