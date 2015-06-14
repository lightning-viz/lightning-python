import requests
import json
from .visualization import Visualization
import webbrowser


class Session(object):
    name = None
    visualizations = []

    def __init__(self, lgn=None, id=None, json=None):
        self.lgn = lgn
        self.host = lgn.host
        self.auth = lgn.auth
        self.id = id

        if json:
            self.id = json.get('id')
            self.name = json.get('name')

    def __str__(self):
        if self.name:
            return self.name
        return str(self.id)

    def __repr__(self):
        if self.name:
            return "Session number: " + str(self.id) + ", name: " + self.name
        return "Session number: " + str(self.id)

    def create_visualization(self, data=None, images=None, type=None):
        viz = Visualization.create(session=self, data=data, images=images, type=type)
        self.visualizations.append(viz)
        return viz

    def open(self):
        webbrowser.open(self.host + '/sessions/' + str(self.id) + '/feed/')

    @classmethod
    def create(cls, lgn, name=None):
        url = lgn.host + '/sessions/'

        payload = {}
        if name:
            payload = {'name': name}

        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

        r = requests.post(url, data=json.dumps(payload), headers=headers, auth=lgn.auth)
        return cls(lgn=lgn, json=r.json())
