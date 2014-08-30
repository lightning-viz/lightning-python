import requests
import os
import time
import json
from visualization import Visualization

class Session(object):
    name = None

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


    def create_visualization(self, data=None, images=None, type=None):
        viz = None
        url = self.host + '/sessions/' + str(self.id) + '/visualizations'

        if not images:
            payload = {'data': data, 'type': type}
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            
            r = requests.post(url, data=json.dumps(payload), headers=headers)
            viz = Visualization(session=self, json=r.json())
        
        else:
            first_image, remaining_images = images[0], images[1:]
            files = {'file': firstImage}
            
            r = requests.post(url, files=files, data={'type': type})
            viz = Visualization(session=self, json=r.json())
            for image in remaining_images:
                viz.append_image(image)

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
