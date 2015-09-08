import requests
import json
import webbrowser
import random
import string

class Visualization(object):

    def __init__(self, session=None, json=None, auth=None):

        self.session = session
        self.id = json.get('id')
        self.auth = auth

        if self.session.lgn.ipython_enabled:
            from IPython.kernel.comm import Comm
            self.comm = Comm('lightning', {'id': self.id})
            self.comm_handlers = {}
            self.comm.on_msg(self._handle_comm_message)

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

    def get_public_link(self):
        return self.get_permalink() + '/public/'

    def get_embed_link(self):
        return self._format_url(self.get_permalink() + '/embed')

    def get_html(self):
        r = requests.get(self.get_embed_link(), auth=self.auth)
        return r.text

    def open(self):
        webbrowser.open(self.get_public_link())

    def delete(self):
        url = self.get_permalink()
        return requests.delete(url)

    def on(self, event_name, handler):

        if self.session.lgn.ipython_enabled:
            self.comm_handlers[event_name] = handler

        else:
            raise Exception('The current implementation of this method is only compatible with IPython.')

    def _handle_comm_message(self, message):
        # Parsing logic taken from similar code in matplotlib
        message = json.loads(message['content']['data'])

        if message['type'] in self.comm_handlers:
            self.comm_handlers[message['type']](message['data'])

    @classmethod
    def _create(cls, session=None, data=None, images=None, type=None, options=None, description=None):

        if options is None:
            options = {}

        url = session.host + '/sessions/' + str(session.id) + '/visualizations'

        if not images:
            payload = {'data': data, 'type': type, 'options': options}
            if description:
                payload['description'] = description
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            r = requests.post(url, data=json.dumps(payload), headers=headers, auth=session.auth)
            if r.status_code == 404:
                raise Exception(r.text)
            elif not r.status_code == requests.codes.ok:
                raise Exception('Problem uploading data')

            viz = cls(session=session, json=r.json(), auth=session.auth)

        else:
            first_image, remaining_images = images[0], images[1:]
            files = {'file': first_image}
            payload = {'type': type, 'options': json.dumps(options)}
            if description:
                payload['description'] = description
            r = requests.post(url, files=files, data=payload, auth=session.auth)
            if r.status_code == 404:
                raise Exception(r.text)
            elif not r.status_code == requests.codes.ok:
                raise Exception('Problem uploading images')

            viz = cls(session=session, json=r.json(), auth=session.auth)
            for image in remaining_images:
                viz._append_image(image)

        return viz

class VisualizationLocal(object):

    def __init__(self, html):
        self._html = html

    @classmethod
    def _create(cls, data=None, images=None, type=None, options=None):

        import base64
        from jinja2 import Template, escape

        t = Template(cls.load_template())

        options = escape(json.dumps(options))
        random_id = 'A' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(9))
        fields = {'viz': type, 'options': options, 'viz_id': random_id}

        if images:
            bytes = ['data:image/png;base64,' + base64.b64encode(img) + ',' for img in images]
            fields['images'] = escape(json.dumps(bytes))
        else:
            data = escape(json.dumps(data))
            fields['data'] = data

        html = t.render(**fields)
        viz = cls(html)
        return viz

    def get_html(self):
        """
        Return html for this local visualization.

        Assumes that Javascript has already been embedded,
        to be used for rendering in notebooks.
        """
        return self._html

    def save_html(self, filename=None, overwrite=False):
        """
        Save self-contained html to a file.

        Parameters
        ----------
        filename : str
            The filename to save to
        """

        if filename is None:
            raise ValueError('Please provide a filename, e.g. viz.save_html(filename="viz.html").')

        import os
        base = self._html
        js = self.load_embed()
        if os.path.exists(filename):
            if overwrite is False:
                raise ValueError("File '%s' exists. To ovewrite call save_html with overwrite=True."
                                 % os.path.abspath(filename))
            else:
                os.remove(filename)
        with open(filename, "wb") as f:
            f.write(base.encode('utf-8'))
            f.write('<script>' + js.encode('utf-8') + '</script>')

    @staticmethod
    def load_template():
        import os
        location = os.path.join(os.path.dirname(__file__), 'lib/template.html')
        return open(location).read()

    @staticmethod
    def load_embed():
        import os
        location = os.path.join(os.path.dirname(__file__), 'lib/embed.js')
        import codecs
        return codecs.open(location, "r", "utf-8").read()


