import requests
import os
import time
import json


class Visualization(object):


    def __init__(self, session=None, json=None):
        self.session = session
        self.id = json.get('id')


    def append_image(self, image):
        url = self.session.host + '/sessions/' + str(self.session.id) + '/visualizations' + str(self.id) + '/data/images'
        files = {'file': image}
        r = requests.post(url, files=files)


    def append_data(self, data):
        pass

    def update_data(self, data):
        pass