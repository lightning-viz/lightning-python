import requests
import json
import webbrowser


class Visualization(object):

    def __init__(self, session=None, json=None, auth=None):
        self.session = session
        self.id = json.get('id')
        self.auth = auth

    def _format_url(self, url):
        if not url.endswith('/'):
            url += '/'
        try:
            from urllib.parse import quote
        except ImportError:
            from urllib import quote
        return url + '?host=' + quote(self.session.host)

    def _update_image(self, image):
        url = self.session.host + '/sessions/' + str(self.session.id) + '/visualizations/' + str(self.id) + '/data/images'
        url = self._format_url(url)
        files = {'file': image}
        return requests.put(url, files=files, data={'type': 'image'}, auth=self.auth)

    def _append_image(self, image):
        url = self.session.host + '/sessions/' + str(self.session.id) + '/visualizations/' + str(self.id) + '/data/images'
        url = self._format_url(url)
        files = {'file': image}
        return requests.post(url, files=files, data={'type': 'image'}, auth=self.auth)

    def _append_data(self, data=None, field=None):
        payload = {'data': data}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}        
        url = self.session.host + '/sessions/' + str(self.session.id) + '/visualizations/' + str(self.id) + '/data/'
        if field:
            url += field

        url = self._format_url(url)
        return requests.post(url, data=json.dumps(payload), headers=headers, auth=self.auth)

    def _update_data(self, data=None, field=None):
        payload = {'data': data}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}        
        url = self.session.host + '/sessions/' + str(self.session.id) + '/visualizations/' + str(self.id) + '/data/'
        if field:
            url += field

        url = self._format_url(url)
        return requests.put(url, data=json.dumps(payload), headers=headers, auth=self.auth)

    def get_permalink(self):
        return self.session.host + '/visualizations/' + str(self.id)

    def get_embed_link(self):
        return self._format_url(self.get_permalink() + '/embed')

    def get_html(self):
        r = requests.get(self.get_embed_link(), auth=self.auth)
        return r.text

    def open(self):
        webbrowser.open(self.session.host + '/visualizations/' + str(self.id) + '/')

    def delete(self):
        url = self.get_permalink()
        return requests.delete(url)

    @classmethod
    def create(cls, session=None, data=None, images=None, type=None, options=None):

        if options is None:
            options = {}

        url = session.host + '/sessions/' + str(session.id) + '/visualizations'

        if not images:
            payload = {'data': data, 'type': type, 'opts': options}
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

            r = requests.post(url, data=json.dumps(payload), headers=headers, auth=session.auth)

            if not r.status_code == requests.codes.ok:
                raise Exception('Problem uploading data')

            viz = cls(session=session, json=r.json(), auth=session.auth)

        else:

            first_image, remaining_images = images[0], images[1:]
            files = {'file': first_image}
            
            r = requests.post(url, files=files, data={'type': type, 'opts': options}, auth=session.auth)

            if not r.status_code == requests.codes.ok:
                raise Exception('Problem uploading images')

            viz = cls(session=session, json=r.json(), auth=session.auth)
            for image in remaining_images:
                viz._append_image(image)

        return viz

