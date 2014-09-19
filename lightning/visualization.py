import requests
import os
import time
import json


class Visualization(object):


    def __init__(self, session=None, json=None):
        self.session = session
        self.id = json.get('id')


    def append_image(self, image):
        url = self.session.host + '/sessions/' + str(self.session.id) + '/visualizations/' + str(self.id) + '/data/images'
        files = {'file': image}
        return requests.post(url, files=files)


    def append_data(self, data=None, field=None):
        payload = {'data': data}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}        
        url = self.session.host + '/sessions/' + str(self.session.id) + '/visualizations/' + str(self.id) + '/data/'
        if field:
            url += field
        return requests.post(url, data=json.dumps(payload), headers=headers)


    def update_data(self, data=None, field=None):
        payload = {'data': data}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}        
        url = self.session.host + '/sessions/' + str(self.session.id) + '/visualizations/' + str(self.id) + '/data/'
        if field:
            url += field
        return requests.put(url, data=json.dumps(payload), headers=headers)


        
    @classmethod
    def create(cls, session=None, data=None, images=None, type=None):
        url = session.host + '/sessions/' + str(session.id) + '/visualizations'

        if not images:
            payload = {'data': data, 'type': type}
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            
            r = requests.post(url, data=json.dumps(payload), headers=headers)

            if not r.status_code == requests.codes.ok:
                raise Exception('Problem uploading data')

            viz = cls(session=session, json=r.json())


        else:
            if not type:
                if len(images) > 1:
                    type = 'volume'
                else:
                    type = 'image'


            first_image, remaining_images = images[0], images[1:]
            files = {'file': first_image}
            
            r = requests.post(url, files=files, data={'type': type})

            if not r.status_code == requests.codes.ok:
                raise Exception('Problem uploading images')

            viz = Visualization(session=session, json=r.json())
            for image in remaining_images:
                viz.append_image(image)

        return viz
